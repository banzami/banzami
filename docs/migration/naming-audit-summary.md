# Naming Inversion — Audit Summary

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Auditor:** BANZA-NAMING-INVERSION-STEP-002

---

## Audit Scope

Three repositories:

| Repo | Path | Stack |
|------|------|-------|
| Banzami (kernel) | `/Users/fm65/Banzami` | Rust, Go, TypeScript |
| BanzamIA (AI OS) | `/Users/fm65/BanzamIA` | TypeScript, Python |
| Banza (operator/docs) | `/Users/fm65/Banza` | TypeScript, Go, Markdown |

---

## Total Occurrences

| Category | Count |
|----------|-------|
| **Total files with naming occurrences** | **~220** |
| Banzami kernel repo | ~36 files |
| BanzamIA AI OS repo | ~44 files |
| Banza operator repo | ~140 files |
| Total distinct env vars to rename | 11 |
| Total Rust crates to rename | 21 |
| Total React components to rename | 5 |
| Total published npm packages affected | 3 |
| Total published non-npm packages affected | 2 (pub.dev, Composer) |

---

## Occurrences by Class

| Class | Count (files) | Rename action | Risk |
|-------|--------------|---------------|------|
| PROTOCOL | ~80 | Banzami → Banza | Low |
| PRODUCT | ~60 | Banza → Banzami | Medium |
| AI_OS | ~44 | BanzamIA → BanzAI | Medium |
| ORG | ~10 | Confirm with founder | Low |
| DOMAIN | ~30 | PROTECTED | — |
| EMAIL | ~5 | PROTECTED | — |
| REPO | ~8 | DEFERRED | Critical |
| PACKAGE | ~29 | Mixed (see conflicts) | Critical |
| ENV_VAR | 11 | BANZAMIA_* → BANZAI_* | High |
| CODE_SYMBOL | ~30 | Mixed (see conflicts) | Medium–Critical |
| DATABASE | 0 | No action | — |
| API_ROUTE | ~15 | All rename (with compatibility window); wire format in Wave 5c | High |
| PUBLIC_COPY | ~80 | Rename per wave | Medium |
| SVG_TEXT | ~40 | Rename in Wave 2 (with exceptions) | Low–Medium |
| TEST_FIXTURE | ~15 | Rename with code symbols | Low |

---

## Protected Occurrences (must never rename)

**STEP-002B override:** `/.well-known/banzami/operator.json` and QR prefixes are no longer permanently protected — they migrate in Wave 5c.

| Occurrence | Reason |
|------------|--------|
| `banzami.org` (and all subdomains) | Registered domain — **PROTECTED** |
| `contact@banzami.org`, `security@banzami.org` | Email addresses — **PROTECTED** |
| `github.com/banzami` org | GitHub organization — separate ADR required |
| `Banzami Lda` (legal entity name in formal docs) | Legally binding text |

**Total permanently protected occurrences: ~35** (reduced from ~50 by removing wire format from protected list)

---

## Safe Occurrences (can rename without conflict)

These occurrences have no external consumers and no ambiguity. They can be renamed as soon as the corresponding wave begins.

| Occurrence | Target | Wave |
|------------|--------|------|
| ADR prose text (all non-016 ADRs) | Banzami → Banza | 1 |
| RFC prose text (excluding wire format identifier strings) | Banzami → Banza | 1 |
| GOVERNANCE.md, CONTRIBUTING.md | Banzami → Banza | 1 |
| Architecture SVG labels (diagram text) | Banzami → Banza; BanzamIA → BanzAI | 2 |
| BanzamIA React component symbols | BanzamIA* → BanzAI* | 4 |
| BanzamIA UI text strings | BanzamIA → BanzAI | 4 |
| BANZAMIA_* env vars (internal) | → BANZAI_* | 5a |
| QR generator prefix | BANZAMI: → BANZA:; BANZAMI-SBX: → BANZA-SBX: | 5c |
| Operator manifest path | /.well-known/banzami/ → /.well-known/banza/ (+ redirect) | 5c |
| All 21 banzami-* Rust crates (unpublished) | → banza-* | 7 |
| Internal SDK (checkout-web): BanzamiApiError | → BanzaApiError | 6 |

**Total safe occurrences: ~120 files**

---

## High-Risk Occurrences

Occurrences that require coordination, deprecation, or sequencing decisions:

