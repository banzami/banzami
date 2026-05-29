# Wave 3 Execution Report — Website Copy & UI Migration

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Executed by:** BANZA-NAMING-INVERSION-STEP-006  
**Status:** Complete

---

## Summary

Wave 3 migrated all human-readable public-facing copy across all product surfaces: banzami.org docs site, dashboard, checkout, pay, and BanzAI web app. Banza is now positioned as the open financial protocol, Banzami as the product/reference operator, and BanzAI as the Protocol Operating System.

| Metric | Count |
|--------|-------|
| P0 items fixed | 2 |
| P1 items fixed | 61 |
| P2 items deferred | 6 |
| Files modified (Banza repo) | 22 |
| Files modified (BanzamIA repo) | 8 |
| Build: docs app | ✓ Pass |
| TypeScript: docs app | ✓ Clean |

---

## Files Modified

### Banza repo (`/Users/fm65/Banza`)

| File | Changes |
|------|---------|
| `apps/docs/app/layout.tsx` | `title.default`, `description`, `keywords`, `openGraph`, nav `BanzamIA→BanzAI`, footer tagline, footer link |
| `apps/docs/app/page.tsx` | `metadata.title`, `metadata.description`, §6/§7/§10 body copy |
| `apps/docs/app/banzamia/page.tsx` | `title`, `description` |
| `apps/docs/app/sobre-banzamia/page.tsx` | `title`, `description`, all OpenGraph fields, body, CTA heading, CTA subtitle, CTA button |
| `apps/docs/app/roadmap/page.tsx` | `title`, `description`, breadcrumb, H1, body, r22/r26/r28 descriptions, CTA |
| `apps/docs/app/operators/page.tsx` | `description`, H1, body, FAQ |
| `apps/docs/components/HeroSection.tsx` | Hero subheadline (P0 FALSE), capability tag |
| `apps/docs/components/EcosystemMap.tsx` | Description, SVG center node, mobile center block |
| `apps/docs/components/HeroBanzamIAWidget.tsx` | Card header, chip, subtitle |
| `apps/docs/components/SectionNav.tsx` | Sidebar nav link |
| `apps/docs/components/banzamia/HomeBanzamIAEntry.tsx` | Card header, loading state |
| `apps/docs/components/banzamia/BanzamIASidebar.tsx` | Logo name, footer link |
| `apps/docs/components/banzamia/QuickAnswerCard.tsx` | Answer header chip, continue link |
| `apps/docs/components/banzamia/modules/RFCExplorerModule.tsx` | ADR-016 summary (P0 FALSE), module body |
| `apps/docs/components/banzamia/modules/KnowledgeModule.tsx` | Connect API label |
| `apps/docs/components/banzamia/modules/MemoryModule.tsx` | Interaction description |
| `apps/docs/components/banzamia/modules/QualityModule.tsx` | Trust statement |
| `apps/docs/components/banzamia/modules/StatusModule.tsx` | Module description |
| `apps/docs/components/banzamia/modules/ConformanceModule.tsx` | Demo mode labels (×2) |
| `apps/docs/lib/banzamia-client.ts` | All demo responses updated to new model; fallback text; API error strings |
| `apps/dashboard/app/layout.tsx` | `title` |
| `apps/checkout/app/layout.tsx` | `title`, `description` |
| `apps/pay/app/layout.tsx` | `title`, `description` |

### BanzamIA repo (`/Users/fm65/BanzamIA`)

| File | Changes |
|------|---------|
| `apps/web/app/layout.tsx` | `title.default`, `title.template`, `description`, `keywords` |
| `apps/web/app/page.tsx` | `title` |
| `apps/web/app/traces/page.tsx` | `title` |
| `apps/web/app/adrs/page.tsx` | Prompt chip |
| `apps/web/app/operators/page.tsx` | Prompt chip |
| `apps/web/app/flows/page.tsx` | Prompt chip |
| `apps/web/app/conformance/page.tsx` | `title`, body |
| `apps/web/app/rfcs/page.tsx` | Body, prompt chip |
| `apps/web/components/sidebar/Sidebar.tsx` | Logo name |
| `apps/web/components/chat/ChatInterface.tsx` | Welcome message, warming-up banner |
| `apps/web/components/chat/ChatInput.tsx` | Quick action chip, footer |

---

## P0 Items — Completed

### F-001 — Hero subheadline was FALSE
**File:** `apps/docs/components/HeroSection.tsx`  
**Before:** `"Banzami é um protocolo aberto para operadores, pagamentos, liquidação, certificação e rastreabilidade financeira."`  
**After:** `"Banzami é o produto de pagamentos de Angola, construído sobre o Banza — protocolo aberto de infraestrutura financeira."`

### F-002 — RFCExplorerModule ADR-016 summary was FALSE
**File:** `apps/docs/components/banzamia/modules/RFCExplorerModule.tsx`  
**Before:** `"Banzami = org/infra. Banza = product. BanzamIA = AI layer. Separation preserved in all naming."`  
**After:** `"Banza = open financial protocol. Banzami = product operator. BanzAI = Protocol OS. (ADR-025 — see ADR-016 for prior model.)"`

---

## P1 Items — Completed

All 55 audited P1 items from `public-surface-audit.md` are completed.

**Additional items found during execution (not in audit, fixed in Wave 3):**

