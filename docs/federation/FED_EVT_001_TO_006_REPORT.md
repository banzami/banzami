# FED-EVT-001 through FED-EVT-006 Report

**Document ID:** FED-EVT-001-TO-006-REPORT-001  
**Date:** 2026-05-31  
**Status:** ALL 61 PASS — federation event conformance layer complete  
**Authority:** FEDERATION_TEST_SUITE_SPEC.md, FEDERATION_CONTRACT_SURFACE.md, FEDERATION_INVARIANTS.md, ADR-026

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
  ✓ FED-EVT-001 — federation.routing.accepted Emitted on Operator B
  ✓ FED-EVT-002 — federation.payment.initiated Emitted on Operator A
  ✓ FED-EVT-003 — federation.payment.completed Emitted on Operator B
  ✓ FED-EVT-004 — federation.obligation.recorded Emitted on Operator A
  ✓ FED-EVT-005 — All Federation Events for Same Payment Share trace_id (INV-FED-001)
  ✓ FED-EVT-006 — Federation Events Validate Against Schema
  → 6 passed, 0 failed, 0 skipped
```

---

## Commands

```bash
# Terminal 1 — start fixture server (Operator A)
python3 tools/banza-conformance/fixture_server.py --port 8099

# Terminal 2 — run full suite (FED-CERT through FED-EVT)
python3 tools/banza-conformance/run.py --federation --url http://localhost:8099

