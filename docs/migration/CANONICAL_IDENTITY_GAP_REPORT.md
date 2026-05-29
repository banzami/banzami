---
title: CANONICAL_IDENTITY_GAP_REPORT — BANZA-CANONICAL-REFERENCE-REWRITE
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no modifications applied
---

# Canonical Identity Gap Report

**Purpose:** Consolidated view of every remaining gap between the current state of `BANZAMI_REFERENCE.md` + its diagrams and 100% ADR-025 conceptual consistency.

**Definition of "gap":** Any content where a visitor would form a mental model inconsistent with the ADR-025 canonical hierarchy:
- BANZA = protocol · infrastructure · ecosystem
- BanzAI = Protocol Operating System
- Banzami = Reference Operator / Payment Product

---

## GAP-001 — The Brand Architecture Diagram Shows the Wrong Root (P0)

**File:** `apps/docs/public/images/architecture/brand-architecture.svg`
**Rendered on:** `banzami.org/o-que-e-o-banza` (§1 — the first section page)
**Section:** §1 `### Arquitectura de dois níveis`

**The gap:**

The diagram root node reads: **BANZAMI (organização · protocolo · ecossistema)**

This states three things simultaneously:
1. BANZAMI is the organization → implies the protocol is owned by Banzami
2. BANZAMI is the protocol → direct inversion of ADR-025
3. BANZAMI is the ecosystem → direct inversion of ADR-025

A visitor reading this diagram concludes: "BANZAMI is the top-level entity. Everything lives inside it: the product called Banzami, and the AI called BanzAI."

The canonical conclusion must be: "BANZA is the protocol. BanzAI is the OS layer of the protocol. Banzami is the reference operator — one of possibly many operators."

**Mechanism:** This is a structural, architectural claim embedded in a visual hierarchy. It cannot be fixed by changing body copy. The SVG root node must change.

**Why it matters:** This is the single most-visited diagram. §1 is the entry point for any new visitor navigating the reference documentation. The first diagram they encounter contradicts 32 other correctly-aligned diagrams in the same document.

**Validation test:**
- Would the root node be BANZAMI if Banzami (the product) disappeared? NO — the protocol would still exist.
- Would the root node be BANZAMI if 100 operators existed? NO — none of them would own the ecosystem.
- Therefore: The root belongs to BANZA.

---

## GAP-002 — The Section Heading Encodes the Pre-ADR-025 Model (P0)

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** §1, line 48: `### Arquitectura de dois níveis`

**The gap:**

The heading "dois níveis" (two levels) encodes the ADR-016 two-tier model: organization → product + AI. The canonical model under ADR-025 has three tiers: protocol → OS / reference operator. By calling it "dois níveis", the section:

1. Implicitly references ADR-016 (two-tier model)
2. Implicitly excludes BANZA as a distinct level (because in a two-tier model, BANZA is the root that contains Banzami + BanzAI, not a separate tier from them)
3. Locks the mental model to the pre-ADR-025 framing

**Correct heading:** "Arquitectura de três níveis" (or "Arquitectura Canónica do Protocolo") — reflecting that BANZA, BanzAI, and Banzami are three distinct tiers.

---

## GAP-003 — The Architecture Reference Cites ADR-016, Not ADR-025 (P0)

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** §1, line 52: `Esta arquitectura de marca está definida no ADR-016.`

**The gap:**

ADR-016 defined the two-tier BANZAMI/Banzami model. ADR-025 supersedes ADR-016 for the brand hierarchy. A reader following this reference to ADR-016 will read the pre-ADR-025 model and potentially use it to understand the current architecture. The reference document should cite ADR-025.

**Note:** This is the smallest of the three P0 findings — it's a reference fix, not a conceptual rewrite.

---

## GAP-004 — The Four Pillars Are Attributed to Banzami Instead of BANZA (P1)

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** §1, line 54: `### Os quatro pilares do Banzami`

**The gap:**

The four pillars listed are:
- Programmable — any app integrates payments via SDK
- Wallet-native — payments are wallet transfers
- QR-native — primary payment surface is QR
- Instant settlement — money moves at confirmation

**Validation test:**
- Would "Programmable" still be true if Banzami disappeared and a different operator built on BANZA? YES.
- Would "Wallet-native" be a property of BANZA if 100 operators existed? YES — the BANZA protocol is wallet-native at the protocol level.
- Would "Instant settlement" still happen if Banzami was replaced by another operator? YES — it is a BANZA protocol invariant.

All four pillars are BANZA protocol properties. They apply to any certified operator. Attributing them to Banzami implies they are Banzami product features, not protocol properties. A new operator reading this might believe these are Banzami-specific features they cannot offer.

**Correct framing:** "Os quatro princípios do protocolo" or "Os quatro pilares do protocolo Banza" — with content updated to explicitly state that any certified operator implements these properties.

---

## GAP-005 — BanzAI Is Called a "Produto" (P1)

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** §9, line 632: `O BanzAI é um produto de primeira classe do ecossistema Banza`

**The gap:**

