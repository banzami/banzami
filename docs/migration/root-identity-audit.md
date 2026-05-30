---
title: Root Identity Audit — BANZA-NAMING-INVERSION-STEP-009A
version: 1.0
date: 2026-05-29
scope: All user-facing identity surfaces on banzami.org (Banza docs site)
status: AUDIT COMPLETE — no code changes applied
---

# Root Identity Audit

Audit of every user-facing identity surface on `banzami.org` (the `apps/docs` Next.js app in the Banza repo) following ADR-025 (naming inversion) and STEP-008 consolidation.

**Classification legend:**

| Code | Meaning |
|------|---------|
| CORRECT | Matches ADR-025 canonical model |
| CONTEXTUAL | Correct given that banzami.org is now the BANZA institutional site |
| OUTDATED | Still shows pre-inversion name; needs update |
| MISLEADING | Technically not wrong but creates incorrect mental model |
| FALSE | Directly contradicts ADR-025 |

---

## 1. Global Layout — `apps/docs/app/layout.tsx`

### 1.1 SEO Metadata

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| `title.default` | `'Banzami — Pagamentos Instantâneos em Kwanza'` | layout.tsx:17 | MISLEADING |
| `title.template` | `'%s · Banzami'` | layout.tsx:18 | MISLEADING |
| `description` | `'Banzami constrói a infraestrutura que permitirá Angola pagar digitalmente...'` | layout.tsx:20–21 | FALSE |
| `openGraph.title` | `'Banzami — Pagamentos Instantâneos em Kwanza'` | layout.tsx:37 | MISLEADING |
| `openGraph.description` | `'Banzami constrói a infraestrutura que permitirá Angola pagar digitalmente...'` | layout.tsx:38–40 | FALSE |
| `openGraph.siteName` | `'Banzami'` | layout.tsx:39 | OUTDATED |
| `authors` | `[{ name: 'Organização Banzami' }]` | layout.tsx:55 | CORRECT |

**Notes:**
- The description "Banzami constrói a infraestrutura" directly contradicts ADR-025: BANZA (the protocol) builds the infrastructure; Banzami is the reference operator. This is the most critical SEO/metadata issue.
- "Organização Banzami" is the legal entity name — protected identifier, keep as-is.
- The Banzami product tagline "Pagamentos Instantâneos em Kwanza" is Banzami-product language on what is now a BANZA protocol institutional site.

### 1.2 Top Navigation Bar

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| Logo image alt | `'Banzami'` | layout.tsx:72 | CORRECT (domain exception) |
| Logo wordmark | `'Banzami'` | layout.tsx:74 | CORRECT (domain exception) |
| Nav link: BanzAI label | `'BanzAI'` | layout.tsx:87 | CORRECT |
| Nav link: BanzAI route | `href="/banzamia"` | layout.tsx:87 | OUTDATED (Wave 5b) |
| All other nav link labels | Referência, Programadores, Comerciantes, Arquitectura, Segurança, Operadores, Validação | layout.tsx:80–86 | CORRECT |

**Notes:**
- Logo "Banzami" is accepted under the domain exception: the domain is banzami.org and the logo represents the site operator.
- Route `/banzamia` is a Wave 5b item (breaking change requiring backend coordination).

### 1.3 Left Sidebar — `SectionNav.tsx`

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| Sidebar logo label | `'Banzami'` (uppercase, tracking-widest) | SectionNav.tsx:65 | MISLEADING |
| Sidebar sublabel | `'Documentação oficial'` | SectionNav.tsx:67 | MISLEADING |
| Sidebar nav item: BanzAI display | `'BanzAI'` | SectionNav.tsx:71 | CORRECT |
| Sidebar nav item: BanzAI route | `'/sobre-banzamia'` | SectionNav.tsx:71 | OUTDATED (Wave 5b) |

**Notes:**
- "Banzami — Documentação oficial" implies this is the Banzami product documentation, not the BANZA protocol documentation. Under ADR-025, banzami.org is now the BANZA institutional site. The label should read "Banza" or "Banza Protocol".
- This label is the first text a visitor reads in the sidebar — its positioning as a primary identifier is high-impact.

