---
name: final-public-surface-checklist
description: Public-facing document surface checklist — everything a new contributor or operator sees first — ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001
metadata:
  type: project
---

# Final Public Surface Checklist

**Mission:** ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001  
**Date:** 2026-05-30

The public surface is defined as: documents that a new contributor sees within the first 5 minutes of opening any repository. This is where identity confusion has the highest cost.

---

## ~/banza — Public Surface

### README.md

| Check | Status | Notes |
|-------|--------|-------|
| Header (first 6 lines) identifies BANZA = protocol | ✓ PASS | Ecosystem table is correct |
| Title is `# BANZA` (all caps) | ✓ PASS | |
| Tagline is protocol-focused | ✓ PASS | "The open financial infrastructure protocol for Angola" |
| BanzAI described as Protocol OS (not chatbot, not Banzami product) | ⚠ ISSUE | Lines 124, 132: `banzami.org/banzamia` (stale URL) |
| Banzami described as reference operator | ✓ PASS | |
| GitHub URLs correct | ✗ ISSUE | Lines 273–274, 469: `github.com/banzami/banzami` stale |
| "What is Banza?" section uses consistent capitalisation | ⚠ ISSUE | Lowercase "Banza" throughout; P1-001 |
| Naming note (ADR-025) is accurate | ✗ ISSUE | "Banza was formerly called Banzami" — misleading; P1-002 |
| Related section (end of README) accurate | ✗ ISSUE | `github.com/banzami/banza` listed for Banzami; P2-003 |

**README public surface: 4/9 PASS · 3 ISSUES · 2 FAILS**

### CLAUDE.md

| Check | Status | Notes |
|-------|--------|-------|
| Ecosystem identity table correct | ✓ PASS | |
| Protocol guardrail stated | ✓ PASS | |
| No operator content | ✓ PASS | |

**CLAUDE.md: PASS ✓**

### BANZA_REFERENCE.md (canonical protocol reference)

| Check | Status | Notes |
|-------|--------|-------|
| Scope limited to protocol rules, invariants, governance, certification | ✓ PASS | |
| BanzAI mentioned once (paragraph + cross-ref) | ✓ PASS | |
| Banzami mentioned as reference operator only | ✓ PASS | |
| Cross-repo links valid | ✓ PASS | |

**BANZA_REFERENCE.md: PASS ✓**

### BANZA_GOVERNANCE.md

| Check | Status | Notes |
|-------|--------|-------|
| No "governed by Banzami" language | ✓ PASS | Fixed in CANONICAL-REPOSITORY-FOUNDATION-001 |
| ADR process correctly described | ✓ PASS | |
| Security link updated to BANZA_SECURITY.md | ✓ PASS | Fixed in ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001 |

**BANZA_GOVERNANCE.md: PASS ✓**

---

## ~/banzai — Public Surface

### README.md

| Check | Status | Notes |
|-------|--------|-------|
| Header identifies BanzAI = Protocol OS | ✓ PASS | |
| Ecosystem table correct (all 3 layers) | ✓ PASS | |
| "8 Capabilities" count | ✗ ISSUE | BANZAI_REFERENCE.md defines 6; README says 8; P1-003 |
| 16 modules listed correctly | ✓ PASS | |
| Deterministic-first principle stated | ✓ PASS | |
| Hosting vs ownership distinction correct | ✓ PASS | |
| GitHub URLs in ecosystem table | ✓ PASS | `github.com/banza-protocol/*` all correct |
| `banzami.org/banzai` route references | ✓ PASS | README uses correct `/banzai` route |

**README public surface: 7/8 PASS · 1 FAIL**

### CLAUDE.md

| Check | Status | Notes |
|-------|--------|-------|
| Ecosystem identity table correct | ✓ PASS | |
| Deterministic-first stated | ✓ PASS | |
| "BanzAI serves the protocol, not the operator" stated | ✓ PASS | |

**CLAUDE.md: PASS ✓**

### BANZAI_REFERENCE.md (canonical Protocol OS reference)

