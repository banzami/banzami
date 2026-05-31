# BANZA Federation Gap Analysis

**Audit ID:** BANZA-FEDERATION-READINESS-AUDIT-001  
**Date:** 2026-05-31

---

## Top 10 Missing Protocol Artifacts

Ranked by blocking impact on L3 certification:

### GAP-001 — Federation Trust Infrastructure (CRITICAL)
**What is missing:** No PKI for operator-to-operator trust. No mechanism for Operator A to verify that Operator B is a legitimate BANZA federation member.

**Required artifacts:**
- Protocol spec for operator key distribution
- `contracts/federation/operator-certificate.json` — schema for operator certificate
- `contracts/federation/federation-trust.json` — trust establishment protocol
- Trust anchor definition (who anchors the BANZA trust chain?)

**Why critical:** Without trust, operator discovery is insecure. Any entity can serve a manifest at the well-known URL. No federation is possible without verified identity.

---

### GAP-002 — Operator-to-Operator Message Protocol (CRITICAL)
**What is missing:** No protocol for Operator A to send a payment routing request to Operator B. RFC-0001 defines the Rust trait but not the wire format.

**Required artifacts:**
- `contracts/federation/federation-routing.json` — cross-operator routing request/response schema
- HTTP endpoint spec for `POST /federation/route` or equivalent
- Authentication scheme for inter-operator requests
- Error response codes for routing failures

**Why critical:** Even with trust, operators have no agreed protocol for initiating a cross-operator payment. The `InteropRoutingEngine` trait exists in design; nothing sends it over the network.

---

### GAP-003 — Cross-Operator Routing Implementation (CRITICAL)
**What is missing:** `InteropRoutingEngine` trait defined in RFC-0001 but not implemented. `banza-routing` crate does single-operator only.

**Required artifacts:**
- Implementation of `InteropRoutingEngine` in `core/crates/banza-routing/`
- `OperatorDescriptor` struct (list of available operators at routing time)
- `OperatorRouteRequest` struct (RFC-0001)
- `OperatorRoutingDecision` struct (RFC-0001)
- Integration with operator discovery (how does the router know which operators exist?)

**Why critical:** Routing is the entry point of every cross-operator payment.

---

### GAP-004 — Cross-Operator Settlement Implementation (HIGH)
**What is missing:** `CrossOperatorSettlementProvider` trait defined in RFC-0002 but not implemented. No obligation recording, no netting, no bilateral settlement execution.

**Required artifacts:**
- Implementation of `InteropObligation` struct
- Implementation of `CrossOperatorSettlementProvider`
- Netting computation logic
- `contracts/federation/federation-obligation.json` — obligation schema
- Integration with existing `banza-settlement` single-operator batch system

---

### GAP-005 — Federation Conformance Vectors (HIGH)
**What is missing:** All existing L3 conformance tests are single-operator (manifest validity, capability declaration). No multi-operator test scenarios.

**Required artifacts:**
- `conformance/vectors/federation-routing.json` — cross-operator routing vectors
- `conformance/vectors/federation-settlement.json` — obligation and netting vectors
- `conformance/vectors/federation-discovery.json` — operator discovery vectors
- `conformance/vectors/federation-trust.json` — trust establishment vectors
- `conformance/federation/suite.json` — federation conformance suite

**Minimum vectors required:**
- FED-001: Operator A discovers Operator B manifest
- FED-002: Operator A verifies Operator B identity
- FED-003: Cross-operator routing decision selects Operator B
- FED-004: Obligation recorded for cross-operator payment
- FED-005: Net position computed between two operators
- FED-006: Bilateral settlement executed

---

### GAP-006 — Operator Certificate / Certification Attestation (HIGH)
**What is missing:** No mechanism for an operator to prove its certification level to another operator. The `certification_level` field in the manifest is informational only — not signed or verified.

**Required artifacts:**
- `contracts/federation/operator-certificate.json` — signed certification artifact schema
- Protocol spec for how BANZA issues certification artifacts
- Protocol spec for how operators present certification proofs in federation
- Revocation mechanism (operator loses certification — how does federation know?)

---

### GAP-007 — Federation Event Schema (MEDIUM)
**What is missing:** No schema for events that cross operator boundaries. Cross-operator payments need events from both Operator A and Operator B in the same trace flow.

**Required artifacts:**
- `contracts/federation/federation-event.json` — cross-operator event envelope
- Protocol spec for trace_id propagation across operator boundaries
- Event delivery mechanism between operators
- Conformance vectors: FED-EVT-001 through FED-EVT-004

---

### GAP-008 — Manifest Signing and Verification (MEDIUM)
**What is missing:** RFC-0005 defines `"public_key": "ed25519:base64..."` in the manifest format, but no code signs or verifies manifests.

