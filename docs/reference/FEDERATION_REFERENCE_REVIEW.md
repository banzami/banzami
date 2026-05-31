# BANZA Federation Reference Review

**Document ID:** BANZA-FEDERATION-REFERENCE-INTEGRATION-001  
**Date:** 2026-05-31  
**Status:** Canonical — gap analysis and integration record for the federation public reference layer.

---

## 1. Scope

This document audits the current state of federation explanations across the BANZA public reference layer and identifies what was missing before the federation section was rewritten.

Files reviewed:

| File | Lines | Federation coverage |
|------|-------|---------------------|
| `README.md` | — | Single mention: "certified operators" and BanzAI description. No federation behavior. |
| `BANZA_REFERENCE.md §10` | 30 | Sparse. Design-phase note, 5 requirements, 3-row roadmap. |
| `BANZA_ARCHITECTURE.md §Federação` | 3 | One sentence + pointer to BANZA_REFERENCE.md |
| `BANZA_CERTIFICATION.md` | — | Certification levels mention "federation_ready" at L4 but do not explain what federation is. |
| `BANZA_GOVERNANCE.md` | — | No federation content. |

---

## 2. Gaps Identified in §10 (Before Rewrite)

### 2.1 Missing Explanations

| Gap | Impact |
|-----|--------|
| No explanation of WHY federation exists | A regulator or investor cannot understand the problem being solved |
| No before/after comparison | No mental model of the change federation makes |
| No example transaction | Abstract description only; nothing is concrete |
| No trust model explanation | ADR-026 specifies the trust architecture but BANZA_REFERENCE.md never mentions it |
| No explanation of obligations | The concept of an inter-operator financial obligation is never introduced |
| No explanation of netting | How obligations eventually settle is missing entirely |
| No description of BanzAI's federation role | The document does not state what BanzAI does (or does NOT do) in federation |
| No network effect explanation | Why the network becomes more valuable as operators join is not stated |

### 2.2 Missing Diagrams

| Missing Diagram | Purpose |
|-----------------|---------|
| Before federation: isolated operator islands | Establish the problem |
| After federation: connected operator network | Show the solution |
| Cross-operator payment flow | Show how a payment moves from Customer A to Merchant B |
| Trust chain | Show the BANZA → certificate → operator trust model |
| Authority model | Show BANZA / BanzAI / Operators hierarchy |
| Obligation and netting cycle | Show how money settles between operators |

### 2.3 Terminology Inconsistencies Found

| Location | Issue |
|----------|-------|
| `BANZA_REFERENCE.md §9` | L3 = "Federation Operator" — but per FEDERATION_CERTIFICATION_PATH.md, L3 should be "Settlement Operator" and L4 should be "Federation Operator" (pending ADR-028). |
| `BANZA_REFERENCE.md §10` | "Conta de liquidação partilhada com BANZA" (shared BANZA settlement account) — this was the old model. ADR-026 defines bilateral netting between operators, not shared accounts with BANZA. |
| `BANZA_REFERENCE.md §10` | Contains the reference operator's commercial name ("the reference operator") — violates identity-guard principle that operator names should not appear in protocol specifications. |
| `BANZA_CERTIFICATION.md` | L4 description says "federation_ready" capability — but per the conformance design, federation participation requires the full trust model, not just a capability flag. |

### 2.4 Audience Mismatch

The existing §10 was written for someone who already knows what federation means in the context of payment protocols. It reads as a technical note for engineers.

A regulator, investor, bank, merchant, or non-technical executive reading §10 would not be able to answer:
- Why does federation exist?
- How does it work?
- How do operators trust each other?
- What happens to the money?
- What does BanzAI do?
- Why does the network become more valuable over time?

### 2.5 Outdated Status

The section stated "A federação encontra-se na fase de desenho" (federation is in the design phase). As of 2026-05-31, the specification is complete:

