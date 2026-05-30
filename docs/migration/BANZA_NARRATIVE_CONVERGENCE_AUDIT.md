---
title: BANZA_NARRATIVE_CONVERGENCE_AUDIT
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no modifications applied
---

# BANZA Narrative Convergence Audit

**Mission:** Determine whether every public surface converges toward the canonical thesis —
that BANZA is the protocol layer Angola lacks — and whether the narrative hierarchy
(BANZA → BanzAI → Banzami) is consistently the dominant mental model a visitor forms.

**This audit does not look for:**
- Naming errors (ADR-025 alignment is complete)
- ADR reference inconsistencies (complete)
- Old terminology (complete)

**This audit looks for:**
- Narrative convergence: does every surface reinforce the canonical thesis?
- Narrative substitution: which surfaces let QR / Wallet / SDK / BanzAI / Banzami become the story instead of BANZA?
- Competitive framing: does BANZA explain why it is not EMIS, Stripe, M-Pesa, blockchain, or traditional acquiring?

**Test standard:** A visitor who reads only this page should leave able to say "BANZA is the protocol layer Angola lacks" — not "BANZA is a QR payment app."

**Scoring:**
- PASS — page actively reinforces the canonical thesis
- PARTIAL — thesis is implied or present but not dominant
- ABSENT — page does not reference the thesis
- FAIL — page actively works against the thesis (something else becomes the story)

---

## Surface 1 — Homepage (`/`)

### Narrative Arc (section sequence)

```
[1] Hero badge:           "Infraestrutura Financeira Programável para Angola"
[2] Hero H1:              "Infraestrutura financeira programável."
[3] Hero subheadline:     "Banza define como o dinheiro se move digitalmente —
                           através de operadores certificados, regras verificáveis,
                           infraestrutura aberta..."
[4] BanzAI widget         (HomeBanzamIAEntry — embedded above fold)
[5] ManifestoQuote:       "Angola não precisa de copiar o modelo de pagamentos dos outros..."
[6] Eyebrow: "O problema" / H2: "O que Angola precisa de ultrapassar"
[7] 5 problem cards       (cash dependence, WhatsApp proofs, apps without payments,
                           TPA exclusion, no SDK)
[8] Eyebrow: "Como funciona" / H2: "Liquidação atómica. Ledger imutável. Confirmação instantânea."
[9] Eyebrow: "Filosofia wallet-native" / H2: "O telemóvel é a carteira."
[10] Eyebrow: "Ecossistema" / H2: "Uma rede. Múltiplos actores."
[11] Eyebrow: "QR Commerce" / H2: "QR como primitiva nativa do protocolo."
[12] Eyebrow: "Casos de uso" / H2: "Banza em toda Angola"
[13] Eyebrow: "Mobile-first" / H2: "O pagamento perfeito dura menos de 3 segundos."
[14] Eyebrow: "Para programadores" / H2: "SDK-first. Integração em Kwanza."
[15] Eyebrow: "Segurança" / H2: "Infraestrutura de grau bancário."
[16] ManifestoQuote:      "O QR torna-se o terminal. O telemóvel torna-se a carteira."
[17] Reference grid       (all sections)
```

### The Narrative Problem

Sections [1]–[3] establish BANZA as infrastructure. Sections [8]–[14] systematically replace that frame:

- Section [9]: **Wallet becomes the story.** "O telemóvel é a carteira." The headline erases the protocol and makes the consumer device the protagonist.
- Section [11]: **QR becomes the story.** "QR como primitiva nativa do protocolo." QR takes the headline, even though the sub-text correctly adds "do protocolo."
- Section [12]: **Use cases become the story.** Taxis, cantinas, delivery — product applications, not protocol.
- Section [13]: **Mobile-first becomes the story.** "O pagamento perfeito dura menos de 3 segundos." A consumer UX claim, not a protocol claim.
- Section [14]: **SDK becomes the story.** "SDK-first. Integração em Kwanza." Correct framing — but positioned as a developer feature, not a protocol property.
- Section [16]: **QR and wallet become the story again.** "O QR torna-se o terminal. O telemóvel torna-se a carteira." The closing manifesto quote doubles down on product framing.

After section [3], the homepage never returns to "BANZA is the protocol layer Angola lacks." The canonical thesis is stated once in the hero subheadline — then buried under 10 product sections.

