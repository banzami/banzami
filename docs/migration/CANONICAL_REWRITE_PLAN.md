---
title: CANONICAL_REWRITE_PLAN — BANZA-CANONICAL-REFERENCE-REWRITE
version: 1.0
date: 2026-05-30
status: PLAN — awaiting approval
---

# Canonical Rewrite Plan

**Objective:** Reach 100% ADR-025 conceptual consistency in `BANZAMI_REFERENCE.md` and its diagrams.

**Total items:** 8 (1 SVG rebuild + 7 text changes)
**Estimated effort:** Medium — all items are surgical (no full-section rewrites required)

**Execution rule:** Apply in priority order. Each item is independent — they can be applied in any sequence within a tier, but P0 items should be applied before P1 and P2.

---

## P0 — Conceptually False (apply first)

### REWRITE-001 — Rebuild brand-architecture.svg

**File:** `apps/docs/public/images/architecture/brand-architecture.svg`
**Gap:** GAP-001 in CANONICAL_IDENTITY_GAP_REPORT.md

**What to change:**

The entire SVG must be rebuilt with BANZA as the root node. The visual structure changes from a two-branch tree (two-tier) to a three-tier architecture.

**Before (current):**
```
[Title: "Arquitectura de Dois Níveis"]

BANZAMI (organização · protocolo · ecossistema)   ← ROOT (wrong entity)
├─ Banzami (produto principal de pagamento)
└─ BanzAI (Sistema Operativo de Protocolo)
```

**After (required):**
```
[Title: "Arquitectura de Três Níveis"]

BANZA (protocolo · infraestrutura · ecossistema)   ← ROOT (correct entity)
├─ BanzAI (Sistema Operativo do Protocolo)
│   └─ [Modules: Compreender · Explicar · Validar · Simular · Certificar · Federar]
└─ Banzami (Operador de Referência)
    └─ [Products: Wallet · Business · QR · SDK]
```

