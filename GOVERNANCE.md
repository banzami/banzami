# Banza Governance

## Overview

BANZA is governed as an **open protocol** — its rules, contracts, and certification framework are defined by the RFC and ADR process, not by any single operator. The governance model separates **protocol decisions** (which affect all operator implementations) from **implementation decisions** (which are internal to each SDK or plugin).

Banzami is the reference operator implementation of the BANZA protocol. It is not the protocol's governing body. No single operator governs the protocol. See [BANZA_REFERENCE.md](BANZA_REFERENCE.md) for the canonical ecosystem hierarchy.

---

## Decision types

### Protocol decisions (ADR required)

Changes to the canonical protocol affect all SDK implementations worldwide and must follow the Architecture Decision Record process:

- Changes to `contracts/openapi/` — API shape changes
- Changes to `contracts/webhooks/` — webhook payload changes
- Changes to `contracts/qr/` — QR payload format changes
- Changes to `contracts/sdk-certification/` — certification vector changes
- New major SDK API surface changes
- Changes to the @handle identity system

**Process:** Open a GitHub Discussion → propose an ADR → review period (minimum 7 days) → merge with ADR.

### Implementation decisions

Improvements within existing protocol bounds (bug fixes, performance, ergonomics):

- SDK implementation details
- Plugin improvements
- Documentation updates
- Example additions

**Process:** Standard pull request review.

---

## Architecture Decision Records

All ADRs live in [`docs/adr/`](docs/adr/). Each ADR must include:

- **Context** — what problem this decision addresses
- **Decision** — what was decided
- **Rationale** — why this decision was made
- **Alternatives considered** — what else was evaluated
- **Consequences** — tradeoffs and downstream effects

ADR numbering is sequential and permanent. ADRs are never deleted — they are superseded by newer ADRs when decisions change.

---

## Versioning policy

Everything published in this repository is part of the **Banza ecosystem contract surface**. Breaking changes affect every SDK implementation worldwide.

### Semantic versioning

| Change type | Version bump | Required |
|---|---|---|
| New feature, backwards compatible | Minor (`x.Y.0`) | No additional process |
| Bug fix, no API change | Patch (`x.y.Z`) | No additional process |
| Breaking API change | Major (`X.0.0`) | ADR required + deprecation notice |

### Breaking change requirements

A breaking change requires:

1. An ADR explaining the change and rationale
2. A **deprecation notice** in the previous minor version
3. A **migration guide** published alongside the new version
4. A minimum **90-day deprecation period** before removal

This applies to: SDKs · QR payload format · webhook schemas · OpenAPI contracts.

### Certification suite stability

The SDK certification vectors (`contracts/sdk-certification/`) are particularly stable. Changes to certification vectors require:

- An ADR
- Coordination with all known SDK implementors
- A transition period where both old and new vectors are accepted

---

## SDK compatibility

Banza maintains a compatibility guarantee for SDK consumers:

- Minor versions are backwards compatible
- Breaking changes require a major version bump, deprecation notice, and migration guide
- The certification suite (`contracts/sdk-certification/`) defines the minimum compatibility bar for any Banza-compatible implementation

Third-party SDK implementations that pass the certification suite are considered **Banza-compatible**.

---

## Ecosystem stewardship

The BANZA protocol is stewarded by its open governance process — RFCs, ADRs, and the certification framework. Protocol evolution decisions are made with the following priorities:

1. **Backwards compatibility** — existing integrations must not break silently
2. **Developer experience** — protocol changes should reduce, not increase, integration complexity
3. **Financial correctness** — any change to payment flows must preserve financial invariants
4. **Security** — security improvements take precedence over API stability

---

## Maintainers

The BANZA protocol is maintained by its core engineering team. External maintainers may be added for specific SDK languages based on demonstrated sustained contribution. Contact: see `docs/governance/` for the full governance framework.

---

## Ecosystem boundaries

### Banza (this repository) — infrastructure layer

| Scope | Examples |
|-------|---------|
| Kernel crates | ledger, wallets, routing, acquiring, settlement, QR |
| Protocol specifications | OpenAPI contracts, webhook schemas, QR payload format |
| Provider trait definitions | `AcquirerProvider`, `SettlementExecutionProvider`, `NotificationProvider` |
| Capability model | `WalletCapabilitySet`, `OperatorManifest`, `ProviderCapabilityDescriptor` |
| Official SDKs | TypeScript, Python, PHP, Go, Flutter |
| Reference implementations | Fake providers, mock routing, local ledger, sandbox operator |
| Certification suite | SDK compliance vectors |
| Governance docs | ADRs, RFCs, this document |

### Operators (external repositories) — implementation layer

| Scope | Examples |
|-------|---------|
| Provider implementations | EMIS acquirer, Multicaixa adapter, real bank settlement |
| Compliance and KYC/AML | Identity verification, risk scoring, fraud detection |
| Consumer and merchant apps | Mobile apps, web dashboards, POS terminals |
| Production deployment | Infrastructure, CI/CD, monitoring, disaster recovery |
| Business logic | Fee structures, credit products, merchant agreements |
| Regulatory obligations | Licensing, reporting, audit trails |

**The kernel never contains operator business logic. Operators never modify kernel
invariants.** This boundary is permanent and enforced by code review.

### Banzami — one operator among many

Banzami is the first commercial operator built on Banza. It is not:

- A privileged operator with special kernel access
- The hidden center of the ecosystem
- The reference for how all operators must work

Banzami implements the same public provider traits as any future operator.
Its private repository contains no code that belongs in the kernel, and the
kernel contains no code specific to Banzami.

---

## RFC process

Significant changes to the Banza protocol go through the RFC process before
implementation. See [`docs/rfc/README.md`](docs/rfc/README.md).

ADRs record decisions after they are made. RFCs propose changes before they are made.

---

## Contact

- Protocol questions: open a GitHub Discussion
- RFC proposals: open a PR to `docs/rfc/`
- Security issues: security@banzami.org (see [SECURITY.md](SECURITY.md))
- Code of conduct: conduct@banzami.org
