# L3 Federation Certification — First Pass Implementation Plan

**Document ID:** L3-FIRST-PASS-IMPLEMENTATION-PLAN-001  
**Date:** 2026-05-31  
**Status:** Canonical implementation roadmap  
**Authority:** FEDERATION_TEST_SUITE_SPEC.md, FEDERATION_CONFORMANCE_MODEL.md, FEDERATION_RUNNER_DESIGN.md

---

## Principle

**Implement by conformance order, not by module order.**

Every implementation step must unlock a specific conformance test. Nothing is built without a test to unlock. The first milestone is not "federation is implemented" — it is "FED-CERT-001 PASS".

---

## Phase 1 — Test Dependency Analysis

### FED-CERT-001 Exact Requirements

**Test:** `GET /.well-known/banza/certificate.json` — HTTP 200, valid JSON, Content-Type: application/json, schema valid against `operator-certificate.json`.

| Requirement | Source | Status |
|---|---|---|
| `operator-certificate.json` JSON Schema | `contracts/federation/` | **MISSING** |
| Runner: HTTP GET client | `tools/banza-conformance/run.py` | exists (extend) |
| Runner: schema validator | runner extension | **MISSING** |
| Runner: `--federation` flag | runner extension | **MISSING** |
| Runner: test root keypair generation | runner extension | **MISSING** |
| Runner: certificate issuance (CERT-A-VALID) | runner extension | **MISSING** |
| Runner: Operator A setup (deliver cert) | runner extension | **MISSING** |
| Operator A: `/.well-known/banza/certificate.json` endpoint | operator | **MISSING** |
| Operator A: conformance setup endpoint | operator | **MISSING** |

**FED-CERT-001 is a structure test only.** The runner validates schema. No signature verification is required for FED-CERT-001. However, the runner must issue CERT-A-VALID and configure it on Operator A before any test runs, because that is what the operator will serve.

### Full FED-CERT Suite Dependency Classification

| Test | Type | Runner-Only? | Requires Operator Trust Engine? |
|---|---|---|---|
| FED-CERT-001 | Endpoint presence + schema | Yes | No |
| FED-CERT-002 | ed25519 signature verify | Yes | No |
| FED-CERT-003 | Expiry check | Yes | No |
| FED-CERT-004 | operator_id regex | Yes | No |
| FED-CERT-005 | public_key format | Yes | No |
| FED-CERT-006 | issuer string equality | Yes | No |
| FED-CERT-007 | Lifetime ≤ 90 days | Yes | No |
| FED-CERT-008 | Operator A rejects expired cert | **No** | **Yes (Step 2.4)** |
| FED-CERT-009 | Operator A rejects BRL-revoked cert | **No** | **Yes (Step 2.6)** |
| FED-CERT-010 | Operator A rejects cert/manifest mismatch | **No** | **Yes (Step 2.9)** |
| FED-CERT-011 | Operator A fetches unknown key | **No** | **Yes (key rotation)** |

**FED-CERT-001 through FED-CERT-007** pass purely on runner-side logic. These seven tests verify structural and cryptographic properties that the runner checks itself.

**FED-CERT-008 through FED-CERT-011** test Operator A's trust enforcement behavior. These require Operator A to have a working trust engine.

---

## Phase 2 — Minimum Implementation Surface

### For FED-CERT-001 PASS Only

The smallest possible executable slice:

| Artifact | Location | What It Does |
|---|---|---|
| `operator-certificate.json` | `contracts/federation/` | JSON Schema for schema validation |
| Runner `--federation` flag | `tools/banza-conformance/run.py` | Activates federation test mode |
| Runner: keypair generator | `tools/banza-conformance/trust_root.py` | Generates test BANZA root ed25519 keypair |
| Runner: certificate issuer | `tools/banza-conformance/trust_root.py` | Issues CERT-A-VALID signed by test root |
| Runner: setup delivery | `tools/banza-conformance/run_fed.py` | Delivers test cert + private key to Operator A |
| Runner: FED-CERT-001 test | `tools/banza-conformance/run_fed.py` | GET + status + Content-Type + schema validation |
| Runner: evidence collector | `tools/banza-conformance/run_fed.py` | Records HTTP response + validation result |
| Operator A: cert endpoint | operator repo | Serves the configured test certificate |
| Operator A: setup endpoint | operator repo | Receives test cert from runner |

**Total new files in this repo: 3** (1 schema, 1 trust root, 1 fed runner)  
**Total modified files: 1** (`run.py`)

### For Full FED-CERT Suite PASS (001–011)

Additional requirements beyond 001–007:

