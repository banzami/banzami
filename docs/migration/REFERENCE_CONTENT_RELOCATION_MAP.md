---
title: REFERENCE_CONTENT_RELOCATION_MAP
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: REFERENCE-CANONICAL-SEPARATION-001
---

# Reference Content Relocation Map

**Purpose:** For every section and subsection of the existing combined `banzami/docs/BANZA_REFERENCE.md`, specify the relocation action and destination document.

**Actions:**

| Action | Meaning |
|--------|---------|
| `KEEP` | Moves to the owning document with no content change |
| `MOVE` | Moves to the owning document; opening paragraph reframed |
| `SPLIT` | Section split — parts go to different documents |
| `REFERENCE` | Content stays in one document; other documents get a cross-reference link |
| `ABSORB` | Content merged into another section |

---

## Section Relocation Table

### §1 — O Problema: Angola Tem as Peças (lines ~39–99)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Full section (Angola payment gap) | `KEEP` | `banza/BANZA_REFERENCE.md §1` | Protocol problem framing. No change needed. |
| — | — | — | Zero duplication in Banzami or BanzAI docs. |

---

### §2 — A Camada que Falta (lines ~103–207)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Uma analogia (road network) | `KEEP` | `banza/BANZA_REFERENCE.md §2` | Pure protocol concept. |
| Liquidação vs. protocolo | `KEEP` | `banza/BANZA_REFERENCE.md §2` | Protocol distinction. |
| Dois modelos (M-Pesa vs Pix/UPI) | `KEEP` | `banza/BANZA_REFERENCE.md §2` | Protocol open/closed model. |
| A diferença estrutural (comparison table) | `KEEP` | `banza/BANZA_REFERENCE.md §2` | Protocol. |
| O que acontece se o Banzami desaparecer? | `KEEP` | `banza/BANZA_REFERENCE.md §2` | Protocol survivability argument — defines why protocol ≠ operator. |

---

### §3 — O que é o BANZA (lines ~211–373)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Arquitectura de três níveis | `MOVE` | `banza/BANZA_REFERENCE.md §3` | Reframe heading: remove "dois níveis" (P0 audit finding). Use ADR-025 three-tier model. |
| O que é o BANZA (concrete definition) | `KEEP` | `banza/BANZA_REFERENCE.md §3` | Core protocol definition. |
| O que o BANZA não é (table) | `KEEP` | `banza/BANZA_REFERENCE.md §3` | Protocol boundary definitions. |
| Os quatro princípios | `MOVE` | `banza/BANZA_REFERENCE.md §3` | Reframe: "Estes são invariantes do protocolo — não funcionalidades do Banzami." (addresses P1 audit finding) |
| A distinção fundamental: protocolo ≠ operador | `KEEP` | `banza/BANZA_REFERENCE.md §3` | Core protocol/operator distinction. |
| O papel do BanzAI | `REFERENCE` | `banza/BANZA_REFERENCE.md §3` | Keep 1-paragraph summary + "Ver BANZAI_REFERENCE.md para arquitectura completa." |
| A experiência canónica (SCAN → CONFIRMAR → PAGO) | `KEEP` | `banza/BANZA_REFERENCE.md §3` | Protocol-level UX invariant. |
| O nome (etymology) | `SPLIT` | BANZA: Banza etymology / Banzami: Banzami etymology | Each document gets its own name explanation. |

---

### §4 — Princípios Fundamentais (lines ~376–401)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Ferramentas determinam a verdade | `REFERENCE` | `banza/BANZA_REFERENCE.md §4` (1 line) + full treatment in `banzai/BANZAI_REFERENCE.md §7` | Principle belongs to BanzAI section. BANZA section cites it. |
| A correcção financeira não é negociável | `KEEP` | `banza/BANZA_REFERENCE.md §4` | Protocol invariant principle. |
| O protocolo é o produto | `KEEP` | `banza/BANZA_REFERENCE.md §4` | Core protocol/product distinction. |
| Os operadores implementam política. O Kernel implementa o protocolo. | `KEEP` | `banza/BANZA_REFERENCE.md §4` | Protocol architecture principle. |
| Rastreabilidade por defeito | `KEEP` | `banza/BANZA_REFERENCE.md §4` | Protocol property. |
| Angola primeiro | `SPLIT` | `banza/BANZA_REFERENCE.md §4` (1 sentence) + `banzami/BANZAMI_REFERENCE.md §7` (full treatment) | The protocol is Angola-first by design. Banzami's operator strategy is also Angola-first. Different reasons. |

