---
title: NARRATIVE_PROPAGATION_AUDIT
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no files modified
canonical_source: BANZA_REFERENCE.md §§1–3
---

# Narrative Propagation Audit

**Canonical thesis (from §§1–3):**

1. Angola has settlement infrastructure (EMIS) and payment products — but lacks an open protocol layer
2. The five symptoms of cash/WhatsApp/exclusion are one structural problem, not five separate ones
3. BANZA is the open protocol layer — the rules, not the product
4. The protocol/product distinction is the central distinction of the entire ecosystem
5. Any certified entity can implement the protocol — the protocol survives any operator
6. BanzAI exists because protocols are hard to navigate at scale — it is the Protocol OS
7. Banzami is the reference implementation — the first certified operator, not the owner

---

## Surface 1 — Homepage (`/`)

### What the page says

- **Title:** "Banza — Protocolo de Infraestrutura Financeira Programável"
- **Hero headline:** "Infraestrutura financeira programável."
- **Hero subheadline:** "Banza define como o dinheiro se move digitalmente — através de operadores certificados, regras verificáveis, infraestrutura aberta..."
- **Problem section label:** "O que Angola precisa de ultrapassar"
- **Problem section intro:** "O mercado angolano tem tudo para ser digital — smartphones, vontade, escala. O que falta é a infraestrutura de pagamento certa."
- Five problem cards: cash dependency, WhatsApp proofs, apps without payment, small businesses excluded, no Angolan SDK
- **"Como funciona" section:** leads with "Liquidação atómica. Ledger imutável. Confirmação instantânea."
- **"Para programadores":** "integra pagamentos em Kwanza com uma única chamada ao Banzami SDK oficial"
- **Manifesto quote:** "Angola não precisa de copiar o modelo de pagamentos dos outros."
- No mention of the protocol/product distinction
- No survivability argument
- `getSectionByNumber(15)` hardcoded for "Why Now" link → §15 is now "Segurança e Integridade Financeira" after the §§1–3 integration; should be §17

### What the canonical narrative requires

- The problem section must name the structural cause: **not just "infrastructure missing" but "open protocol layer missing"**
- The five symptoms must be identified as five symptoms of one cause — not five separate problems
- The manifesto quote must connect to the protocol model, not just to Angola-specific framing
- The "Como funciona" section leads with technical features before establishing why the protocol model matters — architecture before argument
- "Banzami SDK" in the developers teaser implies Banzami = the SDK maker, not BANZA = the protocol

### Gaps

| Gap | Type | Severity |
|---|---|---|
| Problem section says "infraestrutura de pagamento certa" not "camada de protocolo aberta" | Missing concept | HIGH |
| Five problems presented as list, not as symptoms of one structural cause | Contradictory framing | HIGH |
| No protocol/product distinction anywhere on the page | Missing concept | CRITICAL |
| No survivability argument — "what happens if Banzami disappears?" not addressed | Missing protocol argument | MEDIUM |
| "Como funciona" leads with technical features, not with protocol-vs-product argument | Product-first positioning | MEDIUM |
| "Banzami SDK oficial" — implies Banzami is the SDK maker, not BANZA is the protocol | Operator-first positioning | MEDIUM |
| `getSectionByNumber(15)` → wrong section (§15 is Security, should be §17 "Por que Angola") | Integration bug | CRITICAL |
| Manifesto quote does not name the protocol layer gap | Weak differentiation | LOW |

---

## Surface 2 — Operators Page (`/operators`)

### What the page says

- **Title:** "Registo de Operadores Banza"
- **Description:** "Registo curado de operadores que implementam o protocolo Banza."
- Page opens directly with a registry list — manifests, capabilities, conformance levels, federation readiness
- Three footer notes: "Registo curado", "Manifests validados", "Conformidade pública"
- No introduction of why operators exist or why becoming one matters
- No protocol/product distinction
- No explanation of what "certified" means in the context of an open protocol

