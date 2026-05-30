---
title: CANONICAL_FILENAME_MIGRATION_PLAN
version: 1.0
date: 2026-05-30
status: PLAN — not yet authorized for execution
---

# Canonical Filename Migration Plan

**Purpose:** Ordered migration sequence for aligning the repository structure with ADR-025. Grouped into four waves by dependency order and risk profile.

**Constraint:** Each wave must be completed and verified before the next begins. Wave 3 is the highest-risk wave and requires explicit authorization before execution.

---

## Wave 1 — Internal Infrastructure (Zero Public Impact)

**Goal:** Rename internal backend directories, Docker infrastructure, and package identifiers. No public URLs change. No build pipeline changes. Lowest risk, smallest blast radius.

**Items:** NM-013, NM-015, NM-027, NM-028, NM-029, NM-030

---

### W1-001 — Rename `apps/banzamia/` → `apps/banzai/` (Banzami repo)

**Repo:** Banzami (`/Users/fm65/Banzami`)

**Steps:**
1. `mv apps/banzamia apps/banzai`
2. Update `docker/banzamia/docker-compose.yml` build context: `../../apps/banzamia` → `../../apps/banzai`
3. Update `apps/banzamia/package.json` → `apps/banzai/package.json`: `"name": "banzami"` → `"name": "banzai"`, description to "BanzAI — Protocol Operating System"
4. Update `apps/banzai/tsconfig.json` if it has self-referential paths
5. Update `Banzami/README.md` references to `apps/banzamia/`
6. Update all `QualityModule.tsx` UI strings that display `apps/banzamia` as a code path

**Verification:** `npm run build` in `apps/banzai/`. All 7 tests in `apps/banzai/tests/` pass.

---

### W1-002 — Rename `docker/banzamia/` → `docker/banzai/` (Banzami repo)

**Repo:** Banzami (`/Users/fm65/Banzami`)

**Steps:**
1. `mv docker/banzamia docker/banzai`
2. Update any deploy scripts or CI references to `docker/banzamia/`
3. Update `docker-compose.yml` internal service names: `banzamia` → `banzai`, `banzamia-api` → `banzai-api`, `banzamia-qdrant` → `banzai-qdrant`

**Verification:** `docker compose -f docker/banzai/docker-compose.yml config` validates correctly.

---

### W1-003 — Update `apps/banzamia/package.json` description

**Already covered in W1-001.** Included separately to track the description string:
- `"BanzamIA — AI-native protocol agent for Banzami"` → `"BanzAI — Protocol Operating System for the BANZA protocol"`

---

**Wave 1 commit:** `chore(naming): W1 — rename banzamia → banzai in Banzami repo infrastructure`

---

## Wave 2 — Internal Frontend (No Public URL Change)

**Goal:** Rename frontend components, the client library, SVG filenames, and the BanzAI docs directory. No public routes change. Build will break mid-wave (path changes) and must be validated at end.

**Items:** NM-004, NM-005, NM-006 through NM-012, NM-014, NM-018 through NM-026, NM-031

**Important:** All steps in Wave 2 must be executed as a single atomic commit. Partial execution breaks the build.

---

### W2-001 — Rename `lib/banzamia-client.ts` → `lib/banzai-client.ts`

**Repo:** Banza (`/Users/fm65/Banza`)

**Steps:**
1. `mv apps/docs/lib/banzamia-client.ts apps/docs/lib/banzai-client.ts`
2. Update all 19 import sites: `@/lib/banzamia-client` → `@/lib/banzai-client`
   - `components/banzamia/BanzamIAApp.tsx`
   - `components/banzamia/BanzamIAChat.tsx`
   - `components/banzamia/BanzamIASourcesPanel.tsx`
   - `components/banzamia/HomeBanzamIAEntry.tsx`
   - `components/banzamia/QuickAnswerCard.tsx`
   - `components/banzamia/modules/CertificationCopilotModule.tsx`
   - `components/banzamia/modules/DigitalTwinModule.tsx`
   - `components/banzamia/modules/FederationModule.tsx`
   - `components/banzamia/modules/GraphExplorerModule.tsx`
   - `components/banzamia/modules/MemoryModule.tsx`
   - `components/banzamia/modules/QualityModule.tsx`
   - `components/banzamia/modules/ResearchModule.tsx`
   - `components/banzamia/modules/SimulatorModule.tsx`
   - `components/banzamia/modules/StatusModule.tsx`
   - (any remaining modules)
3. Within the file: rename constant `BANZAMIA_API_URL` → `BANZAI_API_URL` (update all internal usages)
4. Update env variable name in the file: `NEXT_PUBLIC_BANZAMIA_API_URL` → `NEXT_PUBLIC_BANZAI_API_URL`
5. Update the UI mode string in `BanzamIASourcesPanel.tsx`: `"set NEXT_PUBLIC_BANZAMIA_API_URL"` → `"set NEXT_PUBLIC_BANZAI_API_URL"`

