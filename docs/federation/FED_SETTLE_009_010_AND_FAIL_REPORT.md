# FED-SETTLE-009, FED-SETTLE-010 and FED-FAIL-001 through FED-FAIL-008 Report

**Document ID:** FED-SETTLE-009-010-AND-FAIL-REPORT-001  
**Date:** 2026-05-31  
**Status:** ALL 79 PASS — L3 Federation Certification evidence complete  
**Authority:** FEDERATION_TEST_SUITE_SPEC.md, FEDERATION_FAILURE_SCENARIOS.md, FEDERATION_INVARIANTS.md, ADR-026

---

## Result

```
[Suite] Certificate Validation          → 11 passed, 0 failed, 0 skipped
[Suite] Discovery and Manifest          → 8 passed,  0 failed, 0 skipped
[Suite] Trust Establishment             → 9 passed,  0 failed, 0 skipped
[Suite] Routing Negotiation             → 12 passed, 0 failed, 0 skipped
[Suite] Transfer Execution              → 8 passed,  0 failed, 0 skipped
[Suite] Obligation Lifecycle            → 7 passed,  0 failed, 0 skipped
[Suite] Federation Event Emission       → 6 passed,  0 failed, 0 skipped
[Suite] Netting and Settlement          → 10 passed, 0 failed, 0 skipped
[Suite] Failure and Recovery            → 8 passed,  0 failed, 0 skipped
Total: 79/79 ALL PASS
```

Full FED-SETTLE output:
```
  ✓ FED-SETTLE-001 — Obligation Export Includes All Pending Obligations
  ✓ FED-SETTLE-002 — Net Position Computed Correctly
  ✓ FED-SETTLE-003 — Both Operators Independently Compute Same Net
  ✓ FED-SETTLE-004 — Settlement Execution: Ledger Entries Correct
  ✓ FED-SETTLE-005 — Obligations Marked Settled With Required Fields
  ✓ FED-SETTLE-006 — Reconciliation: All Accepted Routing Requests Have Obligations
  ✓ FED-SETTLE-007 — Reconciliation: Trace Cross-Check Across Both Operators
  ✓ FED-SETTLE-008 — Settlement Blocked on Unresolved Discrepancy
  ✓ FED-SETTLE-009 — Netting Disagreement: Full Obligation Exchange Identifies Discrepancy
  ✓ FED-SETTLE-010 — Zero-Net Case: No Bank Transfer; All Obligations Settled
```

Full FED-FAIL output:
```
  ✓ FED-FAIL-001 — Network Timeout Retry With Same routing_request_id Succeeds (F-101)
  ✓ FED-FAIL-002 — All Retries Fail: Payment Fails, No Debit, No Obligation
  ✓ FED-FAIL-003 — Unparseable Response Treated as Network Failure (F-102)
  ✓ FED-FAIL-004 — Operator A Certificate Rejected by Operator B (F-204)
  ✓ FED-FAIL-005 — Crash Recovery: Missing Obligation Recreated (F-402)
  ✓ FED-FAIL-006 — Extended BRL Outage: Fail-Closed After 12 Hours (F-602)
  ✓ FED-FAIL-007 — Revocation Mid-Flight: Obligation Survives Revocation
  ✓ FED-FAIL-008 — Obligation Amount Mismatch Detected Before Signing (F-404)
```

---

## Commands

```bash
# Terminal 1 — start fixture server (Operator A)
python3 tools/banza-conformance/fixture_server.py --port 8099

# Terminal 2 — run full suite (all 79 tests)
python3 tools/banza-conformance/run.py --federation --url http://localhost:8099

# Run only FED-SETTLE (all 10)
python3 tools/banza-conformance/run.py --federation --fed-suite settle --url http://localhost:8099

# Run only FED-FAIL (all 8)
python3 tools/banza-conformance/run.py --federation --fed-suite fail --url http://localhost:8099
```

---

## FED-SETTLE-009: Netting Disagreement Resolution

### Scenario
Operator A has 3 obligations (50,000 × 3 = 150,000 AOA).  
Simulated Operator B has 4 accepted routings — one was accepted but Op A crashed before committing the obligation.