### What the canonical narrative requires

- The page must answer **"Why become a certified operator?"** before listing who is registered
- The open model must be explained: any entity that passes the conformance suite becomes a certified operator — no bilateral agreement with Banzami required
- The contrast with closed models must be present: in the M-Pesa model, you need an agreement with the operator. In the BANZA model, you pass a conformance suite.
- The value proposition must be stated: as a certified operator you can build on the same infrastructure as Banzami, and your users can transact with users of any other certified operator via federation

### Gaps

| Gap | Type | Severity |
|---|---|---|
| Page opens with a list — never asks or answers "Why become a certified operator?" | Missing protocol argument | CRITICAL |
| No protocol/product distinction — "operator" is treated as an administrative category | Missing concept | CRITICAL |
| No explanation of open certification vs. bilateral agreements | Missing concept | HIGH |
| No federation value proposition — why operators can interoperate | Missing concept | HIGH |
| No contrast between closed model and open model | Weak differentiation | HIGH |
| No mention of what the protocol guarantees certified operators (invariants, settlement, QR) | Missing protocol argument | MEDIUM |

---

## Surface 3 — Reference Landing (`/reference`)

### What the page says

- **Title:** "Banza — Referência Oficial do Protocolo"
- Renders the canonical tagline from BANZA_REFERENCE.md (now: "BANZA é o protocolo. BanzAI é o Sistema Operativo. Banzami é a implementação de referência.")
- Renders all 19 sections of BANZA_REFERENCE.md — including the new §§1–3
- Document metadata: version, status, organisation, date

### What the canonical narrative requires

- The reference page IS the canonical narrative, rendered correctly
- §§1–3 are present and render their full hardened content
- The tagline correctly states the three-tier hierarchy

### Gaps

| Gap | Type | Severity |
|---|---|---|
| Attribution footer still displays `docs/BANZAMI_REFERENCE.md` (old filename) | Naming (NM-001 from naming audit) | LOW |
| Metadata description still says "20 secções" (was V1 count; now 19 sections) | Stale count | LOW |
| No introductory framing before the full document — a visitor who lands here has no context for what they're about to read | Missing concept | MEDIUM |

---

## Surface 4 — Dynamic Section Pages (`/[section]`)

### What the page says

Each section renders its BANZA_REFERENCE.md content via `MarkdownSection`. The section visual component mapping (`SectionVisual`) injects domain-specific diagrams based on hardcoded section numbers.

### Integration bug: All visual assignments shifted

The §§1–3 integration renumbered all sections by +2. The visual component assignments in `[section]/page.tsx` were not updated:

| Hardcoded case | Current section at that number | Assigned visual | Correct? |
|---|---|---|---|
| `case 6` | Arquitectura Técnica | PaymentFlowDiagram | Questionable |
| `case 9` | Modelo de Certificação | QRCommerceVisual | **WRONG** |
| `case 10` | Federação | WalletToWalletVisual | **WRONG** |
| `case 12` | Banzami para Programadores | SDKArchitectureVisual | **CORRECT** |
| `case 13` | Banzami para Comerciantes | MobilePaymentMockup | Acceptable |
| `case 14` | Para Consumidores | EcosystemMap | **WRONG** |
| `case 16` | Sandbox e Ambiente de Testes | SecurityPipelineVisual | **WRONG** |
| `case 17` | Por que Angola. Por que Agora. | SDKArchitectureVisual | **WRONG** |
| `case 18` | Roadmap | EcosystemMap | **WRONG** |

### Correct assignments (post-integration section numbers)

| Section | Title | Correct visual |
|---|---|---|
| §5 | Visão Geral do Ecossistema | EcosystemMap |
| §6 | Arquitectura Técnica | PaymentFlowDiagram |
| §10 | Federação | EcosystemMap |
| §12 | Banzami para Programadores | SDKArchitectureVisual |
| §13 | Banzami para Comerciantes | MobilePaymentMockup (or QRCommerceVisual) |
| §14 | Para Consumidores | MobilePaymentMockup |
| §15 | Segurança e Integridade Financeira | SecurityPipelineVisual |

