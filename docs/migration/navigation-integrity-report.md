---
title: Navigation Integrity Report — BANZA-NAMING-INVERSION-STEP-010B
version: 1.0
date: 2026-05-30
status: COMPLETE
---

# Navigation Integrity Report

All five production 404s resolved. All navigation surfaces audited and aligned to ADR-025. 51/51 tests pass. Deployed.

---

## Navigation Inventory

### Top Navbar

| Label | Route | Exists? | ADR-025 Compliant? | Action |
|---|---|---|---|---|
| Referência | `/reference` | ✓ | ✓ | — |
| Programadores | `/banzami-para-programadores` | ✓ | ✓ | Fixed (was `/banza-para-programadores`) |
| Comerciantes | `/banzami-para-comerciantes` | ✓ | ✓ | Fixed (was `/banza-para-comerciantes`) |
| Arquitectura | `/arquitectura-tecnica` | ✓ | ✓ | — |
| Segurança | `/seguranca-e-integridade-financeira` | ✓ | ✓ | — |
| Operadores | `/operators` | ✓ | ✓ | — |
| Validação | `/validacao` | ✓ | ✓ | — |
| BanzAI ★ | `/banzamia` | ✓ | ✓ | — |

### Sidebar (SectionNav)

| Label | Route | Exists? | ADR-025 Compliant? | Action |
|---|---|---|---|---|
| Início | `/` | ✓ | ✓ | — |
| BanzAI | `/sobre-banzamia` | ✓ | Note (Wave AX) | Deferred — architectural decision pending |
| Referência completa | `/reference` | ✓ | ✓ | — |
| §1 O que é o Banza? | `/o-que-e-o-banza` | ✓ | ✓ | — |
| §2 Princípios Fundamentais | `/principios-fundamentais` | ✓ | ✓ | — |
| §3 Visão Geral do... | `/visao-geral-do-ecossistema` | ✓ | ✓ | — |
| §4 Arquitectura Técnica | `/arquitectura-tecnica` | ✓ | ✓ | — |
| §5 Representação Monetária | `/representacao-monetaria` | ✓ | ✓ | — |
| §6 Governança | `/governanca` | ✓ | ✓ | — |
| §7 Modelo de Certificação | `/modelo-de-certificacao` | ✓ | ✓ | — |
| §8 Federação | `/federacao` | ✓ | ✓ | — |
| §9 BanzAI | `/sobre-banzamia` (override) | ✓ | Note (Wave AX) | Section 9 slug `/banzai` exists as orphan; routing decision pending |
| §10 Banzami para Programadores | `/banzami-para-programadores` | ✓ | ✓ | — |
| §11 Banzami para Comerciantes | `/banzami-para-comerciantes` | ✓ | ✓ | — |
| §12 Para Consumidores | `/para-consumidores` | ✓ | ✓ | — |
| §13 Segurança e Integridade... | `/seguranca-e-integridade-financeira` | ✓ | ✓ | — |
| §14 Sandbox e Ambiente de... | `/sandbox-e-ambiente-de-testes` | ✓ | ✓ | — |
| §15 Por que Angola... | `/por-que-angola-por-que-agora` | ✓ | ✓ | — |
| §16 Roadmap | `/roadmap` | ✓ | ✓ | — |
| §17 Declaração de Visão | `/declaracao-de-visao` | ✓ | ✓ | — |

### Footer

| Label | Route | Exists? | ADR-025 Compliant? | Action |
|---|---|---|---|---|
| O que é o Banza? | `/o-que-e-o-banza` | ✓ | ✓ | Fixed (was `/o-que-e-o-banzami`, label was "O que é o Banzami") |
| Programadores | `/banzami-para-programadores` | ✓ | ✓ | Fixed (was `/banza-para-programadores`) |
| Comerciantes | `/banzami-para-comerciantes` | ✓ | ✓ | Fixed (was `/banza-para-comerciantes`) |
| Arquitectura | `/arquitectura-tecnica` | ✓ | ✓ | — |
| Referência completa | `/reference` | ✓ | ✓ | — |
| Operadores | `/operators` | ✓ | ✓ | — |
| Validação | `/validacao` | ✓ | ✓ | — |
| BanzAI | `/banzamia` | ✓ | ✓ | — |

---

## Broken Links Fixed (Wave AA — P0)

