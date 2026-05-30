---
name: cross-reference-strategy
description: Canonical cross-reference patterns for the three-layer ecosystem documentation — ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001
metadata:
  type: project
---

# Cross-Reference Strategy

**Mission:** ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001  
**Date:** 2026-05-30  
**Status:** Authoritative

---

## Principle

A document may **reference** content from another layer.  
A document must **never duplicate** content from another layer.

Cross-references are the connective tissue that preserves the single source of truth.

---

## The Three Reference Directions

### Direction 1 — BANZAMI references BANZA

Operator documents may reference protocol rules but must never restate them.

**Permitted:**
```markdown
Settlement happens at T+0 — the ledger is updated at the moment of authorization.
This implements the protocol invariant — see [BANZA_REFERENCE.md §7](../banza/BANZA_REFERENCE.md#7-invariantes-financeiros).
```

**Forbidden:**
```markdown
Settlement happens at T+0. The ledger entry must be created immediately.
Debit and credit must be equal. No negative balances are permitted.
```
*This restates INV-LEDGER-001 and INV-STL-002 — creating a second source of truth.*

### Direction 2 — BANZAI references BANZA

Protocol OS documents may reference protocol rules to explain them but must never redefine them.

**Permitted:**
```markdown
BanzAI can explain the zero-sum invariant — see [BANZA_REFERENCE.md §7](../banza/BANZA_REFERENCE.md).
The explanation is grounded in the invariant definition; BanzAI does not define the invariant.
```

**Forbidden:**
```markdown
The zero-sum invariant requires that every debit is matched by an equal credit.
```
*This restates the invariant in a BanzAI document — the invariant belongs to BANZA_REFERENCE.md.*

### Direction 3 — BANZA references BANZAMI

Protocol documents may reference Banzami as the reference operator for implementation examples only.

**Permitted:**
```markdown
The reference implementation is Banzami — see [BANZAMI_REFERENCE.md](../banzami/BANZAMI_REFERENCE.md).
```

**Forbidden:**
```markdown
The reference implementation uses Rust for the financial core, Go for the API gateway,
and Next.js for the merchant dashboard.
```
*Technology stack decisions belong to BANZAMI_ARCHITECTURE.md.*

---

## Canonical Cross-Reference Formats

### Pattern A — Protocol invariant cited in operator document

Use when an operator document must acknowledge a protocol constraint:

```markdown
See [BANZA_REFERENCE.md §7 — Financial Invariants](../banza/BANZA_REFERENCE.md)
for the authoritative definition of this invariant.
```

### Pattern B — Operator product cited in protocol document

Use when a protocol document illustrates implementation with the reference operator:

```markdown
The Banzami reference operator implements this as [product X] — 
see [BANZAMI_REFERENCE.md §N](../banzami/BANZAMI_REFERENCE.md).
```

### Pattern C — Protocol OS capability cited in any document

Use when referencing BanzAI tooling or capabilities:

```markdown
BanzAI's Certification Copilot guides operators through this process — 
see [BANZAI_CAPABILITIES.md](../banzai/BANZAI_CAPABILITIES.md).
```

### Pattern D — Certification requirement cited in operator document

Use when an operator document must reference certification requirements:

```markdown
Certification at this level requires passing the conformance suite — 
see [BANZA_CERTIFICATION.md](../banza/BANZA_CERTIFICATION.md).
```

### Pattern E — Architecture detail cited from another layer

Use when architecture in one layer is referenced from another:

```markdown
The technical architecture of the reference implementation is defined in 
[BANZAMI_ARCHITECTURE.md](../banzami/BANZAMI_ARCHITECTURE.md).
```

### Pattern F — Roadmap item cross-referenced

Use when one layer's roadmap enables or affects another layer:

```markdown
When the Conformance Suite v1 ships (see [BANZA_ROADMAP.md](BANZA_ROADMAP.md)),
BanzAI's Certification Copilot will integrate directly — see [BANZAI_ROADMAP.md](../banzai/BANZAI_ROADMAP.md).
```

---

## Anti-Patterns

### Anti-Pattern 1 — Restating invariants

