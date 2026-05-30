---
title: REFERENCE_CROSS_REFERENCE_STRATEGY
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: REFERENCE-CANONICAL-SEPARATION-001
---

# Reference Cross-Reference Strategy

**Purpose:** Define the canonical patterns for cross-referencing between the three independent reference documents. Ensures each document remains self-consistent while directing readers to the authoritative source for out-of-scope content.

---

## The Cross-Reference Problem

When three independent documents replace one combined document, the risk is:

1. **Duplication** — BANZAMI_REFERENCE restates protocol invariants because they're needed for context
2. **Contradiction** — BANZAMI_REFERENCE defines T+0 slightly differently from BANZA_REFERENCE
3. **Opacity** — reader doesn't know where to find more detail
4. **Dead ends** — reader hits a concept without a navigation path to the authoritative source

The strategy below prevents all four failure modes.

---

## Universal Preamble Block

Every document opens with the same preamble structure, with only the "Scope" field changing:

```markdown
## Ecosystem Hierarchy

BANZA    = open financial infrastructure protocol
BanzAI   = Protocol Operating System
Banzami  = reference operator implementation

## Scope of This Document

This document defines only: **[BANZA PROTOCOL / BanzAI PROTOCOL OS / BANZAMI REFERENCE OPERATOR]**

Anything outside this scope is defined in:
- [BANZA_REFERENCE.md](../banza/BANZA_REFERENCE.md) — The BANZA open protocol (rules, invariants, certification, governance, federation)
- [BANZAI_REFERENCE.md](../banzai/BANZAI_REFERENCE.md) — The BanzAI Protocol OS (protocol intelligence, conformance, operator tooling)
- [BANZAMI_REFERENCE.md](../banzami/BANZAMI_REFERENCE.md) — The Banzami reference operator (wallets, merchant products, QR, SDKs, developer integration)
```

This block is rendered at the very top of each document, before the table of contents.

---

## Cross-Reference Trigger Patterns

### Pattern A — Protocol Invariant Mention in Banzami/BanzAI Document

**When:** A document other than BANZA_REFERENCE needs to mention a financial invariant (INV-*, MON-001, T+0, ledger rules).

**Format:**

```markdown
A liquidação T+0 é um invariante do protocolo BANZA — qualquer operador certificado deve implementá-la.  
Ver [BANZA_REFERENCE.md §7 — Invariantes Financeiros](../banza/BANZA_REFERENCE.md#7-invariantes-financeiros) para a definição normativa.
```

**Rule:** Never restate the invariant's definition. Only state what it means for this document's context. One sentence max.

---

### Pattern B — BanzAI Mention in BANZA/Banzami Document

**When:** BANZA_REFERENCE or BANZAMI_REFERENCE mentions BanzAI.

**Format (BANZA_REFERENCE):**

```markdown
### O Papel do BanzAI

O BanzAI é o Sistema Operativo do protocolo BANZA — a camada cognitiva que torna o protocolo acessível a operadores, programadores, reguladores e auditores. O BanzAI serve o protocolo; não é propriedade de nenhum operador.

Ver [BANZAI_REFERENCE.md](../banzai/BANZAI_REFERENCE.md) para arquitectura completa, módulos e capacidades.
```

**Format (BANZAMI_REFERENCE):**

```markdown
O BanzAI está disponível em `banzami.org/banzai`. Esta instância é alojada pelo Banzami como parte da implementação de referência. O BanzAI serve o protocolo BANZA — não o produto Banzami.

Ver [BANZAI_REFERENCE.md](../banzai/BANZAI_REFERENCE.md) para arquitectura e capacidades completas.
```

**Rule:** BanzAI gets one paragraph (max) in documents that don't own it. The paragraph must not describe BanzAI's internals.

---

### Pattern C — Banzami Mention in BANZA/BanzAI Document

**When:** BANZA_REFERENCE or BANZAI_REFERENCE mentions Banzami.

**Format (BANZA_REFERENCE):**

```markdown
O Banzami é o operador de referência — a primeira implementação certificada do protocolo BANZA. É um operador entre futuros muitos, não o proprietário do protocolo.

Ver [BANZAMI_REFERENCE.md](../banzami/BANZAMI_REFERENCE.md) para descrição completa dos produtos e experiências do operador.
```

**Rule:** Banzami is always described as "one operator" and "reference implementation" — never as the protocol owner. Never describe Banzami's products in detail in BANZA_REFERENCE.

---

### Pattern D — Certification Reference

**When:** BanzAI or Banzami documents mention certification.

**Format:**

```markdown
A certificação de operadores BANZA segue os níveis L0–L4 definidos no protocolo.  
Ver [BANZA_REFERENCE.md §9 — Modelo de Certificação](../banza/BANZA_REFERENCE.md#9-modelo-de-certificacao) para requisitos completos.

O BanzAI guia operadores no processo de certificação — ver [BANZAI_REFERENCE.md §5](../banzai/BANZAI_REFERENCE.md#5-as-seis-capacidades).
```

**Rule:** Certification rules live in BANZA_REFERENCE. BanzAI assistance lives in BANZAI_REFERENCE. Banzami's certification status is described in BANZAMI_REFERENCE.

---

### Pattern E — SDK Mention in Non-Banzami Document

**When:** BANZA_REFERENCE or BANZAI_REFERENCE mentions SDKs.

**Format (BANZA_REFERENCE — when listing protocol SDK requirements):**

```markdown
Todos os SDKs oficiais DEVEM implementar os requisitos de conformidade monetária (MON-001) e expor a superfície de API especificada nos contratos OpenAPI do protocolo. Ver [contracts/](./contracts/) para especificações.

O Banzami publica SDKs TypeScript, Flutter e PHP. Ver [BANZAMI_REFERENCE.md §4](../banzami/BANZAMI_REFERENCE.md#4-banzami-para-programadores) para exemplos de integração.
```