### Protocol Flow
1. 3 routing requests routed normally → 3 obligations on Op A
2. A 4th routing is injected directly into Sim Op B's routing store (simulates Op A crash after Op B accepted)
3. Reconcile endpoint cross-references Op A's obligations vs Op B's accepted list
4. Discrepancy detected: 1 routing_request_id present on Op B, absent on Op A
5. Recovery endpoint creates the missing obligation + debit on Op A
6. Post-recovery: all 4 routing_request_ids have obligations on Op A

### Evidence

| Item | Value |
|---|---|
| `op_a_obligation_count` | 3 (before recovery) → 4 (after) |
| `op_b_accepted_count` | 4 |
| `missing_on_a` | `["rr-...9004"]` |
| `discrepancy_detected` | true |
| `recovery_initiated` | true (HTTP 200 from recover-obligation) |
| `obligation_exists_after_recovery` | true |

---

## FED-SETTLE-010: Zero-Net Settlement

### Scenario
Equal obligations flowing in both directions:
- A→B: 2 × 30,000 = 60,000 AOA gross
- B→A: 2 × 30,000 = 60,000 AOA gross
- net_amount = 0

### Protocol Behavior
- No bank transfer initiated (no money needs to move)
- All A→B obligations still marked `settlement_state=settled`
- `zero_net=True` in the batch and execute response
- `simulated_bank_reference=None` (no bank transfer)
- 0 settlement ledger entries (no entries needed for zero-net)

### Evidence

| Item | Value |
|---|---|
| `gross_a_to_b` | 60,000 |
| `gross_b_to_a` | 60,000 |
| `net_amount` | 0 |
| `zero_net` | true |
| `no_bank_transfer` | true |
| `settlement_ledger_entry_count` | 0 |
| `simulated_bank_reference` | null |
| All A→B obligation states | `settled` |

---

## Failure Injection Infrastructure

### New in runner_infra.py

| Method | Behavior | Used By |
|---|---|---|
| `set_drop_next_route(n)` | Sim Op B returns HTTP 503 for next N requests | FED-FAIL-001, FED-FAIL-002 |
| `set_malformed_response_once()` | Sim Op B returns HTTP 200 with non-JSON body | FED-FAIL-003 |
| `set_trust_failure_once()` | Sim Op B returns `rejection_code=operator_trust_failure` | FED-FAIL-004 |
| `set_brl_very_stale(hours)` | BRL with `expires_at = now - hours` | FED-FAIL-006 |
| `inject_accepted_routing_on_b(...)` | Directly add accepted routing to Sim Op B store | FED-SETTLE-009 |
| `get_sim_b_accepted_routing_ids()` | List all routing_request_ids accepted by Sim Op B | FED-SETTLE-009 |

### New in fixture_server.py

| Endpoint | Purpose | Used By |
|---|---|---|
| `POST /conformance/federation/fail/inject-crash-state` | Inject accepted routing_commit with no obligation/debit | FED-FAIL-005 |
| `POST /conformance/federation/fail/trigger-recovery` | Scan for unrecovered accepted routings; create obligation+debit | FED-FAIL-005 |
| `POST /conformance/federation/fail/recover-obligation` | Create single obligation+debit from provided routing details | FED-SETTLE-009 |
| `POST /conformance/federation/fail/inject-obligation-amount-override` | Make next obligation creation use override amount (triggers INV-FED-005) | FED-FAIL-008 |
| `POST /conformance/federation/netting/reconcile` | Cross-reference Op A obligations vs provided accepted IDs | FED-SETTLE-009 |

### Definitive-only routing_commits (fixture_server.py change)

The fixture server now only stores routing outcomes in `routing_commits` when the outcome is **definitive**:
- `routing_status == "accepted"` — prevents double-debit
- `rejection_code ∈ {valid rejection codes}` — idempotent replay of definitive rejections

**Transient failures** (503, connection error, malformed response) are NOT stored. This allows the test runner to retry with the same `routing_request_id`, which is the behavior required by INV-FED-004.

---

## Tests Implemented

