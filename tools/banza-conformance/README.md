# Banza Conformance Runner

Tests a running Banza operator against the protocol conformance suite and produces a structured JSON report.

## Requirements

Python 3.8+. No third-party packages for the core runner — stdlib only.

For L3 federation conformance (signature verification): `pip install cryptography>=41.0.0`

## Usage

### Standard conformance (L0–L4)

```bash
# Run all suites against a local operator
python3 tools/banza-conformance/run.py --url http://localhost:3000

# Run up to Level 2 only
python3 tools/banza-conformance/run.py --url http://localhost:3000 --level 2

# Run a single suite
python3 tools/banza-conformance/run.py --url http://localhost:3000 --suite health

# Write report to file (quiet mode)
python3 tools/banza-conformance/run.py --url http://localhost:3000 --output report.json --quiet
```

Or via the shell wrapper:

```bash
./tools/banza-conformance/run.sh --url http://localhost:3000 --output report.json
```

### L3 Federation Conformance (79 tests, 9 suites)

The federation conformance suite tests cross-operator federation protocol compliance.
It requires two terminals: one for the fixture server (Operator A adapter) and one for the runner.

```bash
# Terminal 1 — start the fixture server (Operator A)
python3 tools/banza-conformance/fixture_server.py --port 8099

# Terminal 2 — run the full federation suite (79 tests)
python3 tools/banza-conformance/run.py \
  --federation \
  --url http://localhost:8099 \
  --output l3-report.json

# Run only one federation sub-suite
python3 tools/banza-conformance/run.py \
  --federation \
  --url http://localhost:8099 \
  --fed-suite cert        # cert | disc | trust | route | exec | obl | evt | settle | fail
```

**What the federation runner does:**
- Generates an ephemeral test BANZA root keypair (never reused as production)
- Spins up an embedded Simulated Operator B (random port, in-process)
- Spins up an embedded test BRL/key-manifest server (random port, in-process)
- Runs all 79 federation tests against the fixture server
- Produces a structured JSON evidence report

**Federation suites:**

| Suite | Cases | Blocking | What it tests |
|---|---|---|---|
| FED-CERT | 11 | Yes | Certificate schema, signature, expiry, BRL |
| FED-DISC | 8 | Yes | Federation manifest extension fields |
| FED-TRUST | 9 | Yes | All 9 ADR-026 trust protocol steps |
| FED-ROUTE | 12 | Yes | Routing wire protocol, idempotency, rejections |
| FED-EXEC | 8 | Yes | Acceptance semantics, ledger atomicity |
| FED-OBL | 7 | Yes | Obligation creation, signature, state machine |
| FED-EVT | 6 | No | Federation event emission and schema |
| FED-SETTLE | 10 | No | Netting, settlement, reconciliation |
| FED-FAIL | 8 | No | Retry, crash recovery, revocation, mismatches |

**L3 certification decision:** All blocking suites (FED-CERT through FED-OBL) must PASS. FAIL in a blocking suite denies certification. FAIL in a non-blocking suite produces conditional certification (30-day remediation window).

See `docs/federation/FEDERATION_CONFORMANCE_MODEL.md` for the full decision rules.

## Options

| Flag | Description |
|------|-------------|
| `--url` | Base URL of the operator (required) |
| `--level` | Maximum certification level to test, 0–4 (default 4) |
| `--suite` | Run one suite only: `health`, `wallets`, `transfers`, `traces`, `manifest` |
| `--output` | Write JSON report to this path (default: stdout) |
| `--quiet` | Suppress PASS lines; only print failures and summary |

## Certification levels

| Level | Name | Required suites |
|-------|------|----------------|
| 0 | Sandbox Operator | health, wallets, transfers |
| 1 | Payment Operator | + QR, payment requests, events, ledger, settlement |
| 2 | Settlement Operator | + traces |
| 3 | Federation Operator | + manifest |
| 4 | Infrastructure Operator | + settlement invariants |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All executed cases passed |
| 1 | One or more cases failed |
| 2 | Runner error (connectivity, bad arguments) |

## Report format

Reports conform to `conformance/report-schema.json`. Each case records:
- `status`: PASS / FAIL / SKIP / ERROR
- `request` and `response` for HTTP cases
- `assertions`: per-field check results
- `failure_reason`: human-readable explanation on failure

## Adding new suites

1. Implement a runner function `run_<name>(base_url, ctx) -> list[CaseResult]`
2. Register it in the `SUITES` dict
3. Add it to the relevant `LEVEL_SUITES` entries
4. Add the corresponding vectors in `conformance/vectors/`
