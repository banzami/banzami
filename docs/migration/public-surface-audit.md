# Public Surface Audit — Pre-Wave 3

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Executed by:** BANZA-NAMING-INVERSION-STEP-005  
**Status:** Audit complete — no changes made

---

## Canonical Reference (post-inversion)

| Name | Role |
|------|------|
| **Banza** | Open financial protocol / infrastructure kernel |
| **Banzami** | Product — the reference operator and payment product built on Banza |
| **BanzAI** | Protocol Operating System |
| `banzami.org` | Domain — permanent exception |
| `@banza` | Identity namespace — permanent exception |
| `Banzami Lda` | Legal entity — permanent exception |
| `Organização Banzami` | Org name — permanent exception |

---

## Classification Key

| Code | Meaning |
|------|---------|
| **CORRECT** | Matches new canonical naming exactly |
| **PARTIALLY CORRECT** | Mix of correct and outdated; partially accurate |
| **OUTDATED** | Was correct under old naming; now wrong |
| **MISLEADING** | Creates false understanding of the new model |
| **FALSE** | Factually incorrect under the new model |

---

## Surface 1 — banzami.org Docs Site (`apps/docs`)

### 1.1 Global Metadata (`apps/docs/app/layout.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-001 | `metadata.title.default` | `'Banza — Pagamentos Instantâneos em Kwanza \| Banzami'` | `'Banzami — Pagamentos Instantâneos em Kwanza'` | OUTDATED | P1 |
| A-002 | `metadata.title.template` | `'%s · Banzami'` | `'%s · Banzami'` | CORRECT | — |
| A-003 | `metadata.description` | `'Banzami constrói a infraestrutura... Banza SDK para programadores e Banza Business para comerciantes.'` | Banzami (org) correct; `Banza SDK` → `Banzami SDK`; `Banza Business` → `Banzami Business` | PARTIALLY CORRECT | P1 |
| A-004 | `metadata.keywords` | `['Banza', 'Banzami', ..., 'Banza Business', 'Banza SDK', ...]` | `'Banzami Business'`, `'Banzami SDK'` — keep `'Banza'` as protocol keyword | PARTIALLY CORRECT | P2 |
| A-005 | `metadata.openGraph.title` | `'Banza — Pagamentos Instantâneos em Kwanza \| Banzami'` | `'Banzami — Pagamentos Instantâneos em Kwanza'` | OUTDATED | P1 |
| A-006 | `metadata.openGraph.description` | `'...Banza SDK e Banza Business.'` | `Banzami SDK` and `Banzami Business` | OUTDATED | P1 |
| A-007 | `metadata.openGraph.siteName` | `'Banzami'` | `'Banzami'` | CORRECT | — |
| A-008 | `metadata.authors` | `[{ name: 'Organização Banzami' }]` | unchanged (ORG protected) | CORRECT | — |

### 1.2 Navigation (`apps/docs/app/layout.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-009 | Top nav label | `label: 'BanzamIA'` | `'BanzAI'` | OUTDATED | P1 |
| A-010 | Footer nav label | `BanzamIA` (link label) | `BanzAI` | OUTDATED | P1 |
| A-011 | Footer tagline | `Banza — Rede Angolana de Pagamentos Instantâneos por QR Code` | `Banzami — Rede Angolana de Pagamentos Instantâneos por QR Code` | OUTDATED | P1 |
| A-012 | Logo alt text | `alt="Banzami"` | `alt="Banzami"` | CORRECT | — |
| A-013 | Logo wordmark | `Banzami` | `Banzami` | CORRECT | — |

### 1.3 Sidebar (`apps/docs/components/SectionNav.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-014 | Sidebar brand label | `Banzami` (uppercase pill) | `Banzami` | CORRECT | — |
| A-015 | Sidebar nav link | `navLink('/sobre-banzamia', 'BanzamIA')` | `'BanzAI'` | OUTDATED | P1 |

