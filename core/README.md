# Banza Core

**Open-source Rust financial infrastructure crates for programmable instant payments.**

This workspace contains the financial primitives that power Banza-compatible payment systems. Any operator can build on these crates to create their own instant payment network.

---

## Crates

| Crate | Description |
|---|---|
| `banza-types` | Money, Currency, typed IDs — the shared financial primitives |
| `banza-ledger` | Double-entry ledger engine — the single financial truth |
| `banza-wallets` | Merchant wallet engine — ledger-backed balances |
| `banza-consumer-wallets` | Consumer wallet engine — end-user ledger-backed wallets |
| `banza-transactions` | Transaction lifecycle — authorize, capture, reverse |
| `banza-transfers` | P2P wallet-to-wallet transfers via @handle |
| `banza-qr` | QR code generation and validation (static + dynamic) |
| `banza-payment-links` | Shareable payment links with expiry |
| `banza-merchants` | Merchant onboarding and API key management |
| `banza-identity` | Consumer @handle identity and validation |
| `banza-routing` | Payment rail routing engine (rule-based, pluggable) |
| `banza-acquiring` | Acquiring layer — bridge to external payment providers |
| `banza-settlement` | Settlement batch lifecycle |
| `banza-reconciliation` | External statement reconciliation |
| `banza-risk` | Risk limit evaluation framework |
| `banza-compliance` | KYC/KYB status tracking |
| `banza-payouts` | Outbound payout/disbursement model |

---

## Architecture

The core follows a **layered architecture** with clear domain boundaries:

```
┌──────────────────────────────────────────────────────────────┐
│  Operator Layer (your code — private)                        │
│  Apps · APIs · Provider adapters · Business rules           │
└───────────────────┬──────────────────────────────────────────┘
                    │ depends on
┌───────────────────▼──────────────────────────────────────────┐
│  BANZA Core (this workspace — public)                        │
│                                                              │
│  banza-ledger  ←  banza-wallets  ←  banza-transactions │
│  banza-qr      ←  banza-routing  ←  banza-acquiring    │
│  banza-types (foundation — no upstream deps)              │
└──────────────────────────────────────────────────────────────┘
```

---

## Financial invariants

Every crate enforces its invariants at the type level or at validation time:

- **Double-entry**: every ledger posting must sum to zero (debit = credit)
- **Immutability**: ledger entries are append-only; no retroactive mutation
- **No negative balance**: wallet available balance cannot go below zero
- **Idempotency**: identical `idempotency_key` produces the same result
- **Atomic**: balance changes are transactional — partial updates are impossible

---

## Quick start

Add to your `Cargo.toml`:

```toml
[dependencies]
banza-types  = { git = "https://github.com/banza-protocols/banza" }
banza-ledger = { git = "https://github.com/banza-protocols/banza" }
```

Core financial operation — ledger transfer between two wallets:

```rust
use banza_types::{Money, Currency, AccountId};
use banza_ledger::PostingBuilder;

let amount = Money::new(100_000, Currency::AOA); // 1000.00 AOA

let posting = PostingBuilder::new()
    .debit(consumer_wallet_account, amount.clone())
    .credit(merchant_wallet_account, amount)
    .idempotency_key("txn_xyz_20260528")
    .build()?;

ledger_engine.post(posting).await?;
```

---

## Operator integration

Operators implement the engine traits to wire Banza core to their own infrastructure:

```rust
// Your private code: implement AcquirerProvider for your payment rail
struct MyProviderAdapter { ... }

impl AcquirerProvider for MyProviderAdapter {
    async fn initiate_payment(&self, req: InitiatePaymentRequest)
        -> Result<ExternalPaymentRef, AcquirerError> { ... }

    async fn validate_callback(&self, raw: &[u8], sig: &str)
        -> Result<PaymentConfirmation, AcquirerError> { ... }

    fn provider_name(&self) -> &str { "MY_PROVIDER" }
}

// Wire into the generic acquiring engine
let engine = PostgresAcquiringEngine::new(MyProviderAdapter::new(...), repo);
```

---

## Development

Prerequisites: Rust stable (1.75+), PostgreSQL 15+.

```bash
# Build all crates
cargo build

# Run all tests
cargo test

# Run tests for a specific crate
cargo test -p banza-ledger
```

Database-dependent tests require a running PostgreSQL instance:

```bash
export DATABASE_URL=postgres://user:pass@localhost/banza_dev
cargo test -p banza-ledger -- --include-ignored
```

---

## License

Apache-2.0. See [LICENSE](../LICENSE).
