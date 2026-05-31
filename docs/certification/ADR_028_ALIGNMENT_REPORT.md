# ADR-028 Alignment Report

**Document ID:** ADR-028-ALIGNMENT-REPORT-001  
**Date:** 2026-05-31  
**Authority:** ADR-028 (BANZA Certification Level Architecture)  
**Status:** FINAL  

---

## Executive Summary

ADR-028 is accepted and implemented. The BANZA certification level architecture is now frozen.

**One document was updated.** All other documents, contracts, and conformance code were already aligned with the canonical model.

**The conflict is resolved:** `BANZA_CERTIFICATION.md` previously defined L3 as "payouts and reconciliation" and L4 as "acquiring + federation_ready". ADR-028 aligns BANZA_CERTIFICATION.md with ADR-026, which is the authoritative ADR for the federation level threshold (L3).

---

## Files Updated

### Changed

| File | Change summary |
|------|---------------|
| `BANZA_CERTIFICATION.md` | L3 purpose updated to federation-primary; L3 capabilities updated to `cross_operator_routing`, `reconciliation`, `payout.batch`; L4 `federation_ready` capability removed; Authority line updated to reference ADR-028; badge table updated with federation eligibility column |
| `docs/adr/ADR-028-CERTIFICATION-LEVEL-ARCHITECTURE.md` | **New** — canonical authority for the level model |
| `docs/certification/ADR_028_ALIGNMENT_REPORT.md` | **New** — this document |

### Already correct — no changes required

| File | Status |
|------|--------|
| `BANZA_CONFORMANCE.md` | Correct — L3 = "operator manifest + capability declaration" |
| `BANZA_REFERENCE.md` | Correct — L3 = Federation Operator |
| `docs/adr/ADR-026-FEDERATION-TRUST-MODEL.md` | Correct — REQUIRED_LEVEL = 3 |
| `contracts/federation/operator-certificate.json` | Correct — `certification_level >= 3` for 90-day rule |
| `contracts/federation/federation-manifest.json` | Correct — L3+ for `supports_federation` |
| `contracts/events/types.json` | Correct — L0/L1 event tagging |
| `tools/banza-conformance/fixture_server.py` | Correct — `if level < 3: reject` |
| `tools/banza-conformance/run_fed.py` | Correct — `if cert_level >= 3` |
| `tools/banza-conformance/trust_root.py` | Correct — no level references |
| `tools/banza-conformance/runner_infra.py` | Correct — no level references |
| `docs/federation/FEDERATION_FIXTURE_CATALOG.md` | Correct — CERT-L2-LEVEL fixture for FED-TRUST-004 |
| `docs/federation/FEDERATION_INVARIANTS.md` | Correct — INV-TRUST-004 references L3+ |
| `docs/federation/L3_CERTIFICATION_READINESS_REPORT.md` | Correct — targets L3 |
| `docs/federation/FEDERATION_CONFORMANCE_MODEL.md` | Correct — L3 model |

---

## Definitions Removed

| Definition | Was in | Reason for removal |
|-----------|--------|-------------------|
| `federation_ready` capability at L4 | `BANZA_CERTIFICATION.md` L4 | Placeholder; superseded by federation being designed at L3 |
| L3 purpose: "payouts and automated reconciliation" | `BANZA_CERTIFICATION.md` L3 | Incomplete description; `payout.batch` and `reconciliation` remain at L3 but the primary purpose is now federation |
| "participation in BANZA federation (when available)" at L4 | `BANZA_CERTIFICATION.md` L4 | Federation is at L3, not L4 |

---

## Definitions Added

| Definition | Now in |
|-----------|--------|
| L3 purpose: "Cross-operator routing, inter-operator settlement, and automated reconciliation" | `BANZA_CERTIFICATION.md` L3, ADR-028 §Phase 4 |
| `cross_operator_routing` as an explicit L3 capability | `BANZA_CERTIFICATION.md` L3 |
| L3 operator infrastructure requirements (certificate, BRL, endpoints) | `BANZA_CERTIFICATION.md` L3 |
| Federation eligibility column in certification badge table | `BANZA_CERTIFICATION.md` |
| ADR-028 as the authority for certification level architecture | `BANZA_CERTIFICATION.md` authority line |
| Complete canonical level model with dependency graph | `docs/adr/ADR-028-CERTIFICATION-LEVEL-ARCHITECTURE.md` |
| Progression rules P-001 through P-007 | `docs/adr/ADR-028-CERTIFICATION-LEVEL-ARCHITECTURE.md` |
| Certification matrix | `docs/adr/ADR-028-CERTIFICATION-LEVEL-ARCHITECTURE.md` |

---

## Migration Impact

### For operators already at L2

**No action required on their part.** Their L2 certification is valid and unaffected. The change means they can now proceed to L3 (Federation) as their next step — and should be informed that federation does not require L4 as previously suggested in BANZA_CERTIFICATION.md.

### For operators who believed federation required L4

They should be notified:

> BANZA certification has been clarified by ADR-028. Federation eligibility is at Level 3 (Federation Operator), not Level 4. If you have passed Level 2 (Settlement Operator) conformance, you may proceed directly to Level 3 certification. You do not need Level 4 to participate in BANZA federation.

### For the conformance runner

No changes. The conformance runner already implements the correct level thresholds per ADR-026.

### For the operator registry

The operator registry should surface the federation eligibility flag for L3+ operators. The badge table in `BANZA_CERTIFICATION.md` now includes this column.

---

## Backward Compatibility Impact

| Area | Impact |
|------|--------|
| Protocol wire format | None — `certification_level` integer representation unchanged |
| Contract schemas | None — all schemas unchanged |
| Conformance test IDs | None — all FED-* IDs unchanged |
| Invariant IDs | None — all INV-* IDs unchanged |
| Existing L0–L2 certifications | None — unaffected |
| Existing L3 certifications | None — already correct per ADR-026 |
| Hard-coded level checks in code | None — already correct per ADR-026 |

---

## Verdict: Architecture Frozen

**The BANZA certification architecture is now frozen.**

The single source of truth is `docs/adr/ADR-028-CERTIFICATION-LEVEL-ARCHITECTURE.md`.

Any future change to:
- The number of levels
- The names of levels  
- The capabilities at any level
- The progression rules
- The federation eligibility threshold

…requires a new ADR that supersedes ADR-028. Documentation changes alone are insufficient.

### Unblocked

With ADR-028 accepted, production blocker #1 is resolved. Future certification work can proceed against the frozen model without revisiting level definitions:

| Blocker | Status |
|---------|--------|
| #1 ADR-028 — certification level architecture | **RESOLVED** |
| #2 Production BANZA Root key establishment | Open |
| #3 Real two-operator interoperability test | Open |

The remaining two blockers are independent of the certification level model and may proceed in any order.
