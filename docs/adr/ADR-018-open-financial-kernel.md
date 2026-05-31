# ADR-018 — Banza as Open Financial Infrastructure Kernel

**Status:** Accepted  
**Date:** 2026-05-28  
**Author:** the reference operator Organisation  
**Deciders:** Fidel Monteiro (Founder)  
**Supersedes:** None

---

## Context

Banza began as a single private fintech product targeting Angola's payment market. As the platform matured, it became clear that the generic financial primitives — double-entry ledger, wallet engine, transaction FSM, routing, settlement, QR runtime — had value beyond any single commercial deployment.

The problem: the infrastructure was entirely private, tightly coupled to one operator (the reference operator), and inaccessible to contributors, researchers, and alternative operators. This created:

- Invisible coupling: the "infrastructure" was inseparable from the "product"
- Contributor barrier: no way to experiment without access to private infrastructure
- Single-operator lock-in: the architecture could not evolve to support multiple operators
- No external validation: invariants could not be audited by the community

## Decision

Banza is restructured as an **open financial infrastructure kernel**: a collection of generic Rust crates that implement the financial primitives of instant payment networks, published under Apache 2.0 at `github.com/banza-protocol/banza`.

The kernel is operator-neutral. It defines:
- Financial state machines (transactions, wallets, settlement)
- Invariant enforcement (zero-sum ledger, idempotency, atomicity)
- Provider interfaces (acquiring, routing, notification, risk)
- Protocol specifications (QR payload, webhook schemas, OpenAPI contracts)

The analogy is precise:
- Banza kernel = Linux kernel
- the reference operator (first commercial operator) = Ubuntu / first distribution
- Future operators = future distributions

## Consequences

**Positive:**
- Community contribution is now possible without access to private infrastructure
- Financial invariants are publicly auditable
- The architecture supports multiple independent operators
- the reference operator becomes clearly "one operator" rather than "the only possible implementation"
- External trust increases: operators can inspect what they're running

**Negative:**
- Kernel evolution requires careful backwards-compatibility discipline (see ADR-019)
- Provider interfaces must be stable before operators build on them
- Maintaining two repos (public kernel + private operator) adds coordination overhead

## Alternatives considered

**Keep everything private:** Rejected. Creates permanent contributor barrier and prevents ecosystem formation.

**Open-source the entire the reference operator product:** Rejected. the reference operator includes operational secrets, compliance rules, and provider credentials that cannot be public.

**Open-source contracts only (not Rust core):** Rejected. The value is in the verifiable invariant implementations, not just the protocol specs.
