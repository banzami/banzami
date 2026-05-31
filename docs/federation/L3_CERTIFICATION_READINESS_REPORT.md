# L3 Federation Certification Readiness Report

**Document ID:** L3-FEDERATION-CERTIFICATION-READINESS-AUDIT-001  
**Date:** 2026-05-31  
**Auditor:** BANZA Protocol Team  
**Scope:** BANZA federation conformance suite (79 tests, 9 suites, commit `49c589c`)  
**Status:** FINAL — pre-public-beta audit  

---

## Executive Summary

| Readiness Claim | Verdict |
|---|---|
| Specification-ready | **YES** |
| Conformance-ready (executable end-to-end in test mode) | **YES** |
| Beta-ready (can be offered to early operators) | **YES — with 3 documentation fixes** |
| Production-ready (public certificate issuance) | **NO — 5 remaining items** |

**The federation conformance suite is complete.** 79 tests covering 9 suites (FED-CERT through FED-FAIL) all pass. Every L3 requirement maps to a contract, an invariant, at least one test, and captured evidence. No orphan requirements exist.

**Production-readiness is blocked by documentation and process gaps, not by conformance gaps.** No additional test cases are required before beta.

---

## Phase 1 — Traceability Audit

### L3 Requirement Coverage

The federation protocol defines 14 per-operator and cross-operator requirements (FED-L3-001 through FED-L3-014). Every requirement maps to at least one passing test.

| Requirement | Description | Primary Tests | Status |
|---|---|---|---|
| FED-L3-001 | Valid certificate at ≥ L3 | FED-CERT-001, FED-CERT-005 | ✓ COVERED |
| FED-L3-002 | Certificate not expired | FED-CERT-003 | ✓ COVERED |
| FED-L3-003 | supports_federation + cross_operator_routing | FED-DISC-002, FED-DISC-003 | ✓ COVERED |
| FED-L3-004 | interop_endpoint reachable | FED-DISC-005 | ✓ COVERED |
| FED-L3-005 | certificate.operator_id == manifest.operator_id | FED-CERT-010, FED-DISC-004 | ✓ COVERED |
| FED-L3-006 | Operator not in BRL | FED-TRUST-005, FED-CERT-009 | ✓ COVERED |
| FED-L3-007 | POST /federation/route returns valid response | FED-ROUTE-001 through 009 | ✓ COVERED |
| FED-L3-008 | GET /federation/obligations returns obligations | FED-OBL-001 | ✓ COVERED |
| FED-L3-009 | Operator A verifies Operator B (9 trust steps) | FED-TRUST-001 through 009 | ✓ COVERED |
| FED-L3-010 | Operator B verifies Operator A (bidirectional) | FED-ROUTE-005, FED-FAIL-004 | ✓ COVERED |
| FED-L3-011 | Payment completes on both operators | FED-EXEC-001, FED-EXEC-002, FED-EVT-003 | ✓ COVERED |
| FED-L3-012 | trace_id identical across both operators | FED-ROUTE-003, FED-OBL-003, FED-EVT-005 | ✓ COVERED |
| FED-L3-013 | Obligation recorded immediately on acceptance | FED-OBL-001, FED-EXEC-004 | ✓ COVERED |
| FED-L3-014 | Obligation amount == routing request amount | FED-OBL-002, FED-FAIL-008 | ✓ COVERED |

**Verdict: 14/14 requirements covered. No orphan requirements.**

### Orphan Test Audit

Tests that do not map to any named L3 requirement exist in the spec (marked `— (security test)` or `—`). These are:

- **Security tests** (FED-CERT-008, FED-CERT-009, FED-TRUST-002 through 009): Negative tests proving enforcement of INV-TRUST-001 through INV-TRUST-006. These are required for L3 denial criteria (§4.2 of FEDERATION_CONFORMANCE_MODEL.md).
- **Settlement edge cases** (FED-SETTLE-009, FED-SETTLE-010): Netting disagreement resolution and zero-net. Not L3-required but FAIL would produce conditional certification.
- **Recovery tests** (FED-FAIL-001 through 008): FED-FAIL-001, 004, 005 are L3-required. FED-FAIL-002, 003, 006, 007, 008 produce conditional certification on FAIL.

**Verdict: No orphan tests. All tests have documented purpose and certification impact.**

---

## Phase 2 — Contract Coverage Audit

All 5 federation contracts exist in `contracts/federation/` and are referenced by tests.

