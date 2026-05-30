---
title: PHASE_0B_REVIEW
version: 1.0
date: 2026-05-30
status: REVIEW COMPLETE
---

# Phase 0B Review — Hardened §§1–3

**Purpose:** Re-run the same six comprehension tests and full section review applied in Phase 0A. Target: 95+/100 and 100% on all six comprehension tests. No partial scores accepted.

**Baseline:** Phase 0A scored 83/100 with five identified fixes and one partial on the six-test suite.

---

## Validation Test — Six Comprehension Tests

*Can a first-time visitor explain each of the following after reading §§1–3?*

| # | Question | Result | Evidence |
|---|----------|--------|----------|
| 1 | Why does BANZA exist? | **YES** | §1 establishes the protocol gap with five concrete symptoms all attributed to one cause. The "causa oculta" section makes the argument explicit: Angola has rails (EMIS) and products but not the connecting layer. |
| 2 | What is BANZA? | **YES** | §3 opens with the canonical one-sentence definition. Followed by four properties of a protocol, the three-tier hierarchy, and the "not a bank / not a product / not a gateway" table with explanations for each distinction. |
| 3 | Why is BANZA different? | **YES** | §2 provides the full structural comparison: road analogy, explicit settlement-vs-protocol-layer separation, M-Pesa vs. Pix/UPI model table, and the survivability test. §3 adds the contract-vs.-protocol-guarantee concrete example for T+0. |
| 4 | Why does BANZA survive any operator? | **YES** | §2 "O que acontece se o Banzami desaparecer?" answers this directly with three bullet points. §3 reinforces it via the Nubank/Pix analogy and "O protocolo é o que fica." The argument appears in both sections without contradiction. |
| 5 | What role does BanzAI play? | **YES** | §3's BanzAI section now: names BanzAI as the Protocol OS; identifies the problem it solves (protocol navigation at scale); lists all six capabilities (Compreender · Explicar · Validar · Simular · Certificar · Federar) with one-paragraph explanations each; distinguishes from ChatGPT, support, and documentation explicitly; states the canonical principle. |
| 6 | What role does Banzami play? | **YES** | §2 answers via survivability logic. §3 defines it as "the reference implementation" with the Nubank/Pix analogy. "Um operador entre futuros muitos — não o dono do protocolo." |

**Six-test result: 6/6 — NO partial scores.**

---

## Section-by-Section Review

---

### §1 — O Problema: Angola Tem as Peças

**Changes applied vs. draft:**
1. EMIS clarification added to "A causa oculta"
2. Concrete examples added to abstract symptoms 4 and 5

**Strengths**

1. **The EMIS distinction is now explicit.** "O EMIS resolve uma questão específica: como o dinheiro se move entre bancos depois de uma transacção ser aprovada. Não resolve uma questão diferente: quem pode aceder ao sistema de pagamentos, em que condições, e segundo que regras verificáveis." A reader who knows Angola's banking system will no longer carry the "why doesn't EMIS fill this role?" objection into §2.

2. **Symptom 4 ("Dependência de redes proprietárias") is now concrete.** The addition "sem aviso e sem recurso: os utilizadores e comerciantes que dependem dele não têm alternativa além de migrar para outro sistema igualmente fechado" makes the consequence of dependency real, not abstract.

3. **Symptom 5 ("Ausência de garantias de protocolo") now names the contractual alternative explicitly.** "A liquidação instantânea é uma promessa que alguns produtos fazem — no seu contrato de serviço, na sua documentação, no seu marketing. Mas uma promessa contratual não é verificável por auditores independentes." The reader now understands WHY the absence of protocol guarantees is a structural problem, not just a missing feature.

4. **Structure remains intact.** No additions before the "Angola tem as peças" pivot. BANZA still appears only in the final paragraph. The tension arc is preserved.

**Remaining weaknesses**

1. **None identified.** All P0/P1 fixes from Phase 0A have been applied. The section now satisfies its design brief completely.

**Ambiguity risks**

- **None remaining.** The EMIS distinction eliminates the principal ambiguity risk from Phase 0A. The symptom examples eliminate the abstraction risk for symptoms 4 and 5.

**Score: 93/100**

*Minor deduction: "O Brasil resolveu este problema em 2020. A Índia resolveu em 2016." — these claims are introduced in §1 without the structural comparison that §2 provides. A reader who doesn't continue to §2 may not understand why these countries are cited or what they resolved. This is an acceptable forward reference, not an error — but it is marginally incomplete as a standalone sentence. No fix required; §2 resolves it.*

