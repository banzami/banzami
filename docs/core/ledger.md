# banzami-ledger — Double-Entry Ledger Engine

The ledger is the foundation of Banzami's financial correctness. All money movement flows through it.

---

## What it is

`banzami-ledger` is a double-entry accounting ledger engine backed by PostgreSQL. It provides:

- **Accounts** — named buckets of a single currency, typed as ASSET or LIABILITY
- **Postings** — balanced journal entries that move money between accounts
- **Immutability** — entries are append-only; nothing is ever deleted or modified

The ledger does not understand wallets, merchants, transactions, or payments. It only knows accounts and postings. Higher-level crates build on it.

---

## Core types

### Account

An account belongs to one currency and has an `AccountType`:
- `ASSET` — represents something the platform owns (e.g., `system:transit`)
- `LIABILITY` — represents something owed to an external party (e.g., a merchant wallet)

Accounts are created by the wallet engine and referenced by their `AccountId` UUID.

### LedgerEntry

A single debit or credit on a specific account for a specific amount. Entries are always part of a posting — never standalone.

### LedgerPosting

A group of balanced entries. The atomic unit of the ledger.

**Invariants (enforced before writing):**
- Must contain at least 2 entries
- For every currency present: `sum(debits) == sum(credits)` in minor units
- Has a globally unique `idempotency_key`

---

## How postings work

```rust
use banzami_ledger::{PostingBuilder, LedgerEngine};
use banzami_types::{Money, Currency};

let amount = Money::new(500_000, Currency::AOA); // 5000.00 AOA

let posting = PostingBuilder::new(
    "QR payment settlement",
    "settle-qr-txn-abc123",
)
.debit(system_transit_account, amount)   // ASSET: DR reduces platform holding
.credit(merchant_wallet_account, amount) // LIABILITY: CR increases merchant funds
.build()?;

ledger.post(posting).await?;
```

### Idempotency

If the same `idempotency_key` is submitted twice, the second call returns the existing posting. No duplicate entries are created. This is enforced at the database level via a unique index.

---

## Account types and sign conventions

| Account Type | Debit effect | Credit effect |
|---|---|---|
| ASSET | Increases balance | Decreases balance |
| LIABILITY | Decreases balance | Increases balance |

Merchant wallets are LIABILITY accounts. When a payment is received:
- `system:transit` (ASSET) is **debited** — the platform received the funds
- `merchant wallet` (LIABILITY) is **credited** — the platform owes the merchant

This is standard double-entry bookkeeping. The ledger enforces zero-sum; the sign convention is how you read it.

---

## Immutability and audit

Ledger postings are never updated or deleted. The entire financial history is preserved in `ledger_postings` and `ledger_entries`. Any correction (e.g., a refund) is expressed as a new posting with reversed entries.

This makes the ledger a complete, immutable audit trail.

---

## Operator note

The `LedgerEngine` trait is fully generic. The provided implementation (`PostgresLedgerEngine`) uses PostgreSQL. An operator can implement a different backend (e.g., a ledger-as-a-service, or a test in-memory backend) by implementing the trait.

For invariant details, see [financial-invariants.md](financial-invariants.md).
