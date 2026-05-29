---
title: BANZA Canonical Identity Remediation Plan v2 — BANZA-CANONICAL-IDENTITY-AUDIT — PHASE 2
version: 1.0
date: 2026-05-30
status: COMPLETE — all fixes applied
---

# BANZA Canonical Identity Remediation Plan v2

Reference: `docs/migration/banza-identity-deep-audit.md`

---

## Fixes Applied (2026-05-30)

### Fix 1 — BANZAMI_REFERENCE.md §15 Closing Statement (CRITICAL)

**File:** `docs/BANZAMI_REFERENCE.md:1825`

| | Text |
|---|---|
| Before | "O modelo está provado: o Pix no Brasil, o UPI na Índia, o M-Pesa em Moçambique. Angola tem as mesmas pré-condições. O Banzami é a infraestrutura." |
| After | "O modelo está provado: o Pix no Brasil, o UPI na Índia, o M-Pesa em Moçambique. Angola tem as mesmas pré-condições. O Banza é a infraestrutura." |

**Rationale:** The canonical reference document (single source of truth for the docs site) closed §15 with "O Banzami é a infraestrutura" — directly stating that Banzami IS the infrastructure. The canonical model is: BANZA is the infrastructure; Banzami is the reference operator/payment product. This is the highest-priority fix in the repository because this content propagates to the public section page for §15.

---

### Fix 2 — docs/product/positioning.md Full Rewrite (CRITICAL + POSITIONING DRIFT)

**File:** `docs/product/positioning.md`

This document was written before ADR-025 (the naming inversion) and positioned "Banzami" as the infrastructure throughout. It has been rewritten to the ADR-025 three-tier canonical hierarchy.

**Key changes:**

| | Text |
|---|---|
| One-line position (Before) | "Banzami é a infraestrutura programável de pagamentos instantâneos de Angola — QR-native, wallet-native, developer-first." |
| One-line position (After) | "Banza é o protocolo aberto de infraestrutura financeira programável. Banzami é o operador de referência — a rede de pagamentos instantâneos construída sobre o Banza." |
| "What Banza IS" table (Before) | "Angola's programmable instant payments infrastructure" attributed to Banzami |
| "What Banza IS" table (After) | Correctly attributes infrastructure to BANZA, product to Banzami, OS to BanzAI |
| Infrastructure layers (Before) | All four layers attributed to "Banzami" as infrastructure |
| Infrastructure layers (After) | BANZA = protocol + ledger + settlement; Banzami = consumer + merchant + developer layers |

**Rationale:** The positioning document is referenced by CLAUDE.md and strategy documents. A positioning document that inverts the canonical model is more dangerous than a comment in a code file — it creates a false mental model for anyone consulting it as a source of truth.

---

### Fix 3 — docs/api/README.md Opening Statement (CRITICAL)

**File:** `docs/api/README.md:3`

| | Text |
|---|---|
| Before | "Banzami is Angola's programmable instant payments infrastructure. The API is the developer entry point..." |
| After | "Banza is Angola's open programmable financial infrastructure. Banzami is the reference operator — the payment product built on Banza. This API is the developer entry point..." |

**Rationale:** Developer-facing API documentation is read by every developer integrating Banzami. The opening line set the wrong mental model: "Banzami IS the infrastructure." This is the exact inversion that ADR-025 was designed to correct.

---

### Fix 4 — docs/validation/README.md Opening Line (MISLEADING)

**File:** `docs/validation/README.md:3`

| | Text |
|---|---|
| Before | "Sistema de execução e validação do ecossistema Banzami." |
| After | "Sistema de execução e validação do ecossistema Banza." |

**Rationale:** The BANZA protocol validation system validates protocol compliance — it is a Banza infrastructure governance tool. Attributing it to the Banzami ecosystem implies Banzami owns the protocol governance.

---

### Fix 5 — BANZAMI_IMPLEMENTATION_MATRIX.json Meta Description (MISLEADING)

