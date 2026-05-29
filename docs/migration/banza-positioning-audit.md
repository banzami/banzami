---
title: BANZA Ecosystem Positioning Audit — BANZA-POSITIONING-AUDIT-002
version: 1.0
date: 2026-05-30
status: COMPLETE
---

# BANZA Ecosystem Positioning Audit

**Core question:** What is BANZA promising to the world?

**Canonical answer:** Open programmable financial infrastructure — operated by certified operators, governed by verifiable rules, and operated through a native Protocol Operating System (BanzAI) capable of explaining, validating and evolving the protocol.

---

## Canonical Positioning Reference

| Entity | What it is | What it is NOT |
|---|---|---|
| **BANZA** | Open programmable financial infrastructure | A wallet, QR app, checkout product, merchant platform |
| **BanzAI** | Native Protocol Operating System — understands, validates, explains, simulates, certifies, traces | A chatbot, documentation search, support assistant |
| **Banzami** | Reference operator and payment product built on BANZA | The organization, the protocol, the infrastructure |

**Strategic differentiator:** Most financial protocols define rules. BANZA defines rules AND includes a native operating system capable of explaining, validating, researching, simulating, certifying and tracing those rules.

**Canonical hero positioning:**
> Banza define como o dinheiro se move digitalmente — através de operadores certificados, regras verificáveis, infraestrutura aberta e um sistema operativo nativo capaz de explicar, validar e evoluir o protocolo.

---

## Classification Definitions

| Class | Definition |
|---|---|
| **POSITIONING ALIGNED** | Page correctly presents BANZA as infrastructure/protocol; BanzAI as protocol OS; Banzami as product |
| **PARTIALLY ALIGNED** | Core framing is correct but isolated phrases could strengthen the positioning |
| **MISALIGNED** | Page fundamentally presents BANZA through a non-canonical lens |
| **VALUE PROPOSITION DRIFT** | Page unintentionally presents BANZA as a payment app, QR solution, merchant tool or consumer product |

---

## Page-by-Page Audit

### Homepage (`/` — `apps/docs/app/page.tsx`)

| Surface | Content | Classification | Action |
|---|---|---|---|
| Badge | "Infraestrutura Financeira Programável para Angola" | ALIGNED | — |
| H1 | "Infraestrutura financeira programável." | ALIGNED | — |
| Hero subheadline | "Banza define como o dinheiro se move digitalmente em Angola — através de operadores certificados, regras verificáveis e infraestrutura aberta." | **MISALIGNED** | Add BanzAI; remove "em Angola" (global infrastructure) |
| Metadata description | "Banzami é o produto de pagamentos construído sobre o Banza — pagamentos wallet-to-wallet…" leads with product | **MISALIGNED** | Protocol-first description |
| ManifestoQuote | "Angola não precisa de copiar o modelo de pagamentos dos outros…" | PARTIALLY ALIGNED | Keep — Angola-first vision |
| §3 Problema | Problem cards: cash dependency, no SDK, QR-less apps | ALIGNED | Context for why infrastructure needed |
| §4 Como funciona H2 | "Escanear. Confirmar. Pago instantaneamente." | **VALUE PROPOSITION DRIFT** | Product action → protocol principle |
| §4 Como funciona body | "transferência directa entre carteiras, registada no ledger de forma atómica e imutável" | ALIGNED | Correct protocol framing |
| §5 Wallet-to-wallet H2 | "O telemóvel é a carteira." | PARTIALLY ALIGNED | Acceptable — illustrates protocol primitive |
| §6 Ecossistema | "Uma rede. Múltiplos actores." | ALIGNED | Correct infrastructure framing |
| §6 Ecossistema body | "Banzami SDKs, bancos e o core financeiro — todos ligados através de uma infraestrutura do Banza" | ALIGNED | Correct |
| §7 QR Commerce H2 | "Um QR code. Todo o comércio angolano." | **VALUE PROPOSITION DRIFT** | Positions BANZA as a QR commerce product |
| §7 QR Commerce body | "o Banzami QR serve todos os casos de uso do mercado angolano" | **VALUE PROPOSITION DRIFT** | Banzami product feature presented as BANZA capability |
| §8 Casos de uso | Use case cards (táxi, cantinas, etc.) | PARTIALLY ALIGNED | Use cases demonstrate value; acceptable at this level |
| §9 Mobile-first | "O pagamento perfeito dura menos de 3 segundos." | PARTIALLY ALIGNED | Performance claim; does not misrepresent BANZA |
| §10 Para programadores H2 | "SDK-first. Integração em Kwanza." | ALIGNED | Correct |
| §10 Para programadores body | "O Banza é SDK-first. Qualquer app… ao Banzami SDK oficial." | ALIGNED (after prev. fix) | Correct after last session's fix |
| §11 Segurança | "Infraestrutura de grau bancário." | ALIGNED | Strong infrastructure framing |
| BanzAI widget | `HomeBanzamIAEntry` | See below | — |
| Source attribution | "Organização Banzami" | PROTECTED | — |

