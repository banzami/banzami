# FED-CERT-001 First Pass Report

**Document ID:** FED-CERT-001-FIRST-PASS-REPORT-001  
**Date:** 2026-05-31  
**Status:** PASS — first executable Federation conformance result  
**Authority:** FEDERATION_TEST_SUITE_SPEC.md, L3-FIRST-PASS-IMPLEMENTATION-PLAN-001

---

## Result

```
============================================================
FED-CERT-001: PASS

What this proves:
  ✓ Certificate endpoint exists and returns HTTP 200
  ✓ Content-Type is application/json
  ✓ Response is valid JSON
  ✓ JSON satisfies operator-certificate.json schema

What this does NOT yet prove:
  – Signature validity           (FED-CERT-002)
  – Certificate not expired       (FED-CERT-003)
  – Trust engine behavior         (FED-CERT-008–011)
  – Cross-operator routing        (FED-TRUST through FED-OBL)
============================================================
```

---

## Command Run

```bash
# Terminal 1 — start local fixture server
python3 tools/banza-conformance/fixture_server.py --port 8099

# Terminal 2 — run conformance
python3 tools/banza-conformance/run.py --federation --url http://localhost:8099
```

Or standalone:

```bash
python3 tools/banza-conformance/run_fed.py --url http://localhost:8099
```

---

## Files Added

| File | Purpose |
|---|---|
| `contracts/federation/operator-certificate.json` | JSON Schema for the BANZA-issued operator certificate. The canonical contract against which FED-CERT-001 validates. |
| `conformance/fixtures/federation/CERT-A-VALID.json` | Static certificate fixture with deterministic IDs. Valid schema; placeholder cryptographic values. |
| `tools/banza-conformance/trust_root.py` | Test trust root utilities — Slice 0. Provides `generate_test_certificate()` for dynamic fixture generation. Placeholder signatures; real ed25519 in WP-002. |
| `tools/banza-conformance/run_fed.py` | Federation conformance runner. Implements `run_fed_cert_001()`, `run_suite_fed_cert()`, `run_federation_mode()`. |
| `tools/banza-conformance/fixture_server.py` | Local HTTP server that serves `CERT-A-VALID.json` at `/.well-known/banza/certificate.json` for self-contained testing. |

## Files Modified

| File | Change |
|---|---|
| `tools/banza-conformance/run.py` | Added `--federation` flag. When set: delegates entirely to `run_fed.run_federation_mode()`. No existing L0-L2 behavior changed. |

---

## What FED-CERT-001 Proves

FED-CERT-001 is a **structure test**. It answers a single question: does the operator serve a JSON object at the well-known certificate endpoint that conforms to the protocol-defined schema?

Specifically, the test verifies:

1. **Endpoint presence** — `GET /.well-known/banza/certificate.json` returns HTTP 200. The endpoint exists, is publicly accessible without authentication, and responds.

2. **Content negotiation** — `Content-Type` header contains `application/json`. The operator correctly declares the content type.

3. **JSON parsability** — The response body is valid JSON and is a JSON object (not an array or primitive).

4. **Schema conformance** — The JSON object satisfies all constraints in `contracts/federation/operator-certificate.json`:
   - All 11 required fields are present
   - No additional properties
   - `schema_version == "1"`
   - `operator_id` matches pattern `^[a-z0-9][a-z0-9\-]{2,62}[a-z0-9]$`
   - `certification_level` is integer in range [0, 4]
   - `protocol_version` matches pattern `^\d+\.\d+$`
   - `capabilities` is an array of unique strings
   - `public_key` matches pattern `^ed25519:[A-Za-z0-9_-]{43}$`
   - `issued_at` and `expires_at` are non-empty strings
   - `issuer == "BANZA"`
   - `issuer_key_id` is a string
   - `signature` matches pattern `^[A-Za-z0-9_-]{86}$`

This test verifies structure and presence only. It does not verify that the signature is cryptographically valid, that the certificate is not expired, or that the operator implements trust enforcement.

**Contract unlocked:** `contracts/federation/operator-certificate.json` is now an executable conformance artifact, not just documentation.

---

## What FED-CERT-001 Does NOT Prove

