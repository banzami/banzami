# banza-wallets — Merchant Wallet Engine

Merchant wallets hold the funds that merchants accumulate from payments. The wallet engine manages the reserve/release/settle lifecycle and derives balances from the ledger.

---

## What it is

`banza-wallets` provides the merchant wallet lifecycle:
- Create wallets
- Check balances (derived from ledger, never stored separately)
- Reserve funds (hold before payment capture)
- Release reservations (cancel a hold)
- Settle (move funds from reserved to available after payment capture)

For consumer wallets, see `banza-consumer-wallets`.

---

## Balance model

Each wallet maintains two ledger accounts:
- **available_account** — funds the merchant can withdraw
- **reserved_account** — funds held pending transaction capture

```
wallet.available = ledger.balance(available_account)
wallet.reserved  = ledger.balance(reserved_account)
```

Balances are never stored in a wallet column — they are always derived from the ledger. The ledger is the single source of truth.

---

## Reserve / release / settle cycle

This is the core operation for QR and payment link flows:

```
1. RESERVE   — debit available_account, credit reserved_account
               (funds move from free to held)

2a. SETTLE   — debit reserved_account, credit available_account
               (payment confirmed: held funds become free)

2b. RELEASE  — debit reserved_account, credit available_account
               (payment cancelled: held funds return to free)
```

All three are expressed as balanced ledger postings. No balance column is mutated.

### Invariant

At all times: `available + reserved == total inflows - total outflows`

No money is created or destroyed by reserve/release/settle. This is enforced by the ledger's zero-sum rule.

---

## Non-negative balance enforcement

Before accepting a `ReserveRequest`, the engine checks that `available >= amount`. If not, it returns `WalletError::InsufficientFunds`. This prevents the available balance from going negative.

---

## Ledger posting pattern

A QR payment settlement (the canonical flow) produces:

```
DR system:transit          5000.00 AOA   (platform received funds from provider)
CR merchant:available      5000.00 AOA   (merchant credited)
```

A wallet reserve (before capture):

```
DR merchant:available      5000.00 AOA
CR merchant:reserved       5000.00 AOA
```

A settlement (after capture):

```
DR merchant:reserved       5000.00 AOA
CR merchant:available      5000.00 AOA
```

A release (cancelled payment):

```
DR merchant:reserved       5000.00 AOA
CR merchant:available      5000.00 AOA
```

---

## Operator note

`WalletEngine` is generic over `LedgerEngine` and `WalletRepository`. Operators inject their own ledger and repository implementations. The engine itself contains no database calls — it delegates all persistence to the provided implementations.

For invariant details, see [financial-invariants.md](financial-invariants.md).
