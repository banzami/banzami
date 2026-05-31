# BANZA Federation — Website Preparation

**Document ID:** BANZA-FEDERATION-REFERENCE-INTEGRATION-001  
**Date:** 2026-05-31  
**Status:** Canonical — adaptation guide for the future federation public website page.  
**Source:** `BANZA_REFERENCE.md §10` (post-rewrite)

---

## Objective

Map the BANZA_REFERENCE.md §10 content to a future public website page at `banza.network/federation` (or equivalent). Identify what can be published verbatim, what needs simplification, and what needs visual production.

---

## Proposed Page Structure: "How Federation Works"

```
banza.network/federation

[Hero]
  Headline: "Pay anyone. On any certified operator."
  Subheadline: "Federation connects every certified BANZA operator into one network."
  CTA: "Become a certified operator →"

[Section 1] The Problem
[Section 2] The Solution
[Section 3] How It Works (5 steps)
[Section 4] Example Transaction
[Section 5] Trust and Security
[Section 6] For Whom
  → Merchants
  → Customers
  → Operators
  → Regulators
  → Investors
[Section 7] Current Status
[Footer CTA] Certification documentation
```

---

## Section-by-Section Assessment

### Hero

**Source:** BANZA_REFERENCE.md §10 opening paragraph

> "A federação é o mecanismo pelo qual operadores certificados BANZA formam uma rede — permitindo que um cliente com carteira num operador pague um comerciante com carteira noutro operador, sem acordos bilaterais, sem intermediários adicionais, e com as mesmas garantias financeiras de qualquer pagamento intra-operador."

**Website adaptation:**

```
English:
"Federation is the mechanism by which certified BANZA operators form a
network — allowing a customer with a wallet on one operator to pay a
merchant with a wallet on another, without bilateral agreements, without
additional intermediaries, and with the same financial guarantees as any
intra-operator payment."
```

**Readiness:** ✓ Ready for adaptation. One paragraph, no technical jargon.

---

### Section 1 — The Problem

**Source:** "Por que a Federação Existe" + "Antes da Federação" from §10

**Website adaptation (simplified):**

```
Without federation, each operator is an island.

A customer on Operator A can only pay merchants on Operator A.
A merchant on Operator B can only receive from Operator B customers.

Two certified networks. No connection between them.
```

**Visual required:**

```
Production diagram:
  [Operator A circle]  [Operator B circle]
  Each with customers/merchants inside.
  No connection between circles.
  Label: "Without federation"
```

**Readiness:** ✓ Ready for adaptation. Requires production diagram to replace ASCII art.

---

### Section 2 — The Solution

**Source:** "Com Federação" from §10

**Website adaptation:**

```
With federation, every certified operator joins one network.

A customer on any operator can pay a merchant on any operator.
Every new certified operator makes all others more useful.
```

**Visual required:**

```
Production diagram:
  [Operator A] ←— BANZA protocol —→ [Operator B]
  [Operator C] ←——————————————————→ [Operator D]
  Label: "With federation — one network"
  Animation: operators lighting up as they join
```

**Readiness:** ✓ Ready for adaptation. Requires production diagram.

---

### Section 3 — How It Works

**Source:** "Como Funciona a Federação" from §10 (5 steps)

**Simplified website version (remove technical detail):**

```
Step 1 — Trust
  Before routing a payment, Operator A checks that Operator B is
  a legitimate BANZA member. This check takes milliseconds.
  No phone call to BANZA required.

Step 2 — Routing
  Operator A sends a routing request to Operator B:
  "Route 2,000 AOA to merchant B."

Step 3 — Acceptance and Execution
  Operator B accepts — and immediately credits the merchant.
  Acceptance is execution. The merchant receives funds the moment
  Operator A gets the confirmation.

Step 4 — Obligation
  Operator A debits the customer and records a formal obligation:
  "Operator A owes Operator B 2,000 AOA."
  This obligation is cryptographically signed. Non-repudiable.

Step 5 — Settlement
  At the end of each day (or agreed cycle), all obligations between
  operators net out. One bank transfer settles the full day's payments.
  Not one transfer per payment — one per cycle.
```

**Readiness:** ✓ Content is ready. The simplified version above removes ed25519, BRL, and routing_request_id details for general audiences. Technical detail is preserved in BANZA_REFERENCE.md §10.

**Visual required:** Step-by-step flow diagram (5 panels). Animation optional.

---

### Section 4 — Example Transaction

**Source:** "Exemplo Prático" from §10

**Website adaptation (English):**

```
Ana has a wallet on Operator A.
Bento is a merchant on Operator B.
Ana wants to pay Bento 2,000 AOA.

1. Ana initiates payment in the Operator A app.
   Operator A identifies that Bento is on Operator B.

2. Operator A verifies Operator B's BANZA certificate.
   Operator B is a legitimate certified member. Check passes.

3. Operator A sends a signed routing request to Operator B.

4. Operator B verifies Operator A (trust is always mutual).
   Operator B finds Bento's wallet. Credits 2,000 AOA. Responds: "Accepted."

5. Operator A debits Ana's wallet. Records the obligation.

6. Bento receives a payment notification. His balance increased.
   Ana receives confirmation. Her balance decreased.

7. At the end of the day:
   Operators net their obligations. One bank transfer settles everything.
```

**Readiness:** ✓ Ready for direct publication. Clear, concrete, accurate to the protocol.

