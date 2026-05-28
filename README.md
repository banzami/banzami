# Banzami

**Open-source programmable payments infrastructure for Angola.**

> "O Banzami constrói a infraestrutura. O Banza é o primeiro produto construído sobre ela."  
> "Banzami builds the infrastructure. Banza is the first product built on top of it."

---

## Vision

Angola's digital economy runs on cash and manual bank transfers. A merchant receives a payment proof via WhatsApp. A taxi driver waits for a transfer confirmation before releasing a ride. A donation platform cannot collect money programmatically.

Banzami exists to eliminate this friction — by providing open, programmable payment infrastructure that any Angolan application can integrate in hours.

The target experience: **`SCAN QR → CONFIRM → PAID INSTANTLY`**

---

## What is Banzami?

Banzami is an **open-source programmable payments ecosystem** — the infrastructure layer that developers, merchants, and fintech builders use to create instant, wallet-native payment experiences in Angola.

Banzami provides:

- **Protocol specifications** — QR payment payload format, webhook schemas, OpenAPI contracts, event schemas
- **Official SDKs** — TypeScript, Python, PHP, Go, Flutter
- **Integration plugins** — Laravel, Node.js, PHP generic adapters, WooCommerce, Shopify
- **SDK certification** — test vectors and compliance suite for third-party SDK implementations
- **Architecture documentation** — ADRs, domain models, design principles, sandbox environment

Banzami is **not a company product**. It is the ecosystem, the protocol, and the SDK layer that any developer or company can build on.

---

## What is Banza?

**Banza is the first commercial implementation built on Banzami.**

Banza is Angola's instant payment and wallet network — the consumer app, merchant dashboard, QR infrastructure, and payment experience. Banza uses the Banzami SDKs, conforms to the Banzami contracts, and implements the Banzami protocol.

The distinction:

| | Banzami | Banza |
|---|---|---|
| **Type** | Open-source infrastructure | Commercial fintech product |
| **Role** | Ecosystem, protocol, SDKs | Wallet, payments, consumer app |
| **Audience** | Developers, SDK users, integrators | Consumers, merchants, businesses |
| **Repository** | `github.com/banzami/banzami` (public) | `github.com/banzami/banza` (private) |
| **Website** | `banzami.org` | `banza.ao` |

Think of it like: Linux → Ubuntu · Ethereum → MetaMask · Pix standard → banking apps.

---

## Ecosystem architecture

```
                    ┌─────────────────────────────┐
                    │          BANZAMI             │
                    │   Open-source Infrastructure │
                    │   Protocol · SDKs · Specs    │
                    └─────────────────────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
   ┌─────────────┐       ┌──────────────┐       ┌──────────────┐
   │  SDKs/APIs  │       │  Contracts   │       │ Integrations │
   │             │       │              │       │              │
   │ TypeScript  │       │  OpenAPI     │       │  WooCommerce │
   │ Python      │       │  Webhooks    │       │  Shopify     │
   │ PHP         │       │  QR spec     │       │  Laravel     │
   │ Go          │       │  Events      │       │  Node.js     │
   │ Flutter     │       │  Cert suite  │       │  PHP generic │
   └─────────────┘       └──────────────┘       └──────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │            BANZA             │
                    │     Commercial Product       │
                    │  Wallet · QR · Merchant app  │
                    └─────────────────────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    ▼                            ▼
           Consumer wallet              Merchant dashboard
           @handle payments             QR generation
           Pay links                   Instant settlement
           Instant transfers           Payout management
```

---

## Payment model

Banzami is wallet-native. The canonical payment operation is:

```
Consumer Wallet  ──ledger transfer──▶  Merchant Wallet
```

All payment surfaces derive from this:

- **QR payment** — encodes amount + merchant wallet → consumer scans → ledger transfer
- **@handle transfer** — consumer-to-consumer wallet transfer via handle lookup
- **Pay link** — pre-configured URL → resolves to ledger transfer
- **Checkout embed** — hosted checkout widget → same ledger transfer at resolution

Reference models: Pix (Brazil), UPI (India), M-Pesa (East Africa). Not card-first, not Stripe-style.

---

## Repository structure

```
banzami/
├── contracts/              Protocol contracts (canonical specs)
│   ├── openapi/            REST API specifications
│   ├── webhooks/           Webhook payload schemas
│   ├── qr/                 QR payload format specification
│   ├── events/             Internal event schemas
│   └── sdk-certification/  SDK compliance test vectors
├── sdk/                    Official Banzami SDKs
│   ├── typescript/         @banza/sdk — Node.js and browser
│   ├── python/             banza-python
│   ├── php/                banza/sdk-php
│   ├── go/                 banza-go
│   └── checkout-web/       Browser checkout embed
├── integrations/           Commerce and framework integrations
│   └── plugins/            WooCommerce, Shopify, Laravel, Node.js, PHP
├── sdk-certification/      Certification test suite and vectors
├── docs/                   Public documentation
│   ├── adr/                Architecture Decision Records
│   ├── architecture/       System design principles
│   ├── api/                API reference
│   ├── sandbox/            Sandbox environment guide
│   ├── domains/            Domain model documentation
│   └── standards/          Protocol standards
├── examples/               Reference integrations and usage examples
└── assets/                 Brand assets and logos
```

