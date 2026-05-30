---
title: BANZA_REFERENCE_V2_BLUEPRINT
version: 1.0
date: 2026-05-30
status: DESIGN COMPLETE — pending execution authorization
---

# BANZA Reference V2 Blueprint

**Purpose:** Define the complete structural and narrative architecture of BANZAMI_REFERENCE.md V2. Every section specified by: name, purpose, key message, required diagrams, expected visitor takeaway, and narrative flow into the next section.

**Design constraint:** The canonical narrative hierarchy governs section order:

```
Problem → Protocol Gap → BANZA → Certification → Federation
→ BanzAI → Operators → Banzami → Technology
```

**Validation rule applied to every section:**
> "Could BANZA still exist if Banzami disappeared?"
> YES → section belongs before §12 (Banzami). NO → section belongs at or after §12.

---

## V2 Section Map Overview

```
PARTE I — O PROTOCOLO
  §1   O Problema: Angola Tem as Peças
  §2   A Camada que Falta
  §3   O que é o BANZA
  §4   Governança do Protocolo
  §5   Modelo de Certificação
  §6   Regras do Protocolo — Especificações Técnicas
  §7   Federação

PARTE II — O SISTEMA OPERATIVO
  §8   O Problema do Conhecimento do Protocolo
  §9   BanzAI

PARTE III — OS OPERADORES
  §10  O Modelo de Operadores

PARTE IV — BANZAMI
  §11  Banzami — A Implementação de Referência
  §12  Para Programadores
  §13  Para Comerciantes
  §14  Para Consumidores
  §15  Arquitectura Técnica de Referência
  §16  Sandbox e Ambiente de Testes
  §17  Roadmap
  §18  Declaração de Visão
```

**Validation rule check:**

| § | Section | BANZA survives Banzami? | Position verdict |
|---|---------|------------------------|-----------------|
| 1 | O Problema | YES | Before Banzami ✓ |
| 2 | A Camada que Falta | YES | Before Banzami ✓ |
| 3 | O que é o BANZA | YES | Before Banzami ✓ |
| 4 | Governança | YES | Before Banzami ✓ |
| 5 | Certificação | YES | Before Banzami ✓ |
| 6 | Especificações Técnicas do Protocolo | YES | Before Banzami ✓ |
| 7 | Federação | YES | Before Banzami ✓ |
| 8 | Problema do Conhecimento | YES | Before Banzami ✓ |
| 9 | BanzAI | YES | Before Banzami ✓ |
| 10 | Modelo de Operadores | YES | Before Banzami ✓ |
| 11 | Banzami (reference impl.) | NO — Banzami IS this section | Banzami line |
| 12 | Para Programadores | NO — Banzami SDK | After Banzami ✓ |
| 13 | Para Comerciantes | NO — Banzami products | After Banzami ✓ |
| 14 | Para Consumidores | NO — Banzami Wallet | After Banzami ✓ |
| 15 | Arquitectura Técnica | NO — Banzami implementation | After Banzami ✓ |
| 16 | Sandbox | NO — Banzami sandbox | After Banzami ✓ |
| 17 | Roadmap | SPLIT — Protocol track before, Banzami track after | After Banzami ✓* |
| 18 | Declaração de Visão | YES — ecosystem vision | End ✓ |

*Roadmap has two tracks. In V2 both are consolidated into a single section after §11, clearly separated as BANZA Protocol Track and Banzami Product Track.

---

## PARTE I — O PROTOCOLO

---

### §1 — O Problema: Angola Tem as Peças

**ID:** V2-S01
**V1 equivalent:** §15 (currently section 15 of 17) — RELOCATED from near-last to first.

---

**PURPOSE**

Establish the structural problem before introducing any solution. The reader must understand that Angola's payment gap is not a banking gap, not a technology gap, and not a fintech gap — it is a *protocol gap*. This section makes the gap visible, names its consequences, and creates the question that the entire rest of the reference answers.

The section must NOT introduce BANZA by name until its final paragraph. The reader should feel the gap before they receive the answer.

---

**KEY MESSAGE**

Angola already has the ingredients of a digital payment economy. Settlement rails exist (EMIS). Banks exist. Payment products exist. Consumer demand exists. What Angola does not have is the layer that connects them: an open protocol layer that any developer can build on, any operator can implement, and any institution can join without negotiating closed access to a proprietary network.

---

**REQUIRED CONTENT BLOCKS**

1. **"Angola já tem" inventory** — explicit list of what Angola has:
   - EMIS interbank settlement rails
   - 23 licensed commercial banks
   - Growing smartphone penetration
   - A large informal economy with real appetite for digital commerce
   - Payment apps and digital banking products