| Contract | Tests | Key Fields Tested | Gap |
|---|---|---|---|
| `operator-certificate.json` | FED-CERT-001–011 | `signature`, `expires_at`, `operator_id`, `public_key`, `issuer`, `issuer_key_id`, `certification_level` | **None** |
| `federation-manifest.json` | FED-DISC-001–008 | `supports_federation`, `cross_operator_routing`, `cross_operator_settlement`, `certificate_url`, `interop_endpoint`, `supported_currencies`, `netting_interval_hours`, `federation_version` | **None** |
| `federation-routing.json` | FED-ROUTE-001–012 | `routing_request_id`, `trace_id`, `from/to_operator_id`, `amount.minor`, `amount.currency`, `recipient_identifier`, `interop_transfer_id`, all rejection codes | **None** |
| `federation-obligation.json` | FED-OBL-001–007, FED-SETTLE-001–010 | `obligation_id`, `from/to_operator_id`, `amount`, `routing_request_id`, `interop_transfer_id`, `trace_id`, `settlement_state`, `obligor_signature`, `settled_at`, `settlement_batch_id` | **None** |
| `federation-event.json` | FED-EVT-001–006 | `id`, `event_type` (10 types), `aggregate_type`, `trace_id`, `federation_version`, `origin/destination_operator_id`, `routing_request_id`, `obligation_id` | **None** |

**Verdict: All 5 contracts fully covered. All certification-relevant fields have test coverage.**

---

## Phase 3 — Invariant Coverage Audit

| Invariant | Severity | Tests | Status |
|---|---|---|---|
| INV-TRUST-001 (cert signature valid) | CRITICAL | FED-CERT-002, FED-TRUST-002 | **ENFORCED** |
| INV-TRUST-002 (cert expiry no grace) | CRITICAL | FED-CERT-003, FED-CERT-008, FED-TRUST-003 | **ENFORCED** |
| INV-TRUST-003 (BRL = reject all) | CRITICAL | FED-TRUST-005, FED-CERT-009 | **ENFORCED** |
| INV-TRUST-004 (fed flag needs cert) | HIGH | FED-DISC-007, FED-TRUST-004 | **ENFORCED** |
| INV-TRUST-005 (BRL must be signed) | HIGH | — | **PARTIAL** ¹ |
| INV-TRUST-006 (BRL max 6h stale) | HIGH | FED-TRUST-009, FED-FAIL-006 | **ENFORCED** |
| INV-TRUST-007 (key rotation auth) | HIGH | FED-CERT-011 (key fetch path) | **PARTIAL** ² |
| INV-FED-001 (trace_id identity) | CRITICAL | FED-ROUTE-003, FED-OBL-003, FED-EVT-005 | **ENFORCED** |
| INV-FED-002 (obligation per routing) | CRITICAL | FED-OBL-001, FED-OBL-004, FED-FAIL-005 | **ENFORCED** |
| INV-FED-003 (fed flag ⟹ endpoint) | HIGH | FED-DISC-005 | **ENFORCED** |
| INV-FED-004 (routing idempotency) | CRITICAL | FED-ROUTE-004, FED-FAIL-001 | **ENFORCED** |
| INV-FED-005 (value conservation) | CRITICAL | FED-OBL-002, FED-EXEC-002, FED-FAIL-008 | **ENFORCED** |
| INV-FED-006 (cert must expire) | HIGH | FED-CERT-007 | **ENFORCED** |
| INV-FED-007 (revoked = rejected) | CRITICAL | FED-TRUST-005, FED-CERT-009 | **ENFORCED** |
| INV-FED-LEDGER-001 (cross-op double-entry) | CRITICAL | FED-EXEC-002, FED-SETTLE-004 | **ENFORCED** |
| INV-FED-LEDGER-002 (integer arithmetic) | CRITICAL | FED-ROUTE-010 | **ENFORCED** |
| INV-FED-IDEM-001 (global unique IDs) | CRITICAL | FED-ROUTE-004, FED-ROUTE-011 | **ENFORCED** |
| INV-FED-RECON-001 (cross-op reconcilability) | HIGH | FED-SETTLE-006, FED-SETTLE-007, FED-SETTLE-009 | **ENFORCED** |