| # | File:line | Change type | Before | After |
|---|---|---|---|---|
| AA-1 | `apps/docs/app/layout.tsx:82` | navbar href | `/banza-para-programadores` | `/banzami-para-programadores` |
| AA-2 | `apps/docs/app/layout.tsx:83` | navbar href | `/banza-para-comerciantes` | `/banzami-para-comerciantes` |
| AA-3 | `apps/docs/app/layout.tsx:151` | footer href | `/o-que-e-o-banzami` | `/o-que-e-o-banza` |
| AA-4 | `apps/docs/app/layout.tsx:151` | footer label | "O que é o Banzami" | "O que é o Banza?" |
| AA-5 | `apps/docs/app/layout.tsx:152` | footer href | `/banza-para-programadores` | `/banzami-para-programadores` |
| AA-6 | `apps/docs/app/layout.tsx:153` | footer href | `/banza-para-comerciantes` | `/banzami-para-comerciantes` |

---

## Redirects Fixed (Wave AE — P2)

**Removed 14 redirects** whose destinations no longer exist (reference restructured from 20 to 17 sections).

**Fixed 2 redirects** with updated destinations:

| Source | Old destination (broken) | New destination |
|---|---|---|
| `/what-is-banzami` | `/o-que-e-o-banzami` (404) | `/o-que-e-o-banza` |
| `/banzami-for-consumers` | `/banzami-para-consumidores` (404) | `/para-consumidores` |

**Retained 4 working redirects:**

| Source | Destination |
|---|---|
| `/banzami-for-merchants` | `/banzami-para-comerciantes` |
| `/banzami-for-developers` | `/banzami-para-programadores` |
| `/security-financial-integrity` | `/seguranca-e-integridade-financeira` |
| `/technical-architecture` | `/arquitectura-tecnica` |

Final redirect count: **6** (all with verified destinations).

---

## Reference Document Fixed (Waves AB + AC)

### TOC Anchor Fixes (Wave AB)

| # | Line | Before | After |
|---|---|---|---|
| AB-1 | 18 | `#1-o-que-é-o-banzami` | `#1-o-que-e-o-banza` |
| AB-2 | 26 | `#9-banzamia` | `#9-banzai` |
| AB-3 | 27 | `#10-banza-para-programadores` | `#10-banzami-para-programadores` |
| AB-4 | 28 | `#11-banza-para-comerciantes` | `#11-banzami-para-comerciantes` |

### Content Fixes (Wave AC)

| # | Location | Before | After |
|---|---|---|---|
| AC-1 | `BANZAMI_REFERENCE.md:1427` | "o protocolo Banzami auto-gerível" | "o protocolo Banza auto-gerível" |
| AC-2 | `CertificationCopilotModule.tsx:62` | "against Banzami certification requirements" | "against Banza protocol certification requirements" |
| AC-3 | `ConformanceModule.tsx:32` | "Run the Banzami certification suite" | "Run the Banza certification suite" |
| AC-4 | `OperatorBuilderModule.tsx:71` | "building and certifying a Banzami operator" | "building and certifying a Banza protocol operator" |
| AC-5 | `BANZAMI_REFERENCE.md:1930` | ADR-016 citation (standalone) | Added: "(superseded for brand hierarchy by ADR-025)" |

---

## Test Suite Fixed (Wave AD + pre-existing)

### Wave AD — Stale ADR-025 assertions

| # | Line | Before | After |
|---|---|---|---|
| AD-1 | 29 | `toBe('o-que-e-o-banzami')` | `toBe('o-que-e-o-banza')` |
| AD-2 | 223 | `toBe('O que é o Banzami?')` | `toBe('O que é o Banza?')` |
| AD-3 | 280–282 | `toBe('O que é o Banzami?')` | `toBe('O que é o Banza?')` |

### Pre-existing failures — reference restructured 20 → 17 sections

| Change | Before | After |
|---|---|---|
| Section count assertion | `toHaveLength(20)` | `toHaveLength(17)` |
| Sequential numbering assertion | `Array.from({ length: 20 }, ...)` | `Array.from({ length: 17 }, ...)` |
| Last section number | `toBe(20)` | `toBe(17)` |
| Last section lookup | `getSectionByNumber(20)` / `'Declaração de Visão Final'` | `getSectionByNumber(17)` / `'Declaração de Visão'` |
| Out-of-range lookup | `getSectionByNumber(21)` | `getSectionByNumber(18)` |
| Consistency loop | `for n = 1 to 20` | `for n = 1 to 17` |
| Slug count | `toHaveLength(20)` | `toHaveLength(17)` |
| Known-slug lookup | `'a-visao'`, number 4, title 'A Visão' | `'arquitectura-tecnica'`, number 4, title 'Arquitectura Técnica' |
| Subsection threshold | `toBeGreaterThanOrEqual(100)` | `toBeGreaterThanOrEqual(90)` |