| Addition | What It Enables |
|---|---|
| Simulated Operator B (runner-embedded HTTP server) | FED-CERT-008, -009, -010, -011 |
| Sim Op B failure injection API | FED-CERT-008 (expired cert), -009 (BRL hit) |
| Runner test BRL server | FED-CERT-009 (BRL endpoint) |
| Operator A: trust engine (9-step protocol) | FED-CERT-008, -009, -010, -011 |
| Operator A: BRL fetcher + staleness guard | FED-CERT-009 |

### Classification of All Components

| Component | REQUIRED for Slice 0 | REQUIRED for FED-CERT | REQUIRED for L3 PASS | DEFER |
|---|---|---|---|---|
| `operator-certificate.json` schema | ✓ | ✓ | ✓ | — |
| `federation-manifest.json` schema | — | — | ✓ | until FED-DISC |
| `federation-routing.json` schema | — | — | ✓ | until FED-ROUTE |
| `federation-obligation.json` schema | — | — | ✓ | until FED-OBL |
| `federation-event.json` schema | — | — | ✓ | until FED-EVT |
| `banza-revocation-list.json` schema | — | — | ✓ | until FED-TRUST |
| Runner: test trust root | ✓ | ✓ | ✓ | — |
| Runner: Simulated Operator B | — | ✓ (008–011) | ✓ | after 001–007 |
| Runner: BRL server | — | ✓ (009) | ✓ | after 007 |
| Runner: FED-CERT suite | ✓ | ✓ | ✓ | — |
| Runner: FED-DISC suite | — | — | ✓ | after FED-CERT |
| Runner: FED-TRUST suite | — | — | ✓ | after FED-DISC |
| Runner: FED-ROUTE suite | — | — | ✓ | after FED-TRUST |
| Runner: FED-EXEC suite | — | — | ✓ | after FED-ROUTE |
| Runner: FED-OBL suite | — | — | ✓ | after FED-EXEC |
| Runner: FED-EVT suite | — | — | conditional | after FED-OBL |
| Runner: FED-SETTLE suite | — | — | conditional | after FED-OBL |
| Runner: FED-FAIL suite | — | — | partial required | after FED-OBL |
| Runner: evidence packager | — | — | ✓ | after all suites |
| Operator A: cert endpoint | ✓ | ✓ | ✓ | — |
| Operator A: extended manifest | — | — | ✓ | after FED-CERT |
| Operator A: trust engine (9-step) | — | ✓ (008–011) | ✓ | after cert endpoint |
| Operator A: BRL fetcher | — | ✓ (009) | ✓ | after trust engine |
| Operator A: routing endpoint | — | — | ✓ | after FED-TRUST |
| Operator A: obligation engine | — | — | ✓ | after routing |
| Operator A: event emission | — | — | conditional | after obligation |
| Operator A: conformance setup endpoint | ✓ | ✓ | ✓ | — |
| Routing (settlement, networking) | — | — | — | **defer entirely** |

---

## Phase 3 — FED-CERT Implementation Graph

```
FED-CERT-001 (schema present, endpoint alive)
    │
    ├── operator-certificate.json schema
    ├── runner: keypair gen + cert issuance
    ├── runner: --federation + setup delivery
    ├── runner: GET + 200 + Content-Type + schema validation
    └── Operator A: cert endpoint

FED-CERT-002 (signature verifies)
    │
    └── runner: ed25519 verify (cryptography library)

FED-CERT-003 (not expired)
    │
    └── runner: timestamp comparison

FED-CERT-004 (operator_id regex)
    │
    └── runner: regex `^[a-z0-9][a-z0-9\-]{2,62}[a-z0-9]$`

FED-CERT-005 (public_key format)
    │
    └── runner: regex + base64url decode + length check

FED-CERT-006 (issuer == "BANZA")
    │
    └── runner: string equality

FED-CERT-007 (lifetime ≤ 90 days)
    │
    └── runner: (expires_at - issued_at) ≤ 7,776,000 seconds

FED-CERT-008 (Operator A rejects expired cert)
    │
    ├── runner: Simulated Operator B HTTP server
    ├── runner: CERT-EXPIRED fixture generation
    ├── runner: Sim Op B cert swap API
    └── Operator A: trust engine (Step 2.4: expiry check)

FED-CERT-009 (Operator A rejects BRL-revoked cert)
    │
    ├── runner: BRL server (embedded HTTP)
    ├── runner: BRL-CONTAINS-OP-B fixture
    └── Operator A: trust engine (Step 2.6: BRL check)

FED-CERT-010 (cert/manifest operator_id mismatch)
    │
    ├── runner: CERT-MISMATCHED-OPERATOR-ID fixture
    └── Operator A: trust engine (Step 2.9: operator_id binding)

FED-CERT-011 (unknown issuer_key_id triggers key fetch)
    │
    ├── runner: BANZA-KEY-MANIFEST server
    ├── runner: CERT-UNKNOWN-ISSUER-KEY-ID fixture
    └── Operator A: key registry + key rotation fetch
```

