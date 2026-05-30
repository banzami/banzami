---
title: CANONICAL_FILENAME_AUDIT
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no files modified
scope: Banza repo (/Users/fm65/Banza) + Banzami repo (/Users/fm65/Banzami)
---

# Canonical Filename Audit

**Purpose:** Repository-wide inventory of every artefact whose name encodes a pre-ADR-025 identity model. Audit only — no modifications made.

**Canonical model (ADR-025):**
- **BANZA** — The protocol
- **BanzAI** — The Protocol Operating System
- **Banzami** — The Reference Operator / Reference Implementation

**Root naming problem:** The portmanteau **"banzamia"** (Banzami + IA) was coined before ADR-025 as an informal name for what is now canonically called **BanzAI**. Every artefact using "banzamia" or "BanzamIA" as a proper name for the AI system is pre-ADR-025.

---

## Section 1 — Reference Documents

### 1.1 BANZAMI_REFERENCE.md

**Current locations:**
- `/Users/fm65/Banza/docs/BANZAMI_REFERENCE.md` — the live document (canonical source of truth)
- `/Users/fm65/Banzami/docs/BANZAMI_REFERENCE.md` — mirror copy in Banzami repo

**Classification:** CRITICAL

**Rationale:** Under ADR-025, this document is the public reference for the **BANZA protocol ecosystem** — not specifically for the Banzami operator. Its content covers the BANZA protocol (§§1–3), BanzAI (§11), Banzami (§§12–13), and all shared protocol concerns (governance, certification, federation, security). The filename `BANZAMI_REFERENCE.md` implies this is Banzami's reference document. The canonical filename is `BANZA_REFERENCE.md`.

**Current name:** `BANZAMI_REFERENCE.md`
**Canonical name:** `BANZA_REFERENCE.md`

### 1.2 BANZAMI_IMPLEMENTATION_MATRIX.json

**Current location:** `/Users/fm65/Banza/docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json`

**Classification:** LEGACY

**Rationale:** This document tracks the implementation status of the Banzami reference operator — so "BANZAMI" in the filename is not entirely wrong. However it also covers protocol-level invariants, certification, and federation items, making "BANZA_IMPLEMENTATION_MATRIX.json" or "BANZA_VALIDATION_MATRIX.json" more accurate.

**Current name:** `BANZAMI_IMPLEMENTATION_MATRIX.json`
**Canonical name:** `BANZA_IMPLEMENTATION_MATRIX.json`

### 1.3 BANZAMI_ECOSYSTEM_REFERENCE.md

**Current location:** `/Users/fm65/Banza/docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md`

**Classification:** MISLEADING

**Rationale:** This is explicitly described as an "architecture-first" complement to BANZAMI_REFERENCE.md, covering the full ecosystem. Its subject is the BANZA ecosystem, not Banzami specifically.

**Current name:** `BANZAMI_ECOSYSTEM_REFERENCE.md`
**Canonical name:** `BANZA_ECOSYSTEM_REFERENCE.md`

---

## Section 2 — Directories

### 2.1 apps/banzamia/ (Banzami repo)

**Current location:** `/Users/fm65/Banzami/apps/banzamia/`

**Classification:** MISLEADING

**Rationale:** This is the backend service for BanzAI — the RAG engine, protocol graph, orchestrator, and API server. The directory name implies this is an app belonging to Banzami (the operator). It is the engine powering BanzAI (the Protocol OS). The canonical directory name is `apps/banzai/`.

**Contains:** 60+ source files — orchestrator pipeline, RAG engine, knowledge graph, protocol tools, embedding providers, evaluation harness.

### 2.2 apps/docs/components/banzamia/ (Banza repo)

**Current location:** `/Users/fm65/Banza/apps/docs/components/banzamia/`

**Classification:** MISLEADING

**Rationale:** This directory contains all React components for the BanzAI interface — BanzamIAApp, BanzamIAChat, BanzamIASidebar, and 17 module components. The canonical directory name is `components/banzai/`.

**Contains:** 24 files — app shell, chat, sidebar, sources panel, icon, quick answer card, prompt chip, entry widget, and 14 module components.

### 2.3 apps/docs/app/banzamia/ (Banza repo)

**Current location:** `/Users/fm65/Banza/apps/docs/app/banzamia/`