---

### §5 — Visão Geral do Ecossistema (lines ~404–447)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Kernel Banza (18 crates table) | `KEEP` | `banza/BANZA_REFERENCE.md §5` | Protocol kernel definition. |
| Operadores (model definition) | `KEEP` | `banza/BANZA_REFERENCE.md §5` | Protocol operator model. |
| Operador de Referência | `REFERENCE` | `banza/BANZA_REFERENCE.md §5` (1 sentence) + cross-ref to BANZAMI_REFERENCE | BANZA defines the reference operator concept. Banzami is the instance. |
| Operador Sandbox | `KEEP` | `banza/BANZA_REFERENCE.md §5` | Protocol concept. |
| Operadores Certificados | `KEEP` | `banza/BANZA_REFERENCE.md §5` | Protocol concept. |

---

### §6 — Arquitectura Técnica (lines ~451–523)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Stack tecnológico (Rust/Go table) | `SPLIT` | `banza/BANZA_REFERENCE.md §5` (protocol stack rationale) + `banzami/BANZAMI_REFERENCE.md §5` (Banzami's implementation choices) | The Rust/Go/PostgreSQL choice is a protocol-level decision (other operators may differ). Banzami's specific implementation is operator-level. |
| Topologia de serviços (SVG) | `MOVE` | `banzami/BANZAMI_REFERENCE.md §5` | Banzami's specific service topology. Other operators may have different topologies. |
| O ledger de dupla entrada | `KEEP` | `banza/BANZA_REFERENCE.md §6` | Protocol ledger model and invariants. |
| Invariantes financeiros (INV-* table) | `KEEP` | `banza/BANZA_REFERENCE.md §7` | Protocol financial invariants. |
| Sistema de rastreabilidade | `KEEP` | `banza/BANZA_REFERENCE.md §7` | Protocol traceability requirement. |

---

### §7 — Representação Monetária (lines ~525–786)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Regra de Inteiros | `KEEP` | `banza/BANZA_REFERENCE.md §6` | Protocol normative rule. |
| Convenção `*_minor` | `KEEP` | `banza/BANZA_REFERENCE.md §6` | Protocol naming standard. |
| Porquê Inteiros | `KEEP` | `banza/BANZA_REFERENCE.md §6` | Protocol rationale. |
| Semântica de Montantes (gross/net/fee) | `MOVE` | `banza/BANZA_REFERENCE.md §6` | Reframe: "Todo o fluxo de pagamento BANZA produz..." (not "Banzami"). Addresses P2 audit finding. |
| Semântica de Saldo de Carteira | `KEEP` | `banza/BANZA_REFERENCE.md §6` | Protocol wallet balance semantics. |
| Registo de Moedas (AOA, USD, EUR) | `KEEP` | `banza/BANZA_REFERENCE.md §6` | Protocol currency registry. |
| Requisitos de Conformidade Monetária | `KEEP` | `banza/BANZA_REFERENCE.md §6` | Protocol conformance rules for operators. |
| Requisitos para SDKs | `KEEP` | `banza/BANZA_REFERENCE.md §6` | Protocol SDK requirements. |
| Regra MON-001 | `KEEP` | `banza/BANZA_REFERENCE.md §6` | Protocol certification rule. |
| CONFORMANCE-MON-001 | `KEEP` | `banza/BANZA_REFERENCE.md §6` | Protocol conformance vector. |

---

