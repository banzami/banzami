# Conformance and Certification

The Banzami conformance system lets any operator, SDK, or integration verify that it correctly implements the Banzami protocol. Conformance is binary: either a behaviour matches the spec, or it doesn't.

## What conformance covers

- **Operators** — HTTP servers that implement wallets, transfers, QR, payment requests, events, settlement, and traces
- **SDKs** — Client libraries that parse QR payloads, event envelopes, and webhook signatures
- **QR runtimes** — Code that generates or scans `BANZAMI-SBX:` and `BANZAMI:` payloads
- **Event emitters** — Services that emit conformant event envelopes with trace fields
- **Ledger implementations** — Storage that satisfies double-entry and immutability invariants
- **Settlement providers** — Implementations that satisfy the no-money-creation invariant

## Certification levels

| Level | Name | Description |
|-------|------|-------------|
| 0 | Sandbox Operator | Health, wallet creation, basic transfer, environment isolation |
| 1 | Payment Operator | All Level 0 + QR, payment requests, events, ledger, settlement |
| 2 | Settlement Operator | All Level 1 + `trace_id` on all entities, `GET /traces` endpoint |
| 3 | Federation Operator | All Level 2 + valid operator manifest, capability declaration |
| 4 | Infrastructure Operator | All Level 3 + settlement fee model, no-money-creation invariant |

The reference sandbox operator is certified at **Level 2**.

## Running the conformance suite

Start your operator, then:

```bash
python3 tools/banzami-conformance/run.py \
  --url http://localhost:3000 \
  --level 2 \
  --output report.json
```

See `tools/banzami-conformance/README.md` for full options.

## Conformance vectors

All test vectors are deterministic JSON files in `conformance/vectors/`. Each vector specifies an input, the expected HTTP response, and the expected downstream effects (events, ledger entries, trace structure).

| File | Vectors | Covers |
|------|---------|--------|
| `vectors/transfers.json` | TRF-001 – TRF-009 | P2P transfers, idempotency, ledger, traces |
| `vectors/qr-payloads.json` | QR-001 – QR-007 | QR generation, open/fixed amount, single-use, trace |
| `vectors/payment-requests.json` | PR-001 – PR-006 | PR lifecycle, expiry, trace propagation |
| `vectors/settlement-batches.json` | STL-001 – STL-006 | Settlement batches, fee model, idempotency |
| `vectors/event-envelopes.json` | EVT-001 – EVT-008 | Event emission, envelope schema, trace fields |
| `vectors/ledger-postings.json` | LED-001 – LED-006 | Double-entry, balance, immutability, trace |
| `vectors/wallet-balances.json` | WLT-001 – WLT-005 | Wallet creation, seeding, balance after transfer |
| `vectors/operator-manifests.json` | MAN-001 – MAN-004 | Manifest schema, safety invariants |

## Financial invariants

Every operator must satisfy these invariants at all times:

| Invariant | Description |
|-----------|-------------|
| `zero_sum_ledger` | Every transfer creates DEBIT and CREDIT of exactly equal amount |
| `no_negative_balance` | No wallet may reach a negative balance |
| `idempotency` | Same idempotency key always returns the same result |
| `trace_id_propagation` | All entities in a flow share the same `trace_id` |
| `causation_id_set` | Derived transfers carry `causation_id` pointing to the trigger |
| `ledger_immutability` | No ledger entry is modified after creation |
| `single_use_qr` | A paid QR code cannot be paid again |
| `single_use_pr` | A paid payment request cannot be paid again |
| `settlement_no_money_creation` | `net_minor + fee_minor` must equal `gross_minor` exactly |
| `settlement_idempotency` | A transfer appears in exactly one settlement batch |

## Conformance report format

Reports follow `conformance/report-schema.json`. Each run produces:

```json
{
  "report_id": "rpt-20260528T100000Z",
  "certification_level_achieved": 2,
  "summary": { "total": 28, "passed": 28, "failed": 0 },
  "suites": [
    {
      "suite_id": "health",
      "certification_level": 0,
      "passed": 2,
      "failed": 0,
      "cases": [...]
    }
  ]
}
```

## Compatibility badges

Include a badge in your operator's README to declare the certification level:

```markdown
![Protocol Compatible](https://raw.githubusercontent.com/banzami/banzami/main/conformance/badges/protocol-compatible.svg)
![Trace Compatible](https://raw.githubusercontent.com/banzami/banzami/main/conformance/badges/trace-compatible.svg)
![Federation Ready](https://raw.githubusercontent.com/banzami/banzami/main/conformance/badges/federation-ready.svg)
![Settlement Compatible](https://raw.githubusercontent.com/banzami/banzami/main/conformance/badges/settlement-compatible.svg)
```

## Operator manifest

Federation Operators (Level 3+) must serve a manifest at `/.well-known/banzami/operator.json`:

```json
{
  "operator_id": "your-operator-id",
  "environment": "sandbox",
  "simulated": true,
  "production_allowed": false,
  "protocol_version": "1.0",
  "certification_level": 2,
  "capabilities": {
    "supports_wallets": true,
    "supports_qr": true,
    "supports_settlement": true,
    "supports_payment_requests": true,
    "supports_events": true,
    "supports_traces": true
  }
}
```

The manifest schema is validated by `conformance/manifests/schema.json`.

**Safety invariant:** Any sandbox operator MUST declare `simulated: true` and `production_allowed: false`. The conformance runner will fail MAN-002 and ENV-001 if these are not set.

## Adding new vectors

1. Assign a stable ID (e.g. `TRF-010`) — IDs are never reused
2. Add the vector to the appropriate file in `conformance/vectors/`
3. Set `"stability": "experimental"` until it passes the reference operator
4. Reference the vector from the relevant suite's `vectors` array
5. Implement the test case in `tools/banzami-conformance/run.py`

Deprecated vectors get `"deprecated": true` rather than being removed — this preserves history.

## CI integration

The `conformance` GitHub Actions workflow runs on every push to `main` and every pull request:

| Job | What it checks |
|-----|---------------|
| `validate-vectors` | All JSON files parse; vector IDs are unique |
| `openapi-compat` | No breaking changes in the OpenAPI spec |
| `schema-compat` | Report and manifest schemas are structurally valid |
| `qr-compat` | QR vectors decode to the expected payloads |
| `trace-contract` | All vector IDs referenced in suites exist in vector files |
| `manifest-validation` | Manifest schema has all required fields |
| `reference-conformance` | Reference operator achieves Level 2 |

Any invariant, schema, QR, trace, or manifest contract violation fails the build.
