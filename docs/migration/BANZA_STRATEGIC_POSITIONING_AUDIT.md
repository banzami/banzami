---
title: BANZA_STRATEGIC_POSITIONING_AUDIT
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no modifications applied
---

# BANZA Strategic Positioning Audit

**Objective:** Determine whether visitors to banzami.org understand not only WHAT BANZA IS, but WHY BANZA MATTERS — and whether they can explain the difference between BANZA and existing alternatives.

**Method:** Full read of all public surfaces: page source (TSX), rendered content source (BANZAMI_REFERENCE.md sections), component copy, metadata, navigation labels.

**Test standard:** A visitor who spends 5 minutes on a given page should be able to:
1. Say what BANZA is
2. Say why BANZA exists
3. Say what problem it solves
4. Say how BANZA differs from payment networks, fintech APIs, processors, banking infrastructure, blockchain, and open payment protocols
5. Describe BanzAI's role
6. Not confuse BANZA with a payment app
7. Summarise BANZA in one clear sentence

**Verdict codes:** PASS · PARTIAL · FAIL · ABSENT

---

## Surface 1 — Homepage (`/`)

**URL:** `banzami.org`
**Components:** HeroSection, HomeBanzamIAEntry, ManifestoQuote, PaymentFlowDiagram, EcosystemMap, WalletToWalletVisual, QRCommerceVisual, SDKArchitectureVisual, SecurityPipelineVisual, MobilePaymentMockup, use-case grid, problem grid

---

**Q1. What is BANZA?**

The hero headline reads "Infraestrutura financeira programável." with the subheadline: "Banza define como o dinheiro se move digitalmente — através de operadores certificados, regras verificáveis, infraestrutura aberta e um sistema operativo nativo capaz de explicar, validar e evoluir o protocolo."

The badge reads "Infraestrutura Financeira Programável para Angola."

**Verdict: PARTIAL.** The "what" is stated but relies on the word "infraestrutura" doing significant work. A visitor who doesn't know what "programmable financial infrastructure" means (vs a payment app) gets no scaffolding. The homepage does not define "protocol" — the most strategically important noun — anywhere in visible copy.

---

**Q2. Why does BANZA exist?**

The problem section ("O que Angola precisa de ultrapassar") gives five symptom cards: cash dependence, WhatsApp proofs, apps without payments, excluded small businesses, no Angolan SDK.

**Verdict: PARTIAL.** Symptoms are named. But the structural cause is absent: Angola doesn't have a *protocol layer* for finance — it has a settlement network (EMIS/Multicaixa) and bank transfers, but no open infrastructure that any developer or operator can build on. This structural argument — the WHY for the protocol's existence — is never stated on the homepage.

---

**Q3. What problem does BANZA solve?**

Problem cards present product-level problems (no TPA, WhatsApp screenshots). The hero subheadline adds protocol-level language (operadores certificados, regras verificáveis). There is tension: the problems presented are user/merchant problems, but the solution is infrastructure-level.

**Verdict: PARTIAL.** A user reads: "BANZA solves the WhatsApp payment proof problem." The actual claim should be: "BANZA solves the missing protocol layer — the infrastructure problem that causes all the user symptoms." This second-order framing is absent.

---

**Q4. What makes BANZA different?**

The hero is followed directly by problem cards and use cases. There is no differentiation block. The manifesto quotes describe ambition ("Angola não precisa de copiar") but don't compare. The "SDK-first" section and security pipeline are product feature sections, not comparative differentiation.

**Verdict: FAIL.** No section on the homepage answers "different from what?" Payment networks (Multicaixa), fintech APIs, mobile money (M-Pesa), blockchain protocols — none are named or addressed.

---

**Q5. What role does BanzAI play?**

HomeBanzamIAEntry is embedded above the fold with: "O Sistema Operativo nativo do Protocolo Banza — para entender, integrar e evoluir o protocolo." The hero capability tags include "BanzAI."

