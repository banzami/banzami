# BANZA Federation Conformance Model

**Document ID:** FEDERATION-CONFORMANCE-DESIGN-001  
**Date:** 2026-05-31  
**Status:** Canonical — conformance architecture. Executable once the runner implements this spec.  
**Authority:** ADR-026, FEDERATION_INVARIANTS.md, FEDERATION_CONTRACT_SURFACE.md, FEDERATION_PROTOCOL_FLOW.md

---

## Purpose

This document defines the executable conformance model for L3 Federation Certification. It maps every federation requirement to at least one test, defines the nine test suites, specifies pass/fail semantics, and establishes what makes a certification decision unambiguous.

After this document: implementation of the conformance runner can begin without architectural ambiguity.

---

## 1. Conformance Architecture

### 1.1 Two-Operator Problem

L0–L2 conformance tests a single operator in isolation: `runner → Operator A`. Federation conformance must test cross-operator behavior: `runner → Operator A ↔ Operator B`. This requires a new runner invocation mode.

```
# L0-L2 mode (existing)
banza-conformance --operator-a https://api.operator-a.example --level 2

# L3 federation mode (new)
banza-conformance --federation \
  --operator-a https://api.operator-a.example \
  --level 3
```

In federation mode, the runner embeds a **Simulated Operator B** — a fully controlled BANZA-compliant stub that:
- Issues valid trust-verified responses
- Records all interactions for evidence collection
- Can be configured to inject failures on demand
- Uses the test BANZA root (separate from production)

### 1.2 Test Environment Separation

**Production BANZA root ≠ Test BANZA root.**

The conformance runner generates its own ed25519 keypair at startup (the "test root"). This keypair:
- Issues certificates to both Operator A (the operator under test) and Simulated Operator B
- Serves a test BRL endpoint
- Is NOT the BANZA production signing key

This ensures:
- Conformance tests never depend on BANZA production infrastructure
- Tests can inject expired, revoked, and tampered certificates without touching real trust state
- Any operator can run a conformance test against themselves at any time

### 1.3 Suite Execution Order

Suites run in dependency order. A failing early suite may block later suites from producing meaningful results.

```
FED-CERT   (certificate validation)
    ↓
FED-DISC   (discovery and manifest)
    ↓
FED-TRUST  (trust establishment)
    ↓
FED-ROUTE  (routing negotiation)
    ↓
FED-EXEC   (transfer execution)
    ↓
FED-OBL    (obligation creation)
    ↓
FED-EVT    (event emission)
    ↓
FED-SETTLE (netting and settlement)
    ↓
FED-FAIL   (failure and recovery)
```

FED-FAIL may be run in parallel with FED-SETTLE if both have independent fixture sets.

---

## 2. Suite Registry

| Suite ID | Name | Cases | Blocking | Description |
|----------|------|-------|----------|-------------|
| FED-CERT | Certificate Validation | 11 | Yes | Operator certificate schema, signature, expiry, binding |
| FED-DISC | Discovery and Manifest | 8 | Yes | Federation manifest extension fields, well-known endpoints |
| FED-TRUST | Trust Establishment | 9 | Yes | All 9 trust protocol steps; BRL handling |
| FED-ROUTE | Routing Negotiation | 12 | Yes | Routing request/response; idempotency; rejection codes |
| FED-EXEC | Transfer Execution | 8 | Yes | Acceptance semantics; ledger entries; atomicity |
| FED-OBL | Obligation Lifecycle | 7 | Yes | Obligation creation, signature, state machine |
| FED-EVT | Event Emission | 6 | No | Federation event schema and trace propagation |
| FED-SETTLE | Settlement | 10 | No | Netting, net position, bank settlement, reconciliation |
| FED-FAIL | Failure Recovery | 8 | No | Retry behavior, crash recovery, revocation mid-flight |

