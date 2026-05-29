# Banzami Conformance & Certification

Version: 1.0 · Status: Stable

This directory contains the canonical conformance system for the Banzami protocol
ecosystem. It defines what it means for an operator, SDK, provider, QR runtime,
or event emitter to be **Banzami-compatible**.

---

## What is conformance?

Conformance means an implementation correctly implements the Banzami protocol:

- **Protocol compatibility** — request/response shapes match the canonical schemas
- **Invariant correctness** — financial invariants hold (zero-sum ledger, no negative
  balance, idempotency, immutable postings, atomicity)
- **Interoperability readiness** — another conformant implementation can communicate
  with yours predictably

Conformance is tested against **canonical test vectors** — deterministic,
human-readable JSON descriptions of inputs, expected outputs, expected events,
expected ledger effects, and expected trace structures.

---

## What conformance is NOT

```
╔════════════════════════════════════════════════════════════╗
║  CONFORMANCE DOES NOT MEAN:                                ║
║                                                            ║
║  ✗ Regulatory approval                                     ║
║  ✗ Legal compliance                                        ║
║  ✗ Financial institution authorization                     ║
║  ✗ Production security certification                       ║
║  ✗ Banking license                                         ║
║                                                            ║
║  Conformance certifies PROTOCOL INTEROPERABILITY only.     ║
╚════════════════════════════════════════════════════════════╝
```

Any operator deploying Banzami in production is solely responsible for its own
regulatory compliance, security posture, and legal obligations.

---

## Certification levels

| Level | Name | What it certifies |
|-------|------|-------------------|
| **Level 0** | Sandbox Operator | Health, wallet creation, basic transfer, health endpoint |
| **Level 1** | Payment Operator | All Level 0 + QR, payment requests, events, ledger, settlement |
| **Level 2** | Settlement Operator | All Level 1 + trace_id on all operations, GET /traces, causation_id |
| **Level 3** | Federation Operator | All Level 2 + valid manifest, capability declaration, environment isolation |
| **Level 4** | Infrastructure Operator | All Level 3 + settlement lifecycle, fee model, no-money-creation invariant |

Levels are additive — every level requires all lower levels to pass.

---

## Reference operator

The Banzami **sandbox operator** (`reference/sandbox-operator/`) is the canonical
conformance target. It is the reference implementation against which all other
operators, SDKs, and providers validate compatibility.

> Other operators should validate compatibility against the reference operator behavior.

The sandbox operator is guaranteed to pass all conformance suites at Level 4.
If the sandbox fails a suite, that is a bug in the sandbox — file an issue.

---

## Directory structure

```
conformance/
├── README.md           This file
├── report-schema.json  Canonical report format for conformance results
├── vectors/            Canonical test vectors (deterministic, language-neutral)
│   ├── transfers.json
│   ├── qr-payloads.json
│   ├── payment-requests.json
│   ├── settlement-batches.json
│   ├── event-envelopes.json
│   ├── wallet-balances.json
│   ├── ledger-postings.json
│   └── operator-manifests.json
├── operators/          Operator conformance suite
│   └── suite.json
├── sdk/                SDK conformance suite
│   └── suite.json
├── qr/                 QR runtime conformance suite
│   └── suite.json
├── events/             Event schema validation suite
│   └── suite.json
├── ledger/             Ledger invariant suite
│   └── suite.json
├── settlement/         Settlement conformance suite
│   └── suite.json
├── manifests/          Operator manifest validation
│   └── schema.json
├── capabilities/       Capability descriptor validation
│   └── schema.json
└── badges/             Compatibility badge SVGs
```

Run suites against any operator:

```bash
./tools/banzami-conformance/run.sh --url http://localhost:3100
```

See [`tools/banzami-conformance/README.md`](../tools/banzami-conformance/README.md) for full usage.

---

## Suite authorship

Suites are authored in JSON and executed by the conformance runner. Each vector is:

- **Deterministic** — same input always produces the same expected output
- **Stable** — vectors are immutable once published; new cases get new IDs
- **Human-readable** — JSON, no binary formats
- **Language-neutral** — the runner is Python stdlib; vectors work against any HTTP operator

---

## Adding new vectors

1. Choose the correct vector file in `vectors/`
2. Assign a monotonically increasing ID (`TRF-010`, `QR-003`, etc.)
3. Fill all required fields: `id`, `title`, `certification_level`, `input`, `expected`
4. Add the vector to the relevant suite in `operators/suite.json` or domain-specific suite
5. Run the conformance runner to verify the reference operator passes
6. Open a PR — vectors require review by one maintainer

Vector IDs are immutable. If a vector becomes invalid, mark it `deprecated: true`.

---

## Future: federation conformance

The conformance system is designed to extend to multi-operator federation:

- Cross-operator routing vectors
- Inter-operator settlement vectors
- Identity resolution vectors
- CBDC operator conformance
- Government sandbox conformance
- Offline payment mode conformance

Federation conformance will be added when the cross-operator routing protocol
reaches Stable status.