```markdown
# BAD — in BANZAMI_ARCHITECTURE.md
The ledger enforces zero-sum accounting: every debit is matched by an equal credit.
No wallet balance may go negative.

# GOOD — in BANZAMI_ARCHITECTURE.md
The Rust core implements the BANZA protocol financial invariants.
See [BANZA_REFERENCE.md §7](../banza/BANZA_REFERENCE.md) for the authoritative definitions.
```

### Anti-Pattern 2 — Duplicating certification levels

```markdown
# BAD — in BANZAMI_PRODUCTS.md
To accept payments, Banzami must achieve Level 1 certification, which requires:
- wallet.consumer capability
- qr.static capability
- INV-LEDGER-001 compliance
...

# GOOD — in BANZAMI_PRODUCTS.md
Banzami operates at Level 2 (Settlement Operator) certification.
See [BANZA_CERTIFICATION.md](../banza/BANZA_CERTIFICATION.md) for all certification requirements.
```

### Anti-Pattern 3 — Redefining BanzAI capabilities in BANZAMI docs

```markdown
# BAD — in BANZAMI_PRODUCTS.md
BanzAI is available at banzami.org/banzai. It uses Qdrant for vector search,
Hono for the API layer, and LangGraph for tool orchestration.

# GOOD — in BANZAMI_PRODUCTS.md
The BanzAI Protocol OS is hosted at banzami.org/banzai.
See [BANZAI_REFERENCE.md](../banzai/BANZAI_REFERENCE.md) for full capability documentation.
```

### Anti-Pattern 4 — Describing operator products in protocol documents

```markdown
# BAD — in BANZA_ARCHITECTURE.md
The reference operator Banzami uses Next.js for its merchant dashboard,
running at dashboard.banzami.org on port 3000.

# GOOD — in BANZA_ARCHITECTURE.md
The Banzami reference operator demonstrates the protocol in production.
See [BANZAMI_ARCHITECTURE.md](../banzami/BANZAMI_ARCHITECTURE.md) for the implementation topology.
```

---

## Path Conventions

Cross-repository references use relative paths from the file location:

| From | To | Path format |
|------|----|-------------|
| `~/banza/*.md` | `~/banzai/*.md` | `../banzai/BANZAI_REFERENCE.md` |
| `~/banza/*.md` | `~/banzami/*.md` | `../banzami/BANZAMI_REFERENCE.md` |
| `~/banzai/*.md` | `~/banza/*.md` | `../banza/BANZA_REFERENCE.md` |
| `~/banzai/*.md` | `~/banzami/*.md` | `../banzami/BANZAMI_REFERENCE.md` |
| `~/banzami/*.md` | `~/banza/*.md` | `../banza/BANZA_REFERENCE.md` |
| `~/banzami/*.md` | `~/banzai/*.md` | `../banzai/BANZAI_REFERENCE.md` |

Same-repository references use local paths:

```markdown
See [BANZA_GOVERNANCE.md](BANZA_GOVERNANCE.md) for the ADR process.
```

---

## Document Hierarchy for Reference Resolution

When a document needs to reference protocol content, resolve at the highest applicable level:

```
Priority 1: BANZA_REFERENCE.md    — canonical protocol definition
Priority 2: BANZA_CERTIFICATION.md — certification rules
Priority 3: BANZA_CONFORMANCE.md  — conformance test vectors
Priority 4: BANZA_GOVERNANCE.md   — governance process
Priority 5: docs/adr/ADR-NNN.md   — specific decision record
```

Never reference a lower-priority document when a higher-priority one contains the canonical definition.

---

## Universal Preamble (kept from REFERENCE-CANONICAL-SEPARATION-001)

Every REFERENCE document opens with:

```
BANZA    = open financial infrastructure protocol
BanzAI   = Protocol Operating System
Banzami  = reference operator implementation
```

With an arrow (← THIS DOCUMENT) on the owning layer's line.

The new canonical documents (ARCHITECTURE, GOVERNANCE, etc.) do NOT need the full preamble — their filename prefix already establishes ownership. They should open with a one-line ownership declaration:

```markdown
> This document describes: **BANZA** — the open financial infrastructure protocol.
> For other layers: [BanzAI](../banzai/BANZAI_REFERENCE.md) · [Banzami](../banzami/BANZAMI_REFERENCE.md)
```

---

*Produced by: ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001*