---

### `HomeBanzamIAEntry` Component

| Surface | Content | Classification | Action |
|---|---|---|---|
| Widget descriptor | "O Sistema Operativo do Protocolo Banza — para entender, integrar e validar o ecossistema Banzami." | **VALUE PROPOSITION DRIFT** | "ecossistema Banzami" frames BanzAI as a Banzami tool, not a protocol OS |
| Quick prompt chip 1 | "O que é o Banzami?" | REQUIRED_PRODUCT_REFERENCE | Keep — valid user question |
| Quick prompt chip 2 | "Qual é a diferença entre Banzami e Banza?" | REQUIRED_PRODUCT_REFERENCE | Keep — valid user question |
| Quick prompt chips 3–6 | Protocol-focused questions | ALIGNED | Keep |
| Input placeholder | "Pergunte sobre QR, SDKs, operadores, certificação, invariantes…" | ALIGNED | Correct protocol topics |

---

### `HeroBanzamIAWidget` Component

| Surface | Content | Classification | Action |
|---|---|---|---|
| Widget descriptor | "O Sistema Operativo do Protocolo Banza." | ALIGNED | — |
| Quick prompts | "Como integrar o Banzami?", "Como funciona a certificação?", etc. | ALIGNED | Mix of product and protocol questions — correct |
| Input placeholder | "Como posso integrar o Banzami no meu produto?" | REQUIRED_PRODUCT_REFERENCE | Keep — operator/developer intent |

---

### Global Layout (`apps/docs/app/layout.tsx`)

| Surface | Content | Classification | Action |
|---|---|---|---|
| Global metadata description | "Banzami é o produto de pagamentos construído sobre o Banza — wallet-to-wallet, liquidação instantânea…" | **MISALIGNED** | Every page inherits a product-centric description |
| Global OG description | "Banzami é o produto de pagamentos construído sobre o Banza — wallet-to-wallet…" | **MISALIGNED** | Same issue in OG cards |
| Navbar wordmark | "Banza" | ALIGNED | — |
| Footer wordmark | "Banza" | ALIGNED | — |
| Footer tagline | "Banza — Protocolo Aberto de Infraestrutura Financeira para Angola" | ALIGNED | — |
| Navbar items | Protocol sections + BanzAI | ALIGNED | — |
| Footer links | Protocol sections | ALIGNED | — |

---

### `/reference` (Reference page)

| Surface | Content | Classification |
|---|---|---|
| H1 | "Banza — Referência Oficial do Protocolo" | ALIGNED |
| Metadata | "Referência oficial do Protocolo Banza — 20 secções…" | ALIGNED |
| Attribution | "Organização Banzami · v1.0" | PROTECTED |

**Overall:** POSITIONING ALIGNED

---

### `/operators` (Operator Registry)

| Surface | Content | Classification |
|---|---|---|
| H1 | "Registo de Operadores Banza" | ALIGNED |
| Metadata | "Registo público de operadores Banza — manifests, capacidades, conformidade e preparação para federação." | ALIGNED |
| Privacy notice | "Transparência de infraestrutura, não vigilância financeira." | ALIGNED — strong positioning |
| Conformance note | "Os níveis de conformidade (0–4) são determinados pelo runner oficial do Banza." | ALIGNED |
| Footer note | `/.well-known/banzami/operator.json` | PROTECTED — wire format |

**Overall:** POSITIONING ALIGNED

---

### `/banzamia` (BanzAI Interface)

| Surface | Content | Classification |
|---|---|---|
| Metadata title | "BanzAI — Protocol Operating System" | ALIGNED |
| Metadata description | "BanzAI é o Sistema Operativo do Protocolo Banza. 16 módulos. Compreender, Explicar, Validar, Simular, Prever, Guiar, Certificar, Federar. Ferramentas determinam a verdade. A IA explica a verdade." | ALIGNED |

**Overall:** POSITIONING ALIGNED — strongest BanzAI positioning on the site