# Run only FED-EVT
python3 tools/banza-conformance/run.py --federation --fed-suite evt --url http://localhost:8099
```

---

## Federation Event Contract Created

### contracts/federation/federation-event.json

Defines the complete wire format for cross-operator federation events. Extends `contracts/events/envelope.schema.json` with federation-specific fields.

**Base envelope required fields (inherited):**

| Field | Type | Description |
|---|---|---|
| `id` | `evt-<uuid>` | Globally unique event identifier |
| `event_type` | enum (10 values) | Federation event type in `federation.*` namespace |
| `aggregate_type` | `"federation_payment"` | Aggregate type for all federation events |
| `aggregate_id` | string | Primary aggregate ID (typically routing_request_id) |
| `trace_id` | string | Causal trace identifier — INV-FED-001 |
| `correlation_id` | string | Current aggregate step within the trace |
| `payload` | object | Event-specific data |
| `created_at` | ISO 8601 UTC | Emission timestamp |

**Federation extension required fields:**

| Field | Type | Description |
|---|---|---|
| `federation_version` | `"1"` | Marks this as a federation event |
| `origin_operator_id` | string | Operator that emitted this event |
| `destination_operator_id` | string | Operator this event concerns |

**Conditional fields:**

| Field | Required when | Description |
|---|---|---|
| `routing_request_id` | `event_type ∈ routing.* ∪ payment.*` | Routing request this event relates to |
| `interop_transfer_id` | after routing acceptance | Interop transfer ID from Operator B |
| `obligation_id` | `event_type ∈ obligation.* ∪ settlement.*` | Obligation this event relates to |

---

## Event Type Registry

| Event Type | Emitted By | Trigger |
|---|---|---|
| `federation.routing.received` | Operator B | Routing request received |
| `federation.routing.accepted` | Operator B | Routing request accepted |
| `federation.routing.rejected` | Operator B | Routing request rejected |
| `federation.payment.initiated` | Operator A | Cross-operator routing sent |
| `federation.payment.completed` | Operator B | Payment credited on Operator B |
| `federation.payment.failed` | Operator A or B | Payment failed mid-flight |
| `federation.obligation.recorded` | Operator A | Obligation recorded after acceptance |
| `federation.obligation.settled` | Operator A | Obligation settled in a batch |
| `federation.settlement.initiated` | Operator A | Netting cycle started |
| `federation.settlement.completed` | Operator A | Net settlement executed |

---

## Event Emission Model

### Operator A (fixture_server.py)

Per accepted routing request, Operator A emits two events atomically with the debit + obligation in Phase 3:

**Event 1: `federation.payment.initiated`**
```json
{
    "id": "evt-<uuid>",
    "event_type": "federation.payment.initiated",
    "aggregate_type": "federation_payment",
    "aggregate_id": "<routing_request_id>",
    "trace_id": "<trace_id>",
    "correlation_id": "<routing_request_id>",
    "payload": {"amount_minor": N, "currency": "AOA"},
    "created_at": "<ISO 8601>",
    "federation_version": "1",
    "origin_operator_id": "<from_operator_id>",
    "destination_operator_id": "<to_operator_id>",
    "routing_request_id": "<routing_request_id>",
    "interop_transfer_id": "<itx_id>"
}
```

**Event 2: `federation.obligation.recorded`**
```json
{
    "id": "evt-<uuid>",
    "event_type": "federation.obligation.recorded",
    "aggregate_type": "federation_payment",
    "aggregate_id": "<routing_request_id>",
    "trace_id": "<trace_id>",
    "correlation_id": "<routing_request_id>",
    "payload": {},
    "created_at": "<ISO 8601>",
    "federation_version": "1",
    "origin_operator_id": "<from_operator_id>",
    "destination_operator_id": "<to_operator_id>",
    "routing_request_id": "<routing_request_id>",
    "interop_transfer_id": "<itx_id>",
    "obligation_id": "<ob_id>"
}
```

### Simulated Operator B (runner_infra.py)

Per accepted routing request, Operator B emits two events at acceptance time:

**Event 1: `federation.routing.accepted`**
```json
{
    "id": "evt-<uuid>",
    "event_type": "federation.routing.accepted",
    "aggregate_type": "federation_payment",
    "aggregate_id": "<routing_request_id>",
    "trace_id": "<trace_id>",
    "correlation_id": "<routing_request_id>",
    "payload": {},
    "created_at": "<ISO 8601>",
    "federation_version": "1",
    "origin_operator_id": "operator-b-test",
    "destination_operator_id": "<from_operator_id>",
    "routing_request_id": "<routing_request_id>",
    "interop_transfer_id": "<itx_id>"
}
```

**Event 2: `federation.payment.completed`**
```json
{
    "id": "evt-<uuid>",
    "event_type": "federation.payment.completed",
    "aggregate_type": "federation_payment",
    "aggregate_id": "<routing_request_id>",
    "trace_id": "<trace_id>",
    "correlation_id": "<routing_request_id>",
    "payload": {},
    "created_at": "<ISO 8601>",
    "federation_version": "1",
    "origin_operator_id": "operator-b-test",
    "destination_operator_id": "<from_operator_id>",
    "routing_request_id": "<routing_request_id>",
    "interop_transfer_id": "<itx_id>"
}
```

---

## Event Query Model

| Endpoint | Operator | Returns |
|---|---|---|
| `GET /conformance/federation/events` | Operator A (fixture_server) | All events emitted by Operator A |
| `GET /federation/events` | Simulated Operator B (runner_infra) | All events emitted by Operator B |

Both return `{"events": [...]}`. Both are queried via HTTP in the FED-EVT runner tests.

---

## Tests Implemented

| Test | Scenario | Key Assertion | Severity | Invariant |
|---|---|---|---|---|
| FED-EVT-001 | `federation.routing.accepted` on Op B | Event found; routing_request_id + trace_id present | STANDARD | — |
| FED-EVT-002 | `federation.payment.initiated` on Op A | Event found; trace_id + routing_request_id + interop_transfer_id present | STANDARD | — |
| FED-EVT-003 | `federation.payment.completed` on Op B | Event found; trace_id + interop_transfer_id present | STANDARD | — |
| FED-EVT-004 | `federation.obligation.recorded` on Op A | Event found; obligation_id present and matches recorded obligation | STANDARD | — |
| FED-EVT-005 | trace_id cross-check across both operators | ALL events for same payment share identical trace_id | CRITICAL | INV-FED-001 |
| FED-EVT-006 | Schema validation of all events | All events validate against `federation-event.json` | STANDARD | — |

---

## Evidence Captured Per Test

### FED-EVT-001 (routing.accepted on Operator B)

| Item | Value |
|---|---|
| `routing_request_id` | `rr-00000000-0000-0000-0000-000000000002` |
| `operator_b_events_count` | 2 |
| `routing_accepted_event_found` | true |
| `event.event_type` | `federation.routing.accepted` |
| `event.trace_id` | `tr-00000000-0000-0000-0000-000000000002` |

### FED-EVT-002 (payment.initiated on Operator A)

| Item | Value |
|---|---|
| `operator_a_events_count` | 2 |
| `payment_initiated_event_found` | true |
| `event.event_type` | `federation.payment.initiated` |
| `event.trace_id` | `tr-00000000-0000-0000-0000-000000000002` |
| `event.interop_transfer_id` | `itx-<uuid>` (present) |

### FED-EVT-003 (payment.completed on Operator B)

| Item | Value |
|---|---|
| `operator_b_events_count` | 2 |
| `payment_completed_event_found` | true |
| `event.event_type` | `federation.payment.completed` |
| `event.trace_id` | `tr-00000000-0000-0000-0000-000000000002` |

### FED-EVT-004 (obligation.recorded on Operator A)

| Item | Value |
|---|---|
| `recorded_obligation_id` | `ob-<uuid>` |
| `obligation_recorded_event_found` | true |
| `event.event_type` | `federation.obligation.recorded` |
| `event.obligation_id` | matches recorded obligation |
| `event.trace_id` | `tr-00000000-0000-0000-0000-000000000002` |

### FED-EVT-005 (trace_id cross-check)

| Item | Value |
|---|---|
| `operator_a_payment_events` | 2 |
| `operator_b_payment_events` | 2 |
| `all_trace_ids` | `[tr-..., tr-..., tr-..., tr-...]` (all identical) |
| `unique_trace_ids` | `["tr-00000000-0000-0000-0000-000000000002"]` |
| `all_match` | true |
| `trace_id_cross_check.all_match` | true |

### FED-EVT-006 (schema validation)

| Item | Value |
|---|---|
| `total_events` | 4 (2 Op A + 2 Op B) |
| `operator_a_events` | 2 |
| `operator_b_events` | 2 |
| `all_valid` | true |
| `schema_validation_results` | 4 entries, all `valid: true`, `errors: []` |

---

## Files Modified

| File | Change |
|---|---|
| `contracts/federation/federation-event.json` | Created — full federation event schema with base envelope fields + federation extension, conditional routing_request_id and obligation_id rules |
| `tools/banza-conformance/runner_infra.py` | Updated `federation.routing.accepted` and `federation.payment.completed` events on Sim Op B to full federation-event.json format (id, aggregate_type, federation_version, origin/destination operator_id, payload, created_at) |
| `tools/banza-conformance/fixture_server.py` | Updated `federation.payment.initiated` event to full format; added `federation.obligation.recorded` event (with obligation_id) emitted atomically with obligation creation |
| `tools/banza-conformance/run_fed.py` | Version → 0.9.0-slice8; added Slice 8 docstring; added `_find_event_schema_path`; added `_EVT_TYPE_ENUM`, `_EVT_ROUTING_TYPES`, `_EVT_OBLIGATION_TYPES`, `_EVT_ID_PATTERN`; added `validate_federation_event`; added `_EVT_RR_ID`, `_EVT_TRACE_ID` constants; added `_get_sim_b_events_http`; added FED-EVT-001 through FED-EVT-006; added `run_suite_fed_evt`; updated `run_federation_mode` with `run_evt` flag, evt suite invocation, updated summary; updated report slice; updated argparse |

---

## What Is Now Proven

| Assertion | Proven By |
|---|---|
| Operator B emits `federation.routing.accepted` event when routing is accepted | FED-EVT-001 |
| `federation.routing.accepted` event carries routing_request_id | FED-EVT-001 |
| `federation.routing.accepted` event carries correct trace_id | FED-EVT-001 |
| Operator A emits `federation.payment.initiated` event after committing debit + obligation | FED-EVT-002 |
| `federation.payment.initiated` event carries routing_request_id, trace_id, interop_transfer_id | FED-EVT-002 |
| Operator B emits `federation.payment.completed` event after crediting payee | FED-EVT-003 |
| `federation.payment.completed` event carries trace_id and interop_transfer_id | FED-EVT-003 |
| Operator A emits `federation.obligation.recorded` event after recording obligation | FED-EVT-004 |
| `federation.obligation.recorded` event carries obligation_id matching the recorded obligation | FED-EVT-004 |
| All 4 federation events for the same payment carry identical trace_id on both operators | FED-EVT-005 |
| INV-FED-001 enforced across the event stream: trace_id crosses operator boundaries unchanged | FED-EVT-005 |
| All 4 event types validate against federation-event.json schema (id, aggregate_type, federation_version, conditional fields) | FED-EVT-006 |

**INV-FED-001** — trace_id propagated into ALL federation events: **ENFORCEABLE** — FED-EVT-005  
**Federation observability**: cross-operator payment is fully observable and auditable via event streams — FED-EVT-001 through FED-EVT-006

---

## What Remains Unproven

| Not Yet Proven | Tested By | Notes |
|---|---|---|
| Cross-operator reconciliation by trace_id | FED-SETTLE-007 | Requires netting infrastructure |
| Net position computation (bilateral netting) | FED-SETTLE-002–003 | Requires settlement engine |
| Settlement execution: bank transfer ledger entries | FED-SETTLE-004 | Requires bank rail |
| Crash recovery: missing obligation recreated on restart | FED-FAIL-005 | Requires state injection endpoint |
| BRL extended outage: fail-closed after 12 hours | FED-FAIL-006 | Requires configurable BRL endpoint downtime |
| obligor_signature persists through netting and is verifiable at netting time | FED-SETTLE-001 | Requires netting export endpoint |
| `federation.obligation.settled` event emitted on settlement | FED-SETTLE | Requires settlement engine |

---

## Next Tests

FED-EVT is now **complete**. The federation flow is observable, auditable, and traceable across both operators.

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
FED-EVT 001–006 ✓ ALL PASS  ← you are here
    │
FED-SETTLE + FED-FAIL  (netting, settlement, failure recovery)
    │
L3 Blocking Suites: ALL PASS → L3 CERTIFICATION
```
