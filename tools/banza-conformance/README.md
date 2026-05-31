# Banza Conformance Runner

Tests a running Banza operator against the protocol conformance suite and produces a structured JSON report.

## Requirements

Python 3.8+. No third-party packages — stdlib only.

## Usage

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
