# ADR-024 — Reference Operator

**Status:** Accepted  
**Date:** 2026-05-28  
**Author:** Banzami Organisation  
**Deciders:** Fidel Monteiro (Founder)  
**Supersedes:** None  
**See also:** ADR-018, ADR-019, ADR-021, ADR-022

---

## Context

After the kernel extraction (ADR-018), the Banza public repository contained financial primitives, SDKs, contracts, and documentation — but no way to run anything. A contributor who cloned the repo could inspect the code but could not create a wallet, initiate a transfer, generate a QR code, or observe the ledger in action.

The contributor experience was: `git clone → ??? → ???`.

The problem is structural: the only working deployment of Banza was the private Banzami operator, which requires production infrastructure, EMIS credentials, Firebase, and internal secrets. There was no path from "open-source contributor" to "running the system".

## Decision

Create `reference/sandbox-operator/` — a minimal, fully local implementation of the Banza operator model using only public kernel crates and simulated providers.

### What the reference operator is

- A **developer playground** for experimenting with the Banza kernel
- A **contributor runtime** for validating kernel changes
- A **protocol reference** showing how providers are wired to the kernel
- An **educational resource** demonstrating the operator/kernel boundary

### What the reference operator is NOT

- A production financial institution
- A production payment operator
- A compliance-grade deployment
- A starting template for a real fintech (too simplified)

### Components

| Component | Location | Purpose |
|---|---|---|
| Sandbox operator | `reference/sandbox-operator/` | Wires all providers + kernel engines |
| Local ledger | `reference/local-ledger/` | SQLite-backed ledger, no Postgres required |
| Mock routing | `reference/mock-routing/` | Simulated payment rail routing |
| Simulated settlement | `reference/simulated-settlement/` | Fake settlement queue |
| Fake acquirer | `reference/fake-acquirer/` | Implements `AcquirerProvider` with no external calls |
| Local notifications | `reference/local-notifications/` | stdout + WebSocket events, no Firebase |
| Docker environment | `reference/docker-compose.yml` | One-command local startup |

### Target developer experience

```bash
git clone https://github.com/banza-protocol/banzami.git
cd banzami/reference
docker compose up
# → fully functional local Banzami environment
```

Or without Docker:
```bash
cd reference/sandbox-operator
cargo run
# → SQLite-backed sandbox running on localhost
```

### Explicit non-goals

The reference operator must never:
- Connect to real payment rails
- Store production credentials
- Be used as a production deployment template
- Be confused with the Banzami commercial product

### Documentation requirement

`reference/sandbox-operator/README.md` must prominently state that this is a developer sandbox, not a production implementation.

## Consequences

**Positive:**
- Contributors can run the full system without any private infrastructure
- Kernel changes can be validated end-to-end without Banzami access
- The operator/kernel boundary becomes visible through working code, not just documentation
- Banza no longer mentally depends on Banzami for local development

**Negative:**
- Reference implementations require maintenance as the kernel evolves
- Risk of contributors mistaking the reference operator for a production template (mitigated by documentation)
- Additional codebase surface to maintain

## Alternatives considered

**Docker image with Banzami behind a public API:** Rejected. Requires maintaining a public deployment of private infrastructure.

**Embedded test fixtures in existing crates:** Rejected. Doesn't provide the end-to-end runtime experience; contributors still can't run a working system.

**No reference operator (documentation only):** Rejected. "Show, don't tell" — working code is more valuable than architecture diagrams for contributor onboarding.
