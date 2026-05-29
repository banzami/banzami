---
title: CANONICAL_REFERENCE_AUDIT — BANZA-CANONICAL-REFERENCE-REWRITE
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no modifications applied
---

# Canonical Reference Audit

**Scope:** All 17 sections of `docs/BANZAMI_REFERENCE.md`

**Canonical model (ADR-025):**
- **BANZA** — protocol · infrastructure · rules · invariants · certification · federation · settlement · governance
- **BanzAI** — Protocol Operating System · protocol intelligence · conformance assistance · operator tooling
- **Banzami** — reference implementation · reference operator · payment products · wallets · merchant tools · QR payments

**Validation test applied to every section:**
1. Who is the protagonist? (BANZA / BanzAI / Banzami)
2. Would this still be true if Banzami disappeared? → belongs to BANZA
3. Would this still be true if 100 operators existed? → belongs to BANZA
4. Does it describe protocol / OS / product?

---

## §1 — O que é o Banza?

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| §1 intro (lines 40–46) | "Banza é infraestrutura financeira programável..." / "Banzami é o produto principal do Banza" | BANZA / Banzami | No issue — correctly separates protocol from product | ALIGNED |
| §1 callout (line 46) | "Banza constrói a infraestrutura. Banzami move o dinheiro." | BANZA / Banzami | Correct canonical tagline | ALIGNED |
| **Subsection heading (line 48)** | `### Arquitectura de dois níveis` | — | The title encodes the pre-ADR-025 ADR-016 two-tier model. The canonical model has three tiers: BANZA (protocol) → BanzAI (OS) → Banzami (product). Calling it "dois níveis" freezes the pre-ADR-025 mental model in the heading. | **P0** |
| **ADR-016 reference (line 52)** | `Esta arquitectura de marca está definida no ADR-016.` | — | ADR-016 defined the two-tier model. ADR-025 supersedes ADR-016 for the brand hierarchy. The reference document should cite ADR-025, not ADR-016. | **P0** |
| **SVG diagram (line 50)** | `brand-architecture.svg` — renders BANZAMI as root: "organização · protocolo · ecossistema" | — | See CANONICAL_DIAGRAM_AUDIT.md §D-001. The diagram is the pre-ADR-025 model visualised. This is the highest-priority finding in the entire document because it is the first thing a visitor sees after reading the §1 opening. | **P0** |
| **Subsection heading (line 54)** | `### Os quatro pilares do Banzami` | — | The four pillars (Programmable, Wallet-native, QR-native, Instant settlement) are BANZA protocol properties. A certified operator can build a non-Banzami product and it would still be Programmable, Wallet-native, QR-native, Instant settlement — because those properties come from the protocol, not from Banzami. Attributing them to Banzami misrepresents them as product features. | **P1** |
| Four pillars table (lines 57–61) | Programmable, Wallet-native, QR-native, Instant settlement | Banzami (heading says) | The content of the table is correct — each pillar is described accurately. The issue is the section heading. The pillars apply to any certified operator. | P1 (heading only) |
| §1 canonical experience | `SCAN QR → CONFIRMAR → PAGO INSTANTANEAMENTE` | BANZA | Protocol-level canonical experience. Would still be true with 100 operators. ALIGNED. | ALIGNED |
| §1 name etymology | "Banzami... Banza..." | Both | Correctly traces both names to Bantu roots. ALIGNED. | ALIGNED |

**§1 verdict:** Two P0 findings (heading + ADR reference), one P1 (pillar attribution). The diagram is the most urgent. The heading "dois níveis" and ADR-016 reference perpetuate the pre-ADR-025 mental model at the top of the most-visited page.

**Validation test results for §1:**
- Would "Arquitectura de dois níveis" be true if Banzami disappeared? → NO. The architecture would still have BANZA and BanzAI. It is not a two-level architecture even without Banzami.
- Would the four pillars apply if 100 operators existed? → YES. Any certified operator implements them. They belong to BANZA.

---