**Note on env var:** The environment variable `NEXT_PUBLIC_BANZAMIA_API_URL` must be renamed in any server `.env` or deployment configuration before deploying. Failure to do so will cause the live app to fall back to demo mode silently. Plan a coordinated config update with the code deployment.

---

### W2-002 — Rename React components (BanzamIA* → BanzAI*)

**Repo:** Banza (`/Users/fm65/Banza`)

The component renaming is a find-and-replace within `components/banzamia/` (before the directory itself is renamed).

**Components to rename:**

| File | Current Export | New Export |
|---|---|---|
| `BanzamIAApp.tsx` | `BanzamIAApp`, `ModuleId` type | `BanzAIApp`, `ModuleId` |
| `BanzamIAChat.tsx` | `BanzamIAChat` | `BanzAIChat` |
| `BanzamIAIcon.tsx` | `BanzamIAIcon` | `BanzAIIcon` |
| `BanzamIASidebar.tsx` | `BanzamIASidebar` | `BanzAISidebar` |
| `BanzamIASourcesPanel.tsx` | `BanzamIASourcesPanel` | `BanzAISourcesPanel` |
| `HomeBanzamIAEntry.tsx` | `HomeBanzamIAEntry` | `HomeBanzAIEntry` |
| `HeroBanzamIAWidget.tsx` | `HeroBanzamIAWidget` | `HeroBanzAIWidget` |

**Steps:**
1. Update export names within each file
2. Update all import sites to use new export names
3. Pages affected:
   - `app/banzamia/page.tsx` → imports `BanzamIAApp`, function `BanzamIAPage`
   - `app/page.tsx` → imports `HomeBanzamIAEntry`
   - `components/HeroSection.tsx` → imports `HeroBanzamIAWidget`
   - `components/HeroBanzamIAWidget.tsx` → imports `BanzamIAIcon`
   - `components/banzamia/BanzamIAApp.tsx` → imports `BanzamIASidebar`, `BanzamIAChat`, `BanzamIASourcesPanel`
   - `components/banzamia/BanzamIASidebar.tsx` → imports `BanzamIAIcon`, `type ModuleId`
   - `components/banzamia/BanzamIAChat.tsx` → imports `BanzamIAIcon`

---

### W2-003 — Rename `components/banzamia/` → `components/banzai/`

**Repo:** Banza (`/Users/fm65/Banza`)

**Steps:**
1. `mv apps/docs/components/banzamia apps/docs/components/banzai`
2. Update all import paths: `@/components/banzamia/` → `@/components/banzai/`
   - All pages and components that import from the directory
   - All module files that import from sibling paths (e.g., `./BanzamIAApp`)

**Do after W2-002** to avoid chasing both component names and paths simultaneously.

---

### W2-004 — Rename SVG files (banzamia-* → banzai-*)

**Repo:** Banza (`/Users/fm65/Banza`)

**Steps:**
1. Rename 8 files in both `docs/images/architecture/` and `apps/docs/public/images/architecture/`:
   - `banzamia-canonical-architecture.svg` → `banzai-canonical-architecture.svg`
   - `banzamia-internal-architecture.svg` → `banzai-internal-architecture.svg`
   - `banzamia-cognitive-layer.svg` → `banzai-cognitive-layer.svg`
   - `banzamia-force-multiplier.svg` → `banzai-force-multiplier.svg`
   - `banzamia-knowledge-gap.svg` → `banzai-knowledge-gap.svg`
   - `banzamia-model-routing.svg` → `banzai-model-routing.svg`
   - `banzamia-product-architecture.svg` → `banzai-product-architecture.svg`
   - `banzamia-truth-model.svg` → `banzai-truth-model.svg`
2. Update all 8 image references in `docs/BANZAMI_REFERENCE.md` §11
3. Optionally rename `banzami-ecosystem.svg` → `banza-ecosystem.svg` (lower priority)

---

### W2-005 — Rename `docs/banzamia/` → `docs/banzai/`

**Repo:** Banza (`/Users/fm65/Banza`)

**Steps:**
1. `mv docs/banzamia docs/banzai`
2. Update `docs/index.md` — all relative links `banzamia/*.md` → `banzai/*.md`
3. Update cross-references within the 9 files (e.g., `../banzamia/overview.md` → `../banzai/overview.md`)
4. Update `docs/certification.md`, `docs/conformance.md` references
5. Update any `apps/docs/components/banzamia/modules/QualityModule.tsx` strings that display `docs/banzamia/` as a documentation path

---

### W2-006 — Rename `BANZAMI_ECOSYSTEM_REFERENCE.md`

**Repo:** Banza (`/Users/fm65/Banza`)

