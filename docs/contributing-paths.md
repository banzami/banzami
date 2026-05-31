# Contribution Paths

This document maps contribution areas to review requirements. It helps
contributors understand where to start, what is safe to work on independently,
and what requires stricter review.

---

## Safe contribution areas

These areas have well-defined interfaces and low risk of financial invariant
violations. Good starting points for new contributors.

### Core Rust crates — non-financial

| Area | Crates | Examples |
|------|--------|---------|
| Identity | `banza-identity` | `@handle` validation, namespace rules |
| QR parsing | `banza-qr` | QR payload encoding, expiry logic |
| Payment links | `banza-payment-links` | Link lifecycle, URL generation |
| Routing algorithms | `banza-routing` | New routing strategies, rail priority logic |
| Capability model | `banza-capabilities` | New capability flags, operator manifests |
| Risk limits | `banza-risk` | Limit rules, velocity checks |

### Reference implementations

All of `reference/` is safe for contribution. Reference crates use only simulated
providers and have no impact on real financial flows.

| Component | Path | Examples |
|-----------|------|---------|
| Sandbox operator | `reference/sandbox-operator/` | New API endpoints, better logging |
| Mock routing | `reference/mock-routing/` | Routing failure scenarios, logging |
| Local ledger | `reference/local-ledger/` | SQLite performance, seed data |
| Demo wallet | `reference/demo-wallet/` | UI improvements, new views |
| Simulated providers | `reference/fake-acquirer/`, `reference/simulated-settlement/` | New simulation scenarios |

### SDKs

| SDK | Path | Examples |
|-----|------|---------|
| TypeScript | `sdk/typescript/` | Type improvements, new methods |
| Python | `sdk/python/` | Type stubs, new endpoints |
| PHP | `sdk/php/` | New client methods, error handling |
| Go | `sdk/go/` | Idiomatic Go improvements |
| Flutter | `sdk/checkout-web/` | Widget improvements |

### Documentation

All of `docs/` — ADRs, RFCs, domain docs, architecture docs — welcomes
contribution. New RFCs require no special permission; draft them and open a PR.

### Testing and tooling

- New unit tests for any crate
- New mock provider implementations
- New SDK certification test vectors
- CI configuration improvements
- Docker / local development tooling

---

## Sensitive contribution areas

These areas are adjacent to financial invariants or concurrency correctness.
They require stricter review by at least one maintainer with financial
infrastructure experience.

### Double-entry ledger

**Crate:** `banza-ledger`

Risk: An incorrect change could allow:
- Unbalanced postings (money created from nothing)
- Double-counting (same entry applied twice)
- Ledger entry mutation (financial history altered)

**Review gate:** Every change to `posting.rs`, `engine.rs`, or `repository.rs`
must be accompanied by a proof that the zero-sum invariant (INV-L01) is
preserved under the change. New operations must include an invariant test.

### Wallet balance mutation

**Crate:** `banza-wallets`, `banza-consumer-wallets`

Risk: An incorrect change could allow:
- Negative available balance (money spent that does not exist)
- Reserve/release asymmetry (reserved funds not returned on cancel)
- Balance from stored value rather than entries (stale balance reads)

**Review gate:** Changes to reserve/release/settle logic must include:
- An invariant test demonstrating conservation
- Proof that the DB transaction wraps all balance mutations atomically

### Settlement lifecycle

**Crate:** `banza-settlement`

Risk: Incorrect settlement logic could cause:
- Duplicate bank transfers (same payment settled twice)
- Missing settlements (payment confirmed but merchant never paid)
- Incorrect netting (wrong amount transferred)

**Review gate:** Changes must demonstrate idempotency under retry and correct
handling of partial failures.

### Transaction FSM

**Crate:** `banza-transactions`

Risk: An incorrect state transition could allow:
- A transaction to be refunded before it is settled
- A cancelled transaction to be captured
- A completed transaction to be re-processed

**Review gate:** Every new state transition must be accompanied by a state
diagram update and a test covering both the happy path and the invalid
transition attempt.

---

## Contribution checklist

Before opening a PR:

- [ ] Tests pass: `cargo test` in the relevant workspace
- [ ] No compile warnings: `cargo build` clean
- [ ] No new operator-specific assumptions in kernel code
- [ ] No compile-time sqlx macros (use `sqlx::query()` runtime form)
- [ ] For sensitive areas: invariant test included
- [ ] For new provider traits: `ProviderCapabilityDescriptor` implemented

For RFCs:
- [ ] Filed as `docs/rfc/RFC-XXXX-title.md`
- [ ] Status set to `Draft`
- [ ] All required sections present (see RFC template in `docs/rfc/README.md`)

---

## Multi-operator architecture contribution

The ecosystem is designed for eventual multi-operator deployments. Contributions
that prepare for this future are welcome:

- New entries in `OperatorCapabilityFlags` (with RFC)
- New wallet capability flags (with RFC)
- Provider capability negotiation improvements
- Operator manifest format improvements
- Reference interop test implementations

Contributions that couple the kernel to a specific operator are never accepted.
If you are building an operator-specific adapter, it belongs in your private
operator repository.

---

## Long-term ecosystem direction

Banza is built to be:

- **Infrastructure**, not application code
- **Neutral**, not tied to any operator, geography, or provider
- **Extensible**, not opinionated about deployment topology
- **Correct**, where correctness is defined by financial invariants, not by tests

The goal is for Banza to occupy the same position in financial infrastructure
that Linux occupies in operating systems: a stable, auditable, neutral foundation
that any operator can deploy, extend, and build commercial products on top of.

Contributions that move the ecosystem in this direction — better abstractions,
more comprehensive invariant coverage, cleaner provider interfaces, richer
capability negotiation — are the most valuable long-term contributions.