**Verdict: PARTIAL.** The label is correct ("Sistema Operativo nativo do Protocolo Banza"). But BanzAI is introduced on the homepage primarily as a widget — not as a strategic capability. A visitor who uses the widget and gets an answer learns nothing about WHY BanzAI exists at the protocol level.

---

**Q6. Could a visitor confuse BANZA with a payment app?**

The homepage has: wallet-to-wallet visual, QR commerce visual, mobile payment mockup, use case cards for taxis / cantinas / delivery. All are product-experience frames. The word "app" appears in the capability badge: "Apps sem pagamento integrado" (a problem) and "Apps de Táxi" (a use case). The infrastructure framing is present in hero and subheadline, but 80% of visible body content describes product experience.

**Verdict: HIGH RISK.** A visitor who skims (vs reads) will finish the homepage thinking "Banzami is a QR payment app for Angola, like M-Pesa." The infrastructure/protocol layer is in the hero but drowned by product-experience sections below.

---

**Q7. Can a visitor summarise BANZA in one sentence?**

Likely output: "Banza is Angola's QR payment system." or "Banza is a programmable payment infrastructure for Angola."

The second version is closer to correct but misses: open protocol, multiple operators, certification layer.

**Verdict: PARTIAL.** One sentence possible, but at product abstraction level, not protocol level.

---

**Homepage Summary Score:**

| Question | Verdict |
|----------|---------|
| What is BANZA? | PARTIAL |
| Why does BANZA exist? | PARTIAL |
| What problem? | PARTIAL |
| What makes BANZA different? | FAIL |
| BanzAI role? | PARTIAL |
| Confusable with payment app? | HIGH RISK |
| One-sentence summary? | PARTIAL |

**Critical finding:** The homepage presents BANZA as a QR/wallet product rather than an open protocol. The infrastructure-as-protocol claim is present in one sentence but is not the dominant mental model a visitor would form.

---

## Surface 2 — Reference (`/reference`)

**Content source:** All 17 sections of `docs/BANZAMI_REFERENCE.md`

---

**Q1. What is BANZA?**

§1 opens: "Banza é infraestrutura financeira programável de código aberto para Angola." Then: "Não é um banco. Não é uma carteira digital simples. Não é uma plataforma fintech genérica adaptada de um modelo ocidental. É o protocolo que define como o dinheiro se move digitalmente em Angola — com regras imutáveis, invariantes financeiros verificáveis e uma camada de inteligência artificial que explica cada decisão do protocolo."

**Verdict: PASS.** The "what" is clearly stated in §1. This is the strongest "what" statement on the site.

---

**Q2. Why does BANZA exist?**

§2 (Princípios Fundamentais) provides six principles that imply purpose: financial correctness, protocol as product, traceability by default, Angola first. §15 (Por que Angola) names the structural opportunity: mobile penetration, informal economy, technology leapfrog.

**Verdict: PARTIAL.** The "why" is distributed across §1, §2, §15. A visitor must read 15 sections before reaching the Angola argument. There is no concentrated "why BANZA must exist" statement in §1.

---

**Q3. What problem does BANZA solve?**

§15 lists the problems: cash dependence, WhatsApp proofs, no SDK, TPA exclusion. §1 defines BANZA as the answer. §17 (Declaração de Visão) closes with the transformation narrative.

**Verdict: PASS** — for a visitor who reads all 17 sections. PARTIAL for a visitor who reads §1 only.

---

**Q4. What makes BANZA different?**

§1 has three negative statements ("Não é um banco... Não é uma carteira... Não é uma plataforma fintech genérica"). §2 has "Ferramentas determinam a verdade. A IA explica a verdade." — a key differentiator vs generic AI. §15 mentions Pix/UPI/M-Pesa in three sentences.

**Verdict: PARTIAL.** Negative definitions ("not a bank") exist but comparative analysis against specific categories (payment networks, fintech APIs, blockchain) does not. Pix/UPI/M-Pesa appear but without analysis of how BANZA is similar or different.

---

**Q5. What role does BanzAI play?**

§9 is entirely dedicated to BanzAI. The Protocol OS framing is strong. The "Por que é diferente de IA genérica" section exists. The four-layer cognitive architecture is explained.

