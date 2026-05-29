# Wave 3 UI Migration Plan — Website Copy & Public Surface

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Source:** BANZA-NAMING-INVERSION-STEP-005 (public-surface-audit.md)  
**Status:** Plan — not yet executed

---

## Scope

Wave 3 covers all human-readable copy on public surfaces:

- `apps/docs` — banzami.org docs site (all pages, components, metadata)
- `apps/dashboard` — Banzami Business dashboard
- `apps/checkout` — Banzami Checkout
- `apps/pay` — Banzami Pay
- `BanzamIA/apps/web` — BanzAI web app

**Out of scope for Wave 3:**

| Surface | Wave |
|---------|------|
| Route paths (`/banzamia`, `/sobre-banzamia`) | 5b |
| Env vars (`BANZAMIA_*`) | 5a |
| Wire format strings (`BANZAMI:`, `BANZAMI-SBX:`) | 5c |
| Rust crate names, code symbols | 7 |
| Directory/filename renames | 9 |

---

## Canonical Reference (post-inversion)

| Name | Role |
|------|------|
| **Banza** | Open financial protocol / infrastructure kernel |
| **Banzami** | Product — the reference operator and payment app built on Banza |
| **BanzAI** | Protocol Operating System (was BanzamIA) |
| `banzami.org` | Domain — permanent exception |
| `@banza` | Identity namespace — permanent exception |
| `Banzami Lda` | Legal entity — permanent exception |
| `Organização Banzami` | Org name — permanent exception |

---

## Priority Order

Execute in this order within each wave:

1. **P0 — FALSE** (2 items): Fix immediately — these create wrong product understanding
2. **P1 — OUTDATED / MISLEADING** (53 items): Core rename pass
3. **P2 — PARTIALLY CORRECT** (6 items): Surgical fixes requiring judgment

---

## Group 1 — Hero Sections

**Priority: P0 + P1**

### 1.1 Home hero subheadline — FALSE (A-018)

**File:** `apps/docs/components/HeroSection.tsx`  
**Current:** `"Banzami é um protocolo aberto para operadores, pagamentos, liquidação, certificação e rastreabilidade financeira."`  
**Issue:** Banzami is the product, not the protocol. This is the highest-priority false statement on the site.  
**Fix:** `"Banzami é o produto de pagamentos de Angola, construído sobre o Banza — protocolo aberto de infraestrutura financeira."`

### 1.2 Home hero capability tag (A-019)

**File:** `apps/docs/components/HeroSection.tsx` — CAPABILITY_TAGS  
**Current:** `'BanzamIA'`  
**Fix:** `'BanzAI'`

### 1.3 Home page description (A-017)

**File:** `apps/docs/app/page.tsx` — `metadata.description`  
**Current:** `'Banza é a rede angolana de pagamentos... Banza SDKs oficiais.'`  
**Fix:** `'Banzami é a rede angolana... Banzami SDKs oficiais.'`

---

## Group 2 — Navigation

**Priority: P1**

All navigation changes are in `apps/docs/app/layout.tsx`.

| # | Location | Current | Fix |
|---|----------|---------|-----|
| A-001 | `metadata.title.default` | `'Banza — Pagamentos Instantâneos em Kwanza \| Banzami'` | `'Banzami — Pagamentos Instantâneos em Kwanza'` |
| A-005 | `metadata.openGraph.title` | `'Banza — Pagamentos Instantâneos em Kwanza \| Banzami'` | `'Banzami — Pagamentos Instantâneos em Kwanza'` |
| A-009 | Top nav label | `'BanzamIA'` | `'BanzAI'` |
| A-010 | Footer nav label | `BanzamIA` | `BanzAI` |
| A-011 | Footer tagline | `Banza — Rede Angolana de Pagamentos...` | `Banzami — Rede Angolana de Pagamentos...` |

Note: nav `href` values (`/banzamia`) are NOT changed in Wave 3 — routes are Wave 5b.

---

## Group 3 — Metadata & SEO

**Priority: P1**

Covers `metadata.title`, `metadata.description`, `metadata.keywords`, and OpenGraph fields across all page files.

