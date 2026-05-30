---
title: CANONICAL_FILENAME_PRIORITY_REPORT
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no files modified
---

# Canonical Filename Priority Report

**Top 25 structural naming issues, ranked by architectural importance.**

Architectural importance is defined as: the degree to which the name encodes an incorrect conceptual model that a reader, developer, or visitor will encounter and internalize. Occurrence count is not the ranking criterion — a name seen once in a critical place outranks a name seen twenty times in internal scaffolding.

---

## Rank 1 — `BANZAMI_REFERENCE.md`

**Classification:** CRITICAL
**Wave:** 3

The single most architecturally important naming error in the project. This is the canonical reference document for the **BANZA protocol ecosystem**. Its name implies it is Banzami's document. Every developer, operator, regulator, and auditor who encounters this filename internalises the wrong hierarchy: "Banzami owns the reference → Banzami owns the protocol."

The filename is referenced in 5 ADRs, 2 CLAUDE.md files, the build parser, the docs README, and dozens of cross-references. It is also the literal name of the file that ADR-015 canonises as the single source of truth.

**Canonical name:** `BANZA_REFERENCE.md`

**Why it ranks first:** A reference document named `BANZA_REFERENCE.md` makes the protocol hierarchy structurally visible from the filesystem. Any future contributor reading the repo sees "BANZA owns the reference" before reading a single line of content.

---

## Rank 2 — Route `/banzamia` (Public URL)

**Classification:** CRITICAL
**Wave:** 4

`banzami.org/banzamia` is the publicly accessible URL for the BanzAI interface. Every visitor, operator, developer, and journalist who visits this URL sees "banzamia" — a portmanteau of Banzami + AI that predates ADR-025. The canonical URL is `banzami.org/banzai`.

This is the highest-visibility structural naming issue after the reference document.

**Canonical name:** `/banzai`

---

## Rank 3 — Route `/sobre-banzamia` (Public URL)

**Classification:** CRITICAL
**Wave:** 4

`banzami.org/sobre-banzamia` means "about Banzamia" — using the pre-ADR-025 name for BanzAI. A visitor who lands here is told, via the URL, that they are looking at "Banzamia" not "BanzAI". This directly contradicts the ADR-025 identity model.

**Canonical name:** `/sobre-o-banzai`

**Secondary bug here:** `SectionCard.tsx` and `SectionNav.tsx` still hardcode `section.number === 9` for this route. BanzAI is now §11 after the §§1–3 integration. This is a functional bug independent of the naming issue.

---

## Rank 4 — `lib/banzamia-client.ts`

**Classification:** MISLEADING
**Wave:** 2

Every developer working on the frontend reads this filename. It is imported in 19 files. A new developer sees `banzamia-client.ts` and infers: "the Banzamia client". The canonical name makes the subject explicit: `banzai-client.ts` — "the BanzAI client".

**Canonical name:** `lib/banzai-client.ts`

---

## Rank 5 — `NEXT_PUBLIC_BANZAMIA_API_URL` Environment Variable

**Classification:** MISLEADING
**Wave:** 2 (code change) + deployment (config change)

This environment variable is the configuration toggle between demo mode and live mode. Any developer configuring a deployment sees this variable and reads "Banzamia API" — not "BanzAI API". The canonical name is `NEXT_PUBLIC_BANZAI_API_URL`.

**Special risk:** The environment variable rename is the only change in this migration where a code update alone is insufficient. The server configuration must be updated before or simultaneously with the code deployment. A deployment with the new code but old env var name will silently fall into demo mode.

**Canonical name:** `NEXT_PUBLIC_BANZAI_API_URL`

---

## Rank 6 — `apps/banzamia/` Directory (Banzami repo)

**Classification:** MISLEADING
**Wave:** 1

