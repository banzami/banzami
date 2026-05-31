# FED-EXEC-001 through FED-EXEC-008 Report

**Document ID:** FED-EXEC-001-TO-008-REPORT-001  
**Date:** 2026-05-31  
**Status:** ALL 48 PASS — transfer execution semantics conformance layer complete  
**Authority:** FEDERATION_TEST_SUITE_SPEC.md, FEDERATION_PROTOCOL_FLOW.md, ADR-026

---

## Result

```
[Suite] Certificate Validation (blocking=True)
  ✓ FED-CERT-001 through ✓ FED-CERT-011
  → 11 passed, 0 failed, 0 skipped

[Suite] Discovery and Manifest Validation (blocking=True)
  ✓ FED-DISC-001 through ✓ FED-DISC-008
  → 8 passed, 0 failed, 0 skipped

[Suite] Trust Establishment (blocking=True)
  ✓ FED-TRUST-001 through ✓ FED-TRUST-009
  → 9 passed, 0 failed, 0 skipped

[Suite] Routing Negotiation (blocking=True)
  ✓ FED-ROUTE-001 through ✓ FED-ROUTE-012
  → 12 passed, 0 failed, 0 skipped

[Suite] Transfer Execution (blocking=True)
  ✓ FED-EXEC-001 — Payee Wallet Credited Simultaneously with Acceptance
  ✓ FED-EXEC-002 — Ledger Entries Correct on Both Operators
  ✓ FED-EXEC-003 — No Debit Without Acceptance (BC-001)
  ✓ FED-EXEC-004 — Debit and Obligation Are Atomic (BC-003)
  ✓ FED-EXEC-005 — Acceptance Is Irrevocable on Operator B (BC-004)
  ✓ FED-EXEC-006 — Operator B Internal Failure After Acceptance Does Not Affect Obligation
  ✓ FED-EXEC-007 — Provisional Completion: All 7 Criteria Met
  ✓ FED-EXEC-008 — Double-Debit Prevention Via Posting Idempotency Key
  → 8 passed, 0 failed, 0 skipped
```

---

## Commands

```bash
# Terminal 1 — start fixture server (Operator A)
python3 tools/banza-conformance/fixture_server.py --port 8099

# Terminal 2 — run full suite (FED-CERT + FED-DISC + FED-TRUST + FED-ROUTE + FED-EXEC)
python3 tools/banza-conformance/run.py --federation --url http://localhost:8099

# Run only FED-EXEC
python3 tools/banza-conformance/run.py --federation --fed-suite exec --url http://localhost:8099
```

---

## Execution Model Implemented

### Core behavioral decision: Operator B acceptance is simultaneous execution

When Operator B returns `status: "accepted"`, the payee wallet is already credited.
This is proven by FED-EXEC-001: querying the payee wallet immediately after receiving
the accepted response shows the balance has already increased.

### Phase 4 — Transfer Execution (Operator A)

On receiving `status: "accepted"` from Operator B, Operator A executes atomically:

```
DEBIT  payer_wallet                        amount.minor
CREDIT federation_payable:operator-b-test  amount.minor
→ record obligation
→ emit federation.payment.initiated event
```

The three operations (debit + obligation + event) are committed in a single lock-held
transaction under `_handle_fed_route`. Either all succeed or none do — there is no
intermediate state where debit exists without obligation.

---

## Atomicity Model

**Implemented in `fixture_server.py` `_handle_fed_route`:**

```
Phase 1 (under lock):
  - Idempotency check: routing_commits[routing_request_id] → return cached if found
  - Balance check: sender_balance ≥ amount_minor

Phase 2 (outside lock):
  - Forward pre-signed routing request to Sim Op B
  - Receive routing response

Phase 3 (under lock):
  - Re-check idempotency (race guard)
  - If accepted:
      wallet[sender].balance_minor -= amount_minor     (DEBIT)
      ledger.append(DEBIT entry with trace_id)
      obligations[routing_request_id] = obligation     (one per routing_request_id)
      events.append(federation.payment.initiated)
      routing_commits[routing_request_id] = result     (idempotency commit)
  - If rejected: routing_commits[routing_request_id] = result (no debit, no obligation)
```