### 1.4 Home Page (`apps/docs/app/page.tsx` + `apps/docs/components/HeroSection.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-016 | `metadata.title` | `'Banza — Pagamentos Instantâneos em Kwanza \| Banzami'` | `'Banzami — Pagamentos Instantâneos em Kwanza'` | OUTDATED | P1 |
| A-017 | `metadata.description` | `'Banza é a rede angolana de pagamentos... Banza SDKs oficiais.'` | `'Banzami é a rede angolana... Banzami SDKs oficiais.'` | OUTDATED | P1 |
| A-018 | Hero subheadline | `'Banzami é um protocolo aberto para operadores, pagamentos, liquidação...'` | `'Banzami é o produto de pagamentos da Angola construído sobre o Banza, protocolo aberto de infraestrutura financeira.'` | **FALSE** | **P0** |
| A-019 | Hero capability tag | `'BanzamIA'` (in CAPABILITY_TAGS) | `'BanzAI'` | OUTDATED | P1 |
| A-020 | §6 Ecossistema body | `'todos ligados através de uma infraestrutura do Banzami'` | `'...infraestrutura do Banza'` | OUTDATED | P1 |
| A-021 | §7 QR Commerce | `'o Banza QR serve todos os casos de uso'` | `'o Banzami QR serve todos os casos de uso'` | OUTDATED | P1 |
| A-022 | §10 Programadores | `'O Banza é SDK-first... Banza SDK oficial'` | `'O Banzami é SDK-first... Banzami SDK oficial'` | OUTDATED | P1 |
| A-023 | §10 Programadores link | `'O Motor de Crescimento do Banza'` | `'O Motor de Crescimento do Banza'` | CORRECT (protocol) | — |

### 1.5 EcosystemMap Component (`apps/docs/components/EcosystemMap.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-024 | Badge text | `'Ecossistema Banza'` | `'Ecossistema Banza'` | CORRECT (protocol ecosystem) | — |
| A-025 | Description | `'Uma rede centrada no Core do Banzami'` | `'Uma rede centrada no Core do Banza'` | OUTDATED | P1 |
| A-026 | SVG center node (desktop) | `BANZAMI` (inline TSX SVG text) | `BANZA` | MISLEADING | P1 |
| A-027 | Center node (desktop) sublabel | `API · Ledger · Core Rust` | `API · Ledger · Core Rust` | CORRECT | — |
| A-028 | Mobile center block | `BANZAMI CORE` | `BANZA CORE` | MISLEADING | P1 |
| A-029 | Mobile center sublabel | `API · Ledger · Rust` | `API · Ledger · Rust` | CORRECT | — |

### 1.6 HeroBanzamIAWidget (`apps/docs/components/HeroBanzamIAWidget.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-030 | Header chip label | `BanzamIA` | `BanzAI` | OUTDATED | P1 |
| A-031 | Card subtitle | `'O Agente de Protocolo nativo de IA do ecossistema Banzami.'` | `'O Sistema Operativo de Protocolo do ecossistema Banzami.'` | PARTIALLY CORRECT | P1 |
| A-032 | Input placeholder | `'Como posso integrar o Banzami no meu produto?'` | unchanged (Banzami = product; integrating the product = correct) | CORRECT | — |
| A-033 | Quick prompt | `'Como integrar o Banzami?'` | unchanged (product integration) | CORRECT | — |

### 1.7 HomeBanzamIAEntry (`apps/docs/components/banzamia/HomeBanzamIAEntry.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-034 | Quick prompt | `'O que é o Banzami?'` | unchanged (product question) | CORRECT | — |
| A-035 | Quick prompt | `'Qual é a diferença entre Banzami e Banza?'` | unchanged (canonical distinction) | CORRECT | — |
| A-036 | Card subtitle | `'A interface inteligente oficial para entender... ecossistema Banzami.'` | unchanged (Banzami = product ecosystem) | CORRECT | — |
| A-037 | Card header | `'Pergunte ao BanzamIA'` | `'Pergunte ao BanzAI'` | OUTDATED | P1 |
| A-038 | Loading state | `'BanzamIA está a consultar o protocolo…'` | `'BanzAI está a consultar o protocolo…'` | OUTDATED | P1 |

### 1.8 BanzamIASidebar (docs side, `apps/docs/components/banzamia/BanzamIASidebar.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-039 | Sidebar logo name | `BanzamIA` | `BanzAI` | OUTDATED | P1 |
| A-040 | Sidebar logo subtitle | `Protocol Operating System` | `Protocol Operating System` | CORRECT | — |
| A-041 | Sidebar footer link | `'Sobre o BanzamIA'` | `'Sobre o BanzAI'` | OUTDATED | P1 |