**Most critical absence:** No section explains WHY the protocol must exist. The problem cards (Section [7]) show symptoms: WhatsApp proofs, no SDK, TPA exclusion. Not one card names the cause: Angola has no open protocol layer that any developer or operator can build on. The symptoms exist *because* the protocol layer is missing. Without the cause, the homepage reads as five product problems solved by one product (Banzami).

---

### 7-Question Audit

**Q1. What is BANZA?**
PASS — hero subheadline: "Banza define como o dinheiro se move digitalmente — através de operadores certificados, regras verificáveis, infraestrutura aberta."

**Q2. Why does BANZA exist?**
FAIL — No section explains the structural reason: Angola has settlement rails and payment products but no open protocol layer. The problem section shows symptoms (WhatsApp proofs, no TPA alternative) but never names the infrastructure gap as the root cause.

**Q3. What infrastructure gap does BANZA fill?**
ABSENT — "Protocol layer" is never used. "Missing layer" is never stated. "EMIS exists but isn't the protocol" is never stated.

**Q4. Why not use the existing alternative?**
ABSENT — No comparison to EMIS, Multicaixa, Stripe, M-Pesa, bank transfers. The TPA problem card implicitly compares (TPA is expensive), but doesn't explain the structural difference.

**Q5. What role does BanzAI play?**
PARTIAL — HomeBanzamIAEntry widget is visible: "O Sistema Operativo nativo do Protocolo Banza." The label is correct. But a visitor who uses the widget gets answers, not an understanding of WHY BanzAI exists at the protocol level.

**Q6. What role does Banzami play?**
FAIL — Banzami is implied as the product that does everything. The three-tier hierarchy (BANZA → BanzAI → Banzami) is never visible on the homepage. A visitor has no way to understand that Banzami is the reference implementation of the protocol, not the protocol itself.

**Q7. Can a visitor explain BANZA after reading only this page?**
PARTIAL — Likely output: "BANZA is Angola's programmable payment system. It has QR, wallets, and SDKs." Not: "BANZA is the open protocol layer Angola lacks — like Pix for Brazil or UPI for India."

### CURRENT / IMPLICIT / DESIRED

**Finding 1 — Problem section:**
```
CURRENT:  5 symptom cards (cash, WhatsApp, apps, TPA, SDK)
IMPLICIT: "Banzami solves 5 payment problems"
DESIRED:  Cards converge on one cause: "Angola has settlement rails and payment products
           but no open protocol layer. These five symptoms have one root."
```

**Finding 2 — Wallet section:**
```
CURRENT:  Eyebrow: "Filosofia wallet-native" / H2: "O telemóvel é a carteira."
IMPLICIT: "BANZA is a mobile wallet"
DESIRED:  "Wallet-native is a protocol property — not a product feature.
           Any certified operator on BANZA is wallet-native by design."
```

**Finding 3 — QR section:**
```
CURRENT:  Eyebrow: "QR Commerce" / H2: "QR como primitiva nativa do protocolo."
IMPLICIT: "BANZA is a QR payment system"
DESIRED:  Sub-text correctly says "do protocolo" — but the H2 should lead with
           the protocol angle: "Any BANZA operator can issue and accept QR payments.
           QR is a protocol primitive — not a Banzami feature."
```

**Finding 4 — Closing manifesto quote:**
```
CURRENT:  "O QR torna-se o terminal. O telemóvel torna-se a carteira.
           Angola salta directamente para a infraestrutura de pagamento do futuro."
IMPLICIT: "This is a product vision — a QR/mobile payment future"
DESIRED:  A quote that names the protocol as the mechanism: "The protocol layer
           makes the leap possible. BANZA is that layer."
```

**Finding 5 — No "protocol layer" section:**
```
CURRENT:  No section exists that explains the infrastructure gap
IMPLICIT: None — the gap is simply invisible
DESIRED:  A section between the manifesto quote and the problem cards: "Angola has
           settlement infrastructure. Angola has payment products. What Angola lacks
           is a protocol layer — open rules any developer can build on. BANZA is that layer."
```

### Overall Narrative Verdict

**FAIL.** The homepage correctly names BANZA as infrastructure in the hero, then immediately replaces that frame with product sections. A visitor who skims the section headers reads: Problem / How it works / Wallet / Ecosystem / QR / Use cases / Mobile / SDK / Security. None of these headers say "protocol layer."

---

## Surface 2 — Reference (`/reference` and section pages)

