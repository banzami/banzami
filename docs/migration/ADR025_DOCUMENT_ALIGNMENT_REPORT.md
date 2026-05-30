---
name: adr025-document-alignment-report
description: ADR-025 alignment verification for the canonical document architecture — ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001
metadata:
  type: project
---

# ADR-025 Document Alignment Report

**Mission:** ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001  
**Date:** 2026-05-30  
**Reference:** ADR-025 — Ecosystem Naming Inversion (2026-05-29)  
**Status:** Authoritative

---

## ADR-025 Requirements Summary

ADR-025 established three binding requirements:

1. **Identity clarity** — BANZA = protocol, BanzAI = Protocol OS, Banzami = reference operator
2. **No cross-contamination** — each layer's documents must describe only its own domain
3. **Repository as architecture** — the file tree itself must communicate the ecosystem hierarchy

---

## Validation Criteria

### Section 1 — BANZA Repository Identity

| Criterion | Test | Status |
|-----------|------|--------|
| B1 | Opening `~/banza` reveals `BANZA = protocol` without opening any file | PASS — every document is prefixed `BANZA_` |
| B2 | No BANZA document describes Banzami Wallet, Banzami Business, or merchant onboarding | PASS — BANZAMI_PRODUCTS.md owns these |
| B3 | No BANZA document describes BanzAI capabilities or model routing | PASS — BANZAI_ARCHITECTURE.md owns these |
| B4 | Protocol invariants are defined ONLY in BANZA_REFERENCE.md §7 | PASS — all other docs cross-reference |
| B5 | Certification levels L0–L4 are owned by BANZA_CERTIFICATION.md | PASS — promoted from banzami/docs/ to banza/ |
| B6 | Conformance suite is owned by BANZA_CONFORMANCE.md | PASS — promoted from docs/conformance.md |
| B7 | Protocol governance is owned by BANZA_GOVERNANCE.md | PASS — renamed from GOVERNANCE.md |
| B8 | Protocol security is owned by BANZA_SECURITY.md | PASS — renamed from SECURITY.md |
| B9 | Protocol manifesto exists as BANZA_MANIFESTO.md | PASS — created |
| B10 | Protocol roadmap exists as BANZA_ROADMAP.md | PASS — created |

**BANZA Identity Score: 10/10 PASS**

---

### Section 2 — BANZAI Repository Identity

| Criterion | Test | Status |
|-----------|------|--------|
| AI1 | Opening `~/banzai` reveals `BanzAI = Protocol OS` without opening any file | PASS — every document is prefixed `BANZAI_` |
| AI2 | No BANZAI document redefines protocol rules, invariants, or certification | PASS — BANZAI_REFERENCE.md has no invariant definitions |
| AI3 | No BANZAI document describes Banzami Wallet or Banzami Business | PASS — scope is Protocol OS only |
| AI4 | BanzAI architecture is owned by BANZAI_ARCHITECTURE.md | PASS — created from §4 |
| AI5 | BanzAI capabilities are owned by BANZAI_CAPABILITIES.md | PASS — created from §5–6 |
| AI6 | Deterministic-first principle is stated in BANZAI documents | PASS — in BANZAI_REFERENCE.md §7 |
| AI7 | BanzAI governance is owned by BANZAI_GOVERNANCE.md | PASS — renamed |
| AI8 | BanzAI security is owned by BANZAI_SECURITY.md | PASS — renamed |
| AI9 | BanzAI roadmap exists as BANZAI_ROADMAP.md | PASS — created |
| AI10 | Hosting vs ownership distinction stated: "hosted by Banzami, serves BANZA protocol" | PASS — in BANZAI_REFERENCE.md §1 |

**BANZAI Identity Score: 10/10 PASS**

---

### Section 3 — BANZAMI Repository Identity

| Criterion | Test | Status |
|-----------|------|--------|
| MI1 | Opening `~/banzami` reveals `Banzami = reference operator` without opening any file | PASS — every document is prefixed `BANZAMI_` |
| MI2 | No BANZAMI document redefines protocol governance or certification | PASS — cross-references only |
| MI3 | No BANZAMI document redefines protocol invariants | PASS — cross-references only |
| MI4 | Operator architecture is owned by BANZAMI_ARCHITECTURE.md | PASS — created |
| MI5 | Operator products are owned by BANZAMI_PRODUCTS.md | PASS — created |
| MI6 | Operator operations are owned by BANZAMI_OPERATIONS.md | PASS — created |
| MI7 | Operator deployment is owned by BANZAMI_DEPLOYMENT.md | PASS — created |
| MI8 | Operator governance is owned by BANZAMI_GOVERNANCE.md | PASS — renamed |
| MI9 | Operator security is owned by BANZAMI_SECURITY.md | PASS — renamed |
| MI10 | Operator roadmap exists as BANZAMI_ROADMAP.md | PASS — created |

**BANZAMI Identity Score: 10/10 PASS**

---

### Section 4 — Cross-Layer Contamination Check

| Check | Test | Status |
|-------|------|--------|
| CC1 | BANZA_MANIFESTO.md mentions no Banzami products by name as central to the protocol vision | PASS |
| CC2 | BANZAI_ARCHITECTURE.md does not redefine any BANZA financial invariant | PASS |
| CC3 | BANZAMI_PRODUCTS.md does not define certification requirements | PASS — cross-refs BANZA_CERTIFICATION.md |
| CC4 | BANZAMI_ARCHITECTURE.md does not claim to own the protocol kernel | PASS — references BANZA_ARCHITECTURE.md |
| CC5 | BANZA_GOVERNANCE.md does not prescribe Banzami's deployment process | PASS — operator decisions are separate |

