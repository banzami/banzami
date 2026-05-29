# Banzami

**The open financial infrastructure core for programmable instant payments in Angola.**

> "O Banzami constrói a infraestrutura. O Banza é o primeiro produto construído sobre ela."  
> "Banzami builds the infrastructure. Banza is the first product built on top of it."

---

## Start here — run the sandbox

Before touching any crate, reading any ADR, or building any integration:
**run the sandbox operator**.

```bash
git clone https://github.com/banzami/banzami
cd banzami/reference
cargo run --bin sandbox-operator
```

Then open `reference/demo-wallet/index.html` in your browser.

In five minutes you will have executed real wallet transfers, QR payments,
payment requests, settlement batches, and a live event stream — all against
the Banzami financial kernel, with zero cloud infrastructure.

```bash
# Verify the kernel is running
curl http://localhost:3100/health

# Send your first transfer
curl -X POST http://localhost:3100/transfers \
  -H 'Content-Type: application/json' \
  -d '{"from_wallet_id":"sandbox-consumer-1","to_wallet_id":"sandbox-merchant-1","amount_minor":50000,"currency":"AOA"}'
```

Full walkthrough: [`docs/getting-started.md`](docs/getting-started.md)  
Full API reference: [`docs/reference-api.md`](docs/reference-api.md)  
OpenAPI spec: [`contracts/openapi/reference-operator.yaml`](contracts/openapi/reference-operator.yaml)

---

## What is Banzami?

Banzami is the **open-source financial infrastructure kernel** that operators, developers, and fintech builders use to create instant, wallet-native payment networks.

Like Linux for operating systems, like Kubernetes for container orchestration, like PostgreSQL for databases — Banzami is the open foundation that any financial operator can deploy, extend, and build on.

Banzami provides:

- **Financial core crates** (Rust) — double-entry ledger, wallet engine, transaction FSM, settlement, reconciliation, routing, acquiring abstraction, QR runtime, identity
- **Protocol specifications** — QR payload format, webhook schemas, OpenAPI contracts, event schemas
- **Official SDKs** — TypeScript, Python, PHP, Go, Flutter
- **Integration plugins** — generic e-commerce and framework plugins (Laravel, Node.js, PHP, open plugin standard)
- **SDK certification** — test vectors and compliance suite for third-party implementations
- **Architecture documentation** — ADRs, domain models, design principles, sandbox environment

---

## What is Banza?

**Banza is the first commercial operator and product built on Banzami.**

Banza is Angola's instant payment and wallet network — the consumer app, merchant dashboard, QR infrastructure, and payment experience. Banza uses Banzami core crates, conforms to Banzami contracts, and implements Banzami SDKs.

Banza is to Banzami what:
- Ubuntu is to the Linux kernel
- Google Kubernetes Engine is to Kubernetes
- Samsung One UI is to Android AOSP
- A managed Postgres service is to PostgreSQL

The public/private split is **not** language-based. It is:

| Public — Banzami | Private — Banza |
|---|---|
| Generic financial infrastructure | Operator-specific business logic |
| Ledger, wallets, routing, QR engine | EMIS/Multicaixa provider adapters |
| Transaction FSM, settlement model | Production compliance rules |
| SDKs, contracts, protocol specs | Consumer/merchant apps |
| Certification test vectors | Production deployment + infra |
| Reference sandbox | Fraud scoring heuristics |

---

## Ecosystem architecture

```
                    ┌─────────────────────────────┐
                    │          BANZAMI             │
                    │   Open Financial Kernel      │
                    │   Protocol · Core · SDKs     │
                    └─────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼                         ▼                         ▼
 ┌────────────┐          ┌──────────────┐          ┌──────────────┐
 │  Rust Core │          │  Contracts   │          │  SDKs /      │
 │            │          │              │          │  Integrations│
 │  ledger    │          │  OpenAPI     │          │              │
 │  wallets   │          │  Webhooks    │          │  TypeScript  │
 │  qr        │          │  QR spec     │          │  Python      │
 │  routing   │          │  Events      │          │  PHP / Go    │
 │  acquiring │          │  Cert suite  │          │  Flutter     │
 │  ...       │          │              │          │  Plugins     │
 └────────────┘          └──────────────┘          └──────────────┘
                    │                                         │
        ┌───────────┘                         ┌──────────────┘
        ▼                                     ▼
┌──────────────────────┐        ┌──────────────────────────────┐
│        BANZA         │        │          BanzamIA            │
│  First Operator      │        │  Protocol Operating System   │
│                      │        │                              │
│  Consumer app        │        │  16 modules · 3 layers       │
│  Merchant dashboard  │        │  8 capabilities              │
│  EMIS/Multicaixa     │        │  Compreender · Explicar      │
│  QR infrastructure   │        │  Validar · Simular · Prever  │
│  Production infra    │        │  Guiar · Certificar · Federar│
│  L1 Certified        │        │  banzami.org/banzamia        │
└──────────────────────┘        └──────────────────────────────┘
```

