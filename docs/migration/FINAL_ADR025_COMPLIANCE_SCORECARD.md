---
name: final-adr025-compliance-scorecard
description: ADR-025 compliance scorecard across the entire ecosystem documentation surface — ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001
metadata:
  type: project
---

# Final ADR-025 Compliance Scorecard

**Mission:** ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001  
**Date:** 2026-05-30  
**Reference:** ADR-025 — Ecosystem Naming Inversion (2026-05-29)

---

## Scoring Method

Each criterion is assessed across the relevant document surface.

| Score | Meaning |
|-------|---------|
| ✓ PASS | Fully compliant with ADR-025 |
| ⚠ PARTIAL | Canonical documents compliant; legacy documents have residual issues |
| ✗ FAIL | Active ADR-025 violation |

---

## Section 1 — BANZA Identity

| # | Criterion | Document Surface | Score | Notes |
|---|-----------|-----------------|-------|-------|
| B1 | BANZA is described as "protocol", not "product" or "company" | BANZA_REFERENCE, BANZA_MANIFESTO, BANZA_ARCHITECTURE | ✓ PASS | |
| B2 | BANZA does not own or govern Banzami | BANZA_GOVERNANCE, BANZA_REFERENCE | ✓ PASS | |
| B3 | BANZA is not described as an application or wallet | All BANZA_* docs | ✓ PASS | |
| B4 | BANZA is not called "Banzami" | All canonical docs | ✓ PASS | |
| B5 | BANZA README header is correct | `banza/README.md` header | ✓ PASS | |
| B6 | banza/README.md body consistently uses "BANZA" / "BANZA protocol" | `banza/README.md` body | ⚠ PARTIAL | Lowercase "Banza" throughout body; P1-001 |
| B7 | Naming note in banza/README.md is accurate | `banza/README.md:49` | ⚠ PARTIAL | "Banza was formerly called Banzami" — misleading; P1-002 |
| B8 | No BANZA document describes Banzami Wallet or Business products | All BANZA_* docs | ✓ PASS | |
| B9 | Banzami is correctly described as "reference operator" in BANZA docs | BANZA_REFERENCE, BANZA_MANIFESTO | ✓ PASS | |

**BANZA Score: 7/9 PASS · 2 PARTIAL · 0 FAIL**

---

## Section 2 — BanzAI Identity

| # | Criterion | Document Surface | Score | Notes |
|---|-----------|-----------------|-------|-------|
| AI1 | BanzAI is described as "Protocol Operating System", not "chatbot" or "Banzami product" | BANZAI_REFERENCE, BANZAI_ARCHITECTURE | ✓ PASS | |
| AI2 | BanzAI does not redefine protocol invariants | BANZAI_REFERENCE, BANZAI_CAPABILITIES | ✓ PASS | Explains them; does not define |
| AI3 | BanzAI does not describe Banzami Wallet or Business | BANZAI_* docs | ✓ PASS | |
| AI4 | Deterministic-first principle stated and respected | BANZAI_REFERENCE §7, BANZAI_CAPABILITIES | ✓ PASS | |
| AI5 | Hosting vs ownership distinction stated correctly | BANZAI_REFERENCE §1 | ✓ PASS | "hosted by Banzami — not owned by Banzami" |
| AI6 | banzai/README.md header is correct | `banzai/README.md` header | ✓ PASS | |
| AI7 | banzai/README.md capability count matches BANZAI_REFERENCE.md | `banzai/README.md:27` | ✗ FAIL | README says 8; BANZAI_REFERENCE.md defines 6; P1-003 |
| AI8 | banzai/package.json name reflects ADR-025 identity | `banzai/package.json` | ⚠ PARTIAL | `@banzami/banzamia` — pre-ADR-025; P2-018 |
| AI9 | banzai/CONTRIBUTING.md fork URL is correct | `banzai/CONTRIBUTING.md:45` | ✗ FAIL | Points to old `github.com/banzami/banzamia`; P2-012 |

**BanzAI Score: 6/9 PASS · 1 PARTIAL · 2 FAIL**

*Note: The 2 FAILs are in CONTRIBUTING and package.json — not in canonical REFERENCE documents. The REFERENCE layer is fully compliant.*

---

## Section 3 — Banzami Identity