**Result: 51/51 tests pass.**

---

## Consistency Validation Matrix

| Surface | Before | After | Status |
|---|---|---|---|
| Navbar — Programadores | `/banza-para-programadores` (404) | `/banzami-para-programadores` | ✓ |
| Navbar — Comerciantes | `/banza-para-comerciantes` (404) | `/banzami-para-comerciantes` | ✓ |
| Footer — §1 label | "O que é o Banzami" | "O que é o Banza?" | ✓ |
| Footer — §1 link | `/o-que-e-o-banzami` (404) | `/o-que-e-o-banza` | ✓ |
| Footer — Programadores | `/banza-para-programadores` (404) | `/banzami-para-programadores` | ✓ |
| Footer — Comerciantes | `/banza-para-comerciantes` (404) | `/banzami-para-comerciantes` | ✓ |
| Reference TOC §1 anchor | `#1-o-que-é-o-banzami` (broken) | `#1-o-que-e-o-banza` | ✓ |
| Reference TOC §9 anchor | `#9-banzamia` (broken) | `#9-banzai` | ✓ |
| Reference TOC §10 anchor | `#10-banza-para-programadores` (broken) | `#10-banzami-para-programadores` | ✓ |
| Reference TOC §11 anchor | `#11-banza-para-comerciantes` (broken) | `#11-banzami-para-comerciantes` | ✓ |
| Reference §9 body | "protocolo Banzami" | "protocolo Banza" | ✓ |
| Certification Copilot UI | "Banzami certification requirements" | "Banza protocol certification requirements" | ✓ |
| Conformance Runner UI | "Banzami certification suite" | "Banza certification suite" | ✓ |
| Operator Builder UI | "certifying a Banzami operator" | "certifying a Banza protocol operator" | ✓ |
| next.config.ts redirects | 20 entries (14 dead destinations) | 6 entries (all valid) | ✓ |
| Test assertions | 11 stale / failing | 0 failing | ✓ |

---

## Remaining Deferred Items

### Wave AX — Section 9 Routing (requires architectural decision)

**Current state:**
- `/banzai` — exists, renders section 9 content, zero nav links (orphan)
- `/sobre-banzamia` — exists, receives all section 9 nav links via override in `SectionNav.tsx` and `SectionCard.tsx`

**Decision required before any code change:**
- Option A: Make `/sobre-banzamia` canonical — add redirect `/banzai` → `/sobre-banzamia`
- Option B: Make `/banzai` canonical (recommended — slug-derived from section title "BanzAI") — add redirect `/sobre-banzamia` → `/banzai`, remove nav overrides

**Not touched in this step. Blocked on product owner decision.**

### Waves 4–9 (deferred, out of scope)

| Item | Wave |
|---|---|
| Component identifiers `BanzamIA*` | Wave 4 |
| Env var `BANZAMIA_*_URL` | Wave 5a |
| Routes `/banzamia`, `/sobre-banzamia` | Wave 5b (blocked on Wave AX) |
| Wire format `/.well-known/banzami/`, `BANZAMI:` QR prefix | Wave 5c — PROTECTED |
| File/directory renames | Wave 9 |

---

## Commits

| Hash | Message |
|---|---|
| `a0dbfa5` | fix(nav): Wave AA — repair broken nav and footer links post-ADR-025 |
| `4f4c41a` | fix(redirects): Wave AE — clean redirect table, fix 2, remove 14 dead destinations |
| `2cdad77` | fix(reference): Waves AB+AC — fix 4 broken TOC anchors, 1 false protocol attribution, ADR-025 citation |
| `93bde43` | fix(banzai): Wave AC — correct false Banzami certification attributions in BanzAI modules |
| `80c67ca` | test(reference): Waves AD + pre-existing — sync assertions to current reference structure |

Pushed to `origin/main`. Deployed via `./deploy.sh docs-frontend`.

---

*Applied: 2026-05-30. Build: clean. Tests: 51/51 pass.*
