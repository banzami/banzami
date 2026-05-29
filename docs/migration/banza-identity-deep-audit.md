---
title: BANZA Canonical Identity Audit — BANZA-CANONICAL-IDENTITY-AUDIT — PHASE 2
version: 1.0
date: 2026-05-30
status: COMPLETE — fixes applied
---

# BANZA Canonical Identity Deep Structural Audit

**Scope:** Repository-wide conceptual identity audit across `/Users/fm65/Banza/` and `/Users/fm65/Banzami/`. Not a word search — this audit classifies conceptual implications, hierarchy statements, and narrative structures.

**Canonical model (ADR-025):**

| Entity | What it is | What it is NOT |
|---|---|---|
| **BANZA** | Open programmable financial infrastructure — protocol, ledger, settlement engine, certification system | A wallet app, QR product, company name, consumer-facing product |
| **BanzAI** | Native Protocol Operating System — explains, validates, simulates, certifies, traces the protocol | A chatbot, documentation assistant, support tool |
| **Banzami** | Reference operator and payment product built on BANZA — wallets, QR, merchant tools, SDKs | The organization, the protocol, the infrastructure, the ecosystem |

**Protected identifiers (never change):** `banzami.org`, `@banzami.org`, `Banzami Lda`, `/.well-known/banzami/`, `BANZAMI:` QR prefix, `BANZAMI-SBX:`, `Organização Banzami`

---

## Executive Summary

| Class | Description | Surfaces Found | Status |
|---|---|---|---|
| **A — CRITICAL hierarchy inversions** | Banzami explicitly IS the infrastructure/protocol | 3 | Fixed |
| **B — MISLEADING ecosystem attribution** | "Banzami ecosystem" used where "Banza ecosystem" is correct | 4 | Fixed |
| **C — POSITIONING drift** | Document has pre-ADR-025 product-first framing throughout | 1 document | Fixed |
| **D — DOCUMENTATION gaps** | Technical docs open with inverted positioning | 1 | Fixed |
| **E — TERMINOLOGY** (acceptable) | "Banzami app", "Banzami network" in product-layer contexts | Many | Protected — no action |
| **F — NARRATIVE** (acceptable) | Vision statements with Angola-first framing, pre-ADR-025 context | Several | Accepted |

**Total CRITICAL + MISLEADING fixes applied:** 9

---

## Classification Definitions

| Class | Definition | Action |
|---|---|---|
| **A — CRITICAL** | A sentence explicitly states Banzami IS the infrastructure, the protocol, or the ecosystem — directly contradicting ADR-025 | Fix immediately |
| **B — MISLEADING** | A phrase attributes the ecosystem, the protocol, or the infrastructure to Banzami (e.g. "Banzami ecosystem" in a protocol context) | Fix immediately |
| **C — POSITIONING DRIFT** | A document's framing as a whole positions Banzami as the infrastructure rather than the reference operator | Rewrite |
| **D — DOCUMENTATION GAP** | A technical document opens with or prominently contains an inverted identity claim | Fix immediately |
| **E — ACCEPTABLE PRODUCT REFERENCE** | "Banzami app", "Banzami QR", "Banzami network" in product/consumer/merchant contexts | No action |
| **F — ACCEPTABLE NARRATIVE** | Pre-ADR-025 vision statements, Angola-first framing, organizational references | No action |

---

## Top 20 Priority Fixes (Ordered by Impact)