### FED-SETTLE-009–010

| Test | Spec Reference | Key Behavior Proven | Invariant |
|---|---|---|---|
| FED-SETTLE-009 | Suite FED-SETTLE | Netting disagreement detected; missing routing_request_id identified; recovery creates obligation | INV-FED-RECON-001 |
| FED-SETTLE-010 | Suite FED-SETTLE | Zero-net: no bank transfer; obligations still settled | INV-FED-LEDGER-001 |

### FED-FAIL-001–008

| Test | Failure Code | Key Behavior Proven | Invariant |
|---|---|---|---|
| FED-FAIL-001 | F-101 | Idempotent retry after network drop; payee credited once; one obligation | INV-FED-004 |
| FED-FAIL-002 | F-104 | All retries exhausted → no debit, no obligation, payment fails | INV-FED-002 |
| FED-FAIL-003 | F-102 | Malformed response treated as failure; no debit; retry succeeds | INV-FED-004 |
| FED-FAIL-004 | F-204 | Operator A cert rejected → `rejection_code=operator_trust_failure`; no money moved | INV-TRUST-001 |
| FED-FAIL-005 | F-402 | Crash recovery recreates missing obligation; debit also created atomically | INV-FED-002 |
| FED-FAIL-006 | F-602 | BRL >12h stale → trust step 2.6 fails; routing refused fail-closed | INV-TRUST-006 |
| FED-FAIL-007 | — | Revocation after obligation recording doesn't delete existing obligations | INV-FED-002 |
| FED-FAIL-008 | F-404 | Amount mismatch before signing halts obligation recording; no debit | INV-FED-005 |

---

## Evidence Per FED-FAIL Test

### FED-FAIL-001 (Idempotent Retry)
| Item | Value |
|---|---|
| First attempt result | `routing_status=rejected` (503 from Sim Op B) |
| No payer debit after first | true |
| No obligation after first | true |
| Second attempt result | `routing_status=accepted` |
| Payee balance after | 50,000 AOA (credited once) |
| Obligation count | 1 (created once) |

### FED-FAIL-002 (All Retries Fail)
| Item | Value |
|---|---|
| Routing result | `routing_status=rejected` (503 ×3) |
| Payer balance unchanged | true |
| No obligation recorded | true |

### FED-FAIL-003 (Malformed Response)
| Item | Value |
|---|---|
| First attempt HTTP status | 500 (fixture server failed to parse) |
| No payer debit after malformed | true |
| Retry accepted | true |
| Payee credited once | true (50,000 AOA) |

### FED-FAIL-004 (Op A Cert Rejected)
| Item | Value |
|---|---|
| `rejection_code` | `operator_trust_failure` |
| Payer debited | false |
| Obligation recorded | false |

### FED-FAIL-005 (Crash Recovery)
| Item | Value |
|---|---|
| No obligation before recovery | true |
| No debit before recovery | true |
| `recovered_count` | 1 |
| Obligation exists after recovery | true |
| Debit exists after recovery | true |
| Both linked by `routing_request_id` | true |

### FED-FAIL-006 (Extended BRL Outage)
| Item | Value |
|---|---|
| BRL stale hours | 13 (> 12h threshold) |
| `trusted` | false |
| Step 2.6 result | fail (brl_expired) |
| Routing refused | true |

### FED-FAIL-007 (Revocation Mid-Flight)
| Item | Value |
|---|---|
| Obligation state before revocation | `pending` |
| Obligation state after revocation | `pending` (unchanged) |
| Obligation still exists | true |
| `obligation_id` unchanged | true |

### FED-FAIL-008 (Amount Mismatch)
| Item | Value |
|---|---|
| Routing amount | 50,000 AOA |
| Attempted obligation amount | 49,999 AOA |
| `routing_status` | `failed_inv_fed_005` |
| Payer debited | false |
| Obligation recorded | false |
| Invariant reference | `INV-FED-005` |

---

## Files Modified

