# FED-DISC-001 through FED-DISC-008 Report

**Document ID:** FED-DISC-001-TO-008-REPORT-001  
**Date:** 2026-05-31  
**Status:** ALL 19 PASS — federation manifest discovery layer complete  
**Authority:** FEDERATION_TEST_SUITE_SPEC.md, FEDERATION_CONTRACT_SURFACE.md, ADR-026-FEDERATION-TRUST-MODEL.md

---

## Result

```
[Suite] Certificate Validation (blocking=True)
  ✓ FED-CERT-001 — Certificate Present at Well-Known URL
  ✓ FED-CERT-002 — Certificate Signature Verifies Against Test BANZA Root
  ✓ FED-CERT-003 — Certificate Not Expired
  ✓ FED-CERT-004 — operator_id Matches Declared Format
  ✓ FED-CERT-005 — public_key Format Correct
  ✓ FED-CERT-006 — issuer is Exactly "BANZA"
  ✓ FED-CERT-007 — Lifetime ≤ 90 Days for L3+
  ✓ FED-CERT-008 — Expired Certificate Fails Trust Step 2.4
  ✓ FED-CERT-009 — Revoked Operator Rejected by BRL Check
  ✓ FED-CERT-010 — Certificate-Manifest operator_id Binding
  ✓ FED-CERT-011 — Unknown issuer_key_id Triggers Key Fetch
  → 11 passed, 0 failed, 0 skipped

[Suite] Discovery and Manifest Validation (blocking=True)
  ✓ FED-DISC-001 — Manifest Present at Well-Known URL
  ✓ FED-DISC-002 — supports_federation == true
  ✓ FED-DISC-003 — cross_operator_routing == true
  ✓ FED-DISC-004 — certificate_url Accessible and Returns Valid Certificate
  ✓ FED-DISC-005 — interop_endpoint Reachable
  ✓ FED-DISC-006 — supported_currencies Non-Empty
  ✓ FED-DISC-007 — supports_federation Cannot Be True Without Valid L3+ Certificate
  ✓ FED-DISC-008 — netting_interval_hours Within Bounds
  → 8 passed, 0 failed, 0 skipped
```

---

## Commands

```bash
# Terminal 1 — start fixture server (Operator A)
python3 tools/banza-conformance/fixture_server.py --port 8099

# Terminal 2 — run full FED-CERT + FED-DISC suite
python3 tools/banza-conformance/run.py --federation --url http://localhost:8099

# Run only FED-DISC
python3 tools/banza-conformance/run.py --federation --fed-suite disc --url http://localhost:8099
```

---

## Contract Created

### `contracts/federation/federation-manifest.json`

Canonical JSON Schema for the BANZA federation manifest extension. Defines the additional fields an operator must serve at `/.well-known/banza/operator.json` to participate in federation.

**Required fields:**

| Field | Type | Constraint |
|---|---|---|
| `federation_version` | string | const `"1"` |
| `certificate_url` | string (URI) | accessible, returns valid cert |
| `interop_endpoint` | string (URI) | TCP-reachable |
| `supports_federation` | boolean | `true` for federation |
| `cross_operator_routing` | boolean | `true` when `supports_federation=true` |
| `cross_operator_settlement` | boolean | participation in netting |
| `federation_capabilities` | object | see sub-fields |
| `federation_capabilities.routing_version` | string | const `"1"` |
| `federation_capabilities.settlement_version` | string | const `"1"` |
| `federation_capabilities.supported_currencies` | array | non-empty, ISO 4217 |
| `federation_capabilities.netting_interval_hours` | integer | 1–168 |

**if/then constraint:** `supports_federation == true` → `cross_operator_routing` MUST be `true`.

---

## Fixture Server Changes

`fixture_server.py` now serves `GET /.well-known/banza/operator.json` with a dynamically-built federation manifest. The manifest is constructed at serve time from:

- `operator_id` and `certification_level` from the cert stored in setup state
- `certificate_url` and `interop_endpoint` built from the `Host` request header

This allows the manifest to reference the correct localhost port for `certificate_url` and `interop_endpoint`, enabling FED-DISC-004 (certificate_url follow-through) and FED-DISC-005 (endpoint reachability) to pass.

---

## Fixtures Added