| # | Criterion | Document Surface | Score | Notes |
|---|-----------|-----------------|-------|-------|
| MI1 | Banzami is described as "reference operator", not "the protocol" | BANZAMI_REFERENCE, BANZAMI_PRODUCTS | ✓ PASS | |
| MI2 | Banzami does not claim to govern BANZA | BANZAMI_GOVERNANCE, BANZAMI_REFERENCE | ✓ PASS | Explicitly disclaimed |
| MI3 | Banzami does not redefine certification requirements | BANZAMI_PRODUCTS, BANZAMI_ARCHITECTURE | ✓ PASS | Cross-references BANZA_CERTIFICATION.md |
| MI4 | banzami/README.md header is correct | `banzami/README.md` header | ✓ PASS | |
| MI5 | banzami/README.md body consistently uses "Banzami" | `banzami/README.md` body | ✗ FAIL | Uses "Banza" throughout to mean Banzami; P1-004 |
| MI6 | banzami/README.md does not assign BANZA identity to Banzami | `banzami/README.md:13` | ✗ FAIL | "open-source ecosystem lives at…" assigns BANZA's role to Banzami; P1-005 |
| MI7 | Banzami does not own the open-source SDK ecosystem | `banzami/README.md:13` | ✗ FAIL | Same as MI6; P1-005 |
| MI8 | Banzami correctly described as operator, not protocol | All BANZAMI_* canonical docs | ✓ PASS | |
| MI9 | Protocol invariants cross-referenced, not restated | BANZAMI_ARCHITECTURE, BANZAMI_PRODUCTS | ✓ PASS | |

**Banzami Score: 6/9 PASS · 0 PARTIAL · 3 FAIL**

*Note: All 3 FAILs are in banzami/README.md. The REFERENCE layer is fully compliant.*

---

## Section 4 — Cross-Contamination

| # | Criterion | Score | Notes |
|---|-----------|-------|-------|
| CC1 | No BANZA document describes operator deployment details | ✓ PASS | |
| CC2 | No BANZAI document redefines a financial invariant | ✓ PASS | |
| CC3 | No BANZAMI document defines certification requirements | ✓ PASS | |
| CC4 | No BANZAMI document claims to own the BANZA kernel | ✓ PASS | |
| CC5 | No BANZA document implies Banzami is the only operator | ✓ PASS | "one operator among many" stated |

**Cross-Contamination Score: 5/5 PASS**

---

## Section 5 — GitHub and URL Consistency

| # | Criterion | Score | Notes |
|---|-----------|-------|-------|
| GH1 | All GitHub URLs in canonical docs use `banza-protocol/` org | ✓ PASS | |
| GH2 | All GitHub URLs in README files use `banza-protocol/` org | ✗ FAIL | Multiple stale `github.com/banzami/` URLs; P2-002 to P2-017 |
| GH3 | All `banzami.org` route references use `/banzai` not `/banzamia` | ⚠ PARTIAL | Canonical docs: PASS. Legacy docs: 26+ stale `/banzamia` routes; P2-019 to P2-026 |
| GH4 | No document implies `banzami.org` is the final identity of BANZA | ✓ PASS | |
| GH5 | `banza.network` (future domain) not prematurely referenced | ✓ PASS | 0 mentions |

**URL Score: 3/5 PASS · 1 PARTIAL · 1 FAIL**

---

## Overall ADR-025 Compliance

| Layer | Score | Critical Issues |
|-------|-------|----------------|
| Canonical docs (REFERENCE, ARCHITECTURE, GOVERNANCE, SECURITY, ROADMAP) | **100%** | None |
| CLAUDE.md files | **100%** | None |
| README files | **60%** | P1-001–P1-005 |
| CONTRIBUTING files | **50%** | P2-011, P2-012 |
| Package metadata | **0%** | P2-018 |
| Legacy docs (pre-ADR-025 combined reference, docs/banzamia/) | **30%** | P2 batch |

**Canonical Layer: FULLY COMPLIANT**  
**Legacy/Peripheral Layer: REQUIRES CLEANUP**

---

## Remediation Priority

| Priority | Action | Effort |
|----------|--------|--------|
| 1 | Fix banzami/README.md "Banza" → "Banzami" body (P1-004) | Medium |
| 2 | Fix banzami/README.md line 13 identity + URL (P1-005) | Low |
| 3 | Fix banzai/README.md capability count: 8 → 6 (P1-003) | Low |
| 4 | Fix banzai/CONTRIBUTING.md fork URL (P2-012) | Low |
| 5 | Fix banza/README.md naming note (P1-002) | Low |
| 6 | Batch replace `github.com/banzami/` URLs (P2-002 to P2-017) | Medium (multi-file) |
| 7 | Batch replace `banzami.org/banzamia` → `banzami.org/banzai` (P2-019 to P2-026) | Medium (multi-file) |
| 8 | Update `banzai/package.json` name (P2-018) | Low |

---

*Produced by: ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001 — 2026-05-30*
