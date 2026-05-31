# L3 Cryptographic Integrity Hardening Report

**Task ID:** L3-PRODUCTION-HARDENING-CRYPTO-INTEGRITY-001  
**Date:** 2026-05-31  
**Status:** COMPLETE  

---

## Objective

Harden the L3 federation conformance runner cryptographically by adding:

1. BRL ed25519 signature verification enforced before revocation decisions.
2. Tamper-evident evidence package signing using the test BANZA root key.

These address production blockers 2 and 3 from `L3_CERTIFICATION_READINESS_REPORT.md`.

---

## BRL Signature Model

### Invariant

**INV-TRUST-005**: An unsigned or unverifiable BRL MUST be treated as absent. The trust engine MUST fail closed when BRL signature verification fails.

### Signed payload structure

```json
{
  "schema_version": "1",
  "issuer": "BANZA",
  "issuer_key_id": "<key-id>",
  "issued_at": "<ISO-8601>",
  "expires_at": "<ISO-8601>",
  "revoked": [...],
  "signature": "<base64url-ed25519>"
}
```

### Signing rule (ADR-026 canonical)

1. Remove `signature` field from BRL dict.
2. Serialize remaining fields: `json.dumps(payload, sort_keys=True, separators=(',',':'))`.
3. Encode as UTF-8.
4. Sign with ed25519 private key (test BANZA root or production root).
5. Store signature as base64url without padding.

### Verification rule

1. Fetch BRL.
2. If `issuer_key_id` is present and crypto is available: look up public key in runner key registry.
3. If key not found: fail closed (`brl_issuer_key_id_unknown`).
4. Reconstruct canonical bytes (same as signing, excluding `signature`).
5. Verify ed25519 signature.
6. If verification fails: fail closed (`brl_signature_invalid`).
7. Then proceed to expiry/staleness and revocation checks.

### Trust engine enforcement (fixture_server.py Step 2.6)

```
fetch BRL → verify signature → verify issuer_key_id → check expiry → check revocations
                ↓ on failure
          fail closed: rejection_reason = "brl_signature_invalid"
```

---

## Evidence Package Signature Model

### Signed payload

Report JSON minus `{package_signature, evidence_hash}`, serialized with `json.dumps(sort_keys=True, separators=(',',':'))`.

### Signed fields added

```json
{
  "evidence_hash": "<sha256-hex>",
  "package_signature": {
    "algorithm": "ed25519",
    "issuer": "BANZA_TEST_ROOT",
    "issuer_key_id": "<key-id>",
    "runner_public_key": "ed25519:<base64url>",
    "signature": "<base64url>",
    "signed_at": "<ISO-8601>",
    "signed_payload": "canonical_json_sha256"
  }
}
```

### Verification procedure

```python
from trust_root import verify_evidence_package_signature
ok, detail = verify_evidence_package_signature(report, root_public_key_bytes)
```

The verifier:
1. Reconstructs canonical JSON of report (excluding `package_signature` and `evidence_hash`).
2. Verifies ed25519 signature against the public key embedded in `runner_public_key` (confirmed against a trusted key store).
3. Recomputes `evidence_hash` and compares to the reported value.
4. Returns `(True, "evidence package signature valid")` or `(False, <reason>)`.

---

## Files Changed

| File | Change |
|------|--------|
| `tools/banza-conformance/runner_infra.py` | Added `configure_signing_keys()` method; updated all `set_brl_*` methods to auto-use stored keys (INV-TRUST-005) |
| `tools/banza-conformance/run_fed.py` | Initialized `root_priv`, `root_pub`, `key_id` to `None`; added `infra.configure_signing_keys()` call; added evidence package signing to report output |
| `tools/banza-conformance/trust_root.py` | No changes — BRL and evidence signing already implemented in previous phase |
| `tools/banza-conformance/fixture_server.py` | No changes — BRL signature enforcement already implemented in previous phase |
| `tests/unit/test_crypto_integrity.py` | **New** — 15 unit tests covering BRL and evidence signing/verification |
| `docs/federation/L3_CRYPTO_INTEGRITY_HARDENING_REPORT.md` | **New** — this report |

---

## Tests Run

### Unit tests (15 tests, all pass)