**Rule:** BANZA_REFERENCE defines SDK requirements. BANZAMI_REFERENCE provides SDK examples. BANZA_REFERENCE may point to examples but does not include them.

---

### Pattern F — Operator Product Mention in BANZA Document

**When:** BANZA_REFERENCE discusses the canonical payment experience (SCAN → CONFIRMAR → PAGO) without attributing it to Banzami.

**Format:**

```markdown
A experiência canónica de pagamento do protocolo:

**SCAN QR** → **CONFIRMAR** → **PAGO INSTANTANEAMENTE**

Esta experiência é definida pelo protocolo — qualquer operador certificado deve atingir este fluxo. O Banzami implementa-a como experiência de consumidor principal.

Ver [BANZAMI_REFERENCE.md §2 — Banzami Wallet](../banzami/BANZAMI_REFERENCE.md#2-banzami-wallet) para a implementação de referência.
```

**Rule:** Protocol defines the UX target. Banzami implements it. Never conflate the two.

---

## Bidirectional Anchors

Cross-references must be bidirectional where the connection is strong:

| From | To | Anchor phrase |
|------|----|--------------|
| `banza/BANZA_REFERENCE.md §7` (invariants) | `banzami/BANZAMI_REFERENCE.md §5` (implementation) | "Ver como o Banzami implementa estes invariantes em BANZAMI_REFERENCE §5." |
| `banzami/BANZAMI_REFERENCE.md §5` (implementation) | `banza/BANZA_REFERENCE.md §7` (invariants) | "Estas escolhas de implementação satisfazem os invariantes definidos em BANZA_REFERENCE §7." |
| `banza/BANZA_REFERENCE.md §9` (certification) | `banzai/BANZAI_REFERENCE.md §5` (BanzAI assists) | "O BanzAI guia operadores neste processo — ver BANZAI_REFERENCE §5." |
| `banzai/BANZAI_REFERENCE.md §5` (BanzAI assists) | `banza/BANZA_REFERENCE.md §9` (certification rules) | "As regras de certificação estão em BANZA_REFERENCE §9. O BanzAI explica-as." |
| `banza/BANZA_REFERENCE.md §5` (operator model) | `banzami/BANZAMI_REFERENCE.md §1` (Banzami is one operator) | "O Banzami é o operador de referência — ver BANZAMI_REFERENCE §1." |
| `banzami/BANZAMI_REFERENCE.md §1` (Banzami identity) | `banza/BANZA_REFERENCE.md §3` (protocol/operator distinction) | "A distinção protocolo/operador está definida em BANZA_REFERENCE §3." |

---

## Concepts That Require Protocol-Level References

The following concepts must ALWAYS cross-reference BANZA_REFERENCE when used in BanzAI or Banzami documents:

| Concept | Authoritative Location |
|---------|----------------------|
| T+0 settlement invariant | `banza/BANZA_REFERENCE.md §7 — INV-STL-*` |
| Double-entry ledger | `banza/BANZA_REFERENCE.md §7 — INV-LEDGER-*` |
| Integer monetary representation | `banza/BANZA_REFERENCE.md §6 — MON-001` |
| Certification levels L0-L4 | `banza/BANZA_REFERENCE.md §9` |
| Operator Manifesto schema | `banza/BANZA_REFERENCE.md §9` |
| @banza handle format rules | `banza/BANZA_REFERENCE.md §3` |
| `gross_minor = net_minor + fee_minor` | `banza/BANZA_REFERENCE.md §6 — INV-STL-001` |
| `balance_minor = available_minor + reserved_minor` | `banza/BANZA_REFERENCE.md §6 — INV-WALLET-001` |
| Federation requirements | `banza/BANZA_REFERENCE.md §10` |
| RFC/ADR governance | `banza/BANZA_REFERENCE.md §8` |

---

## Concepts That Require BanzAI References

| Concept | Authoritative Location |
|---------|----------------------|
| Protocol knowledge retrieval | `banzai/BANZAI_REFERENCE.md §4` |
| Conformance copilot | `banzai/BANZAI_REFERENCE.md §6` |
| Operator Digital Twin | `banzai/BANZAI_REFERENCE.md §6` |
| Federation Intelligence | `banzai/BANZAI_REFERENCE.md §6` |
| "Tools determine truth. AI explains truth." | `banzai/BANZAI_REFERENCE.md §7` |
| Protocol Graph | `banzai/BANZAI_REFERENCE.md §4` |

---

## Anti-Patterns to Avoid

| Anti-pattern | Why it fails | Correct pattern |
|-------------|-------------|-----------------|
| Restating INV-LEDGER-001 in BANZAMI_REFERENCE | Creates two sources of truth for the invariant | Cross-reference BANZA_REFERENCE §7 |
| Describing BanzAI's RAG system in BANZA_REFERENCE | BanzAI owns its own architecture | Reference BANZAI_REFERENCE |
| Describing Banzami's SDK API in BANZA_REFERENCE | SDK examples are operator-level | Reference BANZAMI_REFERENCE §4 |
| "Banzami's T+0 settlement" without protocol attribution | T+0 is a protocol invariant, not an operator feature | "T+0 (BANZA protocol invariant, see §7)" |
| Certification rules restated in BANZAMI_REFERENCE | Creates drift risk | One sentence + cross-reference |
| BanzAI described as "Banzami's AI assistant" anywhere | Violates ADR-025 BanzAI identity | "BanzAI is the Protocol OS, hosted by Banzami" |

---

*Cross-reference strategy produced: 2026-05-30. No files modified.*
