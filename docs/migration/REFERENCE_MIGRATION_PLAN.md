---
title: REFERENCE_MIGRATION_PLAN
version: 1.0
date: 2026-05-30
status: DESIGN COMPLETE — pending execution authorization
---

# Reference Migration Plan

**Purpose:** Specify every content change required to migrate BANZAMI_REFERENCE.md from V1 to V2. For each section: what moves, what is rewritten, what is new, what is split, and what is absorbed.

**Source file:** `/Users/fm65/Banza/docs/BANZAMI_REFERENCE.md`
**Target:** same file, rebuilt structure
**Approach:** In-place rebuild (not a parallel file) — the document is rebuilt section by section

---

## Migration Status Legend

| Status | Meaning |
|--------|---------|
| `RELOCATE` | Content moves to a new position. No rewriting. |
| `REFRAME` | Content stays in similar position. Opening paragraph rewritten. Body preserved. |
| `EXPAND` | Content preserved. New paragraphs added. No content removed. |
| `SPLIT` | Section content divided into two destinations. |
| `ELEVATE` | Subsection becomes a standalone section. |
| `NEW` | No V1 content. Entirely new writing required. |
| `ABSORB` | Content from multiple V1 sources merged into one section. |
| `PRESERVE` | No change. Content is correct as-is. |

---

## Section-by-Section Migration Map

### §1 — O Problema: Angola Tem as Peças
**Migration status:** `RELOCATE` + `EXPAND`

**V1 source:** §15 "Por que Angola. Por que Agora." (lines ~1815–1868)

**What moves:**
- All content from V1 §15 moves here verbatim as the base
- "A oportunidade" → becomes "Angola já tem" inventory
- "O problema que o Banzami resolve" → becomes the symptom→cause mapping section

**What is new (additions):**
1. Opening framing paragraph: establishes the document will start with the problem, not the definition
2. "Angola já tem" explicit inventory (settlement rails, banks, smartphone penetration, payment products)
3. "O que Angola não tem" structural gap argument (4 missing properties: open rules, open certification, verifiable invariants, interoperability)
4. Symptom → Cause mapping: the 5 homepage symptoms mapped to the single structural cause (the protocol gap)
5. Closing paragraph that names BANZA as the answer without providing details: "Este é o vazio que o BANZA preenche. Não como banco. Não como produto fintech. Como protocolo."

**Diagram required:** V2-D01 (three-layer stack with gap highlighted — new diagram)