### 3.1 `apps/docs/app/layout.tsx` (global)

| # | Field | Current | Fix |
|---|-------|---------|-----|
| A-001 | `title.default` | `'Banza — Pagamentos... \| Banzami'` | `'Banzami — Pagamentos Instantâneos em Kwanza'` |
| A-003 | `description` | `...Banza SDK... Banza Business...` | `...Banzami SDK... Banzami Business...` |
| A-004 | `keywords` | `['Banza Business', 'Banza SDK', ...]` | `['Banzami Business', 'Banzami SDK', ...]` — keep `'Banza'` |
| A-005 | `openGraph.title` | `'Banza — Pagamentos... \| Banzami'` | `'Banzami — Pagamentos Instantâneos em Kwanza'` |
| A-006 | `openGraph.description` | `...Banza SDK e Banza Business.` | `...Banzami SDK e Banzami Business.` |

### 3.2 `apps/docs/app/page.tsx` (home)

| # | Field | Current | Fix |
|---|-------|---------|-----|
| A-016 | `title` | `'Banza — Pagamentos... \| Banzami'` | `'Banzami — Pagamentos Instantâneos em Kwanza'` |
| A-017 | `description` | `'Banza é a rede angolana...'` | `'Banzami é a rede angolana...'` |

### 3.3 `apps/docs/app/banzamia/page.tsx`

| # | Field | Current | Fix |
|---|-------|---------|-----|
| A-042 | `title` | `'BanzamIA — Protocol Operating System'` | `'BanzAI — Protocol Operating System'` |
| A-043 | `description` | `'BanzamIA é o Sistema Operativo do Protocolo Banzami...'` | `'BanzAI é o Sistema Operativo do Protocolo Banza...'` |

### 3.4 `apps/docs/app/sobre-banzamia/page.tsx`

| # | Field | Current | Fix |
|---|-------|---------|-----|
| A-044 | `title` | `'Sobre o BanzamIA'` | `'Sobre o BanzAI'` |
| A-045 | `description` | `'BanzamIA — o Sistema Operativo do Protocolo Banzami.'` | `'BanzAI — o Sistema Operativo do Protocolo Banza.'` |
| A-046 | `openGraph.title` | `'Sobre o BanzamIA · Banzami'` | `'Sobre o BanzAI · Banzami'` |
| A-047 | `openGraph.description` | `'O Sistema Operativo do Protocolo Banzami.'` | `'O Sistema Operativo do Protocolo Banza.'` |

### 3.5 `apps/docs/app/roadmap/page.tsx`

| # | Field | Current | Fix |
|---|-------|---------|-----|
| A-053 | `title` | `'Roadmap — BanzamIA Protocol Operating System'` | `'Roadmap — BanzAI Protocol Operating System'` |
| A-054 | `description` | `'Roadmap público do BanzamIA...'` | `'Roadmap público do BanzAI...'` |

### 3.6 `apps/docs/app/operators/page.tsx`

| # | Field | Current | Fix |
|---|-------|---------|-----|
| A-062 | `description` | `'Registo público de operadores Banzami'` | `'Registo público de operadores Banza'` |

### 3.7 `apps/dashboard/app/layout.tsx`

| # | Field | Current | Fix |
|---|-------|---------|-----|
| B-001 | `title` | `'Banza Business'` | `'Banzami Business'` |

### 3.8 `apps/checkout/app/layout.tsx`

| # | Field | Current | Fix |
|---|-------|---------|-----|
| C-001 | `title` | `'Banza Checkout'` | `'Banzami Checkout'` |
| C-002 | `description` | `'Pagamento seguro via Banza'` | `'Pagamento seguro via Banzami'` |

### 3.9 `apps/pay/app/layout.tsx`

| # | Field | Current | Fix |
|---|-------|---------|-----|
| D-001 | `title` | `'Banza Pay'` | `'Banzami Pay'` |
| D-002 | `description` | `'Pague com a app Banza'` | `'Pague com a app Banzami'` |

### 3.10 `BanzamIA/apps/web/app/layout.tsx`

