---
title: CANONICAL_DIAGRAM_AUDIT — BANZA-CANONICAL-REFERENCE-REWRITE
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no modifications applied
---

# Canonical Diagram Audit

**Scope:** All 33 SVG files in `apps/docs/public/images/architecture/`

**Audit method:** For each diagram, validate the architectural claims — not the labels. A diagram that shows:
```
BANZAMI (organização · protocolo · ecossistema)
├─ Banzami (product)
└─ BanzAI (OS)
```
is structurally wrong under ADR-025, regardless of whether the label text says "Banzami" or "Banza".

**Canonical structure (ADR-025):**
```
BANZA (protocol · infrastructure · ecosystem)
├─ BanzAI (Protocol Operating System)
└─ Banzami (Reference Operator / Payment Product)
```

---

## D-001 — brand-architecture.svg ⚠️ P0 STRUCTURAL

**File:** `apps/docs/public/images/architecture/brand-architecture.svg`
**Used in:** `BANZAMI_REFERENCE.md` §1 (line 50), rendered on `banzami.org/o-que-e-o-banza`

**Current structure:**
```
BANZAMI (organização · protocolo · ecossistema)   ← ROOT
├─ Banzami (produto principal de pagamento)
│   └─ [Products: Wallet, Business, QR, SDK]
└─ BanzAI (Sistema Operativo de Protocolo)
    └─ [Modules: Chat, Operator Builder, Conformance, ...]
```

**Issue — Conceptually false (P0):**

The diagram root is `BANZAMI` described as `organização · protocolo · ecossistema`. This represents the pre-ADR-025 model (ADR-016) where BANZAMI was simultaneously the organization, the protocol AND the ecosystem — with Banzami (product) and BanzAI (OS) as children of BANZAMI.

Under ADR-025:
- The organization is `Organização Banzami` (a legal entity — protected identifier, unchanged)
- The protocol is `BANZA` — open financial infrastructure
- Banzami is the reference operator (a child of BANZA, not BANZAMI)
- BanzAI is the Protocol OS (a peer of Banzami, both children of BANZA)

The current diagram tells visitors: "BANZAMI owns the protocol, the organization, and the ecosystem. Banzami and BanzAI are products within it." This is the pre-ADR-025 mental model.

**Required structure:**
```
BANZA (protocolo · infraestrutura · ecossistema)  ← ROOT
├─ BanzAI (Sistema Operativo do Protocolo)
│   └─ [Modules: Understand, Explain, Validate, Simulate, ...]
└─ Banzami (Operador de Referência)
    └─ [Products: Wallet, Business, QR, SDK]
```

**Required label changes:**
- Root node: `BANZAMI` → `BANZA`
- Root subtitle: `organização · protocolo · ecossistema` → `protocolo · infraestrutura · ecossistema`
- Title banner: `Arquitectura de Dois Níveis` → `Arquitectura de Três Níveis`
- Node order: BanzAI should appear at same visual level as Banzami (both children of BANZA)

**Note on "organização":** The word "organização" in the root node is especially problematic — it implies BANZAMI the organization owns the protocol. The organization is `Organização Banzami` (the legal entity), not the protocol. Removing it from the root node corrects this.

**Impact:** This is the first diagram a visitor encounters on the site (§1, first page). It sets the visitor's mental model before they read anything else. It is also the only diagram that contradicts the ADR-025 hierarchy at the structural level.

---

## D-002 — banzami-ecosystem.svg ✓ ALIGNED

**File:** `apps/docs/public/images/architecture/banzami-ecosystem.svg`
**Used in:** §3 (Visão Geral do Ecossistema)

**Structure:**
```
[Title: "Banza Ecosystem — PROGRAMMABLE FINANCIAL INFRASTRUCTURE FOR ANGOLA"]
└─ BANZA KERNEL — Rust Financial Core (18 crates)
    ├─ [18 kernel crates: ledger, wallets, consumer-wallets, ...]
    └─ [Operators layer with Banzami as reference operator]
```

**Verdict:** ALIGNED. BANZA is the root. Banzami appears as an operator implementing the protocol. The title correctly identifies this as BANZA infrastructure, not Banzami infrastructure.

---

## D-003 — banzamia-canonical-architecture.svg ✓ ALIGNED

