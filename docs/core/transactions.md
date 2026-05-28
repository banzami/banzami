# banzami-transactions — Transaction Lifecycle

The transactions crate manages the state machine for merchant payment transactions from initiation through capture, settlement, and refund.

---

## What it is

`banzami-transactions` provides:
- Transaction state machine with strict transitions
- Lifecycle operations: initiate, capture, cancel, fail, refund
- Integration with wallet reserve/release/settle

---

## State machine

```
INITIATED
    │
    └─▶ PENDING (payment reference generated)
            │
    ┌───────┼───────────┐
    │       │           │
CAPTURED  CANCELLED  EXPIRED
    │
    └─▶ SETTLED / FAILED / REFUNDED
```

Transitions:
- `INITIATED → PENDING` — provider reference generated
- `PENDING → CAPTURED` — customer completed payment (callback received)
- `PENDING → CANCELLED` — merchant cancelled
- `PENDING → EXPIRED` — payment window elapsed
- `CAPTURED → SETTLED` — funds cleared to merchant wallet
- `CAPTURED → REFUNDED` — amount returned to customer
- `CAPTURED → FAILED` — settlement failed (retryable)

Invalid transitions are rejected by the engine.

---

## Atomicity

State transitions that involve money movement (PENDING → CAPTURED, CAPTURED → SETTLED) are atomic with their corresponding wallet operations:

- `PENDING → CAPTURED`: wallet reserve is posted atomically with the status update
- `CAPTURED → SETTLED`: wallet commit is posted atomically with the status update
- `PENDING → CANCELLED` / `EXPIRED`: wallet release is posted atomically with the status update

If the wallet operation fails, the transaction status is not updated. There is no state where a wallet is reserved but no corresponding transaction is PENDING.

---

## Idempotency

Each operation that moves money carries an `idempotency_key` derived from the transaction ID and the operation type. Re-submitting the same event produces the same result without side effects.

---

## Invariants

- Invalid state transitions return an error — no silent state corruption
- All money-moving transitions are atomic with their wallet operations
- A transaction cannot be CAPTURED without a wallet reserve
- A transaction cannot be SETTLED without a wallet commit
- CANCELLED and EXPIRED transitions release the wallet reserve

For invariant details, see [financial-invariants.md](financial-invariants.md).
