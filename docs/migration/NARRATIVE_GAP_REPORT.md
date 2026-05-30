---
title: NARRATIVE_GAP_REPORT
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no files modified
---

# Narrative Gap Report

For every gap: Current message → Missing message → Required correction → Priority.

Gaps are ordered by priority: P0 (functional bugs blocking correct rendering) → P1 (critical narrative) → P2 (important narrative) → P3 (improvement).

---

## P0 — Functional Bugs (Fix Immediately, Block Everything Else)

These are rendering bugs introduced by the §§1–3 integration. They cause wrong content to appear on the page. They must be fixed before any narrative work on the affected surfaces is meaningful.

---

### GAP-001 — About BanzAI renders wrong section (§9 instead of §11)

**Surface:** `/sobre-banzamia` → `app/sobre-banzamia/page.tsx`

**Current:** `getSectionByNumber(9)` — renders §9 (Modelo de Certificação). A visitor to "Sobre o BanzAI" reads about the certification model, not BanzAI.

**Missing:** `getSectionByNumber(11)` — §11 is "BanzAI" after the §§1–3 integration.

**Required correction:**
```tsx
// Change line 20: getSectionByNumber(9) → getSectionByNumber(11)
// Change line 24: sections.findIndex((s) => s.number === 9) → s.number === 11
// Change source attribution string: "§9" → "§11"
```

**Priority:** P0 — The page is currently showing the wrong content.

---

### GAP-002 — Homepage "Why Now" links to wrong section (§15 instead of §17)

**Surface:** `/` → `app/page.tsx`

**Current:** `getSectionByNumber(15)` — §15 is "Segurança e Integridade Financeira". The "Porquê agora?" card links to the security section.

**Missing:** `getSectionByNumber(17)` — §17 is "Por que Angola. Por que Agora."

**Required correction:**
```tsx
// Change line 45: getSectionByNumber(15) → getSectionByNumber(17)
// Change the href: from "/seguranca-e-integridade-financeira" (auto-generated slug) 
//                  to "/por-que-angola-por-que-agora"
```

**Priority:** P0 — The "Why Now" card links to an irrelevant section.

---

### GAP-003 — SectionCard and SectionNav route §9 to `/sobre-banzamia` instead of §11

**Surface:** All section cards and sidebar navigation

**Current:** `section.number === 9 ? '/sobre-banzamia'` — §9 is "Modelo de Certificação". The certification section routes to the BanzAI about page.

**Missing:** `section.number === 11 ? '/sobre-banzamia'` — §11 is "BanzAI" and should route to `/sobre-banzamia`.

**Required correction:**
```tsx
// SectionCard.tsx:31 and SectionNav.tsx:71,81:
// Change section.number === 9 → section.number === 11
```

**Priority:** P0 — §9 visitors are routed to the wrong page; §11 visitors don't get the special route.

---

### GAP-004 — [section]/page.tsx visual assignments wrong after renumbering

**Surface:** All dynamically-rendered section pages

**Current:** Six `case` statements in `SectionVisual` match old section numbers. After the §§1–3 integration:
- `case 9` → QRCommerceVisual appears on Modelo de Certificação
- `case 10` → WalletToWalletVisual appears on Federação
- `case 14` → EcosystemMap appears on Para Consumidores
- `case 16` → SecurityPipelineVisual appears on Sandbox
- `case 17` → SDKArchitectureVisual appears on Por que Angola
- `case 18` → EcosystemMap appears on Roadmap

**Required correction:** Update visual assignments to match current section numbers:
```tsx
function SectionVisual({ number }: { number: number }) {
  switch (number) {
    case 5:  return <EcosystemMap />           // Visão Geral do Ecossistema
    case 6:  return <PaymentFlowDiagram />     // Arquitectura Técnica
    case 10: return <EcosystemMap />           // Federação  
    case 12: return <SDKArchitectureVisual />  // Banzami para Programadores
    case 13: return <QRCommerceVisual />       // Banzami para Comerciantes
    case 14: return <MobilePaymentMockup />    // Para Consumidores
    case 15: return <SecurityPipelineVisual /> // Segurança e Integridade
    default: return null
  }
}
```

**Priority:** P0 — Wrong visuals are shown on six sections.

---