This directory contains the BanzAI backend — the RAG engine, knowledge graph, protocol tools, and orchestrator. It is the Protocol Operating System's computational core. A developer navigating `Banzami/apps/` sees: `banzamia/`. They infer "an app called Banzamia" — not "the BanzAI backend". The canonical name is `apps/banzai/`.

**Canonical name:** `apps/banzai/`

---

## Rank 7 — `components/banzamia/` Directory (Banza repo)

**Classification:** MISLEADING
**Wave:** 2

This directory contains all 24 React components for the BanzAI interface. A developer navigating `apps/docs/components/` sees `banzamia/`. The canonical name is `components/banzai/`.

**Canonical name:** `components/banzai/`

---

## Rank 8 — `BanzamIAApp` Component

**Classification:** MISLEADING
**Wave:** 2

This is the root component of the BanzAI interface. Its name — `BanzamIAApp` — encodes the pre-ADR-025 portmanteau. The canonical name is `BanzAIApp`. This component name appears in `app/banzamia/page.tsx` (the live interface) and is the most-encountered component in the codebase.

**Canonical name:** `BanzAIApp`

---

## Rank 9 — `docs/banzamia/` Documentation Directory (Banza repo)

**Classification:** MISLEADING
**Wave:** 2

This directory contains 9 markdown files documenting the BanzAI system — architecture, API contract, operator builder, manifest validator, knowledge search, trace explainer, SDK assistant, roadmap, and overview. The directory is named "banzamia" when its subject is BanzAI.

**Canonical name:** `docs/banzai/`

---

## Rank 10 — `docker/banzamia/` Directory (Banzami repo)

**Classification:** LEGACY
**Wave:** 1

The Docker infrastructure for deploying the BanzAI backend service. The directory name predates ADR-025.

**Canonical name:** `docker/banzai/`

---

## Rank 11 — `banzamia-canonical-architecture.svg`

**Classification:** MISLEADING
**Wave:** 2

This SVG is titled "Arquitectura Canónica do Ecossistema Banza" and depicts the full BANZA ecosystem (Rust kernel → Go services → BanzAI → Applications). The filename implies this is BanzamIA's canonical architecture. The subject is the BANZA ecosystem canonical architecture.

**Canonical name:** `banzai-canonical-architecture.svg`

---

## Rank 12 — `banzamia-product-architecture.svg`

**Classification:** MISLEADING
**Wave:** 2

This SVG shows BanzAI's 16-module architecture across 3 layers. The filename "banzamia-product-architecture" implies this is a product of Banzamia. The canonical name reflects what is depicted: the BanzAI module architecture.

**Canonical name:** `banzai-product-architecture.svg`

---

## Rank 13 — `BANZAMI_IMPLEMENTATION_MATRIX.json`

**Classification:** LEGACY
**Wave:** 3