**Steps:**
1. `mv docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md docs/architecture/BANZA_ECOSYSTEM_REFERENCE.md`
2. Update `docs/README.md` reference

---

**Wave 2 commit:** `refactor(naming): W2 — rename banzamia → banzai in frontend components, library, SVGs, docs`

**Wave 2 verification:** `npm run build` in `apps/docs/`. 51/51 reference tests pass. 80/80 governance tests pass. Visual audit: `/banzamia` page loads with correct components (route has not yet changed).

---

## Wave 3 — The Critical Rename: BANZAMI_REFERENCE.md → BANZA_REFERENCE.md

**Goal:** Rename the canonical reference document and update every pointer to it. This is the highest-risk and most consequential change in the entire migration.

**Items:** NM-001, NM-032

**This wave requires explicit authorization before execution.** It touches the single source of truth file, the build parser, the ADR that defines the architecture, and dozens of cross-references. A partial execution leaves the build broken.

---

### W3-001 — Rename the file

**Repos:** Both Banza and Banzami

**Steps (must be executed atomically):**

**Step 1 — Update the build parser (first, before the file rename):**
```
apps/docs/lib/reference.ts:14
REFERENCE_PATH = path.join(process.cwd(), '../../docs/BANZAMI_REFERENCE.md')
→ 
REFERENCE_PATH = path.join(process.cwd(), '../../docs/BANZA_REFERENCE.md')
```

**Step 2 — Rename the file:**
```
mv /Users/fm65/Banza/docs/BANZAMI_REFERENCE.md /Users/fm65/Banza/docs/BANZA_REFERENCE.md
mv /Users/fm65/Banzami/docs/BANZAMI_REFERENCE.md /Users/fm65/Banzami/docs/BANZA_REFERENCE.md
```

**Step 3 — Update `docs/README.md`:**
```
[BANZAMI_REFERENCE.md](BANZAMI_REFERENCE.md) → [BANZA_REFERENCE.md](BANZA_REFERENCE.md)
```

**Step 4 — Update `CLAUDE.md`:** All 10+ occurrences of `BANZAMI_REFERENCE.md` → `BANZA_REFERENCE.md`.

**Step 5 — Update ADR-015:**
Add superseding amendment at the top of `ADR-015-markdown-first-content-architecture.md`:
```markdown
> **Amendment (2026-MM-DD):** The filename `BANZAMI_REFERENCE.md` was renamed to
> `BANZA_REFERENCE.md` per ADR-025 canonical naming alignment. All references to
> `BANZAMI_REFERENCE.md` in this document should be read as `BANZA_REFERENCE.md`.
> The architectural decision itself remains unchanged.
```

**Step 6 — Update `docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json`:**
- `meta.referenceFile` field: `"docs/BANZAMI_REFERENCE.md"` → `"docs/BANZA_REFERENCE.md"`
- All `evidence[]` entries containing `"docs/BANZAMI_REFERENCE.md §N"` strings

**Step 7 — Update all UI strings in `apps/docs/`:**
- `app/[section]/page.tsx` — comment strings
- `app/page.tsx` — UI string
- `app/reference/page.tsx` — UI strings
- `app/sobre-banzamia/page.tsx` — UI string (will be renamed in Wave 4)
- `app/validacao/page.tsx` — UI strings
- `components/validation/ArchitectureHealth.tsx` — UI strings

**Step 8 — Update `apps/docs/README.md`:**
Three occurrences of `BANZAMI_REFERENCE.md`.

**Step 9 — Update `apps/docs/lib/banzamia-client.ts` (or `banzai-client.ts` after Wave 2):**
Two demo data citation strings.

**Step 10 — Update test file labels:**
`apps/docs/lib/__tests__/reference.test.ts` — describe block label and comment strings.

**Step 11 — Update `docs/glossary.md`, `docs/certification.md`, `docs/conformance.md`:**
All `BANZAMI_REFERENCE.md §N` cross-references.

**Step 12 — Update `docs/validation/README.md` and `VALIDATION_DOMAINS.md`.**

**Step 13 — Rename `BANZAMI_IMPLEMENTATION_MATRIX.json`:**
```
mv docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json docs/validation/BANZA_IMPLEMENTATION_MATRIX.json
```
Update all references in `apps/validation-studio/` and governance engine.

---

**Wave 3 verification:**
1. `npm run build` in `apps/docs/` — must succeed
2. `npx vitest run lib/__tests__/reference.test.ts` — 51/51 pass
3. Visit `/reference` — all 19 sections render
4. Visit `docs/BANZA_REFERENCE.md` exists and `docs/BANZAMI_REFERENCE.md` does not
5. `grep -r "BANZAMI_REFERENCE" docs/ apps/docs/` — should return only historical audit files (acceptable) and no build-time or routing references