---

### `/sobre-banzamia` (About BanzAI)

| Surface | Content | Classification |
|---|---|---|
| Metadata title | "Sobre o BanzAI" | ALIGNED (after prev. fix) |
| OG title | "Sobre o BanzAI · Banza" | ALIGNED (after prev. fix) |
| OG description | "O Sistema Operativo do Protocolo Banza. 16 módulos…" | ALIGNED |
| Body | "O BanzAI é o Sistema Operativo do Protocolo Banza — 16 módulos especializados que tornam o protocolo compreensível, validável, simulável e certificável. Não é um chatbot. É a interface cognitiva do protocolo…" | ALIGNED — explicitly rejects "chatbot" framing |

**Overall:** POSITIONING ALIGNED

---

### `/roadmap` (BanzAI Roadmap)

| Surface | Content | Classification |
|---|---|---|
| Metadata | "Roadmap público do BanzAI — Protocol Operating System do Protocolo Banza." | ALIGNED |
| Body intro | "Protocol Operating System for the Banza protocol." | ALIGNED (after prev. fix) |
| Status badge | "Protocol Operating System — Understand · Explain · Validate · Simulate · Predict · Guide" | ALIGNED |

**Overall:** POSITIONING ALIGNED

---

### `/validacao` (Validation System)

| Surface | Content | Classification |
|---|---|---|
| Metadata description | "Sistema de execução e validação do ecossistema Banza" | ALIGNED (after prev. fix) |
| H1 | "Execução e Validação do Protocolo Banza" | ALIGNED (after prev. fix) |
| Governance notice | "edição restrita à administração Banzami" | REQUIRED_PRODUCT_REFERENCE |

**Overall:** POSITIONING ALIGNED

---

### BanzAI Chat Welcome Screen

| Surface | Content | Classification |
|---|---|---|
| H1 | "BanzAI" | ALIGNED |
| Descriptor | "BanzAI é o Sistema Operativo do Protocolo Banza. 16 módulos. Ferramentas determinam a verdade. A IA explica a verdade." | ALIGNED |
| Sub-descriptor | "Tools determine truth. AI explains truth." | ALIGNED |
| Example questions | Protocol questions (operators, certification, federation, etc.) | ALIGNED |

**Overall:** POSITIONING ALIGNED — strongest BanzAI strategic framing on the site

---

### `SectionCard` Component

| Surface | Content | Classification |
|---|---|---|
| Section number badge | `§N` | ALIGNED |
| Title | From BANZAMI_REFERENCE.md section headings | ALIGNED |
| Preview | First paragraph of section content | ALIGNED |

**Overall:** POSITIONING ALIGNED

---

### `SectionNav` Sidebar

| Surface | Content | Classification |
|---|---|---|
| Wordmark | "BANZA" | ALIGNED |
| Sublabel | "Documentação do Protocolo" | ALIGNED |
| Section links | Derived from reference titles and slugs | ALIGNED |

**Overall:** POSITIONING ALIGNED

---

## BanzAI Strategic Differentiator Assessment

**Flag: BanzAI appearing as chatbot/assistant:**

| Page | BanzAI framing | Status |
|---|---|---|
| `/banzamia` | "Protocol Operating System" | ALIGNED |
| `/sobre-banzamia` | "Não é um chatbot. É a interface cognitiva do protocolo." | ALIGNED |
| `/roadmap` | "Protocol Operating System" | ALIGNED |
| `HeroBanzamIAWidget` | "O Sistema Operativo do Protocolo Banza." | ALIGNED |
| `HomeBanzamIAEntry` (before fix) | "para entender, integrar e validar o ecossistema Banzami" | VALUE PROPOSITION DRIFT |
| Hero subheadline (before fix) | Not mentioned | MISALIGNED (absence) |
| Global metadata (before fix) | Not mentioned | MISALIGNED (absence) |

**Gap identified:** The hero positioning statement and global metadata did not include BanzAI as a strategic differentiator. BanzAI's role was only communicated on pages visitors navigate to after landing. Fixed in this session.

---

## Summary Counts

| Classification | Pages/Surfaces | Action taken |
|---|---|---|
| POSITIONING ALIGNED | 9 pages/surfaces | No action |
| PARTIALLY ALIGNED | 4 surfaces | Documented; not changed (acceptable) |
| MISALIGNED | 3 surfaces | Fixed |
| VALUE PROPOSITION DRIFT | 4 surfaces | Fixed |

---

*Audit completed: 2026-05-30.*
