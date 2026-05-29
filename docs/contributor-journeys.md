# Contributor Journeys

This document maps common contributor goals to the specific crates, files,
reference flows, and relevant design docs involved.

**Start every journey by running the sandbox:**

```bash
cd reference && cargo run --bin sandbox-operator
open reference/demo-wallet/index.html
```

The sandbox gives you a running system to observe, test against, and break safely.

---

## Journey 1 — "I want to improve the ledger"

**Goal:** Modify or extend double-entry ledger behaviour in `banzami-ledger`.

### Where to start

1. Read the ledger invariants in [`docs/core/ledger.md`](core/ledger.md)
2. Read [`docs/adr/ADR-002-ledger-immutability.md`](adr/ADR-002-ledger-immutability.md)
3. Read [`core/crates/banzami-ledger/src/lib.rs`](../core/crates/banzami-ledger/src/lib.rs)

### Crates involved

| Crate | Role |
|-------|------|
| `banzami-ledger` | Primary — posting engine, entry types, balance derivation |
| `banzami-types` | `Money`, `Currency`, `AccountId` types used throughout |
| `banzami-transfers` | Calls the ledger to post transfer entries |
| `local-ledger` | SQLite reference implementation in `reference/` |

### Reference flows

Run a transfer and watch it in the ledger:

```bash
# Trigger a transfer
curl -X POST http://localhost:3100/transfers \
  -H 'Content-Type: application/json' \
  -d '{"from_wallet_id":"sandbox-consumer-1","to_wallet_id":"sandbox-merchant-1","amount_minor":50000,"currency":"AOA"}'

# Inspect the ledger
curl http://localhost:3100/ledger/sandbox-consumer-1
curl http://localhost:3100/ledger/sandbox-merchant-1
```

The sandbox also has the **Ledger tab** in the demo wallet, which shows you
double-entry postings visually.

### Key invariants (must remain true after any change)

- Every posting must sum to zero (DEBIT + CREDIT = 0)
- Entries are append-only — no updates or deletions
- `derived_balance = SUM(CREDIT) - SUM(DEBIT)` always
- Same `idempotency_key` → same result, no double-posting

### Relevant ADRs and stability

- ADR-002: Ledger immutability
- ADR-010: Idempotency model
- **Stability level:** `STABLE` — changes require 90-day deprecation + ADR

---

## Journey 2 — "I want to build a QR plugin"

**Goal:** Build a custom QR payment integration against the kernel's QR runtime.

### Where to start

1. Read the QR payload spec in [`contracts/qr/`](../contracts/qr/)
2. Read [`core/crates/banzami-qr/src/lib.rs`](../core/crates/banzami-qr/src/lib.rs)
3. Explore the QR flow in the sandbox

### Crates involved

| Crate | Role |
|-------|------|
| `banzami-qr` | QR payload encoding, QR code lifecycle (active → paid) |
| `banzami-types` | `Money`, `Currency` |
| `banzami-transactions` | Transaction FSM triggered on QR payment |

### Reference flow — full QR lifecycle

```bash
# Generate QR
curl -X POST http://localhost:3100/qr \
  -H 'Content-Type: application/json' \
  -d '{"merchant_wallet_id":"sandbox-merchant-1","amount_minor":30000,"currency":"AOA"}'
# → {"id":"qr-abc","payload_data":"BANZAMI-SBX:eyJ..."}

# The payload_data decodes to:
# {"sandbox":true,"qr_id":"qr-abc","merchant_wallet_id":"sandbox-merchant-1","amount_minor":30000,"currency":"AOA"}

# Consumer pays
curl -X POST http://localhost:3100/qr/qr-abc/pay \
  -H 'Content-Type: application/json' \
  -d '{"consumer_wallet_id":"sandbox-consumer-1"}'
# → {"status":"paid","transfer_id":"txfr-xyz"}

# Watch the events
curl http://localhost:3100/events/history | jq '.events[] | select(.event_type | startswith("qr"))'
```

In production, the `payload_data` string encodes into a real QR image.
The consumer app decodes the QR, reads the `BANZAMI:` prefix, parses the JSON,
and calls the operator's payment endpoint.

### Relevant design docs

- [`contracts/qr/`](../contracts/qr/) — canonical payload format spec
- RFC-0003 — wallet capability flags including `qr_payments`
- **Stability level:** QR payload format is `STABLE`. Internal QR engine details are `INTERNAL`.

---

## Journey 3 — "I want to experiment with routing"

