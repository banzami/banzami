# Banza Governance

## Overview

BANZA is governed as an **open protocol** — its rules, contracts, and certification framework are defined by the RFC and ADR process, not by any single operator. The governance model separates **protocol decisions** (which affect all operator implementations) from **implementation decisions** (which are internal to each SDK or plugin).

## Operator Independence

**An operator is an independent commercial entity.** It is not the protocol's governing body. Key facts:

- BANZA is **not owned by the reference operator**
- BANZA is **not governed by the reference operator**
- the reference operator does **not control** the certification framework
- the reference operator is **not part of** the BANZA protocol organization (`github.com/banza-protocol`)
- Um operador operates at `github.com/banza` and `banza.network`
- the reference operator may contribute to BANZA via the ADR process, like any other operator
- The BANZA protocol continues to exist if the reference operator ceases operations

**No single operator governs the protocol.** See [BANZA_REFERENCE.md](BANZA_REFERENCE.md) for the canonical ecosystem hierarchy.

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

### Operators — independent participants in the protocol

A certified operator built on Banza. It is not:

- A privileged operator with special kernel access
- The hidden center of the ecosystem
- The reference for how all operators must work

the reference operator implements the same public provider traits as any future operator.
Its private repository contains no code that belongs in the kernel, and the
kernel contains no code specific to operador.

---

## RFC process

Significant changes to the Banza protocol go through the RFC process before
implementation. See [`docs/rfc/README.md`](docs/rfc/README.md).

ADRs record decisions after they are made. RFCs propose changes before they are made.

---

## Contact

- Protocol questions: open a GitHub Discussion
- RFC proposals: open a PR to `docs/rfc/`
- Security issues: security@banza.network (see [BANZA_SECURITY.md](BANZA_SECURITY.md))
- Code of conduct: conduct@banza.network

---

## Operator Neutrality Principle

Operator neutrality is an **architectural invariant** of BANZA — not a style preference, not a branding policy.

### Architectural dependency

```
     Operators   (Operator A, Operator B, Operator C, ...)
         ↑
       BanzAI    (Protocol Operating System)
         ↑
       BANZA     (this repository — the protocol itself)
```

Operators build on BANZA and BanzAI. The arrows point upward. BANZA never has a downward dependency on any specific operator.

### What this means in practice

**BANZA defines:**
- Protocol rules and invariants (INV-LEDGER-*, INV-WALLET-*, INV-QR-*, ...)
- Contract specifications (OpenAPI, webhook schemas, event envelopes)
- Conformance criteria (what counts as a passing conformance test)
- Certification levels (L0–L4, applicable to any operator)
- Federation protocol (any certified operator may participate)
- Governance process (ADRs and RFCs — open to contributions from any operator)

**BANZA must never contain:**
- Specific operator brands, names, or domains
- Operator business logic (pricing models, product decisions)
- Operator ownership or governance claims over the protocol
- Certification rules or conformance tests written for one specific operator
- Assumptions that only a single operator exists or will ever exist
- Protocol extensions that only apply to one operator's product

### Violations

Any content that implies a specific operator has governance authority over BANZA is a protocol contamination:

| Forbidden pattern | Why it is wrong |
|-------------------|-----------------|
| `[Operator X] governs BANZA` | BANZA is governed by the ADR/RFC process |
| `[Operator X] defines the protocol` | BANZA defines the protocol |
| `[Operator X] certifies operators` | BANZA certification is operator-agnostic |
| `[Operator X]-specific extension` | Extensions belong in the operator's own repository |
| `[Operator X] is required for BANZA` | No operator is required; any operator may implement |

### Automated Enforcement

**Rule:** No specific commercial operator brand may appear in the BANZA repository.

BANZA is an open protocol. Any operator may build on it. No single operator's name, domain, or brand belongs in the protocol specifications, kernel, SDKs, contracts, conformance tests, or documentation.

**Enforcement mechanism:**

| Check | Command | Trigger |
|-------|---------|---------|
| Local | `make identity-check` | Before every commit |
| CI | `identity-guard` workflow | Every push and pull request |
| Pre-commit | `scripts/check-operator-contamination.sh --staged` | Optional pre-commit hook |

**Replacement vocabulary:**

| Forbidden | Use instead |
|-----------|-------------|
| *(specific operator brand)* | certified operator |
| *(specific operator brand)* | reference operator |
| *(specific operator brand)* | operator implementation |
| *(specific operator brand)* | federation member |

Violations fail both local checks and CI. No PR that introduces an operator brand can be merged.