| # | Field | Current | Fix |
|---|-------|---------|-----|
| E-001 | `title.default` | `'BanzamIA — Financial Infrastructure Intelligence'` | `'BanzAI — Financial Infrastructure Intelligence'` |
| E-002 | `title.template` | `'%s · BanzamIA'` | `'%s · BanzAI'` |
| E-003 | `description` | `'BanzamIA is the intelligence layer of the Banzami...'` | `'BanzAI is the intelligence layer of the Banza...'` |
| E-004 | `keywords` | `['Banzami', 'BanzamIA', ...]` | `['Banzami', 'BanzAI', 'Banza', ...]` |

---

## Group 4 — Sidebars

**Priority: P1**

### 4.1 `apps/docs/components/SectionNav.tsx`

| # | Element | Current | Fix |
|---|---------|---------|-----|
| A-015 | Sidebar nav link label | `'BanzamIA'` | `'BanzAI'` |

Note: sidebar `href` (`/sobre-banzamia`) deferred to Wave 5b.

### 4.2 `apps/docs/components/banzamia/BanzamIASidebar.tsx`

| # | Element | Current | Fix |
|---|---------|---------|-----|
| A-039 | Logo name | `BanzamIA` | `BanzAI` |
| A-041 | Footer link | `'Sobre o BanzamIA'` | `'Sobre o BanzAI'` |

### 4.3 `BanzamIA/apps/web/components/sidebar/Sidebar.tsx`

| # | Element | Current | Fix |
|---|---------|---------|-----|
| E-005 | Logo name | `'BanzamIA'` | `'BanzAI'` |

---

## Group 5 — Cards

**Priority: P1 + P2**

### 5.1 `apps/docs/components/HeroBanzamIAWidget.tsx`

| # | Element | Current | Fix |
|---|---------|---------|-----|
| A-030 | Header chip | `BanzamIA` | `BanzAI` |
| A-031 | Card subtitle | `'O Agente de Protocolo nativo de IA do ecossistema Banzami.'` | `'O Sistema Operativo de Protocolo do ecossistema Banzami.'` |

### 5.2 `apps/docs/components/banzamia/HomeBanzamIAEntry.tsx`

| # | Element | Current | Fix |
|---|---------|---------|-----|
| A-037 | Card header | `'Pergunte ao BanzamIA'` | `'Pergunte ao BanzAI'` |
| A-038 | Loading state | `'BanzamIA está a consultar o protocolo…'` | `'BanzAI está a consultar o protocolo…'` |

---

## Group 6 — BanzAI UI (Docs + Web App)

**Priority: P0 + P1**

### 6.1 `apps/docs/components/banzamia/modules/RFCExplorerModule.tsx` — FALSE (A-076)

**Current:** `"Banzami = org/infra. Banza = product. BanzamIA = AI layer."`  
**Issue:** Describes the pre-inversion naming model. Post-ADR-025 this is inverted.  
**Fix:** `"Banza = open financial protocol. Banzami = product operator. BanzAI = Protocol OS. (ADR-025 — see ADR-016 for prior model.)"`

### 6.2 `apps/docs/components/banzamia/modules/RFCExplorerModule.tsx` (A-077)

| # | Element | Current | Fix |
|---|---------|---------|-----|
| A-077 | Module body | `'Browse Banzami protocol decisions'` | `'Browse Banza protocol decisions'` |

### 6.3 `BanzamIA/apps/web/components/chat/ChatInterface.tsx`

| # | Element | Current | Fix |
|---|---------|---------|-----|
| E-007 | Welcome message | `"I'm BanzamIA — the intelligence layer of the Banzami..."` | `"I'm BanzAI — the intelligence layer of the Banza..."` |

### 6.4 `BanzamIA/apps/web/components/chat/ChatInput.tsx`

| # | Element | Current | Fix |
|---|---------|---------|-----|
| E-008 | Quick action chip | `'Explain the Banzami financial trace model'` | `'Explain the Banza financial trace model'` |

### 6.5 `BanzamIA/apps/web/app/conformance/page.tsx`