| File | Purpose |
|---|---|
| `conformance/fixtures/federation/MANIFEST-VALID.json` | Complete federation-capable manifest for Operator A |
| `conformance/fixtures/federation/MANIFEST-B-VALID.json` | Simulated Operator B valid manifest |
| `conformance/fixtures/federation/MANIFEST-FEDERATION-NO-CERT.json` | `supports_federation=true` but cert is L2 — FED-DISC-007 |
| `conformance/fixtures/federation/MANIFEST-B-NO-FEDERATION.json` | `supports_federation=false` — FED-TRUST-006 |
| `conformance/fixtures/federation/MANIFEST-NO-FEDERATION.json` | Operator A variant with federation disabled |
| `conformance/fixtures/federation/MANIFEST-CAPABILITY-MISMATCH.json` | `supports_federation=true` but `cross_operator_routing=false` (schema violation) |
| `conformance/fixtures/federation/MANIFEST-UNSUPPORTED-VERSION.json` | `federation_version="99"` (invalid version) |
| `conformance/fixtures/federation/MANIFEST-MISSING-CERTIFICATE-URL.json` | Missing `certificate_url` field |
| `conformance/fixtures/federation/MANIFEST-WRONG-OPERATOR-ID.json` | `operator_id` does not match cert |

---

## Tests Implemented

| Test | Purpose | Invariant | Severity |
|---|---|---|---|
| FED-DISC-001 | Manifest endpoint returns HTTP 200, validates against schema | — | STANDARD |
| FED-DISC-002 | `supports_federation === true` (boolean) | INV-TRUST-004 | STANDARD |
| FED-DISC-003 | `cross_operator_routing === true` | INV-FED-003 | STANDARD |
| FED-DISC-004 | `certificate_url` accessible; cert valid; `operator_id` bound | INV-TRUST-001 | STANDARD |
| FED-DISC-005 | `interop_endpoint` TCP-reachable (any HTTP response) | INV-FED-003 | STANDARD |
| FED-DISC-006 | `supported_currencies` non-empty; all ISO 4217 | — | STANDARD |
| **FED-DISC-007** | **L2 cert rejected by trust engine (INV-TRUST-004)** | **INV-TRUST-004** | **CRITICAL** |
| FED-DISC-008 | `netting_interval_hours` integer in [1, 168] | — | STANDARD |

---

## FED-DISC-007 Trust Engine Interaction

FED-DISC-007 is the only FED-DISC test that requires the runner infrastructure and the operator trust engine.

**Scenario:**
- Runner configures Sim Op B with a manifest declaring `supports_federation=true, cross_operator_routing=true`
- Sim Op B serves `CERT-B-L2`: a validly-signed certificate with `certification_level=2` (L2)
- Runner calls `POST /conformance/federation/verify-peer` on Operator A with Sim Op B's manifest URL
- Operator A runs the 9-step ADR-026 trust protocol

**Trust protocol execution for FED-DISC-007:**

| Step | Result |
|---|---|
| 2.1 manifest_fetch | PASS — manifest accessible |
| 2.2 certificate_fetch | PASS — cert accessible |
| 2.3 signature_verify | PASS — valid ed25519 signature |
| 2.4 expiry_check | PASS — not expired |
| **2.5 level_check** | **FAIL — `certification_level=2 < 3`** |
| 2.6–2.9 | Not reached |

**Result:** `trusted=false`, `rejection_reason="certification_level_insufficient"` — enforces INV-TRUST-004.

---

## Evidence Captured Per Test

### FED-DISC-001

| Item | Value |
|---|---|
| `manifest_url` | `http://localhost:8099/.well-known/banza/operator.json` |
| `manifest_http_status` | 200 |
| `manifest_content_type` | `application/json; charset=utf-8` |
| `manifest_schema_valid` | true |
| `manifest_operator_id` | `"operator-a-test"` |
| `manifest_federation_version` | `"1"` |

### FED-DISC-004

| Item | Value |
|---|---|
| `manifest_operator_id` | `"operator-a-test"` |
| `certificate_url` | `http://localhost:8099/.well-known/banza/certificate.json` |
| `cert_http_status` | 200 |
| `cert_operator_id` | `"operator-a-test"` |
| `operator_id_match` | true |

### FED-DISC-007

| Item | Value |
|---|---|
| `cert_b_level` | 2 |
| `trusted` | false |
| `rejection_reason` | `"certification_level_insufficient"` |
| `step_2.5` | `{"step": "2.5", "status": "fail", "reason": "certification_level_insufficient", ...}` |

---

## Files Added

| File | Purpose |
|---|---|
| `contracts/federation/federation-manifest.json` | Canonical JSON Schema for federation manifest extension |
| `conformance/fixtures/federation/MANIFEST-*.json` (×9) | Static documentation fixtures |

