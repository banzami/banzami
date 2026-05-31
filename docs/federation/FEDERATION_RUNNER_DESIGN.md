# BANZA Federation Conformance Runner Design

**Document ID:** FEDERATION-CONFORMANCE-DESIGN-001  
**Date:** 2026-05-31  
**Status:** Canonical — runner architecture specification.  
**Authority:** FEDERATION_CONFORMANCE_MODEL.md, FEDERATION_TEST_SUITE_SPEC.md

---

## Overview

The federation conformance runner is the tool that executes L3 certification tests against an operator. It extends the existing `tools/banza-conformance/` single-operator runner with a federation mode that embeds a Simulated Operator B and a test BANZA trust root.

This document specifies the runner's architecture, test environment, isolation model, and behavioral contracts. It does not implement the runner — it is the specification from which implementation proceeds.

---

## 1. Invocation Model

### 1.1 CLI Interface

```bash
# L0-L2 (existing, unchanged)
banza-conformance --operator-a https://api.operator.example --level 2

# L3 Federation (new)
banza-conformance --federation \
  --operator-a https://api.operator-a.example \
  --level 3 \
  --output ./evidence-package/ \
  [--suite FED-CERT,FED-DISC,FED-TRUST]    # optional: run subset
  [--fixture-override ./custom-fixtures/]   # optional: override specific fixtures
  [--sim-b-port 9090]                       # optional: Simulated Operator B port
```

### 1.2 Output

On success:
```
banza-conformance: L3 Federation certification run complete
Evidence package: ./evidence-package/
Overall result: PASS (79/79 tests passed)
Blocking suites: ALL PASS
Submit package to BANZA at: certification@banza.network
```

On failure:
```
banza-conformance: L3 Federation certification run complete
Evidence package: ./evidence-package/
Overall result: FAIL
Critical failures: 2
  - FED-TRUST-002: FAIL (certificate tampered, trust Step 2.3 not enforced) [CRITICAL]
  - FED-ROUTE-004: FAIL (idempotency not enforced, double credit occurred) [CRITICAL]
Blocking suites: FED-TRUST FAIL, FED-ROUTE FAIL
Certification denied. Fix the above failures and re-run.
```

---

## 2. Runner Components

```
┌────────────────────────────────────────────────────────────────┐
│                     Conformance Runner                          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Test        │  │  Evidence    │  │  Report              │  │
│  │  Orchestrator│  │  Collector   │  │  Generator           │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────────────────┘  │
│         │                 │                                      │
│  ┌──────▼───────────────────────────────────────────────────┐   │
│  │                 Test HTTP Client                          │   │
│  │  (sends requests to Operator A; captures responses)      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Test BANZA Trust Root                        │   │
│  │  - Generates test ed25519 keypair at startup              │   │
│  │  - Issues/revokes test certificates                       │   │
│  │  - Serves test BRL at embedded HTTP endpoint              │   │
│  │  - Serves BANZA key manifest at embedded endpoint         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Simulated Operator B                         │   │
│  │  - Full BANZA-compliant operator stub                     │   │
│  │  - Embeds test certificates and manifests                 │   │
│  │  - Routes to pre-configured recipient wallets             │   │
│  │  - Records all interactions for evidence                  │   │
│  │  - Configurable failure injection per fixture             │   │
│  │  - Serves at localhost:{sim-b-port}                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Simulated Bank Rail                          │   │
│  │  - Returns configurable success/failure/timeout           │   │
│  │  - Records transfer initiation for evidence               │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

---

## 3. Test BANZA Trust Root

### 3.1 Keypair Generation

The runner generates a fresh ed25519 keypair at startup:

```
test_banza_private_key = ed25519_generate_private_key()
test_banza_public_key  = ed25519_derive_public_key(test_banza_private_key)
test_issuer_key_id     = "test-banza-key-" + date_stamp   // e.g. "test-banza-key-2026-05"
```

This keypair is ephemeral — a new one is generated per run. This ensures no test run depends on a previous run's keypair state.

### 3.2 Certificate Issuance

The runner issues all test certificates from this keypair:

```python
def issue_certificate(operator_id, level, public_key, lifetime_days=89):
    cert = {
        "schema_version": "1",
        "operator_id": operator_id,
        "certification_level": level,
        "protocol_version": "1.0",
        "capabilities": ["cross_operator_routing", "cross_operator_settlement"],
        "public_key": f"ed25519:{base64url(public_key)}",
        "issued_at": now_iso8601(),
        "expires_at": (now() + timedelta(days=lifetime_days)).iso8601(),
        "issuer": "BANZA",
        "issuer_key_id": test_issuer_key_id
    }
    canonical = canonical_json(cert)  # sorted keys, no whitespace
    cert["signature"] = base64url(ed25519_sign(test_banza_private_key, canonical))
    return cert