## P1 — Critical Narrative (Required for Propagation Completeness)

These gaps mean a major surface fails to answer the canonical question it is responsible for. A visitor on these surfaces cannot independently conclude the canonical identity model.

---

### GAP-005 — Homepage: Problem section names symptoms, not structural cause

**Surface:** `/` — problem section

**Current:** "O mercado angolano tem tudo para ser digital — smartphones, vontade, escala. O que falta é a infraestrutura de pagamento certa." + five problem cards listed without structural connection.

**Missing:** The structural diagnosis from §1 — "these are not five separate problems; they are five symptoms of the same structural problem: the absence of an open protocol layer." And specifically: Angola has EMIS (settlement layer) and payment products (M-Pesa-model operators) — what it lacks is a protocol layer that is open.

**Required correction:** Replace the problem section intro with the §1 structural argument:

> "Angola tem tudo para ser digital. O que falta não é mais uma aplicação de pagamentos. O que falta é a camada de protocolo que qualquer operador, programador ou instituição possa implementar com base em regras abertas — verificáveis, certificáveis, sem depender de nenhum operador único."

Then add a sentence connecting the five cards:
> "Estes não são cinco problemas separados. São cinco sintomas do mesmo problema estrutural."

**Priority:** P1 — Without this, the homepage problem section misses the entire structural argument that differentiates BANZA from a product.

---

### GAP-006 — Operators page: No "Why become a certified operator?" framing

**Surface:** `/operators`

**Current:** Registry opens with stats (N operators registered, N active, N Level 2+) and immediately renders the list. No introductory argument.

**Missing:** The value proposition of becoming a certified BANZA operator:
- Access to the same infrastructure as any other certified operator — no bilateral agreement required
- Federation: your users can transact with users of any other certified operator
- The protocol guarantees verifiable invariants (T+0 settlement, integer arithmetic, double-entry) — no contractual risk
- In the M-Pesa model, you need an agreement with Safaricom to access the network. In the BANZA model, you pass a conformance suite.

**Required correction:** Add an introductory section before the registry that answers: "What does it mean to be a certified BANZA operator, and why does it matter?" This section should derive directly from §3's "Certificação aberta" block and the §2 structural comparison.

**Priority:** P1 — An operator considering certification cannot make an informed decision from this page as it stands.

---

### GAP-007 — BanzAI Interface: No pre-interface context for why Protocol OS exists

**Surface:** `/banzamia`

**Current:** `<BanzamIAApp />` renders immediately with no introductory text.

**Missing:** A brief contextual block (3–4 sentences maximum) before the interface loads:

> "O BanzAI existe porque um protocolo que os seus utilizadores não conseguem navegar não escala. À medida que o BANZA cresce — mais operadores, mais programadores, mais reguladores, mais RFCs — o BanzAI torna o protocolo compreensível, verificável e certificável sem crescer o custo de suporte de forma linear. Não é um assistente de pagamentos para consumidores finais. É a interface cognitiva do protocolo: onde as ferramentas determinam a verdade e o BanzAI explica a verdade."

This should appear as a small banner or header above the interface, or as a collapsible info block.

**Priority:** P1 — A first-time visitor who lands from a search engine has no context before the interface.

---

### GAP-008 — Roadmap: No BANZA protocol vision before BanzAI feature list

**Surface:** `/roadmap`

**Current:** Roadmap header says "Roadmap público do BanzAI — Protocol Operating System for the Banza protocol." Items are all BanzAI tool capabilities.

**Missing:** A BANZA protocol vision section at the top of the roadmap:
- What does the BANZA protocol ecosystem look like at full deployment?
- Multiple certified operators federated across Angola
- Any developer building on protocol rules, not a proprietary API
- BanzAI making the protocol navigable as the ecosystem scales

Required correction: Add a "Visão BANZA" section before the BanzAI roadmap items that states the protocol-level future. Then rename the existing roadmap items section from "BanzAI Roadmap" to "BanzAI — Protocol Operating System Roadmap" and add at least 3–5 protocol-level milestones:
- Federation deployment (RFC-0008 in production)
- Second certified operator
- Protocol governance (multi-entity ADR contribution)

**Priority:** P1 — The roadmap currently describes what BanzAI features will exist, not what future BANZA creates. These are different questions.