### Narrative Arc

The reference is 17 sections. The narrative arc matters as much as individual section content.

```
§1:  O que é o Banza? — defines BANZA as infrastructure, three-tier hierarchy
§2:  Princípios Fundamentais — "O protocolo é o produto"
§3:  Visão Geral do Ecossistema — kernel, operators, BanzAI, SDKs
§4:  Arquitectura Técnica — Rust kernel, 18 crates, Go services
§5:  Representação Monetária — monetary invariants
§6:  Governança — RFCs, ADRs, validation matrix
§7:  Modelo de Certificação — 5 levels, conformance suite
§8:  Federação — inter-operator federation (planned)
§9:  BanzAI — Protocol OS, 16 modules, 900+ lines
§10: Banzami para Programadores — SDK examples
§11: Banzami para Comerciantes — QR, no hardware
§12: Para Consumidores — wallet, @banza handle
§13: Segurança — security pipeline
§14: Sandbox — testing environment
§15: Por que Angola. Por que Agora. — Pix/UPI/M-Pesa (3 sentences)
§16: Roadmap — implementation milestones
§17: Declaração de Visão — emotional close
```

### The Narrative Problem

The reference has the right content — but the wrong architecture for strategic narrative. The sections that contain the most strategically important positioning (§1, §2, §15) are surrounded by deep technical content (§4, §5, §13). A visitor who only reads §1 gets the best positioning. A visitor who reads all 17 sections gets the best technical content but loses the strategic thread.

The canonical thesis ("Angola lacks a protocol layer") is never concentrated in one place. It is distributed across:
- §1 line 42: "É o protocolo que define como o dinheiro se move digitalmente"
- §2: "O protocolo é o produto"
- §15: "O modelo está provado: o Pix no Brasil, o UPI na Índia..."

But these fragments are separated by thousands of lines of technical content. The thesis is never assembled as a complete argument.

**BanzAI becomes the story in §9.** §9 is the longest section by far (900+ lines). It contains genuinely excellent BanzAI positioning. But its size means that for a visitor reading the reference chronologically, BanzAI dominates the reference experience. The protocol-as-infrastructure argument is strongest in §1 and §2; the BanzAI narrative is strongest in §9 and dwarfs everything that came before it.

---

### 7-Question Audit

**Q1. What is BANZA?** PASS — §1 has the strongest "what" on the site.
**Q2. Why does BANZA exist?** PARTIAL — §2 and §15 provide reasons, but no concentrated argument.
**Q3. What infrastructure gap does BANZA fill?** PARTIAL — implied in §1, stated in §15 (briefly). "Protocol layer" not used as a term.
**Q4. Why not use the existing alternative?** PARTIAL — §1 says "Não é um banco... não é uma plataforma fintech genérica." §15 names Pix/UPI/M-Pesa. No comparative analysis of any competitor.
**Q5. What role does BanzAI play?** PASS — §9 is comprehensive.
**Q6. What role does Banzami play?** PASS — §1, §2, §3 are clear post-ADR-025 rewrite.
**Q7. Can a visitor explain BANZA after reading only §1?** PARTIAL — gets "protocol" but not "infrastructure gap" or "why it must exist."

### CURRENT / IMPLICIT / DESIRED

**Finding 1 — §15 Pix/UPI/M-Pesa:**
```
CURRENT:  "O modelo está provado: o Pix no Brasil, o UPI na Índia, o M-Pesa em
           Moçambique. Angola tem as mesmas pré-condições. O Banza é a infraestrutura."
IMPLICIT: "BANZA is similar to Pix, UPI, and M-Pesa"
DESIRED:  "Pix unified Brazil's fragmented payment ecosystem because it is a protocol —
           open rules any bank or fintech can implement. UPI did the same for India.
           M-Pesa is different: it is a closed, operator-controlled network. BANZA
           is the protocol model (Pix/UPI), not the closed model (M-Pesa). BANZA is
           what Angola builds its own ecosystem on."
```

**Finding 2 — §1 negative definitions:**
```
CURRENT:  "Não é um banco. Não é uma carteira digital simples. Não é uma plataforma
           fintech genérica adaptada de um modelo ocidental."
IMPLICIT: "BANZA is none of these things" (but what IS the structural difference?)
DESIRED:  Add: "It exists because none of those things provide what Angola actually
           needs: an open protocol layer — certified rules that any operator, developer,
           or institution can build on without negotiating access to a closed network."
```