**File:** `apps/docs/public/images/architecture/banzamia-canonical-architecture.svg`
**Used in:** §9 (BanzAI — "Arquitectura Canónica do Ecossistema")

**Structure:**
```
[Title: "Banza — Arquitectura Canónica do Ecossistema"]
[Subtitle: "PROTOCOLO · OPERADORES · CERTIFICAÇÃO · BANZAI · APLICAÇÕES"]
├─ Layer 1: Protocolo Banza — Kernel (Rust) [foundation]
├─ Layer 2: Operadores — Entidades certificadas
│   ├─ Banzami (L1 Payment Operator)
│   ├─ Sandbox Operator (L0)
│   ├─ Operador Futuro (L2–L4)
│   └─ SDK — TypeScript · Flutter · PHP
├─ Layer 3: Certification (L0→L4)
├─ Layer 4: BanzAI (Protocol OS)
└─ Layer 5: Applications
```

**Verdict:** ALIGNED. This is the canonical three-tier (actually five-layer) model correctly rendered. BANZA Kernel is the foundation. Banzami appears as a certified operator among others. BanzAI is a distinct layer, not a child of Banzami.

---

## D-004 — banzamia-cognitive-layer.svg ✓ ALIGNED

**Used in:** §9 (BanzAI as Cognitive Layer)

**Structure:** Shows four protocol layers (Física, Financeira, Governança, Cognitiva). BanzAI is the Cognitive Layer — a layer of BANZA protocol, not of Banzami product.

**Verdict:** ALIGNED.

---

## D-005 — protocol-operating-system.svg ✓ ALIGNED

**Used in:** §9 (BanzAI as Protocol OS)

**Structure:** Shows BanzAI as Protocol Operating System with 8 capabilities in orbit (Compreender, Explicar, Validar, Simular, Prever, Guiar, Certificar, Federar).

**Verdict:** ALIGNED. No Banzami claims in the OS architecture.

---

## D-006 — banzamia-product-architecture.svg ✓ ALIGNED

**Used in:** §9 (BanzAI 16 modules)

**Structure:** Shows 16 modules in 3 layers (Protocolo, Operador, Inteligência). Module names correctly attributed to BanzAI.

**Verdict:** ALIGNED.

---

## D-007 — banzamia-force-multiplier.svg ✓ ALIGNED

**Used in:** §9 (BanzAI as force multiplier)

**Structure:** Shows BanzAI multiplying each component of the BANZA ecosystem (Kernel, Certificação, RFCs, Integration Surface, Governança).

**Verdict:** ALIGNED.

---

## D-008 — banzamia-internal-architecture.svg ✓ ALIGNED

**Used in:** §9 (BanzAI internal architecture)

**Structure:** Shows BanzAI internal flow from user question to grounded response. Task Router, Knowledge Retrieval, Model Router, Tool execution.

**Verdict:** ALIGNED.

---

## D-009 — banzamia-model-routing.svg ✓ ALIGNED

**Used in:** §9 (model routing)

**Verdict:** ALIGNED. Shows routing between models (Qwen, Qwen Coder, DeepSeek).

---

## D-010 — banzamia-truth-model.svg ✓ ALIGNED

**Used in:** §9 (Tools determine truth)

**Verdict:** ALIGNED. "Ferramentas determinam a verdade. IA explica a verdade."

---

## D-011 — banzamia-knowledge-gap.svg ✓ ALIGNED

**Used in:** §9 (Protocol Knowledge Gap)

**Verdict:** ALIGNED. Shows developer experience with/without BanzAI.

---

## D-012 — certification-flow.svg ✓ ALIGNED

**Used in:** §7 (Modelo de Certificação)

**Verdict:** ALIGNED. Shows BANZA certification process for operators.

---

## D-013 — certification-copilot.svg ✓ ALIGNED

**Used in:** §9 (Certification Copilot)

**Verdict:** ALIGNED. BanzAI tool for certification readiness analysis.

---

## D-014 — federation.svg ✓ ALIGNED

**Used in:** §8 (Federação)

**Verdict:** ALIGNED. Shows BANZA federation between certified operators.

---

## D-015 — federation-intelligence.svg ✓ ALIGNED

**Used in:** §9 (Federation Intelligence)

**Verdict:** ALIGNED. BanzAI federation compatibility analysis tool.

---

## D-016 — service-topology.svg ✓ ALIGNED

**Used in:** §4 (Arquitectura Técnica)