## §2 — Princípios Fundamentais

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| "Ferramentas determinam a verdade" | Protocol epistemology | BANZA | Correctly placed at protocol level | ALIGNED |
| "A correcção financeira não é negociável" | Protocol invariant | BANZA | Correctly placed | ALIGNED |
| "O protocolo é o produto" (line 89) | "O Banzami (o produto de consumo) é a implementação de referência do protocolo Banza." | BANZA / Banzami | Excellent canonical framing. Explicitly says Banzami is the reference implementation of the BANZA protocol. | ALIGNED |
| "Os operadores implementam política" | Protocol separation of concerns | BANZA | Correct kernel/operator distinction | ALIGNED |
| "Rastreabilidade por defeito" | Protocol property | BANZA | Correct | ALIGNED |
| "Angola primeiro" | Protocol mission | BANZA | Correct | ALIGNED |

**§2 verdict:** FULLY ALIGNED. No issues.

---

## §3 — Visão Geral do Ecossistema

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| Ecosystem diagram | `banzami-ecosystem.svg` — "Banza Ecosystem" header, BANZA KERNEL at centre | BANZA | ALIGNED — see CANONICAL_DIAGRAM_AUDIT.md §D-002 | ALIGNED |
| Kernel Banza description | 18 Rust crates | BANZA | Correctly attributed to Banza | ALIGNED |
| "Operador de Referência" (line 144) | "O Banzami é a implementação de referência do protocolo completo." | Banzami | Correct ADR-025 framing — Banzami = reference operator | ALIGNED |
| "Operadores Certificados" | "Qualquer entidade que obtenha certificação Banza pode implementar o protocolo." | BANZA | Correct — protocol is open to any certified operator | ALIGNED |

**§3 verdict:** FULLY ALIGNED. The ecosystem section correctly places BANZA Kernel at the centre, Banzami as the reference operator among multiple possible operators.

---

## §4 — Arquitectura Técnica

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| Stack table | Rust / Go / Next.js / Flutter / PostgreSQL / Redis / OTel | BANZA | Correctly framed as protocol stack | ALIGNED |
| Service topology SVG | `service-topology.svg` | BANZA | Protocol service architecture | ALIGNED |
| Ledger section | "O ledger de dupla entrada" | BANZA | Protocol financial core | ALIGNED |
| Invariants section | INV-LEDGER-*, INV-WALLET-*, INV-STL-* | BANZA | Protocol invariants | ALIGNED |
| Trace system | `trace-flow.svg` | BANZA | Protocol traceability | ALIGNED |

**§4 verdict:** FULLY ALIGNED.

---

## §5 — Representação Monetária

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| Integer Rule | "Todos os valores monetários no protocolo Banza DEVEM ser representados como inteiros." | BANZA | Correctly attributed: "no protocolo Banza" | ALIGNED |
| `*_minor` convention | Protocol-wide naming rule | BANZA | Correctly framed | ALIGNED |
| **Semântica de Montantes (line 294)** | `"Todo o fluxo de pagamento Banzami produz três montantes monetários com semântica exacta"` | — | The gross/net/fee model is a BANZA protocol requirement (INV-STL-001). Any certified operator must implement it. "Fluxo de pagamento Banzami" implies this is a Banzami-specific mechanism. It is not — it is a protocol invariant. Would be true with 100 operators. | **P2** |
| MON-001 certification rule | "Operadores certificados DEVEM representar todos os valores monetários como minor units inteiras." | BANZA | Correctly framed as protocol certification rule for all operators | ALIGNED |
| SDK requirements | "Todos os SDKs Banza oficiais DEVEM…" | BANZA | Correctly attributed | ALIGNED |

**§5 verdict:** One P2 finding. The monetary flow model is a BANZA protocol property; the heading attributes it to Banzami.

---

## §6 — Governança

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| RFCs | "govern decisões ao nível do protocolo" | BANZA | Correct | ALIGNED |
| ADRs | "govern decisões de implementação" | BANZA | Correct | ALIGNED |
| Validation Matrix | Protocol progress tracking | BANZA | Correct | ALIGNED |
| Validation domains | DOM-FIN, DOM-IDENTITY, etc. | BANZA | Correct | ALIGNED |

**§6 verdict:** FULLY ALIGNED.

---

## §7 — Modelo de Certificação

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| Certification levels L0–L4 | Protocol certification ladder | BANZA | "Qualquer entidade que obtenha certificação Banza" — correct open protocol framing | ALIGNED |
| Certification flow SVG | `certification-flow.svg` | BANZA | Protocol process | ALIGNED |
| Operator Manifest | JSON schema for any operator | BANZA | Protocol standard | ALIGNED |

**§7 verdict:** FULLY ALIGNED.

---

