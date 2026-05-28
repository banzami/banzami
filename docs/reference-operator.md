# Reference Operator

The reference operator is a minimal HTTP server that wires up the Banzami kernel
using fully simulated providers. It runs entirely in memory — no database, no cloud
services, no external network calls.

**The reference operator is not a production financial institution implementation.**
It exists to let developers explore, validate, and build against the Banzami kernel
without standing up any external infrastructure.

## What it is

| Aspect | Value |
|--------|-------|
| Purpose | Local development and kernel exploration |
| State | In-memory (resets on restart) |
| Database | None required |
| External calls | None — all providers are simulated |
| Port | 3100 (default) |

## What it is not

- Not a production payment processor
- Not connected to any real bank or payment rail
- Not suitable for any live transaction processing
- Not a reference for production security configuration

## Quick start

```bash
# Option 1 — Cargo (from monorepo root)
cd reference
cargo run --bin sandbox-operator

# Option 2 — Docker Compose (from reference/ directory)
cd reference
docker compose up
```

The server will be available at `http://localhost:3100`.

## API surface

### Health

```
GET /health
```

Returns operator status and environment tag.

```json
{
  "status": "ok",
  "environment": "sandbox",
  "operator": "banzami-sandbox",
  "note": "This is a local development sandbox — not a production system."
}
```

### Wallets

```
POST /wallets
```

Create an in-memory wallet.

```json
{ "label": "My Test Wallet", "currency": "AOA" }
```

```
GET /wallets/:id
```

Retrieve a wallet by ID. Three seed wallets are created on startup:

| ID | Label | Opening balance |
|----|-------|-----------------|
| `sandbox-merchant-1` | Sandbox Merchant A | 10 000 000 AOA minor units |
| `sandbox-merchant-2` | Sandbox Merchant B |  5 000 000 AOA minor units |
| `sandbox-consumer-1` | Sandbox Consumer   |  2 000 000 AOA minor units |

### Transfers

```
POST /transfers
```

Move funds between two wallets (double-entry: debit source, credit destination).

```json
{
  "from_wallet_id": "sandbox-consumer-1",
  "to_wallet_id":   "sandbox-merchant-1",
  "amount_minor":   50000,
  "currency":       "AOA",
  "note":           "Test payment"
}
```

```
GET /transfers
```

List all transfers recorded in the current session.

## Providers wired up

| Interface | Implementation | Behaviour |
|-----------|---------------|-----------|
| `AcquirerProvider` | `FakeAcquirer` | Returns HMAC-signed fake references; no external calls |
| `SettlementExecutionProvider` | `SimulatedSettlementProvider` | Always succeeds instantly; logs to console |
| `NotificationProvider` | `StdoutNotificationProvider` | Writes events to stdout via `tracing` |

## Writing your own operator

A production operator replaces each simulated provider with a real implementation:

```rust
// Kernel interface (defined in banzami-acquiring)
pub trait AcquirerProvider: Send + Sync {
    async fn initiate_payment(&self, req: InitiatePaymentRequest)
        -> Result<PaymentInitiation, AcquirerError>;

    async fn validate_callback(&self, raw_body: &[u8], signature: &str)
        -> Result<AcquirerCallback, AcquirerError>;
}

// Your production implementation
pub struct EmisAcquirer { /* EMIS credentials */ }

impl AcquirerProvider for EmisAcquirer {
    // real EMIS API calls here
}
```

The kernel (`PostgresAcquiringEngine<P: AcquirerProvider>`) is generic over the
provider. Swap `FakeAcquirer` for `EmisAcquirer` and the kernel works unchanged.

See [ADR-019](adr/ADR-019-operator-separation.md) for the full operator separation
rationale and [ADR-021](adr/ADR-021-provider-abstraction.md) for the provider
abstraction model.

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `PORT` | `3100` | TCP port the operator listens on |
| `RUST_LOG` | `sandbox_operator=debug,banzami=debug,info` | Log level filter |

## Directory layout

```
reference/
├── Cargo.toml              — workspace (fake-acquirer, local-notifications,
│                             simulated-settlement, sandbox-operator)
├── Dockerfile              — builds sandbox-operator from monorepo root
├── docker-compose.yml      — one-command startup
├── fake-acquirer/          — AcquirerProvider: HMAC-signed fake payment rail
├── local-notifications/    — NotificationProvider: stdout + null implementations
├── simulated-settlement/   — SettlementExecutionProvider: always succeeds
└── sandbox-operator/       — HTTP server wiring all providers together
```