### 1.9 BanzAI Module Page (`apps/docs/app/banzamia/page.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-042 | `metadata.title` | `'BanzamIA — Protocol Operating System'` | `'BanzAI — Protocol Operating System'` | OUTDATED | P1 |
| A-043 | `metadata.description` | `'BanzamIA é o Sistema Operativo do Protocolo Banzami...'` | `'BanzAI é o Sistema Operativo do Protocolo Banza...'` | OUTDATED | P1 |

### 1.10 Sobre BanzAI Page (`apps/docs/app/sobre-banzamia/page.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-044 | `metadata.title` | `'Sobre o BanzamIA'` | `'Sobre o BanzAI'` | OUTDATED | P1 |
| A-045 | `metadata.description` | `'BanzamIA — o Sistema Operativo do Protocolo Banzami.'` | `'BanzAI — o Sistema Operativo do Protocolo Banza.'` | OUTDATED | P1 |
| A-046 | `metadata.openGraph.title` | `'Sobre o BanzamIA · Banzami'` | `'Sobre o BanzAI · Banzami'` | OUTDATED | P1 |
| A-047 | `metadata.openGraph.description` | `'O Sistema Operativo do Protocolo Banzami.'` | `'O Sistema Operativo do Protocolo Banza.'` | OUTDATED | P1 |
| A-048 | Body paragraph | `'O BanzamIA é o Sistema Operativo do Protocolo Banzami'` | `'O BanzAI é o Sistema Operativo do Protocolo Banza'` | OUTDATED | P1 |
| A-049 | CTA heading | `'Experimentar o BanzamIA'` | `'Experimentar o BanzAI'` | OUTDATED | P1 |
| A-050 | CTA subtitle | `'Chat ao vivo com o Agente de Protocolo'` | `'Chat ao vivo com o BanzAI'` | PARTIALLY CORRECT | P2 |
| A-051 | CTA button | `'Abrir BanzamIA →'` | `'Abrir BanzAI →'` | OUTDATED | P1 |
| A-052 | Breadcrumb source ref | `docs/BANZAMI_REFERENCE.md §9` | unchanged (code path — Wave 9) | CORRECT | — |

### 1.11 Roadmap Page (`apps/docs/app/roadmap/page.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-053 | `metadata.title` | `'Roadmap — BanzamIA Protocol Operating System'` | `'Roadmap — BanzAI Protocol Operating System'` | OUTDATED | P1 |
| A-054 | `metadata.description` | `'Roadmap público do BanzamIA — Protocol Operating System do ecossistema Banzami.'` | `'Roadmap público do BanzAI — Protocol Operating System do ecossistema Banzami.'` | OUTDATED | P1 |
| A-055 | Breadcrumb | `'BanzamIA'` link text | `'BanzAI'` | OUTDATED | P1 |
| A-056 | H1 heading | `'BanzamIA Roadmap'` | `'BanzAI Roadmap'` | OUTDATED | P1 |
| A-057 | Body description | `'Roadmap público do BanzamIA — Protocol Operating System for the Banzami ecosystem.'` | `'...BanzAI...Banzami ecosystem.'` | OUTDATED | P1 |
| A-058 | Roadmap item r22 | `'BanzamIA submits, monitors...'` | `'BanzAI submits, monitors...'` | OUTDATED | P2 |
| A-059 | Roadmap item r28 | `'BanzamIA identifies gaps...'` | `'BanzAI identifies gaps...'` | OUTDATED | P2 |
| A-060 | CTA heading | `'Experimente o BanzamIA'` | `'Experimente o BanzAI'` | OUTDATED | P1 |
| A-061 | CTA button | `'Abrir BanzamIA'` | `'Abrir BanzAI'` | OUTDATED | P1 |

### 1.12 Operators Page (`apps/docs/app/operators/page.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-062 | `metadata.description` | `'Registo público de operadores Banzami'` | `'Registo público de operadores Banza'` | OUTDATED | P1 |
| A-063 | H1 heading | `'Registo de Operadores Banzami'` | `'Registo de Operadores Banza'` | OUTDATED | P1 |
| A-064 | Body description | `'Registo curado de operadores que implementam o protocolo Banzami.'` | `'...protocolo Banza.'` | OUTDATED | P1 |
| A-065 | FAQ body | `'runner oficial do Banzami. Nenhum operador pode auto-declarar...'` | `'runner oficial do Banza.'` | OUTDATED | P1 |