| # | Element | Current | Fix |
|---|---------|---------|-----|
| E-009 | `metadata.title` | `'Conformance — BanzamIA'` | `'Conformance — BanzAI'` |
| E-010 | Page body | `'Run the Banzami conformance suite'` | `'Run the Banza conformance suite'` |

### 6.6 `BanzamIA/apps/web/app/rfcs/page.tsx`

| # | Element | Current | Fix |
|---|---------|---------|-----|
| E-011 | Page body | `'Browse and search Banzami Request for Comments'` | `'Browse and search Banza Request for Comments'` |
| E-012 | Prompt chip | `'Ask BanzamIA about RFCs'` | `'Ask BanzAI about RFCs'` |

---

## Group 7 — Roadmaps

**Priority: P1 + P2**

All in `apps/docs/app/roadmap/page.tsx`.

| # | Element | Current | Fix |
|---|---------|---------|-----|
| A-055 | Breadcrumb link | `'BanzamIA'` | `'BanzAI'` |
| A-056 | H1 heading | `'BanzamIA Roadmap'` | `'BanzAI Roadmap'` |
| A-057 | Body description | `'Roadmap público do BanzamIA — Protocol Operating System for the Banzami ecosystem.'` | `'Roadmap público do BanzAI — Protocol Operating System for the Banzami ecosystem.'` |
| A-058 | Roadmap item r22 | `'BanzamIA submits, monitors...'` | `'BanzAI submits, monitors...'` |
| A-059 | Roadmap item r28 | `'BanzamIA identifies gaps...'` | `'BanzAI identifies gaps...'` |
| A-060 | CTA heading | `'Experimente o BanzamIA'` | `'Experimente o BanzAI'` |
| A-061 | CTA button | `'Abrir BanzamIA'` | `'Abrir BanzAI'` |

---

## Group 8 — Landing Pages (Body Copy)

**Priority: P1**

### 8.1 `apps/docs/components/EcosystemMap.tsx`

| # | Element | Current | Fix |
|---|---------|---------|-----|
| A-025 | Description paragraph | `'Uma rede centrada no Core do Banzami'` | `'Uma rede centrada no Core do Banza'` |
| A-026 | SVG center node (desktop) | `BANZAMI` | `BANZA` |
| A-028 | Mobile center block | `BANZAMI CORE` | `BANZA CORE` |

Note: A-026 and A-028 are inline TSX SVG text nodes, not SVG files — treat as UI copy.

### 8.2 `apps/docs/components/HeroSection.tsx` — body paragraphs

| # | Element | Current | Fix |
|---|---------|---------|-----|
| A-020 | §6 Ecossistema | `'infraestrutura do Banzami'` | `'infraestrutura do Banza'` |
| A-021 | §7 QR Commerce | `'o Banza QR serve todos os casos de uso'` | `'o Banzami QR serve todos os casos de uso'` |
| A-022 | §10 Programadores | `'O Banza é SDK-first... Banza SDK oficial'` | `'O Banzami é SDK-first... Banzami SDK oficial'` |

### 8.3 `apps/docs/app/sobre-banzamia/page.tsx` — body copy

| # | Element | Current | Fix |
|---|---------|---------|-----|
| A-048 | Body paragraph | `'O BanzamIA é o Sistema Operativo do Protocolo Banzami'` | `'O BanzAI é o Sistema Operativo do Protocolo Banza'` |
| A-049 | CTA heading | `'Experimentar o BanzamIA'` | `'Experimentar o BanzAI'` |
| A-050 | CTA subtitle | `'Chat ao vivo com o Agente de Protocolo'` | `'Chat ao vivo com o BanzAI'` |
| A-051 | CTA button | `'Abrir BanzamIA →'` | `'Abrir BanzAI →'` |

### 8.4 `apps/docs/app/operators/page.tsx` — body copy

| # | Element | Current | Fix |
|---|---------|---------|-----|
| A-063 | H1 heading | `'Registo de Operadores Banzami'` | `'Registo de Operadores Banza'` |
| A-064 | Body description | `'...protocolo Banzami.'` | `'...protocolo Banza.'` |
| A-065 | FAQ body | `'runner oficial do Banzami...'` | `'runner oficial do Banza...'` |