---

## BanzamIA — Protocol Operating System

**BanzamIA** is the Protocol Operating System of Banzami — publicly available at `banzami.org/banzamia`.

BanzamIA is not a chatbot. It is an orchestrated AI system that combines multiple language models, live protocol knowledge retrieval, deterministic validation tools, and certification logic into a single interface.

```
Tools determine truth.
AI explains truth.
```

### Model architecture

BanzamIA routes each request to the right combination of model, knowledge source, and tools:

| Task | Model + Tools |
|------|--------------|
| Documentation / Q&A | Qwen + RAG |
| Code generation / SDKs | Qwen Coder + OpenAPI templates |
| Reasoning / architecture / debugging | DeepSeek + RAG |
| Validation (manifest, schema) | Deterministic tools + DeepSeek |
| Certification (operator levels) | Conformance Runner + DeepSeek |
| Trace analysis / audit | Trace Parser + DeepSeek |

**Models:**
- **Qwen** — general protocol understanding, documentation, Q&A, RFC/ADR summarization
- **Qwen Coder** — implementation assistance, SDK snippets, manifest scaffolding
- **DeepSeek** — deep reasoning, invariant debugging, certification analysis, conformance failure explanation

### Deployment modes

| Mode | Status | Description |
|------|--------|-------------|
| `demo` | Available | Frontend-only · static examples · no backend |
| `live-api-no-model` | Active | Real backend · deterministic tools · mock model · no GPU inference |
| `live-ai` | Planned | RunPod / vLLM · Qwen · Qwen Coder · DeepSeek · full model routing |

**Current mode: `live-api-no-model`** — real validation tools, no active GPU inference.

The architecture is designed so that `live-ai` mode can be enabled without redesigning the system. The GPU node handles inference only — protocol data, indexes, and verification remain outside the GPU node.

### Infrastructure

Always-on: BanzamIA API · Qdrant vector store · knowledge index · deterministic tools

GPU inference (planned): RunPod · RTX 4090 · vLLM · Qwen / Qwen Coder / DeepSeek

### Environment variables (live-ai mode)

```env
BANZAMIA_MODE=live-ai            # demo | live-api-no-model | live-ai
BANZAMIA_QDRANT_URL=...          # Qdrant instance URL
BANZAMIA_VLLM_URL=...            # RunPod vLLM endpoint
BANZAMIA_MODEL_QWEN=...          # Qwen model ID
BANZAMIA_MODEL_QWEN_CODER=...    # Qwen Coder model ID
BANZAMIA_MODEL_DEEPSEEK=...      # DeepSeek model ID
```

### Safety constraints

BanzamIA is read-only. It must never:
- Invent certification results or claim regulatory approval
- Bypass conformance or replace deterministic validation
- Expose private operator data or secrets
- Make financial decisions without tool-verified outputs

Access: `banzami.org/banzamia`  
Documentation: `banzami.org/sobre-banzamia`

---

## Repository structure