**V1 content that stays in §1 from V1 §15:**
- "O salto tecnológico" content (Angola's technological leap conditions)
- "A oportunidade" content (market size, informal economy)

**Estimated new prose:** ~60 lines

---

### §2 — A Camada que Falta
**Migration status:** `NEW`

**V1 source:** None — this section is assembled from fragments scattered across V1 §1, §2, §15, §17.

**Fragment sources in V1:**
- V1 §1: "Não é um banco. Não é uma carteira digital simples..." → conceptual DNA
- V1 §2: "O protocolo é o produto" → principle
- V1 §15: "O modelo está provado: o Pix no Brasil, o UPI na Índia..." → 3-sentence mention to expand
- V1 §17 closing references → emotional DNA

**What is new (full new writing required):**
1. Definition of "protocol layer" in plain language
2. Full Pix / UPI / M-Pesa structural comparison (~300 words):
   - Pix: Brazilian Central Bank, open protocol, any bank implements it, 18 months to dominant
   - UPI: NPCI, open standard, billions of transactions, no single owner
   - M-Pesa: Safaricom/Vodacom, proprietary, other companies integrate with their API, terms change at operator's discretion
   - BANZA: follows Pix/UPI model — open RFCs, open certification, Banzami is reference operator not owner
3. "Por que a distinção importa enormemente" (2 paragraphs):
   - M-Pesa model: Banzami disappears → protocol disappears
   - Pix/UPI model: Banzami disappears → other operators continue
4. Angola's preconditions (mirrors Pix Brazil 2020 / UPI India 2016 conditions)

**Diagram required:** V2-D02 (Pix/UPI model vs. M-Pesa model side-by-side — new diagram)

**Estimated new prose:** ~100 lines

---

### §3 — O que é o BANZA
**Migration status:** `RELOCATE` + `REFRAME`

**V1 source:** §1 "O que é o Banza?" (lines ~38–77)

**What moves:** All content from V1 §1

**What changes (reframe):**
1. Opening sentence reframed: "Banza é infraestrutura financeira programável de código aberto para Angola" → new canonical one-sentence definition that includes the protocol-layer framing from §1–§2: "BANZA é o protocolo aberto que Angola não tem — a infraestrutura certificada que qualquer programador, operador ou instituição pode usar para construir, da mesma forma que o Pix construiu o ecossistema de pagamentos do Brasil e o UPI construiu o da Índia."
2. After the new opening: the three-tier hierarchy and SVG diagram (already updated in ADR-025 execution)
3. "Os quatro princípios" table — explicitly reframed as protocol invariants, not product features. The framing sentence already updated in ADR-025 execution: "Qualquer operador certificado Banza implementa estes quatro princípios." — PRESERVE AS-IS.
4. The negative definitions ("Não é um banco...") — PRESERVE, but add the positive protocol-layer counterpart after each.

**What is NOT changed:** The name etymology (§1 last subsection "O nome") — PRESERVE verbatim.

**Estimated rewriting scope:** ~15 lines (opening + negative-definition counterparts)

---

### §4 — Governança do Protocolo
**Migration status:** `RELOCATE` + `REFRAME`

**V1 source:** §6 "Governança" (lines ~494–541)

**What moves:** All content from V1 §6

**What changes (reframe):**
1. New opening paragraph: "Por que a governança vem antes da tecnologia" argument — establishes the principle that in a protocol, architecture is law, not implementation detail.
2. Body: PRESERVE verbatim (RFCs, ADRs, Validation Matrix, Validation domains)
3. New closing sentence bridging to §5: certification as governance enforcement

**Estimated rewriting scope:** ~10 lines

---

### §5 — Modelo de Certificação
**Migration status:** `RELOCATE` + `EXPAND`

**V1 source:** §7 "Modelo de Certificação" (lines ~542–630)

**What moves:** All content from V1 §7 (certification levels, process, operator manifesto, maintenance)

**What is new (additions):**
1. New opening: "Why certification is the structural difference from traditional access" — the comparison to traditional bank API access vs. open conformance suite
2. Explicit statement: "Qualquer entidade legal que passe o conformance suite torna-se um operador certificado. Sem acesso institucional. Sem acordo bilateral. Sem volume mínimo de transacções."
3. New closing bridge to §6: "A certificação verifica que o operador implementou as regras. Quais são essas regras, exactamente?"

**Estimated new prose:** ~20 lines

---

### §6 — Regras do Protocolo — Especificações Técnicas
**Migration status:** `SPLIT` (from V1 §4 + §5)

**V1 sources:**
- V1 §4 "Arquitectura Técnica" (lines ~154–227) — SPLIT: only protocol-level content (invariants, ledger model) moves here; implementation-specific content (stack, services topology, observability) moves to §15
- V1 §5 "Representação Monetária" (lines ~228–490) — MOVES HERE in full

**Content allocation:**

| V1 Content | Destination |
|-----------|-------------|
| §4 Stack tecnológico (Rust/Go/Next.js table) | → §15 |
| §4 Topologia de serviços | → §15 |
| §4 O ledger de dupla entrada | → §6 (here) |
| §4 Invariantes financeiros | → §6 (here) |
| §4 Sistema de rastreabilidade | → §6 (here) |
| §5 Entire section (Monetary Representation) | → §6 (here) |

**What is new (additions):**
1. New opening framing paragraph: "As especificações desta secção aplicam-se a qualquer operador certificado Banza. O Banzami implementa-as — mas não as define. São definidas pelo protocolo."
2. T+0 as a protocol invariant — explicit statement (currently buried in product descriptions)
3. Bridge to §15: "A secção §15 descreve como o Banzami implementou estas especificações. Outros operadores podem fazer escolhas diferentes."

**Estimated new prose:** ~15 lines

---

### §7 — Federação
**Migration status:** `RELOCATE` + `REFRAME`

**V1 source:** §8 "Federação" (lines ~597–636)

**What moves:** All content from V1 §8

**What changes (reframe):**
1. New opening: "Why federation proves BANZA is infrastructure" — the argument that only a protocol federates; a single-operator product cannot federate with other products
2. Body: PRESERVE verbatim
3. New closing bridge to §8: "O protocolo define as regras. A certificação garante a sua implementação. A federação garante a interoperabilidade. Mas um protocolo que ninguém consegue navegar não escala."

**Estimated rewriting scope:** ~10 lines

---

### §8 — O Problema do Conhecimento do Protocolo
**Migration status:** `ELEVATE` (subsection → standalone section)

**V1 source:** §9 subsections "O Fosso de Conhecimento do Protocolo" (lines ~672–683) + "O que acontece sem BanzAI" (lines ~753–765)

**What moves:** Both subsections, combined and reordered into standalone section

**What is new (additions):**
1. New section header: "O Problema do Conhecimento do Protocolo" (matches the section title)
2. Explicit bridge from protocol sections: "Definimos o protocolo. Definimos governança, certificação, especificações e federação. Mas um protocolo que os seus utilizadores não conseguem navegar não escala. Este é um problema diferente dos que acabámos de resolver."
3. Closing bridge to §9: "O BanzAI existe para resolver exactamente este problema."
4. The canonical principle placed here: "Ferramentas determinam a verdade. A IA explica a verdade." — currently in V1 §2 Princípios Fundamentais. MOVE here as it is the bridge concept.

**V1 §2 impact:** Moving "Ferramentas determinam a verdade. A IA explica a verdade." from §2 to §8 removes it from the Principles section. The remaining principles in V1 §2 either move to §3 (as protocol principles) or to §6 (as protocol invariants).

**Estimated new prose:** ~15 lines

---

### §9 — BanzAI
**Migration status:** `REFRAME` (content preserved, opening added)

**V1 source:** §9 "BanzAI" (lines ~632–1589) — the entire section (~957 lines)

**What changes (reframe only):**
1. New opening paragraph at the very top of §9 (before existing "O BanzAI é o Sistema Operativo nativo do protocolo Banza"):
   > "O BanzAI é o Sistema Operativo nativo do protocolo Banza. Existe porque a secção anterior o torna inevitável: um protocolo que ninguém consegue navegar não escala. O BanzAI é a resposta a esse problema. Não é um assistente de pagamentos. Não responde a 'quando chega o meu dinheiro'. Existe para operadores, programadores, reguladores e auditores que trabalham com o protocolo — não para consumidores finais."
2. All existing §9 content: PRESERVE VERBATIM

**What is NOT changed:** All 16 module descriptions, all architecture sections, all capability descriptions — verbatim

**Estimated rewriting scope:** ~8 lines (opening paragraph only)

---

### §10 — O Modelo de Operadores
**Migration status:** `ELEVATE` + `EXPAND` (subsection → full section)

**V1 source:** §3 subsection "Operadores" (lines ~136–153) — a ~17-line subsection becomes a full section

**What moves:** The subsection content as the seed

**What is new (additions):**
1. Full operator model explanation (~60 new lines):
   - What operators are (entity that implements BANZA, passes conformance, serves users)
   - What operators do (implement protocol spec, expose SDK, serve consumers/merchants)
   - Who can become an operator (explicit: any legal entity)
   - The operator registry (current list + how to join)
   - Why the operator model matters: "Uma rede com um único operador é um produto. Uma rede com múltiplos operadores certificados é uma infraestrutura."
   - Operator responsibilities (Operator Manifesto reference → link to §5)
2. Closing bridge to §11: "O Banzami foi o primeiro operador certificado. É também a implementação de referência — a prova de que o protocolo funciona."

**Note:** The Operator Manifesto content remains in §5 (Certificação). §10 links to it, not duplicates it.

**Estimated new prose:** ~60 lines

---

### §11 — Banzami — A Implementação de Referência
**Migration status:** `NEW`

**V1 source:** None — this section does not exist in V1. Currently Banzami is introduced at the top of §1 ("Banzami é o produto principal do Banza") without its own dedicated section.

**What is new (full new writing required):**
1. Canonical definition: "O Banzami é a implementação de referência do protocolo Banza. É um operador — o primeiro e o maior — mas não o proprietário do protocolo."
2. The Pix/Nubank analogy: "Equivalente ao que o Nubank é para o Pix, ou ao que o GPay é para o UPI: o maior utilizador do protocolo, construído pela mesma organização que o definiu."
3. The four products as protocol implementations: Wallet (wallet-native principle), Business (merchant protocol surface), QR (QR-native principle), SDK (programmable principle)
4. Why "reference implementation" matters for other operators
5. The ADR-025 hierarchy diagram (already in §3 — cross-reference, do not duplicate)

**Estimated new prose:** ~50 lines

---

### §12 — Para Programadores
**Migration status:** `EXPAND` + minor `REFRAME`

**V1 source:** §10 "Banzami para Programadores" (lines ~1591–1681)

**What moves:** All content from V1 §10

**What is new (additions):**
1. New differentiation preface (~20 lines) at the top, before existing content:
   > "Os gateways internacionais não suportam AOA. Exigem infraestrutura de cartão que a economia angolana não tem. Carregam risco de câmbio. Não integram com as rails EMIS. O BANZA é Kwanza-nativo por invariante de protocolo — AOA é a única moeda suportada. Sem câmbio. Sem requisito de cartão. Sem barreira institucional. Um programador que queira construir pagamentos em Angola pode começar com o SDK em horas."

2. Existing content: PRESERVE verbatim (TypeScript SDK, Flutter SDK, webhooks, idempotency, sandbox)

---

### §13 — Para Comerciantes
**Migration status:** `EXPAND` + minor `REFRAME`

**V1 source:** §11 "Banzami para Comerciantes" (lines ~1682–1724)

**What moves:** All content from V1 §11

**What is new (additions):**
1. New structural differentiation paragraph at the top (~15 lines):
   > "O Multicaixa/TPA exige um contrato de aquisição com um banco, investimento em hardware e custos mensais — criando uma dimensão mínima de comerciante viável. O QR do Banzami não exige nenhum destes porque a liquidação é carteira-para-carteira: sem rede de aquisição no meio. Esta não é uma diferença de funcionalidade. É uma diferença estrutural na forma como o pagamento é encaminhado."

2. Existing content: PRESERVE verbatim

---

### §14 — Para Consumidores
**Migration status:** `EXPAND` (minimal)

**V1 source:** §12 "Para Consumidores" (lines ~1725–1755)

**What moves:** All content from V1 §12

**What is new (additions):**
1. New framing sentence at the top (~3 lines):
   > "A Banzami Wallet é o produto de consumo da Banzami — um operador certificado Banza. Qualquer funcionalidade da wallet que a distingue baseia-se nas garantias do protocolo: T+0, verificabilidade e identidade @banza."

2. Existing content: PRESERVE verbatim

---

### §15 — Arquitectura Técnica de Referência
**Migration status:** `SPLIT` receiver + `REFRAME`

**V1 source:** §4 "Arquitectura Técnica" (lines ~154–227) — only implementation-specific content

**What moves from V1 §4:**
- Stack tecnológico (Rust/Go/Next.js/Flutter table) → HERE
- Topologia de serviços → HERE

**What does NOT move from V1 §4 (goes to §6 instead):**
- O ledger de dupla entrada → §6
- Invariantes financeiros → §6
- Sistema de rastreabilidade → §6

**Also moves here from V1:**
- §13 "Segurança e Integridade Financeira" (lines ~1756–1789) — Banzami's security implementation
- §3 subsection "Kernel Banza" (lines ~111–135) — the kernel crates description

**What is new (additions):**
1. New opening framing paragraph: "Esta secção descreve a arquitectura técnica do Banzami — a implementação de referência. Não é o único modo válido de implementar o protocolo Banza. É o modo que escolhemos. Outros operadores podem usar stacks diferentes, desde que passem o conformance suite."
2. Cross-reference to §6: "As regras do protocolo que esta arquitectura implementa estão definidas em §6."

---

### §16 — Sandbox e Ambiente de Testes
**Migration status:** `PRESERVE` + minor `REFRAME`

**V1 source:** §14 "Sandbox e Ambiente de Testes" (lines ~1790–1811)

**What moves:** All content PRESERVE verbatim

**What is new (additions):**
1. New framing sentence: "O sandbox é um ambiente completo do protocolo Banza para testar implementações de operadores antes da certificação — e para desenvolvimento de SDKs."

---

### §17 — Roadmap
**Migration status:** `EXPAND` (new BANZA Protocol track) + `PRESERVE` (existing Banzami track)

**V1 source:** §16 "Roadmap" (lines ~1835–1868)

**What moves:** All content from V1 §16 → becomes the "Banzami Product Track" sub-section

**What is new (BANZA Protocol Track — new section):**
```
## Roadmap do Protocolo BANZA

### Curto prazo (H2 2026)
- Publicação do conformance suite para operadores externos
- Documentação de certificação open access
- RFC-FEDERATION-001: especificação de federação v1

### Médio prazo (H1 2027)
- Primeiro operador certificado externo ao Banzami
- Federation testnet: dois operadores em ambiente de testes
- Integração EMIS acquiring (L4 certification track)

### Longo prazo (H2 2027+)
- Federation mainnet: múltiplos operadores em produção
- Cross-border protocol extension (AOA ↔ outras moedas africanas)
- RFC process aberto à comunidade
- Protocol governance council
```

**Track separation:** The two tracks must be visually labeled: "BANZA Protocol Track" and "Banzami Product Track" — so a reader understands which milestones benefit all operators vs. Banzami only.

---

### §18 — Declaração de Visão
**Migration status:** `REFRAME`

**V1 source:** §17 "Declaração de Visão" (lines ~1869–1933)

**What moves:** All content from V1 §17

**What changes (reframe):**
1. New opening (~10 lines) — protocol-first vision statement:
   > "O ecossistema de pagamentos digitais de Angola será construído sobre o protocolo Banza — não sobre o produto de um único operador. O ecossistema tem sucesso quando qualquer programador pode construir, qualquer operador pode certificar, e qualquer angolano pode transaccionar."
2. Existing content: PRESERVE (emotional, Angola-first closing — appropriate at the end)
3. New closing anchor (~5 lines):
   > "O protocolo é o que fica. Os operadores mudam. Os produtos evoluem. O que o Banza garante é que as regras permaneçam abertas, a certificação permaneça acessível, e a infraestrutura permaneça de Angola."

---

## V1 Sections That Are Absorbed / Removed

| V1 Section | V1 position | Disposition |
|-----------|-------------|-------------|
| §2 Princípios Fundamentais | §2 | ABSORBED into §3 (protocol principles) + §6 (technical invariants) + §8 (bridge principle). §2 as a standalone section disappears. |
| §3 Visão Geral do Ecossistema | §3 | ABSORBED: "Kernel Banza" → §15; "Operadores" → §10; ecosystem context → §3 |
| §13 Segurança e Integridade Financeira | §13 | ABSORBED into §15 (Arquitectura Técnica de Referência) |

**No content is deleted.** Every line of V1 content is either preserved in place or relocated.

---

## Migration Sequence

The migration should be executed in this order to avoid creating a broken intermediate state:

**Phase 1 — Restructure (no new writing)**
1. Create the four-part labels and table of contents
2. Move §15 to §1 position (relocate, no rewriting yet)
3. Move §6, §7, §8 to §4, §5, §7 positions
4. Move §9 to §9 (same, minor reframe)
5. Move §10, §11, §12 to §12, §13, §14
6. Move §14 to §16

**Phase 2 — New content (new writing required)**
1. Write §2 (A Camada que Falta) — most important new section
2. Write §8 (O Problema do Conhecimento) — elevation
3. Write §10 (O Modelo de Operadores) — expansion
4. Write §11 (Banzami reference implementation) — new

**Phase 3 — Reframes (existing content, new wrappers)**
1. Reframe §1 (expand with gap argument)
2. Reframe §3 (new opening)
3. Reframe §4 (governance framing)
4. Reframe §5 (open certification argument)
5. Reframe §6 (protocol rules framing)
6. Reframe §7 (federation = infrastructure proof)
7. Reframe §9 (BanzAI opening)
8. Reframe §12 (developer differentiation preface)
9. Reframe §13 (merchant structural argument)
10. Reframe §15 (implementation vs. protocol rules framing)
11. Reframe §18 (protocol vision opening)

**Phase 4 — New roadmap and absorptions**
1. Write BANZA Protocol Roadmap track (§17)
2. Verify §2 Princípios absorbed correctly
3. Verify §3 Kernel content in §15
4. Verify §13 Security content in §15

---

## Test Coverage Impact

The test suite at `apps/docs/lib/__tests__/reference.test.ts` (51 tests, all currently passing) must continue to pass after migration.

**Tests at risk from restructuring:**
- Tests that reference section numbers (§1, §2, etc.) by number will need updating if section numbers change
- Tests that check for specific headings will need updating where headings change
- Tests that check for specific anchor IDs will need updating

**Tests NOT at risk:**
- Tests that check for presence of specific content strings (not section positions)
- Tests that check financial invariants (content preserved verbatim)
- Tests that check SDK examples (content preserved verbatim)

**Pre-migration step:** Run the test suite and note which tests are currently tied to section numbers or heading strings. These are the tests that will need updating post-migration.

---

## Estimated Scope

| Phase | New prose lines | Rewriting lines | Relocation (no change) |
|-------|----------------|-----------------|----------------------|
| Phase 1 (restructure) | 0 | 0 | ~1,800 lines |
| Phase 2 (new content) | ~230 | 0 | 0 |
| Phase 3 (reframes) | ~120 | ~80 | 0 |
| Phase 4 (roadmap + absorptions) | ~40 | 0 | 0 |
| **Total** | **~390 new lines** | **~80 rewritten lines** | **~1,800 relocated** |

The document grows from ~1,880 lines to ~2,100 lines. No content is removed.

---

*Migration plan completed: 2026-05-30. No files modified.*