**Classification:** CRITICAL

**Rationale:** This is the Next.js route directory that defines the public URL `banzami.org/banzamia`. The route is publicly accessible and encodes "banzamia" in the URL. The canonical route is `/banzai`.

**Contains:** `page.tsx` — the BanzAI live interface page.

### 2.4 apps/docs/app/sobre-banzamia/ (Banza repo)

**Current location:** `/Users/fm65/Banza/apps/docs/app/sobre-banzamia/`

**Classification:** CRITICAL

**Rationale:** This is the public URL `banzami.org/sobre-banzamia`. "Sobre Banzamia" means "About Banzamia" — the pre-ADR-025 name for what is now BanzAI. The canonical route should be `/sobre-o-banzai` or `/banzai/sobre`.

**Contains:** `page.tsx` — the BanzAI "about" page, rendering BANZAMI_REFERENCE.md §11.

### 2.5 docs/banzamia/ (Banza repo)

**Current location:** `/Users/fm65/Banza/docs/banzamia/`

**Classification:** MISLEADING

**Rationale:** This directory contains BanzAI technical documentation — architecture, API, operator builder, manifest validator, knowledge search, trace explainer, SDK assistant, roadmap. The canonical directory is `docs/banzai/`.

**Contains:** 9 markdown files — overview, architecture, API, operator-builder, manifest-validator, knowledge-search, trace-explainer, sdk-assistant, roadmap.

### 2.6 docker/banzamia/ (Banzami repo)

**Current location:** `/Users/fm65/Banzami/docker/banzamia/`

**Classification:** LEGACY

**Rationale:** The Docker orchestration for the BanzAI backend service. "banzamia" was the service name before ADR-025. Canonical name is `docker/banzai/`.

**Contains:** `Dockerfile`, `docker-compose.yml`.

---

## Section 3 — Source Files

### 3.1 lib/banzamia-client.ts

**Current location:** `/Users/fm65/Banza/apps/docs/lib/banzamia-client.ts`

**Classification:** MISLEADING

**Rationale:** This is the frontend TypeScript client library for the BanzAI API. Its canonical name is `banzai-client.ts`. The file exports `BANZAMIA_API_URL` and `isLiveMode`.

**Internal identifiers also affected:**
- `BANZAMIA_API_URL` (exported constant) → `BANZAI_API_URL`
- `NEXT_PUBLIC_BANZAMIA_API_URL` (environment variable) → `NEXT_PUBLIC_BANZAI_API_URL`

### 3.2 Duplicate BANZAMI_REFERENCE.md (Banzami repo)

**Current location:** `/Users/fm65/Banzami/docs/BANZAMI_REFERENCE.md`

**Classification:** LEGACY

**Rationale:** A copy of the canonical reference document maintained in the Banzami repository. Not the live document (which lives in Banza repo). Should be renamed alongside the primary file.

---

## Section 4 — React Components

All components in `/Users/fm65/Banza/apps/docs/components/banzamia/` use the pre-ADR-025 naming pattern. Listed below with classifications.

| Current Component Name | Canonical Name | Classification |
|---|---|---|
| `BanzamIAApp` | `BanzAIApp` | MISLEADING |
| `BanzamIAChat` | `BanzAIChat` | MISLEADING |
| `BanzamIAIcon` | `BanzAIIcon` | MISLEADING |
| `BanzamIASidebar` | `BanzAISidebar` | MISLEADING |
| `BanzamIASourcesPanel` | `BanzAISourcesPanel` | MISLEADING |
| `HomeBanzamIAEntry` | `HomeBanzAIEntry` | MISLEADING |
| `HeroBanzamIAWidget` | `HeroBanzAIWidget` | MISLEADING |
| `SobreBanzamiaPage` (function name) | `SobreBanzAIPage` | LEGACY |
| `BanzamIAPage` (function name in banzamia/page.tsx) | `BanzAIPage` | LEGACY |

**Module components (14 files):** The module component files themselves (`CertificationCopilotModule.tsx`, `SimulatorModule.tsx`, etc.) have canonical names and do not need renaming. Their import source (`@/lib/banzamia-client`) is the only issue.

---

## Section 5 — Routes (Public URLs)

