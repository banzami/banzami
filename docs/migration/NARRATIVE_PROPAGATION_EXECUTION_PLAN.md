---
title: NARRATIVE_PROPAGATION_EXECUTION_PLAN
version: 1.0
date: 2026-05-30
status: PLAN — not yet authorized for execution
---

# Narrative Propagation Execution Plan

**Four waves. Each wave is a deployable unit.**

Each wave must be committed, pushed, and deployed before the next begins. Wave 1 is not optional — it fixes rendering bugs that make narrative work on subsequent waves meaningless.

---

## Wave 1 — Fix Integration Bugs (Prerequisites for Everything Else)

**Goal:** Correct the four rendering bugs introduced by the §§1–3 integration. These are not narrative issues — they are functional bugs that cause wrong content to appear.

**Items:** GAP-001, GAP-002, GAP-003, GAP-004

**All four items must be executed as a single atomic commit.**

---

### W1-A — Fix About BanzAI section number (GAP-001)

**File:** `apps/docs/app/sobre-banzamia/page.tsx`

**Change 1 — Section lookup:**
```tsx
// Line 20 — was:
const section = getSectionByNumber(9)
// Change to:
const section = getSectionByNumber(11)
```

**Change 2 — Index lookup:**
```tsx
// Line 24 — was:
const idx = sections.findIndex((s) => s.number === 9)
// Change to:
const idx = sections.findIndex((s) => s.number === 11)
```

**Change 3 — Source attribution string:**
```tsx
// Line 94 — was:
<code className="rounded bg-bz-surface px-1.5 font-mono">docs/BANZAMI_REFERENCE.md §9</code>
// Change to:
<code className="rounded bg-bz-surface px-1.5 font-mono">docs/BANZA_REFERENCE.md §11</code>
```

---

### W1-B — Fix Homepage "Why Now" section number (GAP-002)

**File:** `apps/docs/app/page.tsx`

**Change:**
```tsx
// Line 45 — was:
const whyNowSection = getSectionByNumber(15)
// Change to:
const whyNowSection = getSectionByNumber(17)
```

---

### W1-C — Fix SectionCard and SectionNav routing (GAP-003)

**File 1:** `apps/docs/components/SectionCard.tsx`
```tsx
// Line 31 — was:
href={section.number === 9 ? '/sobre-banzamia' : `/${section.slug}`}
// Change to:
href={section.number === 11 ? '/sobre-banzamia' : `/${section.slug}`}
```

**File 2:** `apps/docs/components/SectionNav.tsx`
```tsx
// Line 71 — was:
{navLink('/sobre-banzamia', 'BanzAI')}
// No change needed — this is a direct nav link, not section-number-dependent

// Line 81 — was:
const href = section.number === 9 ? '/sobre-banzamia' : `/${section.slug}`
// Change to:
const href = section.number === 11 ? '/sobre-banzamia' : `/${section.slug}`
```

---

### W1-D — Fix section visual assignments (GAP-004)

**File:** `apps/docs/app/[section]/page.tsx`

**Change the `SectionVisual` function:**
```tsx
function SectionVisual({ number }: { number: number }) {
  switch (number) {
    case 5:  return <EcosystemMap />           // Visão Geral do Ecossistema
    case 6:  return <PaymentFlowDiagram />     // Arquitectura Técnica
    case 10: return <EcosystemMap />           // Federação
    case 12: return <SDKArchitectureVisual />  // Banzami para Programadores
    case 13: return <QRCommerceVisual />       // Banzami para Comerciantes
    case 14: return <MobilePaymentMockup />    // Para Consumidores
    case 15: return <SecurityPipelineVisual /> // Segurança e Integridade Financeira
    default: return null
  }
}
```

Remove: `case 9`, `case 10` (old), `case 16`, `case 17`, `case 18`
Add: `case 5`, updated `case 10`, updated `case 13`, updated `case 14`, updated `case 15`

Also update the comment strings to reflect current section titles.

---

### W1 — Verification

After implementing all four items:
1. Visit `/sobre-banzamia` — confirm it renders §11 (BanzAI) content, not §9 (Certificação)
2. Visit `/` — confirm "Porquê agora?" card links to `/por-que-angola-por-que-agora`
3. Visit section cards — confirm §9 card links to `/modelo-de-certificacao` and §11 card links to `/sobre-banzamia`
4. Visit `/federacao` — confirm no WalletToWalletVisual appears (it was wrongly assigned)
5. Visit `/seguranca-e-integridade-financeira` — confirm SecurityPipelineVisual appears
6. Run `npx vitest run lib/__tests__/reference.test.ts` — 51/51 pass

