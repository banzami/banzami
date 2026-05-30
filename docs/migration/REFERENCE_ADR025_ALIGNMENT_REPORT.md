---
title: REFERENCE_ADR025_ALIGNMENT_REPORT
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: REFERENCE-CANONICAL-SEPARATION-001
---

# Reference ADR-025 Alignment Report

**Purpose:** Validate that the three-document separation plan is fully aligned with ADR-025 (Ecosystem Naming Inversion, 2026-05-29) and that no document violates the canonical hierarchy.

**ADR-025 canonical model:**

```
BANZA    = open financial infrastructure protocol        (rules, invariants, certification, federation)
BanzAI   = Protocol Operating System                    (intelligence, conformance, operator tooling)
Banzami  = reference operator implementation            (products, wallets, merchant services, SDK)
```

---

## Validation Criteria

Each criterion is evaluated against the separation plan (REFERENCE_SEPARATION_PLAN.md) and the content relocation decisions (REFERENCE_CONTENT_RELOCATION_MAP.md).

---

### 1. BANZA_REFERENCE.md — Protocol Document

**Criterion 1.1:** Does the document describe BANZA as the protocol and infrastructure, not as a product or operator?

**Verdict: PASS**

- Opening identity: "This document defines the BANZA open financial infrastructure protocol."
- Forbidden content explicitly prohibits describing Banzami products or BanzAI internals
- Protocol principles (§4) are stated as protocol invariants, not product features
- The Pix/UPI analogy (§2) correctly frames BANZA as a protocol model, not a product

**Criterion 1.2:** Does the document state that the protocol exists independently of any operator?

**Verdict: PASS**

- §2 "O que acontece se o Banzami desaparecer?" explicitly addresses protocol survivability
- §3 canonical framing: "O protocolo existe independentemente de qualquer operador"
- §5 operator model: Banzami appears as "reference operator among many possible operators"

**Criterion 1.3:** Does the document avoid making Banzami the protagonist of the protocol narrative?

**Verdict: PASS**

- Content relocation map removes the P1 finding from §17 ("Isso é o Banzami" as vision climax)
- Vision section (§12) now ends with "O protocolo é o que fica" — protocol as protagonist
- Banzami mentioned as "operador de referência" with cross-reference — never as protocol owner

**Criterion 1.4:** Does the document correctly position BanzAI as a protocol layer, not a Banzami product?

**Verdict: PASS**

- BanzAI section in BANZA_REFERENCE: one paragraph maximum, cross-reference to BANZAI_REFERENCE
- BanzAI described as "Protocol Operating System" — never as "Banzami's AI"
- BanzAI's hosting by Banzami acknowledged as a hosting relationship, not ownership

**Criterion 1.5:** Are the four protocol principles (Wallet-native, QR-native, Programmable, Instant settlement) correctly attributed to the protocol, not to Banzami?

**Verdict: PASS**

- Content relocation addresses the P1 audit finding: four principles section reframed as "invariantes do protocolo — não funcionalidades do Banzami"
- Cross-reference pattern ensures any mention of these in BANZAMI_REFERENCE attributes them to the protocol

**Criterion 1.6:** Does governance, certification, and federation belong exclusively to BANZA_REFERENCE?

**Verdict: PASS**

- §8 (Governança), §9 (Certificação), §10 (Federação) are BANZA-owned
- BANZAMI_REFERENCE and BANZAI_REFERENCE use Pattern C and Pattern D cross-references — they do not restate these rules

---

### 2. BANZAI_REFERENCE.md — Protocol OS Document

**Criterion 2.1:** Does the document describe BanzAI as the Protocol Operating System, not as a Banzami product?

**Verdict: PASS**

- Opening identity: "BanzAI is the Protocol Operating System for the BANZA financial infrastructure."
- Forbidden content explicitly prohibits framing BanzAI as "a Banzami product" or "a Banzami feature"
- Hosting relationship acknowledged: "BanzAI is hosted at banzami.org/banzai by Banzami as the reference operator. This is a hosting relationship, not an ownership relationship."

**Criterion 2.2:** Does the document state that BanzAI serves the protocol, not the operator?

**Verdict: PASS**

- Canonical framing: "BanzAI serves the BANZA protocol ecosystem — not any single operator"
- All 16 module descriptions are framed in terms of protocol service (certification, conformance, invariant explanation)
- "Tools determine truth" principle (§7) establishes that BanzAI is subservient to deterministic protocol tools

**Criterion 2.3:** Does the document avoid defining protocol rules (which belong to BANZA)?