```
tests/unit/test_crypto_integrity.py::test_sign_brl_produces_signature PASSED
tests/unit/test_crypto_integrity.py::test_verify_brl_signature_passes_for_valid_brl PASSED
tests/unit/test_crypto_integrity.py::test_verify_brl_signature_fails_for_tampered_payload PASSED
tests/unit/test_crypto_integrity.py::test_verify_brl_signature_fails_for_wrong_key PASSED
tests/unit/test_crypto_integrity.py::test_verify_brl_signature_fails_for_placeholder_signature PASSED
tests/unit/test_crypto_integrity.py::test_verify_brl_signature_fails_for_missing_signature PASSED
tests/unit/test_crypto_integrity.py::test_brl_with_revoked_entries_signs_and_verifies PASSED
tests/unit/test_crypto_integrity.py::test_sign_evidence_package_adds_required_fields PASSED
tests/unit/test_crypto_integrity.py::test_verify_evidence_package_signature_passes_for_valid_report PASSED
tests/unit/test_crypto_integrity.py::test_verify_evidence_package_fails_for_tampered_field PASSED
tests/unit/test_crypto_integrity.py::test_verify_evidence_package_fails_for_wrong_key PASSED
tests/unit/test_crypto_integrity.py::test_evidence_hash_matches_canonical_payload PASSED
tests/unit/test_crypto_integrity.py::test_verify_evidence_fails_when_package_signature_missing PASSED
tests/unit/test_crypto_integrity.py::test_runner_infra_auto_signs_brl_after_configure_signing_keys PASSED
tests/unit/test_crypto_integrity.py::test_runner_infra_bad_signature_brl_does_not_verify PASSED

15 passed in 0.07s
```

### Conformance runner (79 tests, all pass)

```
FED-CERT-001–011: 11 passed
FED-DISC-001–008:  8 passed
FED-TRUST-001–009: 9 passed
FED-ROUTE-001–012: 12 passed
FED-EXEC-001–008:  8 passed
FED-OBL-001–007:   7 passed
FED-EVT-001–006:   6 passed
FED-SETTLE-001–010: 10 passed
FED-FAIL-001–008:   8 passed

Total: 79 passed, 0 failed, 0 skipped
```

### Other checks

- `make identity-check`: PASS — BANZA operator neutrality verified
- `git diff --check`: PASS — no trailing whitespace

---

## Evidence Output Sample

```json
{
  "evidence_hash": "883d89b4908465193ba3749eb5b05ae1...",
  "package_signature": {
    "algorithm": "ed25519",
    "issuer": "BANZA_TEST_ROOT",
    "issuer_key_id": "test-banza-key-2026-05",
    "runner_public_key": "ed25519:...",
    "signature": "rbRpozDGGXHt8j62PoXi...",
    "signed_at": "2026-05-31T19:45:17.872827+00:00",
    "signed_payload": "canonical_json_sha256"
  }
}
```

### FED-TRUST-001 Step 2.6 BRL evidence

```json
{
  "step": "2.6",
  "name": "brl_check",
  "status": "pass",
  "brl_expires_at": "2026-06-01T02:45:16Z",
  "brl_issued_at": "2026-05-31T19:45:16Z",
  "brl_fetched_at": "2026-05-31T19:45:16Z",
  "brl_issuer_key_id": "test-banza-key-2026-05",
  "brl_signature_valid": true,
  "brl_sig_detail": "BRL signature valid",
  "revoked_count": 0
}
```

---

## Negative Test Coverage

The following negative tests are implemented and pass:

| Test | What it proves |
|------|----------------|
| `test_verify_brl_signature_fails_for_tampered_payload` | Injecting a revocation entry without re-signing fails verification |
| `test_verify_brl_signature_fails_for_wrong_key` | BRL signed with key A rejects against key B |
| `test_verify_brl_signature_fails_for_placeholder_signature` | `"A" * 86` placeholder does not verify |
| `test_verify_brl_signature_fails_for_missing_signature` | Unsigned BRL treated as absent |
| `test_verify_evidence_package_fails_for_tampered_field` | Mutating any evidence field after signing fails |
| `test_runner_infra_bad_signature_brl_does_not_verify` | `set_brl_bad_signature()` fixture fails verification |

**Note:** A spec-enumerated `FED-TRUST-010` test for BRL bad-signature fail-closed behavior is not included because no corresponding ADR or test spec entry exists yet. The `set_brl_bad_signature()` fixture and `verify_brl_signature()` function are ready; a future ADR can add the spec test vector.

---

## Remaining Production Blockers

| # | Blocker | Status |
|---|---------|--------|
| 1 | ADR-028 for certification level naming | Open — not addressed in this task |
| 2 | Evidence package signing by the runner | **RESOLVED** |
| 3 | BRL signature verification in the runner | **RESOLVED** |
| 4 | Production BANZA root key establishment | Open — not addressed in this task |
| 5 | Real two-operator interoperability test | Open — not addressed in this task |

**Production blockers reduced from 5 to 3.**

---

## Updated Production Readiness Status

| Criterion | Before | After |
|-----------|--------|-------|
| L3 conformance executable end-to-end | YES | YES |
| BRL cryptographically verified before revocation | NO | **YES** |
| Tampered BRL fails closed | NO | **YES** |
| Evidence package tamper-evident | NO | **YES** |
| Tampered evidence fails verification | NO | **YES** |
| Production root key established | NO | NO |
| Real two-operator test | NO | NO |
| ADR-028 naming | NO | NO |

**Verdict:** L3 Federation Certification is executable and cryptographically hardened for conformance purposes. It remains NOT yet production-ready (3 blockers remain).
