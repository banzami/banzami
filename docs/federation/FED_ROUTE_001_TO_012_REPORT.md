# FED-ROUTE-001 through FED-ROUTE-012 Report

**Document ID:** FED-ROUTE-001-TO-012-REPORT-001  
**Date:** 2026-05-31  
**Status:** ALL 40 PASS — routing wire protocol conformance layer complete  
**Authority:** FEDERATION_TEST_SUITE_SPEC.md, FEDERATION_CONTRACT_SURFACE.md, ADR-026

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
  ✓ FED-ROUTE-001 — Valid Routing Request Accepted
  ✓ FED-ROUTE-002 — routing_request_id Echoed Unchanged
  ✓ FED-ROUTE-003 — trace_id Propagated Unchanged (INV-FED-001)
  ✓ FED-ROUTE-004 — Idempotent Retry Returns Same Response (INV-FED-004)
  ✓ FED-ROUTE-005 — Request Without Valid Signature Rejected
  ✓ FED-ROUTE-006 — Wrong to_operator_id Rejected
  ✓ FED-ROUTE-007 — Recipient Not Found Returns Structured Rejection
  ✓ FED-ROUTE-008 — Unsupported Currency Returns Structured Rejection
  ✓ FED-ROUTE-009 — Accepted Response Contains Valid interop_transfer_id
  ✓ FED-ROUTE-010 — Non-Positive amount.minor Rejected (INV-FED-LEDGER-002)
  ✓ FED-ROUTE-011 — Duplicate routing_request_id with Different Content Returns duplicate_request
  ✓ FED-ROUTE-012 — Suspended Recipient Wallet Returns Structured Rejection
  → 12 passed, 0 failed, 0 skipped
```

---

## Commands

```bash
# Terminal 1 — start fixture server (Operator A)
python3 tools/banza-conformance/fixture_server.py --port 8099

# Terminal 2 — run full suite (FED-CERT + FED-DISC + FED-TRUST + FED-ROUTE)
python3 tools/banza-conformance/run.py --federation --url http://localhost:8099