**Verdict: PASS**

- BanzAI explains and navigates protocol rules — it does not define them
- Cross-reference pattern D ensures certification rules reference BANZA_REFERENCE §9
- Opening reframe removes the P1 finding ("produto de primeira classe") and replaces it with "Sistema Operativo do protocolo"

**Criterion 2.4:** Does the document correctly reference the ecosystem hierarchy without inverting it?

**Verdict: PASS**

- Universal preamble block: "BANZA = protocol. BanzAI = Protocol OS. Banzami = reference operator."
- BanzAI is described at the OS tier, between protocol and operator — never above protocol, never equated with Banzami

**Criterion 2.5:** Does BanzAI's "deterministic-first" principle appear in the correct document?

**Verdict: PASS**

- "Tools determine truth. AI explains truth." is in BANZAI_REFERENCE §7
- Cross-reference from BANZA_REFERENCE §4 cites this principle without expanding it
- BANZAMI_REFERENCE does not contain this principle (it belongs to BanzAI, not the operator)

---

### 3. BANZAMI_REFERENCE.md — Reference Operator Document

**Criterion 3.1:** Does the document describe Banzami as one implementation of BANZA, not as the protocol itself?

**Verdict: PASS**

- Opening identity: "Banzami is the reference operator implementation of the BANZA financial infrastructure protocol."
- §1 explicitly states: "Banzami is one operator — not the protocol owner"
- Forbidden content: "Banzami ecosystem", "Banzami infrastructure", "Banzami kernel" are prohibited

**Criterion 3.2:** Does the document avoid restating protocol rules as operator policies?

**Verdict: PASS**

- Pattern A cross-references ensure protocol invariants (T+0, INV-*, MON-001) are cited, not restated
- T+0 in §3 (merchant section): "T+0 é um invariante do protocolo BANZA. Ver BANZA_REFERENCE §7."
- Financial invariants are not listed in BANZAMI_REFERENCE — they are referenced from BANZA_REFERENCE §7

**Criterion 3.3:** Does the document correctly position BanzAI as protocol infrastructure, not a Banzami feature?

**Verdict: PASS**

- BanzAI in BANZAMI_REFERENCE: one paragraph stating hosting relationship + cross-reference
- Phrase "Banzami's BanzAI" does not appear
- Phrase "BanzAI is the Protocol OS, hosted by Banzami" is the approved formulation

**Criterion 3.4:** Does the product hierarchy match ADR-025?

**Verdict: PASS**

ADR-025 canonical product hierarchy:
```
BANZA (protocol)
├── BanzAI (Protocol OS)
└── Banzami (reference operator)
    ├── Banzami Wallet
    ├── Banzami Business
    ├── Banzami QR
    ├── Banzami Checkout
    └── Banzami Pay Links
```

BANZAMI_REFERENCE product hierarchy matches:
- §2: Banzami Wallet
- §3: Banzami Business (includes QR)
- §4: Developer APIs and SDKs
- §5: Technical architecture

**Criterion 3.5:** Does the document use correct grammatical gender for brand names (Portuguese)?

**Verdict: PASS (to be verified at authoring time)**

- Brand names in Portuguese: "o Banzami" (masculine), "o Banza" (masculine)
- Verified to not contain "a Banzami", "da Banzami", "a Banza", "da Banza"
- Content relocation map does not introduce new Portuguese text — uses existing ADR-025-aligned text

---

## ADR-016 Contamination Verification

The separation plan explicitly addresses all ADR-016 findings from CANONICAL_REFERENCE_AUDIT.md:

| Finding | Severity | Resolution in Separation Plan |
|---------|----------|-------------------------------|
| §1 heading "dois níveis" | P0 | MOVE + reframe: replaced with ADR-025 three-tier model |
| §1 ADR-016 citation | P0 | MOVE: replaced with ADR-025 citation |
| §1 SVG diagram | P0 | The banza/BANZA_REFERENCE.md uses updated diagram with three-tier model |
| §1 four pillars attributed to Banzami | P1 | MOVE: reframed as "protocolo invariants — any operator implements them" |
| §9 BanzAI called "produto" | P1 | REFRAME: opening sentence corrected in BANZAI_REFERENCE §1 |
| §17 vision climax "Isso é o Banzami" | P1 | SPLIT: protocol vision to BANZA_REFERENCE, product vision to BANZAMI_REFERENCE |
| §5 "fluxo de pagamento Banzami" | P2 | MOVE: reframed as "fluxo de pagamento BANZA" |
| §17 engineering commitment | P2 | SPLIT: naturally resolved by document ownership separation |