---

### §2 — A Camada que Falta

**Changes applied vs. draft:**
1. "Uma analogia antes da finança" subheader removed — flows directly
2. "Liquidação vs. protocolo" section added (explicit settlement layer vs. protocol layer)
3. "Angola escolhe o modelo aberto" → "O BANZA propõe o modelo aberto para Angola"
4. "conformance suite" defined parenthetically on first use
5. Pix and UPI scale numbers added

**Strengths**

1. **The "Liquidação vs. protocolo" section is the most important addition in the entire hardening pass.** It removes the section's most significant ambiguity risk — the implicit assumption that readers understand why EMIS doesn't solve the problem. Now explicit: "A camada de liquidação responde à pergunta: como o dinheiro se move entre bancos depois de uma transacção ser aprovada? A camada de protocolo responde a perguntas diferentes: quem pode oferecer serviços de pagamento? Em que condições? Com que garantias verificáveis?" A regulator, a banker, or an economist who knows EMIS will immediately understand the distinction.

2. **The road analogy flows without interruption.** Removing the subheader warning ("Uma analogia antes da finança") allows the analogy to open the section naturally. A reader who might have skimmed past the analogy now encounters it as part of the continuous prose.

3. **"Conformance suite" is now defined on first use.** "(o conjunto de testes técnicos que qualificam uma implementação como conforme)" — a non-technical reader now has enough context to understand what certification involves without needing to read §5 first.

4. **Impact numbers for Pix and UPI are concrete and comparative.** "Dois anos após o lançamento, o Pix processava mais transacções mensais do que todos os cartões de crédito no Brasil combinados" and "Em 2024, o UPI processava doze mil milhões de transacções por mês" convert abstract claims of "success" into felt impact. These numbers should be verified against published data before the section goes live in the reference.

5. **"O BANZA propõe o modelo aberto para Angola" — the correction is precise.** The original "Angola escolhe" overstated the institutional status of BANZA (implying a state decision, like Pix was a BCB mandate). "Propõe" correctly frames BANZA as offering the open model rather than representing a concluded national decision.

6. **The M-Pesa treatment remains fair.** "Um dos produtos financeiros mais transformadores que África alguma vez produziu" — the fair framing is preserved. The structural comparison is neutral: M-Pesa chose one model; Pix/UPI chose another; BANZA follows the second.

**Remaining weaknesses**

1. **Minor: the table row "Pode um terceiro tornar-se operador independente? — Não [for M-Pesa]"** is accurate but could be softened to "Não, sem acordo bilateral" — some readers may know that M-Pesa has third-party integration programs, and the flat "Não" could trigger a factual objection that distracts from the structural argument. *Low priority — does not affect comprehension.*

2. **Minor: "Dois anos após o lançamento" should be verified before publication.** Pix launched November 2020; the claim refers to approximately late 2022. The card comparison claim is approximately accurate but sourced from BCB reports. Flag for fact-check before integration.

**Ambiguity risks**

- **None significant remaining.** The settlement-vs-protocol-layer section eliminates the principal ambiguity. The "Angola propõe" correction eliminates the overstated institutional status. The conformance suite definition eliminates the undefined-term risk.

**Score: 96/100**

*Minor deductions for the two points above — neither affects comprehension or narrative integrity.*

---

### §3 — O que é o BANZA

**Changes applied vs. draft:**
1. Three-tier hierarchy diagram updated — BanzAI line now includes six capabilities listed
2. "Invariantes verificáveis" expanded with T+0 contract-vs.-protocol-guarantee concrete example
3. "verificáveis por qualquer auditor independentemente de qualquer operador" added
4. BanzAI section completely rewritten — six capabilities + ChatGPT/support/docs distinctions
5. "O arco completo" closing section added

**Strengths**

1. **The T+0 contract-vs.-protocol-guarantee example is the most technically clarifying addition.** Before: "invariantes verificáveis" was a claim. After: the reader has a concrete contrast — bank promises T+0 in a service agreement (contractual, interpretable, disputable) vs. the Rust kernel enforces T+0 as an invariant (mathematical property, inspeccionável, non-configurable). This example makes the difference between a protocol and a product guarantee visceral. A banker, a regulator, or a developer will all understand this from different angles.

2. **The six BanzAI capabilities are now fully explained.** Each capability is named and described in one concise paragraph. The progression is logical: Compreender (basis) → Explicar (output) → Validar (pre-certification check) → Simular (scenario testing) → Certificar (certification guidance) → Federar (federation mapping). A reader finishes the six paragraphs understanding what BanzAI actually does, not just why it exists.