**Verdict: PASS** — for a visitor who reads §9. The BanzAI strategic positioning is the strongest differentiation chapter in the entire reference.

---

**Q6. Could a visitor confuse BANZA with a payment app?**

§1 explicitly states "Não é uma carteira digital simples." §2's "O protocolo é o produto" principle is clear. §10 and §11 speak to developers and merchants in product terms, but §1 anchors everything.

**Verdict: LOW RISK** for a careful reader. HIGH RISK for a skimmer who jumps to §10–§12 (the product sections).

---

**Q7. Can a visitor summarise BANZA in one sentence?**

After reading §1: "Banza é o protocolo aberto que define como o dinheiro se move digitalmente em Angola — com operadores certificados, regras imutáveis e BanzAI como interface cognitiva."

**Verdict: PASS** — §1 equips a visitor for this.

---

**Reference Summary Score:**

| Question | Verdict |
|----------|---------|
| What is BANZA? | PASS |
| Why does BANZA exist? | PARTIAL |
| What problem? | PASS (§15) / PARTIAL (§1 only) |
| What makes BANZA different? | PARTIAL |
| BanzAI role? | PASS |
| Confusable with payment app? | LOW RISK |
| One-sentence summary? | PASS |

**Critical finding:** The reference is the most honest and complete positioning surface. Its weakness is density: the most critical "why BANZA, not something else" argument is distributed across sections rather than concentrated at the entry point.

---

## Surface 3 — Architecture (`/arquitectura-tecnica`)

**Content source:** §4 of BANZAMI_REFERENCE.md — dynamic section page

---

**Q1. What is BANZA?**

Section header from the reference: "Arquitectura Técnica." Body: the 18-crate Rust kernel, service topology diagram, Go services layer, PostgreSQL, event flows. The SectionHero shows "§4 — Arquitectura Técnica."

**Verdict: ABSENT.** This page assumes the visitor already knows what BANZA is. No contextual re-statement of purpose.

---

**Q2. Why does BANZA exist?**

Not addressed. The architecture section describes what was built, not why.

**Verdict: ABSENT.**

---

**Q3. What problem does BANZA solve?**

The architecture choices (immutable ledger, Rust, atomic settlement) imply the problems they solve. But no explicit statement connects kernel decisions to protocol problems.

**Verdict: ABSENT** as explicit argument. Implied through design choices.

---

**Q4. What makes BANZA different?**

No comparative statement. The Rust kernel, 18-crate separation, double-entry ledger are stated as facts, not as differentiators. A visitor doesn't know whether all payment systems work this way.

**Verdict: ABSENT.** A visitor cannot form a differentiation claim from this page alone.

---

**Q5. What role does BanzAI play?**

BanzAI does not appear in §4. The four-layer model is in §9 (BanzAI chapter), not in the architecture chapter.

**Verdict: ABSENT** from this page.

---

**Q6. Could a visitor confuse BANZA with a payment app?**

The architecture content (Rust kernel, PostgreSQL, Go services) signals infrastructure, not app. Technical visitors will correctly identify BANZA as infrastructure.

**Verdict: LOW RISK** for technical visitors. NON-TECHNICAL visitors would not reach this page.

---

**Q7. Can a visitor summarise BANZA in one sentence?**

Likely: "Banza is a payment system with an 18-crate Rust kernel." Technical but incomplete.

**Verdict: PARTIAL** — technical framing, no ecosystem frame.

---

**Architecture Summary Score:**

| Question | Verdict |
|----------|---------|
| What is BANZA? | ABSENT |
| Why does BANZA exist? | ABSENT |
| What problem? | ABSENT |
| What makes BANZA different? | ABSENT |
| BanzAI role? | ABSENT |
| Confusable with payment app? | LOW RISK (tech audience) |
| One-sentence summary? | PARTIAL |

**Critical finding:** The architecture page is entirely descriptive. It answers "what was built" but not "why this architecture choices matter" or "what this means for operators and the ecosystem." The strategic significance of the Rust kernel (correctness guarantees, immutability, determinism) is never stated.