### Gaps

| Gap | Type | Severity |
|---|---|---|
| Six section-to-visual mappings are wrong after §§1–3 integration | Integration bug | HIGH |
| §1, §2, §3 (new) have no visual component — they render text only | Missing concept | LOW |

---

## Surface 5 — BanzAI Live Interface (`/banzamia`)

### What the page says

- **Title:** "BanzAI — Protocol Operating System" — CORRECT
- **Description:** "BanzAI é o Sistema Operativo do Protocolo Banza. 16 módulos..." — CORRECT
- Page body: renders `<BanzamIAApp />` immediately with no introductory text

### What the canonical narrative requires

- A visitor landing on `/banzamia` must understand **why the Protocol OS exists** before encountering the interface
- The canonical argument: "protocols are hard to navigate at scale — BanzAI is the interface that makes BANZA navigable, verifiable, and certifiable"
- Without this context, visitors encounter a complex 16-module interface with no framing of its purpose relative to the protocol

### Gaps

| Gap | Type | Severity |
|---|---|---|
| Zero pre-interface context — page drops visitors into a 16-module interface without explaining why it exists | Missing concept | CRITICAL |
| No statement of the protocol/BanzAI relationship before the interface loads | Missing protocol argument | HIGH |
| No differentiation from a consumer chatbot — a new visitor cannot tell this is protocol infrastructure, not a payment assistant | Missing differentiation | HIGH |

---

## Surface 6 — About BanzAI (`/sobre-banzamia`)

### What the page says

- **Title:** "Sobre o BanzAI" — CORRECT
- **Description:** "BanzAI — o Sistema Operativo do Protocolo Banza..." — CORRECT
- Protocol OS context paragraph: "O BanzAI é o Sistema Operativo do Protocolo Banza — 16 módulos especializados que tornam o protocolo compreensível..." — GOOD
- **CRITICAL BUG:** `getSectionByNumber(9)` — renders §9 (Modelo de Certificação) instead of §11 (BanzAI). This page is currently rendering the wrong section.
- Source attribution says `§9` — should be `§11`
- `SectionHero` shows §9's title — Modelo de Certificação

### Gaps

| Gap | Type | Severity |
|---|---|---|
| `getSectionByNumber(9)` should be `getSectionByNumber(11)` — page renders wrong section | Integration bug | CRITICAL |
| Source attribution `§9` → `§11` | Integration bug | HIGH |
| The prev/next navigation computes relative to §9, not §11 | Integration bug | MEDIUM |

---

## Surface 7 — Roadmap (`/roadmap`)

### What the page says

- **Title:** "BanzAI Roadmap" — BanzAI-specific, not BANZA protocol
- **Description:** "Roadmap público do BanzAI — Protocol Operating System for the Banza protocol."
- Breadcrumb: `Banza / BanzAI / Roadmap` — frames roadmap as child of BanzAI
- All 28 items are BanzAI tool capabilities (RAG pipeline, graph, certification copilot, etc.)
- No BANZA protocol milestones (federation deployment, multi-operator ecosystem, certification of second operator)
- No answer to "What future does BANZA create?"
- Mix of English and Portuguese (roadmap item descriptions are in English, header text is in Portuguese)

### What the canonical narrative requires

- The roadmap must answer: "What future does BANZA create?" before listing features
- The canonical argument: multiple certified operators federated across Angola; any developer building on protocol rules rather than a proprietary API; BanzAI making the protocol navigable as it scales
- The roadmap must distinguish between: (a) protocol milestones and (b) BanzAI tool milestones

### Gaps

