---
title: BANZA_DIFFERENTIATION_EXECUTION_PLAN
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no modifications applied
---

# BANZA Differentiation Execution Plan

**Purpose:** Prioritized, actionable plan for achieving narrative convergence across all public surfaces. Each item specifies what to change, where, and why — ordered by impact.

**Constraint:** This plan does not modify files. It specifies the changes to be made when execution is authorized.

---

## Competitor Differentiation Matrix

Before the execution plan: the full competitor analysis, since competitor framing determines messaging.

### EMIS

**What EMIS is:** Angola's interbank settlement network. Processes settlements between banks and financial institutions.

**Relationship to BANZA:** BANZA *uses* EMIS rails for final settlement (via the `acquiring` kernel crate). BANZA is not competing with EMIS — it is building the protocol layer above EMIS. BANZA makes EMIS rails accessible to any certified operator, without each operator needing a direct institutional EMIS relationship.

**Current differentiation:** ABSENT — EMIS appears only as a kernel crate name (`acquiring | Integração EMIS/Multicaixa`) and in §4 architecture references.

**Argument needed:** "EMIS is the settlement layer. BANZA is the protocol layer above it. EMIS moves money between institutions. BANZA defines the rules by which any certified operator can offer payment services, with final settlement routed through EMIS. The protocol layer is what EMIS doesn't provide."

**Where to add it:** §3 (Visão Geral do Ecossistema), architecture page, operators page footer.

**Classification now → target:** ABSENT → PARTIAL

---

### Multicaixa / TPA

**What Multicaixa is:** Angola's national card payment network. TPA (Terminal de Pagamento Automático) is the physical card terminal infrastructure.

**Relationship to BANZA:** TPA requires acquiring contracts, hardware, and high per-terminal costs — which excludes small merchants. BANZA's QR protocol requires no hardware and no acquiring contract. However, BANZA will eventually integrate acquiring (§16 Roadmap, Level 4 certification).

**Current differentiation:** WEAK — "TPA é caro e burocrático" (homepage problem card), "Sem TPA, sem contrato bancário" (Comerciantes §11). Correct, but symptom-level.

**Argument needed:** "Multicaixa/TPA requires an acquiring agreement with a bank, hardware investment, and monthly fees — creating a minimum viable merchant size. BANZA's QR protocol requires none of these because payment settlement is wallet-to-wallet: no acquiring network in the middle. This is not a feature difference. It is a structural difference in how the payment is routed."

**Where to add it:** Comerciantes page (§11), homepage problem section.

**Classification now → target:** WEAK → PARTIAL

---

### Stripe / Flutterwave / Paystack (International Fintech APIs)

**What they are:** Payment API providers. Stripe is the global standard. Flutterwave and Paystack focus on African markets.

**Relationship to BANZA:** International gateways do not support AOA (Angolan Kwanza) natively. They require card-based payment flows (IBAN, card numbers) rather than wallet-native, QR-first flows. They do not integrate with EMIS rails. An Angolan startup using Stripe would be forced into a USD-denominated flow with forex exposure, card requirement, and no local settlement guarantee.

**Current differentiation:** ABSENT — not named on any surface.

**Argument needed:** "International payment APIs do not support AOA. They require card infrastructure Angola's informal economy doesn't have. They carry USD exchange rate risk. They do not integrate with EMIS settlement rails. BANZA is Kwanza-native by protocol invariant — AOA is the only supported currency. No exchange rate. No card requirement. No institutional access barrier for developers."

**Where to add it:** Programadores page (§10), homepage developer section.

**Classification now → target:** ABSENT → PARTIAL

---

### Traditional Acquiring / Banking

**What it is:** Direct bank integration, wire transfers, bank-managed payment APIs.

**Relationship to BANZA:** Traditional acquiring requires institutional relationships. A developer cannot call a bank API without an agreement. Settlement is T+1 to T+3. Fees are policy-governed. There is no open certification — access is discretionary.

**Current differentiation:** WEAK — "Não é um banco" (§1 negation), T+0 mentioned but not compared.

**Argument needed:** "Traditional bank integration requires institutional access — a legal relationship, compliance approvals, and typically a minimum transaction volume. BANZA's certification is open: any entity that passes the conformance suite can become a certified operator. T+0 settlement is a protocol invariant, not a bank policy that can change. No institutional gatekeeping."

**Where to add it:** §1 of reference (expand the negative definition), operators page.

**Classification now → target:** WEAK → PARTIAL

---

### Blockchain / Crypto Payment Protocols

**What they are:** Ethereum-based payment rails, stablecoin payments, USDC/USDT on-chain, Layer-2 payment networks.