---

### GAP-009 — No protocol/product distinction on any surface except the Reference

**Surface:** Homepage, Operators, BanzAI, Roadmap, Validation

**Current:** The protocol/product distinction (§2 and §3) is present only in the Reference page (which renders BANZA_REFERENCE.md). No other surface states it.

**Missing:** Every major surface should carry, in some form, the protocol/product distinction — calibrated to the surface's audience:
- Homepage: "BANZA não é um produto. É o protocolo que qualquer produto pode implementar."
- Operators: "Tornar-se um operador certificado não é integrar a API do Banzami. É implementar o protocolo BANZA — as mesmas regras que o Banzami implementa."
- BanzAI: "O BanzAI não é um produto do Banzami. É o sistema operativo do protocolo BANZA — serve qualquer operador certificado."

**Priority:** P1 — Without this, visitors across all surfaces can mistake BANZA for a Banzami product.

---

### GAP-010 — No survivability argument on any surface except the Reference

**Surface:** Homepage, Operators, Roadmap

**Current:** The survivability argument ("what happens if Banzami disappears?") is in §2 of BANZA_REFERENCE.md. It appears nowhere in the public surfaces.

**Missing:** On the homepage, at minimum: one sentence that answers why the protocol survives any operator. On the operators page: the survivability argument is one of the strongest reasons to choose the open model.

**Required correction (homepage):** Add to the ecosystem section:
> "O protocolo é o que fica. Os operadores mudam. O BANZA define as regras — nenhum operador, incluindo o Banzami, pode encerrar a infraestrutura."

**Priority:** P1 — This is the single most powerful differentiation argument from §2 and it appears on zero public surfaces.

---

## P2 — Important Narrative (Needed for Full Propagation)

These gaps mean a surface is incomplete or partially misleading, but a visitor can still form a rough correct model of BANZA.

---

### GAP-011 — Homepage "Como funciona" leads with technical features, not protocol argument

**Surface:** `/` — "Como funciona" section

**Current:** "Liquidação atómica. Ledger imutável. Confirmação instantânea." — leads with technical features.

**Missing:** The structural argument before the technical claims. The canonical argument from §3: these are protocol invariants, not product promises. Any certified operator must guarantee them.

**Required correction:** Add one sentence before or alongside the technical claims:
> "Estas não são funcionalidades do Banzami. São invariantes do protocolo BANZA — qualquer operador certificado as implementa porque o protocolo o exige."

**Priority:** P2 — Currently reads as product marketing. With one sentence, reads as protocol architecture.

---

### GAP-012 — "Banzami SDK oficial" on homepage developers section

**Surface:** `/` — Para programadores section

**Current:** "integra pagamentos em Kwanza com uma única chamada ao Banzami SDK oficial."

**Missing:** The canonical framing: the SDK is a Banzami implementation of the BANZA protocol's SDK requirement. Any certified operator exposes an SDK-compatible surface.

**Required correction:** "integra pagamentos em Kwanza com o SDK do protocolo BANZA — disponível para TypeScript, Flutter e PHP."

**Priority:** P2 — The current phrasing ties developers to Banzami specifically rather than to the protocol.

---

### GAP-013 — Validation page: No protocol-validation argument

**Surface:** `/validacao`

**Current:** "Acompanhamento rigoroso da implementação das funcionalidades descritas em BANZAMI_REFERENCE.md." — correct but sparse.

**Missing:** Why public validation matters for an open protocol:
> "Um protocolo aberto não vale promessas contratuais. Vale invariantes verificáveis. Esta página demonstra que as garantias do protocolo BANZA estão implementadas — e qualquer auditor pode verificar."

**Required correction:** Add 2–3 sentences to the hero section that explain why public validation is architecturally meaningful for an open protocol.

**Priority:** P2 — Currently an internal governance tool. With the right framing, it becomes the strongest trust signal in the ecosystem.

---

### GAP-014 — Roadmap: English/Portuguese inconsistency

**Surface:** `/roadmap`

**Current:** Roadmap item descriptions are in English ("RAG pipeline over protocol documents", "Multi-step research: plan → primary retrieval..."). Page header text and CTA are in Portuguese.

**Missing:** All content in Portuguese (pt-AO), consistent with the site's language policy.