---

## Execution Checklist

When executing Wave 3, work through this checklist in order:

### P0 — Fix FALSE occurrences first

- [ ] `apps/docs/components/HeroSection.tsx` — hero subheadline (A-018)
- [ ] `apps/docs/components/banzamia/modules/RFCExplorerModule.tsx` — ADR-016 summary (A-076)

### P1 — Systematic rename pass

**`apps/docs/app/layout.tsx`** (global metadata + nav):
- [ ] A-001: `title.default`
- [ ] A-003: `description`
- [ ] A-004: `keywords`
- [ ] A-005: `openGraph.title`
- [ ] A-006: `openGraph.description`
- [ ] A-009: top nav label `BanzamIA` → `BanzAI`
- [ ] A-010: footer nav label `BanzamIA` → `BanzAI`
- [ ] A-011: footer tagline `Banza —` → `Banzami —`

**`apps/docs/app/page.tsx`** (home metadata):
- [ ] A-016: `title`
- [ ] A-017: `description`

**`apps/docs/components/HeroSection.tsx`** (hero + body copy):
- [ ] A-019: capability tag `BanzamIA` → `BanzAI`
- [ ] A-020: §6 `infraestrutura do Banzami` → `infraestrutura do Banza`
- [ ] A-021: §7 `Banza QR` → `Banzami QR`
- [ ] A-022: §10 `O Banza é SDK-first... Banza SDK` → `O Banzami é SDK-first... Banzami SDK`

**`apps/docs/components/EcosystemMap.tsx`**:
- [ ] A-025: description paragraph
- [ ] A-026: SVG center node `BANZAMI` → `BANZA`
- [ ] A-028: mobile center block `BANZAMI CORE` → `BANZA CORE`

**`apps/docs/components/HeroBanzamIAWidget.tsx`**:
- [ ] A-030: chip `BanzamIA` → `BanzAI`
- [ ] A-031: subtitle (Agente de Protocolo → Sistema Operativo de Protocolo)

**`apps/docs/components/banzamia/HomeBanzamIAEntry.tsx`**:
- [ ] A-037: card header `Pergunte ao BanzamIA` → `Pergunte ao BanzAI`
- [ ] A-038: loading state `BanzamIA está a consultar` → `BanzAI está a consultar`

**`apps/docs/components/SectionNav.tsx`**:
- [ ] A-015: nav link label `BanzamIA` → `BanzAI`

**`apps/docs/components/banzamia/BanzamIASidebar.tsx`**:
- [ ] A-039: logo name `BanzamIA` → `BanzAI`
- [ ] A-041: footer link `Sobre o BanzamIA` → `Sobre o BanzAI`

**`apps/docs/components/banzamia/modules/RFCExplorerModule.tsx`**:
- [ ] A-077: `Browse Banzami protocol decisions` → `Browse Banza protocol decisions`

**`apps/docs/app/banzamia/page.tsx`**:
- [ ] A-042: `title`
- [ ] A-043: `description`

**`apps/docs/app/sobre-banzamia/page.tsx`**:
- [ ] A-044–A-047: all metadata fields
- [ ] A-048: body paragraph
- [ ] A-049: CTA heading
- [ ] A-051: CTA button

**`apps/docs/app/roadmap/page.tsx`**:
- [ ] A-053: `title`
- [ ] A-054: `description`
- [ ] A-055: breadcrumb
- [ ] A-056: H1
- [ ] A-057: body description

**`apps/docs/app/operators/page.tsx`**:
- [ ] A-062: `description`
- [ ] A-063: H1
- [ ] A-064: body description
- [ ] A-065: FAQ body

**`apps/dashboard/app/layout.tsx`**:
- [ ] B-001: `title` → `'Banzami Business'`

**`apps/checkout/app/layout.tsx`**:
- [ ] C-001: `title` → `'Banzami Checkout'`
- [ ] C-002: `description` → `'Pagamento seguro via Banzami'`