| Priority | File | Location | Class | Finding | Status |
|---|---|---|---|---|---|
| 1 | `docs/BANZAMI_REFERENCE.md` | Line 1825 | A | "O Banzami é a infraestrutura." — the canonical reference document contradicts the canonical model | **FIXED** |
| 2 | `docs/product/positioning.md` | Line 11 (and throughout) | A+C | "Banzami é a infraestrutura programável de pagamentos instantâneos de Angola" — the positioning document inverts the hierarchy in its opening statement and throughout | **FIXED** |
| 3 | `docs/api/README.md` | Line 3 | A | "Banzami is Angola's programmable instant payments infrastructure." — inverts hierarchy in developer-facing API docs | **FIXED** |
| 4 | `docs/validation/README.md` | Line 3 | B | "Sistema de execução e validação do ecossistema Banzami." — protocol validation system attributed to Banzami | **FIXED** |
| 5 | `docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` | Line 7 | B | "Implementation and validation matrix for the Banzami ecosystem" — ecosystem attributed to Banzami in the matrix meta | **FIXED** |
| 6 | `docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` | Line 573 | B | "Fonte única de verdade para todo o ecossistema Banzami" — reference document described as serving the Banzami ecosystem | **FIXED** |
| 7 | `docs/banzamia/architecture.md` | Line 126 | B | "The Banzami protocol..." — protocol attributed to Banzami in an SSE response example | **FIXED** |
| 8 | `docs/adr/ADR-016-banzami-banza-brand-architecture.md` | Line 113 | F | Explicitly permits "ecossistema Banzami" — pre-ADR-025 framing now superseded by ADR-025 | Accepted — historical ADR, add superseded notice |
| 9 | `assets/banza/guidelines/BANZA_BRAND_GUIDELINES.md` | §1 | C | Defines "Banza = Organization / infrastructure ecosystem" — pre-ADR-025 two-tier framing; ADR-025 adds BanzAI as the third tier | Accepted — guidelines frozen 2026-05-20; ADR-025 supersedes |
| 10 | `docs/glossary.md` | "Banzami network" | E | "A human-readable payment address...on the Banzami network" — product-layer reference; acceptable | No action |
| 11 | `docs/domains/merchant-onboarding/README.md` | Line 5 | E | "...joins the Banzami network" — product-layer reference; acceptable | No action |
| 12 | `docs/domains/reconciliation/README.md` | Line 40 | E | "settlement_id — the Banzami-internal ID" — internal technical identifier; acceptable | No action |
| 13 | Integration docs (`/doa/`) | Multiple | E | "Banzami app", "Banzami QR", "Banzami payment experience" — all product-layer, correct | No action |
| 14 | `sdk/typescript/package.json` | Line 4 | E | "Official JavaScript/TypeScript SDK for the Banzami payment platform" — SDK belongs to Banzami product layer; acceptable | No action |
| 15 | `README.md` (Banza repo) | Line 13 | F | "Banzami is Angola's instant payment network: a four-layer platform..." — this is the Banzami product README; it correctly describes the Banzami product | No action |
| 16 | `docs/audit/alignment-fixes.md` | Line 133 | F | Historical alignment-fixes document from pre-ADR-025 migration; migration history | No action |
| 17 | `docs/migration/wave-3-ui-migration-plan.md` | Multiple | F | Migration plan document — historical record; references pre-ADR-025 strings | No action |
| 18 | `apps/docs/schemas/operator-manifest.schema.json` | Line 5 | E | "Schema for operator entries in the Banzami public operator registry." — product registry; acceptable | No action |
| 19 | `apps/docs/data/operators.json` | Line 5 | E | "the canonical open-source sandbox operator maintained by the Banzami project" — organizational reference; acceptable | No action |
| 20 | `apps/validation-studio/app/layout.tsx` | Line 11 | E | "Local governance editor for the Banzami implementation matrix" — governance tool descriptor; acceptable | No action |

---

## Class A — CRITICAL Hierarchy Inversions

### A-001 — BANZAMI_REFERENCE.md:1825

**File:** `docs/BANZAMI_REFERENCE.md`
**Line:** 1825
**Section:** §15 — Por que Angola. Por que Agora.

**Finding:**
> "O modelo está provado: o Pix no Brasil, o UPI na Índia, o M-Pesa em Moçambique. Angola tem as mesmas pré-condições. O Banzami é a infraestrutura."

The canonical reference document — the single source of truth for the entire documentation site — closes its most persuasive section (§15, Why Angola, Why Now) with a sentence that directly states Banzami IS the infrastructure. This inverts the canonical model: BANZA is the infrastructure; Banzami is the reference operator/product.

This is the highest-priority fix in the repository because `BANZAMI_REFERENCE.md` is read at build time by the docs site and its content propagates to every section page.

**Fix applied:**
> "O Banza é a infraestrutura."

---

### A-002 — docs/product/positioning.md (throughout)

**File:** `docs/product/positioning.md`
**Lines:** 11, 102, 104, 111

**Finding:** The positioning document was written before ADR-025 (the naming inversion). Its opening statement:
> "Banzami é a infraestrutura programável de pagamentos instantâneos de Angola"

...directly inverts the canonical model. The document also describes four infrastructure layers, all attributed to "Banzami", and its "What Banza IS" section uses "Banza" and "Banzami" interchangeably.

**Fix applied:** Full document rewrite to ADR-025 framing. See remediation plan for before/after.

---

### A-003 — docs/api/README.md:3

**File:** `docs/api/README.md`
**Line:** 3

**Finding:**
> "Banzami is Angola's programmable instant payments infrastructure."

Developer-facing API documentation opens with a direct hierarchy inversion. Any developer reading this before integrating the Banzami SDK will conclude that Banzami is the infrastructure — not the product layer built on Banza infrastructure.

**Fix applied:**
> "Banza is Angola's open programmable financial infrastructure. Banzami is the reference operator — the payment product built on Banza."

---

## Class B — MISLEADING Ecosystem Attribution

### B-001 — docs/validation/README.md:3

**Finding:** "Sistema de execução e validação do ecossistema Banzami."

