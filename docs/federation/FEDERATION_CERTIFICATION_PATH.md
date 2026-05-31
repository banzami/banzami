# BANZA Federation Certification Path

**Audit ID:** BANZA-FEDERATION-READINESS-AUDIT-001  
**Date:** 2026-05-31

---

## The Certification Authority Model

```
BANZA defines certification requirements
    ↓
BanzAI evaluates operator compliance against those requirements
    ↓
Operators demonstrate compliance and receive certification from BANZA
```

This chain applies to federation certification identically to L0–L2. BANZA issues L3 certificates. BanzAI runs the evaluation. Operators pass or fail.

---

## Current L3 Definition (Audit Finding)

Per `BANZA_CERTIFICATION.md` (lines 123–136), L3 currently requires:
- All L0–L2 requirements
- `payout.batch` — batch payouts to bank accounts
- `reconciliation` — automated ledger reconciliation

**L3 is NOT currently federation certification.** L3 is "full single-operator capability." The federation requirement appears at **L4** (`federation_ready` capability). This is a naming issue — the certification level descriptions need to be revised.

**Recommended revision:**
- L3: "Settlement Operator" (current definition — payouts + reconciliation)
- L4: "Federation Operator" (new — cross-operator routing + settlement)
- L5: "Infrastructure Operator" (new — acquiring + federation authority node)

*This revision requires an ADR. No change is made here — this is an audit finding.*

---

## L3 Federation Certification Requirements

The following is the **target state** for what L3 Federation Certification should require when federation is ready.

### Requirements Table

| Requirement | Protocol Artifact | Contract | Conformance Suite | Evidence |
|-------------|------------------|----------|-------------------|---------|
| **FED-L3-001** Operator identity | `operator_id` in manifest | `contracts/federation/operator-certificate.json` | FED-001 — manifest with certificate | Valid manifest + valid certificate |
| **FED-L3-002** Manifest signing | ed25519 signature | `contracts/federation/federation-trust.json` | FED-002 — signature verification | Signature verifies against BANZA public key |
| **FED-L3-003** Capability declaration | `supports_federation: true` in manifest | `conformance/capabilities/schema.json` | CAP-FED-001 | Manifest declares federation capability |
| **FED-L3-004** Federation endpoint | `GET /federation/route` available | `contracts/federation/federation-routing.json` | FED-003 — routing request | Returns valid routing response |
| **FED-L3-005** Trace propagation | `trace_id` in all federation artifacts | `contracts/events/envelope.schema.json` | FED-004 — trace consistency | Federation transaction carries same trace_id across both operators |
| **FED-L3-006** Obligation recording | `POST /federation/obligations` | `contracts/federation/federation-obligation.json` | FED-005 — obligation creation | Obligation created per cross-operator payment |
| **FED-L3-007** Cross-operator payment end-to-end | Full flow: Operator A → Operator B | All above | FED-006 — end-to-end | Consumer on A pays merchant on B; both ledgers correct |

---

## Minimum Conformance Suite for L3 Federation

The minimum set of test vectors required to certify one operator at L3:

```
Suite: federation-core

FED-001: Operator manifest is valid and signed
  - GET /.well-known/banza/operator.json → 200, valid schema
  - Certificate signature verifies against BANZA public key
  - Certification level ≥ 3 in certificate

FED-002: Operator certificate is present and valid
  - GET /.well-known/banza/certificate.json → 200
  - Certificate not expired
  - operator_id matches manifest

FED-003: Federation capability declared
  - manifest.capabilities.supports_federation == true
  - manifest.capabilities.cross_operator_routing == true

FED-004: Routing endpoint accepts federation request
  - POST /federation/route with valid OperatorRouteRequest → 200
  - Response includes interop_transfer_id
  - trace_id in response matches request

FED-005: Obligation created for accepted routing request
  - GET /federation/obligations → includes obligation from FED-004
  - Obligation: from_operator_id, to_operator_id, amount, trace_id

FED-006: Cross-operator payment completes correctly
  - End-to-end flow: Operator A routes to Operator B
  - Operator B ledger shows CREDIT for correct amount
  - Operator A ledger shows DEBIT
  - INV-FED-001: same trace_id in both operators
  - INV-FED-005: total value conserved (no creation, no destruction)
```