### §8 — Governança (lines ~791–836)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| RFCs | `KEEP` | `banza/BANZA_REFERENCE.md §8` | Protocol governance. |
| ADRs | `KEEP` | `banza/BANZA_REFERENCE.md §8` | Protocol governance. |
| Validation Matrix | `KEEP` | `banza/BANZA_REFERENCE.md §8` | Protocol governance. |
| Domínios de validação | `KEEP` | `banza/BANZA_REFERENCE.md §8` | Protocol governance. |

---

### §9 — Modelo de Certificação (lines ~839–889)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Níveis de certificação (L0-L4 table) | `KEEP` | `banza/BANZA_REFERENCE.md §9` | Protocol certification levels. |
| Processo de certificação (SVG) | `KEEP` | `banza/BANZA_REFERENCE.md §9` | Protocol process. |
| Manifesto de Operador | `KEEP` | `banza/BANZA_REFERENCE.md §9` | Protocol standard schema. |
| Manutenção de certificação | `KEEP` | `banza/BANZA_REFERENCE.md §9` | Protocol requirement. |

---

### §10 — Federação (lines ~896–925)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Estado actual | `KEEP` | `banza/BANZA_REFERENCE.md §10` | Protocol federation state. |
| Arquitectura de federação | `KEEP` | `banza/BANZA_REFERENCE.md §10` | Protocol federation architecture. |
| Roadmap de federação | `KEEP` | `banza/BANZA_REFERENCE.md §10` | Protocol roadmap. |

---

### §11 — BanzAI (lines ~929–1887)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Porquê existe o BanzAI | `KEEP` | `banzai/BANZAI_REFERENCE.md §2` | BanzAI rationale. |
| O Fosso de Conhecimento do Protocolo | `KEEP` | `banzai/BANZAI_REFERENCE.md §2` | BanzAI problem definition. |
| Por que é diferente de IA genérica | `KEEP` | `banzai/BANZAI_REFERENCE.md §1` | BanzAI identity. |
| BanzAI como Camada Cognitiva (4 layers) | `KEEP` | `banzai/BANZAI_REFERENCE.md §3` | BanzAI architecture concept. |
| Por que quase nenhum protocolo tem isto | `KEEP` | `banzai/BANZAI_REFERENCE.md §3` | BanzAI differentiation. |
| O que acontece sem BanzAI | `KEEP` | `banzai/BANZAI_REFERENCE.md §2` | BanzAI impact. |
| Arquitectura do Produto (16 modules) | `KEEP` | `banzai/BANZAI_REFERENCE.md §6` | BanzAI module architecture. |
| Arquitectura Canónica do Ecossistema | `REFERENCE` | `banzai/BANZAI_REFERENCE.md §3` (1 paragraph) | Full diagram reference; ecosystem is BANZA-owned. |
| Como o BanzAI Funciona | `KEEP` | `banzai/BANZAI_REFERENCE.md §4` | BanzAI internal architecture. |
| Estratégia de Modelos de IA | `KEEP` | `banzai/BANZAI_REFERENCE.md §4` | BanzAI model routing. |
| Recuperação de Conhecimento (RAG) | `KEEP` | `banzai/BANZAI_REFERENCE.md §4` | BanzAI knowledge system. |
| Modelo de Verdade do Protocolo | `KEEP` | `banzai/BANZAI_REFERENCE.md §7` | BanzAI epistemology. |
| Ferramentas Determinísticas | `KEEP` | `banzai/BANZAI_REFERENCE.md §7` | BanzAI tools. |
| Modos de Deployment | `KEEP` | `banzai/BANZAI_REFERENCE.md §9` | BanzAI operational modes. |
| Avaliação da Qualidade de Recuperação | `KEEP` | `banzai/BANZAI_REFERENCE.md §10` | BanzAI quality framework. |
| Grafo de Protocolo | `KEEP` | `banzai/BANZAI_REFERENCE.md §4` | BanzAI knowledge graph. |
| Agentic Protocol Research | `KEEP` | `banzai/BANZAI_REFERENCE.md §6` | BanzAI research module. |
| Certification Copilot | `KEEP` | `banzai/BANZAI_REFERENCE.md §6` | BanzAI certification module. |
| Quality Dashboard | `KEEP` | `banzai/BANZAI_REFERENCE.md §6` | BanzAI quality module. |
| Protocol Simulator | `KEEP` | `banzai/BANZAI_REFERENCE.md §6` | BanzAI simulation module. |
| Federation Intelligence | `KEEP` | `banzai/BANZAI_REFERENCE.md §6` | BanzAI federation module. |
| Protocol Memory | `KEEP` | `banzai/BANZAI_REFERENCE.md §6` | BanzAI memory module. |
| Operator Digital Twin | `KEEP` | `banzai/BANZAI_REFERENCE.md §6` | BanzAI twin module. |
| Protocol OS Vision | `KEEP` | `banzai/BANZAI_REFERENCE.md §11` | BanzAI roadmap/vision. |
| Impacto no Ecossistema | `KEEP` | `banzai/BANZAI_REFERENCE.md §11` | BanzAI ecosystem impact. |
| Postura de segurança | `KEEP` | `banzai/BANZAI_REFERENCE.md §8` | BanzAI security. |
| Opening sentence "produto de primeira classe" | `REFRAME` | `banzai/BANZAI_REFERENCE.md §1` | P1 audit finding: remove "produto". BanzAI is the Protocol OS, not a product. |