**Blocking:** A FAIL in a blocking suite prevents certification regardless of other suite results.  
**Non-blocking:** A FAIL in a non-blocking suite is noted but does not prevent certification if all blocking suites pass. (FED-EVT, FED-SETTLE, FED-FAIL failures produce a certification with conditions for remediation.)

---

## 3. Requirement → Test Coverage Map

Every requirement from every federation artifact maps to at least one test. No requirement is untestable.

### 3.1 ADR-026 Invariants

| Invariant | Test(s) | Suite |
|-----------|---------|-------|
| INV-TRUST-001 (cert signature) | FED-CERT-002, FED-TRUST-002 | CERT, TRUST |
| INV-TRUST-002 (cert expiry) | FED-CERT-003, FED-CERT-007, FED-CERT-008, FED-TRUST-003 | CERT, TRUST |
| INV-TRUST-003 (BRL = reject) | FED-TRUST-005, FED-CERT-009 | TRUST, CERT |
| INV-TRUST-004 (fed flag needs cert) | FED-DISC-007 | DISC |
| INV-TRUST-005 (BRL must be signed) | FED-TRUST-003 | TRUST |
| INV-TRUST-006 (BRL max 6h) | FED-TRUST-009, FED-FAIL-006 | TRUST, FAIL |
| INV-TRUST-007 (key rotation auth) | FED-CERT-010 | CERT |
| INV-FED-001 (trace_id invariant) | FED-ROUTE-003, FED-OBL-003, FED-EVT-005 | ROUTE, OBL, EVT |
| INV-FED-002 (obligation per routing) | FED-OBL-001, FED-OBL-004, FED-FAIL-005 | OBL, FAIL |
| INV-FED-003 (fed flag ⟹ endpoint) | FED-DISC-005 | DISC |
| INV-FED-004 (routing idempotency) | FED-ROUTE-004, FED-FAIL-001 | ROUTE, FAIL |
| INV-FED-005 (value conservation) | FED-OBL-002, FED-EXEC-002 | OBL, EXEC |
| INV-FED-006 (cert must expire) | FED-CERT-007 | CERT |
| INV-FED-007 (revoked = rejected) | FED-TRUST-005, FED-CERT-009 | TRUST, CERT |
| INV-FED-LEDGER-001 (cross-op double-entry) | FED-EXEC-002, FED-SETTLE-004 | EXEC, SETTLE |
| INV-FED-LEDGER-002 (integer arithmetic) | FED-ROUTE-010 | ROUTE |
| INV-FED-IDEM-001 (global unique IDs) | FED-ROUTE-004, FED-ROUTE-011 | ROUTE |
| INV-FED-RECON-001 (cross-op reconcilability) | FED-SETTLE-006, FED-SETTLE-007 | SETTLE |

### 3.2 Contract Requirements