**Required artifacts:**
- Manifest signing protocol (how does BANZA sign an operator's manifest?)
- Verification code in `banza-capabilities/src/operator.rs`
- Key rotation protocol
- Signed manifest conformance test (MAN-005: signature verification)

---

### GAP-009 — L4 Infrastructure Operator Conformance Suite (MEDIUM)
**What is missing:** L4 is defined in BANZA_CERTIFICATION.md but has no conformance suite, no test vectors, and no certifiable path.

**Required artifacts:**
- `conformance/infrastructure/suite.json` — L4 conformance suite
- `conformance/vectors/federation-full.json` — full federation conformance vectors
- `conformance/vectors/acquiring.json` — acquiring capability vectors
- Definition of `acquiring.emis` capability test

---

### GAP-010 — Federation Registry (LOW)
**What is missing:** RFC-0005 proposes three discovery modes. Only Direct mode (URL) works. DNS and Registry modes not implemented.

**Required artifacts:**
- DNS TXT record format spec for operator discovery
- Or: Simple federation registry API spec (`contracts/federation/federation-registry.json`)
- Conformance vector: FED-DISC-001 through FED-DISC-003

**Note:** A decentralized approach (DNS TXT) avoids centralizing the federation registry. This is the preferred BANZA approach given the operator-neutrality principle.

---

## What Already Exists (Credit Where Due)

The following federation-related artifacts are complete and ready:

| Artifact | Location | Status |
|----------|----------|--------|
| Operator capability flags | `core/crates/banza-capabilities/src/operator.rs` | ✓ Complete |
| Wallet capability model | `core/crates/banza-capabilities/src/wallet.rs` | ✓ Complete |
| Provider capability negotiation | `core/crates/banza-capabilities/src/provider.rs` | ✓ Complete |
| Operator manifest endpoint | `reference/sandbox-operator/src/routes.rs:31` | ✓ Working |
| Manifest schema | `conformance/manifests/schema.json` | ✓ Complete |
| Manifest conformance vectors | `conformance/vectors/operator-manifests.json` | ✓ MAN-001–004 |
| Capability conformance vectors | `conformance/operators/suite.json` | ✓ CAP-001–002 |
| RFC-0001 trait design | `docs/rfc/RFC-0001-multi-operator-routing.md` | ✓ Drafted |
| RFC-0002 settlement protocol | `docs/rfc/RFC-0002-cross-operator-settlement.md` | ✓ Drafted |
| RFC-0003 wallet capabilities | `docs/rfc/RFC-0003-wallet-capabilities.md` | ✓ Drafted |
| RFC-0004 capability negotiation | `docs/rfc/RFC-0004-provider-capability-negotiation.md` | ✓ Drafted |
| RFC-0005 operator discovery | `docs/rfc/RFC-0005-operator-discovery.md` | ✓ Drafted |
| Trace system | `core/crates/banza-transactions/`, `conformance/vectors/event-envelopes.json` | ✓ Complete |
| cross_operator_routing flag | `OperatorCapabilityFlags` struct | ✓ Field exists |
| cross_operator_settlement flag | `OperatorCapabilityFlags` struct | ✓ Field exists |
| interop_endpoint field | `OperatorManifest` struct | ✓ Field exists |
| Federation glossary | `BANZA_REFERENCE.md §10` | ✓ Defined |
| Federation roadmap | `BANZA_REFERENCE.md §10` | ✓ Defined |

---

## Implementation Sequence for L3 Certification

The minimum sequence to make L3 Federation Certification achievable (without introducing centralization):

```
Step 1: Formalize trust model (GAP-001)
   → Write ADR for operator trust (PKI vs. BANZA-signed manifest)
   → Define contracts/federation/operator-certificate.json

Step 2: Implement manifest signing and verification (GAP-008)
   → Extend banza-capabilities crate with ed25519 signing
   → Add MAN-005 (signature verification) to conformance suite

Step 3: Define federation event schema (GAP-007)
   → Write contracts/federation/federation-event.json
   → Add cross-operator trace_id propagation spec

Step 4: Write federation conformance suite (GAP-005)
   → Start with FED-001 through FED-006 minimum vectors
   → Each vector tests one federation surface area

Step 5: Implement InteropRoutingEngine skeleton (GAP-003)
   → Add OperatorDescriptor, OperatorRouteRequest, OperatorRoutingDecision
   → StaticInteropRoutingEngine: routes to operator based on manifest capability flags

Step 6: Implement obligation recording (GAP-004)
   → Add InteropObligation struct to banza-settlement
   → Add CrossOperatorSettlementProvider trait skeleton

Step 7: Certify two operators in controlled federation
   → Sandbox Operator A ↔ Sandbox Operator B
   → Run federation conformance suite
   → Both operators pass → first L3 certification issued
```

Total scope: approximately 8–10 new ADRs/contracts + 2 crate extensions + 1 new conformance suite.
