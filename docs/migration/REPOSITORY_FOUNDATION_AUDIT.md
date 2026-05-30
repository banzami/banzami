---
title: REPOSITORY_FOUNDATION_AUDIT
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: CANONICAL-REPOSITORY-FOUNDATION-001
---

# Repository Foundation Audit

**Scope:** Root-level governance files in ~/banza, ~/banzai, ~/banzami  
**Purpose:** Identify all missing, outdated, and conflicting root files before standardization.

---

## 1. Inventory

### ~/banza

| File | Exists | ADR-025 Aligned | Status |
|------|--------|----------------|--------|
| README.md | ✓ | ⚠ Partial | Old GitHub URLs, missing ecosystem hierarchy header |
| CLAUDE.md | ✓ | ✓ | Aligned — new session opens correctly |
| CONTRIBUTING.md | ✓ | ⚠ Partial | Wrong repo URLs in clone instructions |
| CODE_OF_CONDUCT.md | ✓ | ✓ | Contributor Covenant — no ADR-025 content |
| SECURITY.md | ✓ | ⚠ Minor | Out-of-scope note mentions "Banzami commercial product" correctly |
| LICENSE | ✓ | ✓ | Apache 2.0 |
| GOVERNANCE.md | ✓ | ✗ P0 CRITICAL | "governed by Banzami (the organization)" — complete ADR-016 inversion |
| BANZA_REFERENCE.md | ✓ | ✓ | Canonical protocol reference — aligned |
| .github/workflows/conformance.yml | ✓ | ✓ | Conformance test automation |
| .github/ISSUE_TEMPLATE/ | ✗ | — | Missing |
| .github/PULL_REQUEST_TEMPLATE.md | ✗ | — | Missing |

### ~/banzai

| File | Exists | ADR-025 Aligned | Status |
|------|--------|----------------|--------|
| README.md | ✓ | ✗ P1 | Multiple pre-rename issues (old URLs, BANZAMIA_MODE, CLI name) |
| CLAUDE.md | ✓ | ✓ | Aligned — new session opens correctly |
| CONTRIBUTING.md | ✓ | ✓ | Good content, deterministic-first principle preserved |
| CODE_OF_CONDUCT.md | ✗ | — | MISSING |
| SECURITY.md | ✓ | ✓ | Correctly scoped to BanzAI |
| LICENSE | ✓ | ✓ | Apache 2.0 |
| GOVERNANCE.md | ✗ | — | MISSING |
| BANZAI_REFERENCE.md | ✓ | ✓ | Canonical BanzAI reference — aligned |
| .github/ | ✗ | — | MISSING — no workflows, no templates |

### ~/banzami

| File | Exists | ADR-025 Aligned | Status |
|------|--------|----------------|--------|
| README.md | ✓ | ⚠ Partial | "Private Commercial Product" framing, missing ecosystem position |
| CLAUDE.md | ✓ | ✓ | Aligned — new session opens correctly |
| CONTRIBUTING.md | ✗ | — | MISSING |
| CODE_OF_CONDUCT.md | ✗ | — | MISSING |
| SECURITY.md | ✗ | — | MISSING |
| LICENSE | ✗ | — | MISSING |
| GOVERNANCE.md | ✗ | — | MISSING |
| BANZAMI_REFERENCE.md | ✓ | ✓ | Canonical operator reference — aligned |
| .github/workflows/ci.yml | ✓ | ✓ | Rust + Go CI pipeline |
| .github/ISSUE_TEMPLATE/ | ✗ | — | Missing |
| .github/PULL_REQUEST_TEMPLATE.md | ✗ | — | Missing |

---

## 2. Severity Classification

### P0 — Protocol Identity Crisis (must fix before any publication)

| Finding | File | Issue |
|---------|------|-------|
| P0-001 | `banza/GOVERNANCE.md` | "Banza is governed by Banzami (the organization)" — states the protocol is owned by the operator. Directly contradicts ADR-025. |

### P1 — Naming Regression (pre-rename language still present)

| Finding | File | Issue |
|---------|------|-------|
| P1-001 | `banzai/README.md` | Ecosystem table URLs reference old `github.com/banzami/*` org. Roles are swapped: banzami described as "protocol kernel", banza described as "commercial operator". |
| P1-002 | `banzai/README.md` | `BANZAMIA_MODE` → should be `BANZAI_MODE` |
| P1-003 | `banzai/README.md` | CLI command `banzamia ask` → should be `banzai ask` |
| P1-004 | `banzai/README.md` | Architecture directory shown as `banzamia/` → should be `banzai/` |
| P1-005 | `banzai/README.md` | Hosted URL `banzami.org/banzamia` → `banzami.org/banzai` |
| P1-006 | `banza/README.md` | Clone URL `github.com/banzami/banzami` → `github.com/banza-protocol/banzami` |
| P1-007 | `banza/CONTRIBUTING.md` | Same old URL in fork instructions |

### P2 — Missing Required Files

| Finding | Repo | Missing file |
|---------|------|-------------|
| P2-001 | ~/banzami | CONTRIBUTING.md |
| P2-002 | ~/banzami | CODE_OF_CONDUCT.md |
| P2-003 | ~/banzami | SECURITY.md |
| P2-004 | ~/banzami | LICENSE |
| P2-005 | ~/banzami | GOVERNANCE.md |
| P2-006 | ~/banzai | CODE_OF_CONDUCT.md |
| P2-007 | ~/banzai | GOVERNANCE.md |
| P2-008 | ~/banzai | .github/ directory and workflows |
| P2-009 | All | .github/ISSUE_TEMPLATE/ |
| P2-010 | All | .github/PULL_REQUEST_TEMPLATE.md |

### P3 — Cosmetic / Improvement

| Finding | File | Issue |
|---------|------|-------|
| P3-001 | `banzami/README.md` | "Private Commercial Product" in title — should be "Reference Operator Implementation" |
| P3-002 | `banza/README.md` | Missing three-tier ecosystem hierarchy header |
| P3-003 | `banzai/README.md` | Missing three-tier ecosystem hierarchy header |
| P3-004 | `banzami/README.md` | Missing three-tier ecosystem hierarchy header |

---

## 3. ADR-025 Forbidden Assumptions in Existing Files

| File | Forbidden assumption found | Severity |
|------|--------------------------|---------|
| `banza/GOVERNANCE.md` | "governed by Banzami" — implies Banzami owns the protocol | P0 |
| `banzai/README.md` | Ecosystem table inverted: banzami = "protocol kernel", banza = "commercial operator" | P1 |
| `banzai/README.md` | `banzami.org/banzamia` URL — still uses old BanzamIA branding | P1 |
| `banza/README.md` | `github.com/banzami/banzami` — old org URL | P1 |

---

## 4. What is NOT a Finding

- `banzami/README.md` calling itself a "private" repository — this is correct, Banzami is proprietary
- `banza/SECURITY.md` referencing `security@banzami.org` — this is a protected name, intentionally unchanged per ADR-025
- The `banzami.org` domain appearing in any file — protected name, not renamed
- `banzami-types`, `banzami-ledger` crate names in any file — explicitly out of scope per ADR-025

---

*Audit produced: 2026-05-30.*