**Relationship to BANZA:** BANZA is not blockchain. The Rust kernel is a single-ledger, append-only system — not a distributed chain. Settlement is deterministic, not probabilistic. The currency is AOA (Kwanza) — not a token or stablecoin. BANZA operates within Angola's regulatory framework and uses EMIS rails. A sophisticated visitor familiar with Web3 could mistake BANZA's protocol language ("invariants," "certified operators," "federation," "immutable ledger") for blockchain terminology.

**Current differentiation:** ABSENT — no disambiguation anywhere.

**Argument needed:** "BANZA is not blockchain. There is no token, no chain, no crypto exposure. The BANZA ledger is a single Rust kernel — deterministic, immediate, AOA-denominated. Finality is instant and absolute, not probabilistic. Settlement uses EMIS rails — Angola's existing banking infrastructure. BANZA operates within, not outside, Angola's regulatory framework."

**Where to add it:** §1 of reference (brief disambiguation), about/FAQ section if created.

**Classification now → target:** ABSENT → PARTIAL

---

### M-Pesa (Closed Mobile Money)

**What it is:** Safaricom/Vodacom's mobile money network, dominant in Kenya and several African markets.

**Relationship to BANZA:** M-Pesa is the most common "comparable" a visitor might reach for. It is the wrong comparison. M-Pesa is a closed, operator-controlled system — Safaricom owns the protocol, the rules, and the access. No independent company can "implement M-Pesa." BANZA is an open protocol — any certified entity can implement it. The distinction between closed mobile money (M-Pesa model) and open payment protocol (Pix/UPI model) is the most important single concept for understanding BANZA's design philosophy.

**Current differentiation:** ABSENT as comparison — named in §15 but not contrasted with BANZA.

**Argument needed:** "M-Pesa is a closed network: Safaricom defines the rules, controls access, and no independent company can implement it. BANZA follows the open protocol model — any certified entity can operate, the rules are public, and the protocol survives any single operator leaving. Banzami is one operator on BANZA, the same way PhonePe is one app on UPI. The protocol, not the operator, is the product."

**Where to add it:** §15 of reference (expand the Pix/UPI/M-Pesa comparison), homepage (new section or callout).

**Classification now → target:** ABSENT → STRONG

---

### Pix (Open Payment Protocol — Brazil)

**What it is:** Brazil's open payment protocol, launched by the Central Bank of Brazil in 2020.

**Relationship to BANZA:** Pix is the closest structural analogue to BANZA. Both are open protocol standards. Both enable multiple operators (banks, fintechs) to implement the same payment interface and interoperate. Pix is the proof that the model works at national scale.

**Current differentiation:** ABSENT as comparison — named in §15 but not explained or compared.

**Argument needed:** Full Pix/UPI comparison as developed in BANZA_CORE_THESIS_REPORT.md. BANZA = Pix model (open protocol), not M-Pesa model (closed operator).

**Where to add it:** §15 (full expansion), homepage (dedicated section or callout).

**Classification now → target:** ABSENT → STRONG

---

### UPI (Open Payment Protocol — India)

**Same analysis as Pix.** UPI is the other structural analogue. Both support the argument.

**Classification now → target:** ABSENT → STRONG

---

## Execution Tiers

### Tier 0 — Core Thesis Insertion (Maximum impact, surgical scope)

These are the changes that establish the canonical thesis where it is completely absent. They require new copy, not rewrites of existing copy.

**T0-001 — Homepage: Add "Protocol Layer" section**

Add one section to the homepage between the ManifestoQuote and the problem cards. This section establishes WHY the protocol must exist before showing what the symptoms are.

Estimated scope: 1 new React section (~30 lines TSX, 4 sentences of copy).

Content model:
```
Eyebrow: "A camada que falta"
H2: "Angola tem as peças. Falta o protocolo."
Body: [3-4 sentences establishing the gap]
Supporting visual: Simple three-column diagram:
  "EMIS + Bancos" | ← gap → | "Apps e Wallets"
                  "BANZA"
```

**T0-002 — Homepage: Reframe problem cards**

Add one sentence before the 5 problem cards that names them as symptoms of the protocol gap, not as independent problems. This requires no structural change — one `<p>` element before the grid.

Content model: "Cinco sintomas. Uma causa: Angola não tem uma camada de protocolo aberta que qualquer programador, operador ou instituição possa usar."

**T0-003 — Operators page: Add protocol narrative paragraph**

Replace the current hero body ("Registo curado de operadores que implementam o protocolo Banza.") with a version that explains WHY the operator model exists.

Content model: "BANZA é um protocolo aberto: qualquer entidade que passe o conformance suite pode tornar-se operador certificado. Esta é a diferença estrutural face a redes fechadas. O registo abaixo mostra quem já certificou."

