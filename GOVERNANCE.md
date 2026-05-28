# Banzami Governance

## Overview

Banzami is governed by Banzami (the organization) and maintained as an open-source ecosystem project. The governance model separates **protocol decisions** (which affect all implementations) from **implementation decisions** (which are internal to each SDK or plugin).

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

Everything published in this repository is part of the **Banzami ecosystem contract surface**. Breaking changes affect every SDK implementation worldwide.

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

Banzami maintains a compatibility guarantee for SDK consumers:

- Minor versions are backwards compatible
- Breaking changes require a major version bump, deprecation notice, and migration guide
- The certification suite (`contracts/sdk-certification/`) defines the minimum compatibility bar for any Banzami-compatible implementation

Third-party SDK implementations that pass the certification suite are considered **Banzami-compatible**.

---

## Ecosystem stewardship

The Banzami protocol is stewarded by Banzami (the organization). Protocol evolution decisions are made with the following priorities:

1. **Backwards compatibility** — existing integrations must not break silently
2. **Developer experience** — protocol changes should reduce, not increase, integration complexity
3. **Financial correctness** — any change to payment flows must preserve financial invariants
4. **Security** — security improvements take precedence over API stability

---

## Maintainers

The project is maintained by [Banzami](https://banzami.org). External maintainers may be added for specific SDK languages based on demonstrated sustained contribution.

---

## Contact

- Protocol questions: open a GitHub Discussion
- Security issues: security@banzami.org (see [SECURITY.md](SECURITY.md))
- Code of conduct: conduct@banzami.org