### 1.4 Footer

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| Footer logo image alt | `'Banzami'` | layout.tsx:140 | CORRECT (domain exception) |
| Footer logo wordmark | `'Banzami'` | layout.tsx:142 | CORRECT (domain exception) |
| Footer tagline | `'Banzami — Rede Angolana de Pagamentos Instantâneos por QR Code'` | layout.tsx:145 | MISLEADING |
| Footer link: BanzAI | `'BanzAI'` | layout.tsx:157 | CORRECT |
| Footer link: BanzAI route | `href="/banzamia"` | layout.tsx:157 | OUTDATED (Wave 5b) |

**Notes:**
- "Rede Angolana de Pagamentos Instantâneos por QR Code" is the Banzami product tagline. On a BANZA protocol institutional site the footer should describe the protocol, not the product.

---

## 2. Homepage — `apps/docs/app/page.tsx` + components

### 2.1 HeroSection — `components/HeroSection.tsx`

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| Badge | `'Infraestrutura Financeira Programável para Angola'` | HeroSection.tsx:37 | CONTEXTUAL |
| H1 | `'Infraestrutura financeira programável.'` | HeroSection.tsx:41–52 | CONTEXTUAL |
| Subheadline | `'Banzami é o produto de pagamentos de Angola, construído sobre o Banza — protocolo aberto de infraestrutura financeira.'` | HeroSection.tsx:56–58 | CORRECT |
| Capability tags | Operadores certificados, Federação, Liquidação, Rastreabilidade, Conformidade, BanzAI | HeroSection.tsx:8–15 | CORRECT |

**Notes:**
- Badge and H1 are CONTEXTUAL: under ADR-025, banzami.org is the BANZA institutional site, so "Infraestrutura financeira programável" is exactly the right protocol-level language. This was a finding in the previous STEP-007 audit but is now resolved by the site's repositioning.
- The subheadline correctly positions Banzami as the product built on Banza.

### 2.2 HeroBanzamIAWidget — `components/HeroBanzamIAWidget.tsx`

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| Card header title | `'Pergunte ao BanzAI'` | HeroBanzamIAWidget.tsx:44 | CORRECT |
| Card header descriptor | `'O Sistema Operativo de Protocolo do ecossistema Banzami.'` | HeroBanzamIAWidget.tsx:45–46 | CORRECT |
| Card badge | `'BanzAI'` | HeroBanzamIAWidget.tsx:51 | CORRECT |
| Input placeholder | `'Como posso integrar o Banzami no meu produto?'` | HeroBanzamIAWidget.tsx:79 | CORRECT |
| Widget route target | `href="/banzamia"` | HeroBanzamIAWidget.tsx:24 | OUTDATED (Wave 5b) |

### 2.3 HomeBanzamIAEntry — `components/banzamia/HomeBanzamIAEntry.tsx`

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| Widget description | `'A interface inteligente oficial para entender, integrar e validar o ecossistema Banzami.'` | HomeBanzamIAEntry.tsx:84 | MISLEADING |
| Loading text | `'BanzAI está a consultar o protocolo…'` | HomeBanzamIAEntry.tsx:145 | CORRECT |
| CTA link text | `'Abrir BanzamIA completo →'` | HomeBanzamIAEntry.tsx:129 | FALSE |
| Error link text | `'Pode abrir o BanzamIA completo'` | HomeBanzamIAEntry.tsx:165 | FALSE |
| CTA link route | `href="/banzamia"` | HomeBanzamIAEntry.tsx:128 | OUTDATED (Wave 5b) |
| Error link route | `href="/banzamia"` | HomeBanzamIAEntry.tsx:165 | OUTDATED (Wave 5b) |

**Notes:**
- "A interface inteligente oficial" does not use the canonical description "Protocol Operating System". This is MISLEADING — it frames BanzAI as an AI interface, not as the protocol's operating system.
- "Abrir BanzamIA completo" and "Pode abrir o BanzamIA completo" use the pre-inversion name. These are user-visible link labels and classify as FALSE (wrong brand name in production UI).

---

## 3. BanzAI Shell — `apps/docs/app/banzamia/page.tsx`

