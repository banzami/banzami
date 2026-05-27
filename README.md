# Banzami

**Open-source programmable payments infrastructure for Angola.**

> "O Banzami constrói a infraestrutura. O Banza move o dinheiro."  
> "Banzami builds the infrastructure. Banza moves the money."

---

## What is Banzami?

Banzami is the open-source foundation for building instant, wallet-native payment experiences in Angola.

It provides:

- **Protocol specifications** — QR payment payload format, webhook schemas, OpenAPI contracts, event schemas
- **Official SDKs** — TypeScript, Python, PHP, Go, Flutter runtime
- **Integration plugins** — Laravel, Node.js, PHP generic adapters
- **SDK certification** — test vectors and compliance suite for third-party implementations
- **Architecture documentation** — ADRs, domain models, design principles

Banzami is NOT the commercial product. It is the ecosystem, the protocol, and the SDK layer that any developer or company can build on.

The first commercial implementation built on Banzami is **Banza** — Angola's instant payment and wallet network.

---

## Repository structure

```
banzami/
├── contracts/          Protocol contracts (OpenAPI, webhooks, QR, events)
│   ├── openapi/        REST API specifications
│   ├── webhooks/       Webhook payload schemas
│   ├── qr/             QR payload format specification
│   ├── events/         Internal event schemas
│   └── sdk-certification/  SDK compliance test vectors
├── sdk/                Official Banzami SDKs
│   ├── typescript/     @banza/sdk — Node.js and browser
│   ├── python/         banza-python
│   ├── php/            banza/sdk-php
│   ├── go/             banza-go
│   └── checkout-web/   Browser checkout embed
├── integrations/       Commerce and framework integrations
│   └── plugins/        Laravel, Node.js, PHP generic plugins
├── docs/               Public documentation
│   ├── adr/            Architecture Decision Records
│   ├── architecture/   System design principles
│   ├── api/            API reference
│   ├── sandbox/        Sandbox environment guide
│   └── standards/      Protocol standards (webhook signatures, etc.)
├── examples/           Reference integrations and usage examples
└── tools/              Developer tooling
```

---

## Core principles

- **Wallet-native** — every account is a wallet, every payment is a wallet transfer
- **QR-first** — QR codes are the primary payment initiation mechanism
- **@handle identity** — payments addressed to human-readable handles
- **Instant by default** — all payment experiences target under 2 seconds
- **Angola-first** — optimized for Angolan consumers, merchants, and Kwanza (AOA)

---

## Payment model

```
Consumer Wallet  ──ledger transfer──▶  Merchant Wallet
```

This is the canonical payment operation. QR, @handle, pay links, and checkout all derive from it.

---

## SDKs

| Language | Package | Status |
|---|---|---|
| TypeScript / Node.js | `@banza/sdk` | Available |
| Python | `banza-python` | Available |
| PHP | `banza/sdk-php` | Available |
| Go | `banza-go` | Available |
| Flutter (runtime) | `banza_sdk` | Available |
| Browser (checkout embed) | `@banza/checkout-web` | Available |

---

## Quick start

### TypeScript

```ts
import { BanzaClient } from '@banza/sdk';

const banza = new BanzaClient({
  apiKey: 'sk_sandbox_...',
  environment: 'sandbox',
});

const transfer = await banza.transfers.create({
  recipient: '@joao',
  amount_minor: 100000, // 1000.00 AOA
  currency: 'AOA',
});
```

### Python

```python
from banza import BanzaClient

banza = BanzaClient(api_key="sk_sandbox_...", environment="sandbox")

transfer = banza.transfers.create(
    recipient="@joao",
    amount_minor=100000,
    currency="AOA",
)
```

---

## Contracts

All payment protocol specifications live in [`contracts/`](contracts/). External implementations must conform to these contracts to be considered Banzami-compatible.

- [OpenAPI specs](contracts/openapi/) — REST API definitions
- [Webhook schemas](contracts/webhooks/) — event payload formats
- [QR payload format](contracts/qr/) — QR code content specification
- [SDK certification vectors](contracts/sdk-certification/) — compliance test suite

---

## Contributing

We welcome contributions to SDKs, contracts, documentation, and integrations.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Governance

Banzami follows a structured Architecture Decision Record (ADR) process for all protocol and ecosystem decisions. See [`docs/adr/`](docs/adr/).

See [GOVERNANCE.md](GOVERNANCE.md) for the full governance model.

---

## License

- SDKs and contracts: [Apache 2.0](LICENSE)
- Examples: MIT
- Documentation: Creative Commons CC BY 4.0

---

## Related

- **Banza** — the first commercial implementation of Banzami (`github.com/banzami/banza`, private)
- **banzami.org** — public documentation website