**Certification gate:** Any FAIL in FED-CERT = certification denied (blocking suite).

```
FED-CERT PASS
    ↓
FED-DISC PASS (manifest fields + endpoint reachability)
    ↓
FED-TRUST PASS (9-step trust protocol — all 9 steps, BRL, negative tests)
    ↓
FED-ROUTE PASS (routing wire protocol, idempotency, rejections)
    ↓
FED-EXEC PASS (simultaneous credit, debit+obligation atomicity)
    ↓
FED-OBL PASS (obligation lifecycle, signatures, uniqueness)
    ↓
[FED-EVT, FED-SETTLE, FED-FAIL-001/004/005] — conditional/mandatory recovery
    ↓
L3 CERTIFICATION GRANTED
```

---

## Phase 4 — Federation Slice 0 (First Executable Slice)

### Slice 0 Definition

**Includes:**
- Test BANZA root: keypair generation + certificate issuance
- Operator A certificate configuration: setup delivery
- Certificate endpoint: `GET /.well-known/banza/certificate.json`
- Schema validation: `operator-certificate.json`
- FED-CERT-001 through FED-CERT-007 test execution
- Evidence capture: raw HTTP response + validation results

**Explicitly excludes:**
- Simulated Operator B
- BRL server
- Routing logic
- Obligations
- Settlement
- Events
- Reconciliation
- Any two-operator test (FED-CERT-008 through FED-CERT-011 are deferred to Slice 1)

### Slice 0 Produces

```
FED-CERT-001 PASS — certificate endpoint present
FED-CERT-002 PASS — signature verifies against test root
FED-CERT-003 PASS — not expired
FED-CERT-004 PASS — operator_id format correct
FED-CERT-005 PASS — public_key format correct
FED-CERT-006 PASS — issuer == "BANZA"
FED-CERT-007 PASS — lifetime ≤ 90 days
```

These are 7 PASS results. Certification is not yet granted (FED-CERT-008 through -011 remain, plus all downstream suites), but the first real conformance evidence exists.

### Slice 0 Does Not Produce L3 Certification

Slice 0 is intentionally incomplete. It proves the infrastructure works end-to-end — the runner can issue a certificate, deliver it to an operator, and verify it. Every subsequent slice builds on this foundation.

---

## Phase 5 — Runner Integration

### Changes Required in `tools/banza-conformance/`

#### New file: `tools/banza-conformance/trust_root.py`

```python
# Responsibilities:
# - generate_test_root_keypair() → (private_key, public_key, key_id)
# - issue_certificate(operator_id, operator_public_key, ...) → cert_dict
# - sign_json(private_key, dict_without_signature) → base64url_signature
# - canonical_json(dict) → bytes (sorted keys, no whitespace, no signature field)
# - generate_brl(revoked_ids=[]) → brl_dict (signed)
# - verify_certificate(cert_dict, public_key) → bool
```

The `cryptography` library (PyPI) must be added as a dependency. It provides:
- `Ed25519PrivateKey.generate()`
- `Ed25519PrivateKey.sign(data)`
- `Ed25519PublicKey.verify(signature, data)`

This is the only external dependency required. Everything else uses the Python stdlib.

#### New file: `tools/banza-conformance/run_fed.py`

```python
# Responsibilities:
# - setup_operator_a(base_url, cert, private_key, brl_url, key_manifest_url)
#   POST /conformance/setup → delivers test configuration to Operator A
# - run_fed_cert(base_url, trust_root) → list[TestResult]
#   Implements FED-CERT-001 through FED-CERT-007 (Slice 0)
#   Defers FED-CERT-008 through -011 until Slice 1
# - run_fed_disc(base_url, schemas) → list[TestResult]  (Slice 1)
# - Evidence capture per test
```

#### Modified: `tools/banza-conformance/run.py`

```diff
+ parser.add_argument("--federation", action="store_true",
+     help="Run L3 Federation certification tests")
+ parser.add_argument("--sim-b-port", type=int, default=9090)

+ if args.federation:
+     from run_fed import run_federation_mode
+     sys.exit(run_federation_mode(base_url, args))
```

Existing L0-L2 suites are completely unchanged.

#### New file: `tools/banza-conformance/requirements.txt`

```
cryptography>=42.0.0
```

### What `reference/` Needs

No changes to `reference/`. The reference documentation is already complete via the federation docs in `docs/federation/`.

### What `core/` Needs

No changes to the Rust core for runner operation. The core implements the operator's ledger engine. For Slice 0, only the certificate endpoint is needed — no ledger operations.

For full L3 certification, the operator (which uses the core) must implement:
- Routing request handling (uses ledger for atomic debit)
- Obligation creation (uses ledger for double-entry)
- Trust engine (no ledger dependency — pure cryptography)

---