```
banzami/
├── core/                   Open-source Rust financial infrastructure
│   ├── Cargo.toml          Workspace root
│   ├── crates/
│   │   ├── banzami-types/          Money, Currency, typed IDs
│   │   ├── banzami-ledger/         Double-entry ledger engine
│   │   ├── banzami-wallets/        Merchant wallet engine
│   │   ├── banzami-consumer-wallets/ Consumer wallet engine
│   │   ├── banzami-transactions/   Transaction lifecycle
│   │   ├── banzami-transfers/      P2P wallet transfers
│   │   ├── banzami-qr/             QR code runtime
│   │   ├── banzami-payment-links/  Payment link engine
│   │   ├── banzami-merchants/      Merchant onboarding
│   │   ├── banzami-identity/       @handle identity
│   │   ├── banzami-routing/        Payment rail routing
│   │   ├── banzami-acquiring/      Acquiring abstraction
│   │   ├── banzami-settlement/     Settlement lifecycle
│   │   ├── banzami-reconciliation/ Statement reconciliation
│   │   ├── banzami-risk/           Risk limit framework
│   │   ├── banzami-compliance/     KYC/KYB tracking
│   │   └── banzami-payouts/        Outbound disbursements
│   └── README.md
├── contracts/              Protocol contracts (canonical specs)
│   ├── openapi/            REST API specifications
│   ├── webhooks/           Webhook payload schemas
│   ├── qr/                 QR payload format specification
│   ├── events/             Event schemas
│   └── sdk-certification/  SDK compliance test vectors
├── sdk/                    Official Banzami SDKs
│   ├── typescript/         @banza/sdk
│   ├── python/             banza-python
│   ├── php/                banza/sdk-php
│   ├── go/                 banza-go
│   └── checkout-web/       Browser checkout embed
├── integrations/           Commerce and framework integrations
│   └── plugins/
├── sdk-certification/      Certification test suite and vectors
├── reference/              Local development sandbox (no external infra)
│   ├── sandbox-operator/   In-memory HTTP server on :3100
│   ├── fake-acquirer/      Simulated AcquirerProvider (HMAC-signed, no bank)
│   ├── local-notifications/ StdoutNotificationProvider + NullNotificationProvider
│   ├── simulated-settlement/ SettlementExecutionProvider (always succeeds)
│   └── docker-compose.yml  One-command startup
├── docs/                   Public documentation
│   ├── adr/                Architecture Decision Records
│   ├── architecture/       System design principles
│   ├── core/               Domain documentation (ledger, wallets, QR, ...)
│   └── ...
└── examples/               Reference integrations
```

---

## Sandbox architecture

![Sandbox operator architecture](docs/images/reference/sandbox-architecture.svg)

The sandbox operator wires the Banzami kernel crates together with four simulated
providers (FakeAcquirer, SimulatedSettlement, StdoutNotifications, MockRouting)
and exposes a REST API + SSE event stream on `:3100`. No external services required.

---

## Financial core — quick start

The core is a Rust workspace. Each crate is independently usable.

```toml
[dependencies]
banzami-types  = { git = "https://github.com/banzami/banzami" }
banzami-ledger = { git = "https://github.com/banzami/banzami" }
```

Core financial operation — double-entry ledger transfer:

```rust
use banzami_types::{Money, Currency};
use banzami_ledger::PostingBuilder;

let amount = Money::new(100_000, Currency::AOA); // 1000.00 AOA

let posting = PostingBuilder::new()
    .debit(consumer_account_id, amount.clone())
    .credit(merchant_account_id, amount)
    .idempotency_key("txn_xyz_20260528")
    .build()?;

ledger_engine.post(posting).await?;
```

See [`core/README.md`](core/README.md) for full documentation.

---

## Local sandbox — full feature set

The sandbox operator is the **official local development target** for Banzami.
Run it before touching any kernel crate or building any integration.

```bash
cd reference && cargo run --bin sandbox-operator
# Then: open reference/demo-wallet/index.html
```

**What the sandbox provides:**

| Feature | Endpoint | Status |
|---------|----------|--------|
| Wallet management | `GET/POST /wallets` | Stable |
| P2P transfers (double-entry) | `POST /transfers` | Stable |
| Payment requests (pull payments) | `POST /payment-requests` | Stable |
| QR payment flow | `POST /qr` | Stable |
| Ledger inspection | `GET /ledger/{id}` | Stable |
| Settlement simulation | `POST /settlement/batches` | Stable |
| Live event stream (SSE) | `GET /events` | Stable |
| Financial trace API | `GET /traces/{trace_id}` | Stable |
| Operator manifest | `GET /.well-known/banzami/operator.json` | Experimental |