## §8 — Federação

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| "A federação é uma camada de primeira classe" | Protocol architecture | BANZA | Correct | ALIGNED |
| "Todos os pagamentos são actualmente processados pelo operador de referência Banzami" (line 601) | Current state | Banzami | Correct — acknowledges Banzami is the current reference operator, not the protocol | ALIGNED |
| Federation architecture SVG | `federation.svg` | BANZA | Protocol federation layer | ALIGNED |

**§8 verdict:** FULLY ALIGNED. Notably good: explicitly says "operador de referência Banzami" not "o Banzami é a federação".

---

## §9 — BanzAI

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| **Opening sentence (line 632)** | `"O BanzAI é um produto de primeira classe do ecossistema Banza"` | — | BanzAI is the Protocol Operating System — a native cognitive layer of the BANZA protocol infrastructure. Calling it a "produto" (product) places it in the same category as Banzami (a payment product). The canonical model distinguishes BanzAI as the OS tier, not the product tier. Would BanzAI exist if Banzami disappeared? YES. Would it exist if 100 operators existed? YES. It belongs to BANZA infrastructure. | **P1** |
| "Se o Kernel é o motor financeiro..." | "O BanzAI é a interface cognitiva do Banza" | BanzAI | Correct framing in the second sentence | ALIGNED |
| "Ferramentas determinam a verdade..." | Protocol epistemology principle | BanzAI/BANZA | Correct | ALIGNED |
| §9 BanzAI cognitive layer content | Four-layer protocol model (Física, Financeira, Governança, Cognitiva) | BANZA/BanzAI | Correct — BanzAI is the Cognitive Layer of BANZA | ALIGNED |
| "Por que quase nenhum protocolo tem isto" | Protocol differentiation claim | BANZA | Correct — BanzAI is a BANZA protocol-level innovation | ALIGNED |
| Module tables (lines 789–815) | 16 modules in 3 layers | BanzAI | Correct | ALIGNED |
| "Protocol OS Vision" | BanzAI as Protocol OS | BanzAI | Correct | ALIGNED |
| §9 "Interface Humana do Protocolo" (line 1536) | Four BANZA protocol pillars: Kernel, Certificação, Federação, BanzAI | BANZA | Correct — BanzAI is one of four BANZA pillars (not a Banzami feature) | ALIGNED |
| "Postura de segurança" | BanzAI is read-only | BanzAI | Correct | ALIGNED |

**§9 verdict:** One P1 finding — the opening sentence. The rest of §9 is the strongest BanzAI positioning in the entire document. The opening contradicts itself: it says "produto" but then correctly describes BanzAI as the cognitive interface of the BANZA protocol.

**Validation test for §9:**
- Would BanzAI exist if Banzami disappeared? YES — BanzAI explains the BANZA protocol, not the Banzami product.
- Would BanzAI exist if 100 operators existed? YES — it would serve all of them.
- Therefore: BanzAI belongs to BANZA infrastructure, not the product tier.

---

## §10 — Banzami para Programadores

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| SDK descriptions | TypeScript `@banza/sdk`, Flutter `banzami_sdk`, PHP `banza/sdk` | Banzami | Product-layer section. Correctly describes developer integration with Banzami product. | ALIGNED |
| Code examples | BanzaClient, client.qr.createDynamic, etc. | Banzami | Product API surface. Correct. | ALIGNED |
| Webhooks, Idempotency, Sandbox | Product developer experience | Banzami | Correct | ALIGNED |

**§10 verdict:** FULLY ALIGNED. Correctly describes Banzami as the SDK/product layer.

---

## §11 — Banzami para Comerciantes

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| "Sem hardware. Sem burocracia." | Banzami merchant UX | Banzami | Correct product-layer claim | ALIGNED |
| QR types, T+0 settlement | Merchant product features | Banzami | Correct | ALIGNED |
| Banzami Business dashboard | Product feature | Banzami | Correct | ALIGNED |
| Payment Links | Product feature | Banzami | Correct | ALIGNED |

**§11 verdict:** FULLY ALIGNED.

---

## §12 — Para Consumidores

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| Banzami Wallet | Consumer product | Banzami | Correct | ALIGNED |
| @banza identity | Protocol primitive used by product | BANZA/Banzami | Correct — @banza handle is a protocol primitive (BANZA), Banzami wallet uses it | ALIGNED |
| Consumer security | Product security layer | Banzami | Correct | ALIGNED |

