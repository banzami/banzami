---
title: CANONICAL_REWRITE_EXECUTION_REPORT — BANZA-CANONICAL-REFERENCE-REWRITE
version: 1.0
date: 2026-05-30
status: EXECUTION COMPLETE
---

# Canonical Rewrite Execution Report

**Operation:** BANZA-CANONICAL-REWRITE-EXECUTION  
**Source plan:** `docs/migration/CANONICAL_REWRITE_PLAN.md`  
**Source gaps:** `docs/migration/CANONICAL_IDENTITY_GAP_REPORT.md`  
**Executed against commit:** `ec830e5` (pre-execution HEAD)  
**Items executed:** 8 (1 SVG rebuild + 7 text edits)  
**Build status post-execution:** PASS (0 errors)  
**Test status post-execution:** 51/51 PASS  

---

## Objective

Achieve 100% ADR-025 conceptual alignment in `BANZAMI_REFERENCE.md` and its associated diagrams.

**Target conditions:**
- 0 remaining ADR-016 architecture model references (treating ADR-016 as canonical)
- 0 remaining occurrences where Banzami is presented as protocol, ecosystem, or infrastructure
- 0 remaining occurrences where BanzAI is presented as a product rather than the Protocol OS
- 100% three-tier hierarchy consistently encoded: BANZA → BanzAI + Banzami

---

## Files Modified

### 1. `apps/docs/public/images/architecture/brand-architecture.svg`

**Change type:** Full rebuild (SVG content replaced)  
**Gap addressed:** GAP-001 (P0 — Conceptually false)  
**REWRITE item:** REWRITE-001  

**Before:**
- Root node: `BANZAMI` with subtitle `organização · protocolo · ecossistema`
- Title: `Arquitectura de Dois Níveis`
- Banzami subtitle: `produto principal de pagamento`
- BanzAI section: labelled `MÓDULOS`, listing product feature names

**After:**
- Root node: `BANZA` with subtitle `protocolo · infraestrutura · ecossistema`
- Title: `Arquitectura de Três Níveis`
- Banzami subtitle: `operador de referência · produto`
- BanzAI section: labelled `CAPACIDADES`, listing the 6 canonical Protocol OS verbs: Compreender · Explicar · Validar · Simular · Certificar · Federar

**Structural correction:** The diagram now matches the 32 other aligned SVGs. BANZA is the root. BanzAI and Banzami are peer children. The word "organização" is removed from the root — it implied BANZAMI the organization owned the protocol.

---

### 2. `docs/BANZAMI_REFERENCE.md`

Seven surgical edits. No full-section rewrites.

#### Edit 1 — §1 Section Heading (line 48)
**REWRITE item:** REWRITE-002 (P0)

```
BEFORE: ### Arquitectura de dois níveis
AFTER:  ### Arquitectura de três níveis
```

#### Edit 2 — §1 Alt-text (line 50)
**REWRITE item:** REWRITE-001 companion (P0)

```
BEFORE: ![Arquitectura de dois níveis — Banza (protocolo) ramifica em Banzami (produto) e BanzAI (inteligência)](/images/architecture/brand-architecture.svg)
AFTER:  ![Arquitectura de três níveis — BANZA (protocolo) ramifica em BanzAI (Sistema Operativo do Protocolo) e Banzami (Operador de Referência)](/images/architecture/brand-architecture.svg)
```

#### Edit 3 — §1 ADR Reference (line 52)
**REWRITE item:** REWRITE-003 (P0)

```
BEFORE: Esta arquitectura de marca está definida no ADR-016.

AFTER:  Esta arquitectura está definida no ADR-025. O ADR-016 documenta a história da
        separação Banza/Banzami; o ADR-025 estabelece a hierarquia de três níveis com
        BanzAI como Sistema Operativo do Protocolo.
```

#### Edit 4 — §1 Pillars Heading and Framing (lines 54–61)
**REWRITE item:** REWRITE-004 (P1)

```
BEFORE: ### Os quatro pilares do Banzami

AFTER:  ### Os quatro princípios do protocolo
        Qualquer operador certificado Banza implementa estes quatro princípios. O
        Banzami é a implementação de referência — não o detentor exclusivo destas
        propriedades.
```

Programmable row corrected:
```
BEFORE: O Banzami não é só uma app — é a camada de pagamentos de Angola.
AFTER:  O protocolo é SDK-first — qualquer operador certificado expõe esta superfície.
```

#### Edit 5 — §5 Monetary Flow Attribution (line 294→296)
**REWRITE item:** REWRITE-007 (P2)

```
BEFORE: Todo o fluxo de pagamento Banzami produz três montantes monetários com semântica exacta:
AFTER:  Todo o fluxo de pagamento Banza produz três montantes monetários com semântica exacta:
```

#### Edit 6 — §9 BanzAI Opening Sentence (line 632→634)
**REWRITE item:** REWRITE-005 (P1)

```
BEFORE: O BanzAI é um produto de primeira classe do ecossistema Banza — não um componente
        interno, não um chatbot, não um wrapper genérico de LLM. É a interface cognitiva
        do protocolo.

AFTER:  O BanzAI é o Sistema Operativo nativo do protocolo Banza — não um componente
        interno, não um chatbot, não um wrapper genérico de LLM. É a interface cognitiva
        do protocolo.
```

#### Edit 7 — §17 Vision Climax (line 1877→1879)
**REWRITE item:** REWRITE-006 (P1)

```
BEFORE: **Isso é o Banzami — construído pelo Banza.**
AFTER:  **Isso é a infraestrutura Banza em acção. O Banzami é como Angola a acede.**
```

#### Edit 8 — References Section (lines 1930→1932–1933)
**Additional correction (companion to REWRITE-003)**