2. **"O que Angola não tem" argument** — the structural gap:
   - An open protocol layer: public rules any developer can read
   - Open certification: any entity that passes conformance can operate
   - Verifiable invariants: financial correctness enforced by rules, not promised by a bank
   - Interoperability: wallets in different apps cannot currently exchange value
   - Protocol-level settlement guarantees (vs. bank-policy-level promises)

3. **Symptom → Cause mapping** — the 5 visible symptoms are ONE structural cause:
   - A developer cannot build payment features without a proprietary bank agreement → protocol gap
   - A fintech cannot process payments without becoming a bank → protocol gap
   - WhatsApp screenshots are used as payment proof → no open verification layer → protocol gap
   - Merchants cannot receive digital payments without TPA contracts → protocol gap
   - International payment APIs do not support AOA → no sovereign protocol layer → protocol gap

4. **Closing paragraph** — names BANZA as the answer (no details yet):
   > "Este é o vazio que o BANZA preenche. Não como banco. Não como produto fintech. Como protocolo."

---

**REQUIRED DIAGRAMS**

- **Diagram V2-D01:** The three-layer stack:
  ```
  ┌─────────────────────────────────┐
  │      APPS E PRODUTOS            │  ← wallets, payment apps
  ├─────────────────────────────────┤
  │      [CAMADA EM FALTA]          │  ← the gap — highlight this
  │      protocolo aberto           │
  │      certificação               │
  │      interoperabilidade         │
  ├─────────────────────────────────┤
  │      EMIS / RAILS DE            │  ← interbank settlement
  │      LIQUIDAÇÃO                 │
  └─────────────────────────────────┘
  ```
  This diagram must show the gap in the middle as the structural missing element.

---

**EXPECTED VISITOR TAKEAWAY**

After reading §1, a visitor must be able to say:

> "Angola has banks, settlement infrastructure, and payment apps. But there is no open protocol layer connecting them — no public rules any developer can build on, no open certification for operators, no interoperability between wallets. Those 5 symptoms I see on the website are all the same root problem: the missing protocol layer."

---

**NARRATIVE FLOW INTO §2**

End §1 with: "BANZA é essa camada. Mas o que é, exactamente, uma camada de protocolo?"

§2 answers this question directly.

---

---

### §2 — A Camada que Falta

**ID:** V2-S02
**V1 equivalent:** No direct equivalent. The "protocol layer" argument is assembled from fragments in §1, §2, §3, §15 of V1. This section is NEW — it assembles the full argument.

---

**PURPOSE**

Define what a "protocol layer" is. Distinguish it from a bank, a payment product, a gateway, and a closed operator network. Introduce the Pix/UPI/M-Pesa comparison as the primary frame for understanding what BANZA is and is not.

This section answers the question "What is a protocol layer?" so that §3 can answer "What is BANZA?" without the reader needing to already know what a protocol is.

---

**KEY MESSAGE**

A protocol layer is not a product. A protocol layer is a set of open, public rules that any developer can read, any operator can implement, and any regulator can audit. The protocol is what Pix is for Brazil and UPI is for India — not M-Pesa, which is a closed operator product. BANZA follows the Pix/UPI model.

---

**REQUIRED CONTENT BLOCKS**

1. **"O que é uma camada de protocolo"** — plain definition:
   - Open, public rules (not a closed API)
   - Certification open to any entity (not institutional gatekeeping)
   - Interoperability by design (any certified operator can exchange value)
   - Rules enforced at the protocol level (not promised by a company)

2. **Pix / UPI / M-Pesa comparison** — full structural analysis:
   - **Pix (Brazil, 2020):** BCB created an open protocol. Nubank, GPay, Itaú all implement Pix. The protocol unified them. Pix is not a product. Any certified entity implements it.
   - **UPI (India, 2016):** NPCI created the protocol. PhonePe, Google Pay, Paytm all implement UPI. Billions of transactions monthly. No single company owns UPI.
   - **M-Pesa (Kenya):** Safaricom/Vodacom own and operate M-Pesa. Other companies integrate with M-Pesa's proprietary API. When Safaricom changes terms, every merchant and user is subject to that decision. M-Pesa is a product, not a protocol.
   - **BANZA:** Follows the Pix/UPI model, not M-Pesa. Open RFCs. Open certification. Banzami is the reference operator — not the owner of the protocol.

3. **"Por que a distinção importa enormemente"**:
   - M-Pesa model: if Banzami stopped operating, the protocol disappears.
   - Pix/UPI model: if Banzami stopped operating, other certified operators continue. The protocol survives any single operator.
   - This is why BANZA is infrastructure. Banzami is not.

4. **Angola has the preconditions** — same as Pix/UPI did in 2016/2020:
   - Growing smartphone penetration
   - Underbanked informal economy
   - Real appetite for digital commerce
   - Existing settlement rails (EMIS)
   - Window of opportunity: the protocol layer does not yet exist

