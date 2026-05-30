# Getting Started with Banza

> The fastest way to understand the Banza financial kernel is to run it.
>
> This guide takes you from zero to executing real payment flows against the local sandbox in under five minutes.

---

## What you are running

The **Banza Sandbox Operator** is a fully local payment server — an HTTP service
on `:3100` that wires the kernel's financial primitives together using simulated
providers. It has no external dependencies.

| Property | Value |
|----------|-------|
| State | In-memory (resets on restart) |
| Database | None required |
| Cloud services | None — all providers are simulated |
| API keys | None required |
| Network | Localhost only |
| Port | 3100 (default) |

Every provider — acquiring, settlement, notifications, routing — is simulated. The
goal is to understand the kernel protocol, not to run production infrastructure.

---

## Requirements

| Tool | Minimum version | Notes |
|------|-----------------|-------|
| Rust toolchain | 1.70+ | Install via [rustup.rs](https://rustup.rs/) |
| Cargo | included with Rust | |
| Git | any | |
| Browser | any modern | For the demo wallet UI |
| Docker | optional | Required only for Option B |

No database. No cloud credentials. No external services.

---

## Step 1 — Clone

```bash
git clone https://github.com/banza-protocol/banzami
cd banzami
```

---

## Step 2 — Run the sandbox

### Option A — Cargo (recommended for kernel development)

```bash
cd reference
cargo run --bin sandbox-operator
```

First run downloads and compiles dependencies (~2 minutes). Subsequent runs start
in under a second. You will see:

```
╔══════════════════════════════════════════════════╗
║  Banzami Sandbox Operator                        ║
║  Local development environment — NOT production  ║
║  simulated=true  production_allowed=false        ║
╚══════════════════════════════════════════════════╝

Providers (all simulated — no external calls):
  acquirer     → FakeAcquirer
  settlement   → SimulatedSettlementProvider
  notifications→ StdoutNotificationProvider

Seed wallets:
  sandbox-consumer-1   (Consumer,    2 000 000 AOA)
  sandbox-merchant-1   (Merchant,   10 000 000 AOA)
  sandbox-government-1 (Government, 50 000 000 AOA)
  sandbox-merchant-2   (Merchant,    5 000 000 AOA)

Listening on http://localhost:3100
```

### Option B — Docker

```bash
cd reference
docker compose up
```

Docker builds from the monorepo root using the multi-stage Dockerfile in
`reference/`. This is slower to build but requires no Rust toolchain.

### Verify

```bash
curl http://localhost:3100/health
```

Expected response:

```json
{
  "status": "ok",
  "environment": "sandbox",
  "simulated": true,
  "production_allowed": false
}
```

---

## Step 3 — Open the demo wallet

The demo wallet is a single HTML file — no build step, no npm, no framework.

```bash
# macOS
open reference/demo-wallet/index.html

# Linux
xdg-open reference/demo-wallet/index.html

# Or: File → Open in any browser
```

The header shows a green dot labelled **sandbox online** once the UI connects to
the operator on `:3100`. You will see four seed wallets with simulated balances
in the **Wallets** tab.

---

## Walkthrough 1 — Send a transfer

A transfer is the canonical operation: move funds from one wallet to another
via a double-entry ledger posting.

**Via demo wallet:**

1. Click the **Transfer** tab
2. From Wallet ID: `sandbox-consumer-1`
3. To Wallet ID: `sandbox-merchant-1`
4. Amount: `50000` (= 500.00 AOA in minor units)
5. Click **Send Transfer**

**Via curl:**

```bash
curl -X POST http://localhost:3100/transfers \
  -H 'Content-Type: application/json' \
  -d '{
    "from_wallet_id": "sandbox-consumer-1",
    "to_wallet_id":   "sandbox-merchant-1",
    "amount_minor":   50000,
    "currency":       "AOA",
    "note":           "hello world"
  }'
```

Response:

```json
{
  "id": "txfr-a1b2c3d4",
  "from_wallet_id": "sandbox-consumer-1",
  "to_wallet_id":   "sandbox-merchant-1",
  "amount_minor":   50000,
  "currency":       "AOA",
  "note":           "hello world",
  "created_at":     "2026-05-28T10:00:00Z"
}
```

**What happened in the kernel:**

1. The ledger posted two entries: DEBIT on `sandbox-consumer-1`, CREDIT on `sandbox-merchant-1`
2. Both entries sum to zero — the double-entry invariant is enforced
3. Balances updated atomically — no partial application
4. Two events emitted: `payment.sent` and `payment.received`

Open the **Ledger** tab and enter `sandbox-consumer-1` to see the debit entry.

**Retry safety — idempotent transfers:**

```bash
curl -X POST http://localhost:3100/transfers \
  -H 'Content-Type: application/json' \
  -d '{
    "from_wallet_id":  "sandbox-consumer-1",
    "to_wallet_id":    "sandbox-merchant-1",
    "amount_minor":    50000,
    "currency":        "AOA",
    "idempotency_key": "my-unique-key-001"
  }'
```

Sending the same `idempotency_key` twice returns the same `id` and makes no
balance change on the second call. This is how the kernel prevents double-charges.

---

## Walkthrough 2 — Payment request lifecycle

A payment request is a pull payment: the merchant creates a request, the consumer
pays it. This models invoice-style or QR-triggered payment flows.

**Via demo wallet:**

1. Click **Payment Request**
2. Under "Create Payment Request":
   - To Wallet: `sandbox-merchant-1`
   - Amount: `25000` (250.00 AOA)
   - Description: `Invoice #001`
3. Click **Create Request** — the ID (e.g. `pr-abc123`) appears in the result
4. The ID auto-fills the "Pay Payment Request" form
5. From Wallet: `sandbox-consumer-1`
6. Click **Pay Request**

**Via curl:**

```bash
# Merchant creates the request
curl -X POST http://localhost:3100/payment-requests \
  -H 'Content-Type: application/json' \
  -d '{
    "to_wallet_id":  "sandbox-merchant-1",
    "amount_minor":  25000,
    "currency":      "AOA",
    "description":   "Invoice #001"
  }'
```

```json
{ "id": "pr-abc123", "status": "pending", "amount_minor": 25000, ... }
```

```bash
# Consumer pays it
curl -X POST http://localhost:3100/payment-requests/pr-abc123/pay \
  -H 'Content-Type: application/json' \
  -d '{"from_wallet_id":"sandbox-consumer-1"}'
```

```json
{ "status": "paid", "transfer_id": "txfr-xyz" }
```

Attempting to pay the same request twice returns `422 Unprocessable Entity` with
`{"error":"already paid"}`. The kernel enforces single-payment semantics.

---

## Walkthrough 3 — QR payment flow

QR codes are how merchants request payment in the physical world. The sandbox
emulates the full generate / scan / pay loop.

**Via demo wallet:**

1. Click **QR**
2. Under "Generate QR":
   - Merchant Wallet: `sandbox-merchant-1`
   - Amount: `30000` (300.00 AOA)
   - Description: `Table 4`
3. Click **Generate QR** — the QR ID fills automatically and the `BANZAMI-SBX:` payload is shown
4. Under "Pay QR":
   - QR Code ID is pre-filled from the generation step
   - Consumer Wallet: `sandbox-consumer-1`
5. Click **Pay QR**

**Via curl:**

```bash
# Merchant generates QR
curl -X POST http://localhost:3100/qr \
  -H 'Content-Type: application/json' \
  -d '{
    "merchant_wallet_id": "sandbox-merchant-1",
    "amount_minor":       30000,
    "currency":           "AOA",
    "description":        "Table 4"
  }'
```

```json
{
  "id":           "qr-abc123",
  "status":       "active",
  "payload_data": "BANZAMI-SBX:eyJzYW5kYm94Ijp0cnVlLCJxcl9pZCI6InFyLWFiYzEyMyIsIm1lcmNoYW50X3dhbGxldF9pZCI6InNhbmRib3gtbWVyY2hhbnQtMSIsImFtb3VudF9taW5vciI6MzAwMDAsImN1cnJlbmN5IjoiQU9BIn0="
}
```

```bash
# Consumer scans and pays
curl -X POST http://localhost:3100/qr/qr-abc123/pay \
  -H 'Content-Type: application/json' \
  -d '{"consumer_wallet_id":"sandbox-consumer-1"}'
```

```json
{ "status": "paid", "transfer_id": "txfr-xyz" }
```

**The `payload_data` field** (`BANZAMI-SBX:{base64}`) is the canonical sandbox QR
payload. In production, this string would be encoded into an actual QR image via any
QR library. The consumer's app decodes the QR, extracts the payload, verifies the
prefix, and initiates payment. See [`contracts/qr/`](../contracts/qr/) for the
production format.

---

## Understanding the event stream

Every kernel action emits an event. Open the **Events** tab in the demo wallet
and click **Connect** to subscribe to the live SSE stream. Then perform any transfer,
payment request, or QR payment in another tab — events appear in real time.

| Event type | Triggered by |
|------------|-------------|
| `wallet.created` | `POST /wallets` |
| `payment.sent` | any transfer (debit side) |
| `payment.received` | any transfer (credit side) |
| `payment_request.created` | `POST /payment-requests` |
| `payment_request.paid` | `POST /payment-requests/{id}/pay` |
| `qr.generated` | `POST /qr` |
| `qr.paid` | `POST /qr/{id}/pay` |
| `settlement.created` | `POST /settlement/batches` |
| `settlement.completed` | same request (instant in sandbox) |

The event stream uses the browser's native `EventSource` API. In a production
operator, these events are delivered via webhooks to merchant backends. See
[`contracts/events/`](../contracts/events/) for the canonical event schema.

Full event history is always available at `GET /events/history`.

---

## Understanding settlement simulation

Settlement converts wallet receipts into bank disbursements. In the real world
this triggers an actual bank transfer. In the sandbox it is instant and always
succeeds.

**Via demo wallet:**

1. First complete at least one transfer to `sandbox-merchant-1`
2. Click **Settlement**
3. Wallet ID: `sandbox-merchant-1`
4. Click **Create Batch**

The result shows:

| Field | Meaning |
|-------|---------|
| `gross_minor` | Total of all unsettled receipts |
| `fee_minor` | 1% simulated platform fee (minimum 1.00 AOA) |
| `net_minor` | What the merchant receives after fee |
| `provider_ref` | `SBX-SETTLE-{uuid}` — simulated bank reference |
| `status` | `completed` — instant in sandbox |

In production the settlement provider triggers a real bank transfer. Here it
always completes immediately and emits `settlement.created` + `settlement.completed`
events.

---

## Walkthrough 4 — Trace your first payment

Every operation in Banza creates a `trace_id` that links the full causal
chain: the originating operation, resulting transfers, ledger postings, events,
and eventual settlement.

### Step 1 — Execute a transfer and capture its trace_id

```bash
curl -s -X POST http://localhost:3100/transfers \
  -H 'Content-Type: application/json' \
  -d '{"from_wallet_id":"sandbox-consumer-1","to_wallet_id":"sandbox-merchant-1","amount_minor":75000,"currency":"AOA"}'
```

The response includes `"trace_id": "tr-..."`. Copy it.

### Step 2 — Inspect the full causal chain

```bash
curl http://localhost:3100/traces/tr-{your-trace-id} | python3 -m json.tool
```

The response contains:

| Section | Contents |
|---------|----------|
| `timeline` | Sorted list of all operations — timestamps, types, summaries |
| `transfers` | The transfer that was executed |
| `ledger_entries` | Both the DEBIT and CREDIT entries |
| `events` | `payment.sent` and `payment.received` events |
| `payment_requests` | Empty — this was a direct transfer |
| `qr_codes` | Empty — this was a direct transfer |

### Step 3 — Trace a QR payment flow

```bash
# Generate QR
QR=$(curl -s -X POST http://localhost:3100/qr \
  -H 'Content-Type: application/json' \
  -d '{"merchant_wallet_id":"sandbox-merchant-1","amount_minor":50000,"currency":"AOA"}')
QR_ID=$(echo $QR | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
QR_TRACE=$(echo $QR | python3 -c "import sys,json; print(json.load(sys.stdin)['trace_id'])")

# Pay QR
curl -X POST http://localhost:3100/qr/$QR_ID/pay \
  -H 'Content-Type: application/json' \
  -d '{"consumer_wallet_id":"sandbox-consumer-1"}'

# Trace the full flow — QR + transfer + ledger + events all in one view
curl http://localhost:3100/traces/$QR_TRACE | python3 -m json.tool
```

This time the trace includes:
- `qr_codes`: the QR code that was generated (status: `paid`)
- `transfers`: the transfer caused by the QR payment (`causation_id === qr_id`)
- `ledger_entries`: both DEBIT and CREDIT entries
- `events`: `qr.generated`, `payment.sent`, `payment.received`, `qr.paid`

### Step 4 — List all traces

```bash
curl http://localhost:3100/traces
```

Returns all distinct `trace_id`s currently in memory. In the demo wallet,
click the **Trace** tab to see the same list with click-to-inspect.

### Identifier reference

| Identifier | Value in QR flow |
|------------|-----------------|
| `trace_id` | Same on: QR code, transfer, both ledger entries, all events |
| `correlation_id` | Transfer: `transfer_id`. Ledger entries: `transfer_id`. Events: `transfer_id`. |
| `causation_id` | Transfer only: `qr_id` — the QR that caused this transfer |

Full tracing documentation: [`docs/observability/financial-tracing.md`](observability/financial-tracing.md)

---

## Next steps

| I want to… | Start here |
|------------|-----------|
| Read the full API docs | [`docs/reference-api.md`](reference-api.md) |
| Understand financial tracing | [`docs/observability/financial-tracing.md`](observability/financial-tracing.md) |
| Understand the kernel crates | [`core/crates/`](../core/crates/) |
| Build a custom provider | [`docs/reference-operator.md`](reference-operator.md) |
| Follow a contributor journey | [`docs/contributor-journeys.md`](contributor-journeys.md) |
| Understand what is stable | [`docs/stability.md`](stability.md) |
| Read the compatibility policy | [`docs/compatibility.md`](compatibility.md) |
| Read architecture decisions | [`docs/adr/`](adr/) |
| Explore protocol RFCs | [`docs/rfc/`](rfc/) |
| Run the mock routing engine | [`reference/mock-routing/`](../reference/mock-routing/) |
