# FED-CERT-002 through FED-CERT-007 Report

**Document ID:** FED-CERT-002-TO-007-REPORT-001  
**Date:** 2026-05-31  
**Status:** ALL 7 PASS — cryptographic certificate validation layer complete  
**Authority:** FEDERATION_TEST_SUITE_SPEC.md, L3-FIRST-PASS-IMPLEMENTATION-PLAN-001

---

## Result

```
BANZA Federation Conformance Runner 0.2.0-slice1

[Suite] Certificate Validation (blocking=True)
  ✓ FED-CERT-001 — Certificate Present at Well-Known URL
  ✓ FED-CERT-002 — Certificate Signature Verifies Against Test BANZA Root
  ✓ FED-CERT-003 — Certificate Not Expired
  ✓ FED-CERT-004 — operator_id Matches Declared Format
  ✓ FED-CERT-005 — public_key Format Correct
  ✓ FED-CERT-006 — issuer is Exactly "BANZA"
  ✓ FED-CERT-007 — Lifetime ≤ 90 Days for L3+
  → 7 passed, 0 failed, 0 skipped

FED-CERT-001 through FED-CERT-007: ALL PASS
```

---

## Commands Run

```bash
# Terminal 1 — start fixture server
python3 tools/banza-conformance/fixture_server.py --port 8100

# Terminal 2 — run conformance
python3 tools/banza-conformance/run.py --federation --url http://localhost:8100

# Optional: run only FED-CERT suite
python3 tools/banza-conformance/run.py --federation --url http://localhost:8100 --fed-suite cert
```

---

## Tests Implemented

| Test | Title | Spec Severity | Invariant |
|---|---|---|---|
| FED-CERT-001 | Certificate Present at Well-Known URL | STANDARD | — |
| FED-CERT-002 | Certificate Signature Verifies Against Test BANZA Root | **CRITICAL** | INV-TRUST-001 |
| FED-CERT-003 | Certificate Not Expired | **CRITICAL** | INV-TRUST-002 |
| FED-CERT-004 | operator_id Matches Declared Format | STANDARD | — |
| FED-CERT-005 | public_key Format Correct | STANDARD | — |
| FED-CERT-006 | issuer is Exactly "BANZA" | **CRITICAL** | INV-TRUST-001 |
| FED-CERT-007 | Lifetime ≤ 90 Days for L3+ | STANDARD | INV-FED-006 |

2 CRITICAL tests now enforce INV-TRUST-001 and INV-TRUST-002.

---

## Files Added

| File | Purpose |
|---|---|
| `tools/banza-conformance/requirements.txt` | `cryptography>=41.0.0` dependency declaration |
| `conformance/fixtures/federation/CERT-EXPIRED.json` | Cert with past timestamps; used by FED-CERT-008 |
| `conformance/fixtures/federation/CERT-INVALID-SIGNATURE.json` | Cert with explicitly invalid signature ('B'×86); used by FED-TRUST-002 |
| `conformance/fixtures/federation/CERT-UNKNOWN-ISSUER-KEY-ID.json` | Cert with unknown issuer_key_id; used by FED-CERT-011 |
| `conformance/fixtures/federation/CERT-L2-LEVEL.json` | L2 cert; used by FED-TRUST-004 |
| `conformance/fixtures/federation/CERT-MISMATCHED-OPERATOR-ID.json` | Cert with wrong operator_id; used by FED-CERT-010, FED-TRUST-008 |

## Files Modified

| File | Change |
|---|---|
| `tools/banza-conformance/trust_root.py` | Complete rewrite with real ed25519 support via `cryptography` package |
| `tools/banza-conformance/fixture_server.py` | Added `POST /conformance/setup` endpoint; supports in-memory cert update |
| `tools/banza-conformance/run_fed.py` | Added FED-CERT-002 through FED-CERT-007; updated runner version to 0.2.0-slice1 |
| `tools/banza-conformance/run.py` | Added `--fed-suite` flag |

---

## Cryptographic Decisions

### Algorithm: ed25519 (RFC 8032)

Per ADR-026 §Phase 4, the only acceptable signing algorithm. Selected rationale:
- 32-byte public key, 64-byte signature — minimal certificate payload overhead
- Constant-time verification — important for the routing hot path
- No parameter selection vulnerability — unlike ECDSA, no nonce management
- Widely available: `cryptography` package exposes `Ed25519PrivateKey` / `Ed25519PublicKey`

### Canonical JSON (ADR-026 §Phase 4)

Signed payload construction:
```python
payload = {k: v for k, v in cert.items() if k != "signature"}
canonical = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
```

Rule: all fields **except** `signature`, sorted lexicographically, no whitespace, UTF-8 encoded.

This is the same rule that BANZA production uses when issuing real certificates. The conformance test runner verifies that the operator serves exactly the canonical form that was signed.

### Ephemeral Test Root

A fresh ed25519 keypair is generated per runner invocation. This keypair is the "test BANZA root" for that run. No static keypair is committed to the repository.

Consequence: the conformance test is self-contained and does not depend on BANZA's production signing infrastructure. Any operator can run a conformance test against themselves at any time.

### Signature Encoding

- ed25519 signature = 64 bytes
- base64url-encoded without padding = 86 characters
- Schema pattern: `^[A-Za-z0-9_-]{86}$` — exact match

### Public Key Encoding

- ed25519 public key = 32 bytes
- base64url-encoded without padding = 43 characters
- Format in certificate: `"ed25519:<43 chars>"`
- Schema pattern: `^ed25519:[A-Za-z0-9_-]{43}$` — exact match

### Setup Protocol