---

## Cross-Operator Certification (Interoperability Test)

L3 federation certification requires testing **two operators together**. This is a fundamentally different conformance model from L0–L2 (which tests a single operator in isolation).

### The Interoperability Problem

Single-operator conformance: `run_tests(Operator_A_URL)` → pass/fail

Cross-operator conformance: `run_tests(Operator_A_URL, Operator_B_URL)` → pass/fail

The conformance runner (`tools/banza-conformance/run.py`) is currently single-URL. Federation conformance requires a new invocation mode:

```bash
# Proposed CLI (not yet implemented)
python3 tools/banza-conformance/run.py \
  --federation \
  --operator-a https://api.operator-a.example \
  --operator-b https://api.operator-b.example \
  --level 3
```

BanzAI's role here: run the federation conformance suite against two operators and report the interoperability result. BANZA issues L3 certification if both operators pass.

---

## Certification Path — Minimum Sequence

The **smallest possible implementation sequence** to achieve L3 Federation Certification without introducing centralization:

```
Phase 1 — ADR (governance prerequisite)
  ADR-026: Federation Trust Model
    → Decides: PKI approach, certificate format, revocation strategy
  ADR-027: Federation Wire Protocol
    → Decides: HTTP-based operator-to-operator protocol, authentication
  ADR-028: Certification Level Revision
    → Decides: L3 = settlement operator, L4 = federation operator, L5 = infrastructure

Phase 2 — Contracts (protocol specification)
  contracts/federation/operator-certificate.json
  contracts/federation/federation-routing.json
  contracts/federation/federation-obligation.json
  contracts/federation/federation-event.json
  contracts/federation/federation-trust.json

Phase 3 — Kernel (Rust — banza-capabilities, banza-routing, banza-settlement)
  Implement manifest signing (ed25519, banza-capabilities crate)
  Implement InteropRoutingEngine trait (banza-routing crate)
  Implement InteropObligation + CrossOperatorSettlementProvider (banza-settlement crate)

Phase 4 — Conformance
  conformance/federation/suite.json
  conformance/vectors/federation-routing.json
  conformance/vectors/federation-settlement.json
  conformance/vectors/federation-discovery.json

Phase 5 — Reference operator
  Enable cross_operator_routing in sandbox manifest
  Implement /federation/* endpoints in reference/sandbox-operator
  Run federation conformance: Sandbox A ↔ Sandbox B

Phase 6 — Certification issuance
  BANZA issues first L3 certificate to passing operators
  BanzAI federation intelligence module can evaluate L3 readiness for any operator
```

**Total estimated scope:** 5 ADRs, 5 new contracts, 3 crate extensions, 1 new conformance suite, 1 reference implementation extension, 1 conformance runner extension.

---

## BanzAI's Role in Federation Certification

| Task | Who Does It | Notes |
|------|-------------|-------|
| Define certification requirements | BANZA (ADRs, contracts) | Protocol authority |
| Issue certification artifacts | BANZA | Trust authority |
| Evaluate operator readiness | BanzAI | Runs conformance suite |
| Run cross-operator conformance | BanzAI | Requires two-operator invocation mode |
| Verify certificate signatures | BanzAI + operators | Cryptographic verification |
| Maintain federation topology map | BanzAI | Protocol Graph capability |
| Report on federation compatibility | BanzAI | Federation Intelligence capability |
| Approve or reject certification | BANZA only | Never BanzAI |

---

## Final Answer: What is the minimum to achieve L3 Federation Certification?

**Minimum protocol artifacts:**
1. ADR-026 (trust model decision)
2. `contracts/federation/operator-certificate.json`
3. `contracts/federation/federation-routing.json`
4. `contracts/federation/federation-obligation.json`
5. Manifest signing implementation in `banza-capabilities`
6. `InteropRoutingEngine` skeleton in `banza-routing`
7. `InteropObligation` struct in `banza-settlement`
8. `conformance/federation/suite.json` with FED-001 through FED-006
9. Two operators passing FED-001 through FED-006

**The one prerequisite that blocks everything:** A decision on the trust model (GAP-001). Without a trust model, manifests cannot be signed, certificates cannot be issued, and trust cannot be established between operators. The trust model ADR unlocks all other work.