**Finding 3 — §2 "O protocolo é o produto" (most important principle):**
```
CURRENT:  A one-line heading in a six-principle list. No visual prominence.
IMPLICIT: "This is one of several design principles"
DESIRED:  This is the single most important strategic claim on the site.
           It deserves visual treatment: a callout block, a diagram, or a dedicated
           subsection — not one line among six.
```

### Overall Narrative Verdict

**PARTIAL.** The reference contains all the right content. Its weakness is architecture: the canonical thesis is distributed, not concentrated. A determined reader assembles it; a casual reader doesn't.

---

## Surface 3 — Architecture (`/arquitectura-tecnica`)

### Narrative Arc

This is a technical section page (§4 of the reference). It shows:
- 18-crate Rust kernel table
- Service topology diagram
- Go services, PostgreSQL, event flows

No narrative frame. Opens on technical content. Closes on technical content.

### 7-Question Audit

**Q1. What is BANZA?** ABSENT — section opens on kernel structure, not protocol definition.
**Q2. Why does BANZA exist?** ABSENT
**Q3. What infrastructure gap?** ABSENT
**Q4. Why not use existing alternatives?** ABSENT
**Q5. BanzAI role?** ABSENT
**Q6. Banzami role?** ABSENT
**Q7. One-page explanation?** FAIL — visitor learns "BANZA is a Rust payment system."

### CURRENT / IMPLICIT / DESIRED

**Finding 1 — No strategic frame for architecture choices:**
```
CURRENT:  18-crate table listing: ledger, wallets, consumer-wallets, transactions...
IMPLICIT: "BANZA is a sophisticated payment API"
DESIRED:  Preface with why these choices matter: "The BANZA kernel enforces the protocol
           rules at the infrastructure level. The 18-crate separation means no operator
           can collapse ledger logic into business logic. Financial correctness is
           structural — not policy."
```

**Finding 2 — EMIS appears as a crate, not as context:**
```
CURRENT:  "| `acquiring` | Integração EMIS/Multicaixa |" (one table row)
IMPLICIT: "BANZA integrates with EMIS/Multicaixa" (unclear what relationship)
DESIRED:  A brief note: "BANZA operates above the EMIS settlement rails — using them
           for final settlement, while providing the protocol layer (certification,
           invariants, federation) that EMIS does not."
```

### Overall Narrative Verdict

**ABSENT.** The architecture page is correctly technical. Its gap is the complete absence of strategic context for why the architectural choices matter. A future "Architecture" section intro could establish this frame in 3–4 sentences.

---

## Surface 4 — Operators (`/operators`)

### Narrative Arc

```
[1] Badge: "Registo Público · Protocolo v1.0"
[2] H1: "Registo de Operadores Banza"
[3] Body: "Registo curado de operadores que implementam o protocolo Banza.
           Manifests validados, capacidades declaradas, níveis de conformidade
           e preparação para federação."
[4] Stats: N operators registered / N active / N Level 2+
[5] Privacy notice: "Transparência de infraestrutura, não vigilância financeira"
[6] Operator registry (filters, cards)
[7] Footer: 3 factual notes about registry curation, manifest validation, conformance
```

### The Narrative Problem

The page answers "what is the operator registry" but not "why does the operator model matter." A visitor learns that some companies have implemented the Banza protocol. They do not learn:
- Why multiple operators on one protocol is better than one company controlling payments
- What a visitor or developer gains from certified operators existing
- Why certification prevents capture of the ecosystem by any single operator
- Why early certification is strategically valuable (federation interoperability)

**Operators become the story** — but the operators-as-mechanism story (they enable open ecosystem competition) is absent. The registry reads as a list of partner companies, not as evidence that BANZA has achieved something structurally significant.

---

### 7-Question Audit

**Q1. What is BANZA?** PARTIAL — implied as "the protocol" but not defined.
**Q2. Why does BANZA exist?** ABSENT
**Q3. What infrastructure gap?** ABSENT
**Q4. Why not use existing alternatives?** PARTIAL — one implicit claim: "Nenhum operador pode auto-declarar certificação." Implies self-declaration is insufficient.
**Q5. BanzAI role?** ABSENT
**Q6. Banzami role?** ABSENT — Banzami does not appear on the operators page at all.
**Q7. One-page explanation?** FAIL — "Banza is a payment network with certified partners."