---

**REQUIRED DIAGRAMS**

- **Diagram V2-D02:** Protocol model comparison:
  ```
  PIX / UPI MODEL (open)        M-PESA MODEL (closed)
  ──────────────────────        ─────────────────────
  NPCI / BCB                    SAFARICOM
  (protocol governance)         (operator + owner)
        │                              │
   Open Protocol                 Proprietary API
        │                              │
  ┌─────┴─────┐               ┌────────┴────────┐
  │  GPay     │               │  Merchant A      │
  │  Nubank   │               │  Merchant B      │
  │  Itaú     │               │  (all dependent) │
  └───────────┘               └─────────────────┘

  BANZA follows the PIX/UPI model.
  ```

---

**EXPECTED VISITOR TAKEAWAY**

> "A protocol layer is open rules any developer can build on. Pix did this for Brazil. UPI did this for India. BANZA is doing it for Angola — following the Pix/UPI open model, not the M-Pesa closed model. If Banzami stopped operating, the BANZA protocol would continue."

---

**NARRATIVE FLOW INTO §3**

End §2 with: "Agora que sabemos o que é uma camada de protocolo e por que Angola precisa dela — o que é o BANZA, exactamente?"

---

---

### §3 — O que é o BANZA

**ID:** V2-S03
**V1 equivalent:** §1 (restructured and reframed)

---

**PURPOSE**

Provide the complete canonical definition of BANZA as a three-tier ecosystem. This is the section a visitor references when asked "What is BANZA?" It must include: the three-tier hierarchy, the four protocol principles, the three-tier diagram, and the canonical identity distinctions (not a bank, not a product, not a gateway).

---

**KEY MESSAGE**

BANZA is the open protocol layer Angola lacks. It defines how money moves digitally in Angola through open rules, certified operators, and verifiable invariants. BanzAI is its operating system. Banzami is its reference implementation.

---

**REQUIRED CONTENT BLOCKS**

1. **One-sentence canonical definition**:
   > "BANZA é o protocolo aberto que Angola não tem — a infraestrutura certificada que qualquer programador, operador ou instituição pode usar para construir, da mesma forma que o Pix construiu o ecossistema de pagamentos do Brasil e o UPI construiu o da Índia."

2. **Three-tier hierarchy** with the SVG diagram (already rebuilt in ADR-025 execution):
   - BANZA: the protocol layer (open rules, certified operators, verifiable invariants)
   - BanzAI: the Protocol Operating System (makes the protocol navigable at scale)
   - Banzami: the reference implementation (proves the protocol works; one operator among future many)

3. **Identity distinctions** (negative + positive):
   - Não é um banco → é um protocolo que qualquer operador pode implementar
   - Não é um produto fintech → é a infraestrutura na qual produtos são construídos
   - Não é uma API fechada → é um conjunto de regras públicas que qualquer programador pode ler
   - Não é a M-Pesa → é Pix/UPI (protocol-first, not operator-first)

4. **Four protocol principles** — framed as protocol invariants (not product features):
   | Princípio | O que significa para o protocolo |
   |-----------|----------------------------------|
   | Wallet-native | Cada conta é uma carteira em Kwanza. Sem IBAN. Sem código bancário. Qualquer operador certificado implementa isto. |
   | QR-native | QR é a superfície primária de pagamento do protocolo. Sem terminal. Qualquer operador certificado expõe isto. |
   | Programmable | Integração via SDK em horas. SDK-first é um requisito do protocolo. Qualquer operador certificado expõe esta superfície. |
   | Instant settlement | T+0 é um invariante do protocolo — não uma promessa de produto. Verificável no kernel. |

5. **The name** — Angola etymology (from current §1, preserved)

---

**REQUIRED DIAGRAMS**

- **Diagram V2-D03:** Three-tier SVG (existing `brand-architecture.svg` — already ADR-025 aligned)
- **Diagram V2-D04:** "Como o protocolo funciona" — the canonical flow: Developer/Operator reads spec → implements → passes conformance → becomes certified → serves consumers

---

**EXPECTED VISITOR TAKEAWAY**

> "BANZA is not a payment app. It is the open protocol layer that Angola's payment ecosystem needs. BanzAI is the operating system of that protocol. Banzami is the reference implementation that proves it works. Any certified operator can build on BANZA — without institutional access."

---

**NARRATIVE FLOW INTO §4**

End §3 with: "Um protocolo aberto precisa de governança aberta. Como é que o BANZA garante que as regras permanecem públicas e verificáveis?"

---

---

### §4 — Governança do Protocolo

**ID:** V2-S04
**V1 equivalent:** §6 (Governança) — RELOCATED from §6 to §4.

---

**PURPOSE**