**Goal:** Understand or modify payment rail routing behaviour.

### Where to start

1. Read [`docs/core/routing.md`](core/routing.md) if it exists, otherwise start with the crate
2. Read [`core/crates/banzami-routing/src/lib.rs`](../core/crates/banzami-routing/src/lib.rs)
3. Read the mock routing implementations in [`reference/mock-routing/`](../reference/mock-routing/)

### Crates involved

| Crate | Role |
|-------|------|
| `banzami-routing` | `RoutingEngine` trait, `RoutingRule`, `RailDecision` |
| `mock-routing` | Three test implementations: normal, failing, degraded |
| `banzami-types` | `Money`, `Currency`, `PaymentRail` |

### Reference implementations

The `reference/mock-routing/` crate provides three `RoutingEngine` implementations
you can use as templates:

```rust
// Routes normally, logs every decision
MockRoutingEngine::new(config)

// Always returns NoEligibleRail
FailingRoutingEngine

// Always returns AllRailsDegraded
DegradedRoutingEngine
```

To test routing failure handling:
- Swap `SandboxRoutingEngine` for `FailingRoutingEngine` in `sandbox-operator/src/state.rs`
- Run transfers and observe the error responses
- Watch the event stream — no `payment.sent` events should appear

### Relevant design docs

- RFC-0001 — multi-operator routing (experimental)
- **Stability level:** `RoutingEngine` trait is `STABLE`. Mock implementations are `INTERNAL`.

---

## Journey 4 — "I want to build a wallet UI"

**Goal:** Build a consumer or merchant UI that talks to a Banza operator API.

### Where to start

1. Read [`docs/reference-api.md`](reference-api.md)
2. Read [`contracts/openapi/reference-operator.yaml`](../contracts/openapi/reference-operator.yaml)
3. Read the demo wallet source at [`reference/demo-wallet/index.html`](../reference/demo-wallet/index.html)

### The demo wallet as a template

The demo wallet is a minimal but complete example of a UI talking to the
sandbox operator. It covers:

- Wallet listing and balance display (`GET /wallets`)
- Transfer execution with idempotency keys
- Payment request creation and payment
- QR code generation and payment
- Ledger entry inspection
- Settlement batch creation
- SSE event stream subscription

Use it as a starting point — copy patterns you need, ignore the rest.
The entire UI is in one HTML file with no build step.

### SDK option

For a real UI, use the TypeScript SDK instead of raw `fetch()` calls:

```ts
import { BanzaClient } from '@banza/sdk';
const client = new BanzaClient({ baseUrl: 'http://localhost:3100' });
const wallets = await client.wallets.list();
```

See [`sdk/typescript/`](../sdk/typescript/) for the SDK.

### Key patterns to know

- All monetary values are **minor units** — display by dividing by 100
- The event stream (`GET /events`) lets the UI react to server-side state changes
- Idempotency keys protect against double-submit on transfers
- Wallet balances should be refreshed after any transfer or QR payment

### Relevant design docs

- [`docs/getting-started.md`](getting-started.md) — workflow walkthroughs
- RFC-0003 — wallet capability flags (what can each wallet type do?)

---

## Journey 5 — "I want to add a provider"

**Goal:** Implement a custom `AcquirerProvider`, `SettlementExecutionProvider`,
`NotificationProvider`, or `RoutingEngine` for use in an operator.

### Where to start

1. Identify which provider interface you are implementing
2. Read the trait definition in the relevant kernel crate
3. Read the reference implementation for that provider type
4. Read [`docs/reference-operator.md`](reference-operator.md) — "Writing your own operator"

### Provider trait locations

| Provider | Trait location | Reference implementation |
|----------|----------------|-------------------------|
| Acquirer | `banzami-acquiring` | `reference/fake-acquirer/` |
| Settlement | `banzami-settlement` | `reference/simulated-settlement/` |
| Notifications | `banzami-notifications` | `reference/local-notifications/` |
| Routing | `banzami-routing` | `reference/mock-routing/` |

### Implementation pattern

Every provider follows the same pattern:

```rust
// 1. The kernel defines the trait
pub trait AcquirerProvider: Send + Sync {
    async fn initiate_payment(&self, req: InitiatePaymentRequest)
        -> Result<PaymentInitiation, AcquirerError>;
    async fn validate_callback(&self, raw: &[u8], sig: &str)
        -> Result<AcquirerCallback, AcquirerError>;
}

// 2. Your production impl
pub struct EmisAcquirer { /* EMIS credentials, HTTP client */ }
impl AcquirerProvider for EmisAcquirer { /* real EMIS API calls */ }

// 3. The sandbox impl (in reference/)
pub struct FakeAcquirer;
impl AcquirerProvider for FakeAcquirer { /* HMAC-signed fake responses */ }

// 4. The kernel engine is generic over the provider
pub struct AcquiringEngine<P: AcquirerProvider> { provider: P }
```