**T0-004 — BanzAI interface: Add landing state**

Before the full-screen interface loads, show a 3-second landing state that names BanzAI as the Protocol OS and distinguishes it from a chatbot.

Content model:
```
Title: "BanzAI — Protocol Operating System"
Subtitle: "O protocolo explica-se a si mesmo."
Line: "Ferramentas determinam a verdade. A IA explica a verdade."
Capability tags: [Compreender] [Explicar] [Validar] [Simular] [Certificar] [Federar]
CTA: "Abrir interface →" (or auto-opens after 2s)
```

Alternatively (simpler): a persistent banner at the top of the BanzAI interface — 1 line identifying it as Protocol OS, linking to /sobre-banzamia.

---

### Tier 1 — Differentiation Layer (High impact, targeted copy changes)

**T1-001 — §15 Reference: Expand the Pix/UPI/M-Pesa comparison**

The current three-sentence mention becomes a structured comparison. Three subsections:
1. "O modelo que funciona" — what Pix and UPI are (open protocols, multiple operators, interoperability)
2. "O que o BANZA não é" — M-Pesa is a closed operator network; BANZA is an open protocol
3. "O que o BANZA é" — Angola's Pix equivalent: rules, not product; protocol, not operator

Estimated scope: Replace 3 sentences with ~200 words + possibly the existing banzami-canonical-architecture.svg diagram reframed.

**T1-002 — §1 Reference: Expand negative definitions to structural argument**

Current: "Não é um banco. Não é uma carteira digital simples. Não é uma plataforma fintech genérica."

Add after: "Existe porque nenhuma destas coisas preenche o que Angola precisa: uma camada de protocolo aberta — regras certificadas que qualquer operador, programador ou instituição pode adoptar sem negociar acesso a uma rede fechada."

Estimated scope: 2-3 sentences appended to existing paragraph.

**T1-003 — Programadores page: Add developer differentiation preface**

Before the SDK table, add 3-4 sentences explaining why BANZA is the right choice for an Angolan developer, naming the alternatives by category (not necessarily by brand name) and explaining why they fail.

**T1-004 — Validation page: Add strategic frame to hero**

Add 2 sentences to the validation hero explaining that public implementation tracking is a protocol transparency principle — not just a dashboard feature.

**T1-005 — Roadmap page: Add BANZA protocol track**

Create a second section in /roadmap showing the BANZA protocol roadmap (from §16 of the reference): federation milestones, open operators, acquiring integration. Label the existing content "BanzAI Roadmap" and the new section "BANZA Protocol Roadmap."

---

### Tier 2 — Supporting Narrative (Medium scope, medium impact)

**T2-001 — Architecture page (§4): Add strategic frame**

Add a brief intro paragraph before the kernel table: 4-5 sentences explaining why the Rust kernel, 18-crate separation, immutable ledger, and PostgreSQL choices matter strategically — not just technically.

**T2-002 — Comerciantes page (§11): Add protocol attribution for T+0**

Add one sentence attributing T+0 settlement to the protocol invariant, not to Banzami policy: "A liquidação T+0 é um invariante do protocolo Banza — não uma política do Banzami."

**T2-003 — §1 Reference: Add blockchain disambiguation**

2 sentences, after the negative definitions: "O BANZA não é blockchain. Não há tokens, não há cadeia distribuída, não há criptomoeda. O ledger é um sistema Rust determinístico com liquidação atómica em Kwanza, integrado nos carris EMIS."

**T2-004 — Homepage closing ManifestoQuote: Reframe**

The closing quote ("O QR torna-se o terminal. O telemóvel torna-se a carteira.") makes QR and wallet the protagonists. Replace or supplement with a quote that names the protocol as the enabling layer.

**T2-005 — Operators page footer: Reframe conformance note**

Current: "Nenhum operador pode auto-declarar certificação sem ter passado os testes."

Add: "Isso inclui o Banzami. O protocolo aplica as mesmas regras a todos os participantes — o que distingue uma rede de protocolo aberta de uma rede controlada por um único operador."

**T2-006 — Sobre-banzamia: Link from /banzamia header or sidebar**

The /banzamia interface currently has no link to /sobre-banzamia. Adding a "Sobre o BanzAI →" link in the interface header or sidebar is a navigational fix with significant strategic impact.

---

### Tier 3 — Structural Additions (New pages or major new sections)

**T3-001 — Create /protocolo page (or expand /o-que-e-o-banza)**

A dedicated page that contains the canonical thesis in full:
- The protocol layer argument
- The Pix/UPI/M-Pesa comparison (fully developed)
- The three-tier hierarchy with visual
- The "why operators matter" argument
- The "why certification matters" argument