## Phase 6 — Implementation Work Packages

### WP-001 — Certificate Schema

**Purpose:** Define the operator certificate contract. Without this schema, no certificate validation is possible.

| Field | Value |
|---|---|
| Files | `contracts/federation/operator-certificate.json` |
| Effort | 30 minutes |
| Tests unlocked | FED-CERT-001 (schema validation), FED-CERT-002 through -007 (all reference this schema) |
| Certification impact | Prerequisite for entire FED-CERT suite |
| Blocking | Yes — no federation runner can start without this |

**Schema fields to define:**
- `schema_version` (string, required)
- `operator_id` (string, pattern: `^[a-z0-9][a-z0-9\-]{2,62}[a-z0-9]$`)
- `certification_level` (integer, enum: [1,2,3,4])
- `protocol_version` (string)
- `capabilities` (array of strings)
- `public_key` (string, pattern: `^ed25519:[A-Za-z0-9_-]{43}$`)
- `issued_at` (string, ISO 8601 UTC)
- `expires_at` (string, ISO 8601 UTC)
- `issuer` (string, const: "BANZA")
- `issuer_key_id` (string)
- `signature` (string)

---

### WP-002 — Test Trust Root + Certificate Issuance

**Purpose:** The runner must be able to generate an ephemeral test BANZA keypair and issue valid certificates. Without this, Operator A has nothing to serve.

| Field | Value |
|---|---|
| Files | `tools/banza-conformance/trust_root.py`, `tools/banza-conformance/requirements.txt` |
| Effort | 2 hours |
| Tests unlocked | FED-CERT-002 (signature verification), all FED-TRUST tests, FED-CERT-008/009 |
| Certification impact | Foundational — every federation test depends on this |
| Blocking | Yes — no signed certificates without this |

**Key implementation points:**
- Ephemeral keypair: new keypair per runner invocation
- Canonical JSON: sort keys lexicographically, no whitespace, exclude `signature` field when signing
- Certificate lifetime: exactly 89 days for CERT-A-VALID (satisfies FED-CERT-007: ≤ 90 days)
- Both Operator A keypair (for routing signatures) and Operator B keypair (for Sim Op B) issued from the same test root

---

### WP-003 — Federation Runner Entry Point + FED-CERT-001 to FED-CERT-007

**Purpose:** The minimal runner capable of executing Slice 0.

| Field | Value |
|---|---|
| Files | `tools/banza-conformance/run_fed.py` (new), `tools/banza-conformance/run.py` (modified) |
| Effort | 2 hours |
| Tests unlocked | FED-CERT-001 through FED-CERT-007 |
| Certification impact | First 7 passing tests |
| Blocking | No cert tests pass without this |

**Implementation sequence within WP-003:**
1. `setup_operator_a()` — POST /conformance/setup to deliver test cert + key + BRL URL
2. `run_fed_cert_001()` — GET cert endpoint, check 200 + schema + Content-Type
3. `run_fed_cert_002()` — verify ed25519 signature using trust_root.verify_certificate()
4. `run_fed_cert_003()` — compare expires_at to runner clock
5. `run_fed_cert_004()` — regex match on operator_id
6. `run_fed_cert_005()` — regex + base64url decode on public_key
7. `run_fed_cert_006()` — strict string equality: issuer == "BANZA"
8. `run_fed_cert_007()` — (expires_at - issued_at) ≤ 7,776,000 seconds

---

### WP-004 — Federation Manifest Schema + FED-DISC Suite

**Purpose:** Define the manifest extension contract and implement discovery tests.

| Field | Value |
|---|---|
| Files | `contracts/federation/federation-manifest.json`, `run_fed.py` extension |
| Effort | 2 hours |
| Tests unlocked | FED-DISC-001 through FED-DISC-008 |
| Certification impact | Blocking suite — any DISC FAIL = denied |
| Prerequisite | WP-001, WP-002, WP-003 (FED-CERT must pass first) |

---

### WP-005 — Simulated Operator B + BRL Server

**Purpose:** Two-operator tests require a fully controlled BANZA-compliant stub. This unlocks FED-CERT-008 through -011 and all of FED-TRUST.

| Field | Value |
|---|---|
| Files | `tools/banza-conformance/sim_b/server.py`, `sim_b/wallets.py`, `sim_b/routing.py`, `sim_b/obligations.py`, `sim_b/events.py`, `trust_root.py` BRL extension |
| Effort | 5 hours |
| Tests unlocked | FED-CERT-008, FED-CERT-009, FED-CERT-010, FED-CERT-011, all FED-TRUST |
| Certification impact | Blocking — trust tests cannot run without Sim Op B |
| Prerequisite | WP-002, WP-003 |

