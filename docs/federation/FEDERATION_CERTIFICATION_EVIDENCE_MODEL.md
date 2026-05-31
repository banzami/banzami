# BANZA Federation Certification Evidence Model

**Document ID:** FEDERATION-CONFORMANCE-DESIGN-001  
**Date:** 2026-05-31  
**Status:** Canonical — defines what an operator must submit to receive L3 Federation Certification.  
**Authority:** ADR-026, FEDERATION_CONFORMANCE_MODEL.md

---

## Evidence Philosophy

Evidence is the record that a certification decision was made on verifiable facts, not assertions. Every pass or fail decision in the conformance runner is accompanied by machine-readable evidence that BANZA can independently review. BANZA never certifies based on operator self-report alone.

**Evidence collection is automatic.** The conformance runner collects all required evidence as a side effect of running tests. Operators do not submit evidence manually — they run the runner and submit the generated evidence package.

**Evidence is tamper-evident.** The evidence package is signed by the runner using the test BANZA root keypair. Any modification to the package after generation invalidates the signature.

---

## 1. Automated Evidence — Collected by Runner

The following evidence items are captured automatically for every conformance run. No manual submission required.

### 1.1 Certificate Evidence

| Evidence Item | Source | Format | Required For |
|---------------|--------|--------|-------------|
| `cert.raw_json` | `GET /.well-known/banza/certificate.json` | Raw HTTP response body | All CERT tests |
| `cert.http_status` | HTTP status code | Integer | FED-CERT-001 |
| `cert.http_headers` | HTTP response headers | Key-value map | FED-CERT-001 |
| `cert.schema_validation_result` | Runner schema validation | `{valid: bool, errors: []}` | FED-CERT-001 |
| `cert.canonical_json` | Runner canonical form computation | String | FED-CERT-002 |
| `cert.signature_verification_result` | ed25519_verify result | `{verified: bool, key_id: string}` | FED-CERT-002 |
| `cert.expiry_check` | `{expires_at, checked_at, valid: bool}` | JSON | FED-CERT-003 |
| `cert.lifetime_days` | `(expires_at - issued_at) in seconds / 86400` | Float | FED-CERT-007 |
| `cert.operator_id_match` | cert.operator_id vs manifest.operator_id | `{cert_id, manifest_id, match: bool}` | FED-CERT-010 |

### 1.2 Manifest Evidence

| Evidence Item | Source | Format | Required For |
|---------------|--------|--------|-------------|
| `manifest.raw_json` | `GET /.well-known/banza/operator.json` | Raw HTTP response body | All DISC tests |
| `manifest.http_status` | HTTP status | Integer | FED-DISC-001 |
| `manifest.base_schema_valid` | Validation against conformance/manifests/schema.json | `{valid: bool}` | FED-DISC-001 |
| `manifest.fed_schema_valid` | Validation against federation-manifest.json | `{valid: bool}` | FED-DISC-001 |
| `manifest.certificate_url_check` | HTTP GET to certificate_url | `{status, valid_cert: bool}` | FED-DISC-004 |
| `manifest.interop_endpoint_check` | TCP/HTTP to interop_endpoint | `{reachable: bool, latency_ms}` | FED-DISC-005 |

### 1.3 Trust Verification Evidence

| Evidence Item | Source | Format | Required For |
|---------------|--------|--------|-------------|
| `trust.brl_fetch_log` | BRL fetch attempt | `{url, status, fetched_at, expires_at}` | FED-TRUST-001 |
| `trust.brl_signature_verified` | BRL signature check | `{verified: bool}` | FED-TRUST-003 |
| `trust.brl_staleness_check` | BRL age computation | `{age_seconds, limit_seconds=21600, ok: bool}` | FED-TRUST-009 |
| `trust.step_results` | Per-step trust log | `[{step: 1-9, result: pass/fail, reason}]` | FED-TRUST-001 through FED-TRUST-008 |
| `trust.final_result` | `TRUSTED` or `UNTRUSTED` | String | All trust tests |

### 1.4 Routing Evidence

| Evidence Item | Source | Format | Required For |
|---------------|--------|--------|-------------|
| `routing.request_raw` | Raw HTTP request body + headers | Bytes | All ROUTE tests |
| `routing.request_timestamp` | Unix timestamp at send | Integer | FED-ROUTE-005 (signature) |
| `routing.response_raw` | Raw HTTP response | Bytes | All ROUTE tests |
| `routing.response_parsed` | Parsed RoutingResponse | JSON | All ROUTE tests |
| `routing.trace_id_check` | req.trace_id vs resp.trace_id | `{match: bool}` | FED-ROUTE-003 |
| `routing.routing_request_id_check` | req.routing_request_id vs resp.routing_request_id | `{match: bool}` | FED-ROUTE-002 |
| `routing.idempotency_check` | First vs second response comparison | `{identical: bool}` | FED-ROUTE-004 |
| `routing.interop_transfer_id_format` | Regex match on interop_transfer_id | `{matches: bool, value}` | FED-ROUTE-009 |

