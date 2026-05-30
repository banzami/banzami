---
title: REPOSITORY_STANDARDIZATION_PLAN
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: CANONICAL-REPOSITORY-FOUNDATION-001
---

# Repository Standardization Plan

**Purpose:** Specify every action required to bring all three repositories to a consistent, ADR-025-aligned foundation state.

---

## Execution Order

Actions are ordered by severity: P0 first, then P1, then missing files, then .github templates.

---

## Wave 1 — P0 Fixes (critical identity issues)

### W1-001 — Fix banza/GOVERNANCE.md

**File:** `~/banza/GOVERNANCE.md`  
**Issue:** "Banza is governed by Banzami (the organization)" — protocol governed by operator — ADR-025 inversion  
**Action:** Rewrite overview section. Remove "Banzami (the organization)" as governing entity. Replace with open protocol governance model.  
**Risk:** None — text only change  
**Effort:** 15 minutes

---

## Wave 2 — P1 Fixes (naming regressions)

### W2-001 — Fix banzai/README.md

**File:** `~/banzai/README.md`  
**Issues:**
- Ecosystem table: wrong URLs, inverted roles (banzami = protocol, banza = commercial)
- `BANZAMIA_MODE` → `BANZAI_MODE`
- `banzamia ask` → `banzai ask` (CLI command)
- `banzamia/` directory in architecture → `banzai/`
- `banzami.org/banzamia` → `banzami.org/banzai`

**Action:** Fix all occurrences. Retain all technical content.  
**Risk:** None — no code changes  
**Effort:** 20 minutes

### W2-002 — Fix banza/README.md

**File:** `~/banza/README.md`  
**Issues:**
- `github.com/banzami/banzami` → `github.com/banza-protocol/banzami`
- `cd banzami/reference` → `cd banzami` (the reference operator repo)
- Add three-tier ecosystem hierarchy header

**Action:** Fix URLs, add ecosystem header.  
**Risk:** None  
**Effort:** 10 minutes

### W2-003 — Fix banza/CONTRIBUTING.md

**File:** `~/banza/CONTRIBUTING.md`  
**Issues:**
- `git clone https://github.com/banzami/banzami.git` → correct org
- `cd banzami` → `cd banza`

**Action:** Fix URLs.  
**Risk:** None  
**Effort:** 5 minutes

---

## Wave 3 — Create Missing Files (banzami)

### W3-001 — Create banzami/CONTRIBUTING.md

**Scope:** Operator implementation contributions  
**Sections:**
- What you can contribute to: dashboard, SDK wrappers, payment flows, documentation
- What is out of scope: protocol rule changes (see ~/banza), BanzAI internals (see ~/banzai)
- Contribution principles: financial correctness first, operator guardrails
- Branch naming, commit conventions, PR process, testing, documentation

### W3-002 — Create banzami/CODE_OF_CONDUCT.md

**Scope:** Identical to ~/banza/CODE_OF_CONDUCT.md (Contributor Covenant)  
**Action:** Copy with same content

### W3-003 — Create banzami/SECURITY.md

**Scope:** Payment and operator vulnerabilities  
**Sections:**
- Reporting: `security@banzami.org`
- Scope: payment flows, wallet APIs, merchant APIs, consumer APIs, SDK
- Out of scope: protocol invariant definitions (see ~/banza), BanzAI AI safety (see ~/banzai)
- Financial invariant vulnerabilities section

### W3-004 — Create banzami/LICENSE

**Action:** Copy Apache 2.0 from ~/banza/LICENSE  
**Note:** Banzami is a private commercial product — license determines what is open-sourced if Banzami open-sources any component.

### W3-005 — Create banzami/GOVERNANCE.md

**Scope:** Operator governance  
**Sections:**
- Overview: Banzami is governed by the Banzami engineering team as the reference operator implementation of the BANZA protocol
- Decision types: protocol changes (defer to ~/banza ADR process), operator product decisions (internal), API versioning policy
- Deployment governance: deploy.sh governance
- Contact

---

## Wave 4 — Create Missing Files (banzai)

### W4-001 — Create banzai/CODE_OF_CONDUCT.md

**Action:** Copy from ~/banza/CODE_OF_CONDUCT.md with same content

### W4-002 — Create banzai/GOVERNANCE.md

**Scope:** Protocol OS governance  
**Sections:**
- Overview: BanzAI is governed as the cognitive infrastructure layer of the BANZA protocol
- Decision types: protocol content changes (require protocol team review), capability additions, prompt changes, model routing changes
- Deterministic-first governance: changes to certification/conformance logic require explicit protocol team sign-off
- AI safety principles

---

## Wave 5 — .github Templates (all repos)

### W5-001 — Create .github/ISSUE_TEMPLATE/ (all repos)

Templates to create for each repo:
- `bug_report.yml` — structured bug report with reproduction steps
- `feature_request.yml` — structured feature/capability request
- `security_report.md` — security disclosure (routes to email)

Repo-specific additional template:
- `adr_proposal.yml` — for ~/banza only (protocol ADR proposals)

### W5-002 — Create .github/PULL_REQUEST_TEMPLATE.md (all repos)

Standard checklist with repo-specific items.

### W5-003 — Create banzai/.github/workflows/ci.yml

TypeScript/Node.js CI for banzai:
- Type check (tsc --noEmit)
- Lint (eslint)
- Tests (if any)
- Build check

---

## Wave 6 — README ecosystem header (all repos)

Add three-line ecosystem hierarchy to the top of each README (after the H1 title), e.g.:

```
> **BANZA** = open financial infrastructure protocol  
> **BanzAI** = Protocol Operating System ← this repository  
> **Banzami** = reference operator implementation
```

This is the most visible signal that all three repos are part of the same ecosystem.

---

## Success Criteria After Execution

| Criterion | Verifiable by |
|-----------|------------|
| Opening ~/banza immediately reveals its protocol role | Reading first 5 lines of README |
| Opening ~/banzai immediately reveals its Protocol OS role | Reading first 5 lines of README |
| Opening ~/banzami immediately reveals its operator role | Reading first 5 lines of README |
| No README creates protocol/product confusion | Checking for forbidden assumptions |
| No governance file contradicts ADR-025 | Checking GOVERNANCE.md in all repos |
| All repos feel part of the same ecosystem | Ecosystem header present in all READMEs |
| Each repo clearly distinct | CLAUDE.md and *_REFERENCE.md confirm identity |
| Shared governance exists | CODE_OF_CONDUCT and CONTRIBUTING present in all |
| Ownership boundaries explicit | GOVERNANCE.md in all repos |

---

*Plan produced: 2026-05-30.*