### 1.13 Reference Page (`apps/docs/app/reference/page.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-066 | `metadata.title` | `'Banzami — Referência Oficial'` | `'Banzami — Referência Oficial'` | CORRECT | — |
| A-067 | `metadata.description` | `'Referência oficial do ecossistema Banzami... visão da rede Banza para Angola.'` | unchanged | CORRECT | — |
| A-068 | H1 heading | `'Banzami — Referência Oficial'` | `'Banzami — Referência Oficial'` | CORRECT | — |
| A-069 | Attribution | `'Organização Banzami · v...'` | unchanged (ORG protected) | CORRECT | — |

### 1.14 Validação Page (`apps/docs/app/validacao/page.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-070 | `metadata.description` | `'Sistema de execução e validação do ecossistema Banzami'` | `'...ecossistema Banzami'` | CORRECT (product ecosystem) | — |
| A-071 | Body heading | `'Execução e Validação do Ecossistema Banzami'` | unchanged | CORRECT | — |
| A-072 | Body footnote | `'administração Banzami'` | unchanged (org reference) | CORRECT | — |
| A-073 | Attribution | `'Organização Banzami'` | unchanged (ORG protected) | CORRECT | — |

### 1.15 Section Pages (`apps/docs/app/[section]/page.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-074 | `metadata.description` | `'Banzami — §N: [title]'` | `'Banzami — §N: [title]'` | CORRECT (Banzami product) | — |
| A-075 | `metadata.openGraph.description` | `'Referência oficial Banzami — secção...'` | unchanged | CORRECT | — |

### 1.16 BanzAI Modules — RFCExplorerModule (`apps/docs/components/banzamia/modules/RFCExplorerModule.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-076 | ADR-016 summary | `'Banzami = org/infra. Banza = product. BanzamIA = AI layer.'` | `'Banza = protocol/infra. Banzami = product. BanzAI = Protocol OS.'` | **FALSE** | **P0** |
| A-077 | Module body | `'Browse Banzami protocol decisions'` | `'Browse Banza protocol decisions'` (BanzamIA repo) | OUTDATED | P2 |

### 1.17 Site Webmanifest (`apps/docs/public/site.webmanifest`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| A-078 | `name` | `"Banzami"` | `"Banzami"` | CORRECT (product name) | — |
| A-079 | `short_name` | `"Banzami"` | `"Banzami"` | CORRECT | — |

---

## Surface 2 — Dashboard App (`apps/dashboard`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| B-001 | `metadata.title` | `'Banza Business'` | `'Banzami Business'` | OUTDATED | P1 |
| B-002 | `metadata.description` | `'Business dashboard — Banzami'` | unchanged (Banzami = product/org) | CORRECT | — |
| B-003 | Sidebar logo wordmark | `Banzami` | `Banzami` | CORRECT | — |
| B-004 | Sidebar brand label | `Banzami Business` (wordmark + badge) | `Banzami Business` | CORRECT | — |

---

## Surface 3 — Checkout App (`apps/checkout`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| C-001 | `metadata.title` | `'Banza Checkout'` | `'Banzami Checkout'` | OUTDATED | P1 |
| C-002 | `metadata.description` | `'Pagamento seguro via Banza'` | `'Pagamento seguro via Banzami'` | OUTDATED | P1 |

---

## Surface 4 — Pay App (`apps/pay`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| D-001 | `metadata.title` | `'Banza Pay'` | `'Banzami Pay'` | OUTDATED | P1 |
| D-002 | `metadata.description` | `'Pague com a app Banza'` | `'Pague com a app Banzami'` | OUTDATED | P1 |
| D-003 | Profile page title | `'${display_name} (@${handle}) — Banzami'` | unchanged (Banzami = product) | CORRECT | — |
| D-004 | Profile not found title | `'Perfil não encontrado — Banzami'` | unchanged | CORRECT | — |

---

## Surface 5 — BanzAI Web App (`/Users/fm65/BanzamIA/apps/web`)

### 5.1 Layout (`apps/web/app/layout.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| E-001 | `metadata.title.default` | `'BanzamIA — Financial Infrastructure Intelligence'` | `'BanzAI — Financial Infrastructure Intelligence'` | OUTDATED | P1 |
| E-002 | `metadata.title.template` | `'%s · BanzamIA'` | `'%s · BanzAI'` | OUTDATED | P1 |
| E-003 | `metadata.description` | `'BanzamIA is the intelligence layer of the Banzami programmable financial infrastructure ecosystem.'` | `'BanzAI is the intelligence layer of the Banza programmable financial infrastructure ecosystem.'` | OUTDATED | P1 |
| E-004 | `metadata.keywords` | `['Banzami', 'BanzamIA', ...]` | `['Banzami', 'BanzAI', 'Banza', ...]` | OUTDATED | P2 |

