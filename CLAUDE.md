# BANZA — Protocol Kernel

> **I am working on the open financial infrastructure protocol.**  
> The protocol exists independently of any operator.

---

## Ecosystem Identity (ADR-025)

```
BANZA    = open financial infrastructure protocol        ← THIS REPO
BanzAI   = Protocol Operating System                    ~/banzai
the reference operator  = Reference operator implementation            ~/banza
```

Read the shared operating rules first: [docs/governance/CLAUDE_BASE.md](docs/governance/CLAUDE_BASE.md)

---

## This Repository's Purpose

`~/banza` is the **open protocol kernel**. It defines the rules that all operators must follow. It does not implement any specific operator's product. It is not the reference operator. It is not a wallet app. It is the infrastructure beneath all operators.

**The protocol exists independently of any operator.**  
If the reference operator ceases operations, the BANZA protocol — its specifications, contracts, SDKs, conformance suite, and certification framework — remains fully available to all operators.

---

## Responsibilities of This Repository

| Area | Description |
|---|---|
| `core/` | Protocol kernel — ledger engine, wallet engine, settlement, reconciliation, risk, compliance (Rust) |
| `contracts/` | Canonical protocol contracts — OpenAPI specs, webhook schemas, QR payload spec, event contracts |
| `sdk/` | Official operator SDKs — TypeScript, PHP, Go, Python, Flutter |
| `conformance/` | Conformance suite — certification test vectors for operator compliance |
| `sdk-certification/` | SDK certification vectors |
| `reference/` | Protocol reference documentation |
| `examples/` | Integration examples for operators |
| `integrations/` | Integration adapters and plugins |
| `docs/adr/` | Architecture Decision Records governing the protocol |
| `docs/governance/` | Shared operating rules (CLAUDE_BASE.md) |
| `apps/` | Platform applications (including BanzAI backend) |

---

## Protocol-Specific Guardrails

**Never introduce product logic into protocol specifications.**

Protocol specifications define rules (what is correct), not operator experiences (how a product looks). If a change is specific to how the reference operator's app works, it belongs in `~/banza`, not here.

**Never make the protocol dependent on a single operator.**

All protocol contracts, invariants, and certification criteria must be operator-agnostic. No operator name (including the reference operator) should appear in protocol specifications as a hard dependency.

**Never weaken a financial invariant for convenience.**

The financial invariants are the protocol's integrity guarantees:
- `INV-LEDGER-*` — double-entry, immutability, precision, atomicity
- `INV-WALLET-*` — no negative balance, ledger-derived balances
- `INV-SETTLE-*` — settlement amount identity, ledger correctness
- `INV-IDEM-*` — replay safety, idempotency key scope
- `INV-RECON-*` — posting linkage, external reconcilability
- `INV-QR-*` — unique resolution, single-use dynamic, expiry enforcement

**Protocol specs ship before operator implementations.**

No operator implementation may reference a feature that has not first been specified in `contracts/`. No feature may exist only in prose documentation (`docs/`) once implementation begins — it must have a corresponding artifact in `contracts/`.

---

## Technology Stack (Protocol Layer)

| Layer | Technology | Rationale |
|---|---|---|
| Financial kernel | **Rust** | Memory safety, deterministic behavior, infrastructure-grade reliability |
| API orchestration | **Go** | Simplicity, concurrency, operational reliability |
| Database | **PostgreSQL** | Single source of financial truth — transactional guarantees |
| Cache / coordination | **Redis** | Idempotency, distributed locking, rate limiting |
| Observability | **OpenTelemetry + Prometheus + Grafana** | No black boxes |

---

## Rust Kernel Standards

- Use integer arithmetic (i64, u64) for all monetary values — never floating point
- All ledger writes are synchronous and atomic (never async for the posting step)
- Double-entry enforcement is non-negotiable — every debit has a corresponding credit
- Wallet balances are always ledger-derived — never updated directly
- Every financial operation MUST be idempotent

---

## ADR Reference

| ADR | Subject |
|---|---|
| ADR-002 | Double-entry ledger |
| ADR-004 | Idempotency and rate limiting |
| ADR-006 | QR payment system |
| ADR-012 | SDK-first ecosystem |
| ADR-013 | Wallet-native identity |
| ADR-018 | Open financial kernel |
| ADR-019 | Operator separation |
| ADR-020 | Double-entry invariant enforcement |
| ADR-024 | Reference operator |
| ADR-025 | Ecosystem naming inversion (canonical — supersedes ADR-016) |

---

## Validation Governance

The the reference operator implementation matrix lives in `~/banza/docs/validation/BANZA_IMPLEMENTATION_MATRIX.json` (the reference operator repo, not this repo). Status changes to that matrix require governed approval per the the reference operator repo's governance model.

This repo (`~/banza`) does not own a validation matrix — it owns protocol specifications in `contracts/`, conformance vectors in `conformance/`, and certification criteria in `BANZA_CERTIFICATION.md`.

---

## Deployment

The protocol kernel components are deployed via `./deploy.sh` in `~/banza` (the reference operator repo). Protocol kernel changes are not deployed independently — they are consumed by the reference operator and by any other certified operator.

---

## Operator Neutrality Rule (Enforced)

**No specific commercial operator brand may appear in this repository.**

BANZA is an open protocol. It must be buildable, understandable, and governable without any knowledge of any specific operator. Use these terms instead:

| Forbidden | Use instead |
|-----------|-------------|
| *(specific operator name)* | certified operator |
| *(specific operator name)* | reference operator |
| *(specific operator name)* | operator implementation |
| *(specific operator name)* | federation member |

**Automated enforcement:** `make identity-check` and the `identity-guard` CI job on every push and pull request.

---

## What This Repository Is NOT

- Not a consumer app
- Not a merchant dashboard
- Not any operator's private implementation
- Not a proprietary product
- Not a wallet interface
- Not BanzAI (that is `~/banzai`)