| Check | Status | Notes |
|-------|--------|-------|
| Scope limited to Protocol OS | ✓ PASS | |
| Does not redefine protocol rules | ✓ PASS | |
| Hosting vs ownership stated | ✓ PASS | |
| Cross-repo links valid | ✓ PASS | |

**BANZAI_REFERENCE.md: PASS ✓**

### CONTRIBUTING.md

| Check | Status | Notes |
|-------|--------|-------|
| Deterministic-first principle | ✓ PASS | |
| Fork URL correct | ✗ ISSUE | `github.com/banzami/banzamia` — wrong; P2-012 |
| Protocol kernel reference | ✗ ISSUE | `github.com/banzami/banzami` — wrong; P2-011 |

**CONTRIBUTING.md: 1/3 PASS · 2 ISSUES**

---

## ~/banzami — Public Surface

### README.md (critical — 1972 lines)

| Check | Status | Notes |
|-------|--------|-------|
| Header identifies Banzami = reference operator | ✓ PASS | |
| Ecosystem table correct | ✓ PASS | |
| Naming note (ADR-025) accurate | ✓ PASS | |
| Line 13: identity/URL of open-source ecosystem | ✗ FAIL | Assigns BANZA's role to Banzami + wrong URL; P1-005 |
| Body text uses "Banzami" (not "Banza") for operator | ✗ FAIL | "Banza is built with…", "Banza follows…" etc.; P1-004 |
| GitHub URLs throughout body | ✗ ISSUE | Multiple stale `github.com/banzami/` |
| Engineering philosophy describes Banzami | ✗ FAIL | Uses "Banza" — P1-004 |
| Architectural principles describe Banzami | ✗ FAIL | "Banza follows a modular monolith" — P1-004 |

**README public surface: 3/8 PASS · 5 FAILS**

### CLAUDE.md

| Check | Status | Notes |
|-------|--------|-------|
| Ecosystem identity table correct | ✓ PASS | |
| Operator guardrail stated | ✓ PASS | "Never redefine protocol rules locally" |
| Protocol ownership disclaimed | ✓ PASS | |
| SDK-first principle | ✓ PASS | |

**CLAUDE.md: PASS ✓**

### BANZAMI_REFERENCE.md (canonical operator reference)

| Check | Status | Notes |
|-------|--------|-------|
| Scope limited to operator products | ✓ PASS | |
| Protocol invariants cross-referenced not restated | ✓ PASS | |
| "Banzami é um operador entre futuros muitos" | ✓ PASS | |
| Cross-repo links valid | ✓ PASS | |

**BANZAMI_REFERENCE.md: PASS ✓**

---

## Overall Public Surface Summary

| Repository | Canonical Docs | README | CLAUDE.md | CONTRIBUTING.md |
|------------|---------------|--------|-----------|-----------------|
| ~/banza | ✓ PASS | ⚠ ISSUES | ✓ PASS | ✓ PASS |
| ~/banzai | ✓ PASS | ⚠ ISSUE | ✓ PASS | ✗ ISSUES |
| ~/banzami | ✓ PASS | ✗ FAILS | ✓ PASS | n/a |

### Priority fix order for maximum public surface impact

1. `banzami/README.md` — Replace "Banza" → "Banzami" in body (P1-004) **HIGH IMPACT**
2. `banzami/README.md:13` — Fix line 13 identity + URL (P1-005) **HIGH IMPACT**
3. `banzai/README.md:27` — Fix capability count 8 → 6 (P1-003) **HIGH IMPACT**
4. `banzai/CONTRIBUTING.md` — Fix URLs (P2-011, P2-012) **MEDIUM IMPACT**
5. `banza/README.md` — Fix naming note, stale URLs (P1-002, P2-002–P2-003) **MEDIUM IMPACT**
6. All stale `github.com/banzami/` URLs — batch replace **LOW IMPACT** (users don't navigate to these)

---

*Produced by: ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001 — 2026-05-30*
