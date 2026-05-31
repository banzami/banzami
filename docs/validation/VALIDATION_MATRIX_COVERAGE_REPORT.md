# VALIDATION_MATRIX_COVERAGE_REPORT.md

**Audit ID:** VALIDATION-STUDIO-COVERAGE-AUDIT-001  
**Date:** 2026-05-31

Field-by-field comparison of the existing Validation Studio schema (`~/banzami`) against the target BANZA protocol governance model defined in the Phase B directive.

---

## Required fields — classification

| Required field | Studio schema field | Classification | Notes |
|---|---|---|---|
| `feature_id` | `id` | **PRESENT** | Same concept, field named `id` |
| `title` | `title` | **PRESENT** | Exact match |
| `domain` | `validationDomain` (DOM-FIN, DOM-DEV…) | **PARTIAL** | Present but uses product-oriented domain taxonomy. Missing protocol domains: `protocol-kernel`, `conformance`, `certification` |
| `category` | `categoryId` | **PRESENT** | 24 categories covering all product areas |
| `priority` | `priority` (CRITICAL/HIGH/MEDIUM/LOW) | **PRESENT** | Exact match |
| `status` | `status` (VALIDATED/IMPLEMENTED/PLANNED…) | **PARTIAL** | Richer status model than needed. Maps to target: VALIDATED≈implemented, PLANNED≈missing, BLOCKED≈blocked |
| `reference_section` | `referenceSection` | **PRESENT** | Points to BANZA_REFERENCE.md sections |
| `ADR/RFC reference` | `evidence[type=adr]` | **PARTIAL** | ADRs appear in evidence entries, not as a structured top-level field |
| `contract reference` | `evidence[ref=contracts/...]` | **PARTIAL** | Exists for 4 of 79 items. Phase A contracts absent. Not a structured field |
| `SDK coverage` | `evidence[ref=sdk/...]` + `technicalArea` | **PARTIAL** | SDK language coverage is not tracked per-language. Appears as free-text in `technicalArea`. No per-SDK status |
| `conformance suite coverage` | *(absent)* | **MISSING** | No field for conformance vector IDs or suite case links |
| `certification level` | *(absent)* | **MISSING** | No field for L0–L4 protocol certification level |
| `implementation source` | `evidence[type=route/component/config]` | **PARTIAL** | Captures file references but not kernel crate, reference impl, or SDK implementation specifically |
| `test coverage` | `testCoverage: boolean` + `validationMethods[]` | **PRESENT** | Boolean + method list. More granular than required |
| `validation status` | `status` | **PRESENT** | Maps cleanly |
| `blocking reason` | `blockingIssues[]` | **PRESENT** | Explicit array of blocking issue descriptions |
| `confidence score` | `confidence.score` (0-100) + `confidence.level` + `confidence.basis[]` | **PRESENT** | Exceeds the target requirement. Fully computed, not declared |

---

## Fields present in studio but not in target spec

These are additive — they strengthen the model:

| Field | Value |
|---|---|
| `acceptanceCriteria[]` | Explicit pass/fail criteria per item |
| `invariants[]` with `PASS/FAIL/UNKNOWN/NOT_RUN` | Per-item financial invariant enforcement status |
| `history[]` | Full immutable audit trail with fingerprint + commit |
| `requires[]` | Enforced dependency locking (not just informational) |
| `affects[]` | Downstream impact tracking |
| `revalidateWhenChanged[]` | File glob patterns for automated revalidation triggers |
| `freezeReason` | Reason an item is locked at REVALIDATION_REQUIRED |
| `lastValidatedAt` | ISO date of last VALIDATED transition |
| `validatedAgainstCommit` | Commit hash at validation time |

These fields should be retained and adopted in any extension of the protocol matrix.

---

## Fields missing in studio that must be added

| Missing field | Target purpose | Proposed addition |
|---|---|---|
| `certification_level` | Maps feature to L0–L4 protocol cert level | Add as top-level integer field: `0`, `1`, `2`, `3`, `4` |
| `contract_artifacts` | Structured list of contracts/\* that specify this feature | Add as `contractArtifacts: string[]` listing files under contracts/ |
| `conformance_vectors` | List of conformance vector IDs covering this feature | Add as `conformanceVectors: string[]` (e.g. `["QR-001","QR-002"]`) |
| `conformance_suite_cases` | Wired suite cases in conformance/operators/suite.json | Add as `conformanceSuiteCases: string[]` |
| `sdk_coverage` | Per-language SDK status | Add as `sdkCoverage: Record<'typescript'|'python'|'php'|'go'|'flutter', 'implemented'|'partial'|'missing'|'not_applicable'>` |
| `reference_impl` | Sandbox operator file and function reference | Add as `referenceImpl: { file: string, function?: string }` |
| `kernel_crate` | Rust kernel crate implementing this feature | Add as `kernelCrate?: string` |

---

## Coverage summary

| Target requirement layer | Studio coverage |
|---|---|
| Feature identification | ✅ Full — 79 items with IDs, titles, categories |
| Domain classification | ⚠️ Partial — product domains present; protocol conformance domains absent |
| Priority and status | ✅ Full |
| Evidence and references | ⚠️ Partial — file references exist; contract/SDK/conformance structured links absent |
| Financial invariants | ✅ Full — per-item PASS/FAIL with mandatory enforcement |
| Confidence scoring | ✅ Full — computed, not declared |
| Audit history | ✅ Full — immutable, fingerprinted |
| Governance enforcement | ✅ Full — automated rule checks |
| Protocol certification levels | ❌ Absent |
| Conformance suite traceability | ❌ Absent |
| Per-language SDK coverage | ❌ Absent |
| Kernel-level implementation mapping | ❌ Absent |
| Phase A contract integration | ❌ Absent |

---

## Risk assessment

| Risk | Severity | Detail |
|---|---|---|
| Phase B matrix (`~/banza/docs/validation/`) duplicates schema | **HIGH** | Two competing matrices with different schemas and item sets. If committed as-is, creates two sources of truth for overlapping features |
| No Protocol certification tracking | **HIGH** | Cannot determine if any operator can pass L1 certification without this data |
| No conformance suite traceability | **HIGH** | 55 conformance vectors orphaned — no matrix item links to them |
| Phase A contracts unlinked | **MEDIUM** | Events, webhooks, QR contracts have no matrix entries referencing them |
| SDK per-language coverage hidden | **MEDIUM** | SDK-001 through SDK-004 are all PLANNED with no language-level granularity |