### 1.5 Execution Evidence

| Evidence Item | Source | Format | Required For |
|---------------|--------|--------|-------------|
| `exec.payee_balance_before` | Wallet balance before routing request | Integer (minor) | FED-EXEC-001 |
| `exec.payee_balance_after` | Wallet balance immediately after acceptance | Integer (minor) | FED-EXEC-001 |
| `exec.payee_balance_delta` | after - before | Integer | FED-EXEC-001 |
| `exec.payer_balance_before` | Payer wallet before | Integer | FED-EXEC-003 |
| `exec.payer_balance_after` | Payer wallet after | Integer | FED-EXEC-003, FED-EXEC-008 |
| `exec.operator_a_ledger_entry` | DEBIT entry for payer_wallet | JSON | FED-EXEC-002 |
| `exec.operator_b_ledger_entry` | CREDIT entry for payee_wallet | JSON | FED-EXEC-002 |
| `exec.atomicity_check` | Debit and obligation co-exist or neither | `{debit_exists, obligation_exists, consistent: bool}` | FED-EXEC-004 |

### 1.6 Obligation Evidence

| Evidence Item | Source | Format | Required For |
|---------------|--------|--------|-------------|
| `obligation.raw_json` | `GET /federation/obligations/{id}` | JSON | All OBL tests |
| `obligation.amount_match` | obligation.amount vs routing_request.amount | `{match: bool}` | FED-OBL-002 |
| `obligation.trace_id_match` | obligation.trace_id vs routing_request.trace_id | `{match: bool}` | FED-OBL-003 |
| `obligation.uniqueness_check` | Count of obligations with same routing_request_id | `{count: int}` | FED-OBL-004 |
| `obligation.signature_verification` | ed25519_verify with Operator A public key | `{verified: bool}` | FED-OBL-005 |
| `obligation.state_history` | Observed states in order | `[pending, in_netting, settled]` | FED-OBL-006 |

### 1.7 Event Evidence

| Evidence Item | Source | Format | Required For |
|---------------|--------|--------|-------------|
| `events.federation_events` | All federation events from both operators | Array of event JSON | All EVT tests |
| `events.trace_id_cross_check` | trace_id in all events for same payment | `{all_match: bool, trace_id}` | FED-EVT-005 |
| `events.schema_validation_results` | Per-event schema validation | `[{event_id, valid: bool}]` | FED-EVT-006 |
| `events.event_types_observed` | Set of event_type values seen | Array of strings | FED-EVT-001 through FED-EVT-004 |

### 1.8 Settlement Evidence

| Evidence Item | Source | Format | Required For |
|---------------|--------|--------|-------------|
| `settle.obligation_export_A_to_B` | Operator A's netting period export | JSON | FED-SETTLE-001 |
| `settle.obligation_export_B_to_A` | Simulated Operator B's netting period export | JSON | FED-SETTLE-001 |
| `settle.net_position_A` | Operator A's computed net | `{gross_A_to_B, gross_B_to_A, net}` | FED-SETTLE-002 |
| `settle.net_position_B` | Simulated Operator B's computed net | `{gross_A_to_B, gross_B_to_A, net}` | FED-SETTLE-003 |
| `settle.net_agreement` | Both nets compared | `{agree: bool}` | FED-SETTLE-003 |
| `settle.bank_transfer_log` | Bank transfer initiation | `{initiated: bool, amount, reference}` | FED-SETTLE-004 |
| `settle.obligations_settled` | Post-settlement obligation states | Array of obligation IDs with state=settled | FED-SETTLE-005 |
| `settle.reconciliation_report` | Cross-reference result | `{total_accepted, total_obligations, missing: [], mismatched: []}` | FED-SETTLE-006, FED-SETTLE-007 |

---

## 2. Evidence Package Structure

The runner generates a single evidence package per conformance run:

