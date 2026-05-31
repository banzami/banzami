# FED-CERT-008 through FED-CERT-011 Report

**Document ID:** FED-CERT-008-TO-011-REPORT-001  
**Date:** 2026-05-31  
**Status:** ALL 11 PASS — operator peer trust verification layer complete  
**Authority:** FEDERATION_TEST_SUITE_SPEC.md, ADR-026-FEDERATION-TRUST-MODEL.md

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
```

---

## Commands

```bash
# Terminal 1 — start fixture server (Operator A)
python3 tools/banza-conformance/fixture_server.py --port 8099

# Terminal 2 — run full FED-CERT suite
python3 tools/banza-conformance/run.py --federation --url http://localhost:8099
```

---

## Operator Trust Engine Surface

The operator under test must expose:

```
POST /conformance/federation/verify-peer
Body:    { "peer_manifest_url": "http://..." }
Returns: {
  "trusted": bool,
  "rejection_reason": str | null,
  "steps": [{"step": "2.1" … "2.9", "name": str, "status": "pass"|"fail", ...}]
}
```

This endpoint is the conformance mechanism for testing the ADR-026 9-step trust protocol without requiring full routing to be implemented.

### Extended Setup Payload

```
POST /conformance/setup
{
  "certificate":       { ...Operator A signed cert... },
  "banza_root_keys":   { "test-banza-key-2026-05": "ed25519:<43 chars>" },
  "brl_url":           "http://localhost:<port>/federation/revocation-list.json",
  "key_manifest_url":  "http://localhost:<port>/federation/public-keys.json"
}
```

---

## Simulated Operator B Behavior

`runner_infra.RunnerInfra` starts two embedded servers per test run:

| Server | Default Port | Endpoints |
|---|---|---|
| SimBServer | dynamic free port | `GET /.well-known/banza/operator.json`, `GET /.well-known/banza/certificate.json` |
| TrustRootServer | dynamic free port | `GET /federation/revocation-list.json`, `GET /federation/public-keys.json` |

The runner configures these servers between tests:

| Test | Sim Op B Cert | BRL |
|---|---|---|
| FED-CERT-008 | CERT-B-EXPIRED (real sig, `expires_at` 10 days ago) | Empty |
| FED-CERT-009 | CERT-B-VALID (real sig, not expired) | Contains "operator-b-test" as revoked |
| FED-CERT-010 | CERT-B-MISMATCHED (`operator_id="some-other-operator"`) | Empty |
| FED-CERT-011 | CERT-B-SECONDARY (signed with secondary root key) | Empty |

All Sim Op B certs are **dynamically generated with real ed25519 signatures** per runner invocation. Static fixture files serve as documentation only.

---

## ADR-026 9-Step Trust Protocol Mapping

The trust engine in `fixture_server.py` implements all 9 steps. Step IDs match the test spec numbering:

| Step ID | Name | Description | Tests |
|---|---|---|---|
| 2.1 | `manifest_fetch` | GET peer manifest; parse JSON; extract `operator_id` | All |
| 2.2 | `certificate_fetch` | GET `manifest.certificate_url`; parse cert JSON | All |
| 2.3 | `signature_verify` | `ed25519_verify(BANZA_root_PK, canonical_json, sig)` | All |
| 2.3_key_fetch | `key_manifest_fetch` | Fetch key manifest on unknown `issuer_key_id` | FED-CERT-011 |
| 2.4 | `expiry_check` | `expires_at > now` AND `issued_at ≤ now` | **FED-CERT-008 fails here** |
| 2.5 | `level_check` | `certification_level >= 3` | — |
| 2.6 | `brl_check` | Fetch BRL; check `operator_id` not in `revoked` | **FED-CERT-009 fails here** |
| 2.7 | `federation_support_check` | `manifest.supports_federation == true` | — |
| 2.8 | `routing_capability_check` | `"cross_operator_routing" in cert.capabilities` | — |
| 2.9 | `operator_id_binding` | `cert.operator_id == manifest.operator_id` | **FED-CERT-010 fails here** |

For **FED-CERT-011**: Step 2.3_key_fetch inserts between Step 2.2 and Step 2.3. The engine fetches the key manifest, adds the new key to its local registry, then proceeds with Step 2.3 successfully → `trusted: true`.

---

## Tests Implemented

| Test | Purpose | Spec Step | Invariant | Severity |
|---|---|---|---|---|
| FED-CERT-008 | Operator rejects expired peer cert | Step 2.4 | INV-TRUST-002 | **CRITICAL** |
| FED-CERT-009 | Operator rejects BRL-revoked peer | Step 2.6 | INV-TRUST-003, INV-FED-007 | **CRITICAL** |
| FED-CERT-010 | Operator rejects cert/manifest mismatch | Step 2.9 | INV-TRUST-001 | **CRITICAL** |
| FED-CERT-011 | Operator fetches key on unknown issuer_key_id | 2.3_key_fetch | — | STANDARD |

3 CRITICAL tests enforce INV-TRUST-001, INV-TRUST-002, and INV-TRUST-003.

---

## Evidence Captured Per Test

### FED-CERT-008

| Item | Value |
|---|---|
| `peer_manifest_url` | Sim Op B manifest URL |
| `peer_operator_id` | "operator-b-test" |
| `trusted` | false |
| `rejection_reason` | "certificate_expired" |
| `trust_step_results` | All 9 steps (2.4 = fail) |

### FED-CERT-009

| Item | Value |
|---|---|
| `peer_manifest_url` | Sim Op B manifest URL |
| `brl_revoked` | ["operator-b-test"] |
| `trusted` | false |
| `rejection_reason` | "operator_revoked" |
| `trust_step_results` | Steps 2.3-2.5 = pass, step 2.6 = fail |

### FED-CERT-010

| Item | Value |
|---|---|
| `cert_operator_id` | "some-other-operator" |
| `manifest_operator_id` | "operator-b-test" |
| `trusted` | false |
| `rejection_reason` | "operator_id_mismatch" |
| `trust_step_results` | Steps 2.3-2.8 = pass, step 2.9 = fail |

### FED-CERT-011

| Item | Value |
|---|---|
| `secondary_issuer_key_id` | "test-banza-key-2026-05-secondary" |
| `trusted` | true |
| `key_fetch_step` | `{"step": "2.3_key_fetch", "status": "pass", "key_id": "..."}` |
| `trust_step_results` | Key fetch logged; all subsequent steps pass |

---

## Files Added

| File | Purpose |
|---|---|
| `tools/banza-conformance/runner_infra.py` | `RunnerInfra` class — starts/stops `SimBServer` (Sim Op B) + `TrustRootServer` (BRL + key manifest) in daemon threads |

## Files Modified

| File | Change |
|---|---|
| `tools/banza-conformance/trust_root.py` | Added `issued_at_override` / `expires_at_override` params to `generate_test_certificate`; added `generate_brl()` and `generate_key_manifest()` |
| `tools/banza-conformance/fixture_server.py` | Switched to `ThreadingHTTPServer`; added trust engine (`trust_verify_peer`); added `POST /conformance/federation/verify-peer`; extended `POST /conformance/setup` to store BANZA root keys, BRL URL, key manifest URL |
| `tools/banza-conformance/run_fed.py` | Added `RunnerInfra` import; extended `setup_operator_for_federation`; added FED-CERT-008 through 011; updated `run_suite_fed_cert`; updated `run_federation_mode` to start infra and generate all test certs |

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
| **Operator rejects expired remote cert (Step 2.4)** | **FED-CERT-008** |
| **Operator rejects BRL-revoked remote operator (Step 2.6)** | **FED-CERT-009** |
| **Operator rejects cert/manifest operator_id mismatch (Step 2.9)** | **FED-CERT-010** |
| **Operator performs key rotation on unknown issuer_key_id** | **FED-CERT-011** |

---

## Invariants Now Enforceable

| Invariant | Status |
|---|---|
| INV-TRUST-001 — cert signature chain from BANZA root | **ENFORCEABLE** — FED-CERT-002, 006, 010 |
| INV-TRUST-002 — no expired certificate accepted | **ENFORCEABLE** — FED-CERT-003, **008** |
| INV-TRUST-003 — BRL-revoked operator rejected | **ENFORCEABLE** — **FED-CERT-009** |
| INV-FED-006 — cert lifetime ≤ 90 days for L3+ | **ENFORCEABLE** — FED-CERT-007 |
| INV-TRUST-004 — federation flag needs L3+ cert | Deferred to FED-DISC-007 |
| INV-TRUST-006 — BRL max 6h staleness | Deferred to FED-TRUST-009 |

---

## What Remains Unproven

| Not Yet Proven | Tested By | Notes |
|---|---|---|
| Federation manifest extension fields | FED-DISC-001–008 | Requires `federation-manifest.json` |
| Full 9-step trust protocol across suites | FED-TRUST-001–009 | Requires FED-DISC complete |
| Routing wire protocol | FED-ROUTE-001–012 | Requires Operator A routing endpoint |
| Transfer execution semantics | FED-EXEC-001–008 | Requires Operator A ledger + obligation |
| Obligation lifecycle | FED-OBL-001–007 | Requires Operator A obligation engine |

---

## Next Tests

FED-CERT is now **complete**. The next suite is **FED-DISC** (8 tests, blocking):

```
FED-CERT 001–011 ✓ ALL PASS  ← you are here
    │
FED-DISC 001–008  (federation manifest extension fields)
    - contracts/federation/federation-manifest.json (not yet created)
    - Operator A: extended /.well-known/banza/operator.json with federation fields
    │
FED-TRUST 001–009  (full trust protocol; requires FED-DISC)
    │
FED-ROUTE + FED-EXEC + FED-OBL  (routing + obligations)
    │
L3 Blocking Suites: ALL PASS → L3 CERTIFICATION
```