---

## Surface 4 — Operators (`/operators`)

**Content source:** operators/page.tsx, RegistryFilters component

---

**Q1. What is BANZA?**

The page header: "Registo de Operadores Banza." Subheading: "Registo curado de operadores que implementam o protocolo Banza."

**Verdict: PARTIAL.** BANZA is implied (as "the protocol") but not defined. A visitor arriving here without prior context would know "Banza is a protocol" but nothing more.

---

**Q2. Why does BANZA exist?**

Not addressed on this page.

**Verdict: ABSENT.**

---

**Q3. What problem does BANZA solve?**

Not addressed.

**Verdict: ABSENT.**

---

**Q4. What makes BANZA different?**

The footer note mentions: "Nenhum operador pode auto-declarar certificação sem ter passado os testes." This implies a verification mechanism that distinguishes BANZA from systems where compliance is self-declared. But this is buried in a footnote.

The "Transparência de infraestrutura, não vigilância financeira" privacy framing is a genuine differentiator — and the only comparative claim on the page.

**Verdict: PARTIAL (one claim, weakly positioned).**

---

**Q5. What role does BanzAI play?**

BanzAI is not mentioned on the operators page.

**Verdict: ABSENT.**

---

**Q6. Could a visitor confuse BANZA with a payment app?**

A visitor sees a list of operators with stats (active count, Level 2+ count). The privacy notice mentions "manifests, capacidades de protocolo" — which signals infrastructure. But a visitor might still think: "This is a registry of payment service providers, like a Visa/Mastercard network."

**Verdict: MODERATE RISK.** The operator model narrative (why multiple operators on one protocol matters) is completely absent.

---

**Q7. Can a visitor summarise BANZA in one sentence?**

Likely: "Banza is a payment network with certified operators."

**Verdict: FAIL** — "payment network" is the closest mental model a visitor would form, which misses the open protocol / certification-as-mechanism dimension.

---

**Operators Summary Score:**

| Question | Verdict |
|----------|---------|
| What is BANZA? | PARTIAL |
| Why does BANZA exist? | ABSENT |
| What problem? | ABSENT |
| What makes BANZA different? | PARTIAL |
| BanzAI role? | ABSENT |
| Confusable with payment app? | MODERATE RISK |
| One-sentence summary? | FAIL |

**Critical finding:** The operators page is the natural home for the ecosystem narrative — the argument that BANZA's open certification model creates competition and resilience rather than payment monopoly. This argument is completely absent. The page reads as a technical registry, not as a strategic surface.

---

## Surface 5 — Validation (`/validacao`)

**Content source:** validacao/page.tsx, ValidationDashboard, ValidationMetrics

---

**Q1. What is BANZA?**

Hero: "Execução e Validação do Protocolo Banza." BANZA is implied as "the protocol being validated."

**Verdict: ABSENT as definition.**

---

**Q2. Why does BANZA exist?**

Not addressed.

**Verdict: ABSENT.**

---

**Q3. What problem does BANZA solve?**

Not addressed directly. A technical reader might infer: "BANZA is solving the problem of financial infrastructure for Angola, and this page tracks progress."

**Verdict: ABSENT.**

---

**Q4. What makes BANZA different?**

The validation matrix itself is a genuine differentiator: public, governance-locked, fingerprint-verified progress tracking for financial infrastructure. No other payment system publishes this level of implementation transparency. But this differentiator is never named as such.

**Verdict: ABSENT as explicit claim** — the differentiator is latent in the feature but never stated.

---

**Q5. What role does BanzAI play?**

Not mentioned on the validation page.

**Verdict: ABSENT.**

---

**Q6. Could a visitor confuse BANZA with a payment app?**

The validation content is highly technical (implementation matrix, acceptance criteria, confidence scores). A visitor would not mistake this for a payment app. But they'd also struggle to understand what they're looking at without context.

**Verdict: LOW RISK (page is too technical for casual confusion).**

---

**Q7. Can a visitor summarise BANZA in one sentence?**