Explain how the BANZA protocol is governed. Why governance comes before technology. The protocol's trustworthiness depends on its governance model — open RFCs, public ADRs, the validation matrix. This section establishes that BANZA's rules cannot be changed unilaterally by any single operator, including Banzami.

---

**KEY MESSAGE**

The BANZA protocol is governed by public RFCs and ADRs that any entity can read, propose changes to, and audit. No single operator — including Banzami — can change the protocol unilaterally. Governance is what makes the protocol infrastructure, not a product.

---

**REQUIRED CONTENT BLOCKS**

1. **RFCs** — what they are, how they work, where to find them
2. **ADRs** — what they are, the canonical list, ADR-025 as current primary
3. **Validation Matrix** — what it is, how it enforces protocol correctness
4. **Validation domains** — the 7 domains
5. **"Por que a governança vem antes da tecnologia"** — new framing argument:
   > "Num produto, a arquitectura é interna. Num protocolo, a arquitectura é a lei. A governança define o que qualquer operador deve implementar. A tecnologia descreve como a implementação de referência o fez. Nesta referência, a governança vem antes da tecnologia porque o protocolo vem antes de qualquer operador."

---

**REQUIRED DIAGRAMS**

- **Diagram V2-D05:** Governance flow: RFC proposed → community review → ADR ratified → enters protocol spec → validation matrix updated → operators must conform

---

**EXPECTED VISITOR TAKEAWAY**

> "BANZA is governed by public RFCs and ADRs. No single company changes the protocol. The validation matrix enforces correctness. I can read every rule and every decision."

---

**NARRATIVE FLOW INTO §5**

End §4 with: "A governança define as regras. A certificação garante que qualquer operador as implementou correctamente."

---

---

### §5 — Modelo de Certificação

**ID:** V2-S05
**V1 equivalent:** §7 (Modelo de Certificação) — RELOCATED from §7 to §5.

---

**PURPOSE**

Explain the open certification model. The certification model is what makes BANZA an open protocol rather than a closed network. Any entity that passes the conformance suite can become a certified operator — no institutional gatekeeping, no bilateral agreements, no minimum transaction volume.

---

**KEY MESSAGE**

BANZA's certification is open: any entity that passes the conformance suite becomes a certified operator. This is the structural difference from traditional acquiring (which requires institutional relationships) and from closed operator networks (which require proprietary agreements). Open certification is how the protocol achieves ecosystem scale.

---

**REQUIRED CONTENT BLOCKS**

1. **What certification is** — the conformance suite, what it tests, what it certifies
2. **Certification levels** (L1 through L4 — from current §7)
3. **Who can certify** — explicitly: any legal entity, no institutional access requirement
4. **Certification process** — the steps
5. **Operator Manifesto** — the public commitment certified operators make
6. **Maintenance** — how certification is maintained over time
7. **Structural comparison** to traditional access:
   - Traditional bank API: requires legal agreement, compliance approval, minimum volume → excludes startups
   - BANZA certification: requires passing the conformance suite → any entity qualifies

---

**REQUIRED DIAGRAMS**

- **Diagram V2-D06:** Certification path: Entity → Reads spec → Implements → Runs conformance suite → Passes → Certified Operator → Joins operator registry → Serves users

---

**EXPECTED VISITOR TAKEAWAY**

> "Any company that passes the BANZA conformance suite becomes a certified operator. No institutional gatekeeping. No bilateral agreement. Open certification is what makes BANZA a protocol, not a product."

---

**NARRATIVE FLOW INTO §6**

End §5 with: "A certificação verifica que o operador implementou as regras. Quais são essas regras, exactamente?"

---

---

### §6 — Regras do Protocolo — Especificações Técnicas

**ID:** V2-S06
**V1 equivalent:** §4 (Arquitectura Técnica) + §5 (Representação Monetária) — SPLIT and REFRAMED.

**What moves here vs. §15 (Arquitectura Técnica de Referência):**
- **§6 (here):** Protocol-level specifications that apply to ALL operators. These are the rules.
- **§15 (later):** Banzami-specific implementation details. This is how Banzami implements the rules.

---

**PURPOSE**

Define the technical rules of the protocol: monetary representation, financial invariants, ledger model, settlement semantics. These are not Banzami's implementation choices — they are protocol invariants that any operator must implement correctly to become certified.

---

**KEY MESSAGE**

These are the technical rules of the BANZA protocol. They apply to every certified operator, not just Banzami. Financial correctness is enforced by the kernel, not promised by a company. Every invariant is verifiable.

---

**REQUIRED CONTENT BLOCKS**

1. **Framing paragraph** — explicitly state: "As especificações desta secção aplicam-se a qualquer operador certificado Banza. O Banzami implementa-as — mas não as define. São definidas pelo protocolo."