### 5.2 Sidebar (`apps/web/components/sidebar/Sidebar.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| E-005 | Logo name | `'BanzamIA'` | `'BanzAI'` | OUTDATED | P1 |
| E-006 | Logo subtitle | `'Protocol Operating System'` | `'Protocol Operating System'` | CORRECT | — |

### 5.3 Chat Interface (`apps/web/components/chat/ChatInterface.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| E-007 | Welcome message | `"I'm BanzamIA — the intelligence layer of the Banzami programmable financial infrastructure ecosystem."` | `"I'm BanzAI — the intelligence layer of the Banza programmable financial infrastructure ecosystem."` | OUTDATED | P1 |

### 5.4 Chat Input (`apps/web/components/chat/ChatInput.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| E-008 | Quick action | `'Explain the Banzami financial trace model'` | `'Explain the Banza financial trace model'` | OUTDATED | P2 |

### 5.5 Conformance Page (`apps/web/app/conformance/page.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| E-009 | `metadata.title` | `'Conformance — BanzamIA'` | `'Conformance — BanzAI'` | OUTDATED | P1 |
| E-010 | Page body | `'Run the Banzami conformance suite'` | `'Run the Banza conformance suite'` | OUTDATED | P1 |

### 5.6 RFC Explorer (`apps/web/app/rfcs/page.tsx`)

| # | Location | Current text | Expected text | Classification | Priority |
|---|----------|-------------|---------------|----------------|----------|
| E-011 | Page body | `'Browse and search Banzami Request for Comments'` | `'Browse and search Banza Request for Comments'` | OUTDATED | P1 |
| E-012 | Prompt chip | `'Ask BanzamIA about RFCs'` | `'Ask BanzAI about RFCs'` | OUTDATED | P1 |

---

## Occurrence Count Summary

| Classification | Count | Action Required |
|----------------|-------|-----------------|
| **FALSE** | 2 | Immediate fix — creates wrong mental model |
| **MISLEADING** | 3 | High priority — confuses Banza/Banzami roles |
| **OUTDATED** | 52 | Wave 3 — systematic rename |
| **PARTIALLY CORRECT** | 6 | Wave 3 — surgical fix |
| **CORRECT** | 31 | No action |
| **Total audited** | 94 | — |

---

## FALSE Occurrences — Highest Priority

### F-001: Hero subheadline says Banzami is the protocol

**File:** `apps/docs/components/HeroSection.tsx:57`  
**Current:** `"Banzami é um protocolo aberto para operadores, pagamentos, liquidação, certificação e rastreabilidade financeira."`  
**Issue:** Under the new model, **Banzami is the product** — not the protocol. Banza is the open protocol.  
**Fix:** `"Banzami é o produto de pagamentos de Angola, construído sobre o Banza — protocolo aberto de infraestrutura financeira."`  

### F-002: RFCExplorerModule ADR-016 summary describes old model

**File:** `apps/docs/components/banzamia/modules/RFCExplorerModule.tsx:20`  
**Current:** `"Banzami = org/infra. Banza = product. BanzamIA = AI layer."`  
**Issue:** This is the pre-inversion model. Post-ADR-025 it is inverted.  
**Fix:** `"Banza = open financial protocol. Banzami = product operator. BanzAI = Protocol OS. (ADR-025 inverted ADR-016 naming.)"`  

---

## Protected Occurrences — Verified Intact

| String | Occurrences found | Status |
|--------|-------------------|--------|
| `banzami.org` | Multiple (layout footers, metadata) | ✓ Protected |
| `@banza` | Multiple (hero, ecosystem map) | ✓ Protected |
| `Banzami Lda` | Not in UI (docs only) | ✓ Protected |
| `Organização Banzami` | reference/page, validacao/page | ✓ Protected |
| `site.webmanifest` name/short_name | `"Banzami"` | ✓ CORRECT (product) |

---

## Routes Identified for Wave 5b

The following routes use old naming and will need renaming in Wave 5b (not touched in Wave 3):

| Route | Used by | Wave |
|-------|---------|------|
| `/banzamia` | Nav link href, sidebar links, page routes | 5b |
| `/sobre-banzamia` | Sidebar footer link, breadcrumbs | 5b |