| Occurrence | Risk | Reason |
|------------|------|--------|
| `BanzaClient` (TypeScript/PHP SDK, published) | Critical | Breaking API change for SDK consumers |
| `BanzaError` (TypeScript SDK, published) | Critical | Breaking API change |
| `BanzaPay` (Flutter, published) | Critical | Breaking API change |
| `@banza/sdk` (npm scope) | Critical | Published — may not need rename (C-001) |
| `banza_flutter` (pub.dev) | Critical | Published |
| `banza/sdk-php` (Composer) | Critical | Published |
| GitHub repo names | Critical | All clone URLs break |
| `/banzamia` URL route | High | SEO + bookmarks |
| BANZAMIA_* env vars on production | High | Coordinated deploy required |
| Docker service names | High | Live deployment |

**Total high-risk occurrences: ~25 files, ~80 line occurrences**

---

## Critical Conflicts

| ID | Description | Blocks |
|----|-------------|--------|
| C-001 | SDK scope: does `@banza/sdk` stay or become `@banzami/sdk`? | Wave 6 |
| C-002 | `BanzaClient` class: rename or keep? (depends on C-001) | Wave 6 |
| C-004 | `/banzamia` URL path: rename to `/banzai` or keep? | Wave 3 |
| C-007 | `/.well-known/banzami/` URL | **RESOLVED: KEEP AS-IS** |
| C-008 | QR prefixes `BANZAMI-SBX:` / `BANZAMI:` | **RESOLVED: KEEP AS-IS** |

Two conflicts are permanently resolved (C-007, C-008 — protocol wire format, cannot change without RFC). The remaining three (C-001, C-002, C-004) require founder decisions before their respective waves begin.

---

## Migration Readiness Score

**Score: 82 / 100** *(updated from 68/100 after STEP-002B)*

| Dimension | Score | Notes |
|-----------|-------|-------|
| Planning completeness | 98/100 | ADR, map, classification rules, conflict register, breaking migration doc all complete |
| Critical conflict resolution | 80/100 | C-001, C-002, C-004, C-007, C-008, C-009 resolved. C-003, C-005, C-006 unresolved (low stakes) |
| Protected items identified | 100/100 | Domains/emails protected; wire format correctly marked for migration |
| Safe rename scope defined | 92/100 | ~130 files identified as safe; wire format now included |
| Wave sequencing | 90/100 | Wave 5 split into 5a/5b/5c; repo swap (Wave 8) still needs separate ADR |
| SDK strategy | 90/100 | C-001 resolved: no breaking class renames; Wave 6 is mostly documentation |
| Domain/repo strategy | 20/100 | Wave 8 deferred; no ADR yet for repo renames |
| Wire format strategy | 85/100 | Breaking protocol migration documented; compatibility strategy defined |

**Composite: 82/100**

---

## Recommendation

> **✅ Ready to begin Wave 1 now. All major blockers resolved.**

### What must be decided before Wave 1–2 (low-risk waves)

Nothing. Wave 1 (documentation) and Wave 2 (SVGs) can begin immediately.

### What must be decided before Wave 3

Nothing. C-004 resolved: canonical route is `/banzai`. Proceed after Wave 2.

### What must be decided before Wave 5c (wire format)

Nothing — C-007 and C-008 resolved by STEP-002B. Read `naming-breaking-protocol-migration.md` before executing; test requirements are mandatory.

### What must be decided before Wave 6 (SDKs)

Nothing — C-001 and C-002 resolved. Wave 6 is primarily documentation updates, not breaking releases. Python SDK `BanzamiAuthenticationError` rename is the only code change.

### What must be decided before Wave 8 (repos)

A separate ADR (ADR-026) for repository rename sequencing. The "swap problem" requires temporary intermediate names. This is the only remaining unresolved high-stakes item.

### Remaining unresolved (all low stakes, non-blockers)

| Conflict | Stakes | Recommendation |
|----------|--------|----------------|
| C-003 BanzamIA root package | Low — internal only | Defer to Wave 8 |
| C-005 Component directory name | Low | Defer to Wave 9 |
| C-006 BANZAMI_REFERENCE.md filename | Medium | Rename to PROTOCOL_REFERENCE.md (Wave 9) |

---

## Readiness for Wave 1

**✅ READY FOR WAVE 1 NOW**

Wave 1 (documentation prose) can begin immediately. ~30–40 files, all PROTOCOL and AI_OS class, all internal. No further decisions required.