2. **Representação Monetária** (from current §5 — preserved in full):
   - Regra de inteiros
   - Convenção `*_minor`
   - Semântica de montantes
   - Regra MON-001 + CONFORMANCE-MON-001

3. **Invariantes Financeiros** (from current §4 — key protocol invariants):
   - Double-entry ledger model
   - The financial invariants that any operator must preserve
   - Conservation laws

4. **Liquidação T+0** — as a protocol invariant (not a product feature):
   > "T+0 não é uma promessa de produto. É um invariante do protocolo. Qualquer transacção Banza que complete o ciclo de confirmação liquida no mesmo instante. Isto não pode ser alterado por um operador sem perder a certificação."

5. **Sistema de rastreabilidade** — as a protocol requirement (not a Banzami feature)

---

**REQUIRED DIAGRAMS**

- **Diagram V2-D07:** Double-entry ledger model (from current §4 — preserved)
- **Diagram V2-D08:** Financial invariants: conservation of value through the payment lifecycle

---

**EXPECTED VISITOR TAKEAWAY**

> "The BANZA protocol has specific technical rules: integer-only monetary representation, double-entry ledger, T+0 settlement as an invariant. Every certified operator must implement these. These rules are what make BANZA financially verifiable — not just trustworthy by reputation."

---

**NARRATIVE FLOW INTO §7**

End §6 with: "As regras do protocolo definem o presente. A federação define o futuro — como operadores certificados poderão eventualmente comunicar entre si."

---

---

### §7 — Federação

**ID:** V2-S07
**V1 equivalent:** §8 (Federação) — RELOCATED from §8 to §7.

---

**PURPOSE**

Explain the federation architecture. Federation is the protocol's long-term interoperability model. It is what distinguishes BANZA from a single-operator system: multiple certified operators that can route payments between each other without bilateral agreements. This section exists before Banzami because federation exists independently of Banzami.

---

**KEY MESSAGE**

Federation is how multiple certified operators exchange value without bilateral agreements. A wallet with Operator A can pay a wallet with Operator B — because both implement the same open protocol. Federation is proof that BANZA is infrastructure, not a product: it only makes sense if there are multiple operators.

---

**REQUIRED CONTENT BLOCKS**

1. **What federation is** — and why it requires multiple certified operators
2. **Current state** — federation is in design phase; the architecture is defined
3. **Federation architecture** — the planned routing model
4. **Federation roadmap** — from current §8
5. **Why federation proves BANZA is infrastructure**:
   > "Um produto não se federa. Uma carteira digital não se federa com outra carteira digital — cada um tem os seus utilizadores presos na sua rede. Um protocolo federa-se. Quando dois operadores certificados Banza implementam as mesmas regras abertas, os seus utilizadores podem transaccionar entre si — sem acordo bilateral, sem API proprietária."

---

**REQUIRED DIAGRAMS**

- **Diagram V2-D09:** Federation topology: Operator A ↔ BANZA Federation Layer ↔ Operator B — consumers on each side can transact

---

**EXPECTED VISITOR TAKEAWAY**

> "Federation means multiple certified operators can route payments between each other. A BANZA wallet from one operator can pay a BANZA wallet from another — because both implement the same open protocol. Federation is why BANZA is infrastructure."

---

**NARRATIVE FLOW INTO §8**

End §7 with: "O protocolo define as regras. A certificação garante a sua implementação. A federação garante a interoperabilidade. Mas um protocolo que ninguém consegue navegar não escala. É aqui que entra o BanzAI."

---

---

## PARTE II — O SISTEMA OPERATIVO

---

### §8 — O Problema do Conhecimento do Protocolo

**ID:** V2-S08
**V1 equivalent:** §9 subsection "O Fosso de Conhecimento do Protocolo" + "O que acontece sem BanzAI" — ELEVATED to its own section.

---

**PURPOSE**

Establish the problem that BanzAI solves before introducing BanzAI. A protocol is only as powerful as its adoption. Adoption requires understanding. Understanding at scale requires a cognitive layer. This section creates the question that §9 answers.

---

**KEY MESSAGE**

Protocols are hard to adopt at scale because they are dense, technical, and vast. Every new operator needs to understand thousands of pages of spec. Every developer needs to find the right invariant. Every regulator needs to audit compliance. Without a cognitive layer, more operators means more human support burden — and the protocol fails to scale.

---

**REQUIRED CONTENT BLOCKS**

1. **The protocol knowledge problem** — why protocols create an adoption bottleneck at scale
2. **What happens without BanzAI** — concrete consequences: operator support load, certification friction, developer confusion
3. **"Ferramentas determinam a verdade. A IA explica a verdade."** — the canonical principle, placed here as the bridge to BanzAI

---

**EXPECTED VISITOR TAKEAWAY**