---

## SDKs

| Language | Package | Server / Client |
|---|---|---|
| TypeScript / Node.js | `@banza/sdk` | Server |
| Python | `banza-python` | Server |
| PHP | `banza/sdk-php` | Server |
| Go | `banza-go` | Server |
| Flutter | `banza_sdk` | Client |
| Browser checkout embed | `@banza/checkout-web` | Client |

All SDKs provide: typed APIs · environment isolation (sandbox/live) · automatic idempotency · retries with backoff · webhook signature verification · QR helpers · structured error hierarchy.

### Quick start — TypeScript

```ts
import { BanzaClient } from '@banza/sdk';

const banza = new BanzaClient({
  apiKey: 'sk_sandbox_...',
  environment: 'sandbox',
});

// Create a payment intent
const intent = await banza.paymentIntents.create({
  amount_minor: 100000, // 1000.00 AOA
  currency: 'AOA',
  recipient: '@joao',
});

// Generate a QR code
const qr = await banza.qr.generate({
  merchant_id: 'merch_...',
  amount_minor: 50000,
  currency: 'AOA',
  reference: 'order_123',
});
```

### Quick start — Python

```python
from banza import BanzaClient

banza = BanzaClient(api_key="sk_sandbox_...", environment="sandbox")

intent = banza.payment_intents.create(
    amount_minor=100000,
    currency="AOA",
    recipient="@joao",
)
```

---

## Contracts

All payment protocol specifications live in [`contracts/`](contracts/). External implementations must conform to these contracts to be considered Banzami-compatible.

- [OpenAPI specs](contracts/openapi/) — REST API definitions for all endpoints
- [Webhook schemas](contracts/webhooks/) — event payload format and signature spec
- [QR payload format](contracts/qr/) — QR code content specification
- [SDK certification vectors](contracts/sdk-certification/) — compliance test suite

---

## Integrations

Commerce platform plugins in [`integrations/plugins/`](integrations/plugins/):

| Plugin | Platform |
|---|---|
| `woocommerce/` | WooCommerce (WordPress) |
| `shopify/` | Shopify |
| `generic-laravel/` | Laravel / PHP framework |
| `generic-node/` | Node.js / Express |
| `generic-php/` | PHP (framework-agnostic) |

---

## Governance

Banzami uses **Architecture Decision Records (ADRs)** for all protocol and ecosystem decisions. ADRs live in [`docs/adr/`](docs/adr/) and are permanent — never deleted, only superseded.

**Protocol changes** (contracts, webhook schemas, QR spec) require an ADR:
1. Open a GitHub Discussion
2. Propose an ADR
3. Minimum 7-day review period
4. Merge with ADR

**Implementation changes** (SDK improvements, bug fixes, docs) follow standard pull request review.

See [GOVERNANCE.md](GOVERNANCE.md) for the full governance model.

---

## Versioning policy

Everything in this repository is part of the **Banzami ecosystem contract surface**. Breaking changes affect every SDK implementation worldwide.

- Minor versions are backwards compatible
- Breaking changes require a **major version bump + deprecation notice + migration guide**
- The certification suite (`contracts/sdk-certification/`) defines the minimum compatibility bar

This applies to: SDKs · QR specs · webhook schemas · OpenAPI contracts.

---

## Contributing

Contributions are welcome to SDKs, contracts, documentation, and integrations.

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

What you can contribute to:

| Area | Examples |
|---|---|
| SDKs | Bug fixes, new language features, better error messages, test coverage |
| Contracts | OpenAPI corrections, webhook schema improvements, QR spec clarifications |
| Documentation | Translations, examples, guides |
| Integrations | New framework plugins, commerce platform adapters |
| SDK certification | New test vectors, edge case coverage |

---

## Security

To report a vulnerability, **do not open a public issue**. Email [security@banzami.org](mailto:security@banzami.org).

See [SECURITY.md](SECURITY.md) for the full responsible disclosure policy.

---

## License

- SDKs and contracts: [Apache 2.0](LICENSE)
- Examples: MIT
- Documentation: Creative Commons CC BY 4.0

---

## Reference document

[`docs/BANZAMI_REFERENCE.md`](docs/BANZAMI_REFERENCE.md) is the canonical reference for the entire Banzami ecosystem — product definition, architecture, payment philosophy, UX principles, SDK policy, and brand guidelines.

---

## Long-term ecosystem vision

Banzami's goal is to become the open standard for instant, wallet-native payments in Angola — and eventually across the Lusophone African market.

The network grows through:
- **Merchants** adopting QR payment infrastructure
- **Developers** integrating Banza SDKs into Angolan applications
- **Third-party implementations** building on Banzami contracts and certification
- **Ecosystem partners** creating new products on the same open infrastructure

Any company, developer, or application can build on Banzami. Banza is the first — not the only.

---

## Related

- **Banza** — first commercial implementation (`github.com/banzami/banza`, private)
- **banzami.org** — public documentation and ecosystem reference