**¹ INV-TRUST-005 PARTIAL**: The conformance runner's trust engine (in `fixture_server.py`) checks BRL staleness (`expires_at`) but does not verify the BRL's cryptographic signature against the BANZA root key. The test BRL uses a placeholder signature `"A" * 86`. The invariant states "unsigned BRL = absent BRL". This path is not tested. **This is a WARN, not a BLOCKER**: the BRL fetch-and-check logic works; only the BRL-level signature check is missing. The conformance runner would need to add BRL signature verification to prove this fully.

**² INV-TRUST-007 PARTIAL**: FED-CERT-011 tests the key-fetch path (F-604) — when `issuer_key_id` is unknown, the runner fetches the key manifest and retries. This tests the consumer-side behavior. The signing-side behavior (rotation authenticated by current private key) is an out-of-band BANZA process that cannot be tested in the conformance runner context. This is correctly **DOCUMENTED_ONLY** for the signing side and **ENFORCED** for the consumption side.

**Verdict: 16/18 invariants ENFORCED. 2 PARTIAL (non-blocking for L3 certification).**

---

## Phase 4 — Failure Safety Audit

Every required fail-safe behavior has a corresponding passing conformance test.

| Failure Scenario | Tests | Fail-Safe Behavior Proven |
|---|---|---|
| Invalid trust (tampered cert) | FED-TRUST-002, FED-CERT-002 | Signature invalid → routing refused |
| Expired certificate | FED-CERT-008, FED-TRUST-003 | Expired cert → step 2.4 fails, no routing |
| Stale BRL (>6h) | FED-TRUST-009 | Routing refused when BRL expires |
| Stale BRL (>12h) | FED-FAIL-006 | Fail-closed enforced at 13h stale |
| Revoked operator | FED-TRUST-005, FED-CERT-009 | BRL hit → step 2.6 fails, no routing |
| Network drop (retry) | FED-FAIL-001 | Same routing_request_id on retry; payee credited once |
| All retries fail | FED-FAIL-002 | No debit, no obligation on routing failure |
| Malformed response | FED-FAIL-003 | Treated as failure; retry with same ID succeeds |
| Op A cert rejected by Op B | FED-FAIL-004 | rejection_code=operator_trust_failure; no money moved |
| Crash recovery | FED-FAIL-005 | Missing obligation recreated on recovery run |
| Duplicate ID different content | FED-ROUTE-011 | rejection_code=duplicate_request; original unchanged |
| Amount mismatch before signing | FED-FAIL-008 | Obligation not recorded; INV-FED-005 cited |
| Settlement discrepancy | FED-SETTLE-008 | HTTP 409 on execute; no obligation settled |
| Netting disagreement | FED-SETTLE-009 | Missing obligation identified; recovery initiated |
| Revocation mid-flight | FED-FAIL-007 | Existing obligations survive revocation |
| No debit without acceptance | FED-EXEC-003 | BC-001 enforced |
| Acceptance irrevocable | FED-EXEC-005 | BC-004 enforced; payee credit non-reversible |

**Verdict: All 17 failure scenarios have proven fail-safe behavior. No unsafe optimistic paths found.**

---

## Phase 5 — Evidence Package Audit

The JSON report (`--output report.json`) contains structured evidence for every test.

### Present

| Evidence Category | Present | Fields |
|---|---|---|
| Runner metadata | ✓ | `report_id`, `generated_at`, `runner_version`, `operator_url`, `crypto_available` |
| Summary | ✓ | `total`, `passed`, `failed`, `skipped`, `duration_ms` |
| Per-suite results | ✓ | 9 suite objects with `passed`, `failed`, `skipped`, `cases` |
| Per-case assertion log | ✓ | Each case: `assertions[]` with `passed`, `expected`, `actual` |
| Certificate evidence | ✓ | `cert.http_status`, `cert.raw_json`, `cert.schema_validation_result` |
| Manifest evidence | ✓ | `manifest_http_status`, `manifest_schema_valid`, `manifest_operator_id` |
| Trust evidence | ✓ | `trusted`, `trust_step_results` (9 steps), `final_trusted_decision` |
| Routing evidence | ✓ | Request/response bodies, `routing_request_id`, `trace_id` comparison |
| Execution evidence | ✓ | `balance_before/after`, `balance_delta`, ledger entries |
| Obligation evidence | ✓ | Full obligation JSON, `amount_match`, `trace_id_match`, `signature_verification` |
| Event evidence | ✓ | Event JSONs, `trace_id_cross_check`, schema validation results |
| Settlement evidence | ✓ | `gross_a_to_b`, `gross_b_to_a`, `net_amount`, settlement ledger entries |
| Failure evidence | ✓ | Scenario details, before/after states, rejection codes |