### 3.1 Page Metadata

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| `metadata.title` | `'BanzAI — Protocol Operating System'` | banzamia/page.tsx:7 | CORRECT |
| `metadata.description` | `'BanzAI é o Sistema Operativo do Protocolo Banza. 16 módulos...'` | banzamia/page.tsx:8–9 | CORRECT |
| Page function name | `BanzamIAPage()` | banzamia/page.tsx:12 | OUTDATED (Wave 4 code identifier) |

### 3.2 BanzamIAApp — `components/banzamia/BanzamIAApp.tsx`

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| Component name | `BanzamIAApp` | BanzamIAApp.tsx:65 | OUTDATED (Wave 4) |
| Module content area comment | `{/* Module content — relative so BanzamIAChat can use absolute inset-0 */}` | BanzamIAApp.tsx:145 | OUTDATED (comment only) |

All user-visible text inside this component is mediated through child components. No direct user-visible identity strings here.

### 3.3 BanzamIASidebar — `components/banzamia/BanzamIASidebar.tsx`

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| Sidebar brand name | `'BanzAI'` | BanzamIASidebar.tsx:198 | CORRECT |
| Sidebar brand descriptor | `'Protocol Operating System'` | BanzamIASidebar.tsx:199 | CORRECT |
| Demo mode badge text | `'Demo mode'` | BanzamIASidebar.tsx:211 | CORRECT |
| Live mode badge text | `'Live — API connected'` | BanzamIASidebar.tsx:210 | CORRECT |
| Footer link label | `'Sobre o BanzAI'` | BanzamIASidebar.tsx:249 | CORRECT |
| Footer link route | `href="/sobre-banzamia"` | BanzamIASidebar.tsx:241 | OUTDATED (Wave 5b) |
| Footer motto | `'Tools determine truth. AI explains truth.'` | BanzamIASidebar.tsx:253–254 | CORRECT |
| Component name | `BanzamIASidebar` | BanzamIASidebar.tsx:189 | OUTDATED (Wave 4) |

**Notes:**
- The sidebar brand display ("BanzAI" + "Protocol Operating System") is fully correct in code as of STEP-008 deployment.
- Screenshots provided for this audit showed "BanzamIA" in the sidebar — this likely reflects a pre-deployment production state. The code is correct; production state should match after the next container rebuild.

### 3.4 BanzamIAChat — `components/banzamia/BanzamIAChat.tsx`

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| Welcome screen H1 | `'BanzamIA'` | BanzamIAChat.tsx:280 | FALSE |
| Welcome screen body (line 1) | `'BanzamIA é o Sistema Operativo do Protocolo Banzami. 16 módulos.'` | BanzamIAChat.tsx:281–282 | FALSE |
| Welcome screen body (line 2) | `'Ferramentas determinam a verdade. A IA explica a verdade.'` | BanzamIAChat.tsx:283–284 | CORRECT |
| Error message | `'Erro ao conectar com BanzamIA. Verifique a configuração do endpoint.'` | BanzamIAChat.tsx:252 | FALSE |
| Input placeholder | `'Pergunta sobre o protocolo Banza, código SDK, invariantes, certificação…'` | BanzamIAChat.tsx:381 | CORRECT |
| Example question prompts | 5 questions about Banza protocol features | BanzamIAChat.tsx:23–29 | CORRECT |
| Component name | `BanzamIAChat` | BanzamIAChat.tsx:182 | OUTDATED (Wave 4) |

**Notes:**
- The welcome screen H1 "BanzamIA" is the most visible user-facing identity surface inside the BanzAI shell. It is the first branded text a user reads when opening the chat module.
- The welcome body "BanzamIA é o Sistema Operativo do Protocolo Banzami" contains two errors: wrong brand name AND "Protocolo Banzami" instead of "Protocolo Banza".
- The error text "Erro ao conectar com BanzamIA" surfaces only on API failure but is still user-visible.
- These three strings in `BanzamIAChat.tsx` are NOT code identifiers — they are display strings. They classify as immediate-remediation items, not Wave 4.

---

## 4. About BanzAI Page — `apps/docs/app/sobre-banzamia/page.tsx`