## Files Modified

| File | Change |
|---|---|
| `tools/banza-conformance/fixture_server.py` | Added `GET /.well-known/banza/operator.json` — serves dynamic federation manifest |
| `tools/banza-conformance/run_fed.py` | Added `validate_federation_manifest`, `_fetch_manifest`, `_find_manifest_schema_path`, FED-DISC-001–008, `run_suite_fed_disc`, `cert_b_l2` generation; updated `run_federation_mode` to run both suites |

---

## What Is Now Proven

| Assertion | Proven By |
|---|---|
| Certificate endpoint + schema valid | FED-CERT-001 |
| ed25519 signature valid (INV-TRUST-001) | FED-CERT-002 |
| Certificate not expired (INV-TRUST-002) | FED-CERT-003 |
| operator_id format | FED-CERT-004 |
| public_key is 32-byte ed25519 | FED-CERT-005 |
| issuer == "BANZA" | FED-CERT-006 |
| Lifetime ≤ 90 days (INV-FED-006) | FED-CERT-007 |
| Operator rejects expired remote cert (Step 2.4) | FED-CERT-008 |
| Operator rejects BRL-revoked operator (Step 2.6) | FED-CERT-009 |
| Operator rejects cert/manifest mismatch (Step 2.9) | FED-CERT-010 |
| Operator performs key rotation on unknown issuer_key_id | FED-CERT-011 |
| **Manifest endpoint exists, HTTP 200, validates against federation-manifest.json** | **FED-DISC-001** |
| **supports_federation is true (boolean)** | **FED-DISC-002** |
| **cross_operator_routing is true (INV-FED-003)** | **FED-DISC-003** |
| **certificate_url accessible; cert valid; operator_id bound (INV-TRUST-001)** | **FED-DISC-004** |
| **interop_endpoint TCP-reachable (INV-FED-003)** | **FED-DISC-005** |
| **supported_currencies non-empty, all ISO 4217** | **FED-DISC-006** |
| **L2 cert rejected by trust engine (INV-TRUST-004)** | **FED-DISC-007** |
| **netting_interval_hours integer in [1, 168]** | **FED-DISC-008** |

---

## Invariants Now Enforceable

| Invariant | Status |
|---|---|
| INV-TRUST-001 — cert signature chain from BANZA root | **ENFORCEABLE** — FED-CERT-002, 006, 010, DISC-004 |
| INV-TRUST-002 — no expired certificate accepted | **ENFORCEABLE** — FED-CERT-003, 008 |
| INV-TRUST-003 — BRL-revoked operator rejected | **ENFORCEABLE** — FED-CERT-009 |
| INV-TRUST-004 — federation flag requires L3+ cert | **ENFORCEABLE** — **FED-DISC-007** |
| INV-FED-003 — routing endpoint declared and reachable | **ENFORCEABLE** — FED-DISC-003, 005 |
| INV-FED-006 — cert lifetime ≤ 90 days for L3+ | **ENFORCEABLE** — FED-CERT-007 |
| INV-FED-007 — revoked operators excluded | **ENFORCEABLE** — FED-CERT-009 |
| INV-TRUST-006 — BRL max 6h staleness | Deferred to FED-TRUST-009 |

---

## What Remains Unproven

| Not Yet Proven | Tested By | Notes |
|---|---|---|
| Full 9-step trust protocol (all steps) | FED-TRUST-001–009 | Steps 2.3/2.4/2.5/2.6/2.7/2.8/2.9 tested via FED-CERT/DISC; step 2.7 not yet a standalone test |
| Routing wire protocol | FED-ROUTE-001–012 | Requires Operator A routing endpoint |
| Transfer execution semantics | FED-EXEC-001–008 | Requires Operator A ledger + obligation |
| Obligation lifecycle | FED-OBL-001–007 | Requires Operator A obligation engine |

---

## Next Tests

FED-DISC is now **complete**. The next suite is **FED-TRUST** (9 tests, blocking):

```
FED-CERT 001–011 ✓ ALL PASS
    │
FED-DISC 001–008 ✓ ALL PASS  ← you are here
    │
FED-TRUST 001–009  (full trust protocol across suites; requires FED-DISC)
    │
FED-ROUTE + FED-EXEC + FED-OBL  (routing + obligations)
    │
L3 Blocking Suites: ALL PASS → L3 CERTIFICATION
```