**Wave 1 commit message:** `fix(integration): correct section numbering bugs from §§1–3 integration`

---

## Wave 2 — Homepage

**Goal:** Propagate the §§1–3 canonical narrative into the homepage. The homepage is the highest-traffic surface and must independently communicate the canonical identity model.

**Items:** GAP-005, GAP-009 (homepage), GAP-010 (homepage), GAP-011, GAP-012, GAP-020

**Canonical requirement:** A visitor who reads only the homepage must be able to answer "Why does BANZA exist?" within the first screen.

---

### W2-A — Restructure the problem section (GAP-005)

**File:** `apps/docs/app/page.tsx` — problem section

**Replace the problem section intro:**
```tsx
// Current:
<h2 className="mb-4 text-2xl font-bold tracking-tight text-bz-text md:text-3xl">
  O que Angola precisa de ultrapassar
</h2>
<p className="mb-10 max-w-2xl text-bz-muted">
  O mercado angolano tem tudo para ser digital — smartphones, vontade, escala. 
  O que falta é a infraestrutura de pagamento certa.
</p>

// Replace with:
<h2 className="mb-4 text-2xl font-bold tracking-tight text-bz-text md:text-3xl">
  Angola tem as peças. Falta a camada que as liga.
</h2>
<p className="mb-4 max-w-2xl text-bz-muted">
  Angola tem smartphones. Tem uma economia informal enorme. Tem rails de liquidação 
  interbancária. O que falta não é mais um produto de pagamentos — é a camada de 
  protocolo aberta que qualquer operador, programador ou instituição possa implementar 
  com base em regras verificáveis.
</p>
<p className="mb-10 max-w-2xl text-xs text-bz-muted">
  Estes não são cinco problemas separados. São cinco sintomas do mesmo problema estrutural.
</p>
```

---

### W2-B — Add survivability argument to ecosystem section (GAP-010)

**File:** `apps/docs/app/page.tsx` — ecosystem section

**Add to the paragraph beneath the "Ecossistema" heading:**
```tsx
// Current:
<p className="mb-8 max-w-2xl text-bz-muted">
  Consumidores, comerciantes, apps externas, Banzami SDKs, bancos e o core financeiro 
  — todos ligados através de uma infraestrutura do Banza.
</p>

// Replace with:
<p className="mb-8 max-w-2xl text-bz-muted">
  Consumidores, comerciantes, programadores e operadores certificados — todos ligados 
  através do protocolo BANZA. O protocolo é o que fica. Os operadores mudam. Nenhum 
  operador, incluindo o Banzami, pode encerrar a infraestrutura.
</p>
```

---

### W2-C — Add protocol invariants framing to "Como funciona" (GAP-011)

**File:** `apps/docs/app/page.tsx` — "Como funciona" section

**Add one sentence before or inside the section:**
```tsx
// Add to the paragraph beneath the section heading:
<p className="mb-8 max-w-2xl text-bz-muted">
  Cada pagamento BANZA é uma transferência directa entre carteiras, registada no ledger 
  de forma atómica e imutável. Estas não são funcionalidades do Banzami — são invariantes 
  do protocolo. Qualquer operador certificado as implementa porque o protocolo o exige.
</p>
```

---

### W2-D — Fix "Banzami SDK" framing in developers section (GAP-012)

**File:** `apps/docs/app/page.tsx` — Para programadores section

```tsx
// Current:
<p className="mb-8 max-w-2xl text-bz-muted">
  O Banza é SDK-first. Qualquer app — táxi, delivery, escola, ecommerce — integra 
  pagamentos em Kwanza com uma única chamada ao Banzami SDK oficial.
</p>

// Replace with:
<p className="mb-8 max-w-2xl text-bz-muted">
  O BANZA é SDK-first. A integração programática via SDK é um requisito do protocolo — 
  não uma funcionalidade opcional. Qualquer app integra pagamentos em Kwanza com o SDK 
  do protocolo, disponível para TypeScript, Flutter e PHP.
</p>
```

---

### W2-E — Add protocol/product distinction to hero subheadline (GAP-009, homepage)

**File:** `apps/docs/components/HeroSection.tsx`

The current subheadline is close but doesn't explicitly state the protocol/product distinction. Add a short line after the tagline:

```tsx
// Current:
<p className="mx-auto mb-7 max-w-2xl text-lg leading-relaxed text-bz-muted md:text-xl">
  Banza define como o dinheiro se move digitalmente — através de operadores certificados, 
  regras verificáveis, infraestrutura aberta e um sistema operativo nativo...
</p>

// Add after the main subheadline (as a secondary line or part of the badge):
// A small pill/tag beneath the main headline:
<div className="mb-6 text-sm text-bz-muted">
  BANZA é o protocolo. Não um produto. Não um operador. A infraestrutura que nenhum 
  operador pode fechar.
</div>
```

---

### W2 — Verification

After implementing all Wave 2 items:
1. Visit `/` — first screen must name the protocol layer gap
2. The five problem cards must follow "São cinco sintomas do mesmo problema estrutural"
3. The ecosystem section must include the survivability argument
4. The "Como funciona" section must name invariants, not features
5. The developers section must reference the protocol SDK, not the "Banzami SDK oficial"
6. Visual audit: does the homepage independently communicate the canonical identity model?

**Wave 2 commit message:** `feat(narrative): W2 — homepage protocol narrative propagation`

---

## Wave 3 — Operators + BanzAI + Roadmap

**Goal:** Propagate the canonical narrative into the three surfaces most affected by missing context — the operators page (WHY become certified), the BanzAI interface (WHY Protocol OS exists), and the roadmap (WHAT future BANZA creates).

**Items:** GAP-006, GAP-007, GAP-008, GAP-009 (operators, BanzAI), GAP-010 (operators), GAP-013 (partial), GAP-015

---

### W3-A — Operators page: Add "Why certified operator?" opening (GAP-006, GAP-009)

**File:** `apps/docs/app/operators/page.tsx`

**Add a section BEFORE the registry hero that frames the WHY:**

```tsx
{/* Protocol argument — above the hero */}
<div className="border-b border-bz-border bg-bz-primary-light px-5 py-8 md:px-8 lg:px-12">
  <div className="mx-auto max-w-4xl">
    <h2 className="mb-3 text-lg font-bold text-bz-primary">
      O modelo aberto: o que significa ser um operador certificado BANZA
    </h2>
    <p className="mb-4 max-w-2xl text-sm text-bz-muted">
      No modelo fechado, aceder à infraestrutura de pagamentos exige um acordo bilateral 
      com o operador dominante — que pode alterar as condições, restringir o acesso ou 
      encerrar o serviço. No modelo BANZA, aceder à infraestrutura exige passar um 
      conformance suite — um conjunto de testes técnicos que qualificam a implementação. 
      Nenhum acordo com o Banzami. Nenhum volume mínimo. Só as regras do protocolo.
    </p>
    <p className="max-w-2xl text-sm text-bz-muted">
      Qualquer operador certificado partilha a mesma infraestrutura: as mesmas invariantes 
      verificáveis, o mesmo modelo de federação, as mesmas garantias de protocolo. 
      Os seus utilizadores podem transaccionar com utilizadores de qualquer outro operador 
      certificado — porque ambos implementam o mesmo protocolo aberto.
    </p>
    <div className="mt-4">
      <a href="/banzamia" className="text-xs font-semibold text-bz-primary hover:underline">
        Usar o BanzAI Certification Copilot para avaliar prontidão →
      </a>
    </div>
  </div>
</div>
```

---

### W3-B — BanzAI Interface: Add pre-interface context block (GAP-007, GAP-009)

**File:** `apps/docs/app/banzamia/page.tsx`

**Add a brief context block above `<BanzamIAApp />`:**

```tsx
export default function BanzamIAPage() {
  return (
    <>
      <NoBodyScroll />
      {/* Protocol context — visible for ~2s before interface is ready */}
      <div className="fixed inset-x-0 top-14 z-20 border-b border-bz-border bg-bz-surface px-4 py-2">
        <p className="text-xs text-bz-muted max-w-2xl mx-auto text-center">
          O BanzAI é o Sistema Operativo do Protocolo BANZA — não um chatbot de pagamentos. 
          Existe para quem trabalha com o protocolo: programadores, operadores, reguladores, auditores.{' '}
          <span className="font-medium text-bz-text">Ferramentas determinam a verdade. A IA explica a verdade.</span>
        </p>
      </div>
      <div className="fixed inset-x-0 bottom-0 top-[calc(3.5rem+2.5rem)] z-30 overflow-hidden">
        <Suspense fallback={null}>
          <BanzamIAApp />
        </Suspense>
      </div>
    </>
  )
}
```

