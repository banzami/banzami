---
title: REFERENCE_SEPARATION_PLAN
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: REFERENCE-CANONICAL-SEPARATION-001
---

# Reference Separation Plan

**Purpose:** Define the scope, structure, forbidden content, and success criteria for each of the three independent canonical reference documents.

**Context:** The existing `banzami/docs/BANZA_REFERENCE.md` is a combined reference covering all three ecosystem layers in a single 2234-line document. This plan specifies the three independent canonical references that will replace it conceptually (while the combined file continues to serve the banzami.org website).

---

## Document Registry

| Document | Location | Owner | Audience |
|----------|----------|-------|----------|
| `BANZA_REFERENCE.md` | `~/banza/BANZA_REFERENCE.md` | BANZA protocol | Regulators, institutional partners, future operators, protocol contributors |
| `BANZAI_REFERENCE.md` | `~/banzai/BANZAI_REFERENCE.md` | BanzAI Protocol OS | Operators using BanzAI, developers integrating BanzAI, protocol auditors |
| `BANZAMI_REFERENCE.md` | `~/banzami/BANZAMI_REFERENCE.md` | Banzami reference operator | Merchants, consumers, developers integrating with Banzami, Banzami partners |

---

## Document 1: BANZA_REFERENCE.md

### Identity

> **This document defines the BANZA open financial infrastructure protocol.**  
> BANZA exists independently of any operator. If all operators ceased operations tomorrow, this document would remain valid.

### Scope

**Must answer:**
- What is the BANZA protocol?
- Why does Angola need a protocol layer (not just a product)?
- What rules must any operator implement to be certified?
- How does governance work (RFCs, ADRs)?
- What are the financial invariants?
- How does certification work?
- What is the federation model?
- What is the protocol roadmap?

**Must NOT answer:**
- How does the Banzami wallet work?
- How does the Banzami merchant dashboard work?
- What does BanzAI's RAG system do internally?
- What are Banzami's specific SDK examples?

### Section Structure

```
## Ecosystem Hierarchy

## Scope

## 1. O Problema: Angola Tem as Peças

## 2. A Camada que Falta

## 3. O que é o BANZA
   ### Arquitectura de três níveis
   ### O que é o BANZA (concrete definition)
   ### O que o BANZA não é
   ### Os quatro princípios do protocolo
   ### A distinção fundamental: protocolo ≠ operador

## 4. Princípios Fundamentais

## 5. Arquitectura do Ecossistema
   ### Kernel Banza
   ### Operadores
   ### Governança

## 6. Representação Monetária (normativa)
   ### Regra de Inteiros
   ### Convenção *_minor
   ### Invariantes monetários
   ### Conformance — MON-001

## 7. Invariantes Financeiros
   ### Ledger invariants (INV-LEDGER-*)
   ### Wallet invariants (INV-WALLET-*)
   ### Settlement invariants (INV-STL-*)
   ### Traceability invariants (INV-TRACE-*)

## 8. Governança do Protocolo
   ### RFCs
   ### ADRs
   ### Validation Matrix
   ### Validation Domains

## 9. Modelo de Certificação
   ### Certification levels L0–L4
   ### Operator Manifesto
   ### Certification process
   ### Open access principle

## 10. Federação
    ### Architecture
    ### Current state
    ### Roadmap

## 11. Roadmap do Protocolo

## 12. Declaração de Visão do Protocolo

## References
```

### Forbidden Content

The following concepts must NOT appear as primary subjects:
- Banzami-specific products (Banzami Business, Banzami Wallet as product descriptions)
- BanzAI internal architecture (RAG, Protocol Graph, 16 modules)
- SDK code examples (belong in BANZAMI_REFERENCE)
- Operator-specific operational procedures

BanzAI may be mentioned exactly once — in the ecosystem hierarchy section — with a cross-reference to `BANZAI_REFERENCE.md`. It must NOT be described in detail.

Banzami may be mentioned as the reference operator — with a cross-reference to `BANZAMI_REFERENCE.md`. Banzami's products must NOT be described.

### Canonical Framing Principle