The validation matrix for the entire Banza ecosystem implementation. "BANZAMI" in the filename is partially correct (it tracks Banzami's implementation) but the file also covers protocol-level invariants, certification, and federation — making "BANZA" more accurate.

**Canonical name:** `BANZA_IMPLEMENTATION_MATRIX.json`

---

## Rank 14 — `HomeBanzamIAEntry` Component

**Classification:** MISLEADING
**Wave:** 2

The BanzAI entry widget on the homepage. Encountered by every visitor to banzami.org. Its name encodes the pre-ADR-025 portmanteau in the most prominent user-facing component.

**Canonical name:** `HomeBanzAIEntry`

---

## Rank 15 — `HeroBanzamIAWidget` Component

**Classification:** MISLEADING
**Wave:** 2

The hero section BanzAI interaction widget. Appears on every page load.

**Canonical name:** `HeroBanzAIWidget`

---

## Rank 16 — `banzamia-internal-architecture.svg`

**Classification:** MISLEADING
**Wave:** 2

Shows BanzAI's internal architecture (RAG pipeline, knowledge graph, orchestrator). The subject is BanzAI, not BanzamIA.

**Canonical name:** `banzai-internal-architecture.svg`

---

## Rank 17 — `banzamia-cognitive-layer.svg`

**Classification:** MISLEADING
**Wave:** 2

Shows BanzAI as a four-layer cognitive architecture. The subject is BanzAI.

**Canonical name:** `banzai-cognitive-layer.svg`

---

## Rank 18 — `BanzamIAChat` Component

**Classification:** MISLEADING
**Wave:** 2

The chat interface component of BanzAI.

**Canonical name:** `BanzAIChat`

---

## Rank 19 — `BanzamIASidebar` Component

**Classification:** MISLEADING
**Wave:** 2

The module navigation sidebar of BanzAI.

**Canonical name:** `BanzAISidebar`

---

## Rank 20 — `banzamia-truth-model.svg`

**Classification:** MISLEADING
**Wave:** 2

Depicts the "Tools determine truth / AI explains truth" model — BanzAI's epistemological architecture.

**Canonical name:** `banzai-truth-model.svg`

---

## Rank 21 — `package.json "name": "banzamia"` (Banzami repo)

**Classification:** MISLEADING
**Wave:** 1

Every developer who reads the backend package manifest sees `"banzamia"` as the package name and `"BanzamIA — AI-native protocol agent for Banzami"` as the description. Both encode the pre-ADR-025 identity.

**Canonical name:** `"banzai"`, description: `"BanzAI — Protocol Operating System"`

---

## Rank 22 — `BANZAMI_ECOSYSTEM_REFERENCE.md`

**Classification:** MISLEADING
**Wave:** 2 (or 3, alongside BANZAMI_REFERENCE.md)

The architecture-first complement to the reference document. Its subject is the BANZA ecosystem, not Banzami specifically.

**Canonical name:** `BANZA_ECOSYSTEM_REFERENCE.md`

---

## Rank 23 — `BanzamIAIcon` Component

**Classification:** MISLEADING
**Wave:** 2

The icon component for BanzAI — the glyph that appears in the sidebar, chat, and hero widget.

**Canonical name:** `BanzAIIcon`

---

## Rank 24 — Docker Container Names (`banzamia-api`, `banzamia-qdrant`)

**Classification:** LEGACY
**Wave:** 1

Infrastructure names visible in `docker ps` output and server logs. Engineers monitoring the server see "banzamia-api" and must mentally translate to "BanzAI API".

**Canonical names:** `banzai-api`, `banzai-qdrant`

---

## Rank 25 — `BanzamIASourcesPanel` Component

**Classification:** MISLEADING
**Wave:** 2

The citations panel that appears alongside BanzAI's responses.

**Canonical name:** `BanzAISourcesPanel`

---

## Structural Conclusion

After completing all four waves, the following canonical structure will be visible in the filesystem:

```
Banza repo:
  docs/
    BANZA_REFERENCE.md           ← Protocol owns the reference
    banzai/                      ← BanzAI documentation
    architecture/
      BANZA_ECOSYSTEM_REFERENCE.md
  apps/docs/
    app/
      banzai/                    ← /banzai route
      sobre-o-banzai/            ← /sobre-o-banzai route
    components/
      banzai/                    ← BanzAI components
        BanzAIApp.tsx
        BanzAIChat.tsx
        ...
    lib/
      banzai-client.ts           ← BanzAI API client

Banzami repo:
  apps/
    banzai/                      ← BanzAI backend engine
  docker/
    banzai/                      ← BanzAI Docker config
```

At that point, a developer exploring the codebase for the first time will see, without reading any documentation:

- BANZA is the protocol (owns the reference document)
- BanzAI is the Protocol Operating System (has its own directory, its own components, its own backend service)
- Banzami is the operator (has its own apps, its own brand assets, its own mobile apps)

The structural hierarchy will match the conceptual hierarchy of ADR-025.

---

*Priority report completed: 2026-05-30. No files modified.*