| Gap | Type | Severity |
|---|---|---|
| Roadmap answers "what features does BanzAI get?" not "what future does BANZA create?" | BanzAI-first positioning | HIGH |
| No protocol milestones — federation deployment, second certified operator, RFC milestones | Missing protocol argument | HIGH |
| No opening statement of the BANZA protocol vision before the feature list | Missing concept | HIGH |
| English/Portuguese mix in roadmap items | Consistency | LOW |

---

## Surface 8 — Validation (`/validacao`)

### What the page says

- **Title:** "Validação"
- **H1:** "Execução e Validação do Protocolo Banza" — CORRECT, protocol-first
- Governance framing: "Consulta pública · edição restrita à administração Banzami" — CORRECT
- References `BANZAMI_REFERENCE.md` (old filename, NM-001)
- No explanation of WHY the validation system exists in the context of an open protocol

### What the canonical narrative requires

- For a first-time visitor: what does it mean that an open protocol has a public implementation matrix?
- The canonical argument: an open protocol's guarantees are only meaningful if they are verifiable — the validation system is proof that the protocol's invariants are implemented, not just promised

### Gaps

| Gap | Type | Severity |
|---|---|---|
| No opening explanation of why public validation exists for an open protocol | Missing protocol argument | MEDIUM |
| References `BANZAMI_REFERENCE.md` (stale filename from naming audit NM-001) | Naming | LOW |

---

## Surface 9 — Navigation (global header)

### What the nav says

Nav order: Referência → Programadores → Comerciantes → Arquitectura → Segurança → Operadores → Validação → BanzAI

### What the canonical narrative requires

- The canonical narrative hierarchy: Problem → Protocol → Certification → Federation → BanzAI → Operators → Banzami
- The nav currently places "Referência" first (GOOD) but the new §§1-3 entry points are not prominently surfaced
- Visitors can reach the canonical narrative via Referência, but there is no direct nav link to "O Problema" or "A Camada que Falta" or "O que é o BANZA"

### Gaps

| Gap | Type | Severity |
|---|---|---|
| No nav shortcut to the three foundational sections (§1, §2, §3) | Missing concept | MEDIUM |
| Footer link "O que é o Banza?" links to `/o-que-e-o-banza` — this slug is now §3 in the new structure and should still resolve | Navigation | LOW |

---

## Surface 10 — Metadata / OG / SEO

### What the metadata says

- Site title: "Banza — Protocolo de Infraestrutura Financeira Programável" — GOOD
- OG description: "Banza é o protocolo aberto de infraestrutura financeira programável. Operadores certificados, regras verificáveis, infraestrutura aberta." — GOOD
- Keywords: includes "Banzami Business", "Banzami SDK" — operator-level
- Missing protocol-level keywords: "protocolo aberto Angola", "certificação aberta", "BanzAI Protocol OS", "camada de protocolo Angola"

### Gaps

| Gap | Type | Severity |
|---|---|---|
| Keywords dominated by Banzami operator terms, missing BANZA protocol terms | Legacy narrative | LOW |
| OG description lacks the protocol survivability differentiation | Weak differentiation | LOW |
| Individual section OG descriptions are generic ("Referência oficial Banza — §N: Title") | Missing protocol argument | LOW |

---

## Critical Integration Bugs (Blocking, Fix Before Propagation)

These are functional bugs introduced by the §§1–3 integration that must be fixed regardless of narrative work:

| Bug | Location | Effect |
|---|---|---|
| `getSectionByNumber(9)` | `sobre-banzamia/page.tsx:20` | Renders §9 (Certificação) instead of §11 (BanzAI) |
| `getSectionByNumber(15)` | `page.tsx:45` | "Why Now" links to §15 (Security) instead of §17 |
| `section.number === 9` routing | `SectionCard.tsx:31`, `SectionNav.tsx:71,81` | Routes §9 visitors to `/sobre-banzamia` instead of §11 |
| Visual assignments in `[section]/page.tsx` | `case 9,10,14,16,17,18` | 6 wrong visuals shown on wrong sections |

---

*Audit completed: 2026-05-30. No files modified.*