| Contract | Requirement | Test(s) |
|----------|-------------|---------|
| operator-certificate | Certificate at well-known URL | FED-CERT-001 |
| operator-certificate | Signature verifies | FED-CERT-002 |
| operator-certificate | Not expired | FED-CERT-003 |
| operator-certificate | operator_id format | FED-CERT-004 |
| operator-certificate | public_key format | FED-CERT-005 |
| operator-certificate | issuer == "BANZA" | FED-CERT-006 |
| operator-certificate | 90-day max for L3+ | FED-CERT-007 |
| federation-manifest | supports_federation | FED-DISC-002 |
| federation-manifest | cross_operator_routing | FED-DISC-003 |
| federation-manifest | certificate_url accessible | FED-DISC-004 |
| federation-manifest | interop_endpoint accessible | FED-DISC-005 |
| federation-manifest | supported_currencies non-empty | FED-DISC-006 |
| federation-manifest | INV-TRUST-004 enforcement | FED-DISC-007 |
| federation-routing | Valid request accepted | FED-ROUTE-001 |
| federation-routing | routing_request_id echo | FED-ROUTE-002 |
| federation-routing | trace_id echo | FED-ROUTE-003 |
| federation-routing | Idempotency | FED-ROUTE-004 |
| federation-routing | Signature required | FED-ROUTE-005 |
| federation-routing | to_operator_id check | FED-ROUTE-006 |
| federation-routing | Recipient resolution | FED-ROUTE-007 |
| federation-routing | Currency check | FED-ROUTE-008 |
| federation-routing | interop_transfer_id format | FED-ROUTE-009 |
| federation-routing | Positive amount | FED-ROUTE-010 |
| federation-routing | Duplicate ID diff content | FED-ROUTE-011 |
| federation-routing | Suspended wallet | FED-ROUTE-012 |
| federation-obligation | Obligation created | FED-OBL-001 |
| federation-obligation | Amount equality | FED-OBL-002 |
| federation-obligation | trace_id propagation | FED-OBL-003 |
| federation-obligation | Uniqueness | FED-OBL-004 |
| federation-obligation | obligor_signature | FED-OBL-005 |
| federation-obligation | State transitions | FED-OBL-006 |
| federation-obligation | Settled fields | FED-OBL-007 |
| federation-event | routing.accepted emitted | FED-EVT-001 |
| federation-event | payment.initiated emitted | FED-EVT-002 |
| federation-event | payment.completed emitted | FED-EVT-003 |
| federation-event | obligation.recorded emitted | FED-EVT-004 |
| federation-event | trace_id propagation | FED-EVT-005 |
| federation-event | Schema validity | FED-EVT-006 |

### 3.3 Protocol Flow Requirements

| Phase | Behavioral Requirement | Test(s) |
|-------|----------------------|---------|
| Phase 1 | Manifest fetched and validated | FED-DISC-001 |
| Phase 1 | Currency checked against supported list | FED-DISC-006 |
| Phase 2 | All 9 trust steps pass | FED-TRUST-001 |
| Phase 2 | BRL fetched and verified | FED-TRUST-003 |
| Phase 3 | routing_request_id assigned before send | FED-ROUTE-001 |
| Phase 3 | Same ID on retry | FED-ROUTE-004, FED-FAIL-001 |
| Phase 3 | Bidirectional trust verification | FED-ROUTE-005 |
| Phase 4 | Operator B credits payee on acceptance | FED-EXEC-001 |
| Phase 4 | Ledger entries correct on both sides | FED-EXEC-002 |
| Phase 5 | Operator A debit + obligation atomic | FED-EXEC-005, FED-OBL-001 |
| Phase 6 | Net position computed independently | FED-SETTLE-002 |
| Phase 6 | Both operators agree before settlement | FED-SETTLE-003 |
| Phase 7 | F-101 retry with same ID | FED-FAIL-001 |
| Phase 7 | F-402 crash recovery | FED-FAIL-005 |
| Phase 8 | Revocation before routing → abort | FED-TRUST-005 |
| Phase 8 | Revocation mid-flight → obligation survives | FED-FAIL-007 |
| Phase 9 | Obligation cross-reference | FED-SETTLE-006 |
| Phase 9 | Trace cross-check | FED-SETTLE-007 |
| BC-001 | No debit without acceptance | FED-EXEC-003 |
| BC-003 | Debit and obligation atomic | FED-EXEC-005 |
| BC-004 | Acceptance irrevocable | FED-EXEC-007 |
| BC-005 | Same routing_request_id on retry | FED-ROUTE-004 |
| BC-010 | Amount immutability | FED-OBL-002 |

### 3.4 Failure Scenario Requirements