```
evidence-package/
  runner-version.txt
  run-id.txt                          # Unique run identifier
  operator-url.txt
  started-at.txt
  completed-at.txt
  
  certificates/
    cert-A.json                       # Raw certificate from Operator A
    cert-B.json                       # Certificate served by Simulated Operator B
    verification-results.json         # Per-certificate verification outcomes
    
  manifests/
    manifest-A.json                   # Raw manifest from Operator A
    validation-results.json
    
  trust-logs/
    brl-fetch.json                    # BRL fetch log
    trust-steps-op-b.json             # 9-step trust verification against Sim Op B
    
  routing-logs/
    FED-ROUTE-001-request.json
    FED-ROUTE-001-response.json
    FED-ROUTE-001-result.json         # Pass/fail determination
    ... (one set per test case)
    
  execution-logs/
    payee-wallet-before.json
    payee-wallet-after.json
    payer-wallet-before.json
    payer-wallet-after.json
    operator-a-ledger-entry.json
    operator-b-ledger-entry.json
    
  obligations/
    obligation-001.json               # Raw obligation from Operator A
    obligation-verification.json      # Signature verification; amount match
    
  events/
    federation-events-A.json          # All federation events from Operator A
    federation-events-B.json          # All federation events from Sim Op B
    trace-cross-check.json
    
  settlement/
    netting-export-A.json
    netting-export-B.json
    net-position-comparison.json
    reconciliation-report.json
    
  suite-results/
    FED-CERT.json                     # Suite-level summary
    FED-DISC.json
    FED-TRUST.json
    FED-ROUTE.json
    FED-EXEC.json
    FED-OBL.json
    FED-EVT.json
    FED-SETTLE.json
    FED-FAIL.json
    
  report.json                         # Machine-readable conformance report
  package-signature.json             # Runner's ed25519 signature of all above
```

---

## 3. Manual Review Items

The following cannot be verified automatically and require BANZA manual review:

| Item | Why Manual | What BANZA Reviews |
|------|-----------|-------------------|
| Production BANZA certificate request | Runner uses test root; production cert requires BANZA's production key | Operator applies to BANZA with conformance report; BANZA issues production certificate |
| Key management procedures | Cannot be tested without access to operator's HSM | Operator documents how private key is stored and rotated |
| Bank account details for settlement | Real bank accounts are outside the test environment | Operator provides settlement bank details for production netting |
| Operational runbook | Organizational process | Operator documents how they respond to F-101 through F-602 failure scenarios |
| Network security | TLS configuration, firewall rules | Operator confirms federation endpoints use TLS 1.2+ |

---

## 4. Evidence Verification by BANZA

When BANZA receives an evidence package for L3 certification:

**Step 1 — Package integrity:**
```
ed25519_verify(test_runner_public_key, package_hash, package_signature.sig)
```
If verification fails: package rejected. Operator must re-run.

**Step 2 — Run ID uniqueness:**
The run-id must be unique and not seen before. Prevents re-submission of old evidence.

**Step 3 — Operator URL match:**
operator-url in package must match the URL Operator A used to register with BANZA.

**Step 4 — Suite result checks:**
```
for each blocking suite [FED-CERT, FED-DISC, FED-TRUST, FED-ROUTE, FED-EXEC, FED-OBL]:
  if suite.overall_result != "PASS": DENY certification
```

**Step 5 — Critical invariant scan:**
Any test case with severity=CRITICAL and result=FAIL → DENY certification.

**Step 6 — Spot verification:**
BANZA independently fetches and verifies:
- `{operator_url}/.well-known/banza/operator.json`
- `{operator_url}/.well-known/banza/certificate.json`
- Verifies certificate signature against test BANZA root key

**Step 7 — Issue production certificate:**
If all checks pass: BANZA issues a production operator certificate, signed with the PRODUCTION BANZA root key. This replaces the test certificate and is valid in the live federation.

---

## 5. Evidence Retention

| Artifact | Retention | Reason |
|----------|-----------|--------|
| Evidence package | 3 years | Audit trail; dispute resolution |
| Suite results | 3 years | Certification history |
| Obligation export | Until settled + 1 year | Settlement disputes |
| Routing logs | 90 days | Operational debugging |
| BRL fetch logs | 90 days | Trust audit |

---

## 6. L3 Certification Evidence Checklist

Before BANZA issues a production certificate, ALL of the following must be present and verified:

```
☐ Evidence package signature verifies against known test runner public key
☐ Run ID unique (not previously submitted)
☐ FED-CERT: all 11 cases PASS
☐ FED-DISC: all 8 cases PASS
☐ FED-TRUST: all 9 cases PASS
☐ FED-ROUTE: cases 001-009 PASS; cases 010-012 PASS or CONDITIONAL
☐ FED-EXEC: cases 001-005 PASS
☐ FED-OBL: cases 001-005 PASS
☐ FED-EVT: all 6 cases PASS or CONDITIONAL
☐ FED-SETTLE: cases 001-008 PASS
☐ FED-FAIL: cases 001, 004, 005 PASS
☐ Zero CRITICAL-severity failures
☐ Manual review completed (key management, bank details, TLS confirmation)
☐ Operator URL verified as publicly reachable
☐ Production certificate request submitted with operator_id and public key
```

When this checklist is complete: BANZA issues the production operator certificate.