**Invariant enforcement:**
- No valid state where DEBIT exists without obligation (BC-003)
- No debit without acceptance (BC-001, BC-002)
- `routing_commits` dict acts as unique constraint on `routing_request_id` for debit + obligation

---

## In-Memory Ledger and Obligation Model

### Operator A (fixture_server.py `fed_exec` state)

| Component | Structure | Purpose |
|---|---|---|
| `wallets["wallet-sender-test-001"]` | `{balance_minor: 500000}` | Pre-funded payer wallet |
| `ledger` | List of DEBIT entries with trace_id | Audit trail for Operator A side |
| `obligations` | Dict routing_request_id → obligation | One per accepted routing |
| `routing_commits` | Dict routing_request_id → result | Idempotency cache for Phase 4 |
| `events` | List of federation events | `federation.payment.initiated` per acceptance |

### Obligation record structure

```json
{
  "schema_version": "1",
  "obligation_id": "ob-<uuid>",
  "from_operator_id": "operator-a-test",
  "to_operator_id": "operator-b-test",
  "amount": {"minor": 50000, "currency": "AOA"},
  "routing_request_id": "rr-00000000-0000-0000-0000-000000000001",
  "interop_transfer_id": "itx-<uuid>",
  "trace_id": "tr-00000000-0000-0000-0000-000000000001",
  "recorded_at": "<ISO 8601>",
  "settlement_state": "pending"
}
```

### Simulated Operator B (runner_infra.py `_sim_b_state`)

| Component | Structure | Purpose |
|---|---|---|
| `wallets["wallet-payee-test-001"]` | `{status: active, balance_minor: N}` | Payee wallet |
| `ledger` | List of CREDIT entries with trace_id | Audit trail for Operator B side |
| `events` | List of federation events | `routing.accepted` + `payment.completed` |

---

## Conformance Endpoints Added to Operator A (fixture_server.py)

| Endpoint | Purpose | Used By |
|---|---|---|
| `POST /conformance/federation/route` | Execute routing flow; debit + obligation on acceptance | FED-EXEC-002–008 |
| `POST /conformance/federation/reset` | Reset all execution state (wallet, ledger, obligations, events) | All FED-EXEC tests |
| `GET /conformance/federation/wallet/{id}` | Query payer wallet balance | FED-EXEC-003, 008 |
| `GET /conformance/federation/ledger/{wallet_id}` | Query ledger entries with trace_id | FED-EXEC-002, 004, 007, 008 |
| `GET /conformance/federation/obligations/{rr_id}` | Query single obligation by routing_request_id | FED-EXEC-004, 006, 007, 008 |
| `GET /conformance/federation/obligations` | Query all obligations | (available) |
| `GET /conformance/federation/events` | Query federation events emitted by Operator A | FED-EXEC-007 |

## New Endpoints on Simulated Operator B (runner_infra.py)

| Endpoint | Purpose | Used By |
|---|---|---|
| `GET /federation/events` | Federation events emitted by Sim Op B | FED-EXEC-007 |
| `GET /ledger/{wallet_id}` | Payee ledger entries with trace_id | FED-EXEC-002 |

---

## Tests Implemented

| Test | Scenario | Key Assertion | Severity | Invariant |
|---|---|---|---|---|
| FED-EXEC-001 | Payee credited simultaneously with acceptance | `balance_after - balance_before == amount.minor` immediately | CRITICAL | INV-FED-LEDGER-001 |
| FED-EXEC-002 | Ledger entries correct on both operators | Operator A: DEBIT with trace_id; Operator B: CREDIT with trace_id; amounts match | CRITICAL | INV-FED-LEDGER-001, INV-FED-005 |
| FED-EXEC-003 | No debit when routing rejected | `balance_after == balance_before` after rejection | CRITICAL | BC-001 |
| FED-EXEC-004 | Debit and obligation are atomic | DEBIT entry exists ↔ obligation exists; both linked by routing_request_id | CRITICAL | BC-003 |
| FED-EXEC-005 | Acceptance is irrevocable | Cancel endpoint returns 404/405; payee balance unchanged | STANDARD | BC-004 |
| FED-EXEC-006 | Sim Op B internal state irrelevant to obligation | Obligation exists, settlement_state=pending regardless | STANDARD | INV-FED-002 |
| FED-EXEC-007 | All 7 provisional completion criteria | All 7 criteria true simultaneously | STANDARD | INV-FED-001 |
| FED-EXEC-008 | Double-debit prevention | Balance decremented exactly once; exactly 1 DEBIT entry; exactly 1 obligation | CRITICAL | INV-FED-IDEM-001 |

