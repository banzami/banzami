# Financial Invariants

These invariants are mandatory across all Banza core crates. Any operator implementation that violates them is not a correct Banza implementation.

---

## Ledger invariants

### INV-L01 — Zero-sum balance

Every `LedgerPosting` must be perfectly balanced: for each currency present, `sum(debits) == sum(credits)` in minor units. A posting with a non-zero net is rejected by the engine before writing to the database.

The check is enforced in `LedgerPosting::assert_balanced()` which is called by the engine before any database write.

### INV-L02 — Immutability

Ledger entries are append-only. Once posted, a `LedgerPosting` and its entries are never modified or deleted. Corrections are made by posting reversing entries.

### INV-L03 — Idempotency

Every posting carries a caller-supplied `idempotency_key`. If the same key is submitted twice, the engine returns the existing posting without creating a duplicate. This is enforced at the database level via `UNIQUE ON (idempotency_key)` and at the application level by checking before inserting.

### INV-L04 — No orphan entries

Every `LedgerEntry` belongs to a `LedgerPosting`. Entries are never inserted standalone — they are always part of a balanced posting.

---

## Wallet invariants

### INV-W01 — Non-negative available balance

The available balance of any wallet must never go below zero. The engine enforces this by checking the balance before posting a reserve. Any operation that would result in a negative available balance is rejected with `InsufficientFunds`.

### INV-W02 — Reserve/release/commit consistency

For any sequence of operations on a wallet:

```
available + reserved = total funds credited - total funds settled
```

The reserve operation moves funds from `available` to `reserved`. Release moves them back. Commit (settle) removes them from `reserved` and credits the merchant. No money is created or destroyed.

### INV-W03 — Balance via ledger

Wallet balances are derived from the ledger — there is no separate balance column that can diverge. The engine sums `LedgerEntry` amounts for the wallet's accounts to produce the balance. This means the ledger is the single source of truth.

### INV-W04 — Account type consistency

Wallet accounts are `LIABILITY` type in the ledger (representing funds owed to the merchant). Credit increases the liability (funds available to merchant). Debit decreases it (funds paid out or reserved). The engine negates the raw ledger value to produce merchant-facing positive balances.

---

## Transaction invariants

### INV-T01 — Deterministic state transitions

Transaction states follow a strict finite state machine:

```
INITIATED → PENDING → CAPTURED → SETTLED / FAILED / REFUNDED
                ↓
            CANCELLED / EXPIRED
```

Any transition not in the FSM is rejected. The engine validates the state before writing.

### INV-T02 — Replay safety

Processing the same transaction event twice produces the same result. Transaction state transitions are idempotent — if the transaction is already in the target state, the operation is a no-op.

### INV-T03 — Atomicity

All state change operations (status + ledger posting) are executed within a single database transaction. A transaction cannot be captured without a corresponding wallet reserve. A transaction cannot be settled without a corresponding wallet commit.

---

## Settlement invariants

### INV-S01 — Explicit lifecycle states

Settlement batches follow a strict lifecycle:

```
PENDING → PROCESSING → COMPLETED / FAILED
```

No batch is permanently lost — failed batches remain in FAILED state and can be retried.

### INV-S02 — No partial mutation

Settlement batch amounts (gross, fee, net) are computed at creation time and are immutable. The engine never modifies batch amounts after creation. Corrections require creating a new batch.

### INV-S03 — Period coverage

Each settlement batch covers a specific, non-overlapping time period. The scheduler ensures that no two batches for the same merchant + wallet + period can coexist (idempotent creation via `ON CONFLICT DO NOTHING`).

---

## Routing invariants

### INV-R01 — Environment isolation

The routing engine must never route a production payment through a sandbox rail or vice versa. Operators are responsible for configuring separate routing tables per environment. The engine carries no environment enforcement — that is the operator's responsibility at the provider level.

### INV-R02 — No implicit fallback

If no routing rule matches a payment, the engine returns an error. It does not silently route through a default or fallback provider. Silence would hide misconfiguration.

---

## Acquiring invariants

### INV-A01 — Signature validation before state change

Inbound provider callbacks are HMAC-validated before any state change occurs. An invalid or missing signature causes the request to be rejected before the acquiring payment record is touched.

### INV-A02 — Idempotent callback processing

Duplicate callbacks (same `idempotency_key`) are detected via the `acquiring_callbacks.idempotency_key` unique index. Duplicate callbacks return the current payment state without re-processing.

### INV-A03 — Wallet credit after confirmation only

A merchant wallet is credited only after a payment callback is validated and the acquiring payment is moved to `CONFIRMED`. There is no pre-credit.

---

## Enforcement

These invariants are enforced at multiple layers:

| Layer | Mechanism |
|---|---|
| Rust type system | Strong types prevent unit confusion (e.g., `Money` wraps `i64`) |
| Engine pre-conditions | Checked before database writes |
| Database constraints | `UNIQUE`, `CHECK`, `NOT NULL` on critical columns |
| Idempotency keys | Unique at database level, checked at application level |
| Tests | Unit tests verify invariant properties; property tests for ledger balance |

---

## Violations

If you discover a violation of any invariant — in the core crates, in documentation, or in a reference implementation — please open a GitHub issue tagged `financial-invariant`.

Security-sensitive violations (e.g., a way to credit a wallet without a corresponding debit) should be reported via the security policy in [SECURITY.md](../../SECURITY.md).