> "A great protocol that's too hard to understand doesn't get adopted. The more operators join, the more knowledge support burden grows — unless the protocol can explain itself. That's the problem BanzAI solves."

---

**NARRATIVE FLOW INTO §9**

End §8 with: "O BanzAI existe para resolver exactamente este problema. É o Sistema Operativo do protocolo."

---

---

### §9 — BanzAI

**ID:** V2-S09
**V1 equivalent:** §9 (BanzAI) — PRESERVED in full, with new framing at top.

---

**PURPOSE**

Introduce BanzAI as the Protocol Operating System. BanzAI exists because protocols need cognitive infrastructure to scale. Its 6 capabilities (Compreender · Explicar · Validar · Simular · Certificar · Federar) map directly to the adoption lifecycle of any certified operator.

---

**KEY MESSAGE**

BanzAI is not a payment chatbot. It is the cognitive infrastructure that makes the BANZA protocol navigable, explainable, and auditable at scale. Tools determine truth. AI explains truth. Without BanzAI, the protocol cannot scale beyond what a human support team can carry.

---

**REQUIRED CONTENT BLOCKS**

1. **New framing paragraph** at the top (new in V2):
   > "O BanzAI é o Sistema Operativo nativo do protocolo Banza. Existe porque a secção anterior o torna inevitável: um protocolo que ninguém consegue navegar não escala. O BanzAI é a resposta a esse problema."

2. **All existing §9 content** — preserved (porquê existe, fosso de conhecimento, diferença de IA genérica, camada cognitiva, sem BanzAI, BanzAI multiplica, arquitectura, módulos, etc.)

3. **Explicit anti-confusion statement** (new):
   > "O BanzAI não é um assistente de pagamentos. Não responde a 'quando chega o meu dinheiro'. Existe para operadores, programadores, reguladores e auditores que trabalham com o protocolo — não para consumidores finais."

---

**REQUIRED DIAGRAMS**

- **Diagram V2-D10:** BanzAI as OS: 6 capabilities mapped to the operator adoption lifecycle
- **All existing BanzAI architecture diagrams** — preserved

---

**EXPECTED VISITOR TAKEAWAY**

> "BanzAI is the Protocol Operating System. Its 6 capabilities (Understand, Explain, Validate, Simulate, Certify, Federate) cover every stage of the operator adoption lifecycle. It exists because the protocol, without cognitive infrastructure, cannot scale."

---

**NARRATIVE FLOW INTO §10**

End §9 with: "O BanzAI serve os operadores. Quem são os operadores? Como funciona o modelo de operadores?"

---

---

## PARTE III — OS OPERADORES

---

### §10 — O Modelo de Operadores

**ID:** V2-S10
**V1 equivalent:** §3 subsection "Operadores" — EXPANDED from subsection to full section.

---

**PURPOSE**

Define what operators are, who can become one, how the operator registry works, and why the operator model matters for the protocol ecosystem. This section closes Part I-III of the reference (protocol foundation) and transitions to Banzami as the first concrete example of an operator.

---

**KEY MESSAGE**

Operators are certified entities that implement the BANZA protocol and serve consumers and merchants. Any entity that passes the conformance suite becomes a certified operator. Banzami is the first and reference operator — but not the only one. The operator model is what makes BANZA an ecosystem rather than a product.

---

**REQUIRED CONTENT BLOCKS**

1. **What an operator is** — the full definition
2. **What operators do** — what they implement, what they expose to users
3. **Who can become an operator** — explicitly: any legal entity
4. **The operator registry** — curated, public
5. **Why the operator model matters**:
   > "Uma rede de pagamentos com um único operador é um produto. Uma rede com múltiplos operadores certificados — cada um competindo em UX, preço e nicho — é uma infraestrutura. O BANZA é infraestrutura. O modelo de operadores é o mecanismo que o torna possível."
6. **Operator responsibilities** — the Operator Manifesto (from current §7)
7. **Current operator count** + registry link

---

**REQUIRED DIAGRAMS**

- **Diagram V2-D11:** Ecosystem: BANZA protocol → multiple certified operators → each serving their own consumers/merchants → all interoperable via federation

---

**EXPECTED VISITOR TAKEAWAY**

> "Any entity can become a certified BANZA operator. Banzami is the reference operator — the first one. The operator model is what makes BANZA an ecosystem: many operators, one protocol, full interoperability."

---

**NARRATIVE FLOW INTO §11**

End §10 with: "O Banzami foi o primeiro operador certificado. É também a implementação de referência — a prova de que o protocolo funciona."

---

---

## PARTE IV — BANZAMI

---

### §11 — Banzami — A Implementação de Referência

**ID:** V2-S11
**V1 equivalent:** §1 partial + §11 (Comerciantes) + §12 (Consumidores) reorganized — CONSOLIDATED.

