# Reference Operator

The reference operator is a minimal HTTP server that wires up the Banza kernel
using fully simulated providers. It runs entirely in memory — no database, no cloud
services, no external network calls.

**The reference operator is not a production financial institution implementation.**
It exists to let developers explore, validate, and build against the Banza kernel
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
| A second Banzami | No EMIS, no Multicaixa, no real bank rails |
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

1. Does it help a developer understand the Banza kernel?
2. Can it run entirely without external infrastructure?
3. Would it be useful in any operator's context (not just Banzami)?

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
// Kernel interface (defined in banza-acquiring)
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
directly in a browser — no build step, no framework.

---

## Demo Wallet

The demo wallet is a single-file browser UI — `reference/demo-wallet/index.html` —
that provides a visual interface to every sandbox endpoint. Open it directly in any
browser while the sandbox operator is running on `:3100`.

```bash
open reference/demo-wallet/index.html   # macOS
xdg-open reference/demo-wallet/index.html  # Linux
```

The header shows a live connection indicator. A green dot means the sandbox is
reachable on `:3100`. When you interact with any tab, the UI calls the sandbox
REST API and updates in real time.

**Purpose**: The demo wallet is an educational tool. It is not a product template,
not a reference UI library, and not a production interface. Its goal is to let you
_see_ the kernel's operations without writing any code.

### Tab 1 — Wallets

Shows all wallets in the current sandbox session. Seed wallets appear immediately
on startup with their simulated balances.

**What to observe:**

- Four seed wallets: consumer, two merchants, government
- Balances update immediately after any transfer
- Click a wallet row to auto-fill the wallet ID into all other forms

**Relationship to kernel**: calls `GET /wallets` and `GET /wallets/{id}`. Wallet
creation calls `POST /wallets`, which invokes `banza-wallets` internally.

**Expected output** after opening:

```
sandbox-consumer-1   Consumer    20,000.00 AOA
sandbox-merchant-1   Merchant   100,000.00 AOA
sandbox-merchant-2   Merchant    50,000.00 AOA
sandbox-government-1 Government 500,000.00 AOA
```

---

### Tab 2 — Transfer

Executes wallet-to-wallet transfers. Shows transfer history in the current session.

**What to observe:**

- Transfer executes immediately (no settlement lag in sandbox)
- Wallet balances on the Wallets tab update after transfer
- Ledger entries appear on the Ledger tab after transfer
- Events appear on the Events tab (`payment.sent`, `payment.received`)

**Idempotency key field**: fill this in and submit twice — the second submission
returns the same transfer ID and makes no balance change. This demonstrates the
kernel's idempotency guarantees.

**Relationship to kernel**: calls `POST /transfers`, which invokes
`banza-transfers` → `banza-ledger` (two entries) → `NotificationProvider`
(two events).

---

### Tab 3 — Payment Request

Demonstrates the pull-payment flow: merchant creates a request, consumer pays it.

**Example workflow:**

1. "Create Payment Request" — enter merchant wallet and amount, click Create
2. The created ID auto-fills the "Pay Payment Request" form
3. Enter a consumer wallet ID and click Pay
4. Try paying the same request again — it returns an error (already paid)

**What to observe:**

- Status changes from `pending` → `paid` after payment
- The transfer ID in the paid response links to the underlying transfer
- Payment request list updates after each action
- Paying an already-paid request returns `422 Unprocessable Entity`

**Relationship to kernel**: calls `POST /payment-requests` and
`POST /payment-requests/{id}/pay`, which internally creates a transfer.

---

### Tab 4 — QR

Demonstrates the QR payment loop: generate a QR payload, then pay it.

**Example workflow:**

1. "Generate QR" — enter merchant wallet and amount, click Generate
2. The QR ID auto-fills the "Pay QR" form
3. The `BANZAMI-SBX:` payload string is shown — this is what goes into a real QR image
4. Enter a consumer wallet and click Pay QR
5. Try paying the same QR again — it returns an error (already paid)

**What to observe:**

- The `payload_data` starts with `BANZAMI-SBX:` and is base64-encoded JSON
- Decode it to see the structured QR payload: `qr_id`, `merchant_wallet_id`, `amount_minor`, `currency`
- In production, this string is encoded into an actual QR image by any QR library
- QR codes are single-use — a second payment attempt returns `422`

**Relationship to kernel**: calls `POST /qr` and `POST /qr/{id}/pay`. The QR
payload format is defined in [`contracts/qr/`](../contracts/qr/).

---

### Tab 5 — Ledger

Inspects the double-entry ledger for a specific wallet.

**What to observe:**

- Every transfer creates exactly two ledger entries: DEBIT on sender, CREDIT on receiver
- Enter `sandbox-consumer-1` and `sandbox-merchant-1` to see both sides of a transfer
- DEBIT entries are shown in red with a `−` prefix; CREDIT entries in green with `+`
- The derived balance is computed from entries: `SUM(CREDIT) - SUM(DEBIT)`
- Reference IDs link each entry back to the transfer that created it

**Example:** send a 500.00 AOA transfer from consumer to merchant, then inspect both wallets. You will see:

```
sandbox-consumer-1 ledger:
  DEBIT   − 500.00 AOA   Transfer to sandbox-merchant-1   [txfr-abc]

sandbox-merchant-1 ledger:
  CREDIT  + 500.00 AOA   Transfer from sandbox-consumer-1  [txfr-abc]
```

**Relationship to kernel**: calls `GET /ledger/{wallet_id}`, which derives the
balance from `banza-ledger` entries in real time.

---

### Tab 6 — Settlement

Demonstrates the settlement lifecycle: collect merchant receipts → apply fee → produce a bank reference.

**Example workflow:**

1. Complete two or three transfers to `sandbox-merchant-1`
2. Enter `sandbox-merchant-1` in the Settlement tab and click Create Batch
3. Observe the gross/fee/net breakdown and the `SBX-SETTLE-` provider reference

**What to observe:**

- **Gross**: total of all unsettled inbound transfers for this wallet
- **Fee**: 1% of gross (simulated platform commission), minimum 1.00 AOA
- **Net**: gross minus fee — what the merchant would receive in a real bank transfer
- **Provider ref** (`SBX-SETTLE-{uuid}`): in production this is the bank's transaction reference
- **Status**: always `completed` in the sandbox — in production this could be `pending`
- A transfer can only be settled once; each batch clears the queue

**Relationship to kernel**: calls `POST /settlement/batches`, which invokes
`SettlementExecutionProvider` (simulated) → emits `settlement.created` and
`settlement.completed` events.

---

### Tab 7 — Events

Shows the live SSE event stream and the full event history since startup.

**What to observe:**

**Live stream:** Click **Connect** — a green dot appears. Now perform any action
in another tab (transfer, QR payment, etc.) and watch events appear in real time.
Each event shows its type, full timestamp, correlation IDs, and a collapsible
payload preview.

**History:** All events since the sandbox started, in reverse chronological order.
Each event has a collapsible payload so you can inspect exactly what the kernel emitted.

**Color coding by event type:**

| Colour | Event category |
|--------|---------------|
| Green | `payment.*` |
| Accent (warm) | `wallet.*`, `qr.*` |
| Yellow | `payment_request.*` |
| Cyan | `settlement.*` |

**Relationship to kernel**: live stream uses `GET /events` (SSE via
`tokio::sync::broadcast` + `BroadcastStream`). History uses `GET /events/history`.
In production, these events are delivered as webhooks to merchant backends.

---

## Guided workflows

See [`docs/getting-started.md`](getting-started.md) for step-by-step walkthroughs
of the complete payment flows visible in the demo wallet.