| Surface | Current value | File:line | Status |
|---------|---------------|-----------|--------|
| `metadata.title` | `'Sobre o BanzAI'` | sobre-banzamia/page.tsx:9 | CORRECT |
| `metadata.description` | `'BanzAI — o Sistema Operativo do Protocolo Banza...'` | sobre-banzamia/page.tsx:10 | CORRECT |
| OG title | `'Sobre o BanzAI · Banzami'` | sobre-banzamia/page.tsx:13 | CORRECT |
| OG description | `'O Sistema Operativo do Protocolo Banza. 16 módulos...'` | sobre-banzamia/page.tsx:14 | CORRECT |
| Page intro text | `'O BanzAI é o Sistema Operativo do Protocolo Banza — 16 módulos...'` | sobre-banzamia/page.tsx:36–38 | CORRECT |
| CTA label | `'Experimentar o BanzAI'` | sobre-banzamia/page.tsx:44 | CORRECT |
| CTA sub-label | `'Chat ao vivo com o BanzAI'` | sobre-banzamia/page.tsx:45 | CORRECT |
| CTA button route | `href="/banzamia"` | sobre-banzamia/page.tsx:48 | OUTDATED (Wave 5b) |
| Footer link label | `'Abrir BanzAI'` | sobre-banzamia/page.tsx:103 | CORRECT |
| Footer link route | `href="/banzamia"` | sobre-banzamia/page.tsx:102 | OUTDATED (Wave 5b) |
| Source reference | `docs/BANZAMI_REFERENCE.md §9` | sobre-banzamia/page.tsx:94 | OUTDATED (filename, Wave 9) |
| Function name | `SobreBanzamiaPage()` | sobre-banzamia/page.tsx:18 | OUTDATED (Wave 4) |

**Notes:** The `/sobre-banzamia` page is the best-maintained identity surface on the site. All user-visible strings correctly use BanzAI and Banza. Only route strings and code identifiers remain outdated.

---

## 5. Summary — Issues by Severity

### Tier 1 — FALSE (wrong brand name visible to users, fix immediately)

| # | Surface | Current | Correct | File:line |
|---|---------|---------|---------|-----------|
| F-01 | Chat welcome H1 | `BanzamIA` | `BanzAI` | BanzamIAChat.tsx:280 |
| F-02 | Chat welcome body | `BanzamIA é o Sistema Operativo do Protocolo Banzami` | `BanzAI é o Sistema Operativo do Protocolo Banza` | BanzamIAChat.tsx:281–282 |
| F-03 | Chat error message | `Erro ao conectar com BanzamIA.` | `Erro ao conectar com BanzAI.` | BanzamIAChat.tsx:252 |
| F-04 | Homepage entry CTA link | `Abrir BanzamIA completo →` | `Abrir BanzAI completo →` | HomeBanzamIAEntry.tsx:129 |
| F-05 | Homepage entry error link | `Pode abrir o BanzamIA completo` | `Pode abrir o BanzAI completo` | HomeBanzamIAEntry.tsx:165 |

### Tier 2 — FALSE/MISLEADING (wrong factual claim in SEO metadata)

| # | Surface | Current | Correct | File:line |
|---|---------|---------|---------|-----------|
| M-01 | SEO description | `Banzami constrói a infraestrutura` | `Banza constrói a infraestrutura` | layout.tsx:20–21 |
| M-02 | OG description | `Banzami constrói a infraestrutura` | `Banza constrói a infraestrutura` | layout.tsx:38–40 |
| M-03 | SEO title.default | `Banzami — Pagamentos Instantâneos em Kwanza` | `Banza — Protocolo de Infraestrutura Financeira` | layout.tsx:17 |
| M-04 | OG title | `Banzami — Pagamentos Instantâneos em Kwanza` | `Banza — Protocolo de Infraestrutura Financeira` | layout.tsx:37 |
| M-05 | Title template | `%s · Banzami` | `%s · Banza` | layout.tsx:18 |
| M-06 | Footer tagline | `Banzami — Rede Angolana de Pagamentos Instantâneos por QR Code` | `Banza — Protocolo Aberto de Infraestrutura Financeira` | layout.tsx:145 |
| M-07 | Sidebar logo label | `Banzami` | `Banza` | SectionNav.tsx:65 |
| M-08 | BanzAI entry descriptor | `A interface inteligente oficial` | `O Sistema Operativo do Protocolo Banza` | HomeBanzamIAEntry.tsx:84 |