**Note:** The exact height offset depends on the banner height. Adjust `top-[calc(...)]` to match.

---

### W3-C — Roadmap: Add BANZA protocol vision section (GAP-008)

**File:** `apps/docs/app/roadmap/page.tsx`

**Add a "Visão do Protocolo" section before the feature items:**

```tsx
{/* Protocol vision — before the roadmap items */}
<div className="mb-10 rounded-2xl border border-bz-primary/20 bg-bz-primary-light p-6">
  <h2 className="mb-3 text-base font-bold text-bz-primary">Visão: O que o BANZA cria</h2>
  <p className="mb-3 text-sm text-bz-muted">
    O objectivo não é um conjunto de ferramentas. O objectivo é uma infraestrutura 
    que nenhum operador pode fechar — onde qualquer entidade certificada pode construir, 
    qualquer programador pode integrar, e qualquer regulador pode verificar.
  </p>
  <ul className="space-y-2 text-sm text-bz-muted">
    <li>→ Múltiplos operadores certificados federados em Angola — qualquer utilizador transacciona com qualquer outro</li>
    <li>→ Qualquer programador constrói sobre regras abertas, não sobre uma API proprietária</li>
    <li>→ O BanzAI torna o protocolo navegável à medida que o ecossistema escala</li>
    <li>→ Invariantes verificáveis: nenhum operador pode prometer T+0 — o protocolo garante-o</li>
  </ul>
</div>
```

**Also add BANZA protocol milestones to the roadmap items:** Supplement the existing BanzAI feature list with 3–5 protocol-level items:
```
{ id: 'p1', status: 'in-progress', title: 'RFC-0008 Federation — Produção', description: '...' }
{ id: 'p2', status: 'planned', title: 'Segundo operador certificado', description: '...' }
{ id: 'p3', status: 'planned', title: 'Governança multi-entidade de ADRs', description: '...' }
```

---

### W3-D — Translate roadmap items to Portuguese (GAP-014)

All roadmap item descriptions in English must be translated to Portuguese. This is a content update to `ITEMS` in `apps/docs/app/roadmap/page.tsx`.

---

### W3 — Verification

1. `/operators` — first section answers "Why become a certified operator?" before the registry
2. `/banzamia` — context banner explains why Protocol OS exists before interface loads
3. `/roadmap` — protocol vision appears before the BanzAI feature list; Portuguese throughout

**Wave 3 commit message:** `feat(narrative): W3 — operators, BanzAI, roadmap protocol narrative propagation`

---

## Wave 4 — Validation + Remaining Surfaces

**Goal:** Complete propagation to the remaining surfaces — validation page, reference landing, navigation, metadata, and the three new dynamic section pages (§§1–3).

**Items:** GAP-013, GAP-016 (already in W1), GAP-017, GAP-018, GAP-019, GAP-021

---

### W4-A — Validation page: Add protocol-validation argument (GAP-013)

**File:** `apps/docs/app/validacao/page.tsx`

**Add 2–3 sentences to the hero:**
```tsx
// After the current hero description, add:
<p className="mb-4 text-sm text-bz-muted max-w-2xl">
  Um protocolo aberto não vale promessas contratuais. Vale invariantes verificáveis. 
  Este sistema demonstra que as garantias do protocolo BANZA estão implementadas — 
  e qualquer auditor pode inspeccionar a evidência.
</p>
```

**Also add BanzAI pointer:**
```tsx
<p className="text-xs text-bz-muted">
  O BanzAI inclui um Certification Copilot que analisa prontidão de certificação.{' '}
  <a href="/banzamia" className="text-bz-primary hover:underline">Experimentar →</a>
</p>
```

---

### W4-B — Reference landing: Add intro sentence (GAP-017)

**File:** `apps/docs/app/reference/page.tsx`

**Add one sentence between the metadata block and the first section:**
```tsx
<div className="mt-6 mb-10 rounded-xl border border-bz-border bg-bz-surface px-5 py-4">
  <p className="text-sm text-bz-muted">
    Este documento define o protocolo BANZA — a camada de infraestrutura aberta que qualquer 
    operador certificado pode implementar, da mesma forma que o Pix define os pagamentos 
    instantâneos no Brasil e o UPI os define na Índia. Começa pelo problema (§1), explica 
    o modelo (§2), define o protocolo (§3), e cobre governança, certificação, federação, 
    BanzAI e Banzami nas secções seguintes.
  </p>
</div>
```