---

### §12 — Banzami para Programadores (lines ~1888–1977)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| SDK integração arquitectura | `KEEP` | `banzami/BANZAMI_REFERENCE.md §4` | Banzami developer experience. |
| TypeScript example | `KEEP` | `banzami/BANZAMI_REFERENCE.md §4` | Banzami SDK. |
| Flutter example | `KEEP` | `banzami/BANZAMI_REFERENCE.md §4` | Banzami SDK. |
| Webhooks | `KEEP` | `banzami/BANZAMI_REFERENCE.md §4` | Banzami integration. |
| Idempotência | `KEEP` | `banzami/BANZAMI_REFERENCE.md §4` | Banzami integration. |
| Sandbox | `KEEP` | `banzami/BANZAMI_REFERENCE.md §4` | Banzami sandbox. |

---

### §13 — Banzami para Comerciantes (lines ~1979–2019)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| QR types | `KEEP` | `banzami/BANZAMI_REFERENCE.md §3` | Banzami merchant product. |
| T+0 settlement | `REFERENCE` | `banzami/BANZAMI_REFERENCE.md §3` (1 sentence) + cross-ref to `banza/BANZA_REFERENCE.md §9` | T+0 is a BANZA protocol invariant. Banzami implements it. |
| Banzami Business | `KEEP` | `banzami/BANZAMI_REFERENCE.md §3` | Banzami operator product. |
| Payment Links | `KEEP` | `banzami/BANZAMI_REFERENCE.md §3` | Banzami operator product. |

---

### §14 — Para Consumidores (lines ~2022–2050)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Banzami Wallet | `KEEP` | `banzami/BANZAMI_REFERENCE.md §2` | Banzami consumer product. |
| @banza identity | `SPLIT` | `banza/BANZA_REFERENCE.md §3` (protocol primitive definition) + `banzami/BANZAMI_REFERENCE.md §2` (how Banzami uses it) | @banza is a BANZA protocol primitive. Banzami implements it as a consumer handle. |
| Consumer security | `KEEP` | `banzami/BANZAMI_REFERENCE.md §2` | Banzami implementation. |

---

### §15 — Segurança e Integridade Financeira (lines ~2053–2083)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Financial invariants (INV-* table) | `ABSORB` | `banza/BANZA_REFERENCE.md §7` | Protocol invariants — already in §7. Remove duplication. |
| Security layers SVG | `KEEP` | `banzami/BANZAMI_REFERENCE.md §5` | Banzami's implementation architecture. |
| OpenTelemetry observability | `KEEP` | `banzami/BANZAMI_REFERENCE.md §5` | Banzami's observability implementation. |
| Sandbox separation | `REFERENCE` | `banzami/BANZAMI_REFERENCE.md §5` (1 sentence) + cross-ref to §6 | Environment separation is protocol-required (BANZA). Banzami implements it. |