**Sim Op B minimum endpoints for FED-TRUST:**
- `GET /.well-known/banza/certificate.json` (configurable: valid, expired, invalid-sig, L2, mismatched)
- `GET /.well-known/banza/operator.json` (configurable: with/without federation fields)
- Failure injection control API (local port, not exposed to Operator A)
- `GET /federation/revocation-list.json` served by trust root BRL server (runner-side)

---

### WP-006 — FED-TRUST Suite

**Purpose:** Implement all 9 trust protocol step tests.

| Field | Value |
|---|---|
| Files | `run_fed.py` extension (FED-TRUST section) |
| Effort | 2 hours |
| Tests unlocked | FED-TRUST-001 through FED-TRUST-009 |
| Certification impact | Blocking — any trust FAIL = denied |
| Prerequisite | WP-005 (Sim Op B), Operator A trust engine |

---

### WP-007 — Routing Schema + FED-ROUTE + FED-EXEC + FED-OBL Suites

**Purpose:** Wire protocol tests for routing, execution, and obligation lifecycle.

| Field | Value |
|---|---|
| Files | `contracts/federation/federation-routing.json`, `contracts/federation/federation-obligation.json`, `run_fed.py` extensions |
| Effort | 5 hours |
| Tests unlocked | FED-ROUTE-001 through -012, FED-EXEC-001 through -008, FED-OBL-001 through -007 |
| Certification impact | All three are blocking suites |
| Prerequisite | WP-005, WP-006, Operator A routing + obligation implementation |

---

### WP-008 — Event + Settlement + Failure Suites + Evidence Packager

**Purpose:** Non-blocking (conditional) suites plus mandatory recovery tests.

| Field | Value |
|---|---|
| Files | `contracts/federation/federation-event.json`, `run_fed.py` extensions, `tools/banza-conformance/evidence/packager.py` |
| Effort | 4 hours |
| Tests unlocked | FED-EVT, FED-SETTLE, FED-FAIL |
| Certification impact | FED-FAIL-001, -004, -005 are mandatory (denial if failed) |
| Prerequisite | WP-007 |

---

## Phase 7 — Success Definition

### FED-CERT-001 PASS Evidence

The runner captures and records the following to declare FED-CERT-001 PASS:

```
✓ HTTP status == 200
✓ Content-Type contains "application/json"
✓ Response body is valid JSON
✓ JSON validates against operator-certificate.json schema
  (all required fields present, correct types, no extra required fields missing)

Evidence captured:
  cert.http_status = 200
  cert.http_headers = { "Content-Type": "application/json", ... }
  cert.raw_json = { ... full certificate ... }
  cert.schema_validation_result = { "valid": true, "errors": [] }
```

### Full L3 Certification PASS Evidence

All of the following must be simultaneously true in the evidence package:

```
BLOCKING SUITES (all must PASS):
✓ FED-CERT:  11/11 tests PASS
✓ FED-DISC:   8/8  tests PASS
✓ FED-TRUST:  9/9  tests PASS
✓ FED-ROUTE: 12/12 tests PASS
✓ FED-EXEC:   8/8  tests PASS
✓ FED-OBL:    7/7  tests PASS

MANDATORY RECOVERY (all three must PASS):
✓ FED-FAIL-001 — idempotent retry succeeds, no double payment
✓ FED-FAIL-004 — Operator A certificate rejected by Operator B
✓ FED-FAIL-005 — crash recovery recreates missing obligation

CONDITIONAL (must PASS for full, or CONDITIONAL certification):
✓ FED-EVT:     6/6  tests PASS (or conditional: 30-day remediation)
✓ FED-SETTLE:  8/10 tests PASS minimum
✓ FED-FAIL:    5/8  tests PASS minimum

CRYPTOGRAPHIC PROOFS:
✓ CERT-A-VALID: ed25519 signature verifies against test BANZA root
✓ OBLIGATION-PENDING: obligor_signature verifies against Operator A public key
✓ All routing requests: Banza-Federation-Signature verifies on Operator B

FINANCIAL INVARIANTS ENFORCED:
✓ INV-TRUST-001: certificate signature chain from BANZA root
✓ INV-TRUST-002: no expired certificate accepted
✓ INV-TRUST-003: no BRL-revoked operator routed to
✓ INV-FED-001: trace_id invariant across all artifacts
✓ INV-FED-002: exactly one obligation per routing_request_id
✓ INV-FED-004: routing idempotency enforced
✓ INV-FED-005: obligation amount == routing amount (exact integer equality)
✓ INV-FED-LEDGER-001: cross-operator double-entry verified

EVIDENCE PACKAGE:
✓ run-id.txt present
✓ report.json valid
✓ All per-suite result files present
✓ All per-test HTTP logs present
✓ package-signature.json valid (signed by test root)
```

---

## Phase 8 — Roadmap to First L3 PASS

### Step 1: Contract — `operator-certificate.json`