Likely: "Banza is a payment system that's publicly tracking its own implementation progress."

**Verdict: PARTIAL** — technically accurate but missing the protocol-as-infrastructure framing.

---

**Validation Summary Score:**

| Question | Verdict |
|----------|---------|
| What is BANZA? | ABSENT |
| Why does BANZA exist? | ABSENT |
| What problem? | ABSENT |
| What makes BANZA different? | ABSENT (latent) |
| BanzAI role? | ABSENT |
| Confusable with payment app? | LOW RISK |
| One-sentence summary? | PARTIAL |

**Critical finding:** The validation page has an extraordinary hidden differentiator — public, governance-locked implementation tracking for financial infrastructure. No comparable payment system in Africa (or globally) publishes this. The strategic value of this transparency is never stated.

---

## Surface 6 — Roadmap (`/roadmap`)

**Content source:** roadmap/page.tsx

---

**Q1. What is BANZA?**

Subheading: "BanzAI Roadmap." The page is entirely BanzAI-specific. BANZA as protocol is mentioned only in context of "BanzAI — Protocol Operating System for the Banza protocol."

**Verdict: PARTIAL** — BANZA is implied as the protocol BanzAI operates on, but not defined.

---

**Q2. Why does BANZA exist?**

Not addressed.

**Verdict: ABSENT.**

---

**Q3. What problem does BANZA solve?**

Not addressed.

**Verdict: ABSENT.**

---

**Q4. What makes BANZA different?**

The roadmap items (Protocol Simulator, Federation Intelligence, Digital Twin, Certification Copilot) collectively suggest a system that helps operators navigate complex protocol compliance. But this is not framed as a differentiator.

**Verdict: ABSENT as explicit claim.**

---

**Q5. What role does BanzAI play?**

Strong on BanzAI identity: "Protocol Operating System." The opening banner: "Understand · Explain · Validate · Simulate · Predict · Guide." The statement: "We publish this transparently because trust begins with visibility."

**Verdict: PASS** — for BanzAI-specific positioning.

---

**Q6. Could a visitor confuse BANZA with a payment app?**

The roadmap items are sufficiently technical (vLLM, RAG pipeline, Protocol Graph, Conformance Monitoring) that a visitor would not mistake it for a payment app. But they might mistake BANZA for an AI product company, since the roadmap is entirely BanzAI-focused.

**Verdict: MODERATE RISK** — of confusing BANZA with "an AI company building payment tools" rather than "an open protocol with AI as its operating system."

---

**Q7. Can a visitor summarise BANZA in one sentence?**

Likely: "BanzAI is an AI operating system for payments." The parent protocol is invisible.

**Verdict: FAIL** — BANZA the protocol disappears behind BanzAI on this page.

---

**Roadmap Summary Score:**

| Question | Verdict |
|----------|---------|
| What is BANZA? | PARTIAL |
| Why does BANZA exist? | ABSENT |
| What problem? | ABSENT |
| What makes BANZA different? | ABSENT |
| BanzAI role? | PASS |
| Confusable with payment app? | MODERATE RISK |
| One-sentence summary? | FAIL |

**Critical finding:** The roadmap is BanzAI-only. The BANZA protocol roadmap (federation timeline, open operator certification, certification levels 3–4, carris cross-border) exists in §16 of the reference but has no dedicated public page. A visitor interested in the protocol-level future cannot find it without reading the full reference.

---

## Surface 7 — BanzAI Interface (`/banzamia`)

**Content source:** banzamia/page.tsx → BanzamIAApp (full-screen interface)

---

**Q1. What is BANZA?**

The BanzAI interface opens directly to a full-screen chat. The sidebar has module tabs. There is no landing state. No definition of BANZA or BanzAI before the interface loads.

**Verdict: ABSENT.** A visitor arrives at the interface without any framing.

---

**Q2. Why does BANZA exist?**

Not addressed in the interface.

**Verdict: ABSENT.**

---

**Q3. What problem does BANZA solve?**