**Required correction:** Translate roadmap item descriptions to Portuguese.

**Priority:** P2 — Inconsistency breaks the Portuguese-first positioning.

---

### GAP-015 — Operators page: No mention of BanzAI as certification accelerator

**Surface:** `/operators`

**Current:** BanzAI is not mentioned on the operators page.

**Missing:** A pointer from the operators page to the Certification Copilot module in BanzAI:
> "O BanzAI inclui um Certification Copilot que analisa o seu manifesto e indica o que falta para cada nível de certificação. Disponível em `/banzamia`."

**Priority:** P2 — BanzAI is the primary tool for certification — this connection should be present on the operators page.

---

### GAP-016 — About BanzAI: Section number stale in attribution

**Surface:** `/sobre-banzamia`

**Current:** Attribution says `§9`. BanzAI is now §11 after the §§1–3 integration.

**Missing:** `§11` in the attribution string.

**Required correction:** Part of GAP-001 fix.

**Priority:** P2 — Secondary to GAP-001 which fixes the actual content bug.

---

### GAP-017 — Reference page: Section intro missing for first-time visitors

**Surface:** `/reference`

**Current:** Document renders immediately after the metadata block (version, date, organisation, date). No intro sentence for a visitor who arrives without knowing what they're about to read.

**Missing:** A single sentence between the metadata block and the first section: "Este documento define o protocolo BANZA — a camada de infraestrutura aberta que qualquer operador certificado pode implementar, da mesma forma que o Pix define os pagamentos instantâneos no Brasil."

**Priority:** P2 — Minor improvement for the best-scoring surface.

---

### GAP-018 — Global OG keywords: Missing protocol-level terms

**Surface:** `layout.tsx` keywords array

**Current:** keywords include "Banzami Business", "Banzami SDK" — operator-level Banzami terms.

**Missing:** Protocol-level terms: "protocolo aberto Angola", "certificação aberta BANZA", "camada de protocolo Angola", "BanzAI Protocol OS"

**Required correction:** Add protocol-level keywords; remove or reframe operator-level terms.

**Priority:** P2 — SEO alignment with protocol-first narrative.

---

## P3 — Improvement (Enhances Propagation, Not Blocking)

---

### GAP-019 — Navigation: No direct links to §§1–3

**Surface:** Global navigation

**Current:** Nav links to /reference (which contains §§1–3) but no direct link to "O Problema", "A Camada que Falta", or "O que é o BANZA".

**Missing:** The three foundational sections are the protocol's most important narrative pages. Direct nav links, or a "Protocolo" dropdown containing them, would surface them to visitors who don't read the full reference.

**Priority:** P3 — The sections are reachable via the sidebar, but not from the main nav.

---

### GAP-020 — Manifesto quotes lack protocol layer naming

**Surface:** `/` — ManifestoQuote components

**Current:** "Angola não precisa de copiar o modelo de pagamentos dos outros. Angola precisa do seu — construído para o Kwanza, construído para o QR, construído para o smartphone em cada bolso."

**Missing:** A quote that names the protocol layer gap directly:
> "O EMIS resolve a liquidação entre bancos. O que Angola ainda não tinha era a camada que define quem pode oferecer serviços de pagamento, em que condições, com que garantias verificáveis. Essa é a camada que o BANZA constrói."

**Priority:** P3 — The current quotes are strong on the "why Angola" argument but not on the "why protocol layer" argument.

---

### GAP-021 — Dynamic sections §§1–3 have no visual components

**Surface:** `/o-problema-angola-tem-as-pecas`, `/a-camada-que-falta`, `/o-que-e-o-banza`

**Current:** These three new sections render text only — no visual component is assigned.

**Missing:** SVG illustration components for the three foundational sections:
- §1: A visual showing Angola's existing pieces (smartphone penetration, EMIS, payment products) with a gap where the protocol layer should be
- §2: The M-Pesa vs. Pix structural comparison diagram (already in BANZAMI_REFERENCE.md as a table — could be an SVG)
- §3: The three-tier hierarchy diagram (BANZA → BanzAI → Banzami) as an SVG

**Priority:** P3 — Narrative content is strong. Visuals would reinforce it.

---

*Gap report completed: 2026-05-30. No files modified.*