Every section must pass this test:

> "Would this still be true if Banzami were replaced by a different operator tomorrow?"

If YES → the content belongs here.  
If NO → the content belongs in `BANZAMI_REFERENCE.md`.

---

## Document 2: BANZAI_REFERENCE.md

### Identity

> **This document defines BanzAI — the Protocol Operating System for the BANZA financial infrastructure.**  
> BanzAI serves the BANZA ecosystem. It is not a Banzami product. It is not a consumer chatbot. It exists for operators, developers, regulators, and auditors working with the BANZA protocol.

### Scope

**Must answer:**
- What is BanzAI?
- Why does the BANZA protocol need an Operating System?
- What are BanzAI's capabilities?
- How is BanzAI architectured (at the system level)?
- How does BanzAI differ from generic AI assistants?
- What does BanzAI's knowledge system look like?
- What is BanzAI's security posture?
- What is BanzAI's roadmap?

**Must NOT define:**
- Protocol rules (belongs in BANZA_REFERENCE)
- Operator policies (belongs in BANZAMI_REFERENCE)
- Certification ownership (certification belongs to BANZA protocol — BanzAI assists, does not own)
- Consumer product features (Banzami wallet, QR scanner — belongs in BANZAMI_REFERENCE)

### Section Structure

```
## Ecosystem Hierarchy

## Scope

## 1. O que é o BanzAI

## 2. Por que Existe o BanzAI
   ### O Fosso de Conhecimento do Protocolo
   ### O que acontece sem BanzAI

## 3. BanzAI como Camada Cognitiva

## 4. Arquitectura do Sistema
   ### Technology stack
   ### Model routing strategy
   ### Knowledge retrieval (RAG)
   ### Protocol Graph
   ### Deterministic tools

## 5. As Seis Capacidades
   ### Compreender
   ### Explicar
   ### Validar
   ### Simular
   ### Certificar
   ### Federar

## 6. Os 16 Módulos
   ### Camada de Protocolo
   ### Camada de Operador
   ### Camada de Inteligência

## 7. O Princípio de Verdade
   ### Ferramentas determinam a verdade. A IA explica a verdade.
   ### Adversarial validation

## 8. Postura de Segurança

## 9. Modos de Deployment

## 10. Avaliação de Qualidade

## 11. Roadmap do BanzAI

## References
```

### Forbidden Content

- BanzAI must not be described as "a Banzami product" or "a Banzami feature"
- BanzAI must not define protocol rules (reference them, do not own them)
- BanzAI must not describe Banzami consumer/merchant experiences
- BanzAI's hosting by Banzami is acknowledged (one sentence) — not positioned as ownership

### Canonical Framing Principle

> "BanzAI serves the protocol. The protocol does not serve BanzAI."

Every BanzAI capability must be described in terms of how it serves protocol understanding, not how it serves Banzami's product goals.

---

## Document 3: BANZAMI_REFERENCE.md

### Identity

> **This document defines Banzami — the reference operator implementation of the BANZA financial infrastructure protocol.**  
> Banzami is one implementation of BANZA. The protocol is not owned by Banzami. The protocol exists independently of Banzami.

### Scope

**Must answer:**
- What is Banzami?
- What is Banzami's role in the BANZA ecosystem?
- What products does Banzami offer (wallet, Business, QR, checkout, pay links)?
- How do consumers use Banzami?
- How do merchants use Banzami?
- How do developers integrate with Banzami?
- What are Banzami's APIs and SDKs?
- How does Banzami's deployment work?
- What is Banzami's product roadmap?

**Must NOT redefine:**
- Protocol rules (reference BANZA_REFERENCE, do not restate)
- Protocol invariants (do not restate — point to BANZA_REFERENCE §7)
- Certification requirements (point to BANZA_REFERENCE §9)
- BanzAI architecture (point to BANZAI_REFERENCE)

### Section Structure

