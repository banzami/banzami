# Banzami Core

**Open-source Rust financial infrastructure crates for programmable instant payments.**

This workspace contains the financial primitives that power Banzami-compatible payment systems. Any operator can build on these crates to create their own instant payment network.

---

## Crates

| Crate | Description |
|---|---|
| `banzami-types` | Money, Currency, typed IDs — the shared financial primitives |
| `banzami-ledger` | Double-entry ledger engine — the single financial truth |
| `banzami-wallets` | Merchant wallet engine — ledger-backed balances |
| `banzami-consumer-wallets` | Consumer wallet engine — end-user ledger-backed wallets |
| `banzami-transactions` | Transaction lifecycle — authorize, capture, reverse |
| `banzami-transfers` | P2P wallet-to-wallet transfers via @handle |
| `banzami-qr` | QR code generation and validation (static + dynamic) |
| `banzami-payment-links` | Shareable payment links with expiry |
| `banzami-merchants` | Merchant onboarding and API key management |
| `banzami-identity` | Consumer @handle identity and validation |
| `banzami-routing` | Payment rail routing engine (rule-based, pluggable) |
| `banzami-acquiring` | Acquiring layer — bridge to external payment providers |
| `banzami-settlement` | Settlement batch lifecycle |
| `banzami-reconciliation` | External statement reconciliation |
| `banzami-risk` | Risk limit evaluation framework |
| `banzami-compliance` | KYC/KYB status tracking |
| `banzami-payouts` | Outbound payout/disbursement model |

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
│  Banzami Core (this workspace — public)                      │
│                                                              │
│  banzami-ledger  ←  banzami-wallets  ←  banzami-transactions │
│  banzami-qr      ←  banzami-routing  ←  banzami-acquiring    │
│  banzami-types (foundation — no upstream deps)              │
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
banzami-types  = { git = "https://github.com/banzami/banzami" }
banzami-ledger = { git = "https://github.com/banzami/banzami" }
```

Core financial operation — ledger transfer between two wallets:

```rust
use banzami_types::{Money, Currency, AccountId};
use banzami_ledger::PostingBuilder;

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

Operators implement the engine traits to wire Banzami core to their own infrastructure:

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
cargo test -p banzami-ledger
```

Database-dependent tests require a running PostgreSQL instance:

```bash
export DATABASE_URL=postgres://user:pass@localhost/banzami_dev
cargo test -p banzami-ledger -- --include-ignored
```

---

## License

Apache-2.0. See [LICENSE](../LICENSE).