The word "produto" (product) places BanzAI in the same conceptual category as Banzami — a payment product. The canonical model explicitly distinguishes BanzAI as a tier of its own (Protocol OS), not a product tier. Banzami is in the product tier. BanzAI is in the OS tier.

This is particularly damaging in §9 because the section then spends 900+ lines arguing that BanzAI is NOT a chatbot/product but a Protocol Operating System. The opening sentence undercuts the argument.

**Validation test:**
- Would BanzAI exist if Banzami disappeared? YES — BanzAI explains BANZA protocol, not Banzami.
- Is BanzAI a payment product? NO — it is the cognitive interface of the protocol.
- Who uses BanzAI? Operators, developers, auditors, regulators — not just Banzami users.

**Correct framing:** "O BanzAI é o Sistema Operativo nativo do protocolo Banza" — which is the exact framing used in 5 other correct occurrences on the same site (`/banzamia`, `/sobre-banzamia`, `HeroBanzamIAWidget`, `HomeBanzamIAEntry`, hero subheadline).

**Note:** This gap creates an internal inconsistency: the §9 opener calls BanzAI a "produto" while `/banzamia` and `/sobre-banzamia` correctly call it the "Sistema Operativo". A visitor who reads both will notice the contradiction.

---

## GAP-006 — The Monetary Flow Is Attributed to Banzami Instead of BANZA (P2)

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** §5, line 294: `"Todo o fluxo de pagamento Banzami produz três montantes monetários com semântica exacta"`

**The gap:**

The gross/net/fee model (INV-STL-001) is a BANZA protocol invariant that ALL certified operators must implement. It is not a Banzami-specific flow. "Fluxo de pagamento Banzami" implies this is how Banzami handles payments, rather than how the BANZA protocol defines payment flows.

**Correct framing:** "Todo o fluxo de pagamento Banza produz três montantes monetários com semântica exacta"

This is a P2 (legacy wording) rather than P1 because the section heading is correct ("§5 — Representação Monetária" refers to the Banza protocol) and the surrounding text consistently frames these as protocol requirements.

---

## GAP-007 — The Vision Climax Makes Banzami the Protagonist (P1)

**File:** `docs/BANZAMI_REFERENCE.md`
**Location:** §17, line 1877: `**Isso é o Banzami — construído pelo Banza.**`

**The gap:**

§17 is the vision declaration — the last section a reader encounters. Its purpose is to leave the visitor with the definitive identity of BANZA. The section opens correctly with BANZA as the infrastructure protagonist and correctly uses Banzami for the product experience.

However, the section climax (the boldest sentence in §17) is: "**Isso é o Banzami — construído pelo Banza.**"

This sentence:
1. Makes Banzami the subject ("Isso é o Banzami")
2. Relegates BANZA to an instrumental role ("construído pelo Banza")
3. Leaves the visitor with Banzami as the final protagonist

The canonical model requires BANZA to be the infrastructure protagonist. A visitor who remembers one thing from §17 should remember that BANZA is the infrastructure, not that Banzami is the vision.

**Correct framing alternatives:**
- "Isso é o que o Banza torna possível."
- "Isso é a infraestrutura Banza em acção."
- "Isso é o protocolo Banza — a infraestrutura que Angola merecia."

The sentences immediately preceding and following line 1877 are correct and describe Banzami as the product delivering the experience. The issue is that line 1877 is the **bold climax** — the sentence a reader's eye goes to first.

---

## Gap Interaction Map

Some gaps reinforce each other:

```
GAP-001 (brand-architecture.svg: BANZAMI at root)
    ↓ sets wrong mental model before any text is read
GAP-002 (heading: "Arquitectura de dois níveis")
    ↓ reinforces two-tier model in text
GAP-003 (cites ADR-016)
    ↓ sends reader to the pre-ADR-025 source document
        = Three P0 gaps in §1 compound to create a fully pre-ADR-025 §1 experience

GAP-005 (BanzAI called "produto")
    ↓ contradicts correct framing on 5 other site pages
        = Creates inconsistency between §9 opener and /banzamia, /sobre-banzamia

GAP-004 (four pillars attributed to Banzami)
    ↓ visitor concludes: "Banzami is Programmable, QR-native, etc."
        = Any new operator building on BANZA may believe these properties are Banzami-exclusive
```

---

## Completeness Assessment

| Domain | Gaps found | % Aligned |
|---|---|---|
| Reference document (17 sections, line-by-line) | 7 gaps (3×P0, 3×P1, 1×P2) | ~95% |
| Diagrams (33 SVGs) | 1 gap (P0) | 97% |
| Navigation / metadata (previous sessions) | 0 gaps remaining | 100% |
| Overall | 8 gaps | ~96% |

**To reach 100% ADR-025 conceptual consistency:**
- Fix 3 P0 items (brand-architecture.svg, §1 heading, §1 ADR reference)
- Fix 3 P1 items (four pillars attribution, BanzAI opener, §17 climax)
- Fix 1 P2 item (§5 monetary flow wording)

Total: 7 items in `BANZAMI_REFERENCE.md` + 1 SVG rebuild.

---

*Report completed: 2026-05-30. No modifications applied.*