**File:** `contracts/federation/operator-certificate.json`  
**What:** JSON Schema for the operator certificate.  
**Unlocks:** Schema validation in FED-CERT-001.  
**Effort:** 30 min

---

### Step 2: Runner — Test Trust Root

**File:** `tools/banza-conformance/trust_root.py`  
**What:** ed25519 keypair generation, canonical JSON, certificate signing and verification, BRL generation.  
**Unlocks:** Certificate issuance (CERT-A-VALID), FED-CERT-002 signature verification.  
**Effort:** 2 hours

---

### Step 3: Runner — Federation Entry Point + FED-CERT-001 Test

**Files:** `tools/banza-conformance/run_fed.py`, `tools/banza-conformance/run.py`  
**What:** `--federation` flag, operator setup delivery, FED-CERT-001 test execution and evidence capture.  
**Unlocks:** **FED-CERT-001 PASS** — the first executable federation conformance result.  
**Effort:** 1.5 hours

> **This is the first PASS milestone.** After Step 3, the command:
> ```bash
> python3 run.py --federation --operator-a http://localhost:3000 --suite FED-CERT-001
> ```
> produces a real PASS result with captured evidence.

---

### Step 4: Runner — FED-CERT-002 through FED-CERT-007

**File:** `tools/banza-conformance/run_fed.py` (extend)  
**What:** Signature verification, expiry check, format validations, lifetime check.  
**Unlocks:** FED-CERT-002 through FED-CERT-007 — 7 total PASSes.  
**Effort:** 1.5 hours

---

### Step 5: Operator A — Certificate Endpoint + Conformance Setup

**Repo:** operator (reference implementation)  
**What:**
- `GET /.well-known/banza/certificate.json` returning the configured test certificate
- `POST /conformance/setup` accepting `{certificate, private_key, brl_url, key_manifest_url}`
**Unlocks:** Runner can configure and test Operator A.  
**Effort:** 1–2 hours

> Steps 1–5 together produce **FED-CERT-001 through FED-CERT-007 PASS**. This is Federation Slice 0.

---

### Step 6: Contract — `federation-manifest.json`

**File:** `contracts/federation/federation-manifest.json`  
**What:** JSON Schema extending the operator manifest for federation fields.  
**Unlocks:** FED-DISC schema validation.  
**Effort:** 30 min

---

### Step 7: Operator A — Extended Manifest Endpoint

**What:** Add federation fields to `/.well-known/banza/operator.json`:
```json
{
  "supports_federation": true,
  "cross_operator_routing": true,
  "cross_operator_settlement": true,
  "certificate_url": "...",
  "interop_endpoint": "...",
  "federation_version": "1",
  "federation_capabilities": {
    "routing_version": "1",
    "settlement_version": "1",
    "supported_currencies": ["AOA"],
    "netting_interval_hours": 24
  }
}
```
**Unlocks:** FED-DISC-001 through FED-DISC-006, FED-DISC-008.  
**Effort:** 1 hour

---

### Step 8: Runner — FED-DISC Suite

**File:** `tools/banza-conformance/run_fed.py` (extend)  
**What:** All 8 FED-DISC tests, dual schema validation, endpoint reachability checks.  
**Unlocks:** FED-DISC PASS (blocking suite cleared).  
**Effort:** 1.5 hours

---

### Step 9: Runner — Simulated Operator B + BRL Server

**Files:** `tools/banza-conformance/sim_b/server.py`, `sim_b/wallets.py`, `sim_b/routing.py`, `sim_b/obligations.py`, `sim_b/events.py`  
**What:** Embedded HTTP server implementing Sim Op B, configurable per-test fixture, failure injection.  
**Unlocks:** All two-operator tests: FED-CERT-008 through -011, all of FED-TRUST.  
**Effort:** 5 hours

---

### Step 10: Operator A — Trust Engine (9-Step Protocol)

**What:** The complete trust verification implementation in Operator A:

| Step | Verification |
|---|---|
| Step 2.1 | Fetch remote certificate from certificate_url |
| Step 2.2 | Validate schema |
| Step 2.3 | Verify ed25519 signature against BANZA root public key |
| Step 2.4 | Check expires_at > now() AND issued_at ≤ now() |
| Step 2.5 | Check certification_level ≥ 3 |
| Step 2.6 | Fetch BRL; check operator_id not in revoked list |
| Step 2.7 | Fetch manifest; check supports_federation == true |
| Step 2.8 | Check capabilities includes "cross_operator_routing" |
| Step 2.9 | Check cert.operator_id == manifest.operator_id |

**Also includes:** BRL cache (max 6 hours), BRL signature verification, key rotation (unknown issuer_key_id → fetch BANZA key manifest).  
**Unlocks:** FED-CERT-008, -009, -010, -011, FED-TRUST-001 through -009, FED-DISC-007.  
**Effort:** 6–8 hours (this is the hardest component)

