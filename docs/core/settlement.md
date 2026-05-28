# banzami-settlement — Settlement Lifecycle

The settlement crate manages the lifecycle of merchant settlement batches — the process by which accumulated transaction funds are grouped and disbursed to merchants.

---

## What it is

`banzami-settlement` provides:
- Settlement batch creation (grouping captured transactions by merchant + currency + period)
- Settlement state machine (PENDING → PROCESSING → COMPLETED / FAILED)
- Background scheduler that auto-creates daily settlement batches

---

## Settlement model

Settlement is a two-step process:

1. **Batch creation** — the scheduler groups CAPTURED transactions from a time period into a settlement batch, computing gross, fee, and net amounts
2. **Batch execution** — the operator's settlement process moves the batch from PENDING to PROCESSING to COMPLETED (e.g., by initiating a bank transfer)

The core crate handles step 1. Step 2 is operator-specific and depends on the operator's bank integration.

---

## Settlement batch

A batch covers:
- One merchant
- One wallet
- One currency
- One time period (e.g., one UTC day)

Batch amounts are computed once at creation time and are immutable:
- `gross_amount_minor` — total transaction revenue
- `fee_amount_minor` — platform fees
- `net_amount_minor` — amount to disburse to merchant (gross − fee)

---

## State machine

```
PENDING
  │
  └── operator starts processing
       │
  PROCESSING
       │
  ┌────┴────┐
  │         │
COMPLETED  FAILED
```

Transitions:
- `PENDING → PROCESSING` — operator begins disbursement
- `PROCESSING → COMPLETED` — disbursement confirmed (e.g., bank ACK)
- `PROCESSING → FAILED` — disbursement failed (retryable)

---

## Daily scheduler

The `run_settlement_scheduler` background task:
1. Ticks once per configurable interval (default: 24 hours)
2. Aggregates CAPTURED transactions from the previous UTC day per (merchant, wallet, currency)
3. Creates a PENDING batch for each group that doesn't already have one

Idempotency: the scheduler uses `ON CONFLICT DO NOTHING` on `(merchant_id, wallet_id, period_start)`. It is safe to restart without creating duplicate batches.

---

## Operator integration

The operator's settlement execution layer:
1. Queries PENDING batches
2. Initiates bank transfer for each batch
3. Updates batch status based on bank response

The `SettlementEngine` trait provides the query and update interface. Operators can implement alternative backends.

---

## Invariants

- Batch amounts are immutable after creation
- No two batches can cover the same merchant + wallet + period
- Failed batches remain in FAILED state — they are never silently dropped
- Settlement execution is separate from batch creation (separation of concerns)

For invariant details, see [financial-invariants.md](financial-invariants.md).