```
## Ecosystem Hierarchy

## Scope

## 1. O que é o Banzami
   ### Papel no Ecossistema
   ### Banzami não é o protocolo
   ### O que Banzami oferece

## 2. Banzami Wallet (Consumidores)
   ### Carregar carteira
   ### Pagar por QR
   ### Transferências P2P
   ### Identidade @banza

## 3. Banzami Business (Comerciantes)
   ### Onboarding
   ### Interface móvel
   ### Interface web
   ### QR estático e dinâmico
   ### Payment links
   ### Levantamentos

## 4. Banzami para Programadores
   ### SDK TypeScript
   ### SDK Flutter
   ### SDK PHP
   ### Webhooks
   ### Idempotência
   ### Sandbox

## 5. Arquitectura Técnica de Referência
   ### Stack tecnológico
   ### Topologia de serviços
   ### Segurança
   ### Observabilidade

## 6. Sandbox e Ambiente de Testes

## 7. Missão e Posicionamento
   ### Por que Angola
   ### O que o Banzami resolve
   ### Princípios operacionais

## 8. Roadmap do Produto

## 9. Declaração de Visão

## References
```

### Forbidden Content

- Banzami must not describe itself as "the protocol" or "the infrastructure"
- Banzami must not restate protocol invariants as if they were operator policies
- Banzami must not describe BanzAI's internal architecture
- "Banzami ecosystem" must not appear — it is the BANZA ecosystem

### Canonical Framing Principle

> "Banzami implements the protocol. The protocol does not belong to Banzami."

Every Banzami feature must be framed as: "Banzami implements [protocol capability] as [product feature]."

Example: "Banzami implements the BANZA QR-native principle as the Banzami QR product — static QR codes for physical merchants and dynamic QR codes for per-transaction payment."

---

## Relationship Between Documents

```
BANZA_REFERENCE.md          BANZAI_REFERENCE.md         BANZAMI_REFERENCE.md
─────────────────           ──────────────────          ────────────────────
"The protocol"              "The OS"                    "The implementation"

"Here are the rules."       "Here is how to navigate    "Here is how we
                            the rules."                 implement the rules."

"Any operator who passes   "Any protocol participant    "One specific operator."
certification can use       can use BanzAI."
the protocol."
```

### Canonical Cross-Reference Format

Every document begins with:

```markdown
## Ecosystem Hierarchy

BANZA → Open financial infrastructure protocol
BanzAI → Protocol Operating System
Banzami → Reference operator implementation

## Scope

This document defines only: [PROTOCOL / PROTOCOL OS / BANZAMI REFERENCE OPERATOR]

Anything outside this scope is defined in:
- [BANZA_REFERENCE.md](../banza/BANZA_REFERENCE.md) — The BANZA open protocol
- [BANZAI_REFERENCE.md](../banzai/BANZAI_REFERENCE.md) — The BanzAI Protocol OS
- [BANZAMI_REFERENCE.md](../banzami/BANZAMI_REFERENCE.md) — The Banzami reference operator
```

---

## Migration Strategy

### What is NOT changing

`banzami/docs/BANZA_REFERENCE.md` continues to exist unchanged. It serves as the source of truth for the banzami.org website (`apps/docs` reads it at build time). This file is not deprecated.

### What is new

Three new independent canonical references are created alongside the existing combined file. They serve different audiences:

| File | Purpose | Read by |
|------|---------|---------|
| `banzami/docs/BANZA_REFERENCE.md` | Website content source | `apps/docs` build system |
| `banza/BANZA_REFERENCE.md` | Protocol canonical reference | Protocol contributors, regulators |
| `banzai/BANZAI_REFERENCE.md` | BanzAI OS canonical reference | Operators, developers using BanzAI |
| `banzami/BANZAMI_REFERENCE.md` | Operator canonical reference | Merchants, consumers, app developers |

### Content Authority

When content in the three canonical references conflicts with content in `banzami/docs/BANZA_REFERENCE.md`:
- The canonical reference for the owning layer is authoritative for that layer's rules
- `banzami/docs/BANZA_REFERENCE.md` is authoritative for what appears on the website
- Website updates must be preceded by updates to the canonical reference

---

*Separation plan produced: 2026-05-30. No files modified.*