---

### Step 11: Runner — FED-TRUST Suite

**File:** `tools/banza-conformance/run_fed.py` (extend)  
**What:** All 9 FED-TRUST tests using Sim Op B fixture injection.  
**Unlocks:** FED-TRUST PASS (blocking suite cleared).  
**Effort:** 2 hours

---

### Step 12: Contracts — `federation-routing.json`, `federation-obligation.json`

**Files:** `contracts/federation/federation-routing.json`, `contracts/federation/federation-obligation.json`  
**Effort:** 1 hour total

---

### Step 13: Operator A — Routing Endpoint

**What:**
- `POST /federation/route` implementing the Routing Request handler
- Signature verification (Banza-Federation-Signature header)
- Idempotency (routing_request_id cache)
- Wallet lookup + currency check + amount validation
- Simultaneous payee credit on acceptance (atomic)
- Return ROUTING-RESPONSE-ACCEPTED or structured rejection

**Unlocks:** FED-ROUTE-001 through -012.  
**Effort:** 6 hours

---

### Step 14: Runner — FED-ROUTE Suite

**File:** `tools/banza-conformance/run_fed.py` (extend)  
**What:** All 12 FED-ROUTE tests.  
**Unlocks:** FED-ROUTE PASS (blocking suite cleared).  
**Effort:** 2.5 hours

---

### Step 15: Operator A — Obligation Engine

**What:**
- Atomic debit + obligation creation (single database transaction)
- `GET /federation/obligations` endpoint
- obligor_signature (sign canonical obligation with Operator A private key)
- Obligation uniqueness (UNIQUE constraint on routing_request_id)
- `GET /federation/events` endpoint (basic event emission)

**Unlocks:** FED-EXEC-001 through -008, FED-OBL-001 through -007.  
**Effort:** 4–5 hours

---

### Step 16: Runner — FED-EXEC + FED-OBL Suites

**File:** `tools/banza-conformance/run_fed.py` (extend)  
**What:** All 8 FED-EXEC and 7 FED-OBL tests.  
**Unlocks:** FED-EXEC PASS + FED-OBL PASS (both blocking suites cleared).  
**Effort:** 3 hours

> **At this point, all 6 blocking suites PASS.** This is the first state where L3 certification is achievable (pending FED-FAIL-001/004/005 and conditional suites).

---

### Step 17: Contract + Runner — `federation-event.json` + FED-EVT Suite

**Effort:** 2 hours  
**Unlocks:** FED-EVT-001 through -006 (conditional — 30-day remediation if partial)

---

### Step 18: Runner — FED-FAIL-001, FED-FAIL-004, FED-FAIL-005

**What:** Mandatory recovery tests: timeout retry, trust rejection, crash recovery.  
**Note:** FED-FAIL-005 requires Operator A to expose `POST /conformance/inject-state` or it is SKIPPED (noted in evidence).  
**Effort:** 2 hours

---

### Step 19: Evidence Packager + Report Signing

**File:** `tools/banza-conformance/evidence/packager.py`  
**What:** Assemble all evidence items, generate report.json, sign the package with the test root keypair.  
**Unlocks:** Complete evidence package accepted by BANZA for certification review.  
**Effort:** 1.5 hours

---

### Step 20: Submit Evidence Package

```bash
python3 run.py --federation \
  --operator-a https://api.your-operator.example \
  --level 3 \
  --output ./evidence-2026-06-XX/
```

Submit `./evidence-2026-06-XX/` to BANZA for L3 certification review.

---

## Phase 9 — Final Verdict

### 1. Minimum implementation for the first Federation PASS

**For FED-CERT-001 PASS:**

In this repository:
- 1 new file: `contracts/federation/operator-certificate.json`
- 1 new file: `tools/banza-conformance/trust_root.py`
- 1 new file: `tools/banza-conformance/run_fed.py`
- 1 modified file: `tools/banza-conformance/run.py`

In the operator repository:
- 1 new endpoint: `GET /.well-known/banza/certificate.json`
- 1 new endpoint: `POST /conformance/setup`

**Total: 3 new files + 1 modification + 2 operator endpoints.**

### 2. Files actually modified for L3 PASS

| Repository | New Files | Modified Files |
|---|---|---|
| `~/banza` (this repo) | 16 | 1 |
| Operator repo | ~8 | ~3 |