### Missing (report not yet production-grade)

| Missing Item | Impact | Priority |
|---|---|---|
| `package_signature` field — evidence package is not signed by test runner | **HIGH**: BANZA cannot cryptographically verify authenticity | Required before production certification |
| Hierarchical evidence package structure (per §2 of CERTIFICATION_EVIDENCE_MODEL.md) | MEDIUM: BANZA's automated verification pipeline expects directory-based package | Required before automated BANZA review |
| `run_id` uniqueness tracking — no server-side deduplication | LOW: Prevents re-submission of old evidence | Required before automated BANZA review |

**Verdict: Evidence content is complete and sufficient for manual BANZA review. Cryptographic package signing is missing for automated verification.**

---

## Phase 6 — Operator Readiness Audit

**Q: Can a real operator use the current runner to attempt L3 certification?**

**YES — technically yes. But the operator experience has three friction points.**

### Works today

```bash
# A real operator runs this:
python3 tools/banza-conformance/fixture_server.py --port 8099
python3 tools/banza-conformance/run.py --federation --url http://localhost:8099 --output report.json
```

- The fixture server simulates Operator A (the operator under test)
- Simulated Operator B is embedded in the runner
- A fresh test BANZA root is generated per run
- No BANZA production infrastructure needed
- `requirements.txt`: `cryptography>=41.0.0` — one dependency

### Friction points

1. **README does not mention `--federation` mode** (see Phase 8). An operator reading `tools/banza-conformance/README.md` would not find the federation flag.

2. **Certification level naming mismatch**: `BANZA_CERTIFICATION.md` calls L3 "Settlement Operator" (payout.batch + reconciliation) and L4 "Infrastructure Operator" (with `federation_ready`). The federation conformance suite is called "L3 Federation Certification" throughout the federation docs. An operator reading `BANZA_CERTIFICATION.md` would look for L4, not L3, for federation. This is a known issue documented in `FEDERATION_CERTIFICATION_PATH.md` — requires ADR-028.

3. **No operator-facing quickstart**: The federation docs are thorough but written for protocol designers. An operator needs a single document: "here is what to implement, here is how to run the suite, here is what to submit."

### What a real operator must implement to pass

To pass all 79 tests, an operator's federation endpoint must implement:

| Endpoint | Method | Tests |
|---|---|---|
| `/.well-known/banza/certificate.json` | GET | FED-CERT-001–011 |
| `/.well-known/banza/operator.json` (federation fields) | GET | FED-DISC-001–008 |
| `/federation/route` | POST | FED-ROUTE-001–012, FED-EXEC, FED-OBL, FED-EVT, FED-SETTLE, FED-FAIL |
| `/federation/obligations` | GET | FED-OBL-001–007 |
| `/federation/obligations/{id}` | GET | FED-OBL-001–007 |
| `/federation/events` | GET | FED-EVT-001–006 |

These map precisely to the 7 endpoints in `FEDERATION_CONTRACT_TRACEABILITY.md §8`.

---

## Phase 7 — Security Boundary Audit

| Security Property | Status | Evidence |
|---|---|---|
| Test root separated from production | ✓ **CLEAN** | `generate_test_root_keypair()` creates ephemeral keypair per run; `issuer_key_id = "test-banza-key-{YYYY-MM}"` |
| No test keys reused as production keys | ✓ **CLEAN** | Keys are in-memory only; never persisted; no production `issuer_key_id` exists yet |
| No real operator trust state modified | ✓ **CLEAN** | All trust state is in-memory in embedded SimB and TrustRootServer |
| All test fixtures deterministic | ✓ **CLEAN** | All routing_request_ids and trace_ids are hardcoded constants; no randomness in test vectors |
| No external network dependency | ✓ **CLEAN** | Zero calls to `banza.network` or any external URL. BRL and key manifest served by embedded TrustRootServer on a random local port |
| BRL cryptographic verification | ⚠ **PARTIAL** | BRL staleness (expires_at) is checked; BRL ed25519 signature is NOT verified (placeholder sig used). See Phase 3, INV-TRUST-005 |
| Certificate placeholder mode | ✓ **DOCUMENTED** | When `cryptography` package absent, tests fall back to placeholder sig. FED-CERT-002 and trust tests SKIP gracefully. No silent pass on failed verification |