| Current Route | Canonical Route | Classification | Notes |
|---|---|---|---|
| `/banzamia` | `/banzai` | CRITICAL | Public URL. Lives at `app/banzamia/page.tsx`. |
| `/sobre-banzamia` | `/sobre-o-banzai` | CRITICAL | Public URL. Lives at `app/sobre-banzamia/page.tsx`. |

**Note on `/banzamia` route:** The `[section]` dynamic route explicitly excludes `'banzamia'` from static generation (`STATIC_ROUTE_OVERRIDES = new Set(['banzamia'])`). After renaming, this exclusion must be updated to exclude `'banzai'` instead.

**Note on section §11 routing:** `SectionCard.tsx` and `SectionNav.tsx` both hardcode the section §11 mapping:
- `section.number === 9 ? '/sobre-banzamia'` — This was written when BanzAI was §9. It is now §11. This is a double bug: wrong section number AND wrong route name.

---

## Section 6 — SVG Architecture Diagrams

All `banzamia-*.svg` files in `/Users/fm65/Banza/apps/docs/public/images/architecture/` and `/Users/fm65/Banza/docs/images/architecture/` encode the pre-ADR-025 name.

| Current SVG Filename | Canonical Filename | Classification |
|---|---|---|
| `banzamia-canonical-architecture.svg` | `banzai-canonical-architecture.svg` | MISLEADING |
| `banzamia-internal-architecture.svg` | `banzai-internal-architecture.svg` | MISLEADING |
| `banzamia-cognitive-layer.svg` | `banzai-cognitive-layer.svg` | MISLEADING |
| `banzamia-force-multiplier.svg` | `banzai-force-multiplier.svg` | MISLEADING |
| `banzamia-knowledge-gap.svg` | `banzai-knowledge-gap.svg` | MISLEADING |
| `banzamia-model-routing.svg` | `banzai-model-routing.svg` | MISLEADING |
| `banzamia-product-architecture.svg` | `banzai-product-architecture.svg` | MISLEADING |
| `banzamia-truth-model.svg` | `banzai-truth-model.svg` | MISLEADING |

**Note:** `banzami-ecosystem.svg` uses `banzami-` (operator name) for an ecosystem diagram. Classification: MISLEADING — the diagram covers the BANZA ecosystem, not just Banzami. Canonical: `banza-ecosystem.svg`.

**SVG files exist in two locations (must be kept in sync):**
- `docs/images/architecture/` — source
- `apps/docs/public/images/architecture/` — public-facing copy (must match)

**Reference in BANZAMI_REFERENCE.md:** Eight `![...](/images/architecture/banzamia-*.svg)` image references in §11 must be updated when SVG filenames change.

---

## Section 7 — Environment Variables

| Current Variable | Canonical Variable | Classification | Scope |
|---|---|---|---|
| `NEXT_PUBLIC_BANZAMIA_API_URL` | `NEXT_PUBLIC_BANZAI_API_URL` | MISLEADING | `.env.local`, Docker, deployment scripts |

**Usage locations:**
- `apps/docs/lib/banzamia-client.ts:8` — reads the variable
- `apps/docs/components/banzamia/BanzamIASourcesPanel.tsx:126` — displays mode string referencing the variable
- Server-side configuration and any CI/CD environment configurations

---

## Section 8 — Docker and Infrastructure

### 8.1 docker-compose.yml service names

**File:** `/Users/fm65/Banzami/docker/banzamia/docker-compose.yml`

| Current Name | Canonical Name | Classification |
|---|---|---|
| Service name: `banzamia` | `banzai` | LEGACY |
| Container name: `banzamia-api` | `banzai-api` | LEGACY |
| Container name: `banzamia-qdrant` | `banzai-qdrant` | LEGACY |

### 8.2 package.json package name

**File:** `/Users/fm65/Banzami/apps/banzamia/package.json`

| Current | Canonical | Classification |
|---|---|---|
| `"name": "banzamia"` | `"name": "banzai"` | MISLEADING |
| `"description": "BanzamIA — AI-native protocol agent..."` | `"BanzAI — Protocol Operating System..."` | MISLEADING |

---

## Section 9 — Tests and Validation

### 9.1 reference.test.ts

**File:** `/Users/fm65/Banza/apps/docs/lib/__tests__/reference.test.ts`