### CURRENT / IMPLICIT / DESIRED

**Finding 1 — Page hero:**
```
CURRENT:  "Registo curado de operadores que implementam o protocolo Banza."
IMPLICIT: "Here is a list of companies using Banza"
DESIRED:  "Any entity that passes the BANZA conformance suite becomes a certified
           operator — able to offer BANZA payment services independently. This registry
           is evidence that BANZA is not a closed network: it is an open protocol
           that any qualified entity can join."
```

**Finding 2 — Privacy notice:**
```
CURRENT:  "Transparência de infraestrutura, não vigilância financeira."
IMPLICIT: "We publish this for privacy reasons"
DESIRED:  This is a genuine differentiator: "A payment network controlled by one
           company is not required to publish this. BANZA publishes operator
           capabilities publicly because the protocol is open — anyone can verify
           what any operator has certified."
```

**Finding 3 — Footer note on conformance:**
```
CURRENT:  "Os níveis de conformidade (0–4) são determinados pelo runner oficial do
           Banza. Nenhum operador pode auto-declarar certificação sem ter passado os testes."
IMPLICIT: "Quality assurance mechanism"
DESIRED:  "This is what makes BANZA structurally different from a closed payment network:
           no operator — not even Banzami — can claim capabilities they have not
           verified against the conformance suite. The protocol's rules apply equally
           to all participants."
```

### Overall Narrative Verdict

**FAIL.** The operators page is the natural home for the ecosystem narrative. It is the only page that shows the open-protocol model in action. It does not explain what it is showing.

---

## Surface 5 — Validation (`/validacao`)

### Narrative Arc

```
[1] Badge: "Execução e Validação · v[version]"
[2] H1: "Execução e Validação do Protocolo Banza"
[3] Body: "Acompanhamento rigoroso da implementação das funcionalidades descritas em
           BANZAMI_REFERENCE.md."
[4] Governance notice: "Consulta pública · edição restrita à administração Banzami"
[5] Progress percentage + item counts
[6] ValidationMetrics grid
[7] ValidationDashboard (interactive)
[8] ArchitectureHealth
[9] Footer attribution
```

### The Narrative Problem

The validation page is the most unusual surface on the site: it publicly exposes implementation progress, acceptance criteria, confidence scores, and history logs for a financial infrastructure protocol. No comparable payment system in Africa publishes this.

But the page presents this as a routine dashboard — not as the extraordinary transparency signal it is. The word "pública" appears in the governance notice ("Consulta pública") but is not explained: *why* is this public? What does it mean that a financial infrastructure protocol publishes this level of detail?

**Implementation tracking becomes the story.** The visitor sees: percentages, status badges, item counts. The strategic claim — BANZA operates transparently because the protocol is open and the rules are public — is invisible.

---

### 7-Question Audit

**Q1. What is BANZA?** ABSENT
**Q2. Why does BANZA exist?** ABSENT
**Q3. What infrastructure gap?** ABSENT
**Q4. Why not use existing alternatives?** ABSENT
**Q5. BanzAI role?** ABSENT
**Q6. Banzami role?** ABSENT
**Q7. One-page explanation?** FAIL — "Banza is a payment system that publicly tracks its development progress."

### CURRENT / IMPLICIT / DESIRED

**Finding 1 — Hero body:**
```
CURRENT:  "Acompanhamento rigoroso da implementação das funcionalidades descritas em
           BANZAMI_REFERENCE.md. Cada item rastreado ao documento de referência oficial."
IMPLICIT: "This is a development tracker"
DESIRED:  "BANZA publishes its implementation status publicly because the protocol's
           rules are public. No payment infrastructure in Angola publishes this.
           This is what protocol transparency looks like — not a black box."
```

**Finding 2 — Governance notice:**
```
CURRENT:  "Consulta pública · edição restrita à administração Banzami"
IMPLICIT: "You can view but not edit"
DESIRED:  "Public by design. The BANZA protocol is open — its implementation
           progress is too. Operators, developers, and regulators can verify
           what has been built, what is planned, and what invariants hold."
```

### Overall Narrative Verdict

**ABSENT.** The validation page's hidden differentiator — extraordinary public transparency for financial infrastructure — is never named. The page reads as an internal tracker made visible, not as a strategic transparency claim.

---

## Surface 6 — Roadmap (`/roadmap`)

### Narrative Arc