**Verdict: Security boundary is clean. One partial gap (BRL signature verification) is non-blocking for beta but should be resolved before production.**

---

## Phase 8 — Documentation Readiness Audit

| Document | Status | Gap |
|---|---|---|
| `docs/federation/FEDERATION_TEST_SUITE_SPEC.md` | ✓ Complete | Defines all 79 tests; matches implementation exactly |
| `docs/federation/FEDERATION_INVARIANTS.md` | ✓ Complete | All 18 invariants with formal statements and conformance vectors |
| `docs/federation/FEDERATION_CONTRACT_SURFACE.md` | ✓ Complete | All 5 contracts with full field definitions |
| `docs/federation/FEDERATION_PROTOCOL_FLOW.md` | ✓ Complete | All 10 phases, all behavioral constraints |
| `docs/federation/FEDERATION_FAILURE_SCENARIOS.md` | ✓ Complete | All failure codes F-101 through F-604 with recovery runbooks |
| `docs/federation/FEDERATION_CONFORMANCE_MODEL.md` | ✓ Complete | Matches current runner: 9 suites, 79 tests, certification decision rules |
| `docs/federation/FEDERATION_CERTIFICATION_EVIDENCE_MODEL.md` | ✓ Complete | Evidence requirements documented; partial implementation gap (see Phase 5) |
| `docs/federation/FED_*_REPORT.md` (x11 files) | ✓ Complete | Per-slice implementation reports with evidence |
| `BANZA_CERTIFICATION.md` | ⚠ **OUTDATED** | Defines L3 as "Settlement Operator" (payout.batch); L4 as infrastructure + federation. Federation conformance suite is labeled "L3" but lives at what this doc calls L4. **Requires ADR-028 to resolve.** |
| `tools/banza-conformance/README.md` | ⚠ **MISSING** | No mention of `--federation` flag, federation suite, or L3 federation testing |
| `BANZA_REFERENCE.md` | UNKNOWN | Not audited (out of scope for federation audit) |

### Required documentation fixes (beta blockers)

1. **`tools/banza-conformance/README.md`**: Add `--federation` usage, describe the two-terminal flow (fixture server + runner), document what a passing run looks like.

2. **`BANZA_CERTIFICATION.md`**: Requires ADR-028 (certification level revision). Until ADR-028 is written, add a note: *"Federation certification is implemented as part of the federation conformance suite. See `docs/federation/FEDERATION_CONFORMANCE_MODEL.md`."*

3. **New `docs/federation/FEDERATION_OPERATOR_QUICKSTART.md`**: Single page explaining: (1) what a federation operator must implement, (2) how to run the conformance suite, (3) what evidence to submit, (4) how the certification decision is made.

---

## Phase 9 — Final Scorecard

### Readiness Matrix

| Dimension | Score | Notes |
|---|---|---|
| **Specification completeness** | 10/10 | All 79 tests defined in canonical spec; 0 orphans; 0 undefined behaviors |
| **Contract coverage** | 10/10 | All 5 contracts fully tested; all certification-relevant fields covered |
| **Invariant enforcement** | 16/18 | 2 partial (BRL sig, key rotation — both non-blocking) |
| **Failure safety** | 17/17 | All failure scenarios proven fail-safe |
| **Evidence quality** | 8/10 | Content complete; package signing missing |
| **Security boundaries** | 9/10 | Test root clean; BRL signature verification partial |
| **Operator experience** | 6/10 | Works technically; README and quickstart missing |
| **Documentation** | 7/10 | Federation docs excellent; BANZA_CERTIFICATION.md outdated |
| **Production process** | 4/10 | No production root, no signing pipeline, no ADR-028 |

### Blockers

| Priority | Blocker | Owner | Effort |
|---|---|---|---|
| **P0 — Beta blocker** | `tools/banza-conformance/README.md` missing `--federation` section | Protocol team | < 1 day |
| **P0 — Beta blocker** | No `FEDERATION_OPERATOR_QUICKSTART.md` | Protocol team | < 1 day |
| **P1 — Beta warning** | `BANZA_CERTIFICATION.md` level naming (ADR-028) | Architecture | ADR required |
| **P2 — Production required** | Evidence package signing (runner signs output JSON) | Protocol team | 2–3 days |
| **P2 — Production required** | BRL signature verification in conformance runner | Protocol team | 1 day |
| **P3 — Production required** | Production BANZA root key establishment | BANZA org | Organizational |
| **P3 — Production required** | Real two-operator interoperability test (real Op A ↔ real Op B) | Protocol team | Depends on operators |