```

### 3.3 Test Root Endpoint

The runner serves the following at `http://localhost:{root-port}`:

```
GET /federation/public-keys.json  → BANZA-KEY-MANIFEST (signed by test root)
GET /federation/revocation-list.json → current test BRL (configurable per test)
```

### 3.4 Operator A Certificate Setup

Before running tests, the runner:
1. Generates an Operator A test keypair (separate from the BANZA root keypair)
2. Issues CERT-A-VALID to Operator A's operator_id
3. Configures Operator A with the test certificate and the corresponding private key (via environment variable or config endpoint — operator-specific)
4. Configures Operator A to use `http://localhost:{root-port}/federation/revocation-list.json` as its BRL endpoint

**Configuration delivery:** The runner sends a setup request to Operator A's conformance setup endpoint (if present) or uses environment variables documented by the operator. Operators must expose a mechanism for the runner to configure:
- Their own test certificate (CERT-A-VALID)
- Their own private key (for request signing)
- The BRL endpoint URL (pointing to runner's test BRL)
- The BANZA public key endpoint URL

---

## 4. Simulated Operator B

### 4.1 Embedded Implementation

The Simulated Operator B is a lightweight HTTP server embedded in the runner, implementing:

```
GET  /.well-known/banza/operator.json    → MANIFEST-B-VALID (or configured manifest)
GET  /.well-known/banza/certificate.json → CERT-B-VALID (or configured certificate)
POST /federation/route                    → processes routing requests
GET  /federation/obligations             → returns obligation store
GET  /federation/events                  → returns event log
GET  /wallets/{wallet_id}                → wallet balance queries
GET  /ledger/{wallet_id}                 → ledger entry queries
```

### 4.2 Pre-Configured Wallets

Simulated Operator B pre-creates the following wallets at startup:

| Wallet ID | State | Balance | Purpose |
|-----------|-------|---------|---------|
| `wallet-payee-test-001` | active | 0 AOA | Happy-path recipient |
| `wallet-suspended-test-001` | suspended | 0 AOA | FED-ROUTE-012 |

All other wallet IDs resolve to "not found" (FED-ROUTE-007).

### 4.3 Routing Request Handling

The Simulated Operator B's routing handler:

```python
def handle_routing_request(request):
    # Step 1: Parse and validate schema
    # Step 2: Check to_operator_id
    # Step 3: Verify Banza-Federation-Signature
    #   - Fetch certificate_url from request
    #   - Run trust steps 2.3-2.9 on Operator A's cert
    #   - Verify ed25519 signature
    # Step 4: Check idempotency
    #   - If routing_request_id in store with SAME content: replay original response
    #   - If routing_request_id in store with DIFFERENT content: return duplicate_request
    # Step 5: Validate business rules (currency, amount, recipient)
    # Step 6: Apply fixture-configured behavior (drop, malformed, etc.)
    # Step 7: Credit payee and accept (atomically in Sim Op B's in-memory store)
    # Step 8: Return ROUTING-RESPONSE-ACCEPTED
```

### 4.4 Failure Injection

Per-test failure injection is specified in simulation control fixtures:

| Fixture | Injected Behavior |
|---------|------------------|
| SIMULATED-NETWORK-DROP-ONCE | Drop first request (no response); process second normally |
| SIMULATED-B-OFFLINE | Return connection refused for all requests |
| SIMULATED-MALFORMED-RESPONSE | Return HTTP 200 with invalid JSON body |
| SIMULATED-B-INTERNAL-ERROR-AFTER-ACCEPT | Accept routing; return 500 on follow-up status queries |

Failure injection is activated per-test by the Test Orchestrator configuring Sim Op B before each test case.

---

## 5. Network Assumptions

### 5.1 What the Runner Assumes

- Operator A is reachable at the URL provided via `--operator-a`
- Operator A can reach Simulated Operator B at `http://localhost:{sim-b-port}` or a configured URL
- Operator A can reach the runner's test BRL endpoint at `http://localhost:{root-port}/federation/revocation-list.json`
- All connections use TLS in production (HTTP allowed in test/sandbox environments)

### 5.2 What the Runner Does NOT Assume

- Operator A's database schema
- Operator A's internal implementation language
- Operator A's key storage mechanism
- Operator A's event delivery mechanism (polling or SSE are both accepted)

### 5.3 Firewall Considerations

For network-isolated operators, the runner can be configured to expose endpoints on a reachable address:

```bash
banza-conformance --federation \
  --operator-a https://api.operator.example \
  --sim-b-host 0.0.0.0 \
  --sim-b-port 9090 \
  --trust-root-host 0.0.0.0 \
  --trust-root-port 9091
```

The operator then configures:
- Simulated Operator B URL: `http://{runner-host}:9090`
- BRL endpoint: `http://{runner-host}:9091/federation/revocation-list.json`

---

## 6. Test Isolation

### 6.1 Per-Test State Reset

Before each test case, the runner:
1. Resets Simulated Operator B's in-memory state (wallet balances, obligation store, event log)
2. Restores fixture-default wallet states (payee wallet balance = 0)
3. Clears Simulated Operator B's routing request store (idempotency cache)
4. Configures the failure injection for the upcoming test (if any)
5. Resets the test BRL to `BRL-CURRENT-EMPTY` (unless overridden by the test)

### 6.2 Deterministic IDs

Routing request IDs, obligation IDs, and trace IDs are pre-assigned per test case (from the fixture catalog). This ensures:
- Test results are reproducible
- Evidence can be matched across multiple evidence packages (if the same test is run twice)
- Idempotency tests work correctly (Sim Op B recognizes the same routing_request_id on retry)

### 6.3 State Injection (FED-FAIL-005)

For FED-FAIL-005 (crash recovery), the runner injects a pre-existing state into Operator A. If Operator A exposes a conformance state-injection endpoint:

```
POST /conformance/inject-state
{
  "routing_requests": [
    { "routing_request_id": "rr-...", "state": "accepted", "interop_transfer_id": "itx-..." }
  ],
  "obligations": []
}
```

If Operator A does not expose this endpoint, FED-FAIL-005 is marked SKIPPED and a note is added to the evidence package.

---

## 7. Clock Control

### 7.1 Approach

The runner does NOT inject clocks into the operator under test. Instead, it calibrates fixtures relative to the runner's actual wall clock:

- **CERT-A-VALID:** `issued_at = now - 1 day`, `expires_at = now + 89 days` → Always valid
- **CERT-EXPIRED:** `issued_at = now - 100 days`, `expires_at = now - 10 days` → Always expired
- **BRL-CURRENT-EMPTY:** `issued_at = now`, `expires_at = now + 7 hours` → Always fresh
- **BRL-EXPIRED:** `issued_at = now - 8 hours`, `expires_at = now - 1 hour` → Always expired

This means tests are time-invariant: they produce the same results regardless of when they run.

### 7.2 Clock Skew Test (FED-CERT-003)

To test that Operator A correctly rejects future-dated certificates (F-601), the runner issues a certificate with:
- `issued_at = now + 10 minutes` (future-dated, but only slightly)
- `expires_at = now + 89 days`

Operator A should reject this at Step 2.4 (`issued_at > now`).

---

## 8. Replay Behavior

### 8.1 Routing Request Replay

For idempotency tests (FED-ROUTE-004), the runner sends the same routing request twice:
1. First request: Simulated Operator B processes normally, returns accepted
2. Second request (same routing_request_id, same body): Sim Op B returns original response without re-processing
3. Runner verifies: Sim Op B's payee wallet balance increased by exactly one payment

### 8.2 Evidence Replay

The evidence package is the immutable record of a run. If BANZA needs to verify a specific step:
1. BANZA extracts the raw HTTP request from `routing-logs/FED-ROUTE-001-request.json`
2. Re-computes the ed25519 signature verification using the Operator A public key in the evidence
3. Compares to `routing-logs/FED-ROUTE-001-result.json`

This makes all verification steps independently reproducible by BANZA without re-running the operator.

---

## 9. Pass/Fail Determination

### 9.1 Per-Test Determination

Each test case has explicit pass and fail conditions defined in the test spec. The runner evaluates them in order:

```python
def evaluate_test(test_id, evidence):
    for fail_condition in test_spec[test_id].fail_conditions:
        if fail_condition.applies(evidence):
            return TestResult(
                id=test_id,
                result="FAIL",
                reason=fail_condition.description,
                severity=fail_condition.severity,
                evidence=evidence
            )
    for pass_condition in test_spec[test_id].pass_conditions:
        if not pass_condition.applies(evidence):
            return TestResult(id=test_id, result="FAIL", reason="Pass condition not met", ...)
    return TestResult(id=test_id, result="PASS", evidence=evidence)
```

### 9.2 Suite-Level Determination

```python
def evaluate_suite(suite_id, test_results):
    has_critical_fail = any(r.severity == "CRITICAL" and r.result == "FAIL" for r in test_results)
    has_any_fail = any(r.result == "FAIL" for r in test_results)
    
    if has_critical_fail:
        return SuiteResult(result="FAIL", blocking=True)
    elif has_any_fail:
        return SuiteResult(result="FAIL", blocking=(suite_id in BLOCKING_SUITES))
    else:
        return SuiteResult(result="PASS")
```

### 9.3 Certification Decision

```
BLOCKING_SUITES = [FED-CERT, FED-DISC, FED-TRUST, FED-ROUTE, FED-EXEC, FED-OBL]

certification_result = "PASS"
for suite in all_suites:
    if suite.result == "FAIL" and suite.id in BLOCKING_SUITES:
        certification_result = "FAIL"
        break

if any_critical_fail:
    certification_result = "FAIL"
```

### 9.4 Strict Pass/Fail Table

| Condition | Certification | Notes |
|-----------|--------------|-------|
| All 79 tests PASS | GRANTED | No conditions |
| FED-CERT: any FAIL | DENIED | |
| FED-DISC: any FAIL | DENIED | |
| FED-TRUST: any FAIL | DENIED | |
| FED-ROUTE: FAIL on 001-009 | DENIED | |
| FED-ROUTE: FAIL on 010-012 only | CONDITIONAL | Remediation within 30 days |
| FED-EXEC: FAIL on 001-005 | DENIED | |
| FED-EXEC: FAIL on 006-008 only | CONDITIONAL | |
| FED-OBL: FAIL on 001-005 | DENIED | |
| FED-OBL: FAIL on 006-007 only | CONDITIONAL | |
| FED-EVT: any FAIL | CONDITIONAL | Event emission is non-financial |
| FED-SETTLE: FAIL on 001-008 | CONDITIONAL | Settlement cannot be tested end-to-end without real bank |
| FED-FAIL: FAIL on 001, 004, 005 | DENIED | Critical recovery paths |
| FED-FAIL: FAIL on 002, 003, 006, 007, 008 | CONDITIONAL | |
| Any CRITICAL severity FAIL | DENIED | Regardless of suite |

---

## 10. Evidence Package Generation

### 10.1 Package Assembly

At run completion:
```python
def generate_evidence_package(output_dir, test_results, all_evidence):
    write_file(f"{output_dir}/run-id.txt", run_id)
    write_file(f"{output_dir}/report.json", generate_report(test_results))
    
    for suite, results in test_results_by_suite:
        write_file(f"{output_dir}/suite-results/{suite}.json", results)
    
    for evidence_item in all_evidence:
        write_file(f"{output_dir}/{evidence_item.path}", evidence_item.content)
    
    # Sign the package
    all_files_hash = sha256_of_all_files(output_dir)
    signature = ed25519_sign(test_banza_private_key, all_files_hash)
    write_file(f"{output_dir}/package-signature.json", {
        "run_id": run_id,
        "files_hash": hex(all_files_hash),
        "runner_public_key": base64url(test_banza_public_key),
        "runner_key_id": test_issuer_key_id,
        "signature": base64url(signature)
    })
```

### 10.2 Report Format

The `report.json` follows the existing `conformance/report-schema.json` format, extended with federation fields:

```json
{
  "report_id": "rpt-fed-2026-06-01T10:00:00Z-operator-a-test",
  "generated_at": "2026-06-01T10:05:00Z",
  "runner_version": "2.0.0-federation",
  "operator_url": "https://api.operator-a-test.example",
  "operator_id": "operator-a-test",
  "protocol_version": "1.0",
  "federation_mode": true,
  "certification_level_achieved": 3,
  "summary": {
    "total": 79,
    "passed": 79,
    "failed": 0,
    "skipped": 0,
    "warnings": 0
  },
  "suites": [
    {
      "suite_id": "FED-CERT",
      "overall_result": "PASS",
      "blocking": true,
      "tests": [...]
    }
  ]
}
```

---

## 11. Integration With Existing Runner

The federation runner is implemented as an extension to `tools/banza-conformance/`:

```
tools/banza-conformance/
  run.py                          # Existing entrypoint; extended to accept --federation
  suites/
    operators.json                # Existing L0-L2 suites (unchanged)
    federation/                   # New federation suites
      FED-CERT.json
      FED-DISC.json
      FED-TRUST.json
      FED-ROUTE.json
      FED-EXEC.json
      FED-OBL.json
      FED-EVT.json
      FED-SETTLE.json
      FED-FAIL.json
  fixtures/
    federation/                   # All 44 fixtures from FEDERATION_FIXTURE_CATALOG.md
  sim-b/                          # Simulated Operator B HTTP server
    server.py
    wallets.py
    routing.py
    obligations.py
    events.py
  trust-root/                     # Test BANZA trust root
    keygen.py
    issue_certificate.py
    brl_server.py
    key_manifest_server.py
  evidence/
    collector.py
    packager.py
    signer.py
```

---

## 12. Simulated Bank Rail

The Simulated Bank Rail is a simple stub that logs settlement initiation:

```
POST /bank/transfer
  Body: { amount, currency, from_account, to_account, reference }
  Response (SETTLEMENT-BANK-SUCCESS): HTTP 200 { transfer_id, status: "accepted" }
  Response (SETTLEMENT-BANK-FAILURE): HTTP 200 { error: "nsf", status: "rejected" }
```

The runner configures which response the bank returns via the SETTLEMENT-BANK-SUCCESS or SETTLEMENT-BANK-FAILURE fixture. Operator A must be configured to point its `SettlementExecutionProvider` at `http://localhost:{bank-port}/bank/transfer` for testing.
