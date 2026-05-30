---
title: CANONICAL_FILENAME_IMPACT_MATRIX
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no files modified
---

# Canonical Filename Impact Matrix

For every finding: Current Name → Canonical Name → Classification → Risk → Breaking Impact.

---

## Matrix

| ID | Current Name | Canonical Name | Classification | Risk | Breaking Impact |
|----|---|---|---|---|---|
| NM-001 | `docs/BANZAMI_REFERENCE.md` | `docs/BANZA_REFERENCE.md` | CRITICAL | HIGH | **Yes — cascading.** `lib/reference.ts` REFERENCE_PATH constant breaks build. CLAUDE.md, ADR-015, ADR-016, README files, 10+ cross-references in docs, validation matrix referenceFile, §N citation strings across all audit documents. |
| NM-002 | Route `/banzamia` | Route `/banzai` | CRITICAL | HIGH | **Yes — public URL change.** Any external link to `banzami.org/banzamia` breaks. Directory rename required. Static route exclusion set must be updated. All internal hrefs must change. |
| NM-003 | Route `/sobre-banzamia` | Route `/sobre-o-banzai` | CRITICAL | HIGH | **Yes — public URL change.** Any external link breaks. SectionCard.tsx and SectionNav.tsx hardcoded hrefs must change. Also fixes the wrong section number (§9 → §11). |
| NM-004 | `components/banzamia/` directory | `components/banzai/` directory | MISLEADING | HIGH | **Yes — internal only.** All 24 component import paths break. All `@/components/banzamia/*` imports in pages and components must be updated. |
| NM-005 | `lib/banzamia-client.ts` | `lib/banzai-client.ts` | MISLEADING | HIGH | **Yes — internal only.** Imported in 19 files across components and pages. All `@/lib/banzamia-client` import paths must change. |
| NM-006 | `BanzamIAApp` component | `BanzAIApp` | MISLEADING | MEDIUM | Internal only. Affects 2 import sites plus the file that defines it. |
| NM-007 | `BanzamIAChat` component | `BanzAIChat` | MISLEADING | MEDIUM | Internal only. Affects 1 import site plus definition. |
| NM-008 | `BanzamIAIcon` component | `BanzAIIcon` | MISLEADING | MEDIUM | Internal only. Affects 4 import sites plus definition. |
| NM-009 | `BanzamIASidebar` component | `BanzAISidebar` | MISLEADING | MEDIUM | Internal only. Affects 2 import sites plus definition. |
| NM-010 | `BanzamIASourcesPanel` component | `BanzAISourcesPanel` | MISLEADING | MEDIUM | Internal only. Affects 1 import site plus definition. |
| NM-011 | `HomeBanzamIAEntry` component | `HomeBanzAIEntry` | MISLEADING | MEDIUM | Internal only. Affects 1 import site plus definition. |
| NM-012 | `HeroBanzamIAWidget` component | `HeroBanzAIWidget` | MISLEADING | MEDIUM | Internal only. Affects 1 import site (HeroSection.tsx) plus definition. |
| NM-013 | `apps/banzamia/` directory (Banzami repo) | `apps/banzai/` directory | MISLEADING | HIGH | **Yes — cascading in Banzami repo.** package.json, docker-compose.yml build context path, tsconfig.json, all internal references, deploy scripts if they reference this path. |
| NM-014 | `docs/banzamia/` directory (Banza repo) | `docs/banzai/` directory | MISLEADING | MEDIUM | Internal docs directory. All relative links from `docs/index.md` and cross-references within the 9 docs files must change. |
| NM-015 | `docker/banzamia/` directory (Banzami repo) | `docker/banzai/` directory | LEGACY | MEDIUM | Docker compose build context path references `../../apps/banzamia`. If `apps/banzamia` is renamed, docker-compose.yml build context must also change. |
| NM-016 | `banzamia-client.ts` constant `BANZAMIA_API_URL` | `BANZAI_API_URL` | MISLEADING | LOW | Internal constant. Updated within the file when the file is migrated. |
| NM-017 | `NEXT_PUBLIC_BANZAMIA_API_URL` env variable | `NEXT_PUBLIC_BANZAI_API_URL` | MISLEADING | HIGH | **Yes — deployment breaking.** Any `.env.local`, server environment, or CI/CD configuration that sets this variable must be updated. Applications will silently fall back to demo mode if the variable name changes without updating the config. |
| NM-018 | `banzamia-canonical-architecture.svg` | `banzai-canonical-architecture.svg` | MISLEADING | MEDIUM | Image reference in BANZAMI_REFERENCE.md §11 must be updated. File exists in two locations: `docs/images/` and `apps/docs/public/images/`. |
| NM-019 | `banzamia-internal-architecture.svg` | `banzai-internal-architecture.svg` | MISLEADING | MEDIUM | Same as NM-018. Referenced in BANZAMI_REFERENCE.md §11. |
| NM-020 | `banzamia-cognitive-layer.svg` | `banzai-cognitive-layer.svg` | MISLEADING | MEDIUM | Referenced in BANZAMI_REFERENCE.md §11. |
| NM-021 | `banzamia-force-multiplier.svg` | `banzai-force-multiplier.svg` | MISLEADING | MEDIUM | Referenced in BANZAMI_REFERENCE.md §11. |
| NM-022 | `banzamia-knowledge-gap.svg` | `banzai-knowledge-gap.svg` | MISLEADING | MEDIUM | Referenced in BANZAMI_REFERENCE.md §11. |
| NM-023 | `banzamia-model-routing.svg` | `banzai-model-routing.svg` | MISLEADING | MEDIUM | Referenced in BANZAMI_REFERENCE.md §11. |
| NM-024 | `banzamia-product-architecture.svg` | `banzai-product-architecture.svg` | MISLEADING | MEDIUM | Referenced in BANZAMI_REFERENCE.md §11. |
| NM-025 | `banzamia-truth-model.svg` | `banzai-truth-model.svg` | MISLEADING | MEDIUM | Referenced in BANZAMI_REFERENCE.md §11. |
| NM-026 | `banzami-ecosystem.svg` | `banza-ecosystem.svg` | MISLEADING | LOW | Covers the BANZA ecosystem, not just Banzami. Low-urgency. |
| NM-027 | Docker service `banzamia` | `banzai` | LEGACY | LOW | Internal infrastructure name. No public surface impact. |
| NM-028 | Docker container `banzamia-api` | `banzai-api` | LEGACY | LOW | Internal container name. |
| NM-029 | Docker container `banzamia-qdrant` | `banzai-qdrant` | LEGACY | LOW | Internal container name. |
| NM-030 | `package.json "name": "banzamia"` | `"banzai"` | MISLEADING | LOW | Internal package identifier. No npm publish, so no registry impact. |
| NM-031 | `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md` | `BANZA_ECOSYSTEM_REFERENCE.md` | MISLEADING | LOW | Referenced in a small number of docs. ADR reference and `docs/README.md`. |
| NM-032 | `docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` | `BANZA_IMPLEMENTATION_MATRIX.json` | LEGACY | HIGH | Referenced extensively in Validation Studio, governance engine, and the `/validacao` page. The validation-studio test at `governance.test.ts:65` hardcodes the `referenceFile` field value. |
| NM-033 | `SobreBanzamiaPage` function name | `SobreBanzAIPage` | LEGACY | NONE | Purely internal. No import, no export. Rename within the file when route is migrated. |
| NM-034 | `BanzamIAPage` function name | `BanzAIPage` | LEGACY | NONE | Purely internal. Same as NM-033. |

