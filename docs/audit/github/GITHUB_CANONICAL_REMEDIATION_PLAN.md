---
title: GITHUB_CANONICAL_REMEDIATION_PLAN
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: GITHUB-CANONICAL-IDENTITY-001
---

# GitHub Canonical Remediation Plan

**Mission:** GITHUB-CANONICAL-IDENTITY-001  
**Date:** 2026-05-30  
**Scope:** `github.com/banza-protocol` — org, banza, banzai, banzami repos

---

## Wave 0 — Immediate (no dependencies, no migration risks)

These fixes affect only text content. No code changes. No breaking changes. No ADR-025 protected elements.

### W0-001 — Fix org profile README

**File:** `banza-protocol/.github` → `profile/README.md`  
**Problem:** Titled `# Banzami`, describes Banzami as "protocol-first, open-source financial kernel."  
**Fix:** Rewrite to represent the Banza protocol.

Canonical structure:
```markdown
# Banza Protocol

Open financial infrastructure for programmable payments, operators and settlement systems.

| Repository | Role |
|------------|------|
| [banza](https://github.com/banza-protocol/banza) | Open financial kernel — protocol, Rust core, SDKs, conformance |
| [banzai](https://github.com/banza-protocol/banzai) | BanzAI — Protocol Operating System |
| [banzami](https://github.com/banza-protocol/banzami) | Banzami — Reference operator (private) |

BANZA is the protocol.
BanzAI is the Protocol OS.
Banzami is the first operator.
```

**Priority:** CRITICAL  
**Effort:** 30 minutes  
**Risk:** None

---

### W0-002 — Fix banzai repo description

**Location:** GitHub repo settings → Description  
**Current:** "AI-native interface and orchestration layer for the Banzami ecosystem."  
**Fix:** "Protocol Operating System for the Banza financial infrastructure ecosystem."  
**Priority:** HIGH  
**Effort:** 2 minutes  
**Risk:** None

---

### W0-003 — Fix banzami repo description

**Location:** GitHub repo settings → Description  
**Current:** "First commercial operator built on the Banzami financial infrastructure kernel."  
**Fix:** "First commercial operator built on the Banza financial infrastructure kernel."  
**Priority:** HIGH  
**Effort:** 2 minutes  
**Risk:** None

---

### W0-004 — Fix banzai topic

**Location:** GitHub repo settings → Topics  
**Current:** includes `banzami`  
**Fix:** Replace `banzami` with `banza` and `banza-protocol`  
**Priority:** MEDIUM  
**Effort:** 2 minutes  
**Risk:** None

---

### W0-005 — Fix GOVERNANCE.md — attribution language

**File:** `banza-protocol/banza` → `GOVERNANCE.md`  
**Fixes:**
1. "Banza is governed by **Banzami** (the organization)" → "Banza is governed through the ADR process and maintained as a community open-source project."
2. "The Banza protocol is stewarded by **Banzami** (the organization)" → "The Banza protocol is stewarded by its maintainers through the governance process defined in this document."
3. Maintainers section: "The project is maintained by [Banza](https://banzami.org)" → "The project is maintained by the Banza protocol maintainers. Contact: [contact@banzami.org](mailto:contact@banzami.org)" (PROTECTED email preserved)

**Priority:** HIGH  
**Effort:** 15 minutes  
**Risk:** None

---

### W0-006 — Mark ADR-016 as superseded

**File:** `banza-protocol/banza` → `docs/adr/ADR-016-banzami-banza-brand-architecture.md`  
**Fix:** Change `**Status:** Accepted` to `**Status:** Superseded by ADR-025 (2026-05-29)`  
**Add at top of document:**
```
> ⚠️ This ADR has been superseded by [ADR-025](ADR-025-ecosystem-naming-inversion.md). Do not apply the naming rules in this document — use ADR-025 instead.
```
**Priority:** MEDIUM  
**Effort:** 5 minutes  
**Risk:** None

---

### W0-007 — Fix banzami README — "Banza" used to mean "Banzami"

**File:** `banza-protocol/banzami` → `README.md`  
**Fixes:**
- "Banza is built with: fintech-grade agility..." → "Banzami is built with..."
- "Banza follows a modular monolith architecture..." → "Banzami follows..."
- "Banza is building the digital payment layer for Angola..." → "Banzami is building..."
- "Banza is an API-first infrastructure layer" → "Banzami is an API-first infrastructure layer"
- "Product Vision: Banza is building..." → "Banzami is building..."

**Priority:** MEDIUM  
**Effort:** 20 minutes  
**Risk:** None

---

### W0-008 — Fix banzami README — "Banzami SDKs" reference

**File:** `banza-protocol/banzami` → `README.md`  
**Current:** "External integrations use official Banzami SDKs."  
**Fix:** "External integrations use official Banza protocol SDKs. See [github.com/banza-protocol/banza](https://github.com/banza-protocol/banza)."  
**Priority:** LOW  
**Effort:** 5 minutes  
**Risk:** None