Files in this repo:
1. `contracts/federation/operator-certificate.json`
2. `contracts/federation/federation-manifest.json`
3. `contracts/federation/federation-routing.json`
4. `contracts/federation/federation-obligation.json`
5. `contracts/federation/federation-event.json`
6. `contracts/federation/banza-revocation-list.json`
7. `tools/banza-conformance/trust_root.py`
8. `tools/banza-conformance/run_fed.py`
9. `tools/banza-conformance/requirements.txt`
10. `tools/banza-conformance/sim_b/server.py`
11. `tools/banza-conformance/sim_b/wallets.py`
12. `tools/banza-conformance/sim_b/routing.py`
13. `tools/banza-conformance/sim_b/obligations.py`
14. `tools/banza-conformance/sim_b/events.py`
15. `tools/banza-conformance/evidence/packager.py`
16. `tools/banza-conformance/evidence/collector.py`
+ modify: `tools/banza-conformance/run.py`

### 3. Contracts that become executable

| Contract | Becomes Executable At |
|---|---|
| `operator-certificate.json` | Step 3 (FED-CERT-001) |
| `federation-manifest.json` | Step 8 (FED-DISC) |
| `federation-routing.json` | Step 14 (FED-ROUTE) |
| `federation-obligation.json` | Step 16 (FED-OBL) |
| `federation-event.json` | Step 17 (FED-EVT) |

### 4. Invariants that become enforceable

| Invariant | Enforced At |
|---|---|
| INV-TRUST-001 (signature chain) | Step 4 — FED-CERT-002 |
| INV-TRUST-002 (expiry) | Step 4 — FED-CERT-003; Step 11 — FED-TRUST-003 |
| INV-TRUST-003 (BRL rejection) | Step 11 — FED-TRUST-005 |
| INV-TRUST-004 (federation flag needs cert) | Step 11 — FED-TRUST-006 |
| INV-TRUST-006 (BRL max 6h) | Step 11 — FED-TRUST-009 |
| INV-FED-001 (trace_id propagation) | Step 14 — FED-ROUTE-003 |
| INV-FED-002 (one obligation per routing) | Step 16 — FED-OBL-001 |
| INV-FED-003 (federation flag → endpoint) | Step 8 — FED-DISC-005 |
| INV-FED-004 (routing idempotency) | Step 14 — FED-ROUTE-004 |
| INV-FED-005 (value conservation) | Step 16 — FED-OBL-002 |
| INV-FED-006 (cert must expire ≤ 90d) | Step 4 — FED-CERT-007 |
| INV-FED-007 (revoked = rejected) | Step 11 — FED-TRUST-005 |
| INV-FED-LEDGER-001 (cross-op double-entry) | Step 16 — FED-EXEC-002 |
| INV-FED-LEDGER-002 (integer arithmetic) | Step 14 — FED-ROUTE-010 |
| INV-FED-IDEM-001 (global unique IDs) | Step 14 — FED-ROUTE-004 |
| INV-FED-RECON-001 (cross-op reconcilability) | Step 17 — FED-SETTLE-006 |

### 5. Estimated effort to first real L3 conformance PASS

| Phase | Steps | Effort |
|---|---|---|
| Slice 0 — FED-CERT-001 PASS | Steps 1–3 | 4 hours |
| FED-CERT-001 through -007 PASS | Steps 1–5 | 7 hours |
| FED-CERT + FED-DISC PASS | Steps 6–8 | 10 hours |
| + Sim Op B + FED-TRUST PASS | Steps 9–11 | 23 hours |
| + FED-ROUTE PASS | Steps 12–14 | 31 hours |
| + FED-EXEC + FED-OBL PASS | Steps 15–16 | 40 hours |
| **L3 Blocking Suites All PASS** | Steps 1–16 | **~40 hours** |
| Full L3 + evidence package | Steps 17–20 | **~47 hours** |

**Estimate assumes:** operator team with knowledge of the protocol, working in Go or TypeScript for Operator A, with the runner implemented in Python. The trust engine (Step 10) is the single most complex component at ~8 hours.

**The critical bottleneck is not the runner — it is Operator A's trust engine.** Steps 1–9 (runner infrastructure) can be completed in ~20 hours. Operator A (Steps 5, 7, 10, 13, 15) accounts for the remaining ~27 hours, with the trust engine alone at roughly one-third of total effort.

---

## Summary

| Question | Answer |
|---|---|
| First PASS milestone | FED-CERT-001 — certificate endpoint alive + schema valid |
| Files in this repo for first PASS | 3 new + 1 modified |
| Files in this repo for L3 PASS | 16 new + 1 modified |
| Critical operator component | Trust engine (9-step protocol, ~8 hours) |
| Blocking suites for L3 | FED-CERT + FED-DISC + FED-TRUST + FED-ROUTE + FED-EXEC + FED-OBL |
| First executable milestone time | ~4 hours (Steps 1–3) |
| Total to L3 PASS | ~47 hours |
| What to build first | `contracts/federation/operator-certificate.json` |

---

*Implementation begins with proof, not with scope. The first commit is a schema file and a 60-line test. Everything after that builds on a passing baseline.*