| File | Change |
|---|---|
| `tools/banza-conformance/runner_infra.py` | Added 6 new failure injection methods; added `drop_next_route_count`, `malformed_response_once`, `trust_failure_override_once` to Sim Op B state; modified `_handle_route` to check flags; updated `reset_routing_state` to clear flags |
| `tools/banza-conformance/fixture_server.py` | Added `_initial_fail_inject_state()`; added `fail_inject` to server state; added 5 new POST endpoints + 1 GET endpoint for failure injection; added `reconcile` endpoint; modified `_handle_fed_route` to check obligation amount overrides and only store definitive outcomes in routing_commits; modified `_handle_netting_execute` for zero-net case |
| `tools/banza-conformance/run_fed.py` | Version → 1.1.0-slice10; added SETTLE-009/010 and FAIL-001–008 constants; added 8 HTTP helper functions (netting reconcile, 5 fail-inject); added 10 new test functions; extended `run_suite_fed_settle` (8→10 tests); added `run_suite_fed_fail`; updated `run_federation_mode` |

---

## What Is Now Proven (Slice 10 additions)

| Assertion | Proven By |
|---|---|
| Netting disagreement between operators is detected via obligation cross-reference | FED-SETTLE-009 |
| Missing obligation (crash scenario) identified by routing_request_id | FED-SETTLE-009 |
| Recovery procedure creates obligation + debit for missing routing_request_id | FED-SETTLE-009 |
| Zero-net position: no bank transfer initiated when gross_A_to_B == gross_B_to_A | FED-SETTLE-010 |
| Obligations still marked settled when net = 0 (without bank transfer) | FED-SETTLE-010 |
| Idempotent retry after network failure succeeds; payee credited exactly once | FED-FAIL-001 |
| When all retries fail: no payer debit, no obligation, payment fails cleanly | FED-FAIL-002 |
| Malformed response is treated as network failure; retry with same ID succeeds | FED-FAIL-003 |
| Operator B rejects Operator A cert failure with `operator_trust_failure` | FED-FAIL-004 |
| Crash recovery discovers and closes the obligation gap (F-402 runbook) | FED-FAIL-005 |
| BRL older than 12 hours causes routing refusal at step 2.6 (fail-closed) | FED-FAIL-006 |
| Revoking a peer after obligation recording does not delete existing obligations | FED-FAIL-007 |
| Amount mismatch detected before signing halts obligation creation with INV-FED-005 | FED-FAIL-008 |

---

## L3 Certification Checklist Status

From `FEDERATION_CERTIFICATION_EVIDENCE_MODEL.md` §6:

```
☑ Evidence package signature — runner v1.1.0-slice10
☑ FED-CERT: all 11 cases PASS
☑ FED-DISC: all 8 cases PASS
☑ FED-TRUST: all 9 cases PASS
☑ FED-ROUTE: cases 001-012 PASS
☑ FED-EXEC: cases 001-008 PASS
☑ FED-OBL: cases 001-007 PASS
☑ FED-EVT: all 6 cases PASS
☑ FED-SETTLE: cases 001-010 PASS
☑ FED-FAIL: cases 001-008 PASS (cases 001, 004, 005 are L3 required — ALL PASS)
☑ Zero CRITICAL-severity failures
☐ Manual review (key management, bank details, TLS confirmation)
☐ Operator URL publicly reachable
☐ Production certificate request submitted
```

**Automated conformance is complete (79/79).** Remaining items are operational/manual and require BANZA bilateral interaction.

---

## Next Steps

The full automated conformance suite (9 suites, 79 tests) is now complete. The suite spec defined exactly 79 tests across 9 suites — all are implemented and passing.

```
FED-CERT  001–011 ✓  (11)
FED-DISC  001–008 ✓  (8)
FED-TRUST 001–009 ✓  (9)
FED-ROUTE 001–012 ✓  (12)
FED-EXEC  001–008 ✓  (8)
FED-OBL   001–007 ✓  (7)
FED-EVT   001–006 ✓  (6)
FED-SETTLE 001–010 ✓ (10)
FED-FAIL  001–008 ✓  (8)
                     ────
Total:               79  ← all passing
```

**L3 Federation Certification is executable end-to-end.** Submit the evidence package to BANZA to proceed with production certificate issuance.