---

### §16 — Sandbox e Ambiente de Testes (lines ~2087–2105)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Full section | `KEEP` | `banzami/BANZAMI_REFERENCE.md §6` | Banzami's sandbox implementation. |

---

### §17 — Por que Angola. Por que Agora. (lines ~2109–2129)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| O problema que o Banzami resolve | `KEEP` | `banzami/BANZAMI_REFERENCE.md §7` | Banzami operator mission. |
| A oportunidade | `KEEP` | `banzami/BANZAMI_REFERENCE.md §7` | Banzami's market context. |
| O salto tecnológico | `KEEP` | `banzami/BANZAMI_REFERENCE.md §7` | Banzami's strategic positioning. |

---

### §18 — Roadmap (lines ~2134–2163)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| Conformance Suite v1 | `KEEP` | `banza/BANZA_REFERENCE.md §11` | Protocol milestone. |
| Certificação Nível 1–2 | `KEEP` | `banza/BANZA_REFERENCE.md §11` | Protocol milestone. |
| BanzAI Live API | `KEEP` | `banzai/BANZAI_REFERENCE.md §11` | BanzAI milestone. |
| PHP SDK v1 | `KEEP` | `banzami/BANZAMI_REFERENCE.md §8` | Banzami product milestone. |
| Payout automatizado | `KEEP` | `banzami/BANZAMI_REFERENCE.md §8` | Banzami product milestone. |
| Integração acquiring | `KEEP` | `banzami/BANZAMI_REFERENCE.md §8` | Banzami operator milestone. |
| Certificação Nível 3–4 | `KEEP` | `banza/BANZA_REFERENCE.md §11` | Protocol milestone. |
| Operadores de terceiros | `KEEP` | `banza/BANZA_REFERENCE.md §11` | Protocol growth milestone. |
| RFC de federação | `KEEP` | `banza/BANZA_REFERENCE.md §11` | Protocol milestone. |
| BanzAI Knowledge API | `KEEP` | `banzai/BANZAI_REFERENCE.md §11` | BanzAI milestone. |
| Portal de certificação | `KEEP` | `banza/BANZA_REFERENCE.md §11` | Protocol milestone. |
| Piloto de federação | `KEEP` | `banza/BANZA_REFERENCE.md §11` | Protocol milestone. |
| Federação aberta | `KEEP` | `banza/BANZA_REFERENCE.md §11` | Protocol milestone. |

---

### §19 — Declaração de Visão (lines ~2166–2218)

| Subsection | Action | Destination | Notes |
|-----------|--------|-------------|-------|
| "O comércio de Angola merece infraestrutura" | `MOVE` | `banza/BANZA_REFERENCE.md §12` | Reframe: BANZA vision, not Banzami. Remove "isso é o Banzami" P1 finding. |
| "Hoje / Amanhã — com o Banzami" | `KEEP` | `banzami/BANZAMI_REFERENCE.md §9` | Banzami product transformation. |
| "Por que isto importa além do comércio" | `SPLIT` | `banza/BANZA_REFERENCE.md §12` (infrastructure vision) + `banzami/BANZAMI_REFERENCE.md §9` (product transformation) | Two distinct arguments. |
| "A promessa / Banzami — O sistema de pagamentos instantâneos de Angola" | `KEEP` | `banzami/BANZAMI_REFERENCE.md §9` | Banzami operator identity and promise. |
| "Banza — A infraestrutura que permite Angola pagar digitalmente." | `KEEP` | `banza/BANZA_REFERENCE.md §12` | BANZA protocol identity. |

---

## Content Not Relocated (Removed from Combined File Only)

None. No content is deleted. Every line of the combined document either:
1. Moves to the owning canonical reference document
2. Is referenced (cross-linked) from at least one canonical reference

The combined file `banzami/docs/BANZA_REFERENCE.md` is NOT modified. The canonical references are additive.

---

*Relocation map produced: 2026-05-30. No files modified.*
