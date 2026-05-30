---
title: REFERENCE_INFORMATION_ARCHITECTURE_V2
version: 1.0
date: 2026-05-30
status: DESIGN COMPLETE — pending execution authorization
---

# Reference Information Architecture V2

**Purpose:** Define the complete information architecture for BANZAMI_REFERENCE.md V2 — section hierarchy, table of contents structure, cross-reference map, reading paths by audience, and navigation design principles.

---

## 1. Section Hierarchy

```
BANZAMI_REFERENCE.md V2
│
├── PARTE I — O PROTOCOLO
│   ├── §1  O Problema: Angola Tem as Peças
│   │       angola-has-inventory · protocol-gap · symptom-cause-map
│   ├── §2  A Camada que Falta
│   │       protocol-layer-definition · pix-upi-mpesa · open-vs-closed
│   ├── §3  O que é o BANZA
│   │       canonical-definition · three-tier-hierarchy · four-principles · identity-distinctions
│   ├── §4  Governança do Protocolo
│   │       rfcs · adrs · validation-matrix · validation-domains
│   ├── §5  Modelo de Certificação
│   │       conformance-suite · certification-levels · operator-manifesto · open-access
│   ├── §6  Regras do Protocolo — Especificações Técnicas
│   │       monetary-representation · financial-invariants · ledger-model · t+0-invariant · traceability
│   └── §7  Federação
│           federation-architecture · current-state · roadmap
│
├── PARTE II — O SISTEMA OPERATIVO
│   ├── §8  O Problema do Conhecimento do Protocolo
│   │       adoption-bottleneck · knowledge-gap · without-banzai
│   └── §9  BanzAI
│           protocol-os · 6-capabilities · architecture · 16-modules · security
│
├── PARTE III — OS OPERADORES
│   └── §10 O Modelo de Operadores
│           operator-definition · who-can-certify · operator-registry · operator-manifesto
│
└── PARTE IV — BANZAMI
    ├── §11 Banzami — A Implementação de Referência
    │       reference-impl · four-products · pix-nubank-analogy
    ├── §12 Para Programadores
    │       why-banza · typescript-sdk · flutter-sdk · webhooks · idempotency · sandbox
    ├── §13 Para Comerciantes
    │       why-not-tpa · qr-static-dynamic · t+0 · business · payment-links
    ├── §14 Para Consumidores
    │       wallet · @banza-identity · consumer-security
    ├── §15 Arquitectura Técnica de Referência
    │       stack · services-topology · security · observability · environment-separation
    ├── §16 Sandbox e Ambiente de Testes
    │       two-environments · sandbox-tools
    ├── §17 Roadmap
    │       banza-protocol-track · banzami-product-track
    └── §18 Declaração de Visão
            protocol-vision · ecosystem-vision · closing-identity-anchor
```

---

## 2. Table of Contents Structure (V2)

The V2 table of contents must visually communicate the architecture. Part labels are mandatory — they tell the reader what they are about to encounter before they read section titles.

```
## Índice

### Parte I — O Protocolo
1. O Problema: Angola Tem as Peças
2. A Camada que Falta
3. O que é o BANZA
4. Governança do Protocolo
5. Modelo de Certificação
6. Regras do Protocolo — Especificações Técnicas
7. Federação

### Parte II — O Sistema Operativo
8. O Problema do Conhecimento do Protocolo
9. BanzAI

### Parte III — Os Operadores
10. O Modelo de Operadores

### Parte IV — Banzami
11. Banzami — A Implementação de Referência
12. Para Programadores
13. Para Comerciantes
14. Para Consumidores
15. Arquitectura Técnica de Referência
16. Sandbox e Ambiente de Testes
17. Roadmap
18. Declaração de Visão
```

**Design principle:** The four-part label is the first signal to every reader. Before reading a single section, they see: this document is about a Protocol, an Operating System, Operators, and a Reference Implementation — in that order.

---

## 3. Cross-Reference Map

Which sections must reference which other sections, and what the reference should say.

