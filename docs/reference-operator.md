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

The reference operator is emphatically **not** any of the following:

| Claim | Reality |
|-------|---------|
| A production payment processor | State is in-memory and resets on restart |
| A licensed financial institution | No regulatory compliance, no real accounts |
| A commercial operator | No revenue, no customers, no SLA |
| A fintech product | No UI beyond the educational demo wallet |
| A second Banza | No EMIS, no Multicaixa, no real bank rails |
| A production security reference | Fake HMAC secrets, no TLS enforcement, no auth |
| A deployment template | Not hardened, not monitored, not recoverable |

### Boundary enforcement

The following are permanently **forbidden** in `reference/`:

- Real bank or payment rail integrations
- Firebase, APNs, or any cloud push notification service
- Real operator credentials or API keys
- KYC or AML workflows
- Production analytics or observability pipelines
- Merchant onboarding or operations tooling
- Fraud scoring engines
- Any code that could process real payments

When in doubt: if it involves real money or real people, it does not belong in
`reference/`. Open a PR to the appropriate operator's private repository instead.

### Keeping the reference operator minimal

The reference operator must remain a thin, educational shell around the kernel.
New features in `reference/` should answer **yes** to all three:

1. Does it help a developer understand the Banzami kernel?
2. Can it run entirely without external infrastructure?
3. Would it be useful in any operator's context (not just Banza)?

Features that answer **no** to any of these belong in an operator deployment,
not in the public kernel repository.

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
├── Cargo.toml              — workspace root
├── Dockerfile              — builds sandbox-operator from monorepo root
├── docker-compose.yml      — one-command startup
├── demo-wallet/            — browser UI (index.html, no build step)
├── fake-acquirer/          — AcquirerProvider: HMAC-signed fake payment rail
├── local-ledger/           — SQLite double-entry ledger with seed data + reset
├── local-notifications/    — NotificationProvider: stdout + null implementations
├── mock-routing/           — RoutingEngine: verbose mock, failing, degraded modes
├── simulated-settlement/   — SettlementExecutionProvider: always succeeds
└── sandbox-operator/       — HTTP server wiring all providers together (:3100)
```

### local-ledger

A SQLite-backed double-entry ledger that mirrors the kernel's invariants without
requiring PostgreSQL. Seed data populates five accounts (two merchants, two
consumers, one fee account) with deterministic opening balances and a sample
payment posting. State can be reset via `LocalLedger::reset()`.

### mock-routing

Three `RoutingEngine` implementations for local development:

| Type | Behaviour |
|------|-----------|
| `MockRoutingEngine` | Routes normally, logs every decision via `tracing` |
| `FailingRoutingEngine` | Always returns `NoEligibleRail` |
| `DegradedRoutingEngine` | Always returns `AllRailsDegraded` |

### demo-wallet

A standalone HTML file that talks to the sandbox operator via `fetch()`. Open it
directly in a browser — no build step, no framework. Displays seed wallet balances,
lets you create wallets and send transfers, shows transfer history.