The BanzAI sidebar module list (Knowledge, RFC Explorer, Certification Copilot, Graph Explorer, etc.) implies problems: operators need to understand RFCs, pass certification, explore the protocol graph. But these are tool-level problems, not strategic-level problems.

**Verdict: ABSENT as strategic frame.**

---

**Q4. What makes BANZA different?**

Absent from the interface itself. The /sobre-banzamia page (linked from footer) contains the "Por que é diferente de IA genérica" section, but visitors going to /banzamia don't see this.

**Verdict: ABSENT from the primary entry surface.**

---

**Q5. What role does BanzAI play?**

The interface title (page metadata): "BanzAI — Protocol Operating System." The description: "16 módulos. Compreender, Explicar, Validar, Simular..." This is correct and strong — but it's in metadata, not in visible content.

**Verdict: PARTIAL.** The label is correct. The strategic role is not communicated in the interface body.

---

**Q6. Could a visitor confuse BANZA with a payment app?**

The interface looks like a chat interface for payments. Without framing, a visitor could interpret BanzAI as "customer support AI for Banzami payments" rather than "Protocol Operating System."

**Verdict: HIGH RISK.** No onboarding, no landing state, no context.

---

**Q7. Can a visitor summarise BANZA in one sentence?**

After using the interface: "BanzAI is a chatbot that answers questions about Banzami payments."

**Verdict: FAIL.** The interface, without framing, reduces BanzAI to a support chatbot.

---

**BanzAI Interface Summary Score:**

| Question | Verdict |
|----------|---------|
| What is BANZA? | ABSENT |
| Why does BANZA exist? | ABSENT |
| What problem? | ABSENT |
| What makes BANZA different? | ABSENT |
| BanzAI role? | PARTIAL |
| Confusable with payment app? | HIGH RISK |
| One-sentence summary? | FAIL |

**Critical finding:** The BanzAI interface is the most powerful demonstration of a genuinely novel capability (protocol-native AI with citations and tool verification), but it delivers this capability without any framing. The /banzamia entry point is a cold drop into an interface. A visitor who doesn't already understand the protocol will leave having used a chatbot, not having understood the Protocol OS.

---

## Surface 8 — Programadores (`/banzami-para-programadores`)

**Content source:** §10 of BANZAMI_REFERENCE.md — dynamic section page

---

**Q1. What is BANZA?**

Not restated. The section opens with "Integração em horas — A superfície de integração oficial do Banza são os SDKs."

**Verdict: ABSENT** as definition. Assumes prior knowledge.

---

**Q2. Why does BANZA exist?**

Not addressed in §10.

**Verdict: ABSENT.**

---

**Q3. What problem does BANZA solve?**

Implied: developers need a payment SDK for Angola. The SDK section shows the solution. But the problem is never stated ("there was no native Angolan payment SDK").

**Verdict: PARTIAL** — solution visible, problem absent.

---

**Q4. What makes BANZA different?**

No comparative content. Why choose Banza SDK over integrating directly with EMIS/Multicaixa? Over using an international gateway? Over building a custom integration? None of these are addressed.

**Verdict: FAIL.** This is the highest-value differentiation context for a developer audience and it's absent.

---

**Q5. What role does BanzAI play?**

Not mentioned in §10.

**Verdict: ABSENT.**

---

**Q6. Could a visitor confuse BANZA with a payment app?**

SDK code examples (TypeScript, Flutter, PHP) clearly signal infrastructure. A developer would understand they're integrating a payment protocol, not downloading an app.

**Verdict: LOW RISK** for the developer audience of this page.

---

**Q7. Can a visitor summarise BANZA in one sentence?**

"Banza is a payment SDK for Angola." True but incomplete — misses protocol, operators, certification.

**Verdict: PARTIAL** — correct but too narrow.

---

**Programadores Summary Score:**

| Question | Verdict |
|----------|---------|
| What is BANZA? | ABSENT |
| Why does BANZA exist? | ABSENT |
| What problem? | PARTIAL |
| What makes BANZA different? | FAIL |
| BanzAI role? | ABSENT |
| Confusable with payment app? | LOW RISK |
| One-sentence summary? | PARTIAL |