3. **The three-way distinction (BanzAI ≠ ChatGPT, ≠ support, ≠ documentation) is precise and non-defensive.** The paragraphs don't claim BanzAI is "better than" these alternatives — they clarify structural differences: ChatGPT is grounded in the internet; BanzAI is grounded in the protocol. Support scales linearly; BanzAI scales differently. Documentation is searched; BanzAI is questioned. A reader who arrives at /banzamia expecting a chatbot will now understand what they are actually encountering.

4. **The canonical principle — "Ferramentas determinam a verdade. A IA explica a verdade." — is now placed after the six capabilities, where it lands as a summary, not an abstract claim.** In the draft, this principle appeared without the capabilities context that makes it meaningful. Now it closes the BanzAI section as a statement the reader can verify against what they just read.

5. **"O arco completo" is the correct close for all three sections.** It is the only section in §§1–3 that summarizes what was just established (the argument across three sections) and names what comes next (governance, certification, technical specifications, federation). The final sentence — "O protocolo está definido. A seguir, as suas regras." — is precisely calibrated: it closes the introduction without understating it ("we're done") or overpromising ("now comes everything"). It pulls the reader forward.

6. **The three-tier hierarchy diagram now includes BanzAI's six capabilities.** "Seis capacidades: Compreender · Explicar · Validar · Simular · Certificar · Federar." A reader who sees the hierarchy diagram first understands immediately that BanzAI has six specific functions, not just a vague "Protocol OS" label.

**Remaining weaknesses**

1. **Minor: the BanzAI section is now the longest section in §3**, which tips the visual weight of the section toward BanzAI rather than toward the protocol definition itself. This is acceptable — BanzAI was the most under-explained element in the draft — but in the final reference layout, a visual break or slight condensation of the six-capability paragraphs might improve balance. *Not a comprehension issue — a layout consideration for integration.*

2. **Minor: "verificáveis por qualquer auditor independentemente de qualquer operador" is correct but slightly redundant** in context ("independentemente de qualquer operador" restates what "verificáveis" already implies once the contract comparison is given). No fix required.

**Ambiguity risks**

- **None significant remaining.** All six comprehension questions are satisfied. The BanzAI section no longer leaves the reader with a vague "Protocol OS" label. The T+0 example makes "invariante verificável" concrete. The closing arc makes the transition to subsequent sections clear.

**Score: 96/100**

*Minor deductions for the two layout/style points above. No comprehension deductions.*

---

## Cross-Section Narrative Consistency

| Consistency check | Status | Notes |
|-------------------|--------|-------|
| Problem in §1 → protocol gap → answered in §2 → named as BANZA in §3 | **PASS** | Unchanged from Phase 0A. Logical chain is complete. |
| EMIS explicitly excluded from "protocol layer" role | **PASS** | New in this version. §1 "A causa oculta" + §2 "Liquidação vs. protocolo" both make this explicit. |
| Pix/UPI introduced in §2 → referenced in §3 opening sentence | **PASS** | Unchanged. Forward reference works because §2 establishes the full context. |
| "O protocolo é o que fica" → present in both §2 and §3 | **PASS** | Unchanged. Appears in §2 closing (implicit) and §3 body (explicit). |
| Banzami introduced only after BANZA and the protocol model are defined | **PASS** | Banzami not named until §3. Correctly deferred. |
| BanzAI introduced with its six capabilities | **PASS** | New in this version. §3 BanzAI section now complete. |
| M-Pesa treated fairly throughout | **PASS** | No change to the M-Pesa framing. Fair treatment preserved. |
| No feature/product/technology language in §§1–3 | **PASS** | No QR, Wallet, SDK, Rust architecture, or Banzami product references in §§1–3. |
| Closing arc closes §§1–3 and opens §§4–7 | **PASS** | New in this version. "O arco completo" section performs this function. |
| Tone consistency (authoritative, non-promotional) | **PASS** | No marketing language. "O BANZA propõe" removes the only instance of overstated authority. |

---

## Narrative Consistency Score

**Score: 96 / 100**

**Breakdown:**

