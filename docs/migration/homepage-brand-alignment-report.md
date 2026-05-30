---
title: Homepage and Root Brand Alignment Report — BANZA-NAMING-INVERSION-STEP-009C
version: 1.0
date: 2026-05-30
status: COMPLETE
---

# Homepage and Root Brand Alignment Report

BANZA is now the primary visible identity on banzami.org. Banzami is correctly positioned as the reference operator/product. BanzAI is correctly identified as the Protocol Operating System.

---

## Problem Addressed

The global header and footer displayed "Banzami" as the dominant site wordmark, making visitors perceive Banzami as the root identity. Under ADR-025, the site is the BANZA institutional site — the protocol should lead.

Additionally, several page metadata blocks and the BanzAI widget descriptor still described the site with "ecossistema Banzami" or "Banzami" as a root identifier rather than as the product.

---

## Branding Hierarchy After This Step

| Identity | Role | Visibility |
|----------|------|------------|
| **Banza** | Protocol / infrastructure / organization | Primary — navbar wordmark, footer wordmark, page titles, sidebar label |
| **BanzAI** | Protocol Operating System | Navigation (gold star), widget, /banzamia shell |
| **Banzami** | Reference operator / payment product | Subheadline, product sections, SDK references, operator docs |

---

## Files Changed

### `apps/docs/app/layout.tsx`

| Location | Before | After |
|----------|--------|-------|
| Header logo wordmark | `Banzami` | `Banza` |
| Header logo image alt | `Banzami` | `Banza` |
| Footer logo wordmark | `Banzami` | `Banza` |
| Footer logo image alt | `Banzami` | `Banza` |

### `apps/docs/components/HeroBanzamIAWidget.tsx`

| Location | Before | After |
|----------|--------|-------|
| Widget descriptor line | `O Sistema Operativo de Protocolo do ecossistema Banzami.` | `O Sistema Operativo do Protocolo Banza.` |

### `apps/docs/app/page.tsx`

| Location | Before | After |
|----------|--------|-------|
| Source attribution ADR ref | `ADR-015 · ADR-016` | `ADR-015 · ADR-025` |

### `apps/docs/app/roadmap/page.tsx`

| Location | Before | After |
|----------|--------|-------|
| Page metadata description | `Protocol Operating System do ecossistema Banzami.` | `Protocol Operating System do Protocolo Banza.` |
| Breadcrumb home link | `Banzami` | `Banza` |

### `apps/docs/app/validacao/page.tsx`

| Location | Before | After |
|----------|--------|-------|
| Page metadata description | `validação do ecossistema Banzami` | `validação do ecossistema Banza` |

### `apps/docs/app/reference/page.tsx`

| Location | Before | After |
|----------|--------|-------|
| Page H1 heading | `Banzami — Referência Oficial` | `Banza — Referência Oficial do Protocolo` |
| Page metadata title | `Banzami — Referência Oficial` | `Banza — Referência Oficial do Protocolo` |
| Page metadata description | `ecossistema Banzami — 20 secções…` | `Protocolo Banza — 20 secções…` |

---

## What Was NOT Changed

Per ADR-025 domain exception and Wave 4–9 deferrals:

- `banzami.org` domain — unchanged
- `/images/banza/banzami-logo.png` — image filename unchanged (only alt text updated)
- `/banzamia`, `/sobre-banzamia` routes — Wave 5b
- `BanzamIAApp`, `BanzamIAChat`, etc. — component identifiers, Wave 4
- `NEXT_PUBLIC_BANZAMIA_API_URL` — env var name, Wave 5a
- `Organização Banzami` — legal entity name, protected
- `@banzami.org` — email domain, protected
- "O que é o Banzami" footer link — correctly names Banzami the product
- "ecossistema Banzami" in `HomeBanzamIAEntry.tsx:85` — intentional: describes the Banzami operator product ecosystem users are integrating

---

## Visitor Mental Model After This Step

A visitor landing on banzami.org now reads:

1. **Navbar logo:** "Banza" — protocol identity
2. **Sidebar:** "BANZA — Documentação do Protocolo"
3. **Hero badge:** "Infraestrutura Financeira Programável para Angola" — protocol signal
4. **H1:** "Infraestrutura financeira programável." — protocol signal
5. **Subheadline:** "Banzami é o produto de pagamentos de Angola, construído sobre o Banza — protocolo aberto de infraestrutura financeira." — correctly positions both entities
6. **BanzAI widget:** "Pergunte ao BanzAI — O Sistema Operativo do Protocolo Banza." — correct
7. **Footer:** "Banza — Protocolo Aberto de Infraestrutura Financeira para Angola"

The hierarchy is unambiguous: **Banza = protocol → Banzami = product → BanzAI = protocol OS.**

---

## Remaining Deferred Items

| Item | Wave | Notes |
|------|------|-------|
| Route `/banzamia` → `/banzai` | Wave 5b | Requires redirects + coordination |
| Route `/sobre-banzamia` → `/sobre-banzai` | Wave 5b | Requires redirects |
| `BanzamIA*` component identifiers | Wave 4 | No user-visible impact |
| `NEXT_PUBLIC_BANZAMIA_API_URL` env var | Wave 5a | Coordinated deployment |
| `docs/BANZAMI_REFERENCE.md` filename reference | Wave 9 | File rename + redirect |
| Logo image file `/images/banza/banzami-logo.png` | Wave 9 | Image CDN + filename change |

---

## Validation

- TypeScript typecheck: 0 errors
- Next.js build: success
- String sweep: no remaining Banzami-as-root-identity visible strings outside protected identifiers

---

*Applied: 2026-05-30. Committed as `fix(identity): homepage and root brand alignment — Banza leads`.*
