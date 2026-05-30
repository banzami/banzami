---
title: REFERENCE_OWNERSHIP_MATRIX
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: REFERENCE-CANONICAL-SEPARATION-001
---

# Reference Ownership Matrix

**Purpose:** Classify every section of the existing combined `banzami/docs/BANZA_REFERENCE.md` by canonical owner: BANZA / BanzAI / Banzami.

**Canonical ownership rule (ADR-025):**

> BANZA owns the rules.  
> BanzAI explains the rules.  
> Banzami implements the rules.

**Validation test applied to every section:**

1. Would this section still exist if Banzami disappeared tomorrow? → **BANZA**
2. Does this section explain, navigate, or certify the protocol (not own or implement it)? → **BanzAI**
3. Does this section describe a specific operator product, UX, merchant tool, or consumer experience? → **Banzami**

---

## Section Ownership Table

Source file: `banzami/docs/BANZA_REFERENCE.md` (2234 lines, 2026-05-28)

| § | Section Title | Owner | Rationale | Destination |
|---|---|---|---|---|
| §1 | O Problema: Angola Tem as Peças | **BANZA** | The protocol gap exists independently of any operator. Angola's payment problem is a structural, infrastructure problem — not a product problem. Would exist without Banzami. | `banza/BANZA_REFERENCE.md` |
| §2 | A Camada que Falta | **BANZA** | Defines what a protocol layer is vs. a product. Pix/UPI comparison. Protocol survivability argument. All protocol-layer concepts. | `banza/BANZA_REFERENCE.md` |
| §3 | O que é o BANZA | **BANZA** | Canonical protocol definition. Three-tier hierarchy. Four principles (Wallet-native, QR-native, Programmable, Instant settlement). These are protocol invariants — any operator must implement them. | `banza/BANZA_REFERENCE.md` |
| §4 | Princípios Fundamentais | **BANZA** | "Ferramentas determinam a verdade", financial correctness, protocol/operator separation, traceability, Angola-first. Protocol epistemology and principles. | `banza/BANZA_REFERENCE.md` |
| §5 | Visão Geral do Ecossistema | **BANZA** | Kernel crates description, operator model, certified operators. The ecosystem overview is protocol-level. Banzami appears as reference operator — not as owner. | `banza/BANZA_REFERENCE.md` |
| §6 | Arquitectura Técnica | **SPLIT** | Stack and service topology → **Banzami** (implementation choices). Ledger model, financial invariants, traceability → **BANZA** (protocol rules). | BANZA: protocol rules / Banzami: implementation |
| §7 | Representação Monetária | **BANZA** | Entire section is normative for all operators. Integer rule, `*_minor` convention, MON-001, CONFORMANCE-MON-001. Would apply to any operator. | `banza/BANZA_REFERENCE.md` |
| §8 | Governança | **BANZA** | RFCs, ADRs, Validation Matrix, Validation domains. Protocol governance mechanisms. | `banza/BANZA_REFERENCE.md` |
| §9 | Modelo de Certificação | **BANZA** | Certification levels L0–L4, conformance suite, Operator Manifest schema, certification maintenance. Open to any certified entity. | `banza/BANZA_REFERENCE.md` |
| §10 | Federação | **BANZA** | Federation is a first-class protocol layer. Federation architecture, roadmap. Exists independently of Banzami. | `banza/BANZA_REFERENCE.md` |
| §11 | BanzAI | **BanzAI** | The entire BanzAI section (lines 929–1887) defines the Protocol Operating System. 16 modules, cognitive layer architecture, model routing, RAG, Protocol Graph, adversarial validation, quality dashboard. Serves the protocol ecosystem — not the Banzami product. | `banzai/BANZAI_REFERENCE.md` |
| §12 | Banzami para Programadores | **Banzami** | SDK integration examples, TypeScript SDK, Flutter SDK, webhooks, idempotency, sandbox. Describes Banzami's developer surface. | `banzami/BANZAMI_REFERENCE.md` |
| §13 | Banzami para Comerciantes | **Banzami** | QR static/dynamic, Banzami Business, payment links, T+0 settlement for merchants, levantamentos. Operator merchant product. | `banzami/BANZAMI_REFERENCE.md` |
| §14 | Para Consumidores | **Banzami** | Banzami Wallet, @banza identity as used by consumers, consumer security. Operator consumer product. | `banzami/BANZAMI_REFERENCE.md` |
| §15 | Segurança e Integridade Financeira | **SPLIT** | Financial invariant list → **BANZA** (protocol invariants). Security layers SVG, observability, sandbox separation → **Banzami** (implementation). | BANZA: invariants / Banzami: implementation |
| §16 | Sandbox e Ambiente de Testes | **Banzami** | Describes Banzami's sandbox environment. Sandbox API keys, funding tools, simulation tools. Specific to Banzami's implementation. | `banzami/BANZAMI_REFERENCE.md` |
| §17 | Por que Angola. Por que Agora. | **Banzami** | Operator mission statement. Product framing ("O problema que o Banzami resolve"). Angola-first positioning as an operator choice. | `banzami/BANZAMI_REFERENCE.md` |
| §18 | Roadmap | **SPLIT** | Protocol track items (conformance suite, federation RFC, certification levels) → **BANZA**. Product track items (Banzami Business, PHP SDK, acquiring) → **Banzami**. | BANZA: protocol track / Banzami: product track |
| §19 | Declaração de Visão | **SPLIT** | Protocol vision ("o protocolo é o que fica") → **BANZA**. Operator vision ("Banzami torna a economia angolana mais acessível") → **Banzami**. | BANZA: protocol vision / Banzami: operator vision |

---

## Ownership Summary

| Owner | Sections (primary) | Section splits |
|-------|-------------------|----------------|
| **BANZA** | §1, §2, §3, §4, §5, §7, §8, §9, §10 | §6 (protocol parts), §15 (invariants), §18 (protocol track), §19 (protocol vision) |
| **BanzAI** | §11 | — |
| **Banzami** | §12, §13, §14, §16, §17 | §6 (implementation), §15 (security implementation), §18 (product track), §19 (operator vision) |

---

## Lines Distribution (approximate)

| Owner | Approx. lines from source | % of document |
|-------|--------------------------|--------------|
| BANZA | ~1,100 lines (§1-10 + protocol splits) | ~49% |
| BanzAI | ~958 lines (§11 entire) | ~43% |
| Banzami | ~176 lines (§12-17 + product splits) | ~8% |

**Key finding:** The current combined document is 43% BanzAI content and only 8% Banzami-specific product content. This confirms the need for separation — BanzAI content dominates a document nominally describing the Banzami operator.

---

## ADR-016 Contamination (from CANONICAL_REFERENCE_AUDIT)

The existing document was audited and found:

| Severity | Count | Description |
|----------|-------|-------------|
| P0 | 3 | Architecture heading "dois níveis" (pre-ADR-025 mental model), ADR-016 reference citation, §1 SVG diagram (banza/docs legacy version) |
| P1 | 3 | §1 pillar attribution to Banzami (protocol properties), §11 BanzAI called "produto", §17 vision climax makes Banzami protagonist |
| P2 | 2 | §5 "fluxo de pagamento Banzami" (protocol invariant), §17 engineering commitment attributed to Banzami |

These issues resolve naturally when content is split into three separate files, because each file's framing makes the owner explicit from the first paragraph.

---

*Ownership matrix produced: 2026-05-30. No files modified.*