**`apps/pay/app/layout.tsx`**:
- [ ] D-001: `title` → `'Banzami Pay'`
- [ ] D-002: `description` → `'Pague com a app Banzami'`

**`BanzamIA/apps/web/app/layout.tsx`**:
- [ ] E-001: `title.default`
- [ ] E-002: `title.template`
- [ ] E-003: `description`
- [ ] E-004: `keywords`

**`BanzamIA/apps/web/components/sidebar/Sidebar.tsx`**:
- [ ] E-005: logo name `BanzamIA` → `BanzAI`

**`BanzamIA/apps/web/components/chat/ChatInterface.tsx`**:
- [ ] E-007: welcome message

**`BanzamIA/apps/web/app/conformance/page.tsx`**:
- [ ] E-009: `title`
- [ ] E-010: page body

**`BanzamIA/apps/web/app/rfcs/page.tsx`**:
- [ ] E-011: page body
- [ ] E-012: prompt chip

### P2 — Surgical fixes

**`apps/docs/app/roadmap/page.tsx`**:
- [ ] A-058: roadmap item r22
- [ ] A-059: roadmap item r28

**`apps/docs/app/sobre-banzamia/page.tsx`**:
- [ ] A-050: CTA subtitle (Agente de Protocolo → BanzAI)

**`BanzamIA/apps/web/components/chat/ChatInput.tsx`**:
- [ ] E-008: quick action chip

---

## Protected — Do Not Touch in Wave 3

| String | Reason |
|--------|--------|
| `banzami.org` | DOMAIN — permanent |
| `@banza` | IDENTITY_NAMESPACE — permanent |
| `Organização Banzami` | ORG — permanent |
| `Banzami Lda` | ORG — permanent |
| `site.webmanifest` name/short_name | CORRECT as `"Banzami"` (product) |
| `%s · Banzami` title template | CORRECT (product) |
| `metadata.openGraph.siteName: 'Banzami'` | CORRECT (product) |
| `/banzamia` route paths | Wave 5b |
| `/sobre-banzamia` route paths | Wave 5b |
| `BANZAMI:` / `BANZAMI-SBX:` wire format | Wave 5c |
| Any `<code>` / inline code | Wave 7 |

---

## Post-Wave 3 Validation

After all fixes are applied:

```bash
# No BanzamIA in visible UI copy (allow code blocks, comments)
rg 'BanzamIA' apps/docs/components apps/docs/app apps/dashboard/app apps/checkout/app apps/pay/app BanzamIA/apps/web --glob '*.tsx' --glob '*.ts'

# No "protocolo Banzami" in body copy (Banzami is the product, Banza is the protocol)
rg 'protocolo Banzami' apps/ BanzamIA/

# Confirm Banzami.org domain untouched
rg 'banzami\.org' apps/ BanzamIA/ | wc -l

# Confirm Organização Banzami untouched
rg 'Organização Banzami' apps/ BanzamIA/

# Confirm wire format untouched
rg 'BANZAMI:' apps/ BanzamIA/
rg 'BANZAMI-SBX:' apps/ BanzamIA/
```

---

## Suggested Commit

```
feat(naming): wave 3 website copy naming inversion
```

Applied to the Banzami kernel repo after all three repos' UI changes are staged.

---

## Remaining Waves After Wave 3

| Wave | Scope | Status |
|------|-------|--------|
| 1 | Documentation prose | ✓ COMPLETE |
| 2 | SVG diagram text labels | ✓ COMPLETE |
| 3 | Website copy (this wave) | **Pending** |
| 4 | BanzAI UI components, routes, lib rename | Pending |
| 5a | Env vars (`BANZAMIA_*` → `BANZAI_*`), Docker | Pending |
| 5b | BanzAI API routes (`/banzamia` → `/banzai`) | Pending |
| 5c | Wire format (QR prefixes, operator manifest path) | Pending |
| 6 | SDK documentation, Python SDK rename | Pending |
| 7 | Rust crates (`banzami-*` → `banza-*`), code symbols | Pending |
| 8 | GitHub repository renames (ADR-026 needed) | Pending |
| 9 | Final cleanup (directory/filename renames) | Pending |