| Not Proven | Tested By | Notes |
|---|---|---|
| ed25519 signature is cryptographically valid | FED-CERT-002 | Requires real BANZA root keypair; WP-002 |
| Certificate is not expired (`expires_at > now`) | FED-CERT-003 | Timestamp check; runner wall clock |
| Certificate lifetime ≤ 90 days (INV-FED-006) | FED-CERT-007 | Arithmetic check |
| Operator rejects expired remote cert (Step 2.4) | FED-CERT-008 | Requires Sim Op B + Operator A trust engine |
| Operator rejects BRL-revoked operator (Step 2.6) | FED-CERT-009 | Requires BRL server + trust engine |
| Cert/manifest operator_id binding (Step 2.9) | FED-CERT-010 | Requires manifest + trust engine |
| Key rotation fetch on unknown issuer_key_id | FED-CERT-011 | Requires BANZA key manifest server |
| INV-TRUST-001 (signature chain from root) | FED-CERT-002 | Cryptographic invariant |
| INV-TRUST-002 (no expired cert accepted) | FED-CERT-003, FED-TRUST-003 | Runtime enforcement |
| INV-TRUST-003 (BRL revocation) | FED-TRUST-005 | Requires BRL infrastructure |
| Cross-operator routing | FED-TRUST through FED-OBL | Requires full federation implementation |

---

## Evidence Captured

The runner captures the following evidence items per the `FEDERATION_CERTIFICATION_EVIDENCE_MODEL.md §1.1` specification:

| Evidence Item | Value |
|---|---|
| `cert.http_status` | 200 |
| `cert.http_headers` | `{"content-type": "application/json; charset=utf-8", ...}` |
| `cert.raw_json` | Full certificate JSON object |
| `cert.schema_validation_result` | `{"valid": true, "errors": []}` |

Evidence is embedded in the JSON report generated with `--output <file>`.

---

## Next Tests Unlocked

Completing FED-CERT-001 establishes the foundation for the next implementation slice:

### Immediate (Slice 1 — WP-002)

| Test | What's Needed |
|---|---|
| FED-CERT-002 | Real ed25519 signing in `trust_root.py` (`cryptography` library) |
| FED-CERT-003 | Runner timestamp comparison (runner only, no new operator work) |
| FED-CERT-004 | operator_id regex — already in `run_fed.py`; enable after WP-002 |
| FED-CERT-005 | public_key format + base64url decode — already in runner |
| FED-CERT-006 | `issuer == "BANZA"` — already in runner |
| FED-CERT-007 | Lifetime ≤ 90 days — already in runner |

**FED-CERT-002 through FED-CERT-007 require only `trust_root.py` to be upgraded with real ed25519 (`cryptography` package). No Operator A changes needed.**

### After WP-002 (Slice 2 — requires Sim Op B + Operator A trust engine)

| Test | What's Needed |
|---|---|
| FED-CERT-008 | Sim Op B (`tools/banza-conformance/sim_b/`) + Operator A trust engine |
| FED-CERT-009 | BRL server + Operator A BRL fetcher |
| FED-CERT-010 | Operator A Step 2.9 (cert/manifest binding) |
| FED-CERT-011 | BANZA key manifest server + Operator A key rotation |

### After FED-CERT full PASS → FED-DISC

| Test | What's Needed |
|---|---|
| FED-DISC-001 | `contracts/federation/federation-manifest.json` + manifest endpoint extension |
| FED-DISC-002 through -008 | Manifest fields in Operator A + runner FED-DISC suite |

---

## Dependency Graph (from this point)

```
FED-CERT-001 ✓ PASS  ← you are here
    │
FED-CERT-002 through -007  (add real ed25519 to trust_root.py)
    │
FED-CERT-008 through -011  (add Sim Op B + Operator A trust engine)
    │
FED-DISC PASS  (federation manifest extension)
    │
FED-TRUST PASS  (full 9-step trust protocol)
    │
FED-ROUTE PASS  (routing wire protocol)
    │
FED-EXEC + FED-OBL PASS  (transfer execution + obligations)
    │
L3 Blocking Suites: ALL PASS
    │
[FED-FAIL-001/004/005 + FED-EVT] → L3 CERTIFICATION GRANTED
```

---

## Invariants Now Testable

| Invariant | Status |
|---|---|
| Schema conformance of `operator-certificate.json` | **Enforceable** — `validate_operator_certificate()` in runner |
| `issuer == "BANZA"` | **Enforceable** — schema const validation |
| `operator_id` pattern | **Enforceable** — schema pattern validation |
| `public_key` format (ed25519 prefix + base64url) | **Enforceable** — schema pattern validation |
| `signature` format (86 base64url chars) | **Enforceable** — schema pattern validation |
| INV-TRUST-001 (cryptographic validity) | Deferred to FED-CERT-002 |
| INV-TRUST-002 (expiry enforcement) | Deferred to FED-CERT-003 |
| INV-TRUST-003 (BRL rejection) | Deferred to FED-TRUST-005 |
