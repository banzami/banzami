---
title: CANONICAL_STRUCTURAL_MIGRATION_REPORT
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: BANZA-STRUCTURAL-NAMING-MIGRATION-001
---

# Canonical Structural Migration Report

**Mission:** BANZA-STRUCTURAL-NAMING-MIGRATION-001
**Completed:** 2026-05-30

---

## Summary

Five phases executed. All structural names now reflect the ADR-025 identity model:

- **BANZA** = protocol (owns the reference document)
- **BanzAI** = Protocol Operating System (has its own routes, components, backend service)
- **Banzami** = reference operator (has its own apps, brand assets, mobile apps)

---

## Phase 0 — Navigation Bug Fix

**Commit:** `fix(reference-navigation): remove section-number BanzAI routing`

**Problem:** `SectionCard.tsx` and `SectionNav.tsx` hardcoded `section.number === 11` to route to `/sobre-banzamia`. Section numbers are positional and shifted after the §§1–3 integration — this was the same class of bug that broke production twice.

**Fix:** Replaced with `section.slug === 'banzai'`. Slugs are entity-stable identifiers derived from section titles and will not shift during re-numbering.

**Regression test added:** `reference.test.ts` now asserts that the BanzAI section has slug `banzai` and title `BanzAI` — any future re-numbering that changes this will be caught immediately.

---

## Phase 1 — Backend Internal Migration (Banzami repo)

**Commit:** `refactor(banzai): rename backend service internals from banzamia to banzai`

| Before | After |
|---|---|
| `apps/banzamia/` | `apps/banzai/` |
| `docker/banzamia/` | `docker/banzai/` |
| `package.json "name": "banzamia"` | `"name": "banzai"` |
| `"description": "BanzamIA — AI-native protocol agent..."` | `"BanzAI — Protocol Operating System"` |
| `BanzamIAMode` type | `BanzAIMode` type |
| Container: `banzamia-api` | Container: `banzai-api` |
| Container: `banzamia-qdrant` | Container: `banzai-qdrant` |
| Docker service: `banzamia:` | Docker service: `banzai:` |

**Env var backward compatibility:** `config.ts` reads `BANZAI_*` first, falls back to `BANZAMIA_*`. Existing server deployments using `BANZAMIA_MODE` etc. continue working without changes. Both sets of env vars are passed through in `docker-compose.yml`.

**Validation:** TypeScript build clean. 107/107 tests pass.

---

## Phase 2 — Frontend Internal Migration (Banza repo)

**Commit:** `refactor(banzai): rename frontend internals from banzamia to banzai`

| Before | After |
|---|---|
| `components/banzamia/` | `components/banzai/` |
| `lib/banzamia-client.ts` | `lib/banzai-client.ts` |
| `HeroBanzamIAWidget.tsx` | `HeroBanzAIWidget.tsx` |
| `BanzamIAApp.tsx` | `BanzAIApp.tsx` |
| `BanzamIAChat.tsx` | `BanzAIChat.tsx` |
| `BanzamIASidebar.tsx` | `BanzAISidebar.tsx` |
| `BanzamIAIcon.tsx` | `BanzAIIcon.tsx` |
| `BanzamIASourcesPanel.tsx` | `BanzAISourcesPanel.tsx` |
| `HomeBanzamIAEntry.tsx` | `HomeBanzAIEntry.tsx` |
| Export: `BanzamIAApp` | Export: `BanzAIApp` |
| Export: `BanzamIAPage` | Export: `BanzAIPage` |
| Export: `SobreBanzamiaPage` | Export: `SobreBanzAIPage` |
| Const: `BANZAMIA_API_URL` | Const: `BANZAI_API_URL` |
| Env: `NEXT_PUBLIC_BANZAMIA_API_URL` (sole) | Reads `NEXT_PUBLIC_BANZAI_API_URL` first, falls back to `NEXT_PUBLIC_BANZAMIA_API_URL` |

**Public routes unchanged in this phase.** Dockerfile and deploy.sh updated to pass both `NEXT_PUBLIC_BANZAI_API_URL` and `NEXT_PUBLIC_BANZAMIA_API_URL` as build args — existing server configs continue working.

**Validation:** TypeScript clean. 52/52 tests pass.

---

## Phase 3 — Reference File Rename

**Commits:**
- `refactor(reference): rename canonical reference to BANZA_REFERENCE.md` (Banza repo)
- `refactor(reference): update BANZA_REFERENCE.md path in BanzAI backend` (Banzami repo)

| Before | After |
|---|---|
| `docs/BANZAMI_REFERENCE.md` | `docs/BANZA_REFERENCE.md` |

