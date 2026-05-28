# Contributing to Banzami

Thank you for your interest in contributing to Banzami — open financial infrastructure for programmable instant payments.

---

## What you can contribute to

| Area | Examples |
|---|---|
| **Rust core crates** | Bug fixes, new engine features, additional provider trait implementations, invariant tests |
| **SDKs** | Bug fixes, new language features, better error messages, test coverage |
| **Contracts** | OpenAPI corrections, webhook schema improvements, QR spec clarifications |
| **Documentation** | Translations, examples, guides, ADR discussions |
| **Integrations** | New framework plugins, commerce platform adapters |
| **SDK certification** | New test vectors, edge case coverage |

## What is out of scope here

- The Banza commercial product (apps, backend services, production infrastructure)
- Banza design system and branded UI components
- Production deployment and operational tooling
- Operator-specific provider implementations (e.g., EMIS, specific bank adapters)

---

## How to contribute

### 1. Open an issue first

For anything beyond a trivial bug fix, open an issue to discuss the change before writing code. This prevents wasted effort and aligns with Banzami's protocol governance.

### 2. Fork and branch

```bash
git clone https://github.com/banzami/banzami.git
cd banzami
git checkout -b feature/your-change
```

### 3. Make your change

Follow existing code style per area:

**Rust (core crates)**
```bash
cargo fmt --all
cargo clippy --workspace --all-targets
cargo test --workspace
```

**TypeScript**: ESLint + Prettier (`.eslintrc`, `.prettierrc`)

**Python**: Ruff + mypy (`pyproject.toml`)

**PHP**: PSR-12

**Go**: `gofmt`

**Dart/Flutter**: `dart format`

### 4. Test

Every area has a test suite. Run it before submitting:

```bash
# Rust core
cargo test --workspace

# TypeScript SDK
cd sdk/typescript && npm test

# Python SDK
cd sdk/python && pytest

# Go SDK
cd sdk/go && go test ./...
```

SDK changes must pass the certification suite:

```bash
cd sdk-certification && python python/test_webhook_vectors.py
```

### 5. Submit a pull request

- Keep PRs focused — one change per PR
- Include a clear description of what changed and why
- Reference any related issues

---

## Rust core standards

The financial core crates hold the highest correctness bar in the project.

### Financial invariants

Any change to a financially critical crate must preserve all invariants documented in [`docs/core/financial-invariants.md`](docs/core/financial-invariants.md). The invariants are:

- **Zero-sum**: every ledger posting balances (sum of debits == sum of credits)
- **Immutability**: ledger entries are append-only
- **Idempotency**: same key produces same result
- **Non-negative balances**: wallet available balance never goes below zero
- **Atomicity**: balance changes are transactional

If your change touches the ledger, wallets, or transactions, add a test that demonstrates the invariant holds.

### Test requirements for financial crates

- Unit tests for every state transition in the transaction FSM
- Property test for ledger zero-sum (any sequence of balanced postings must produce a net-zero sum)
- Negative tests: confirm that invariant violations are rejected with the correct error
- Idempotency test: posting the same key twice produces the same result

### Clippy and formatting

All core crates must pass `cargo clippy --workspace --all-targets` with no warnings and `cargo fmt --check` before merging.

### No compile-time sqlx macros in public crates

The public Banzami crates use runtime sqlx queries (`sqlx::query()`) instead of compile-time macros (`sqlx::query!()`). This allows contributors to build and test the crates without a live database. Keep new repository implementations consistent with this pattern.

### No operator-specific logic in core

Core crates must remain operator-agnostic. Do not add:
- Hardcoded provider names (EMIS, Multicaixa, specific banks)
- Country-specific or currency-specific assumptions
- Business rules that belong to an operator implementation

If your change requires operator-specific behavior, express it as a configurable parameter or a trait method that operators implement.

### Review requirements

Changes to the following require review from a project maintainer:
- `banzami-ledger` — any change to posting logic or the zero-sum check
- `banzami-wallets` — any change to the reserve/release/settle mechanics
- `banzami-transactions` — any change to the FSM transition table
- `banzami-acquiring` — any change to the callback processing path
- `docs/core/financial-invariants.md` — invariant definitions

---

## Protocol changes

Changes to `contracts/` (OpenAPI, webhooks, QR, events) require an Architecture Decision Record (ADR) in `docs/adr/`. Protocol changes affect all SDK implementations and must be discussed before merging.

---

## SDK certification

If you are implementing a new language SDK, run the certification suite against your implementation before claiming Banzami compatibility. All implementations must pass the signature vectors in `contracts/sdk-certification/`.

---

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## License

By contributing, you agree that your contributions will be licensed under the [Apache 2.0 License](LICENSE).