### Tier 3 — OUTDATED (code identifiers + routes, deferred waves)

| # | Surface | Wave | File(s) |
|---|---------|------|---------|
| O-01 | Route `/banzamia` | Wave 5b | layout.tsx:87, layout.tsx:157, HeroBanzamIAWidget.tsx:24, HomeBanzamIAEntry.tsx:128+165, BanzamIASidebar.tsx:241, sobre-banzamia/page.tsx:48+102 |
| O-02 | Route `/sobre-banzamia` | Wave 5b | SectionNav.tsx:71, BanzamIASidebar.tsx:241 |
| O-03 | Component `BanzamIAApp` | Wave 4 | BanzamIAApp.tsx:65 |
| O-04 | Component `BanzamIAChat` | Wave 4 | BanzamIAChat.tsx:182 |
| O-05 | Component `BanzamIASidebar` | Wave 4 | BanzamIASidebar.tsx:189 |
| O-06 | Function `BanzamIAPage` | Wave 4 | banzamia/page.tsx:12 |
| O-07 | Function `SobreBanzamiaPage` | Wave 4 | sobre-banzamia/page.tsx:18 |
| O-08 | Env var reference `NEXT_PUBLIC_BANZAMIA_API_URL` (sidebar demo note) | Wave 5a | BanzamIASidebar.tsx (demo mode text) |
| O-09 | Source reference `BANZAMI_REFERENCE.md` | Wave 9 | sobre-banzamia/page.tsx:94 |

### Tier 4 — CORRECT

All correctly identified surfaces per ADR-025:

- `BanzamIASidebar.tsx:198–199` — "BanzAI" + "Protocol Operating System"
- `banzamia/page.tsx:7–9` — page metadata fully correct
- `sobre-banzamia/page.tsx` — all user-visible strings correct
- `layout.tsx:87` — nav "BanzAI" label
- `layout.tsx:157` — footer "BanzAI" link
- `HeroBanzamIAWidget.tsx:44,51` — "Pergunte ao BanzAI", "BanzAI" badge
- `HeroSection.tsx:41–58` — H1 + subheadline (CONTEXTUAL: correct for BANZA institutional site)
- `BanzamIAChat.tsx:381` — placeholder uses "protocolo Banza"
- `HomeBanzamIAEntry.tsx:145` — "BanzAI está a consultar o protocolo…"
- `layout.tsx:55` — "Organização Banzami" (legal entity, protected)

---

## 6. Screenshot Evidence

Two screenshots were provided showing production state at time of audit initiation (pre-STEP-008 container rebuild):

**Screenshot 1 — banzami.org homepage**
- Logo: "Banzami" (domain exception — acceptable)
- Left sidebar: "BANZAMI" uppercase label + "Documentação oficial" (maps to M-07)
- Badge: "Infraestrutura Financeira Programável para Angola" (CONTEXTUAL — correct for BANZA site)
- H1: "Infraestrutura financeira programável." (CONTEXTUAL)
- Subheadline: "Banzami é o produto de pagamentos de Angola, construído sobre o Banza" (CORRECT)
- BanzAI widget: "Pergunte ao BanzAI" + "O Sistema Operativo de Protocolo do ecossistema Banzami." (CORRECT)

**Screenshot 2 — banzami.org/banzamia (BanzAI shell)**
- Sidebar brand: "BanzamIA" + "Protocol Operating System" — sidebar code already fixed (BanzamIASidebar.tsx:198 = "BanzAI"); screenshot reflects pre-deployment state
- Chat welcome H1: "BanzamIA" (maps to F-01)
- Chat welcome body: "BanzamIA é o Sistema Operativo do Protocolo Banzami. 16 módulos." (maps to F-02)
- Demo mode badge: "DEMO MODE" (correct)
- Placeholder: "Pergunta sobre o protocolo Banza…" (CORRECT — fixed in STEP-008)
- Nav: "★ BanzAI" gold (CORRECT)
- Footer motto: "Tools determine truth. AI explains truth." (CORRECT)

---

*Audit performed: 2026-05-29. No code changes applied. See root-identity-remediation-plan.md for fix sequence.*