**Critical finding:** The developer page is entirely implementation-focused. The strategic argument for why a developer should choose BANZA over alternatives — EMIS direct integration, international payment APIs, roll-your-own — is completely absent. This is the single highest-ROI missing argument for developer adoption.

---

## Surface 9 — Comerciantes (`/banzami-para-comerciantes`)

**Content source:** §11 of BANZAMI_REFERENCE.md — dynamic section page

---

**Q1. What is BANZA?**

Not defined on this page. Opens with: "Sem hardware. Sem burocracia."

**Verdict: ABSENT** as definition.

---

**Q2. Why does BANZA exist?**

Not addressed.

**Verdict: ABSENT.**

---

**Q3. What problem does BANZA solve?**

Strongly implied: TPA is expensive and bureaucratic. The solution (QR + no hardware) is prominent.

**Verdict: PARTIAL** — problem implicit in the solution framing, not named explicitly.

---

**Q4. What makes BANZA different?**

Compared to TPA/physical terminal: implicit (no hardware, no special banking contract). No comparison to other QR payment solutions, mobile money, or digital payment platforms.

**Verdict: PARTIAL** — one implicit comparison (vs TPA), zero explicit comparisons.

---

**Q5. What role does BanzAI play?**

Not mentioned.

**Verdict: ABSENT.**

---

**Q6. Could a visitor confuse BANZA with a payment app?**

"Conta Banzami Business," "QR impresso," "scan, confirmar, pago" — this page reads entirely as a product description for merchants. "BANZA is a QR payment app" is exactly the mental model this page produces.

**Verdict: HIGH RISK.** The most product-forward page on the site.

---

**Q7. Can a visitor summarise BANZA in one sentence?**

"Banzami is a QR payment system for merchants — no hardware needed."

**Verdict: FAIL** — Banzami (the product) becomes BANZA (the protocol) in this framing. A merchant leaving this page thinks the product is the whole.

---

**Comerciantes Summary Score:**

| Question | Verdict |
|----------|---------|
| What is BANZA? | ABSENT |
| Why does BANZA exist? | ABSENT |
| What problem? | PARTIAL |
| What makes BANZA different? | PARTIAL |
| BanzAI role? | ABSENT |
| Confusable with payment app? | HIGH RISK |
| One-sentence summary? | FAIL |

**Critical finding:** The merchant page is correctly focused on merchant value. But it provides zero upward framing to the protocol layer. A merchant reading this page has no way to understand that the guarantee behind the QR payment is a certified protocol, not a single company's promise.

---

## Cross-Surface Summary

| Surface | What? | Why? | Problem? | Different? | BanzAI? | App confusion risk | 1-sentence? |
|---------|-------|------|----------|-----------|---------|-------------------|-------------|
| Homepage | PARTIAL | PARTIAL | PARTIAL | FAIL | PARTIAL | HIGH | PARTIAL |
| Reference | PASS | PARTIAL | PASS | PARTIAL | PASS | LOW | PASS |
| Architecture | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | LOW | PARTIAL |
| Operators | PARTIAL | ABSENT | ABSENT | PARTIAL | ABSENT | MODERATE | FAIL |
| Validation | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | LOW | PARTIAL |
| Roadmap | PARTIAL | ABSENT | ABSENT | ABSENT | PASS | MODERATE | FAIL |
| BanzAI (interface) | ABSENT | ABSENT | ABSENT | ABSENT | PARTIAL | HIGH | FAIL |
| Programadores | ABSENT | ABSENT | PARTIAL | FAIL | ABSENT | LOW | PARTIAL |
| Comerciantes | ABSENT | ABSENT | PARTIAL | PARTIAL | ABSENT | HIGH | FAIL |

**Overall verdict:** BANZA's strategic positioning lives almost entirely in the reference document. All other public surfaces either inherit the positioning without reinforcing it or actively undermine it by defaulting to product framing.

---

*Audit completed: 2026-05-30. No modifications applied.*