**Cross-Contamination Score: 5/5 PASS**

---

### Section 5 — Protocol Survivability Test

*Would this document still be relevant if Banzami disappeared from the ecosystem?*

| Document | Survivability | Correct Owner |
|----------|--------------|---------------|
| BANZA_REFERENCE.md | YES — protocol continues without Banzami | BANZA ✓ |
| BANZA_MANIFESTO.md | YES — Angola's payment problem predates Banzami | BANZA ✓ |
| BANZA_ARCHITECTURE.md | YES — kernel architecture is protocol-level | BANZA ✓ |
| BANZA_CERTIFICATION.md | YES — other operators still need certification | BANZA ✓ |
| BANZA_CONFORMANCE.md | YES — conformance suite serves all operators | BANZA ✓ |
| BANZA_GOVERNANCE.md | YES — protocol governance is independent | BANZA ✓ |
| BANZA_SECURITY.md | YES — protocol security applies to all implementations | BANZA ✓ |
| BANZA_ROADMAP.md | YES — protocol roadmap is independent | BANZA ✓ |
| BANZAI_REFERENCE.md | YES — BanzAI serves the protocol, not Banzami | BANZAI ✓ |
| BANZAI_ARCHITECTURE.md | YES — Protocol OS is independent of operator | BANZAI ✓ |
| BANZAI_CAPABILITIES.md | YES — capabilities serve the protocol ecosystem | BANZAI ✓ |
| BANZAI_GOVERNANCE.md | YES — Protocol OS governance is independent | BANZAI ✓ |
| BANZAI_SECURITY.md | YES — Protocol OS security is independent | BANZAI ✓ |
| BANZAI_ROADMAP.md | YES — Protocol OS roadmap is independent | BANZAI ✓ |
| BANZAMI_REFERENCE.md | NO — operator-specific content | BANZAMI ✓ |
| BANZAMI_ARCHITECTURE.md | NO — reference implementation specifics | BANZAMI ✓ |
| BANZAMI_PRODUCTS.md | NO — Banzami Wallet, Business, etc. | BANZAMI ✓ |
| BANZAMI_GOVERNANCE.md | NO — operator governance | BANZAMI ✓ |
| BANZAMI_OPERATIONS.md | NO — operator operations | BANZAMI ✓ |
| BANZAMI_DEPLOYMENT.md | NO — operator deployment | BANZAMI ✓ |
| BANZAMI_SECURITY.md | NO — operator security | BANZAMI ✓ |
| BANZAMI_ROADMAP.md | NO — operator product roadmap | BANZAMI ✓ |

**Survivability Test: 22/22 PASS**

---

### Section 6 — 30-Second Comprehension Test

*A new contributor opens a repository. Without opening any file, can they determine:*

| Question | ~/banza | ~/banzai | ~/banzami |
|----------|---------|---------|----------|
| "What is this repo for?" | BANZA_ prefix on all docs → protocol | BANZAI_ prefix → Protocol OS | BANZAMI_ prefix → operator |
| "Does this repo own the rules?" | Yes — BANZA_GOVERNANCE.md, BANZA_CERTIFICATION.md | No — references BANZA | No — references BANZA |
| "Does this repo have products?" | No — no BANZAMI_ files | No — no BANZAMI_ files | Yes — BANZAMI_PRODUCTS.md |
| "Does this repo deploy anything?" | No — no DEPLOYMENT file | No | Yes — BANZAMI_DEPLOYMENT.md |

**30-Second Test: PASS across all three repositories**

---

## ADR-016 Contamination Verification

ADR-016 contamination patterns from the previous CANONICAL_REFERENCE_AUDIT:

| Contamination Pattern | Pre-Mission Status | Post-Mission Status |
|-----------------------|------------------|-------------------|
| "Banzami is the protocol" | CLEARED in REFERENCE-CANONICAL-SEPARATION-001 | CLEAR |
| "GOVERNANCE.md governs Banzami" | AMBIGUOUS — generic filename | CLEAR — BANZA_GOVERNANCE.md |
| "SECURITY.md covers banzami-ledger crates" | AMBIGUOUS | CLEAR — BANZA_SECURITY.md covers protocol scope |
| Operator content in protocol docs | CLEARED | CLEAR |
| Protocol content in operator docs | CLEARED | CLEAR |
| BanzAI described as Banzami product | CLEARED | CLEAR |

**ADR-016 Contamination: 0 ACTIVE violations**

---

## Overall Alignment Score

| Section | Score | Status |
|---------|-------|--------|
| BANZA Repository Identity | 10/10 | PASS |
| BANZAI Repository Identity | 10/10 | PASS |
| BANZAMI Repository Identity | 10/10 | PASS |
| Cross-Layer Contamination | 5/5 | PASS |
| Protocol Survivability | 22/22 | PASS |
| 30-Second Comprehension | 4/4 per repo | PASS |
| ADR-016 Contamination | 0 violations | PASS |

**ADR-025 Document Alignment: FULL COMPLIANCE**

---

## Signed

ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001 — 2026-05-30

*All criteria assessed against the target state described in CANONICAL_DOCUMENT_ARCHITECTURE.md and executed per DOCUMENT_RELOCATION_PLAN.md.*