```
[1] Breadcrumb: Banza / BanzAI / Roadmap
[2] H1: "BanzAI Roadmap"
[3] Body: "Roadmap público do BanzAI — Protocol Operating System for the Banza protocol.
           We publish this transparently because trust begins with visibility."
[4] Status legend
[5] 28 roadmap items grouped by status (BanzAI only)
[6] CTA: "Experimente o BanzAI"
```

### The Narrative Problem

The roadmap is BanzAI-specific. The BANZA protocol roadmap (federation timeline, open operators, acquiring integration, carris cross-border) exists only in §16 of the reference. This creates a structural problem:

- A visitor interested in BANZA's protocol future (federation, open operators, what the network looks like in 2028) has no dedicated surface.
- A visitor who reads the roadmap forms the impression that BANZA's future is primarily about AI tooling — not about open protocol federation and ecosystem growth.

**BanzAI becomes the story of BANZA's future.** The BANZA protocol evolution narrative is invisible from any navigation path except the full reference.

---

### 7-Question Audit

**Q1. What is BANZA?** PARTIAL — BANZA is mentioned as the protocol BanzAI serves.
**Q2. Why does BANZA exist?** ABSENT
**Q3. What infrastructure gap?** ABSENT
**Q4. Why not use existing alternatives?** ABSENT
**Q5. BanzAI role?** PASS — "Protocol Operating System" with 8 capabilities.
**Q6. Banzami role?** ABSENT
**Q7. One-page explanation?** FAIL — "BanzAI is an AI operating system for payments, being built in phases."

### CURRENT / IMPLICIT / DESIRED

**Finding 1 — Page scope:**
```
CURRENT:  28 BanzAI roadmap items. No BANZA protocol milestones.
IMPLICIT: "BANZA's future is BanzAI"
DESIRED:  Two tracks: (1) BanzAI roadmap (current content), (2) BANZA Protocol roadmap
           (federation milestones, open operators, acquiring, cross-border rails).
           The protocol track shows WHY BanzAI matters: more operators joining means
           more protocol to explain. BanzAI scales the protocol's adoption.
```

**Finding 2 — Opening body:**
```
CURRENT:  "Roadmap público do BanzAI — Protocol Operating System for the Banza protocol.
           We publish this transparently because trust begins with visibility."
IMPLICIT: "Transparency is a BanzAI value"
DESIRED:  "Transparency is a BANZA protocol value. The protocol is open; its roadmap
           is too. BanzAI's roadmap tracks the Protocol OS. The BANZA protocol roadmap
           tracks federation, open operators, and ecosystem growth."
```

### Overall Narrative Verdict

**FAIL for BANZA positioning.** PASS for BanzAI positioning. The roadmap makes BanzAI the protagonist of BANZA's future.

---

## Surface 7 — BanzAI Interface (`/banzamia`)

### Narrative Arc

```
[1] Page loads → full-screen BanzamIAApp
[2] Sidebar: module tabs (Knowledge, RFC Explorer, Certification Copilot, etc.)
[3] Chat interface
[4] No landing state, no framing, no context
```

### The Narrative Problem

The /banzamia URL is the primary BanzAI entry point. A visitor navigating to it from the homepage nav (label: "BanzAI") arrives at a full-screen interface with zero context.

**The interface becomes the story.** A visitor sees a chat box. They ask a question. They get an answer with citations. They leave having experienced a chatbot — not having understood the Protocol OS.

The /sobre-banzamia page (which has the Protocol OS explanation from §9) is accessible only from the footer. It is not linked from the BanzAI interface header, the sidebar, or the main navigation.

---

### 7-Question Audit

**Q1. What is BANZA?** ABSENT
**Q2. Why does BANZA exist?** ABSENT
**Q3. What infrastructure gap?** ABSENT
**Q4. Why not use existing alternatives?** ABSENT
**Q5. BanzAI role?** PARTIAL — page metadata: "Protocol Operating System." Not visible in the interface.
**Q6. Banzami role?** ABSENT
**Q7. One-page explanation?** FAIL — "BanzAI is a payment chatbot."

### CURRENT / IMPLICIT / DESIRED

**Finding 1 — No landing state:**
```
CURRENT:  Full-screen interface loads immediately
IMPLICIT: "BanzAI is a tool you use, not a system you understand"
DESIRED:  3-second landing state before the interface: name ("BanzAI — Protocol OS"),
           single differentiator ("Not a chatbot. The protocol explains itself."),
           capability overview (6 OS verbs). Then open the interface.
```