**File:** `docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` (meta.description)

| | Text |
|---|---|
| Before | "Implementation and validation matrix for the Banzami ecosystem — derived from BANZAMI_REFERENCE.md as single source of truth. Per ADR-015." |
| After | "Implementation and validation matrix for the Banza ecosystem — derived from BANZAMI_REFERENCE.md as single source of truth. Per ADR-015." |

**Rationale:** The implementation matrix tracks BANZA protocol implementation status. It is a protocol governance document.

---

### Fix 6 — BANZAMI_IMPLEMENTATION_MATRIX.json IDT-001 Description (MISLEADING)

**File:** `docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` (IDT-001.description)

| | Text |
|---|---|
| Before | "Fonte única de verdade para todo o ecossistema Banzami — definição canónica de produto, arquitectura, filosofia, UX e posicionamento." |
| After | "Fonte única de verdade para todo o ecossistema Banza — definição canónica de protocolo, arquitectura, filosofia, UX e posicionamento." |

**Rationale:** `BANZAMI_REFERENCE.md` defines the BANZA protocol. It is the protocol's canonical reference, not Banzami's product documentation. Also changed "produto" → "protocolo" to correctly describe what the reference document defines.

---

### Fix 7 — docs/banzamia/architecture.md SSE Example (MISLEADING)

**File:** `docs/banzamia/architecture.md:126`

| | Text |
|---|---|
| Before | `data: {"type":"chunk","content":"The Banzami protocol..."}` |
| After | `data: {"type":"chunk","content":"The Banza protocol..."}` |

**Rationale:** BanzAI explains and validates the BANZA protocol. An example BanzAI response that refers to "The Banzami protocol" contradicts BanzAI's purpose — it is the OS of the Banza protocol, not the Banzami protocol.

---

## Accepted (No Fix)

| Surface | Reason |
|---|---|
| `docs/adr/ADR-016-banzami-banza-brand-architecture.md` permits "ecossistema Banzami" | Pre-ADR-025 historical ADR. ADR-025 supersedes. ADR-025 superseded notice added to ADR-016 in Wave AB (previous session). |
| `assets/banza/guidelines/BANZA_BRAND_GUIDELINES.md` two-tier model | Frozen 2026-05-20. ADR-025 adds the third tier (BanzAI) but does not contradict the Banza/Banzami split. Guidelines remain valid at the brand level. |
| `README.md (Banza repo):13` "Banzami is Angola's instant payment network" | Private commercial product repo. Correctly describes the Banzami payment product. |
| Integration docs "Banzami app", "Banzami QR" | All product-layer references. Correct under ADR-025. |
| Domain docs "Banzami network", "Banzami-internal" | Product/internal references. Correct under ADR-025. |

---

## Verification Checklist

- [x] BANZAMI_REFERENCE.md §15 closing sentence: "O Banza é a infraestrutura."
- [x] docs/product/positioning.md: rewritten to ADR-025 three-tier hierarchy
- [x] docs/api/README.md: opening line corrects BANZA/Banzami hierarchy
- [x] docs/validation/README.md: "ecossistema Banza" (not Banzami)
- [x] BANZAMI_IMPLEMENTATION_MATRIX.json meta: "Banza ecosystem" (not Banzami)
- [x] BANZAMI_IMPLEMENTATION_MATRIX.json IDT-001: "ecossistema Banza" + "protocolo" (not produto)
- [x] docs/banzamia/architecture.md SSE example: "The Banza protocol..."
- [x] Build passes: `npm run build` — 0 errors
- [x] TypeScript: `npx tsc --noEmit` — 0 errors
- [x] Tests: 51/51 pass

---

## Commits

| Hash | Message |
|---|---|
| `[pending]` | fix(identity): BANZA-CANONICAL-IDENTITY-AUDIT Phase 2 — correct hierarchy inversions |

---

*Applied: 2026-05-30.*