**Wave 3 commit:** `docs(naming): W3 — rename BANZAMI_REFERENCE.md → BANZA_REFERENCE.md per ADR-025`

---

## Wave 4 — Public Route Migration (/banzamia → /banzai)

**Goal:** Migrate the two public-facing routes. This wave has the highest visibility: it changes URLs that may have been bookmarked or linked externally.

**Items:** NM-002, NM-003

**Prerequisite:** Deploy HTTP 301 redirects for the old routes before or simultaneously with the code change.

---

### W4-001 — Rename route `/banzamia` → `/banzai`

**Repo:** Banza (`/Users/fm65/Banza`)

**Steps:**
1. Add redirect in Next.js config or via nginx: `301 /banzamia → /banzai`
2. `mv apps/docs/app/banzamia apps/docs/app/banzai`
3. Update `page.tsx` internal function name: `BanzamIAPage` → `BanzAIPage` (cosmetic, no breaking impact)
4. Update the static route exclusion set:
   ```tsx
   const STATIC_ROUTE_OVERRIDES = new Set(['banzai'])  // was 'banzamia'
   ```
5. Update all internal hrefs referencing `/banzamia`:
   - `app/layout.tsx` — nav entry and footer link
   - `app/roadmap/page.tsx` — two Link hrefs
   - `app/sobre-banzamia/page.tsx` — two Link hrefs (will be renamed in next step)
   - `components/banzamia/BanzamIASidebar.tsx` — no direct href (it links to `/sobre-banzamia`, handled below)
   - `components/banzamia/HomeBanzamIAEntry.tsx` — two Link hrefs
   - `components/banzamia/QuickAnswerCard.tsx` — deepLink construction
   - `components/HeroBanzamIAWidget.tsx` — `router.push('/banzamia?...')` call

**Note:** `docs/BANZAMI_REFERENCE.md` (or `BANZA_REFERENCE.md` after Wave 3) contains the string `` `banzami.org/banzamia` `` in §11. This reference must also be updated.

---

### W4-002 — Rename route `/sobre-banzamia` → `/sobre-o-banzai`

**Repo:** Banza (`/Users/fm65/Banza`)

**Steps:**
1. Add redirect: `301 /sobre-banzamia → /sobre-o-banzai`
2. `mv apps/docs/app/sobre-banzamia apps/docs/app/sobre-o-banzai`
3. Update `page.tsx` function name: `SobreBanzamiaPage` → `SobreBanzAIPage`
4. Fix the double bug in section routing (wrong route AND wrong section number):
   ```tsx
   // SectionCard.tsx — was:
   section.number === 9 ? '/sobre-banzamia' : ...
   // Must become:
   section.number === 11 ? '/sobre-o-banzai' : ...

   // SectionNav.tsx:71 — was:
   navLink('/sobre-banzamia', 'BanzAI')
   // Must become:
   navLink('/sobre-o-banzai', 'BanzAI')

   // SectionNav.tsx:81 — was:
   section.number === 9 ? '/sobre-banzamia' : ...
   // Must become:
   section.number === 11 ? '/sobre-o-banzai' : ...
   ```
5. Update `BanzamIASidebar.tsx` link: `href="/sobre-banzamia"` → `href="/sobre-o-banzai"`

**Verification:** Both old URLs return 301 to the new URLs. New routes render correctly. Section navigation card for §11 links correctly to `/sobre-o-banzai`.

---

**Wave 4 commit:** `feat(routing): W4 — migrate /banzamia → /banzai and /sobre-banzamia → /sobre-o-banzai`

---

## Migration Summary

| Wave | Description | Risk | Public Impact | Estimated Scope |
|---|---|---|---|---|
| Wave 1 | Banzami repo infrastructure | LOW | None | 4–6 files |
| Wave 2 | Frontend components, library, SVGs, docs | MEDIUM | None (build-internal) | 35–45 files |
| Wave 3 | BANZAMI_REFERENCE.md → BANZA_REFERENCE.md | HIGH | None (content unchanged) | 25–30 files + 100+ string occurrences |
| Wave 4 | Public routes /banzamia → /banzai | MEDIUM | URLs change | 8–10 files + redirects |

**Total estimated scope:** ~80 files, ~140 string occurrences, 2 directory renames in source, 1 critical file rename.

---

## Dependency Ordering Rationale

- Wave 1 before Wave 2: Backend directory renamed first so Wave 2 can update any docs strings pointing to it.
- Wave 2 before Wave 3: Component and library filenames stabilised before the reference file rename adds concurrent churn.
- Wave 3 before Wave 4: The reference file is the most central change; route changes are cosmetic by comparison and should not happen while the document naming is still ambiguous.
- Wave 4 last: Route changes are the most visible. Doing them last means every other system is already consistent when the public URLs change.

---

*Plan completed: 2026-05-30. No files modified.*