---

## BANZAMI_REFERENCE.md Rename: Full Dependency Map (NM-001)

This item has the largest cascading footprint. Every place that references the filename must be updated atomically.

### Files that contain the string "BANZAMI_REFERENCE.md" (must all update together)

**Banza repo:**

| File | Reference count | Type |
|---|---|---|
| `CLAUDE.md` | 10+ | Canonical instruction |
| `apps/docs/lib/reference.ts` | 4 | Build-time parser (REFERENCE_PATH constant) |
| `apps/docs/README.md` | 3 | Developer documentation |
| `apps/docs/app/[section]/page.tsx` | 2 | Comments |
| `apps/docs/app/page.tsx` | 1 | UI string |
| `apps/docs/app/reference/page.tsx` | 2 | UI strings |
| `apps/docs/app/sobre-banzamia/page.tsx` | 1 | UI string |
| `apps/docs/app/validacao/page.tsx` | 2 | UI strings |
| `apps/docs/components/validation/ArchitectureHealth.tsx` | 3 | UI strings |
| `apps/docs/lib/__tests__/reference.test.ts` | 3 | Test describe labels and comments |
| `apps/docs/lib/banzamia-client.ts` | 2 | Source citations in demo data |
| `docs/README.md` | 1 | Documentation index |
| `docs/adr/ADR-015-markdown-first-content-architecture.md` | 20+ | ADR defines the filename |
| `docs/adr/ADR-016-banzami-banza-brand-architecture.md` | 5 | ADR references |
| `docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` | 10+ | Matrix metadata and evidence refs |
| `docs/validation/README.md` | 6 | Validation documentation |
| `docs/validation/VALIDATION_DOMAINS.md` | 1 | Domain documentation |
| `docs/glossary.md` | 5 | Cross-references |
| `docs/certification.md` | 1 | Cross-reference |
| `docs/conformance.md` | 1 | Cross-reference |
| `docs/index.md` | 2 | Documentation index |
| Multiple audit docs in `docs/audit/` | 30+ | Historical, low-priority |

**Banzami repo:**

| File | Reference count | Type |
|---|---|---|
| `docs/BANZAMI_REFERENCE.md` (the file itself) | — | The file to be renamed |
| Various `docs/migration/` docs | 15+ | Historical audit records |

### The lib/reference.ts constant (build-breaking)

```typescript
// apps/docs/lib/reference.ts:14
const REFERENCE_PATH = path.join(process.cwd(), '../../docs/BANZAMI_REFERENCE.md')
```

This is the single line that breaks the build if the file is renamed without updating this constant. It is the first fix that must be applied.

### ADR-015 update requirement

ADR-015 is titled "BANZAMI_REFERENCE.md as Single Source of Truth". Its title, decision record, and architecture diagrams all hardcode the filename. After the rename, ADR-015 must be updated with a superseding amendment noting:

> "The filename `BANZAMI_REFERENCE.md` was changed to `BANZA_REFERENCE.md` by ADR-026 (or equivalent) to align with ADR-025 canonical naming. All references to `BANZAMI_REFERENCE.md` in this document should be read as `BANZA_REFERENCE.md`."

---

## Risk Summary

| Risk Level | Items | Notes |
|---|---|---|
| HIGH — build-breaking | NM-001 (BANZAMI_REFERENCE.md), NM-004 (components/banzamia/), NM-005 (banzamia-client.ts), NM-017 (env var) | Will break build or runtime if changed without coordinated update |
| HIGH — public URL change | NM-002 (/banzamia), NM-003 (/sobre-banzamia) | Breaks external links; requires redirect setup |
| MEDIUM — internal inconsistency | NM-006 to NM-015, NM-018 to NM-026 | Causes daily confusion, no immediate breakage |
| LOW — cosmetic | NM-027 to NM-034 | Infrastructure labels and internal identifiers |

---

*Matrix completed: 2026-05-30. No files modified.*