| Artifact | Status |
|----------|--------|
| ADR-026 (Trust Model) | ✓ Approved |
| Federation Contracts (5 contracts) | ✓ Designed |
| Federation Invariants (18 invariants) | ✓ Defined |
| Federation Protocol Flow (10 phases) | ✓ Specified |
| Federation Conformance Model (79 tests) | ✓ Designed |

The section should accurately reflect the completion of the specification phase.

---

## 3. What Was Correct Before Rewrite

| Element | Assessment |
|---------|------------|
| §3 mention: "Operadores certificados podem encaminhar pagamentos entre si sem acordos bilaterais" | Correct and accurate; retained |
| General framing: protocol not product | Correct |
| Roadmap directional targets (H1 2027, H2 2027, 2028) | Directionally correct; updated to reflect specification completion |
| Federation as L3+ capability | Directionally correct; pending ADR-028 for precise level revision |

---

## 4. Integration Decision

**All federation content in §10 was replaced**, not extended. The existing 30-line section contained too much inaccurate or outdated content to patch. The new §10 was written from the protocol artifacts (ADR-026, contracts, protocol flow) as the authoritative source.

The new §10:
- Is written for a non-technical primary audience
- Contains diagrams using ASCII suitable for future visual production
- Provides a concrete worked example
- States the authority model explicitly
- States BanzAI's role and its explicit limits
- Is accurate to the complete specification
- Is ready for website adaptation

---

## 5. Website Readiness Assessment

### Sections Ready for Direct Publication

| Section | Readiness | Notes |
|---------|-----------|-------|
| "Por que a Federação Existe" | ✓ Ready | Narrative explanation usable verbatim |
| "Antes da Federação / Com Federação" | ✓ Ready with visual upgrade | ASCII diagrams need production visual design |
| "Exemplo Prático" | ✓ Ready | Concrete scenario is clear and accurate |
| "O Papel do BanzAI" | ✓ Ready | Authority model is explicitly stated |
| "Por que a Federação Importa" | ✓ Ready | Network effect explanation usable for investor/regulator audiences |

### Sections Requiring Simplification for Website

| Section | Issue | Recommendation |
|---------|-------|----------------|
| "Como Funciona a Federação" | The 5-step protocol contains some technical detail (certificates, BRL) | Create a "technical" and a "simplified" variant; publish simplified on marketing site |
| "Compensação (Netting)" | The mathematics of netting may be too detailed for general audiences | Pull the core concept into a callout box; detail in a separate technical annex |

### Sections Requiring Visual Production Before Publication

| Section | Needed Visual |
|---------|---------------|
| Before/After federation | Production diagram: two isolated networks → one connected network |
| Trust chain | Production diagram: BANZA certificate chain |
| Cross-operator payment flow | Animated or static step-by-step graphic |
| Obligation and netting cycle | Timeline/table visual |

### Sections Requiring No Changes

| Section | Assessment |
|---------|------------|
| "Estado Actual e Roadmap" | Accurate as of 2026-05-31; update only when milestones change |

---

## 6. Recommendations for Future Website Page: "How Federation Works"

A dedicated website page at `banza.network/federation` could be structured as:

```
Hero: "Pay anyone, on any certified operator."

Section 1: The Problem (2 paragraphs + before diagram)
Section 2: The Solution (2 paragraphs + after diagram)
Section 3: How It Works (5-step visual flow)
Section 4: Example Transaction (Customer A → Merchant B interactive graphic)
Section 5: Trust (1 paragraph + certificate chain diagram)
Section 6: For Operators (certification path, network effect)
Section 7: For Regulators (audit trail, BanzAI transparency)
Section 8: For Merchants (any customer can pay you, regardless of operator)
Section 9: FAQ
```

Primary call-to-action: "Become a certified operator" → certification documentation.

---

## 7. Files Changed

| File | Change |
|------|--------|
| `BANZA_REFERENCE.md §10` | **Complete rewrite** — replaced 30-line placeholder with full federation section |
| `docs/reference/FEDERATION_REFERENCE_REVIEW.md` | **Created** — this document |
| `docs/reference/FEDERATION_WEBSITE_PREPARATION.md` | **Created** — website adaptation plan |