This page becomes the authoritative answer to "What is BANZA and why does it exist?" It can be linked from the homepage hero, the operators page, and the footer.

**T3-002 — Create /operador-certificado page**

A page that speaks directly to potential operators (not existing operators, not developers). Explains:
- What certification means
- Who can certify (any qualified entity)
- What certification unlocks (access to EMIS rails, BanzAI tooling, federation network)
- How to start (Certification Level 0 sandbox)
- Why certify now (federation interoperability with all future operators)

**T3-003 — Add "Por que não X" section to Programadores**

A structured comparison section for developers: "Why BANZA instead of [category]?" with responses to the four main alternatives (international gateway, bank API, EMIS direct, roll-your-own). Does not need to name specific brands — category-level comparison is sufficient.

---

## Execution Order

### Phase 1 — Core thesis installed (Tier 0, ~1 week)

Priority: Maximum narrative impact, minimum scope.

1. T0-001 — Homepage: Protocol Layer section (new section, 30 lines TSX)
2. T0-002 — Homepage: Problem cards reframe (1 sentence, ~5 lines)
3. T0-003 — Operators page: Protocol narrative paragraph (replace hero body)
4. T0-004 — BanzAI interface: Landing state or persistent banner

After Phase 1, a visitor spending 30 seconds on the homepage will encounter the canonical thesis. A visitor going to /banzamia will understand what they are using before they use it.

### Phase 2 — Differentiation installed (Tier 1, ~1 week)

Priority: High-value competitive differentiation, targeted changes.

5. T1-001 — §15 Reference: Pix/UPI/M-Pesa full comparison
6. T1-002 — §1 Reference: Structural gap argument
7. T1-003 — Programadores: Developer differentiation preface
8. T1-004 — Validation: Strategic frame
9. T1-005 — Roadmap: BANZA protocol track

After Phase 2, every primary surface has some version of the canonical thesis. Competitor comparisons exist in the reference.

### Phase 3 — Supporting narrative (Tier 2, ~1 week)

Priority: Closing remaining gaps, precision improvements.

10. T2-001 — Architecture: Strategic frame
11. T2-002 — Comerciantes: Protocol attribution for T+0
12. T2-003 — §1: Blockchain disambiguation
13. T2-004 — Homepage closing quote: Reframe
14. T2-005 — Operators footer: Conformance framing
15. T2-006 — /banzamia to /sobre-banzamia link

### Phase 4 — Structural additions (Tier 3, ~2 weeks)

Priority: Long-term strategic value, new page creation.

16. T3-001 — /protocolo page (or /o-que-e-o-banza expansion)
17. T3-002 — /operador-certificado page
18. T3-003 — "Por que não X" for developers

---

## Per-Change Success Criteria

| Change | Success condition |
|--------|-----------------|
| T0-001 | Homepage visitor can name the "protocol layer gap" after reading one section |
| T0-002 | Problem cards read as symptoms of one structural gap, not five product problems |
| T0-003 | Operators page visitor understands WHY operators exist before seeing the list |
| T0-004 | BanzAI visitor knows it is a Protocol OS, not a chatbot, before using the interface |
| T1-001 | §15 visitor understands BANZA = Pix model (open), not M-Pesa model (closed) |
| T1-002 | §1 visitor understands the structural argument, not just the negative definitions |
| T1-003 | Developer visitor has "why BANZA, not X" answered before seeing any code |
| T1-004 | Validation page visitor knows public tracking is a protocol principle |
| T1-005 | Roadmap visitor sees BANZA protocol future, not only BanzAI future |
| T2-001 | Architecture page explains why these choices matter for the protocol |
| T2-002 | Merchant visitor understands T+0 is protocol-guaranteed, not company policy |
| T2-003 | No visitor can confuse BANZA with blockchain |
| T2-004 | Homepage closing quote names the protocol as the protagonist |
| T2-005 | Conformance note reinforces open protocol equality |
| T2-006 | BanzAI interface has a navigation path to Protocol OS explanation |
| T3-001 | A single URL answers "What is BANZA and why does it exist?" completely |
| T3-002 | A potential operator can find the complete case for certification in one place |
| T3-003 | Developers have a structured "why BANZA" before any SDK documentation |

---

## Final Success Condition

After all phases, a visitor spending 30 seconds on any public surface should be able to leave saying:

> "BANZA is the open protocol layer Angola lacks. Like Pix built Brazil's and UPI built India's payment ecosystems on open protocols — BANZA is building Angola's. BanzAI is the operating system that makes the protocol navigable. Banzami is the reference implementation that proves it works."

Currently, that statement requires reading three different URLs across thousands of lines.

The target is: any 30-second visit to any surface.

---

*Plan created: 2026-05-30. No modifications applied.*