# Run only FED-ROUTE
python3 tools/banza-conformance/run.py --federation --fed-suite route --url http://localhost:8099
```

---

## Routing Contract Created

### contracts/federation/federation-routing.json

Defines the wire format for `POST /federation/route` — the cross-operator payment
routing protocol. Contains:

**RoutingRequest** (sender → receiver):

| Field | Type | Notes |
|---|---|---|
| `schema_version` | string | Always `"1"` |
| `routing_request_id` | string | `rr-<uuid>` — idempotency key (INV-FED-004) |
| `trace_id` | string | Causal trace — propagated unchanged (INV-FED-001) |
| `from_operator_id` | string | Originating operator |
| `to_operator_id` | string | Must match receiving operator's operator_id |
| `amount.minor` | integer | Must be > 0 (INV-FED-LEDGER-002) |
| `amount.currency` | string | ISO 4217, must be in supported_currencies |
| `sender_wallet_id` | string | Payer wallet on originating operator |
| `recipient_identifier` | string | Payee identifier on receiving operator |
| `recipient_identifier_type` | enum | `wallet_id \| handle \| phone \| account_number` |
| `created_at` | ISO 8601 | When originating operator created the request |
| `certificate_url` | URI | Originating operator's certificate for bidirectional trust |

**RoutingResponse** (receiver → sender):

| Field | Presence | Notes |
|---|---|---|
| `schema_version` | always | `"1"` |
| `routing_request_id` | always | Echo of request — must be identical (INV-FED-004) |
| `status` | always | `accepted \| rejected \| pending` |
| `trace_id` | always | Echo of request trace_id — must be identical (INV-FED-001) |
| `interop_transfer_id` | if accepted | `itx-<uuid>` format |
| `accepted_at` | if accepted | ISO 8601 UTC timestamp |
| `rejection_code` | if rejected | From registry (8 structured codes) |
| `rejection_reason` | if rejected | Human-readable explanation |

**Rejection code registry:**

| Code | Trigger |
|---|---|
| `recipient_not_found` | No wallet matching recipient_identifier |
| `recipient_suspended` | Recipient wallet is suspended |
| `currency_not_supported` | Currency not in supported_currencies |
| `amount_below_minimum` | amount.minor ≤ 0 |
| `amount_above_maximum` | Amount exceeds operator limit |
| `operator_trust_failure` | Originating operator cert trust fails |
| `capability_unavailable` | Operator temporarily unavailable |
| `duplicate_request` | routing_request_id reused with different content (INV-FED-IDEM-001) |

---

## Signature Model

**Algorithm:** ed25519  
**HTTP Header:** `Banza-Federation-Signature: t=<unix_seconds>,v1=<ed25519_base64url>`  
**Signed payload:** `utf8(str(unix_seconds)) + "." + raw_request_body_bytes`

The receiving operator verifies by:
1. Parsing `t` and `v1` from the header
2. Reconstructing `str(t) + "." + body_bytes`
3. Verifying the ed25519 signature against the originating operator's public key

In the conformance setup, the runner pre-configures Sim Op B with Operator A's
public key (via `infra.configure_routing()`), eliminating the need for Sim Op B to
fetch and verify Operator A's certificate at routing time. This focuses the FED-ROUTE
suite on the routing wire protocol, not re-testing trust verification.

---

## Simulated Operator B Routing Endpoint

### runner_infra.py — SimB POST /federation/route

Sim Op B now handles `POST /federation/route` with this processing order:

1. **JSON parse** — reject with HTTP 400 on invalid JSON
2. **to_operator_id check** — reject with HTTP 400 if mismatch
3. **Signature verification** — reject with HTTP 401 if header missing or sig invalid
4. **amount.minor > 0** — reject with HTTP 400 if ≤ 0 (INV-FED-LEDGER-002)
5. **Idempotency check** — replay stored response if routing_request_id seen before (INV-FED-004); return `duplicate_request` if same ID but different body
6. **Currency validation** — return `currency_not_supported` if not in supported_currencies
7. **Recipient validation** — return `recipient_not_found` or `recipient_suspended`
8. **Accept** — credit payee wallet, assign `itx-<uuid>`, return status=accepted

### Pre-configured wallets

| Wallet ID | State | Purpose |
|---|---|---|
| `wallet-payee-test-001` | active | Happy-path recipient |
| `wallet-suspended-test-001` | suspended | FED-ROUTE-012 |
| all others | not found | FED-ROUTE-007 |

### Idempotency storage

The idempotency store maps `routing_request_id → {body_hash, response}`.
Body hash is computed as SHA-256 of the canonically serialized JSON (sort_keys=True).
This ensures:
- FED-ROUTE-004: same body on retry → same hash → replay stored response
- FED-ROUTE-011: different body (same ID) → different hash → `duplicate_request`

### New methods

| Method | Purpose |
|---|---|
| `configure_routing(op_a_operator_id, op_a_public_key)` | Configure Operator A's public key for sig verification |
| `reset_routing_state()` | Clear routing store and reset wallet balances (per-test isolation) |
| `get_wallet_balance(wallet_id)` | Query current wallet balance (for FED-ROUTE-004 assertion) |

---

## Tests Implemented

| Test | Scenario | Key Assertion | Severity | Invariant |
|---|---|---|---|---|
| FED-ROUTE-001 | Valid signed request | HTTP 200, status=accepted, all fields present | STANDARD | — |
| FED-ROUTE-002 | routing_request_id echo | response.routing_request_id == request.routing_request_id | STANDARD | INV-FED-004 |
| FED-ROUTE-003 | trace_id echo | response.trace_id == request.trace_id | CRITICAL | INV-FED-001 |
| FED-ROUTE-004 | Idempotent retry | Second response == first; payee credited once | CRITICAL | INV-FED-004 |
| FED-ROUTE-005 | Missing/invalid signature | HTTP 401 on both sub-cases | CRITICAL | — |
| FED-ROUTE-006 | Wrong to_operator_id | HTTP 400 | STANDARD | — |
| FED-ROUTE-007 | Unknown recipient | rejection_code=recipient_not_found | STANDARD | — |
| FED-ROUTE-008 | Unsupported currency (EUR) | rejection_code=currency_not_supported | STANDARD | — |
| FED-ROUTE-009 | interop_transfer_id format | Matches ^itx-[0-9a-f]{8}-...-[0-9a-f]{12}$ | STANDARD | — |
| FED-ROUTE-010 | Zero/negative amount | HTTP 400 on both sub-cases | CRITICAL | INV-FED-LEDGER-002 |
| FED-ROUTE-011 | Duplicate ID, different content | rejection_code=duplicate_request | CRITICAL | INV-FED-IDEM-001 |
| FED-ROUTE-012 | Suspended recipient wallet | rejection_code=recipient_suspended | STANDARD | — |

---

## Evidence Captured Per Test

### FED-ROUTE-001 (happy path)

| Item | Value |
|---|---|
| `routing_request_id` | `rr-00000000-0000-0000-0000-000000000001` |
| `trace_id` | `tr-00000000-0000-0000-0000-000000000001` |
| `response_status` | `accepted` |
| `interop_transfer_id` | `itx-<uuid4>` |
| `accepted_at` | (runner wall clock) |
| `schema_errors` | `[]` |

### FED-ROUTE-004 (idempotency)

| Item | Value |
|---|---|
| `routing_request_id` | `rr-00000000-0000-0000-0000-000000000001` |
| `balance_before` | 0 |
| `balance_after_first` | 50000 |
| `balance_after_second` | 50000 (unchanged) |
| `idempotency_replay_result` | `same_response` |
| `first_response.interop_transfer_id` == `second_response.interop_transfer_id` | true |

### FED-ROUTE-005 (signature rejection)

| Item | Value |
|---|---|
| `no_sig_status` | 401 |
| `no_sig_rejection_code` | `operator_trust_failure` |
| `wrong_sig_status` | 401 |
| `wrong_sig_rejection_code` | `operator_trust_failure` |
| `wrong_sig_used` | `A*86` placeholder (structurally valid, cryptographically invalid) |

### FED-ROUTE-011 (duplicate request)

| Item | Value |
|---|---|
| `routing_request_id` | `rr-00000000-0000-0000-0000-000000000001` |
| `first_amount_minor` | 50000 |
| `second_amount_minor` | 99999 |
| `first_response_status` | `accepted` |
| `second_response_status` | `rejected` |
| `rejection_code` | `duplicate_request` |

---

## Fixtures Added

| File | Purpose |
|---|---|
| `conformance/fixtures/federation/ROUTING-REQUEST-VALID.json` | Happy-path routing request |
| `conformance/fixtures/federation/ROUTING-REQUEST-DUPLICATE-DIFFERENT-CONTENT.json` | Same rr-001, amount=99999 |
| `conformance/fixtures/federation/ROUTING-REQUEST-UNKNOWN-RECIPIENT.json` | wallet-does-not-exist-xxxxxxxx |
| `conformance/fixtures/federation/ROUTING-REQUEST-WRONG-CURRENCY.json` | currency=EUR |
| `conformance/fixtures/federation/ROUTING-REQUEST-WRONG-DESTINATION.json` | to_operator_id=some-other-operator |
| `conformance/fixtures/federation/ROUTING-REQUEST-ZERO-AMOUNT.json` | amount.minor=0 |
| `conformance/fixtures/federation/ROUTING-REQUEST-SUSPENDED-RECIPIENT.json` | wallet-suspended-test-001 |
| `conformance/fixtures/federation/ROUTING-RESPONSE-ACCEPTED.json` | Reference accepted response |
| `conformance/fixtures/federation/ROUTING-RESPONSE-REJECTED.json` | Reference rejected response |

---

## Files Modified

| File | Change |
|---|---|
| `contracts/federation/federation-routing.json` | Created — RoutingRequest + RoutingResponse schemas + rejection code registry |
| `tools/banza-conformance/runner_infra.py` | Added `POST /federation/route` to Sim Op B; added `GET /wallets/{id}`; new methods `configure_routing`, `reset_routing_state`, `get_wallet_balance`; routing state in `_sim_b_state` |
| `tools/banza-conformance/run_fed.py` | Added `validate_routing_response`, `_make_sig_header`, `_post_route`, `_routing_body`; FED-ROUTE-001–012 functions; `run_suite_fed_route`; updated `run_federation_mode` with `run_route` flag, `configure_routing` call; version → 0.6.0-slice5; `--fed-suite route` option |

---

## What Is Now Proven

| Assertion | Proven By |
|---|---|
| Valid routing request accepted; all response fields present | FED-ROUTE-001 |
| routing_request_id echoed unchanged in response | FED-ROUTE-002 |
| trace_id propagated unchanged across routing boundary | FED-ROUTE-003 |
| Idempotent retry returns same response; payee credited once | FED-ROUTE-004 |
| Missing Banza-Federation-Signature → HTTP 401 | FED-ROUTE-005 |
| Invalid ed25519 signature → HTTP 401 | FED-ROUTE-005 |
| Wrong to_operator_id → HTTP 400 | FED-ROUTE-006 |
| Unknown recipient → rejection_code=recipient_not_found | FED-ROUTE-007 |
| Unsupported currency → rejection_code=currency_not_supported | FED-ROUTE-008 |
| interop_transfer_id format matches ^itx-<uuid>$ | FED-ROUTE-009 |
| Zero amount → HTTP 400 | FED-ROUTE-010 |
| Negative amount → HTTP 400 | FED-ROUTE-010 |
| Same routing_request_id, different content → rejection_code=duplicate_request | FED-ROUTE-011 |
| Suspended recipient → rejection_code=recipient_suspended | FED-ROUTE-012 |

**INV-FED-001** — trace_id propagated unchanged: **ENFORCEABLE** — FED-ROUTE-003  
**INV-FED-004** — routing idempotency: **ENFORCEABLE** — FED-ROUTE-002, 004, 011  
**INV-FED-LEDGER-002** — no zero/negative amounts: **ENFORCEABLE** — FED-ROUTE-010  
**INV-FED-IDEM-001** — duplicate content detection: **ENFORCEABLE** — FED-ROUTE-011  

---

## What Remains Unproven

| Not Yet Proven | Tested By | Notes |
|---|---|---|
| Transfer execution semantics (payee credited on acceptance) | FED-EXEC-001–008 | Requires Operator A ledger + obligation endpoints |
| Obligation lifecycle | FED-OBL-001–007 | Requires Operator A obligation engine |
| Federation events | FED-EVT-001–006 | Requires Operator A event stream |
| INV-TRUST-005 — BRL signature verifies | (not yet tested) | Current BRL uses placeholder signature |
| INV-TRUST-007 — key rotation auth | (not yet tested) | Requires operator-initiated key rotation |
| INV-FED-003 full — routing endpoint processes real requests | FED-ROUTE ✓ (SimB receiving); FED-EXEC (Operator A receiving) | Operator A receiving path not yet tested |

---

## Next Tests

FED-ROUTE is now **complete**. The full routing wire protocol is proven before any execution or obligation work.

```
FED-CERT 001–011 ✓ ALL PASS
    │
FED-DISC 001–008 ✓ ALL PASS
    │
FED-TRUST 001–009 ✓ ALL PASS
    │
FED-ROUTE 001–012 ✓ ALL PASS  ← you are here
    │
FED-EXEC 001–008  (transfer execution: payee credit, payer debit, debit/obligation atomicity)
    │
FED-OBL + FED-EVT  (obligation lifecycle, federation events)
    │
L3 Blocking Suites: ALL PASS → L3 CERTIFICATION
```