---

## Evidence Captured Per Test

### FED-EXEC-001 (payee credited simultaneously)

| Item | Value |
|---|---|
| `payee_wallet` | `wallet-payee-test-001` |
| `balance_before` | 0 |
| `balance_after` | 50000 |
| `balance_delta` | 50000 |
| `expected_delta` | 50000 |
| `interop_transfer_id` | `itx-<uuid4>` |

### FED-EXEC-002 (cross-operator ledger entries)

| Item | Value |
|---|---|
| `operator_a_debit_entry.entry_type` | `DEBIT` |
| `operator_a_debit_entry.amount_minor` | 50000 |
| `operator_a_debit_entry.trace_id` | `tr-00000000-0000-0000-0000-000000000001` |
| `sim_op_b_credit_entry.entry_type` | `CREDIT` |
| `sim_op_b_credit_entry.amount_minor` | 50000 |
| `sim_op_b_credit_entry.trace_id` | `tr-00000000-0000-0000-0000-000000000001` |

### FED-EXEC-004 (atomicity)

| Item | Value |
|---|---|
| `debit_exists` | true |
| `obligation_exists` | true |
| `atomicity_check` | true |
| `obligation.settlement_state` | `pending` |
| `obligation.routing_request_id` | matches `debit_entry.routing_request_id` |

### FED-EXEC-007 (all 7 criteria)

| Criterion | Status |
|---|---|
| (1) routing_request accepted | ✓ |
| (2) payer debited on Operator A | ✓ |
| (3) payee credited on Operator B | ✓ |
| (4) obligation pending | ✓ |
| (5) federation.payment.initiated event on Operator A | ✓ |
| (6) federation.payment.completed event on Operator B | ✓ |
| (7) both events share trace_id | ✓ |

### FED-EXEC-008 (double-debit prevention)

| Item | Value |
|---|---|
| `balance_initial` | 500000 |
| `balance_after_first_call` | 450000 |
| `balance_after_second_call` | 450000 (unchanged — no double-debit) |
| `debit_entry_count` | 1 |
| `obligation_exists` | true (exactly 1) |
| `double_debit_check` | PASS |

---

## Files Modified

| File | Change |
|---|---|
| `tools/banza-conformance/runner_infra.py` | Added `ledger` and `events` to Sim Op B state; emit events + record ledger entry on acceptance; added `GET /federation/events` and `GET /ledger/{wallet_id}` endpoints; updated `reset_routing_state` to clear ledger and events; added `get_sim_b_events()` and `get_sim_b_ledger()` to `RunnerInfra` |
| `tools/banza-conformance/fixture_server.py` | Added `import uuid`; added `_initial_fed_exec_state()`; added `fed_exec` to server state; added 7 conformance query/execution endpoints; implemented `_handle_fed_route` (two-phase atomic commit) and `_handle_fed_reset` |
| `tools/banza-conformance/run_fed.py` | Version → 0.7.0-slice6; updated docstring for Slice 6; added `run_exec` flag; added exec helpers (`_build_exec_route_payload`, `_call_fed_route`, `_get_wallet_op_a`, `_get_ledger_op_a`, `_get_obligation_op_a`, `_get_events_op_a`, `_reset_exec_state`); added FED-EXEC-001 through FED-EXEC-008; added `run_suite_fed_exec`; updated `run_federation_mode` with exec suite; updated summary print with FED-EXEC assertions proven |

---

## What Is Now Proven