```bash
# Health check
curl http://localhost:3100/health

# Transfer
curl -X POST http://localhost:3100/transfers \
  -H 'Content-Type: application/json' \
  -d '{"from_wallet_id":"sandbox-consumer-1","to_wallet_id":"sandbox-merchant-1","amount_minor":50000,"currency":"AOA"}'

# Watch events live
curl -N http://localhost:3100/events

# Trace a full payment flow — every reference operation is traceable
TRACE=$(curl -s -X POST http://localhost:3100/transfers \
  -H 'Content-Type: application/json' \
  -d '{"from_wallet_id":"sandbox-consumer-1","to_wallet_id":"sandbox-merchant-1","amount_minor":50000,"currency":"AOA"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['trace_id'])")
curl http://localhost:3100/traces/$TRACE
```

Full docs: [`docs/reference-operator.md`](docs/reference-operator.md) ·
[`docs/reference-api.md`](docs/reference-api.md) ·
[`contracts/openapi/reference-operator.yaml`](contracts/openapi/reference-operator.yaml)

---

## SDKs — quick start

```ts
import { BanzaClient } from '@banza/sdk';

const banza = new BanzaClient({ apiKey: 'sk_sandbox_...', environment: 'sandbox' });

const qr = await banza.qr.generate({
  merchant_id: 'merch_...',
  amount_minor: 50000,  // 500.00 AOA
  currency: 'AOA',
});
```

See [`sdk/`](sdk/) for all languages.

---

## Payment model

Banzami is wallet-native. The canonical operation:

```
Consumer Wallet  ──ledger transfer──▶  Merchant Wallet
```

All surfaces derive from it: QR, @handle, pay links, checkout. Reference models: Pix, UPI, M-Pesa — not card-first.

---

## Financial traceability

Every reference operation is fully traceable across API calls, events, ledger
postings, and simulated settlement.

Three identifiers thread through every operation:

| Identifier | Scope | Purpose |
|------------|-------|---------|
| `trace_id` | Full flow | Shared across the entire payment lifecycle (PR → transfer → ledger → events) |
| `correlation_id` | Current step | Narrows the trace to the current aggregate (changes per layer) |
| `causation_id` | Direct cause | Links a transfer back to the PR or QR that triggered it |

```bash
# After any transfer, QR payment, or payment request — inspect the full causal chain:
curl http://localhost:3100/traces/{trace_id}
```

The response shows a sorted timeline plus typed slices: transfers, ledger entries,
events, payment requests, QR codes, and settlement batches — all linked by `trace_id`.

The demo wallet's **Trace** tab makes this visual: every transfer row, payment
request, settlement batch, and event shows a clickable `trace_id` chip that
opens the full causal chain view.

See [`docs/observability/financial-tracing.md`](docs/observability/financial-tracing.md).

---

## Contracts

All payment protocol specifications live in [`contracts/`](contracts/):

- [OpenAPI specs](contracts/openapi/) — REST API definitions
- [Webhook schemas](contracts/webhooks/) — event payload format and signature spec
- [QR payload format](contracts/qr/) — QR code content specification
- [SDK certification](contracts/sdk-certification/) — compliance test suite

---

## Financial invariants

Every core crate enforces:

- **Double-entry**: every ledger posting sums to zero
- **Immutability**: ledger entries are append-only
- **No negative balance**: wallet available balance cannot go below zero
- **Idempotency**: same key, same result — always
- **Atomicity**: balance changes are transactional

---

## Governance

Protocol changes (contracts, QR spec, webhook schemas) require an Architecture Decision Record and a minimum 7-day review period. See [GOVERNANCE.md](GOVERNANCE.md).

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions welcome to:

- Core Rust crates (ledger, wallets, QR, routing, etc.)
- SDKs (TypeScript, Python, PHP, Go, Flutter)
- Contracts (OpenAPI, webhook schemas, QR spec)
- Integrations (plugins, adapters)
- Documentation and examples

**New contributors:** start with [`docs/getting-started.md`](docs/getting-started.md)
and [`docs/contributor-journeys.md`](docs/contributor-journeys.md).  
**Understand what is stable:** [`docs/stability.md`](docs/stability.md)

---

## Security

Report vulnerabilities to [security@banzami.org](mailto:security@banzami.org). Do not open public issues. See [SECURITY.md](SECURITY.md).

---

## License

- Core crates and contracts: [Apache 2.0](LICENSE)
- SDKs: [Apache 2.0](LICENSE)
- Examples: MIT
- Documentation: Creative Commons CC BY 4.0

---

## Related

- **Banza** — first commercial operator (`github.com/banzami/banza`, private)
- **banzami.org** — public documentation and ecosystem reference