**Finding 2 — Interface framing:**
```
CURRENT:  Chat input: "Pergunte sobre QR, SDKs, operadores, certificação, invariantes…"
IMPLICIT: "This is a support chatbot for BANZA products"
DESIRED:  "Ask the protocol anything. BanzAI grounds answers in protocol documents,
           not AI inference. Every answer cites its source."
```

### Overall Narrative Verdict

**FAIL.** The most differentiated capability on the site is also the most underexplained. A cold visitor leaves thinking "payment chatbot."

---

## Surface 8 — Programadores (`/banzami-para-programadores`)

### Narrative Arc

The section page (§10 of reference) opens on SDK code immediately:

```
[1] SectionHero: "§10 — Banzami para Programadores"
[2] "Integração em horas — A superfície de integração oficial do Banza são os SDKs."
[3] SDK table (TypeScript, Flutter, PHP)
[4] Code examples (QR creation, webhooks, idempotency, sandbox)
```

### The Narrative Problem

**SDK becomes the story.** The developer page assumes the developer has already decided to use BANZA. It does not explain why BANZA is the right choice over existing alternatives. This is the highest-value missing argument for the developer audience.

---

### 7-Question Audit

**Q1. What is BANZA?** ABSENT
**Q2. Why does BANZA exist?** ABSENT
**Q3. What infrastructure gap?** ABSENT
**Q4. Why not use existing alternatives?** FAIL — no comparison to Stripe (no AOA support), Flutterwave (limited Angola), EMIS direct (requires institutional access), or custom HTTP (no protocol guarantees).
**Q5. BanzAI role?** ABSENT
**Q6. Banzami role?** PARTIAL — SDKs are branded as Banzami SDKs.
**Q7. One-page explanation?** FAIL — "Banza is a payment SDK for Angola."

### CURRENT / IMPLICIT / DESIRED

**Finding 1 — Opening line:**
```
CURRENT:  "Integração em horas — A superfície de integração oficial do Banza são os SDKs."
IMPLICIT: "Here is how to use the SDK"
DESIRED:  "No international payment gateway supports AOA natively. Direct EMIS
           integration requires institutional relationships unavailable to startups.
           BANZA is the open protocol layer: SDK-first, Kwanza-native, T+0 settlement,
           and accessible to any developer — no acquiring agreement required."
```

**Finding 2 — SDK table:**
```
CURRENT:  | SDK | Pacote | Casos de uso |
           TypeScript / Flutter / PHP (products, not protocol)
IMPLICIT: "These are Banzami product SDKs"
DESIRED:  Frame as protocol SDKs: "These SDKs implement the BANZA protocol.
           Any app integrating them becomes part of the certified operator ecosystem —
           not just a Banzami customer."
```

### Overall Narrative Verdict

**FAIL.** The developer page is the highest-leverage adoption surface and the weakest narrative surface. It provides implementation without motivation.

---

## Surface 9 — Comerciantes (`/banzami-para-comerciantes`)

### Narrative Arc

```
[1] SectionHero: "§11 — Banzami para Comerciantes"
[2] "Sem hardware. Sem burocracia."
[3] QR types (static vs dynamic)
[4] T+0 settlement
[5] Banzami Business dashboard features
[6] Payment links
```

### The Narrative Problem

**Banzami becomes the story.** The merchant page is correct — merchants buy into Banzami the product. But it provides zero upward framing. A merchant who reads this page has no way to understand:
- The guarantee behind the QR payment is a certified protocol, not a company promise
- Any other BANZA-certified operator can serve them equally
- T+0 settlement is a protocol invariant, not a Banzami business decision

---

### 7-Question Audit

**Q1. What is BANZA?** ABSENT
**Q2. Why does BANZA exist?** ABSENT
**Q3. What infrastructure gap?** ABSENT — "Sem TPA, sem contrato bancário" implies the gap but never names it.
**Q4. Why not use existing alternatives?** PARTIAL — "Sem hardware, sem burocracia" is the implicit TPA comparison. No others.
**Q5. BanzAI role?** ABSENT
**Q6. Banzami role?** PASS — page correctly presents Banzami as the merchant product.
**Q7. One-page explanation?** FAIL — "Banzami is a QR payment app for merchants."