**Verdict:** ALIGNED. Protocol service architecture (Go + Rust + PostgreSQL).

---

## D-017 — trace-flow.svg ✓ ALIGNED

**Used in:** §4 (Sistema de rastreabilidade)

**Verdict:** ALIGNED. Protocol trace architecture.

---

## D-018 — security-layers.svg ✓ ALIGNED

**Used in:** §13 (Segurança)

**Verdict:** ALIGNED. Protocol security architecture.

---

## D-019 — protocol-graph-architecture.svg ✓ ALIGNED

**Used in:** §9 (Protocol Graph)

**Verdict:** ALIGNED. BanzAI knowledge graph of protocol documents.

---

## D-020 — protocol-graph-explorer.svg ✓ ALIGNED

**Used in:** §9 (Graph Explorer)

**Verdict:** ALIGNED. BanzAI module UI.

---

## D-021 — graph-enhanced-retrieval.svg ✓ ALIGNED

**Used in:** §9 (RAG + Graph)

**Verdict:** ALIGNED. BanzAI retrieval pipeline.

---

## D-022 — agentic-research-flow.svg ✓ ALIGNED

**Used in:** §9 (Agentic Research)

**Verdict:** ALIGNED. BanzAI multi-step research pipeline.

---

## D-023 — protocol-simulator.svg ✓ ALIGNED

**Used in:** §9 (Protocol Simulator)

**Verdict:** ALIGNED. BanzAI what-if analysis tool.

---

## D-024 — protocol-memory.svg ✓ ALIGNED

**Used in:** §9 (Protocol Memory)

**Verdict:** ALIGNED. BanzAI operator journey tracking.

---

## D-025 — operator-digital-twin.svg ✓ ALIGNED

**Used in:** §9 (Digital Twin)

**Verdict:** ALIGNED. BanzAI operator virtual representation.

---

## D-026 — quality-dashboard-architecture.svg ✓ ALIGNED

**Used in:** §9 (Quality Dashboard)

**Verdict:** ALIGNED. BanzAI quality metrics.

---

## D-027 — rag-evaluation-architecture.svg ✓ ALIGNED

**Used in:** §9 (RAG evaluation)

**Verdict:** ALIGNED. BanzAI retrieval quality framework.

---

## D-028 — ecosystem-intelligence-layer.svg ✓ ALIGNED

**Used in:** §9 (Ecosystem Intelligence)

**Verdict:** ALIGNED. Four-layer intelligence model of BanzAI.

---

## D-029 — autonomous-protocol-vision.svg ✓ ALIGNED

**Used in:** §9 (Autonomous Protocol Vision)

**Verdict:** ALIGNED. Four phases of protocol evolution.

---

## D-030 — protocol-adoption-economics.svg ✓ ALIGNED

**Used in:** §9 (Adoption Economics)

**Verdict:** ALIGNED. BanzAI's effect on protocol adoption costs.

---

## D-031 — protocol-self-explanation.svg ✓ ALIGNED

**Used in:** §9 (Self-explaining Protocol)

**Verdict:** ALIGNED. Traditional vs BanzAI protocol explanation model.

---

## D-032 — force-multiplier-model.svg ✓ ALIGNED

**Used in:** §9 (Force Multiplier)

**Verdict:** ALIGNED. BanzAI multiplying six ecosystem components.

---

## D-033 — roadmap-architecture.svg ✓ ALIGNED

**Verdict:** ALIGNED.

---

## Summary

| Classification | Count | Files |
|---|---|---|
| **P0 — Conceptually false** | **1** | `brand-architecture.svg` |
| **ALIGNED** | **32** | All other SVGs |

**Critical finding:** 32 of 33 diagrams correctly represent the ADR-025 three-tier model. The single exception — `brand-architecture.svg` — is also the first diagram a visitor sees (§1, rendered on `banzami.org/o-que-e-o-banza`). It contradicts 32 correctly-aligned diagrams.

**Architectural irony:** `banzamia-canonical-architecture.svg` (D-003) — the diagram explicitly titled "Arquitectura Canónica" — correctly shows BANZA at the foundation, BanzAI as the OS layer, and Banzami as a certified operator. It is completely aligned. The only misaligned diagram is `brand-architecture.svg`, which appears in §1 before the canonical architecture is shown.

---

*Audit completed: 2026-05-30. No modifications applied.*