---

## Wave 1 — GitHub content sync (requires local → GitHub push)

These items reflect local migration work (BANZA-STRUCTURAL-NAMING-MIGRATION-001) that has not yet been pushed to the `banza-protocol` org repositories.

### W1-001 — Push BANZA_REFERENCE.md rename to banza repo

**Problem:** `banza-protocol/banza` shows `docs/BANZAMI_REFERENCE.md`. Local Banza repo has been migrated to `docs/BANZA_REFERENCE.md`.  
**Action:** Push the Phase 3 migration commit to the `banza-protocol/banza` remote.  
**Priority:** MEDIUM  
**Risk:** Downstream: `lib/reference.ts` reads `BANZA_REFERENCE.md` — this change must be coordinated with the Dockerfile and deploy.sh (already done in local migration).

---

### W1-002 — Push BanzAI URL updates to banza repo README

**Problem:** banza README references `banzami.org/banzamia` — local migration moved to `banzami.org/banzai`.  
**Action:** Push Phase 4 changes.  
**Priority:** MEDIUM  
**Risk:** None (URLs are already live with 301 redirects in place).

---

### W1-003 — Push BANZAI_MODE env var updates to banzai repo README

**Problem:** banzai README shows `BANZAMIA_MODE=live-api-no-model` — local migration uses `BANZAI_MODE`.  
**Action:** Push Phase 1 migration content to banzai repo.  
**Priority:** MEDIUM  
**Risk:** Backward compat aliases ensure no breakage.

---

### W1-004 — Update banzai CLI name in README

**Problem:** banzai README shows `banzamia ask`, `banzamia certify`, etc.  
**Action:** Update CLI documentation to `banzai ask`, `banzai certify`, etc.  
**Priority:** MEDIUM  
**Risk:** Depends on actual CLI binary name in the banzai repo.

---

## Wave 2 — Protocol independence statement (new content)

### W2-001 — Add protocol survivability statement

**Where:** banza README, GOVERNANCE.md, org profile README  
**Content to add:**
```
The Banza protocol exists independently of any operator. If Banzami (or any operator)
ceases operations, the protocol specifications, contracts, SDKs, conformance suite, and
certification framework remain fully available to all operators.
```
**Priority:** MEDIUM  
**Effort:** 30 minutes  
**Risk:** None — this is a statement of architectural fact

---

### W2-002 — Add certification independence note to GOVERNANCE.md

**Where:** `banza-protocol/banza` → `GOVERNANCE.md`  
**Content to add** (new section):
```markdown
## Certification independence

Operator certification (L0–L4) is performed by BanzAI using deterministic conformance
tools. The certification rules are defined by protocol contracts — not by any single
operator. Banzami, as the first and current reference operator, has no special authority
over the certification process. Any operator passing the conformance suite is
considered Banza-compatible, regardless of their relationship with Banzami.
```
**Priority:** MEDIUM  
**Effort:** 20 minutes  
**Risk:** None

---

## Wave 3 — Deferred (per ADR-025 — requires separate ADR)

These items are PROTECTED by ADR-025 and require a follow-on decision before action.

| Item | Required action | Depends on |
|------|----------------|------------|
| GitHub org rename `banzami` → `banza-protocol` | All clone URLs change — major migration | Separate ADR |
| Domain migration `banzami.org` → `banza.org` or dual-domain | SEO impact, DNS migration | Separate ADR |
| Email migration `@banzami.org` → `@banza-protocol.org` or similar | All public communications | Separate ADR |
| Crate names `banzami-*` → `banza-*` | SDK breaking change, major version bump | ADR + deprecation period |

---

## Remediation Priority Matrix

| Priority | Items | Effort | Risk |
|----------|-------|--------|------|
| CRITICAL | W0-001 (org profile README) | 30 min | None |
| HIGH | W0-002, W0-003, W0-005 | 20 min | None |
| MEDIUM | W0-004, W0-006, W0-007, W1-001 through W1-004, W2-001, W2-002 | 2–3 hours | None |
| LOW | W0-008 | 5 min | None |
| DEFERRED | W3-* | — | Requires ADR |

---

## Execution Order (Recommended)

1. **Start with W0-001** — the org profile README is the most visible failure and requires only text editing. It must be corrected before any other surface.
2. **W0-002 + W0-003** — repo descriptions are two-minute fixes visible on every org page.
3. **W0-005** — GOVERNANCE.md correction; this removes the most structurally damaging language.
4. **W0-006** — ADR-016 superseded status; prevents future contributors from following wrong guidance.
5. **W0-007 + W0-008** — Banzami README cleanup; lower urgency (private repo).
6. **W1-001 through W1-004** — GitHub sync of local migration work; requires push to remote.
7. **W2-001 + W2-002** — New content; can wait until Wave 0 and Wave 1 are complete.
8. **W3-*** — Defer until separate ADR decisions.

---

*Plan complete: 2026-05-30. No files modified. All actions are proposals — no changes have been applied.*
