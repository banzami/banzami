# Banzami Governance

## Overview

Banzami is governed by Banzami (the organization) and maintained as an open-source ecosystem project. The governance model separates protocol decisions (which affect all implementations) from implementation decisions (which are internal to each SDK or plugin).

## Decision types

### Protocol decisions (ADR required)

Changes to the canonical protocol affect all SDK implementations and must follow the Architecture Decision Record process:

- Changes to `contracts/openapi/` — API shape changes
- Changes to `contracts/webhooks/` — webhook payload changes
- Changes to `contracts/qr/` — QR payload format changes
- Changes to `contracts/sdk-certification/` — certification vector changes
- New major SDK API surface changes

**Process:** Open a GitHub Discussion → propose an ADR → review period (minimum 7 days) → merge with ADR.

### Implementation decisions

Improvements within existing protocol bounds (bug fixes, performance, ergonomics):

- SDK implementation details
- Plugin improvements
- Documentation updates
- Example additions

**Process:** Standard pull request review.

## Architecture Decision Records

All ADRs live in [`docs/adr/`](docs/adr/). Each ADR must include:

- **Context** — what problem this decision addresses
- **Decision** — what was decided
- **Rationale** — why this decision was made
- **Alternatives considered** — what else was evaluated
- **Consequences** — tradeoffs and downstream effects

ADR numbering is sequential and permanent. ADRs are never deleted — they are superseded by newer ADRs when decisions change.

## SDK compatibility

Banzami maintains a compatibility guarantee for SDK consumers:

- Minor versions are backwards compatible
- Breaking changes require a major version bump and a deprecation period
- The certification suite (`contracts/sdk-certification/`) defines the minimum compatibility bar

## Maintainers

The project is maintained by [Banzami](https://banzami.org). External maintainers may be added for specific SDK languages based on demonstrated sustained contribution.

## Contact

- Protocol questions: open a GitHub Discussion
- Security issues: security@banzami.org (see [SECURITY.md](SECURITY.md))
- Code of conduct: conduct@banzami.org