**Files updated (cascade):**
- `apps/docs/lib/reference.ts` — `REFERENCE_PATH` constant (build-critical)
- `apps/docs/Dockerfile` — `COPY docs/BANZA_REFERENCE.md` (build-critical — initial deploy failed because this was missed)
- `deploy.sh` — rsync source path
- `CLAUDE.md`, `docs/README.md`, ADR-015, ADR-016, all doc references
- `apps/docs/app/sobre-o-banzai/page.tsx` — footer attribution `§11`
- `apps/docs/app/[section]/page.tsx` — source comment
- `apps/banzai/src/rag/loader.ts` — RAG ingestion path
- `apps/banzai/src/graph/indexer.ts` — authority mapping
- `apps/banzai/evals/benchmark-runner.ts`, `adversarial-eval.ts` — eval fixtures
- `apps/banzai/evals/datasets/protocol-questions.json` — 50+ `expected_sources` entries

**Validation:** TypeScript clean. 52/52 frontend tests pass. 107/107 backend tests pass.

---

## Phase 4 — Public Route Migration

**Commit:** `feat(routes): migrate BanzAI public routes with 301 redirects`

| Before | After |
|---|---|
| `/banzamia` | `/banzai` |
| `/sobre-banzamia` | `/sobre-o-banzai` |
| `app/banzamia/` | `app/banzai/` |
| `app/sobre-banzamia/` | `app/sobre-o-banzai/` |

**Redirects registered in `next.config.ts`:**
```
/banzamia         → /banzai          (301 permanent)
/sobre-banzamia   → /sobre-o-banzai  (301 permanent)
```

All existing external links, bookmarks, and indexed URLs continue to work via HTTP 301.

**Internal links updated:**
- `layout.tsx` nav
- `SectionCard.tsx`, `SectionNav.tsx`
- `BanzAISidebar.tsx`, `HomeBanzAIEntry.tsx`, `HeroBanzAIWidget.tsx`
- `QuickAnswerCard.tsx` deeplinks (`/banzai?question=...`)
- `roadmap/page.tsx`
- `[section]/page.tsx` `STATIC_ROUTE_OVERRIDES`
- `deploy.sh` ALL_SERVICES: `banzamia-api` → `banzai-api`

**Deployed:** `./deploy.sh docs-frontend` — clean build on server.

---

## Phase 5 — Final Validation

### Filesystem (canonical state)

```
Banza repo:
  docs/
    BANZA_REFERENCE.md           ← Protocol owns the reference
  apps/docs/
    app/
      banzai/                    ← /banzai route (BanzAI live interface)
      sobre-o-banzai/            ← /sobre-o-banzai route (About BanzAI)
    components/
      banzai/                    ← BanzAI components
        BanzAIApp.tsx
        BanzAIChat.tsx
        BanzAISidebar.tsx
        BanzAIIcon.tsx
        BanzAISourcesPanel.tsx
        HomeBanzAIEntry.tsx
        modules/                 ← 16 BanzAI modules
    lib/
      banzai-client.ts           ← BanzAI API client

Banzami repo:
  apps/
    banzai/                      ← BanzAI backend engine
  docker/
    banzai/                      ← BanzAI Docker config
      docker-compose.yml         (service: banzai, container: banzai-api)
      Dockerfile
```

### Residual hits (classified)

| Hit | Location | Classification |
|---|---|---|
| `NEXT_PUBLIC_BANZAMIA_API_URL` | `deploy.sh`, `banzai-client.ts`, `Dockerfile` | **PROTECTED — deprecated alias, intentional backward compat** |
| `BANZAMIA_*` env vars | `docker-compose.yml` env section | **PROTECTED — deprecated aliases for existing server configs** |
| `github.com/banzami/banzamia` | `banzai-client.ts:868` demo data | **LEGACY — GitHub repo URL in demo citation data, not a structural name** |
| `banzamia.org` | Various brand references | **CORRECT — this is the operator domain, not the protocol** |
| `banzami-*` container names | `docker-compose.yml` for non-BanzAI services | **CORRECT — Banzami is the operator, these are operator infrastructure names** |
| `com.banzami.*` | Mobile app package IDs | **CORRECT — Banzami is the operator, package IDs belong to the operator** |

### No structural name survives that:
- Implies Banzami owns the protocol reference ✓
- Implies BanzamIA is still the AI system name ✓
- Routes users to `/banzamia` without redirect ✓
- Routes users to `/sobre-banzamia` without redirect ✓

### Mental model from directory structure (achieved)

```
BANZA_REFERENCE.md   → BANZA = protocol (owns the reference)
apps/banzai/         → BanzAI = Protocol Operating System
components/banzai/   → BanzAI = Protocol Operating System
app/banzai/          → BanzAI has its own public route
app/sobre-o-banzai/  → BanzAI has its own about page
Banzami apps/        → Banzami = reference operator
```

---

## Commits (in order)

**Banza repo:**
1. `fix(reference-navigation)` — Phase 0: slug-based routing
2. `refactor(banzai)` — Phase 2: frontend internals
3. `refactor(reference)` — Phase 3: BANZA_REFERENCE.md rename cascade
4. `fix(dockerfile)` — Phase 3 hotfix: Dockerfile COPY path
5. `feat(routes)` — Phase 4: public route migration with 301 redirects

**Banzami repo:**
1. `refactor(banzai)` — Phase 1: backend service internals
2. `refactor(reference)` — Phase 3: backend reference path updates

---

*Migration complete: 2026-05-30. Production deployed.*