---

### Section 5 — Trust and Security

**Source:** "Cadeia de Confiança" and "Como Funciona — 1. Confiança" from §10

**Website version (simplified):**

```
How does Operator A know Operator B is legitimate?

BANZA issues a signed certificate to every certified operator.
Any operator can verify any certificate — without calling BANZA in real time.
If an operator loses certification, BANZA's revocation list ensures
all other operators stop routing to it within 6 hours.

Trust is always mutual: Operator B also verifies Operator A before
accepting any routing request.
```

**Visual required:**

```
Chain graphic:
  [BANZA] → signs certificate → [Operator B certificate]
  [Operator A] verifies certificate → [BANZA public key]
  Label: "No bilateral agreement needed. BANZA is the trust anchor."
```

**Readiness:** ✓ Ready for adaptation. Technical terms (ed25519, BRL) abstracted away.

---

### Section 6 — For Whom

**Source:** "Por que a Federação Importa" from §10

**All four audience sections are ready for direct adaptation:**

#### For merchants

```
A merchant certified with any operator can receive payments from
customers on any other operator. One wallet. Accessible to all.
```

#### For customers

```
Pay any merchant, on any operator, from your app.
The fragmentation of isolated networks ends.
```

#### For operators

```
Every new certified operator makes all others more valuable.
A network of 100,000 users joining a network of 500,000 users
doesn't add 600,000 total — it multiplies each network's reach.
```

#### For regulators

```
Every cross-operator payment is auditable by design.
A single trace identifier exists in both operators for every
cross-operator payment — in all artifacts, on both sides.
Any payment can be reconstructed without operator cooperation.
```

#### For investors

```
Federation transforms BANZA from a set of isolated operators
into a unified payment network. Network value doesn't belong
to any operator — it belongs to the protocol. Every operator
that joins increases the value of all others.
```

**Readiness:** ✓ All sections ready for direct publication.

---

### Section 7 — Current Status

**Source:** "Estado da Especificação e Roadmap" from §10

**Website version (simplified, stripped of implementation detail):**

```
Where we are:

✓ Architecture defined (trust model, certificates, revocation)
✓ Protocol contracts specified (5 federation contracts)
✓ Conformance suite designed (79 tests)
✓ Full protocol flow documented (10 phases, discovery to settlement)

What's next:

→ H1 2027: Runner implementation and kernel implementation
→ H2 2027: Two operators in a controlled federation pilot
→ 2028: Open federation — any certified operator may federate
```

**Readiness:** ✓ Ready for direct publication. Update as milestones are reached.

---

## Visual Production Priority

Ranked by impact on audience comprehension:

| Priority | Visual | Audience Impact |
|----------|--------|-----------------|
| 1 | Before/After: isolated → connected | Everyone — establishes the core value proposition in 2 seconds |
| 2 | Example transaction flow (5 steps animated or static) | Everyone — makes the abstract concrete |
| 3 | Trust chain | Banks, regulators, sophisticated operators |
| 4 | Netting cycle / obligation table | Investors, regulators, banks |
| 5 | Authority model (BANZA / BanzAI / Operators) | Operators, developers, investors |

---

## Audience-Specific Page Variants

The full BANZA_REFERENCE.md §10 is the canonical reference. For the website, consider audience-specific landing paths:

| Audience | Primary Message | Call to Action |
|----------|----------------|----------------|
| Merchants | "Any customer can pay you" | List your merchant wallet |
| Operators | "Your network joins every network" | Certification path |
| Regulators | "Every payment is auditable by design" | Protocol specification |
| Investors | "Network value compounds with each operator" | Whitepaper / BANZA_REFERENCE.md |
| Developers | "One protocol. Any operator. Same guarantees." | SDK documentation |

---

## What Is NOT Ready for General Publication

| Item | Issue | What's Needed |
|------|-------|---------------|
| The technical trust protocol (9 steps) | Too detailed for general audiences | Present as: "9 cryptographic checks happen in milliseconds" |
| The netting mathematics | Numbers are clear but may be intimidating | Simplify to: "Multiple payments. One transfer. Daily." |
| Obligation state machine | Engineering detail | Not needed on website; keep in BANZA_REFERENCE.md |
| Conformance test IDs | Only relevant for operator certification | Keep in conformance documentation |
| Invariant IDs (INV-FED-*) | Engineering detail | Keep in technical reference only |

---

## Final Assessment: Publication Readiness

> Could a non-technical executive understand — from BANZA_REFERENCE.md §10 alone, without reading ADRs, contracts, or conformance suites — why federation exists, how it works, why operators trust each other, why BANZA is needed, what BanzAI does, and why the network becomes more valuable as operators join?

**Yes.**

Each question is now explicitly answered:

| Question | Answered In |
|----------|-------------|
| Why federation exists | "Por que a Federação Existe" |
| How it works | "Como Funciona a Federação" (5 steps) |
| Why operators trust each other | "Cadeia de Confiança" |
| Why BANZA is needed | "Modelo de Autoridade" + "Cadeia de Confiança" |
| What BanzAI does | "O Papel do BanzAI na Federação" (explicit positive and negative lists) |
| Why the network grows in value | "Por que a Federação Importa — Para Operadores" (network effect) |

The §10 rewrite achieves the stated success criterion: **Federation is understandable by humans before it is executable by machines.**