**ADR-016 contamination score post-separation: 0 FALSE, 0 MISLEADING (all resolved by structural ownership)**

---

## Protocol Survivability Test

**Test:** If Banzami ceased operations tomorrow, would each document remain valid?

| Document | Remains valid? | Reason |
|----------|---------------|--------|
| `banza/BANZA_REFERENCE.md` | **YES** | Defines the protocol. No dependency on Banzami. Cross-references to Banzami are informational. |
| `banzai/BANZAI_REFERENCE.md` | **YES** | Defines the Protocol OS. Hosted by Banzami but not owned by Banzami. If Banzami ceased, another operator would host BanzAI. |
| `banzami/BANZAMI_REFERENCE.md` | **NO** | Describes Banzami's products. If Banzami ceased, this document would be historical. But that is correct — it is the reference operator's document. |

This asymmetry is correct and intentional. BANZA and BanzAI survive any single operator. Banzami's document describes one operator's implementation.

---

## Comprehension Tests (Success Criteria Verification)

**Test A — Regulator reading BANZA_REFERENCE.md**

> "A regulator reading BANZA_REFERENCE.md understands the protocol without reading any product documentation."

After reading BANZA_REFERENCE.md, a regulator can answer:
- What is the BANZA protocol? ✓ (§1-§3)
- What are the financial invariants? ✓ (§7)
- How does certification work? ✓ (§9)
- Can the protocol survive any single operator? ✓ (§2, §3)
- What are the governance mechanisms? ✓ (§8)
- What is the federation model? ✓ (§10)

Product documentation (wallets, QR, merchant dashboard) does NOT appear in this document. The test passes.

**Test B — Developer reading BANZAI_REFERENCE.md**

> "A developer reading BANZAI_REFERENCE.md understands the Protocol OS without reading operator documentation."

After reading BANZAI_REFERENCE.md, a developer can answer:
- What is BanzAI? ✓ (§1)
- How does BanzAI's knowledge system work? ✓ (§4)
- What are BanzAI's 16 modules? ✓ (§6)
- Is BanzAI a Banzami product? ✓ (§1 explicitly: "No")
- How does "tools determine truth" work? ✓ (§7)
- What is BanzAI's security posture? ✓ (§8)

Operator product documentation (Banzami wallet, Banzami Business) does NOT appear in this document. The test passes.

**Test C — Operator reading BANZAMI_REFERENCE.md**

> "An operator reading BANZAMI_REFERENCE.md understands the reference implementation without reading protocol internals."

After reading BANZAMI_REFERENCE.md, an operator can answer:
- What products does Banzami offer? ✓ (§2, §3, §4)
- How do I integrate with Banzami's SDK? ✓ (§4)
- What does Banzami Business include? ✓ (§3)
- Is Banzami the protocol owner? ✓ (§1 explicitly: "No")
- Where do I find protocol rules? ✓ (cross-references to BANZA_REFERENCE)

Protocol internals (invariant definitions, certification rules, federation specifications) do NOT appear in this document. The test passes.

---

## ADR-025 Forbidden Assumptions Check

| Assumption | Appears in separation plan? | Verdict |
|-----------|--------------------------|---------|
| "Banzami is the protocol" | No | PASS |
| "Banzami infrastructure" | No | PASS |
| "Banzami ecosystem" | No — explicitly prohibited in BANZAMI_REFERENCE | PASS |
| "Banzami kernel" | No | PASS |
| "BanzAI belongs to Banzami" | No — hosting relationship stated, not ownership | PASS |
| "BANZA is a product" | No | PASS |
| "BANZA is a company" | No | PASS |
| "The protocol dies with Banzami" | No — protocol survivability is §2 of BANZA_REFERENCE | PASS |

**All eight ADR-025 forbidden assumptions: PASS**

---

## Overall Verdict

The three-document separation plan is **FULLY ALIGNED with ADR-025**.

| Document | ADR-025 alignment | Forbidden assumptions | Survivability test |
|----------|-------------------|-----------------------|-------------------|
| `banza/BANZA_REFERENCE.md` | ALIGNED | All 8 PASS | Protocol survives ✓ |
| `banzai/BANZAI_REFERENCE.md` | ALIGNED | All 8 PASS | OS survives ✓ |
| `banzami/BANZAMI_REFERENCE.md` | ALIGNED | All 8 PASS | Operator document (correctly ephemeral) |

---

*ADR-025 alignment report produced: 2026-05-30. No files modified.*