### Testing your provider

1. Write unit tests for the provider in isolation
2. Plug it into `reference/sandbox-operator/src/state.rs` temporarily
3. Run the sandbox and verify the full transfer flow works end-to-end
4. Run `cargo test --workspace` from `reference/`

### Relevant design docs

- [`docs/reference-operator.md`](reference-operator.md)
- ADR-021: Provider abstraction model
- ADR-019: Operator separation rationale
- **Stability level:** Provider trait interfaces are `STABLE`

---

## Journey 6 — "I want to test settlement"

**Goal:** Understand, test, or extend settlement behaviour.

### Where to start

1. Read [`core/crates/banzami-settlement/src/lib.rs`](../core/crates/banzami-settlement/src/lib.rs)
2. Read [`reference/simulated-settlement/src/lib.rs`](../reference/simulated-settlement/src/lib.rs)
3. Run the full settlement flow in the sandbox

### Reference flow — complete settlement lifecycle

```bash
# Step 1: Generate some merchant receipts
curl -X POST http://localhost:3100/transfers \
  -H 'Content-Type: application/json' \
  -d '{"from_wallet_id":"sandbox-consumer-1","to_wallet_id":"sandbox-merchant-1","amount_minor":100000,"currency":"AOA"}'

curl -X POST http://localhost:3100/transfers \
  -H 'Content-Type: application/json' \
  -d '{"from_wallet_id":"sandbox-consumer-1","to_wallet_id":"sandbox-merchant-1","amount_minor":50000,"currency":"AOA"}'

# Step 2: Create settlement batch
curl -X POST http://localhost:3100/settlement/batches \
  -H 'Content-Type: application/json' \
  -d '{"wallet_id":"sandbox-merchant-1"}'
# → {"gross_minor":150000,"fee_minor":1500,"net_minor":148500,"provider_ref":"SBX-SETTLE-..."}

# Step 3: Observe settlement events
curl http://localhost:3100/events/history | jq '.events[] | select(.event_type | startswith("settlement"))'

# Step 4: Inspect the ledger after settlement
curl http://localhost:3100/ledger/sandbox-merchant-1
```

### Key concepts

- **Gross**: sum of all unsettled inbound transfers
- **Fee**: platform commission (1% in sandbox, minimum 1.00 AOA)
- **Net**: gross minus fee — what the merchant receives
- **Provider ref**: the simulated bank reference (`SBX-SETTLE-{uuid}` in sandbox)
- **Idempotency**: a transfer can only be settled once — the sandbox tracks settled IDs

### RFC-0002 and cross-operator settlement

Cross-operator settlement (RFC-0002) extends this model to handle obligations
between two different operators. See [`docs/rfc/RFC-0002-cross-operator-settlement.md`](rfc/RFC-0002-cross-operator-settlement.md).

### Relevant design docs

- RFC-0002: Cross-operator settlement
- **Stability level:** `SettlementExecutionProvider` trait is `STABLE`. Settlement fee model is `INTERNAL`.

---

## Common patterns across all journeys

### Always run the sandbox first

Before touching any kernel crate, reproduce the flow you want to change in the
sandbox. This lets you observe the current behaviour and verify your change
doesn't break it.

### Check the invariants

Every financial crate has documented invariants. Your change must leave all
invariants intact. See [`docs/stability.md`](stability.md) for which invariants
are stability-guaranteed.

### Use the event stream as your audit trail

Connect to `GET /events` via SSE before triggering any operation. The event
stream shows you exactly what the kernel emitted — useful for debugging and
for understanding what a production operator would receive via webhooks.

### Write a test against the sandbox router

The sandbox router can be tested without a running server:

```rust
use tower::ServiceExt;
use sandbox_operator::build_router;

#[tokio::test]
async fn my_test() {
    let app = build_router();
    let res = app.oneshot(/* request */).await.unwrap();
    assert_eq!(res.status(), StatusCode::OK);
}
```

See [`reference/sandbox-operator/tests/integration.rs`](../reference/sandbox-operator/tests/integration.rs) for 17 working examples.