| Failure | Test |
|---------|------|
| F-101 (timeout + retry) | FED-FAIL-001 |
| F-102 (unparseable response) | FED-FAIL-002 |
| F-201 (cert expired) | FED-CERT-008, FED-TRUST-003 |
| F-202 (invalid sig) | FED-CERT-002 (negative), FED-TRUST-002 |
| F-203 (BRL hit) | FED-TRUST-005, FED-CERT-009 |
| F-204 (A cert rejected by B) | FED-FAIL-004 |
| F-205 (BRL unavailable) | FED-TRUST-008, FED-FAIL-006 |
| F-301 (recipient not found) | FED-ROUTE-007 |
| F-302 (wallet suspended) | FED-ROUTE-012 |
| F-303 (duplicate diff content) | FED-ROUTE-011 |
| F-401 (B accepts but ledger fails) | FED-EXEC-006 |
| F-402 (A crash post-accept) | FED-FAIL-005 |
| F-404 (obligation amount mismatch) | FED-FAIL-008 |
| F-501 (netting disagreement) | FED-SETTLE-009 |
| F-502 (bank reject) | FED-SETTLE-010 |
| F-601 (clock skew) | FED-CERT-003 (clock-controlled) |
| F-602 (BRL extended outage) | FED-TRUST-009 |
| F-604 (unknown issuer_key_id) | FED-CERT-011 |

---

## 4. L3 Certification Decision Rules

### 4.1 Certification Granted

L3 Federation Certification is granted when ALL of the following hold:

1. All blocking suite results are PASS (FED-CERT through FED-OBL)
2. FED-EVT: all 6 cases pass
3. FED-SETTLE: cases 001–008 pass (010 allowed as WARNING if zero-net scenario not tested)
4. FED-FAIL: cases 001, 004, 005 pass (mandatory recovery tests)
5. No CRITICAL invariant violation in any suite
6. Evidence package is complete and passes automated verification

### 4.2 Certification Denied

Certification is denied if any of the following:

- Any FAIL in FED-CERT, FED-DISC, or FED-TRUST
- FED-ROUTE: any FAIL in cases 001–009 (core routing correctness)
- FED-EXEC: any FAIL in cases 001–005
- FED-OBL: any FAIL in cases 001–005
- Any CRITICAL invariant violation (INV-TRUST-001, INV-FED-001, INV-FED-002, INV-FED-004, INV-FED-005)
- Evidence package missing required items (see FEDERATION_CERTIFICATION_EVIDENCE_MODEL.md)

### 4.3 Conditional Certification

Conditional certification (granted with remediation timeline):

- FED-EVT cases 002 or 003 fail (event emission — operational, not financial)
- FED-SETTLE cases 009 or 010 fail (netting edge cases)
- FED-FAIL cases 002, 003, 006, 007, 008 fail (non-critical recovery paths)

Conditional certification is valid for 30 days. Remediation must be demonstrated before full certification.

---

## 5. Test ID Namespace

All federation test IDs follow the pattern: `FED-<SUITE>-<NNN>`

| Suite | ID Range | Count |
|-------|----------|-------|
| FED-CERT | FED-CERT-001 to FED-CERT-011 | 11 |
| FED-DISC | FED-DISC-001 to FED-DISC-008 | 8 |
| FED-TRUST | FED-TRUST-001 to FED-TRUST-009 | 9 |
| FED-ROUTE | FED-ROUTE-001 to FED-ROUTE-012 | 12 |
| FED-EXEC | FED-EXEC-001 to FED-EXEC-008 | 8 |
| FED-OBL | FED-OBL-001 to FED-OBL-007 | 7 |
| FED-EVT | FED-EVT-001 to FED-EVT-006 | 6 |
| FED-SETTLE | FED-SETTLE-001 to FED-SETTLE-010 | 10 |
| FED-FAIL | FED-FAIL-001 to FED-FAIL-008 | 8 |
| **Total** | | **79** |

---

## 6. Compliance Assertion

> After FEDERATION-CONFORMANCE-DESIGN-001, every L3 federation requirement has: a contract, an invariant, a test ID, a fixture reference, an evidence requirement, and explicit pass/fail criteria.
>
> Implementation of the conformance runner can begin. No architectural ambiguity remains.