The Banza protocol validation system is presented as belonging to the Banzami ecosystem. The validation system validates BANZA protocol compliance — it is a Banza infrastructure governance tool, not a Banzami product tool.

**Fix applied:** "Sistema de execução e validação do ecossistema Banza."

---

### B-002 — BANZAMI_IMPLEMENTATION_MATRIX.json:7 (meta description)

**Finding:** "Implementation and validation matrix for the Banzami ecosystem"

The implementation matrix tracks what is and isn't implemented of the BANZA protocol specification. It is a protocol governance document, not a product document.

**Fix applied:** "Implementation and validation matrix for the Banza ecosystem"

---

### B-003 — BANZAMI_IMPLEMENTATION_MATRIX.json:573 (IDT-001 description)

**Finding:** "Fonte única de verdade para todo o ecossistema Banzami — definição canónica de produto, arquitectura, filosofia, UX e posicionamento."

This describes `BANZAMI_REFERENCE.md` as serving the Banzami ecosystem. The reference document defines the BANZA protocol — it serves the Banza protocol ecosystem, not the Banzami product.

**Fix applied:** "Fonte única de verdade para todo o ecossistema Banza — definição canónica de protocolo, arquitectura, filosofia, UX e posicionamento."

---

### B-004 — docs/banzamia/architecture.md:126

**Finding:** In the SSE response example:
> `data: {"type":"chunk","content":"The Banzami protocol..."}`

An example BanzAI streaming response attributes the protocol to Banzami. BanzAI explains the BANZA protocol, not the Banzami protocol.

**Fix applied:** `data: {"type":"chunk","content":"The Banza protocol..."}`

---

## Class C — Positioning Drift

### C-001 — docs/product/positioning.md (full document)

Pre-ADR-025 document. Entire framing positions Banzami as the infrastructure. Rewritten to ADR-025 framing — see remediation plan.

---

## Class D — Documentation Gaps

### D-001 — docs/api/README.md

See A-003. Same finding — the opening statement is the most visible line in the developer API documentation.

---

## Class E — Acceptable Product References (No Action)

The following phrases are correct under ADR-025 — they refer to the Banzami payment product at the product layer:

- "Banzami app" — the Banzami consumer mobile app
- "Banzami QR" — QR payments via the Banzami product
- "Banzami SDK" — the SDK for integrating the Banzami product
- "Banzami network" — the payment network operated by Banzami (the product)
- "Banzami Business" — merchant tooling within the Banzami product
- "Banzami dashboard" — merchant/developer dashboard
- "Banzami payment platform" — acceptable description of the product layer
- "joins the Banzami network" — merchants joining the product network
- "BANZAMI: QR prefix" — protected wire format identifier
- "Banzami-internal ID" — internal system identifier
- "Organização Banzami" — organizational reference

---

## Class F — Acceptable Narrative (No Action)

- `README.md (Banza repo):13` — "Banzami is Angola's instant payment network: a four-layer platform..." — this is the private commercial Banzami product repo's README. It correctly describes the Banzami product.
- `docs/adr/ADR-016-banzami-banza-brand-architecture.md` — pre-ADR-025 ADR; historical record; ADR-025 supersedes where they conflict.
- Integration docs (`/doa/`) — all correctly reference "Banzami app" for the payment consumer experience.
- Vision statements — Angola-first narrative framing does not constitute a hierarchy inversion.

---

## BanzAI Identity Audit (Cross-Check)

| Surface | Finding | Classification |
|---|---|---|
| `docs/banzamia/architecture.md` overall | Correctly presents BanzAI as a protocol OS with 16 modules | ALIGNED |
| `docs/banzamia/architecture.md:126` | "The Banzami protocol..." in SSE example | MISLEADING → FIXED |
| `/banzamia` page metadata | "Protocol Operating System" | ALIGNED |
| `/sobre-banzamia` page | "Não é um chatbot. É a interface cognitiva do protocolo." | ALIGNED |
| `/roadmap` page | "Protocol Operating System for the Banza protocol" | ALIGNED |
| `HomeBanzamIAEntry` descriptor | "O Sistema Operativo nativo do Protocolo Banza" | ALIGNED (fixed prev. session) |
| Hero subheadline | Includes BanzAI as foundational differentiator | ALIGNED (fixed prev. session) |

---

## Repository Summary

| Repository | CRITICAL | MISLEADING | Acceptable | No Action |
|---|---|---|---|---|
| `/Users/fm65/Banza/` (main repo) | 3 | 4 | Many | Many |
| `/Users/fm65/Banzami/` (kernel) | 0 | 0 | Several | Several |
| **Total fixes applied** | **3** | **4** | — | — |

---

*Audit completed: 2026-05-30. All CRITICAL and MISLEADING fixes applied.*