---

### W4-C — Update global metadata keywords (GAP-018)

**File:** `apps/docs/app/layout.tsx`

**Update keywords array:**
```tsx
keywords: [
  'BANZA',
  'protocolo aberto Angola',
  'camada de protocolo Angola',
  'pagamentos digitais Angola',
  'certificação aberta BANZA',
  'BanzAI Protocol OS',
  'Banzami',
  'pagamentos em Kwanza',
  'QR Code Angola',
  'carteira digital Angola',
  'infraestrutura financeira Angola',
  'pagamentos instantâneos Angola',
  'federação de operadores',
  'conformance suite BANZA',
],
```

---

### W4-D — Navigation: Add foundational sections as entry points (GAP-019)

**File:** `apps/docs/app/layout.tsx`

**Option A (dropdown):** Add a "Protocolo" dropdown to the desktop nav that links directly to §§1–3:
```
Protocolo ▾
  → O Problema (/o-problema-angola-tem-as-pecas)
  → A Camada que Falta (/a-camada-que-falta)
  → O que é o BANZA (/o-que-e-o-banza)
```

**Option B (inline):** Replace the current "Referência" nav link with three or four direct links:
```
O Problema · A Camada · O que é o BANZA · Referência completa
```

Choose based on nav space constraints.

---

### W4-E — Section visual components for §§1–3 (GAP-021)

**File:** `apps/docs/app/[section]/page.tsx`

Add visual components for the three new sections. These require SVG diagrams to be created first:

| Section | Diagram needed |
|---|---|
| §1 — O Problema | Angola's existing pieces (EMIS, smartphones, products) with a protocol layer gap highlighted |
| §2 — A Camada que Falta | Closed model vs. open model structural comparison (M-Pesa vs. Pix/UPI vs. BANZA) |
| §3 — O que é o BANZA | Three-tier hierarchy (BANZA → BanzAI → Banzami) with function labels |

**Note:** These SVGs should be created as part of the existing SVG illustration standard (ArchitectureDiagram component for SVG). Until the SVGs exist, the sections render text-only, which is acceptable.

---

### W4 — Verification

1. `/validacao` — protocol-validation argument present, BanzAI pointer present
2. `/reference` — intro sentence present before first section
3. Search engine preview — keywords include protocol-level terms
4. `/o-problema-angola-tem-as-pecas` — section renders correctly (text-only acceptable at this stage)
5. Navigation — §§1–3 accessible from main nav in some form

**Wave 4 commit message:** `feat(narrative): W4 — validation, reference, metadata, navigation narrative propagation`

---

## Propagation Complete: Success Criteria

After all four waves, verify the following by visiting each major page cold (no prior context):

| Question | Surface | Expected answer |
|---|---|---|
| Why does BANZA exist? | Homepage (first screen) | Protocol layer gap in Angola — not infrastructure, not products |
| Why not just use a payment app? | Homepage (problem section) | Five symptoms, one structural cause — closed models don't solve it |
| Why become a certified operator? | /operators (first section) | Open certification vs. bilateral agreements; federation rights; protocol invariants |
| What is BANZA not? | /reference (§3) | Not a bank, not a product, not an API, not a gateway, not Banzami |
| Why does the Protocol OS exist? | /banzamia (banner) | Protocols are hard to navigate at scale; BanzAI makes BANZA navigable |
| What future does BANZA create? | /roadmap (first section) | Multiple operators, federated ecosystem, verifiable invariants |
| Why does public validation matter? | /validacao (hero) | Open protocol → verifiable invariants, not contractual promises |

**If a visitor can answer all seven questions from the surfaces listed — narrative propagation is complete.**

---

## Summary

| Wave | Focus | Items | Estimated files | Deploy required? |
|---|---|---|---|---|
| Wave 1 | Integration bug fixes | GAP-001 through GAP-004 | 4 files | Yes — bugs are live |
| Wave 2 | Homepage narrative | GAP-005, 009, 010, 011, 012, 020 | 2–3 files | Yes |
| Wave 3 | Operators + BanzAI + Roadmap | GAP-006, 007, 008, 009, 010, 014, 015 | 3 files | Yes |
| Wave 4 | Validation + remaining surfaces | GAP-013, 017, 018, 019, 021 | 3–4 files | Yes |

**Total: ~12–14 source files. Zero new pages required. All changes are content additions to existing surfaces.**

---

*Execution plan completed: 2026-05-30. No files modified.*
