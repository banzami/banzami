# BANZA Federation Readiness Report

**Audit ID:** BANZA-FEDERATION-READINESS-AUDIT-001  
**Date:** 2026-05-31  
**Status:** Read-only — no modifications  
**Authority:** ADR-025, BANZA_REFERENCE.md §10, RFC-0001 through RFC-0006

---

## Executive Summary

Federation is **in design phase**. The protocol has the architectural primitives and a complete declarative framework. The inter-operator protocol itself is not implemented. L3 and L4 certification are **defined but not yet certifiable**.

**What fraction of Federation already exists?**

| Layer | Status |
|-------|--------|
| Primitive layer (trace, ledger, wallet, capabilities) | ~80% complete |
| Declarative layer (manifests, capability flags, RFCs) | ~70% complete |
| Operational layer (routing code, settlement code) | ~15% complete |
| Trust layer (PKI, certificates, revocation) | ~0% complete |
| Conformance layer (federation test vectors) | ~10% complete |

**Overall: ~35% of Federation already exists implicitly in BANZA.**

---

## The 8 Federation Surface Areas

| Surface | Status | Notes |
|---------|--------|-------|
| **1. Operator Discovery** | PARTIAL | Manifest at well-known endpoint; no signing/verification |
| **2. Operator Identity** | PARTIAL | operator_id field exists; no PKI |
| **3. Operator Trust** | MISSING | No certificates, no revocation, no trust anchors |
| **4. Capability Advertisement** | PRESENT | RFC-0003, RFC-0004 fully implemented; OperatorCapabilityFlags typed |
| **5. Cross-Operator Routing** | PARTIAL | RFC-0001 designed; `StaticRoutingEngine` single-op only |
| **6. Cross-Operator Settlement** | PARTIAL | RFC-0002 designed; `banza-settlement` single-op only |
| **7. Federation Events** | PARTIAL | Single-operator event system works; no cross-operator event schema |
| **8. Federation Conformance** | PARTIAL | L3 manifest/capability vectors exist; no multi-operator vectors |

---

## Canonical Federation Definitions

These definitions are implicitly present across BANZA documentation. This section makes them explicit.

### Operator
An entity that implements the BANZA protocol, has passed conformance testing at L0 or above, and operates financial infrastructure on the BANZA network.

### Certified Operator
An operator that has received a signed certification artifact from BANZA at one of the five levels (L0–L4). Certification is granted by BANZA based on conformance results. BanzAI evaluates readiness; BANZA issues the artifact.

### Federation Member
A certified operator that has achieved L3+ certification and has declared `supports_federation: true` in its operator manifest. A federation member is capable of accepting cross-operator payments and participating in cross-operator settlement.

### Federation
A network of certified operators that can route payments between themselves and settle net obligations periodically. Federation is governed by BANZA protocol rules. No operator governs the federation.

### Federation Identity
A cryptographically attested identity for a certified operator within the federation. Includes: operator_id (stable string), certification_level, public_key (ed25519, planned), and issued_at/expires_at timestamps.

*Status: MISSING — not yet implemented.*

### Federation Trust
The mechanism by which one operator cryptographically verifies that another operator is a legitimate BANZA federation member at the declared certification level. Requires PKI infrastructure: trust anchors, operator certificates, revocation.

*Status: MISSING — not yet implemented.*

### Federation Transaction
A payment that originates on Operator A (sender's wallet) and completes on Operator B (receiver's wallet). Both operators must be federation members. The routing layer selects the destination operator; the ledger records the obligation.

*Status: MISSING — routing code not implemented.*

### Cross-Operator Payment
Synonym for Federation Transaction. A payment that crosses operator boundaries.

### Cross-Operator Settlement
The periodic netting and final settlement of monetary obligations between federation members. Three phases: (1) obligation recording per cross-operator transaction, (2) net position computation, (3) bilateral settlement execution via bank rails.

*Status: PARTIAL — RFC-0002 designed; `CrossOperatorSettlementProvider` trait not implemented.*

### Federation Event
An event emitted by one operator and propagated to another operator in the same federation transaction flow. Carries the same `trace_id` as the originating transaction. Format not yet defined.

*Status: PARTIAL — single-operator events exist; cross-operator event schema missing.*

### Federation Discovery
The protocol by which an operator locates and verifies another operator's manifest. Three modes defined in RFC-0005: Direct (URL), DNS (TXT record), Registry (federated directory).

*Status: PARTIAL — Direct mode works (well-known endpoint); DNS and Registry not implemented.*

### Federation Route
A routing decision that selects Operator B as the destination for a transaction originating on Operator A. Requires: discovery of available operators, capability matching, and routing rule evaluation.

*Status: MISSING — `InteropRoutingEngine` not implemented.*

---

## Certification Readiness by Level

| Level | Name | Certifiable Today? | Blocker |
|-------|------|-------------------|---------|
| L0 | Sandbox Operator | ✓ Yes | None |
| L1 | Payment Operator | ✓ Yes | None |
| L2 | Settlement Operator | ✓ Yes | None |
| L3 | Federation Operator | ✗ No | No L3 multi-operator test vectors; no trust infrastructure |
| L4 | Infrastructure Operator | ✗ No | No L4 conformance suite; L4 test vectors undefined |

---

## BANZA Reference §10 — Official Roadmap

Per `BANZA_REFERENCE.md §10 (Federação)`:

| Milestone | Description | Target |
|-----------|-------------|--------|
| Federation RFC | Define inter-operator protocol | H1 2027 |
| Pilot operators | Two operators in controlled federation | H2 2027 |
| Open federation | Any L4 operator may federate | 2028 |

Federation is on a clear 18–24 month roadmap from the current date.