### CURRENT / IMPLICIT / DESIRED

**Finding 1 — T+0 settlement:**
```
CURRENT:  "O montante líquido é creditado na carteira do comerciante imediatamente
           após a confirmação do pagamento. Não há espera de dias bancários."
IMPLICIT: "This is a Banzami product feature"
DESIRED:  "T+0 settlement is a BANZA protocol invariant — enforced on all certified
           operators. It is not a Banzami policy. The protocol guarantees it."
```

**Finding 2 — Section framing:**
```
CURRENT:  Zero protocol context before merchant features
IMPLICIT: "This is how Banzami works for merchants"
DESIRED:  One sentence at the top: "Banzami is built on the BANZA protocol — the open
           infrastructure layer that makes these guarantees enforceable, not just
           promised."
```

### Overall Narrative Verdict

**FAIL for BANZA positioning.** PASS for Banzami product positioning. The merchant page correctly describes the product. It does not credit the protocol.

---

## Cross-Surface Narrative Substitution Map

The following patterns identify where other narratives crowd out the canonical thesis:

| Pattern | Surfaces where it occurs |
|---------|--------------------------|
| **QR becomes the story** | Homepage (section 11, closing quote), Comerciantes |
| **Wallet becomes the story** | Homepage (section 9), Consumidores |
| **SDK becomes the story** | Homepage (section 14), Programadores |
| **BanzAI becomes the story** | Homepage (widget before problem section), Roadmap, /banzamia |
| **Banzami becomes the story** | Comerciantes, Programadores (SDKs), §17 (partially corrected) |
| **Use cases become the story** | Homepage (use case grid), §17 transformation section |
| **Mobile becomes the story** | Homepage (section 13), Consumidores |

### Critical Observation

Every substitution is individually justifiable. QR is important. Wallets are important. BanzAI is important. The problem is cumulative: each section pushes BANZA one level deeper into supporting context, until the canonical thesis ("BANZA is the protocol layer") has no section, no headline, and no dedicated moment of its own.

The thesis is mentioned once in the hero subheadline. It is never the hero. It is never a section. It is never an eyebrow. It is never a manifesto quote. It is background.

---

## Competitor Narrative Coverage

| Competitor | Coverage | Strongest existing claim |
|-----------|---------|-------------------------|
| EMIS / settlement rails | ABSENT | `acquiring` crate name (§3) |
| Multicaixa / TPA | WEAK | "TPA é caro e burocrático" (homepage problem card) |
| Stripe / international gateways | ABSENT | Nothing |
| Flutterwave / Paystack | ABSENT | Nothing |
| Traditional acquiring | PARTIAL | "Sem TPA, sem contrato bancário" (Comerciantes) |
| Traditional banking | WEAK | "Não é um banco" (§1 negation only) |
| Blockchain / crypto | ABSENT | Nothing |
| M-Pesa (closed mobile money) | ABSENT | Named in §15 but not compared |
| Pix (open protocol) | ABSENT | Named in §15 but not compared |
| UPI (open protocol) | ABSENT | Named in §15 but not compared |

The single most important missing comparison: M-Pesa vs Pix/UPI. M-Pesa is a closed operator network. Pix/UPI are open protocols. BANZA is the Pix/UPI model. This structural distinction — which explains BANZA's entire design philosophy — appears nowhere on the site.

---

## Summary: Convergence Failures by Surface

| Surface | Canonical thesis? | Competitor frame? | Narrative substitution |
|---------|------------------|------------------|----------------------|
| Homepage | PARTIAL (hero only) | ABSENT | QR + Wallet + SDK + BanzAI |
| Reference §1 | PASS | WEAK | None (§1 is clean) |
| Reference §15 | PARTIAL | PARTIAL (3 sentences) | None |
| Architecture | ABSENT | ABSENT | Technical specs |
| Operators | ABSENT | ABSENT | Operator list |
| Validation | ABSENT | ABSENT | Implementation tracker |
| Roadmap | ABSENT | ABSENT | BanzAI |
| BanzAI interface | ABSENT | ABSENT | Chat interface |
| Programadores | ABSENT | ABSENT | SDK |
| Comerciantes | ABSENT | ABSENT | Product features |

**Only one page actively states the canonical thesis: the homepage hero.** Every other surface either doesn't address it or lets something else become the story.

---

*Audit completed: 2026-05-30. No modifications applied.*
