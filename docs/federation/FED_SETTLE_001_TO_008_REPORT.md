# FED-SETTLE-001 through FED-SETTLE-008 Report

**Document ID:** FED-SETTLE-001-TO-008-REPORT-001  
**Date:** 2026-05-31  
**Status:** ALL 69 PASS — settlement and reconciliation conformance layer complete  
**Authority:** FEDERATION_TEST_SUITE_SPEC.md, FEDERATION_CONTRACT_SURFACE.md, FEDERATION_INVARIANTS.md, FEDERATION_PROTOCOL_FLOW.md, ADR-026

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
  ✓ FED-EXEC-001 through ✓ FED-EXEC-008
  → 8 passed, 0 failed, 0 skipped

[Suite] Obligation Lifecycle (blocking=True)
  ✓ FED-OBL-001 through ✓ FED-OBL-007
  → 7 passed, 0 failed, 0 skipped

[Suite] Federation Event Emission (blocking=True)
  ✓ FED-EVT-001 through ✓ FED-EVT-006
  → 6 passed, 0 failed, 0 skipped

[Suite] Netting and Settlement (blocking=True)
  ✓ FED-SETTLE-001 — Obligation Export Includes All Pending Obligations
  ✓ FED-SETTLE-002 — Net Position Computed Correctly
  ✓ FED-SETTLE-003 — Both Operators Independently Compute Same Net
  ✓ FED-SETTLE-004 — Settlement Execution: Ledger Entries Correct
  ✓ FED-SETTLE-005 — Obligations Marked Settled With Required Fields
  ✓ FED-SETTLE-006 — Reconciliation: All Accepted Routing Requests Have Obligations
  ✓ FED-SETTLE-007 — Reconciliation: Trace Cross-Check Across Both Operators
  ✓ FED-SETTLE-008 — Settlement Blocked on Unresolved Discrepancy
  → 8 passed, 0 failed, 0 skipped
```

---

## Commands

```bash
# Terminal 1 — start fixture server (Operator A)
python3 tools/banza-conformance/fixture_server.py --port 8099

# Terminal 2 — run full suite (FED-CERT through FED-SETTLE)
python3 tools/banza-conformance/run.py --federation --url http://localhost:8099

# Run only FED-SETTLE
python3 tools/banza-conformance/run.py --federation --fed-suite settle --url http://localhost:8099
```

---

## Netting Model

Settlement is driven by **bilateral netting**: Operator A and Operator B each accumulate
obligations in one direction and periodically net them to a single bank transfer.

```
gross_a_to_b = sum(all A→B obligations in period)
gross_b_to_a = sum(all B→A obligations in period)
net           = gross_a_to_b - gross_b_to_a