Test suite refers to `BANZAMI_REFERENCE.md` in:
- `describe('BANZAMI_REFERENCE.md — content integrity', ...)` — describe block label
- Comment: `// ─── getReference — metadata (IDT-001: BANZAMI_REFERENCE.md structure)`
- Hardcoded path `REFERENCE_PATH` is derived from `lib/reference.ts`, not directly in test

After BANZA_REFERENCE.md rename: describe labels and comment strings must be updated.

### 9.2 BANZAMI_IMPLEMENTATION_MATRIX.json internal identifiers

**File:** `/Users/fm65/Banza/docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json`

| Field | Current Value | Canonical Value |
|---|---|---|
| `meta.referenceFile` | `"docs/BANZAMI_REFERENCE.md"` | `"docs/BANZA_REFERENCE.md"` |
| `meta.description` | `"...derived from BANZAMI_REFERENCE.md..."` | `"...derived from BANZA_REFERENCE.md..."` |
| Multiple `evidence[]` entries | `"docs/BANZAMI_REFERENCE.md §N"` (appears 10+ times) | `"docs/BANZA_REFERENCE.md §N"` |

---

## Section 10 — Navigation and Metadata

### 10.1 Navigation hardcoding

**File:** `/Users/fm65/Banza/apps/docs/app/layout.tsx`

```tsx
{ href: '/banzamia', label: 'BanzAI', ai: true }
```
The label is correct (`BanzAI`) but the href encodes the pre-ADR-025 route.

**File:** `/Users/fm65/Banza/apps/docs/app/layout.tsx` (footer)
```tsx
<Link href="/banzamia" className="...">BanzAI</Link>
```

### 10.2 Section routing hardcoding (double bug)

**Files:** `SectionCard.tsx:31`, `SectionNav.tsx:71`, `SectionNav.tsx:81`

```tsx
section.number === 9 ? '/sobre-banzamia' : ...
navLink('/sobre-banzamia', 'BanzAI')
```

**Two problems:**
1. Wrong route name: `/sobre-banzamia` should be `/sobre-o-banzai` (post-migration)
2. Wrong section number: BanzAI is now §11, not §9 (the §§1–3 integration renumbered the document)

### 10.3 CLAUDE.md references

**File:** `/Users/fm65/Banza/CLAUDE.md`

`BANZAMI_REFERENCE.md` appears 10+ times in CLAUDE.md as the canonical instruction for "update reference first". All references must be updated to `BANZA_REFERENCE.md` when the file is renamed.

### 10.4 ADR-015 filename definition

**File:** `/Users/fm65/Banza/docs/adr/ADR-015-markdown-first-content-architecture.md`

ADR-015 canonises `BANZAMI_REFERENCE.md` as the single source of truth filename. After the rename, ADR-015 must be amended with a superseding note or a new ADR (ADR-026?) that records the rename decision and the new canonical filename.

---

## Section 11 — Correctly Named Artefacts (CORRECT classification)

These artefacts use "banzami" in contexts where Banzami (the operator) is the correct referent. They are NOT to be changed.

| Artefact | Reason Correct |
|---|---|
| `banzami_logo.svg`, `banzami_icon.png`, `banzami_splash.png` | Brand assets for the Banzami operator application |
| Android package `com.banzami.*` | Mobile app package identifier for the Banzami operator |
| `apps/mobile/`, `apps/merchant/` Flutter apps | These are Banzami operator apps |
| Rust crates `banzami-acquiring`, `banzami-*` | Banzami-specific service crates in Banzami repo |
| `apps/dashboard`, `apps/admin` | Banzami operator management interfaces |
| GitHub org/repo paths `github.com/banzami/*` | Organization and repository identifiers |

---

## Summary Statistics

| Classification | Count | Blocker? |
|---|---|---|
| CRITICAL | 4 items | Yes — encode wrong conceptual model publicly |
| MISLEADING | 22 items | No — internal, but create daily confusion |
| LEGACY | 8 items | No — historical, low conceptual risk |
| CORRECT | 11+ item categories | N/A |

**Total artefacts requiring migration:** ~34 primary items (with cascading references estimated at 100+ string occurrences across documentation, code, and configuration)

---

*Audit completed: 2026-05-30. No files modified.*