| Assertion | Proven By |
|---|---|
| Payee wallet credited simultaneously with Operator B's acceptance response | FED-EXEC-001 |
| Operator A DEBIT entry exists with correct amount and trace_id | FED-EXEC-002 |
| Operator B CREDIT entry exists with correct amount and trace_id | FED-EXEC-002 |
| Cross-operator amounts are identical — no value created or destroyed | FED-EXEC-002 |
| Payer wallet unchanged when routing is rejected | FED-EXEC-003 |
| No debit exists without corresponding obligation | FED-EXEC-004 |
| No obligation exists without corresponding debit | FED-EXEC-004 |
| Operator A debit + obligation committed in one atomic operation | FED-EXEC-004 |
| Cancel endpoint on Operator B returns 404 — no cancellation path exists | FED-EXEC-005 |
| Payee balance unchanged after cancel attempt — acceptance is irrevocable | FED-EXEC-005 |
| Obligation exists on Operator A regardless of Sim Op B subsequent state | FED-EXEC-006 |
| Obligation settlement_state=pending immediately after acceptance | FED-EXEC-006 |
| All 7 provisional completion criteria simultaneously satisfied | FED-EXEC-007 |
| `federation.payment.initiated` event emitted on Operator A with trace_id | FED-EXEC-007 |
| `federation.payment.completed` event emitted on Operator B with trace_id | FED-EXEC-007 |
| Both events share identical trace_id — cross-operator trace continuity | FED-EXEC-007 |
| Second Phase 4 execution with same routing_request_id does not double-debit | FED-EXEC-008 |
| Exactly 1 DEBIT ledger entry per routing_request_id | FED-EXEC-008 |
| Exactly 1 obligation per routing_request_id | FED-EXEC-008 |

**INV-FED-LEDGER-001** — cross-operator double-entry: **ENFORCEABLE** — FED-EXEC-001, 002  
**INV-FED-005** — value conservation: **ENFORCEABLE** — FED-EXEC-002  
**INV-FED-002** — one obligation per accepted routing: **ENFORCEABLE** — FED-EXEC-004, 006, 008  
**INV-FED-001** — trace_id across all artifacts: **ENFORCEABLE** — FED-EXEC-007  
**INV-FED-IDEM-001** — debit idempotency: **ENFORCEABLE** — FED-EXEC-008  
**BC-001** — no debit without acceptance: **ENFORCEABLE** — FED-EXEC-003  
**BC-003** — atomic debit + obligation: **ENFORCEABLE** — FED-EXEC-004  
**BC-004** — acceptance irrevocable: **ENFORCEABLE** — FED-EXEC-005  

---

## What Remains Unproven

| Not Yet Proven | Tested By | Notes |
|---|---|---|
| Obligation lifecycle (pending → in_netting → settled) | FED-OBL-001–007 | Requires netting cycle implementation |
| Federation events validate against federation-event.json schema | FED-EVT-001–006 | Requires federation-event.json contract |
| Cross-operator reconciliation by trace_id | FED-SETTLE-007 | Requires netting infrastructure |
| Net position computation (bilateral netting) | FED-SETTLE-002–003 | Requires settlement engine |
| Settlement execution: bank transfer ledger entries | FED-SETTLE-004 | Requires bank rail |
| Crash recovery: missing obligation recreated on restart | FED-FAIL-005 | Requires state injection endpoint |
| BRL extended outage: fail-closed after 12 hours | FED-FAIL-006 | Requires configurable BRL endpoint downtime |
| obligor_signature on obligation (non-repudiable) | FED-OBL-005 | Obligation signing not yet implemented |

---

## Next Tests

FED-EXEC is now **complete**. All execution semantics are proven before any obligation lifecycle or settlement work.

```
FED-CERT 001–011 ✓ ALL PASS
    │
FED-DISC 001–008 ✓ ALL PASS
    │
FED-TRUST 001–009 ✓ ALL PASS
    │
FED-ROUTE 001–012 ✓ ALL PASS
    │
FED-EXEC 001–008 ✓ ALL PASS  ← you are here
    │
FED-OBL 001–007  (obligation lifecycle: state machine, signature, uniqueness)
    │
FED-EVT + FED-SETTLE  (events, netting, settlement)
    │
L3 Blocking Suites: ALL PASS → L3 CERTIFICATION
```