**§12 verdict:** FULLY ALIGNED.

---

## §13 — Segurança e Integridade Financeira

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| Security layers SVG | `security-layers.svg` | BANZA | Protocol security architecture | ALIGNED |
| Financial invariants | INV-LEDGER-001, INV-STL-001, etc. | BANZA | Protocol invariants | ALIGNED |
| OpenTelemetry observability | Protocol observability | BANZA | Correct | ALIGNED |
| Sandbox separation | Protocol environment isolation | BANZA | Correct | ALIGNED |

**§13 verdict:** FULLY ALIGNED.

---

## §14 — Sandbox e Ambiente de Testes

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| Sandbox vs Live table | Protocol environments | BANZA | Correct | ALIGNED |
| Sandbox tools | Fund, simulate, test | Banzami (reference implementation) | Correct — describes Banzami sandbox tools | ALIGNED |

**§14 verdict:** FULLY ALIGNED.

---

## §15 — Por que Angola. Por que Agora.

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| "O problema que o Banzami resolve" | Product-layer problem framing | Banzami | Correct — Banzami (the product) solves user problems | ALIGNED |
| "O modelo está provado... O Banza é a infraestrutura." | Protocol identity claim | BANZA | Fixed in Phase 2 (was "O Banzami é a infraestrutura") | ALIGNED ✓ |
| "O salto tecnológico" | Infrastructure leap argument | BANZA | Correct | ALIGNED |

**§15 verdict:** FULLY ALIGNED after Phase 2 fix.

---

## §16 — Roadmap

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| Short-term items | Conformance Suite, BanzAI Live API, PHP SDK, Payout | BANZA/BanzAI | All protocol-level milestones. Correct. | ALIGNED |
| Medium-term items | Third-party operators, federation RFC, certification portal | BANZA | Correct — protocol growth milestones | ALIGNED |
| Long-term items | Federation pilot, cross-border rails | BANZA | Correct | ALIGNED |

**§16 verdict:** FULLY ALIGNED.

---

## §17 — Declaração de Visão

| Surface | Content | Owner | Issue | Severity |
|---|---|---|---|---|
| "O comércio de Angola merece infraestrutura" | Vision opening | BANZA | Correct — infrastructure protagonist | ALIGNED |
| **"Isso é o Banzami — construído pelo Banza." (line 1877)** | Vision climax statement | — | The vision section opens with BANZA as the infrastructure protagonist, then climaxes with Banzami as the subject. The canonical model requires BANZA to be the final protagonist of a vision statement. "Isso é o Banzami" concludes the section with the product, relegating the protocol to an instrumental role ("construído pelo Banza"). A visitor who only reads the first and last lines takes away: "the vision is Banzami." | **P1** |
| "Amanhã — com o Banzami:" | Product-layer transformation | Banzami | Correct — Banzami delivers the consumer/merchant experience | ALIGNED |
| "cada decisão de engenharia... no Banzami reflecte um compromisso do Banza" (line 1903) | Attribution | Mixed | P2 — the commitment belongs to BANZA; the design choices in Banzami reflect it. Not wrong, but mixed. | P2 |
| "Banzami — O sistema de pagamentos instantâneos de Angola. Wallet-native. QR-first." (line 1917) | Product tagline | Banzami | Correct — Banzami is the payment product | ALIGNED |
| "Banza — A infraestrutura que permite Angola pagar digitalmente." (line 1918) | Protocol tagline | BANZA | Correct | ALIGNED |

**§17 verdict:** One P1 finding — the vision climax statement makes Banzami the protagonist. The final two lines are excellent but the climax sentence on line 1877 is the one a visitor remembers.

---

## Summary Counts

| Severity | Count | Sections |
|---|---|---|
| **P0 — Conceptually false** | 3 | §1 (2 × architecture heading/reference), plus SVG — see Diagram Audit |
| **P1 — Misleading** | 3 | §1 (pillar attribution), §9 (BanzAI called "produto"), §17 (vision climax) |
| **P2 — Legacy wording** | 2 | §5 ("fluxo de pagamento Banzami"), §17 (line 1903) |
| **P3 — Cosmetic** | 0 | — |
| **ALIGNED** | 12 sections fully aligned | §2, §3, §4, §6, §7, §8, §10, §11, §12, §13, §14, §16 |

---

*Audit completed: 2026-05-30. No modifications applied.*