The runner generates the cert and delivers it to the operator via `POST /conformance/setup`:

```json
POST /conformance/setup
{
  "certificate": { ...signed cert JSON... }
}
```

This models the actual operator conformance setup flow per FEDERATION_RUNNER_DESIGN.md §3.4. The fixture server accepts this endpoint. Real operators must implement it.

---

## Evidence Captured

### FED-CERT-002 Evidence

| Item | Description |
|---|---|
| `cert.canonical_json_sha256` | SHA-256 of the canonical payload that was signed |
| `cert.canonical_json_length_bytes` | Length of canonical JSON in bytes |
| `cert.signature_bytes_length` | Length of decoded signature (should be 64) |
| `cert.issuer_key_id` | The `issuer_key_id` value from the certificate |
| `cert.signature_verification_result` | `{"verified": true/false, "detail": "..."}` |

### FED-CERT-003 Evidence

| Item | Description |
|---|---|
| `cert.expires_at` | The certificate's `expires_at` value |
| `cert.issued_at` | The certificate's `issued_at` value |
| `cert.runner_timestamp` | Runner's wall clock at test time |
| `cert.expiry_check` | `{expires_at, checked_at, valid: bool, remaining_seconds: int}` |

### FED-CERT-005 Evidence

| Item | Description |
|---|---|
| `cert.public_key` | The `public_key` field value |
| `cert.public_key_pattern_match` | Whether the regex matched |
| `cert.public_key_decoded_length_bytes` | Length of base64url-decoded key (should be 32) |

### FED-CERT-007 Evidence

| Item | Description |
|---|---|
| `cert.issued_at` | Issuance timestamp |
| `cert.expires_at` | Expiry timestamp |
| `cert.lifetime_seconds` | `expires_at - issued_at` in seconds |
| `cert.lifetime_days` | Same in days (rounded to 2 decimal places) |
| `cert.max_lifetime_seconds` | 7,776,000 (90 days) |
| `cert.certification_level` | Certificate's `certification_level` field |

---

## What Is Now Proven

| Assertion | Proven By |
|---|---|
| Certificate endpoint exists, returns HTTP 200 | FED-CERT-001 |
| Content-Type is application/json | FED-CERT-001 |
| Response satisfies `operator-certificate.json` schema | FED-CERT-001 |
| **Certificate was signed by the test BANZA root** (INV-TRUST-001) | **FED-CERT-002** |
| **Certificate is not expired** (INV-TRUST-002) | **FED-CERT-003** |
| operator_id conforms to kebab-case format | FED-CERT-004 |
| public_key is a 32-byte ed25519 key in base64url | FED-CERT-005 |
| issuer is exactly "BANZA" (INV-TRUST-001) | FED-CERT-006 |
| Certificate lifetime ≤ 90 days (INV-FED-006) | FED-CERT-007 |

---

## What Remains Unproven

| Not Yet Proven | Tested By | Requires |
|---|---|---|
| Operator rejects an expired remote cert (Step 2.4) | FED-CERT-008 | Simulated Operator B + trust engine |
| Operator rejects BRL-revoked operator (Step 2.6) | FED-CERT-009 | BRL server + trust engine |
| Cert/manifest operator_id binding (Step 2.9) | FED-CERT-010 | Sim Op B + trust engine |
| Key rotation: unknown issuer_key_id triggers fetch | FED-CERT-011 | BANZA key manifest server + Operator A |
| Federation manifest extension fields | FED-DISC-001 to -008 | `federation-manifest.json` contract |
| 9-step trust protocol | FED-TRUST-001 to -009 | Sim Op B + Operator A trust engine |
| Routing wire protocol | FED-ROUTE-001 to -012 | Operator A routing endpoint |
| Transfer execution semantics | FED-EXEC-001 to -008 | Operator A ledger + obligation engine |
| Obligation lifecycle | FED-OBL-001 to -007 | Operator A obligation engine |

---

## Invariants Now Enforceable

| Invariant | Status |
|---|---|
| INV-TRUST-001 — certificate signature chain from BANZA root | **ENFORCEABLE** — FED-CERT-002, FED-CERT-006 |
| INV-TRUST-002 — no expired certificate accepted | **ENFORCEABLE** — FED-CERT-003 |
| INV-FED-006 — certificate lifetime ≤ 90 days for L3+ | **ENFORCEABLE** — FED-CERT-007 |
| Schema conformance of operator-certificate.json | **ENFORCEABLE** — FED-CERT-001 |
| operator_id format | **ENFORCEABLE** — FED-CERT-004 |
| public_key format (32-byte ed25519 in base64url) | **ENFORCEABLE** — FED-CERT-005 |
| INV-TRUST-003 (BRL revocation) | Deferred to FED-TRUST-005 |
| INV-TRUST-006 (BRL max 6h) | Deferred to FED-TRUST-009 |

---

## Next Tests Unlocked

FED-CERT is now fully instrumented for the positive-test cases (001–007). Completing the full FED-CERT suite (008–011) requires implementing:

1. **Simulated Operator B** — embedded HTTP server in runner (WP-005)
2. **Operator A trust engine** — 9-step trust protocol, BRL fetch, key rotation handling

After FED-CERT is fully complete, the dependency chain is:

```
FED-CERT 001–007 ✓ ALL PASS  ← you are here
    │
FED-CERT 008–011  (trust engine negative tests)
    │
FED-DISC 001–008  (federation manifest extension)
    │
FED-TRUST 001–009  (full 9-step trust protocol)
    │
FED-ROUTE, FED-EXEC, FED-OBL  (routing + obligations)
    │
L3 Blocking Suites: ALL PASS → L3 CERTIFICATION
```