net > 0  → Operator A is net payer (owes B the net amount)
net < 0  → Operator B is net payer (owes A the absolute net amount)
net == 0 → no bank transfer; all obligations marked settled
```

Integer arithmetic throughout (INV-FED-LEDGER-002). No floating-point at any stage.

---

## Settlement Batch Model

Each netting cycle produces one `SettlementBatch`:

| Field | Type | Description |
|---|---|---|
| `settlement_batch_id` | `stl-<date>-<hex>` | Unique batch identifier |
| `operator_a_id` | string | Originating operator |
| `operator_b_id` | string | Destination operator |
| `currency` | ISO 4217 | Settlement currency |
| `period_start` / `period_end` | ISO date | Netting period |
| `included_obligations` | array | All obligation_ids in batch |
| `included_a_to_b_routing_ids` | array | routing_request_ids for A→B obligations |
| `gross_a_to_b` | integer | Sum of A→B amounts (minor units) |
| `gross_b_to_a` | integer | Sum of B→A amounts (minor units) |
| `net_amount` | integer | abs(gross_a_to_b − gross_b_to_a) |
| `net_payer_operator_id` | string | Who sends the bank transfer |
| `net_payee_operator_id` | string | Who receives the bank transfer |
| `reconciliation_status` | `clean` \| `discrepancy` | Reconciliation result |
| `settlement_status` | `authorized` \| `blocked` \| `settled` | Lifecycle state |
| `discrepancies` | array | Amount mismatches detected (if any) |
| `simulated_bank_reference` | string | Simulated bank transfer reference |
| `created_at` | ISO 8601 | Batch creation timestamp |
| `settled_at` | ISO 8601 | Settlement execution timestamp (if settled) |

---

## Reconciliation Gate

**Settlement MUST NOT execute unless `reconciliation_status == clean`.**

Reconciliation checks:

1. For every A→B obligation in the batch, Operator B independently confirms the amount.
2. If any `operator_a_amount != operator_b_reported_amount`, the batch is marked
   `reconciliation_status=discrepancy` and `settlement_status=blocked`.
3. A blocked batch cannot be executed — `POST /netting/execute` returns HTTP 409.
4. No obligation may advance to `settled` while the batch is blocked.

This enforces **BC-007** (settlement requires clean reconciliation) and **INV-FED-LEDGER-001**
(cross-operator ledger entries must sum to zero).

---

## Settlement Execution Model

On a clean batch, `POST /netting/execute` produces 4 settlement ledger entries:

| # | Operator | Entry Type | Account |
|---|---|---|---|
| 1 | Operator A | DEBIT | `federation_payable:operator-b-test` |
| 2 | Operator A | CREDIT | `federation_settlement_clearing` |
| 3 | Operator B | DEBIT | `federation_settlement_clearing` |
| 4 | Operator B | CREDIT | `federation_receivable:operator-a-test` |

All entries carry `amount_minor = net_amount`, `settlement_batch_id`, and `recorded_at`.

After execution:
- All A→B obligations in the batch advance to `settlement_state=settled`
- Each receives `settled_at` (ISO 8601) and `settlement_batch_id`
- A `simulated_bank_reference` is issued (no real bank rail)

---

## Mismatch Handling

FED-SETTLE-008 demonstrates the mismatch scenario:

| Actor | routing_request_id | Amount |
|---|---|---|
| Operator A (recorded) | `rr-...3001` | 50,000 AOA |
| Operator B (reported) | `rr-...3001` | 49,999 AOA |

The discrepancy of 1 AOA is detected during `netting/trigger`. The batch is created with:
- `reconciliation_status: "discrepancy"`
- `settlement_status: "blocked"`
- `discrepancies: [{routing_request_id, operator_a_amount, operator_b_reported_amount, discrepancy_amount}]`

Settlement execution returns HTTP 409. No obligation moves to `settled`. No bank transfer occurs.

---

## Tests Implemented

| Test | Scenario | Key Assertion | Severity | Invariant |
|---|---|---|---|---|
| FED-SETTLE-001 | 3 A→B obligations enter netting | All 3 in export; gross correct; states advance to in_netting | STANDARD | — |
| FED-SETTLE-002 | A→B=150K, B→A=40K → net=110K | net_amount == 110,000; integer type | STANDARD | INV-FED-LEDGER-001 |
| FED-SETTLE-003 | Both operators compute same net | Op A net == Op B net == 110K; settlement_status=authorized | STANDARD | INV-FED-LEDGER-001 |
| FED-SETTLE-004 | Settlement execution | 4 ledger entries; correct accounts + amounts | STANDARD | INV-FED-LEDGER-001 |
| FED-SETTLE-005 | Obligations marked settled | settlement_state=settled; settled_at + settlement_batch_id present | STANDARD | — |
| FED-SETTLE-006 | 5 routing requests → 5 obligations | 1:1 match; no orphan routing requests | CRITICAL | INV-FED-RECON-001 |
| FED-SETTLE-007 | trace_id in all 4 artifact types | 3 payments × 4 artifacts = 12 trace_id checks | STANDARD | INV-FED-RECON-001 |
| FED-SETTLE-008 | Amount mismatch blocks settlement | reconciliation_status=discrepancy; HTTP 409 on execute | CRITICAL | INV-FED-LEDGER-001 |

---

## Evidence Captured Per Test

### FED-SETTLE-001 (obligation export)

| Item | Value |
|---|---|
| `routing_request_ids` | `[rr-...3001, rr-...3002, rr-...3003]` |
| `included_a_to_b_routing_ids` | all 3 present |
| `gross_a_to_b` | 150,000 |
| `expected_gross` | 150,000 |
| `obligation_states` | all `in_netting` |
| `reconciliation_status` | `clean` |
| `settlement_batch_id` | `stl-<date>-<hex>` |

### FED-SETTLE-002 (net position)

| Item | Value |
|---|---|
| `a_to_b_obligations` | 3 |
| `b_to_a_obligations` | 1 |
| `gross_a_to_b` | 150,000 |
| `gross_b_to_a` | 40,000 |
| `net_amount` | 110,000 |
| `expected_net` | 110,000 |
| `net_payer_operator_id` | `operator-a-test` |
| `net_payee_operator_id` | `operator-b-test` |

### FED-SETTLE-003 (bilateral agreement)

| Item | Value |
|---|---|
| `operator_a_computed_net` | 110,000 |
| `operator_b_computed_net` | 110,000 |
| `nets_agree` | true |
| `settlement_status` | `authorized` |
| `reconciliation_status` | `clean` |

### FED-SETTLE-004 (settlement ledger)

| Item | Value |
|---|---|
| `net_amount` | 110,000 |
| `ledger_entry_count` | 4 |
| Op A DEBIT account | `federation_payable:operator-b-test` |
| Op A CREDIT account | `federation_settlement_clearing` |
| Op B DEBIT account | `federation_settlement_clearing` |
| Op B CREDIT account | `federation_receivable:operator-a-test` |
| `simulated_bank_reference` | `simulated-bank-ref-<hex>` |

### FED-SETTLE-005 (obligations settled)

| Item | Value |
|---|---|
| All obligations `settlement_state` | `settled` |
| All obligations have `settled_at` | true |
| All obligations have `settlement_batch_id` | true |
| All reference same `settlement_batch_id` | true |

### FED-SETTLE-006 (reconciliation)

| Item | Value |
|---|---|
| `accepted_routing_request_count` | 5 |
| `obligation_routing_request_ids` | 5 matching IDs |
| `missing_obligations_for` | `[]` |
| `extra_obligations_for` | `[]` |
| `reconciliation_clean` | true |

### FED-SETTLE-007 (trace cross-check)

| Trace | ledger_a | obligation_a | ledger_b | event_b |
|---|---|---|---|---|
| `tr-...3001` | ✓ | ✓ | ✓ | ✓ |
| `tr-...3002` | ✓ | ✓ | ✓ | ✓ |
| `tr-...3003` | ✓ | ✓ | ✓ | ✓ |

### FED-SETTLE-008 (discrepancy blocking)

| Item | Value |
|---|---|
| `discrepancy_routing_request_id` | `rr-...3001` |
| `operator_a_amount` | 50,000 |
| `operator_b_reported_amount` | 49,999 |
| `reconciliation_status` | `discrepancy` |
| `settlement_status` | `blocked` |
| `execute_http_status` | 409 |
| `obligation_states_after_blocked_batch` | all `pending` (not advanced) |

---

## Files Modified

| File | Change |
|---|---|
| `tools/banza-conformance/fixture_server.py` | Added `_initial_netting_state()`; added 8 netting endpoints (3 GET + 5 POST); added 9 handler methods including full bilateral netting engine, settlement execution, discrepancy injection |
| `tools/banza-conformance/run_fed.py` | Version → 1.0.0-slice9; added Slice 9 docstring; added `_SETTLE_*` constants; added 7 HTTP helper functions; added `_settle_route_three`; added FED-SETTLE-001–008; added `run_suite_fed_settle`; updated `run_federation_mode` with `run_settle` flag, settle suite invocation, summary; updated report slice; updated argparse |

---

## What Is Now Proven

| Assertion | Proven By |
|---|---|
| All pending A→B obligations are included in the netting export at cutoff | FED-SETTLE-001 |
| Obligations advance to `in_netting` when entering a clean batch | FED-SETTLE-001 |
| gross_a_to_b and gross_b_to_a are computed with integer arithmetic | FED-SETTLE-002 |
| net_amount = abs(gross_a_to_b − gross_b_to_a); type is integer | FED-SETTLE-002 |
| Operator A owes Operator B when gross_a_to_b > gross_b_to_a | FED-SETTLE-002 |
| Both operators independently compute identical net from same obligations | FED-SETTLE-003 |
| Settlement authorization requires bilateral net agreement | FED-SETTLE-003 |
| Settlement produces 4 ledger entries on both operators | FED-SETTLE-004 |
| DEBIT/CREDIT accounts are correct per the protocol ledger model | FED-SETTLE-004 |
| Settlement entries carry the net amount (not gross) | FED-SETTLE-004 |
| Settled obligations have `settlement_state=settled` | FED-SETTLE-005 |
| Settled obligations carry `settled_at` (ISO 8601) | FED-SETTLE-005 |
| Settled obligations carry `settlement_batch_id` | FED-SETTLE-005 |
| Every accepted routing request has exactly one obligation (INV-FED-RECON-001) | FED-SETTLE-006 |
| No accepted routing request exists without a corresponding obligation | FED-SETTLE-006 |
| trace_id appears in ledger entry on Op A for each payment | FED-SETTLE-007 |
| trace_id appears in obligation on Op A for each payment | FED-SETTLE-007 |
| trace_id appears in ledger entry on Op B for each payment | FED-SETTLE-007 |
| trace_id appears in event on Op B for each payment (INV-FED-RECON-001) | FED-SETTLE-007 |
| Amount mismatch between operators produces `reconciliation_status=discrepancy` | FED-SETTLE-008 |
| A discrepant batch has `settlement_status=blocked` | FED-SETTLE-008 |
| Settlement execution returns HTTP 409 on a blocked batch | FED-SETTLE-008 |
| No obligation advances to `settled` when the batch is blocked | FED-SETTLE-008 |
| No simulated bank transfer is initiated on a discrepant batch | FED-SETTLE-008 |

**INV-FED-LEDGER-001** — cross-operator ledger entries sum to zero: **ENFORCEABLE** — FED-SETTLE-004  
**INV-FED-RECON-001** — every payment traceable by trace_id across all 4 artifact types: **ENFORCEABLE** — FED-SETTLE-006, FED-SETTLE-007  
**BC-007** — settlement requires clean reconciliation: **ENFORCEABLE** — FED-SETTLE-008

---

## What Remains Unproven

| Not Yet Proven | Tested By | Notes |
|---|---|---|
| Zero-net case: no bank transfer, all obligations settled | FED-SETTLE-010 | Requires zero-net fixture |
| Netting disagreement: full obligation exchange identifies discrepancy | FED-SETTLE-009 | Requires missing-obligation fixture |
| `federation.settlement.completed` event emitted after settlement | FED-SETTLE-005+ | Requires settlement event emission |
| Crash recovery: missing obligation recreated on restart | FED-FAIL-005 | Requires state injection endpoint |
| Extended BRL outage: fail-closed after 12 hours | FED-FAIL-006 | Requires configurable BRL endpoint downtime |
| obligor_signature persists through netting and verified at settle time | FED-SETTLE-001+ | Requires netting-time signature verification |
| Operator B rejects invalid obligor_signature at netting | (future) | Requires netting protocol endpoint on Sim Op B |

---

## Next Tests

FED-SETTLE-001–008 is now **complete**. The full settlement lifecycle is observable and auditable.

```
FED-CERT 001–011 ✓ ALL PASS
    │
FED-DISC 001–008 ✓ ALL PASS
    │
FED-TRUST 001–009 ✓ ALL PASS
    │
FED-ROUTE 001–012 ✓ ALL PASS
    │
FED-EXEC 001–008 ✓ ALL PASS
    │
FED-OBL 001–007 ✓ ALL PASS
    │
FED-EVT 001–006 ✓ ALL PASS
    │
FED-SETTLE 001–008 ✓ ALL PASS  ← you are here
    │
FED-SETTLE 009–010 + FED-FAIL  (zero-net, disagreement, failure recovery)
    │
L3 Blocking Suites: ALL PASS → L3 CERTIFICATION
```