| Dimension | Phase 0A | Phase 0B | Delta | Rationale |
|-----------|----------|----------|-------|-----------|
| Problem clarity (§1) | 87 | 93 | +6 | EMIS distinction + concrete symptom examples eliminate principal gaps |
| Protocol layer explanation (§2) | 88 | 96 | +8 | Settlement-vs-protocol section added; conformance suite defined; "propõe" correction; impact numbers |
| BANZA definition (§3) | 79 | 96 | +17 | BanzAI six capabilities; T+0 concrete example; closing arc — most improved section |
| Cross-section coherence | 85 | 97 | +12 | EMIS excluded from protocol role explicitly in both §§1 and 2; BanzAI gap closed; arc completed |
| Audience accessibility | 78 | 96 | +18 | Road analogy flows without interruption; "conformance suite" defined; BanzAI not a chatbot; T+0 example accessible to non-technical readers |

---

## Success Criteria Assessment

*After reading §§1–3, can a completely new reader say:*

| Statement | Phase 0A | Phase 0B |
|-----------|----------|----------|
| "BANZA is not a payment application." | YES | **YES** — §3 explicitly: "O BANZA não é um produto fintech." |
| "BANZA is not a bank." | YES | **YES** — §3 explicitly: "O BANZA não é um banco." |
| "BANZA is not a gateway." | YES | **YES** — §3 explicitly: "O BANZA não é um gateway de pagamentos." |
| "BANZA is the protocol layer Angola lacks." | YES | **YES** — §1 names the gap, §2 names the model, §3 names BANZA as the answer. §2 additionally makes the EMIS/settlement layer distinction explicit so "protocol layer" is understood. |
| "BanzAI is the operating system of that protocol." | PARTIAL | **YES** — §3 now explains all six capabilities, distinguishes from ChatGPT/support/documentation, and closes with the canonical principle. The reader knows not just that BanzAI is the Protocol OS but what that means in practice. |
| "Banzami is the reference implementation." | YES | **YES** — unchanged. §2 survivability argument + §3 Nubank/Pix analogy. |

**Six-test result: 6/6. No partial scores. Target achieved.**

---

## Integration Recommendation

**APPROVED FOR INTEGRATION PLANNING.**

The three hardened sections satisfy all design briefs, all six comprehension tests, and all Phase 0A priority fixes. No remaining blocking issues.

**Two pre-integration steps before writing the sections into BANZAMI_REFERENCE.md:**

1. **Fact-check two numbers in §2:**
   - "Dois anos após o lançamento, o Pix processava mais transacções mensais do que todos os cartões de crédito no Brasil combinados" — verify against BCB published data
   - "Em 2024, o UPI processava doze mil milhões de transacções por mês" — verify against NPCI published data
   These are correct to the best of available knowledge at time of writing but should be sourced before publication.

2. **Confirm canonical BanzAI capability names with BanzAI module spec in V1 §9.** The six capabilities used (Compreender · Explicar · Validar · Simular · Certificar · Federar) are consistent with ADR-025 and the V1 BanzAI section. Verify the Portuguese verb forms are the canonical forms in the current codebase/reference before integration.

**After these two steps: the sections are ready to be integrated into BANZAMI_REFERENCE.md as §§1–3 of V2.**

---

## What Changed: Phase 0A → Phase 0B at a Glance

| Fix | Applied | Impact |
|-----|---------|--------|
| §1: EMIS clarification (settlement ≠ protocol layer) | ✓ | Eliminated principal ambiguity for banking/regulatory readers |
| §1: Concrete examples for abstract symptoms 4 and 5 | ✓ | Eliminated abstraction risk for non-technical readers |
| §2: Remove "Uma analogia antes da finança" subheader | ✓ | Analogy flows as narrative, not as a flagged digression |
| §2: "Liquidação vs. protocolo" section | ✓ | Most important structural addition — closes EMIS objection explicitly |
| §2: "Angola escolhe" → "O BANZA propõe" | ✓ | Corrects overstated institutional status |
| §2: "Conformance suite" defined parenthetically | ✓ | Removes undefined-term risk for first-time readers |
| §2: Pix and UPI impact numbers | ✓ | Converts abstract "success" claims into concrete scale |
| §3: BanzAI full rewrite with six capabilities | ✓ | Phase 0A's only partial now fully satisfied |
| §3: T+0 contract-vs.-protocol-guarantee example | ✓ | "Invariante verificável" is now concrete, not a claim |
| §3: "verificáveis por qualquer auditor" | ✓ | Reinforces auditor independence |
| §3: "O arco completo" closing section | ✓ | Three-section arc now closes cleanly and opens §§4–7 |

**All Phase 0A P0 and P1 fixes applied. No remaining priority items.**

---

*Review completed: 2026-05-30. Target score achieved: 96/100. Six comprehension tests: 6/6.*