| From | To | Required reference |
|------|----|--------------------|
| §1 | §2 | "O que é a camada de protocolo que falta?" → §2 |
| §2 | §3 | "O que é o BANZA, exactamente?" → §3 |
| §2 | §5 | Pix/UPI open certification → §5 (BANZA's certification model) |
| §3 | §4 | "Como é que as regras se mantêm abertas?" → §4 |
| §3 | §11 | "Banzami é o operador de referência" → §11 |
| §4 | §5 | "Governança define as regras; certificação verifica a implementação" → §5 |
| §5 | §6 | "O que é que a certificação verifica?" → §6 |
| §5 | §10 | "Como funciona o modelo de operadores?" → §10 |
| §6 | §15 | "Como o Banzami implementa estas especificações" → §15 |
| §7 | §10 | "Federação requer múltiplos operadores" → §10 |
| §8 | §9 | "BanzAI resolve este problema" → §9 |
| §9 | §10 | "BanzAI serve operadores" → §10 |
| §10 | §11 | "Banzami é o operador de referência" → §11 |
| §11 | §12 | "Para programadores, o SDK é a interface" → §12 |
| §11 | §13 | "Para comerciantes, o QR é a interface" → §13 |
| §11 | §14 | "Para consumidores, a wallet é a interface" → §14 |
| §12 | §6 | SDK enforces protocol invariants → §6 |
| §15 | §6 | "These are Banzami's choices; §6 has the protocol rules" → §6 |
| §17 | §7 | BANZA Protocol track → §7 (federation roadmap) |

---

## 4. Reading Paths by Audience

Different visitors need different paths through the reference. The V2 architecture supports four canonical reading paths.

### Path A — "What is BANZA?" (General Visitor, 10 minutes)

```
§1 → §2 → §3 → §10 → §11
```

After this path, the visitor can say:
- BANZA is the protocol layer Angola lacks
- Like Pix/UPI, not M-Pesa
- Any operator can certify
- Banzami is the reference operator, not the protocol owner

**Entry point:** Homepage → Reference (§1 should be visible from homepage link)

---

### Path B — "I want to become an operator" (Operator / Institution)

```
§1 → §2 → §3 → §4 → §5 → §6 → §7 → §9 → §10
```

After this path, the visitor can say:
- I understand what the protocol requires
- I understand the governance model
- I understand certification levels and process
- I understand the financial invariants I must implement
- I understand what BanzAI will help me with
- I know how to start the certification process

**Entry point:** /operators page → Reference (link to §5 specifically)

---

### Path C — "I'm a developer who wants to integrate" (Developer)

```
§1 → §3 → §6 → §12
```

After this path, the visitor can say:
- I understand why BANZA vs. Stripe/Flutterwave
- I understand the protocol guarantees I'm building on
- I have working SDK examples
- I know where the sandbox is

**Entry point:** /programadores page → Reference (link to §12 specifically)

---

### Path D — "I'm a regulator or auditor" (Regulator / Auditor)

```
§2 → §3 → §4 → §5 → §6 → §7 → §9
```

After this path, the visitor can say:
- I understand the protocol model (open vs. closed)
- I understand the governance structure (RFCs, ADRs)
- I understand the certification model
- I understand the financial invariants and how they are enforced
- I understand the BanzAI verification capabilities
- I understand the federation roadmap

**Entry point:** Direct → §4 (Governança)

---

### Path E — "I'm a consumer or merchant curious about Banzami" (Consumer / Merchant)

```
§11 → §13 or §14
```

After this path, the visitor can say:
- Banzami is built on an open protocol (§11 framing)
- Here's how QR payments work for my business (§13)
- Here's how the wallet works (§14)

**Entry point:** /comerciantes or /consumers page → Reference (link to §13/§14)

---

## 5. Navigation Design Principles

### Principle 1 — Parts are mandatory navigation units

The four-part structure must be visible in the sidebar/table of contents. Not just section numbers — the part labels. A reader must be able to jump directly to "PARTE I — O PROTOCOLO" without reading through everything.

### Principle 2 — §1-§3 are always one scroll away from any entry

Whatever page a visitor enters from, the first three sections of the reference (Problem, Protocol Gap, What is BANZA) must be reachable in one click. These sections are the canonical answer to "What is BANZA?" — they must be the most accessible sections.

### Principle 3 — The protocol/Banzami boundary must be visible

The transition from §10 (Operators) to §11 (Banzami) is the most important structural boundary in the document. It is the moment the document transitions from "the protocol" to "one implementation." This boundary must be visually distinct:
- Part label: "PARTE IV — BANZAMI"
- Opening framing of §11 must make the distinction explicit

### Principle 4 — Cross-part navigation anchors

Each section should have a visible "next / previous" or "see also" reference at the bottom. Navigation between §6 (Protocol Specs) and §15 (Banzami Implementation) should be bidirectional and labeled: "Protocol rules are in §6 — this section shows how Banzami implements them."

### Principle 5 — The reading path labels are surfaced on the website

The four reading paths (operator, developer, regulator, consumer/merchant) should correspond to visible entry points on the website. The /operators page links to Path B. The /programadores page links to Path C. The /banzamia page links to BanzAI section (§9). Each path starts where the visitor already is.

---

## 6. Section Length Targets

For prose discipline. Current §9 (BanzAI) is approximately 800 lines — longer than all other sections combined.

| § | Section | V1 approx. lines | V2 target |
|---|---------|-----------------|-----------|
| 1 | O Problema | 15 (was §15) | 80–100 |
| 2 | A Camada que Falta | 0 (new) | 80–100 |
| 3 | O que é o BANZA | ~40 (was §1) | 60–80 |
| 4 | Governança | ~50 (was §6) | 50–70 |
| 5 | Certificação | ~60 (was §7) | 60–80 |
| 6 | Especificações Técnicas | ~350 (§4+§5 protocol parts) | 300–350 |
| 7 | Federação | ~50 (was §8) | 50–70 |
| 8 | Problema do Conhecimento | 0 (elevated subsection) | 30–50 |
| 9 | BanzAI | ~800 (was §9) | 700–800 |
| 10 | Modelo de Operadores | ~20 (was §3 subsection) | 60–80 |
| 11 | Banzami (reference impl.) | 0 (new section) | 40–60 |
| 12 | Para Programadores | ~90 (was §10) | 100–120 |
| 13 | Para Comerciantes | ~50 (was §11) | 60–80 |
| 14 | Para Consumidores | ~30 (was §12) | 30–50 |
| 15 | Arquitectura Técnica | ~100 (§4 impl. parts) | 80–100 |
| 16 | Sandbox | ~30 (was §14) | 30–50 |
| 17 | Roadmap | ~30+new protocol track | 80–120 |
| 18 | Declaração de Visão | ~100 (was §17) | 80–100 |
| **Total** | | **~1880 lines** | **~1800–1900 lines** |

The document should not grow significantly in total length. New content (§1 expanded, §2 new, §8 elevated, §10 expanded, §11 new, §17 protocol track) is offset by reorganization. The BanzAI section (§9) is the only section that should remain near its current length.

---

*Architecture completed: 2026-05-30. No files modified.*