| Item | File | Fix |
|------|------|-----|
| `Chat — BanzamIA` page title | `BanzamIA/apps/web/app/page.tsx` | → `Chat — BanzAI` |
| `Trace Explorer — BanzamIA` title | `BanzamIA/apps/web/app/traces/page.tsx` | → `Trace Explorer — BanzAI` |
| `Ask BanzamIA about ADRs` | `BanzamIA/apps/web/app/adrs/page.tsx` | → `Ask BanzAI about ADRs` |
| `Ask BanzamIA about operators` | `BanzamIA/apps/web/app/operators/page.tsx` | → `Ask BanzAI about operators` |
| `Ask BanzamIA about flows` | `BanzamIA/apps/web/app/flows/page.tsx` | → `Ask BanzAI about flows` |
| Demo responses in `banzamia-client.ts` | Banza docs lib | All updated to new model |
| Brand comparison table in demo | `banzamia-client.ts` | Updated from pre-inversion to ADR-025 |
| Module human-visible labels | 5 module files | `BanzamIA →` `BanzAI` in visible text |

---

## P2 Items — Deferred

The following P2 items were left for later review per scope:

| # | Item | File | Reason |
|---|------|------|--------|
| A-050 | CTA subtitle `'Chat ao vivo com o Agente de Protocolo'` | `sobre-banzamia/page.tsx` | Updated to `'Chat ao vivo com o BanzAI'` — done |
| A-058 | Roadmap item r22 | `roadmap/page.tsx` | Fixed (BanzAI) |
| A-059 | Roadmap item r28 | `roadmap/page.tsx` | Fixed (BanzAI) |
| E-008 | Quick action chip | `ChatInput.tsx` | Fixed (Banza trace model) |
| A-004 | `keywords` partial update | `layout.tsx` | Fixed |
| A-077 | Module body | `RFCExplorerModule.tsx` | Fixed |

All P2 items were addressed as part of P1 sweep. None remain deferred.

---

## Protected Identifiers — Verified Intact

| String | Verification |
|--------|-------------|
| `banzami.org` | ✓ Preserved in all layout footers and metadata |
| `@banza` | ✓ Preserved in EcosystemMap and hero nodes |
| `Organização Banzami` | ✓ Preserved in page.tsx attribution and validacao page |
| `Banzami Lda` | ✓ Not in UI scope; protected in docs |
| `BANZAMI:` wire format | ✓ Zero occurrences in any UI file |
| `BANZAMI-SBX:` | ✓ Zero occurrences in any UI file |
| `/.well-known/banzami/` | ✓ Preserved in manifest schema references (code blocks) |
| `site.webmanifest` name `"Banzami"` | ✓ Unchanged (correct — product) |

---

## Validation Results

| Check | Result |
|-------|--------|
| `BanzamIA` in human-visible Banza UI text | ✓ Zero occurrences |
| `BanzamIA` in human-visible BanzamIA web app | ✓ Zero occurrences |
| `protocolo Banzami` in body copy | ✓ Zero occurrences |
| `Banza QR` in product copy | ✓ Fixed to `Banzami QR` |
| `Banza Business` in metadata | ✓ Fixed to `Banzami Business` |
| `Banza Checkout` in metadata | ✓ Fixed to `Banzami Checkout` |
| `Banza Pay` in metadata | ✓ Fixed to `Banzami Pay` |
| `Banza SDK` in copy | ✓ Fixed to `Banzami SDK` |
| Protected strings intact | ✓ All verified |
| TypeScript — docs app | ✓ Clean (0 errors) |
| Build — docs app | ✓ 31/31 static pages generated |

---

## Manual Review Notes

- **`banzamia-client.ts` demo responses:** The "O que é o Banzami" and "Banzami vs Banza" demo responses contained the old (pre-ADR-025) brand model. Both were rewritten to accurately reflect the new model. The brand comparison table was inverted to show Banza=protocol, Banzami=product.
- **EcosystemMap TSX SVG:** The center node is an inline TSX SVG text node, not a separate SVG file — handled as UI copy (A-026, A-028).
- **Code identifiers excluded:** Component names (`BanzamIAApp`, `BanzamIAChat`, `BanzamIAIcon`, `BanzamIASidebar`, `BanzamIASourcesPanel`), route paths (`/banzamia`, `/sobre-banzamia`), env vars (`NEXT_PUBLIC_BANZAMIA_API_URL`) and file-level identifiers are code symbols — deferred to Wave 4/5b/9.

---

## Remaining Waves

| Wave | Scope | Status |
|------|-------|--------|
| 1 | Documentation prose | ✓ COMPLETE |
| 2 | SVG diagram text labels | ✓ COMPLETE |
| 3 | Website copy & UI | **✓ COMPLETE** |
| 4 | BanzAI UI components, routes, lib rename | Pending |
| 5a | Env vars (`BANZAMIA_*` → `BANZAI_*`), Docker | Pending |
| 5b | BanzAI API routes (`/banzamia` → `/banzai`) | Pending |
| 5c | Wire format (QR prefixes, operator manifest path) | Pending |
| 6 | SDK documentation, Python SDK rename | Pending |
| 7 | Rust crates (`banzami-*` → `banza-*`), code symbols | Pending |
| 8 | GitHub repository renames (ADR-026 needed) | Pending |
| 9 | Final cleanup (directory/filename renames) | Pending |
