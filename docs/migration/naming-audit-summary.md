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
| API_ROUTE | ~15 | 2 PROTECTED, rest rename | Critical (for protected) |
| PUBLIC_COPY | ~80 | Rename per wave | Medium |
| SVG_TEXT | ~40 | Rename in Wave 2 (with exceptions) | Low–Medium |
| TEST_FIXTURE | ~15 | Rename with code symbols | Low |

---

## Protected Occurrences (must never rename)

| Occurrence | Reason |
|------------|--------|
| `banzami.org` (and all subdomains) | Registered domain |
| `contact@banzami.org`, `security@banzami.org` | Email addresses |
| `github.com/banzami` org | GitHub organization |
| `/.well-known/banzami/operator.json` | Protocol wire contract (C-007: RESOLVED KEEP) |
| `BANZAMI-SBX:` QR prefix | Protocol wire format (C-008: RESOLVED KEEP) |
| `BANZAMI:` QR prefix | Protocol wire format (C-008: RESOLVED KEEP) |
| `Banzami Lda` (legal entity name in formal docs) | Legally binding |

**Total protected occurrences: ~50**

---

## Safe Occurrences (can rename without conflict)

These occurrences have no external consumers and no ambiguity. They can be renamed as soon as the corresponding wave begins.

| Occurrence | Target | Wave |
|------------|--------|------|
| ADR prose text (all non-016 ADRs) | Banzami → Banza | 1 |
| RFC prose text (protocol strings excluded) | Banzami → Banza | 1 |
| GOVERNANCE.md, CONTRIBUTING.md | Banzami → Banza | 1 |
| Architecture SVG labels (non-protocol strings) | Banzami → Banza; BanzamIA → BanzAI | 2 |
| BanzamIA React component symbols | BanzamIA* → BanzAI* | 4 |
| BanzamIA UI text strings | BanzamIA → BanzAI | 4 |
| BANZAMIA_* env vars (internal) | → BANZAI_* | 5 |
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

**Score: 68 / 100**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Planning completeness | 95/100 | ADR, map, classification rules, conflict register all complete |
| Critical conflict resolution | 40/100 | 3 of 7 conflicts unresolved (C-001, C-002, C-004 are wave blockers) |
| Protected items identified | 100/100 | All protocol wire format items confirmed and protected |
| Safe rename scope defined | 90/100 | ~120 files identified as safe; classification complete |
| Wave sequencing | 85/100 | Waves defined; repo swap sequencing (Wave 8) still needs separate ADR |
| SDK strategy | 30/100 | C-001 unresolved — critical since SDK renames are the highest-risk action |
| Domain/repo strategy | 20/100 | Wave 8 deferred; no ADR yet for repo renames |

**Composite: 68/100**

---

## Recommendation

> **More decisions required before Wave 3 can begin.**

### What must be decided before Wave 1–2 (low-risk waves)

None — Wave 1 (documentation) and Wave 2 (SVGs) can begin immediately. No conflicts block these waves. All PROTOCOL and AI_OS prose renames are safe.

### What must be decided before Wave 3

**C-004 must be resolved:** Does `/banzamia` become `/banzai` with a redirect, or does the URL stay as `/banzamia`? This is the only Wave 3 blocker.

### What must be decided before Wave 6

**C-001 must be resolved:** If `@banza/sdk` stays (recommended), then `BanzaClient`, `BanzaError`, and `BanzaPay` also stay — Wave 6 becomes documentation-only (Low risk). If `@banza/sdk` renames, Wave 6 requires breaking SDK releases (Critical risk).

This single decision dramatically changes Wave 6 complexity.

### What must be decided before Wave 8

A separate ADR (ADR-026) for repository rename sequencing is required. The "swap problem" (kernel wants `banza`, operator is currently `banza`) requires a temporary intermediate name.

---

## Readiness for Wave 1

**✅ READY FOR WAVE 1 NOW**

Wave 1 (documentation prose) can begin immediately. No conflict resolution is required. ~30–40 files, all PROTOCOL and AI_OS class, all internal.

Recommended first action: Resolve C-001 and C-004 while Wave 1 is in progress, so Wave 3 can follow without delay.