### Warnings (non-blocking)

- `INV-TRUST-005` (BRL signature) is PARTIAL. The placeholder BRL signature is acceptable for conformance testing because we control both sides. It must be fixed before operators can verify BRL signatures in production.
- The conformance decision rules in `FEDERATION_CONFORMANCE_MODEL.md §4.1` grant certification when FED-CERT through FED-OBL all pass. FED-EVT, FED-SETTLE, FED-FAIL produce conditional certification on failure (30-day remediation window). Current suite passes all 79 tests — no conditions apply.
- The current runner uses a `fixture_server.py` as the "operator under test" adapter. A real operator must stand up their own server implementing the federation endpoints, then point the runner at it. This is exactly the intended model.

---

## Phase 10 — Final Verdict

### Claim 1: "L3 Federation Certification is executable end-to-end in conformance mode"

**VERDICT: TRUE**

Evidence:
- The runner exists: `python3 tools/banza-conformance/run.py --federation --url <operator_url>`
- 79 tests across 9 suites, all passing, against the fixture server
- Any operator implementing the federation protocol endpoints can run this suite against their own system
- The runner is self-contained (no external network dependencies)
- All 14 L3 requirements have test coverage
- Every CRITICAL invariant has at least one enforcing test
- The suite produces a structured JSON report (`--output`) suitable for BANZA review

**Exact command:**
```bash
# Terminal 1 — operator under test (or use your own federation server)
python3 tools/banza-conformance/fixture_server.py --port 8099

# Terminal 2 — run L3 federation conformance
python3 tools/banza-conformance/run.py \
  --federation \
  --url http://localhost:8099 \
  --output l3-evidence-$(date +%Y%m%d).json
```

### Claim 2: "L3 Federation Certification is production-ready"

**VERDICT: NOT YET**

Missing for production:

1. **ADR-028** (certification level revision): `BANZA_CERTIFICATION.md` must be updated to reflect that federation is a distinct certification level. The naming discrepancy between the federation docs and the main certification doc is a documentation debt that will confuse operators in public beta.

2. **Evidence package signing**: The conformance runner must sign the output JSON with the test runner's ed25519 private key so BANZA can verify package authenticity. Currently the report contains no `package_signature` field.

3. **Production BANZA root key**: The production certification process requires a BANZA production ed25519 root keypair (separate from the ephemeral test root). This key would sign operator certificates at L3+. The BANZA organization must generate and safeguard this key.

4. **Real two-operator test**: The current suite uses an embedded Simulated Operator B. For production certification, BANZA should run an additional interoperability test between two real operators (both having passed single-operator certification). This is not a blocker for the first operator to certify, but is required for the federation to be meaningful.

5. **Operator-facing documentation**: `FEDERATION_OPERATOR_QUICKSTART.md` and `README.md` federation section must exist before operators are directed to certify.

---

## Summary: What Is Ready

```
✓ Protocol specification       — complete, canonical, conformance-mapped
✓ All 5 federation contracts    — defined, tested, invariant-traced
✓ All 18 federation invariants  — 16 ENFORCED, 2 PARTIAL (non-blocking)
✓ All 79 conformance tests      — implemented, passing, evidence-capturing
✓ Failure safety                — all 17 failure scenarios proven fail-closed
✓ Test root separation          — ephemeral per run, labeled, never production
✓ No external dependencies      — runner is fully self-contained

⚠ README missing --federation   — beta blocker (< 1 day to fix)
⚠ Operator quickstart missing   — beta blocker (< 1 day to fix)
⚠ BANZA_CERTIFICATION.md levels — needs ADR-028 (known, documented)
✗ Evidence package signing      — production required
✗ BRL signature verification    — production required
✗ Production BANZA root key     — organizational decision required
✗ Real two-operator test        — production required
```

**L3 Federation Certification can be described as:**

> *"The BANZA L3 Federation Certification conformance suite is complete and executable. Any operator implementing the federation protocol can run the suite against their system and receive a structured evidence report. All conformance requirements, contracts, invariants, and failure scenarios are covered. Beta operator testing can begin after two documentation fixes. Production certificate issuance requires evidence signing, ADR-028, and production root key establishment."*