**Visual design guidance:**
- Root node: Keep the same dark red (#990011) fill. Replace "BANZAMI" text with "BANZA". Replace subtitle "organização · protocolo · ecossistema" with "protocolo · infraestrutura · ecossistema".
- BanzAI node: Keep the gold (#FEF0C7 fill, #D4A800 stroke) — already correct.
- Banzami node: Keep the pink (#FEF9F5 fill, #DBBCB2 stroke) — already correct.
- Column order: BanzAI left / Banzami right, OR Banzami left / BanzAI right — either order is acceptable. ADR-025 does not mandate order.
- BanzAI module list: Replace the 6-item list (Chat, Operator Builder, Conformance, Trace Explainer, SDK Assistant, RFC/ADR Explorer) with the canonical 6-verb OS capabilities: Compreender · Explicar · Validar · Simular · Certificar · Federar. This aligns with the roadmap page and `/banzamia` page.

**Files affected:**
- `apps/docs/public/images/architecture/brand-architecture.svg` — rebuild

---

### REWRITE-002 — Change §1 Subsection Heading

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** Line 48
**Gap:** GAP-002

**Before:**
```markdown
### Arquitectura de dois níveis
```

**After:**
```markdown
### Arquitectura de três níveis
```

**Rationale:** The canonical model has three tiers (BANZA → BanzAI + Banzami). "Dois níveis" encodes the ADR-016 two-tier model. This is a one-word change in the heading.

---

### REWRITE-003 — Update ADR Reference

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** Line 52
**Gap:** GAP-003

**Before:**
```markdown
Esta arquitectura de marca está definida no ADR-016.
```

**After:**
```markdown
Esta arquitectura está definida no ADR-025. O ADR-016 define a história da separação Banza/Banzami; o ADR-025 estabelece a hierarquia de três níveis com BanzAI como Sistema Operativo do Protocolo.
```

**Rationale:** The current text sends readers to ADR-016 (the pre-ADR-025 two-tier model document) for understanding the architecture. ADR-025 is the canonical reference for the current three-tier model.

---

## P1 — Misleading (apply second)

### REWRITE-004 — Rename "Os quatro pilares do Banzami" and Update Framing

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** Lines 54–61
**Gap:** GAP-004

**Before:**
```markdown
### Os quatro pilares do Banzami

| Pilar | O que significa |
|-------|----------------|
| **Programmable** | Qualquer aplicação angolana integra pagamentos via SDK em horas. O Banzami não é só uma app — é a camada de pagamentos de Angola. |
| **Wallet-native** | Cada conta é uma carteira em Kwanza. Pagamentos são transferências directas entre carteiras. Sem IBAN. Sem código bancário. |
| **QR-native** | A superfície principal de pagamento é um código QR. O comerciante imprime. O consumidor faz o scan. Instantâneo. Sem terminal. |
| **Instant settlement** | O dinheiro move-se no momento da confirmação — confirmado, liquidado e visível em segundos. |
```

**After:**
```markdown
### Os quatro princípios do protocolo

Qualquer operador certificado Banza implementa estes quatro princípios. O Banzami é a implementação de referência — não o detentor exclusivo destas propriedades.

| Princípio | O que significa |
|-----------|----------------|
| **Programmable** | Qualquer aplicação integra pagamentos via SDK em horas. O protocolo é SDK-first — não uma app fechada. |
| **Wallet-native** | Cada conta é uma carteira em Kwanza. Pagamentos são transferências directas entre carteiras. Sem IBAN. Sem código bancário. |
| **QR-native** | A superfície principal de pagamento é um código QR. O comerciante imprime. O consumidor faz o scan. Instantâneo. Sem terminal. |
| **Instant settlement** | O dinheiro move-se no momento da confirmação — confirmado, liquidado e visível em segundos. |
```

**Key changes:**
1. Heading: "pilares do Banzami" → "princípios do protocolo"
2. Add one sentence explicitly stating these apply to any certified operator, not just Banzami
3. Remove "O Banzami não é só uma app — é a camada de pagamentos de Angola." from the Programmable row — this is a product claim, not a protocol claim. Replace with "O protocolo é SDK-first."

---

### REWRITE-005 — Fix BanzAI Opening Sentence in §9

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** Line 632
**Gap:** GAP-005

**Before:**
```markdown
O BanzAI é um produto de primeira classe do ecossistema Banza — não um componente interno, não um chatbot, não um wrapper genérico de LLM. É a interface cognitiva do protocolo.
```

**After:**
```markdown
O BanzAI é o Sistema Operativo nativo do protocolo Banza — não um componente interno, não um chatbot, não um wrapper genérico de LLM. É a interface cognitiva do protocolo.
```

**Key change:** "produto de primeira classe" → "Sistema Operativo nativo"

**Rationale:** This aligns §9 opener with the correct framing used on `/banzamia`, `/sobre-banzamia`, `HeroBanzamIAWidget`, and `HomeBanzamIAEntry`. The phrase "Sistema Operativo nativo do protocolo Banza" is already the canonical descriptor for BanzAI across all other surfaces.

---

### REWRITE-006 — Fix §17 Vision Climax

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** Line 1877
**Gap:** GAP-007

**Before:**
```markdown
**Isso é o Banzami — construído pelo Banza.**
```

**After:**
```markdown
**Isso é a infraestrutura Banza em acção. O Banzami é como Angola a acede.**
```

**Rationale:** The vision climax must leave the visitor with BANZA as the infrastructure protagonist. The rewrite:
1. Names BANZA as the subject of the bold statement
2. Correctly positions Banzami as the access layer for Angola
3. Preserves the Angola-first emotional resonance of the section

**Alternative (if shorter preferred):**
```markdown
**Isso é o protocolo Banza. O Banzami é como Angola o vive.**
```

---

## P2 — Legacy Wording (apply last)

### REWRITE-007 — Fix §5 Payment Flow Attribution

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** Line 294
**Gap:** GAP-006

**Before:**
```markdown
Todo o fluxo de pagamento Banzami produz três montantes monetários com semântica exacta:
```

**After:**
```markdown
Todo o fluxo de pagamento Banza produz três montantes monetários com semântica exacta:
```

**Rationale:** The gross/net/fee model is INV-STL-001 — a BANZA protocol invariant enforced on all certified operators, not a Banzami-specific payment flow. One-word change: "Banzami" → "Banza".

---

## Execution Checklist

### Pre-execution
- [ ] Read current `brand-architecture.svg` (for exact SVG rebuild)
- [ ] Confirm build passes before starting
- [ ] Confirm 51/51 tests pass before starting

### P0 (apply first)
- [ ] REWRITE-001 — Rebuild `brand-architecture.svg`
- [ ] REWRITE-002 — §1 heading: "dois níveis" → "três níveis"
- [ ] REWRITE-003 — §1 ADR reference: ADR-016 → ADR-025

### P1 (apply second)
- [ ] REWRITE-004 — §1 "quatro pilares do Banzami" → "quatro princípios do protocolo"
- [ ] REWRITE-005 — §9 BanzAI opener: "produto de primeira classe" → "Sistema Operativo nativo"
- [ ] REWRITE-006 — §17 vision climax: BANZA as protagonist

### P2 (apply last)
- [ ] REWRITE-007 — §5 "fluxo de pagamento Banzami" → "fluxo de pagamento Banza"

### Post-execution
- [ ] Build passes: `npm run build` — 0 errors
- [ ] TypeScript: `npx tsc --noEmit` — 0 errors
- [ ] Tests: 51/51 pass
- [ ] Visual check: `banzami.org/o-que-e-o-banza` — new diagram shows BANZA at root
- [ ] Commit per logical unit
- [ ] Push origin/main
- [ ] Deploy: `./deploy.sh docs-frontend`

---

## Visitor Mental Model — Before vs After

### Before (current state)
A visitor landing on `banzami.org/o-que-e-o-banza` sees:
1. Title diagram: BANZAMI at the top as "organização · protocolo · ecossistema"
2. Heading: "Arquitectura de dois níveis"
3. Four pillars: titled as "pilares do Banzami"
4. §9 BanzAI: called "produto de primeira classe"
5. §17 vision climax: "Isso é o Banzami"

**Mental model formed:** "BANZAMI is the top-level entity. Banzami and BanzAI are both products inside BANZAMI."

### After (post-rewrite)
A visitor landing on `banzami.org/o-que-e-o-banza` sees:
1. Title diagram: BANZA at the top as "protocolo · infraestrutura · ecossistema"
2. Heading: "Arquitectura de três níveis"
3. Four pillars: "princípios do protocolo" (any operator implements them)
4. §9 BanzAI: "Sistema Operativo nativo do protocolo Banza"
5. §17 vision climax: "Isso é a infraestrutura Banza em acção."

**Mental model formed:** "BANZA is the open protocol. BanzAI is the Protocol OS. Banzami is the reference operator that proves it works."

---

## What This Plan Does NOT Change

- §2 Princípios Fundamentais — ALIGNED, no change
- §3 Visão Geral do Ecossistema — ALIGNED, no change
- §4 Arquitectura Técnica — ALIGNED, no change
- §6 Governança — ALIGNED, no change
- §7 Modelo de Certificação — ALIGNED, no change
- §8 Federação — ALIGNED, no change
- §10 Banzami para Programadores — ALIGNED, no change
- §11 Banzami para Comerciantes — ALIGNED, no change
- §12 Para Consumidores — ALIGNED, no change
- §13 Segurança — ALIGNED, no change
- §14 Sandbox — ALIGNED, no change
- §15 Por que Angola — ALIGNED (Phase 2 fix applied), no change
- §16 Roadmap — ALIGNED, no change
- 32 of 33 SVGs — ALIGNED, no change
- All navigation, metadata, OG tags — ALIGNED (previous sessions), no change

---

*Plan created: 2026-05-30. Awaiting execution approval.*