```
BEFORE: - ADR-016 — Arquitectura de marca Banza/Banzami (superseded for brand hierarchy
          by ADR-025)

AFTER:  - ADR-025 — Hierarquia canónica de três níveis: BANZA (protocolo) · BanzAI
          (Sistema Operativo) · Banzami (Operador de Referência)
        - ADR-016 — Arquitectura de marca Banza/Banzami (histórico — superseded por
          ADR-025)
```

---

## Diagrams

### Replaced
| File | Change |
|------|--------|
| `brand-architecture.svg` | Full rebuild — root BANZA, three-tier structure, CAPACIDADES verb list |

### Unchanged (all aligned)
32 of 33 SVGs were already 100% ADR-025 aligned per `CANONICAL_DIAGRAM_AUDIT.md`. No changes applied.

---

## ADR Reference Verification

| Location | Status |
|----------|--------|
| §1 line 52 | ADR-025 is now the primary citation. ADR-016 is noted as historical. ✓ |
| §1 references section lines 1932–1933 | ADR-025 listed first. ADR-016 marked "histórico — superseded". ✓ |
| Line 1162 (protocol graph example) | `"RFC-001 → ADR-016 → OAS-TRANSFER"` — document node in graph relationship chain, not an architecture model claim. Acceptable. |

**Remaining ADR-016 architecture model references:** 0  
**Remaining ADR-025 citations as non-canonical:** 0

---

## Conceptual Inversion Verification

Post-execution grep results:

| Pattern | Remaining occurrences | Classification |
|---------|----------------------|----------------|
| `Arquitectura de dois níveis` | 0 | ✓ Eliminated |
| `pilares do Banzami` | 0 | ✓ Eliminated |
| `produto de primeira classe` | 0 | ✓ Eliminated |
| `Esta arquitectura.*ADR-016` | 0 | ✓ Eliminated |
| `fluxo de pagamento Banzami` | 0 | ✓ Eliminated |
| `Isso é o Banzami — construído` | 0 | ✓ Eliminated |
| `organização · protocolo · ecossistema` (in SVG root) | 0 | ✓ Eliminated |

**Remaining occurrences where Banzami is presented as protocol, ecosystem, or infrastructure:** 0  
**Remaining occurrences where BanzAI is presented as a product:** 0

---

## Remaining ADR-016 Occurrences (Non-Architecture-Model)

Two occurrences of "ADR-016" remain in `BANZAMI_REFERENCE.md`. Both are correct and intentional:

1. **Line 52** — "O ADR-016 documenta a história da separação Banza/Banzami" — historical reference
2. **Line 1162** — `"RFC-001 → ADR-016 → OAS-TRANSFER"` — protocol graph knowledge node
3. **Line 1933** — "ADR-016 — Arquitectura de marca Banza/Banzami (histórico — superseded por ADR-025)" — reference section

None of these treat ADR-016 as the canonical architecture model.

---

## Remaining Conceptual Inconsistencies

**None found.**

The 32 already-aligned SVGs, 14 already-aligned reference sections, and the 3 corrected P0 items in §1 now form a fully consistent canonical picture. Every surface where BANZA identity is described — from the first diagram a visitor sees to the final bold sentence in §17 — encodes the ADR-025 three-tier model.

---

## Build and Test Verification

| Check | Result |
|-------|--------|
| `npm run build` (from `apps/docs/`) | PASS — 0 errors |
| `npm test -- lib/__tests__/reference.test.ts` | PASS — 51/51 |
| TypeScript `npx tsc --noEmit` | PASS — 0 errors |

---

## Visitor Mental Model — After

A visitor landing on `banzami.org/o-que-e-o-banza` now encounters:

1. **First diagram (§1):** BANZA at the root as "protocolo · infraestrutura · ecossistema"
2. **Section heading:** "Arquitectura de três níveis"
3. **ADR reference:** ADR-025 as canonical; ADR-016 as historical
4. **Four principles:** "Os quatro princípios do protocolo" — explicitly attributed to any certified operator
5. **§9 BanzAI opener:** "Sistema Operativo nativo do protocolo Banza"
6. **§17 vision climax:** "Isso é a infraestrutura Banza em acção. O Banzami é como Angola a acede."

**Mental model formed:** BANZA is the open protocol. BanzAI is the Protocol OS. Banzami is the reference operator that proves it works. Any certified operator implements the same four protocol principles.

---

## ADR-025 Conceptual Alignment — Final Score

| Domain | Before | After |
|--------|--------|-------|
| Brand architecture SVG | ✗ BANZAMI at root | ✓ BANZA at root |
| §1 heading | ✗ dois níveis (ADR-016 model) | ✓ três níveis |
| §1 ADR citation | ✗ ADR-016 as canonical | ✓ ADR-025 as canonical |
| §1 four pillars attribution | ✗ "pilares do Banzami" | ✓ "princípios do protocolo" |
| §5 monetary flow attribution | ✗ "fluxo de pagamento Banzami" | ✓ "fluxo de pagamento Banza" |
| §9 BanzAI classification | ✗ "produto de primeira classe" | ✓ "Sistema Operativo nativo" |
| §17 vision climax protagonist | ✗ Banzami | ✓ BANZA |
| References section | ✗ ADR-016 listed, ADR-025 absent | ✓ ADR-025 primary, ADR-016 historical |
| 32 other SVGs | ✓ Already aligned | ✓ Unchanged |
| 14 other reference sections | ✓ Already aligned | ✓ Unchanged |

**Overall ADR-025 conceptual alignment:** 100%

---

*Execution completed: 2026-05-30. Build: PASS. Tests: 51/51.*
