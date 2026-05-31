# CLAUDE_BASE — Banza Ecosystem Operating Rules

**Version:** 1.0  
**Date:** 2026-05-30  
**Authority:** ADR-025 (Ecosystem Naming Inversion, 2026-05-29)  
**Applies to:** ~/banza · ~/banzai · ~/banzami

This document contains rules shared across all repositories in the `banza-protocol` ecosystem. Every repository-specific CLAUDE.md must be read in conjunction with this base.

---

## Canonical Ecosystem Identity (BINDING — never invert)

```
BANZA
= Open financial infrastructure protocol
= The rules, contracts, certification, and settlement kernel
= Exists independently of any operator

BanzAI
= Protocol Operating System
= Intelligence and conformance layer for the protocol
= Serves the BANZA ecosystem — not an independent product
= NOT a Banzami product

Banzami
= Reference operator
= First commercial implementation built on BANZA
= One operator among many possible operators
= NOT the protocol
= NOT the infrastructure
= NOT the ecosystem
```

### Forbidden assumptions (across all repositories)

The following are architectural errors. Never generate content that implies them:

| Assumption | Why it is wrong |
|---|---|
| "Banzami is the protocol" | Banzami is one operator. BANZA is the protocol. |
| "Banzami infrastructure" | Infrastructure belongs to BANZA. |
| "Banzami ecosystem" | The ecosystem is BANZA's. Banzami participates in it. |
| "Banzami kernel" | The kernel is BANZA. Banzami runs on top of it. |
| "BanzAI belongs to Banzami" | BanzAI is the Protocol OS. It serves BANZA, not Banzami. |
| "BANZA is a product" | BANZA is a protocol specification and kernel. |
| "BANZA is a company" | BANZA is an open infrastructure. No single entity controls it. |
| "The protocol dies with Banzami" | The protocol exists independently of any operator. |

---

## Naming Rules

### "BANZA" — use when referring to:
- The open financial infrastructure protocol
- The Rust kernel (ledger, wallets, settlement, reconciliation)
- Protocol specifications and contracts
- The certification framework
- The federation model
- ADRs governing the protocol layer
- The SDK ecosystem (SDKs are protocol-level, not operator-level)
- "Built on BANZA" / "powered by the BANZA protocol"

### "Banzami" — use when referring to:
- The reference operator product
- Consumer wallets and the Banzami app
- The merchant dashboard and QR infrastructure
- `banzami.com` and all operator-facing services
- The commercial entity behind the reference implementation
- "Banzami is built on BANZA"

### "BanzAI" — use when referring to:
- The Protocol Operating System
- Conformance and certification tooling
- RAG-based protocol intelligence
- ADR navigation and operator onboarding tools
- Lives at `banzami.com/banzai`

### SDK naming (protocol-level, Banza-prefixed)
- `@banza/sdk` (TypeScript), `banza/sdk-php`, `banza-go`, `banza-python`, `banza_flutter`
- Classes: `BanzaClient`, `BanzaPay`, `BanzaWebhooks`
- Webhook header: `banza-signature`
- Env var: `BANZA_WEBHOOK_SECRET`

### Protected names (ADR-025 — do not rename yet)
- `@banza` — identity namespace, permanent
- `banzami.com` — domain, deferred
- `contact@banzami.com`, `security@banzami.com` — emails, deferred
- `github.com/banzami` — old org, deferred
- Rust crate names `banza-types`, `banza-ledger`, etc. — renamed from `banzami-*` in BANZA-FULL-DECONTAMINATION-AND-IDENTITY-ALIGNMENT-001; now canonical

---

## Commit Standards

```
type(scope): description
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `infra`, `validation`, `security`

- Never add `Co-Authored-By: Claude` attribution to commits
- Never bump version numbers in document headers (keep Version: 1.0)
- Commit per logical unit — not one large commit at the end
- Always push to `origin/main` after committing — changes are not done until in production

---

## Documentation Standards

### ADRs
Every major technical decision MUST create an ADR at `docs/adr/`:
```
ADR-NNN-short-title.md
```
Each ADR MUST include: context, decision, rationale, alternatives, consequences, tradeoffs.

### Domain documentation
Every domain MUST have `docs/domains/<domain-name>/` explaining:
- business purpose, architecture, flows, invariants, failure scenarios, reconciliation logic, security assumptions.

### README rules
README files must remain synchronized with implementation reality. Outdated documentation is a defect.

### Documentation completeness
If documentation is missing, the task is NOT complete.

---

## Security Standards

- Secrets NEVER in repositories, logs, screenshots, or documentation examples
- TLS everywhere. Authentication and authorization on all services
- Audit logging on all financial operations
- Secret key: server SDK only. Publishable key: client SDK only
- No force push to main/master without explicit user instruction
- No `--no-verify` hook bypass without explicit user instruction

---

## Testing Standards

All financial operations require:
- unit tests
- integration tests (real database — no mocks for financial invariant tests)
- financial invariant tests
- idempotency tests

Critical flows additionally require:
- reconciliation tests
- concurrency tests

---

## Financial Correctness (applies wherever money moves)

Double-entry accounting is mandatory. Every monetary movement must be:
- auditable, immutable, traceable, reproducible, reconcilable

INVALID: `wallet.balance -= amount`  
VALID: `Customer Wallet -1000 Kz / Merchant Pending +1000 Kz` (ledger entry pair)

All money movement MUST go through: double-entry accounting + atomic transactions + immutable ledger events.

Floating-point arithmetic is FORBIDDEN for money. Use integer minor units.

---

## Protocol Terminology

| Term | Meaning |
|---|---|
| Protocol kernel | The BANZA Rust core (ledger, wallets, settlement) |
| Operator | Any entity that builds a product on BANZA (Banzami is the reference operator) |
| Certified operator | An operator that has passed the BanzAI conformance suite |
| Reference operator | Banzami — the first and canonical operator implementation |
| Federation | Multiple operators sharing the same protocol settlement layer |
| Conformance | BanzAI's certification process for verifying operator compliance |
| Invariant | A financial rule that must hold in all states (INV-LEDGER-*, INV-WALLET-*, etc.) |
| Protocol OS | BanzAI — intelligence, certification, and onboarding tooling for operators |

---

## Audit Methodology

When auditing naming, content, or code for ADR-025 compliance, classify findings as:

- **FALSE** — factually incorrect under ADR-025 (e.g., "Banzami is the protocol")
- **MISLEADING** — creates wrong impression (e.g., "Banzami ecosystem")
- **OUTDATED** — was correct pre-ADR-025, not yet updated
- **CONTEXTUAL** — ambiguous, depends on interpretation
- **CORRECT** — correctly applied
- **PROTECTED** — intentionally preserved per ADR-025 (emails, domains, crate names)

---

*This base document is the single source of shared Claude operating rules for the banza-protocol ecosystem.*  
*Repository-specific CLAUDE.md files extend this base with their own responsibilities and guardrails.*
