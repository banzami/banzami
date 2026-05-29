# Settlement Lifecycle

Version: 1.0 · Status: Stable

Settlement converts accumulated wallet receipts into outbound bank disbursements.
Banza's settlement model is batch-based: unsettled inbound transfers for a wallet
are grouped into a batch, a fee is computed, and the net amount is disbursed.

---

## States

```
created ──process──▶ processing ──complete──▶ completed
                                └──fail──▶    failed
```

The sandbox always completes immediately (simulated settlement provider always
succeeds). Production operators implement `SettlementProvider` to connect to
real banking rails.

---

## Flow

```
Merchant (or operator)
  │
  ├─ POST /settlement/batches { wallet_id }
  │
  ▼
Validation
  ├─ wallet exists?
  └─ unsettled inbound transfers exist?

  │ pass
  ▼
Batch computation
  ├─ find all inbound transfers for wallet NOT in settled_transfer_ids
  ├─ gross_minor = SUM(amount_minor)
  ├─ fee_minor   = MAX(gross_minor / 100, 100)   ← 1% simulated fee, min 1.00 AOA
  └─ net_minor   = gross_minor - fee_minor

  │
  ▼
Mark transfers settled (add to settled_transfer_ids set)

  │
  ▼
Create batch (status: completed immediately in sandbox)
  ├─ provider_ref: "SBX-SETTLE-{uuid}"
  └─ trace_id: new root trace

  │
  ▼
Events emitted
  ├─ settlement.created   { batch_id, wallet_id, gross_minor, net_minor, tx_count }
  └─ settlement.completed { batch_id, provider_ref }

  │
  Response: SandboxSettlementBatch object
```

---

## Fee model

The sandbox applies a simulated 1% platform fee:

```
fee_minor   = MAX(gross_minor / 100, 100)
net_minor   = gross_minor - fee_minor
```

This is visible in the demo wallet as:

```
Gross (N transfers)   100,000.00 AOA
Platform fee (1.0%)    -1,000.00 AOA
Net disbursement        99,000.00 AOA
Provider ref          SBX-SETTLE-{uuid}
```

Production fee models are operator-configurable.

---

## Idempotency of settlement

Each transfer can only appear in one settlement batch. The `settled_transfer_ids`
set prevents a transfer from being included twice.

Calling `POST /settlement/batches` on a wallet with no unsettled transfers returns:
```
422 Unprocessable Entity: "no unsettled receipts for this wallet"
```

---

## Provider interface

In production, the sandbox's simulated settlement is replaced by an implementation
of `SettlementProvider`:

```rust
pub trait SettlementProvider: Send + Sync {
    async fn execute_batch(
        &self,
        wallet_id: &str,
        net_minor: i64,
        currency:  Currency,
    ) -> Result<String, SettlementError>;  // Returns provider_ref
}
```

`SimulatedSettlement` in `reference/simulated-settlement/` always returns
`Ok("SBX-SETTLE-{uuid}")`.

---

## Traceability

Every settlement batch has its own `trace_id` (a root trace, not inherited from
any transfer's trace). This means:

- `GET /traces/{batch.trace_id}` returns the batch and its events
- The batch is NOT linked to the transfers it settles (different traces)

This is by design: settlement is an operational event, not a causal descendant
of individual payments.

---

## Sandbox implementation

- `AppState::create_settlement_batch()` — full lifecycle
- `AppState::settled_transfer_ids` — idempotency set
- `reference/simulated-settlement/` — `SimulatedSettlement` provider