---

**PURPOSE**

Introduce Banzami as the reference operator. This section makes the critical distinction clear: Banzami is one operator among future many. It proves the protocol works. It is equivalent to Nubank on Pix or GPay on UPI — the biggest player, not the owner of the protocol.

---

**KEY MESSAGE**

Banzami is the reference implementation of the BANZA protocol. It proves the protocol works. It is built by the same organization that defined BANZA — but it does not own the protocol. If Banzami stopped operating, other certified operators would continue. The protocol survives any single operator.

---

**REQUIRED CONTENT BLOCKS**

1. **Canonical definition**:
   > "O Banzami é a implementação de referência do protocolo Banza. É um operador — o primeiro e o maior — mas não o proprietário do protocolo. Equivalente ao que o Nubank é para o Pix, ou ao que o GPay é para o UPI: o maior utilizador do protocolo, construído pela mesma organização que o definiu."

2. **The four products** — Wallet, Business, QR, SDK — framed as "how Banzami implements the protocol for Angolan consumers and merchants"

3. **Why "reference implementation" matters** — Banzami proves every protocol invariant in production. When a new operator certifies, they can verify their implementation against Banzami's behavior.

4. **ADR-025 architecture diagram** (already updated)

---

**EXPECTED VISITOR TAKEAWAY**

> "Banzami is the reference implementation. One operator, not the only operator. The protocol is what survives."

---

**NARRATIVE FLOW INTO §12-§14**

The following sections (§12-§14) describe how Banzami serves different audiences. They are Banzami-specific.

---

---

### §12 — Para Programadores

**ID:** V2-S12
**V1 equivalent:** §10 (Banzami para Programadores) — PRESERVED with new opening framing.

---

**PURPOSE**

Show developers how to integrate Banzami SDK. Add the missing "why BANZA instead of alternatives" argument before the technical content.

---

**KEY MESSAGE**

BANZA is Kwanza-native by protocol invariant. No USD exposure. No card requirement. No institutional access barrier. Any developer can integrate in hours.

---

**REQUIRED CONTENT BLOCKS**

1. **New differentiation preface** (new in V2 — from BANZA_MESSAGING_GAPS GAP-STR-003):
   > "Os gateways internacionais não suportam AOA. Exigem infraestrutura de cartão que a economia angolana não tem. Carregam risco de câmbio. Não integram com as rails EMIS. O BANZA é Kwanza-nativo por invariante de protocolo — AOA é a única moeda suportada. Sem câmbio. Sem requisito de cartão. Sem barreira institucional."

2. **All existing §10 content** — TypeScript SDK, Flutter SDK, webhooks, idempotency, sandbox — preserved

---

---

### §13 — Para Comerciantes

**ID:** V2-S13
**V1 equivalent:** §11 (Banzami para Comerciantes) — PRESERVED with structural framing added.

---

**PURPOSE**

Show merchants how Banzami works for them. Add the missing "why QR beats TPA" structural argument.

---

**KEY MESSAGE**

BANZA's QR protocol requires no acquiring contract, no hardware, no minimum transaction volume. This is not a feature difference from Multicaixa/TPA — it is a structural difference in how the payment is routed.

---

**REQUIRED CONTENT BLOCKS**

1. **Structural differentiation from Multicaixa/TPA** (new in V2):
   > "O Multicaixa/TPA exige um contrato de aquisição com um banco, investimento em hardware e custos mensais — criando uma dimensão mínima de comerciante viável. O QR do Banzami não exige nenhum destes porque a liquidação é carteira-para-carteira: sem rede de aquisição no meio. Esta não é uma diferença de funcionalidade. É uma diferença estrutural na forma como o pagamento é encaminhado."

2. **All existing §11 content** — preserved

---

---

### §14 — Para Consumidores

**ID:** V2-S14
**V1 equivalent:** §12 (Para Consumidores) — PRESERVED with minor framing update.

---

**PURPOSE**

Describe Banzami Wallet for consumers.

---

**KEY MESSAGE**

Banzami Wallet is Angola's first wallet-native payment app — built on the BANZA open protocol.

---

**REQUIRED CONTENT BLOCKS**

1. **New framing sentence** (new in V2):
   > "A Banzami Wallet é o produto de consumo da Banzami — um operador certificado Banza. Qualquer funcionalidade da wallet que a distingue baseia-se nas garantias do protocolo: T+0, verificabilidade e identidade @banza."

2. **All existing §12 content** — preserved

---

---

### §15 — Arquitectura Técnica de Referência

**ID:** V2-S15
**V1 equivalent:** §4 (Arquitectura Técnica) — SPLIT from §6 protocol specs. Only Banzami-specific implementation details here.

---

**PURPOSE**

Describe how Banzami implemented the BANZA protocol. This is the reference implementation's technical architecture — NOT the protocol's technical rules (those are in §6). Explicitly framed as "how Banzami did it, not how every operator must do it."

---

**KEY MESSAGE**

This is how Banzami implemented the BANZA protocol. Rust kernel, Go services, Next.js frontends, Flutter SDK. These are Banzami's implementation choices — other operators may make different choices, as long as they pass the conformance suite.

---

**REQUIRED CONTENT BLOCKS**

1. **New framing paragraph** (new in V2):
   > "Esta secção descreve a arquitectura técnica do Banzami — a implementação de referência. Não é o único modo válido de implementar o protocolo Banza. É o modo que escolhemos. Outros operadores podem usar stacks diferentes, desde que passem o conformance suite."

2. **All existing §4 technical content** — stack, services topology, observability, environment separation — preserved

3. **Remove from here:** Financial invariants, monetary representation (already moved to §6)

---

---

### §16 — Sandbox e Ambiente de Testes

**ID:** V2-S16
**V1 equivalent:** §14 (Sandbox) — PRESERVED, minor framing update.

---

**REQUIRED CONTENT BLOCKS**

1. **New framing sentence**: Frame sandbox as "a complete BANZA protocol environment for testing operator implementations before certification"
2. **All existing §14 content** — preserved

---

---

### §17 — Roadmap

**ID:** V2-S17
**V1 equivalent:** §16 (Roadmap) — EXPANDED with BANZA Protocol track.

---

**PURPOSE**

Present two explicit roadmap tracks: the BANZA Protocol roadmap (protocol-level milestones that any operator benefits from) and the Banzami Product roadmap (Banzami-specific milestones).

The BANZA Protocol roadmap track is NEW — it does not exist in V1.

---

**KEY MESSAGE**

BANZA has a protocol roadmap (federation, open operator certification, cross-border rails, acquiring integration) that is separate from Banzami's product roadmap.

---

**REQUIRED CONTENT BLOCKS**

1. **BANZA Protocol Roadmap** (NEW):
   - Federation architecture (Phase 1: spec; Phase 2: reference implementation; Phase 3: multi-operator)
   - Open operator certification process (public conformance suite release)
   - Acquiring integration (L4 certification — EMIS acquiring)
   - Cross-border protocol extension (AOA ↔ other African currencies)
   - Protocol governance evolution (RFC process public opening)

2. **Banzami Product Roadmap** — from existing §16 (preserved)

3. **Separation label**: Make the two tracks visually distinct. A reader must immediately understand which milestones are protocol-level (benefit all operators) vs. Banzami-specific.

---

---

### §18 — Declaração de Visão

**ID:** V2-S18
**V1 equivalent:** §17 (Declaração de Visão) — REFRAMED.

---

**PURPOSE**

Close the reference with the protocol vision, not the product vision. The closing statement should foreground BANZA (the protocol) and frame Banzami as one actor in the ecosystem.

---

**KEY MESSAGE**

Angola's digital payment ecosystem will be built on the BANZA protocol — not on any single operator's product. The ecosystem succeeds when any developer can build, any operator can certify, and any Angolan can transact.

---

**REQUIRED CONTENT BLOCKS**

1. **Reframed vision statement** — protocol-first (existing §17 is product-first, close with product-first closer once the protocol is in focus)

2. **Closing identity anchor**:
   > "O protocolo é o que fica. Os operadores mudam. Os produtos evoluem. O que o Banza garante é que as regras permaneçam abertas, a certificação permaneça acessível, e a infraestrutura permaneça de Angola."

3. **Existing §17 content** — reframed, not replaced. The emotional "O que o comércio de Angola merece" content can close the section after the protocol vision is stated.

---

---

## Summary: What Changes vs. V1

| Change type | Count | Description |
|-------------|-------|-------------|
| RELOCATED (same content, new position) | 4 | §6→§4, §7→§5, §8→§7, §15→§1 |
| ELEVATED (subsection → full section) | 2 | §3 Operators, §9 Knowledge Problem |
| NEW (no V1 equivalent) | 4 | §2 Protocol Layer, §8 Knowledge Problem, Protocol Roadmap track, §6 split |
| REFRAMED (same content, new narrative wrapper) | 6 | §3, §9, §11, §13, §14, §18 |
| SPLIT | 1 | §4 → §6 (protocol specs) + §15 (Banzami impl) |
| PRESERVED (no change) | 3 | §5 Monetary Representation, §12 Developers content, §14 Sandbox content |
| DELETED | 0 | No content removed — only relocated or reframed |

**The most consequential single change:** §15 "Por que Angola. Por que Agora." moves from position 15/17 to position 1/18. The problem argument becomes the opening argument.

---

*Blueprint completed: 2026-05-30. No files modified.*
