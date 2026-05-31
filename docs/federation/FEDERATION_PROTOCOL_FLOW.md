# BANZA Federation Protocol Flow

**Document ID:** FEDERATION-PROTOCOL-FLOW-DESIGN-001  
**Date:** 2026-05-31  
**Status:** Canonical — behavioral specification. No code. No implementation.  
**Authority:** ADR-026, FEDERATION_CONTRACT_SURFACE.md, FEDERATION_INVARIANTS.md  
**Precondition:** Both Operator A and Operator B hold valid BANZA certificates at `certification_level >= 3`

---

## Overview

This document defines the complete behavioral specification of a federated transaction — a payment that originates on Operator A (where the payer holds a wallet) and completes on Operator B (where the payee holds a wallet). It defines what happens, in what order, under what conditions, and with what guarantees.

**The commitment model in one sentence:** Operator B's acceptance of a routing request is simultaneously its commitment to credit the payee. Operator A's recording of an obligation is simultaneously its commitment to pay Operator B at the next netting cycle.

---

## Actors and Roles

| Actor | Role | Owns |
|-------|------|------|
| Consumer | Initiates the payment | Wallet on Operator A |
| Operator A | Originating operator | Payer's wallet; sends routing request; records obligation |
| Operator B | Destination operator | Payee's wallet; accepts routing request; credits payee |
| BANZA | Trust authority | Root signing key; Revocation List (BRL); BANZA public keys |
| BanzAI | Protocol evaluator | Conformance runner; reconciliation auditor; no authority over routing decisions |
| Merchant | Payment recipient | Wallet on Operator B |

**Critical distinctions:**
- BANZA does not participate in routing decisions in real time. It participates only via artifacts it has already issued (certificates, BRL).
- BanzAI does not route payments. It evaluates operator readiness and runs reconciliation.
- No operator governs another operator's routing decisions.

---

## Ledger Account Model

A cross-operator payment requires named accounts on both sides to make the double-entry work across the operator boundary.

### Operator A Accounts

| Account | Type | Meaning |
|---------|------|---------|
| `payer_wallet` | Liability | Consumer's wallet. Decremented when consumer pays. |
| `federation_payable:{operator_b_id}` | Liability | Accumulates what Operator A owes Operator B. Incremented per cross-operator obligation. Decremented at settlement. |
| `federation_settlement_clearing` | Asset | Bridge account used during the bank settlement transfer. |

### Operator B Accounts

| Account | Type | Meaning |
|---------|------|---------|
| `federation_receivable:{operator_a_id}` | Asset | Accumulates what Operator B is owed by Operator A. Incremented when a cross-operator payment is credited. Decremented at settlement. |
| `payee_wallet` | Liability | Merchant's wallet. Incremented when merchant receives payment. |
| `federation_settlement_clearing` | Liability | Bridge account used during the bank settlement transfer. |

### Cross-Operator Double-Entry (INV-FED-LEDGER-001)

For a payment of amount X from Consumer (on A) to Merchant (on B):

**On Operator A's ledger — at routing acceptance:**
```
DEBIT  payer_wallet                     X   (consumer's balance decreases)
CREDIT federation_payable:operator-b    X   (A's liability to B increases)
```

**On Operator B's ledger — at routing acceptance:**
```
DEBIT  federation_receivable:operator-a X   (B's receivable from A increases)
CREDIT payee_wallet                     X   (merchant's balance increases)
```

**At settlement (net = N from A to B, after bilateral netting):**

On Operator A's ledger:
```
DEBIT  federation_payable:operator-b    N   (liability to B decreases)
CREDIT federation_settlement_clearing   N   (bank transfer initiated)
```

On Operator B's ledger:
```
DEBIT  federation_settlement_clearing   N   (bank transfer received)
CREDIT federation_receivable:operator-a N   (receivable from A decreases)
```

The combined view: for every payment, six ledger entries exist (two on A at routing, two on B at routing, two on each side at settlement). The zero-sum invariant holds within each operator's ledger independently, and across both ledgers in aggregate.

---

## Phase 1 — Federation Discovery

### Preconditions
- A payment flow has been initiated on Operator A (consumer initiates payment to a recipient on Operator B)
- Operator A has determined the recipient is on Operator B (via recipient identifier resolution)

### Behavior

**Step 1.1 — Identify the destination operator**

Operator A resolves the `recipient_identifier` + `recipient_identifier_type` to an `operator_id`. Resolution logic:

- If `recipient_identifier_type = "wallet_id"`: the wallet ID encodes the `operator_id` prefix (e.g., `operator-b:wallet-uuid`)
- If `recipient_identifier_type = "handle"`: the `@banza:handle` namespace lookup resolves to an `operator_id`
- If `recipient_identifier_type = "phone"`: phone-to-operator directory lookup (operator-specific, not yet standardized)

The result of this step: Operator A knows `to_operator_id = "operator-b"` and has a manifest URL or `interop_endpoint` for Operator B.

**Step 1.2 — Fetch Operator B's manifest**

```
GET https://{operator_b_base}/.well-known/banza/operator.json
```

- TLS required. Operator A MUST reject manifest responses over plain HTTP.
- Validate response against `conformance/manifests/schema.json` AND `contracts/federation/federation-manifest.json`
- Check required federation extension fields:
  - `supports_federation == true` — abort if false (Operator B is not a federation member)
  - `cross_operator_routing == true` — abort if false
  - `certificate_url` is present and is a valid URI
  - `interop_endpoint` is present and is a valid URI
  - `federation_capabilities.supported_currencies` includes the payment currency — abort if not
  - `federation_capabilities.max_transaction_amount_minor` check if present

**Step 1.3 — Cache the manifest**

Manifests may be cached. Cache TTL:
- If manifest has `expires_at`: cache until `min(expires_at, now + 1h)`
- If no `expires_at`: cache for 1 hour maximum

**Cached manifest use:** Operator A MAY use a cached manifest for discovery (Step 1.2) but MUST re-fetch the certificate (Phase 2) at every routing decision. Manifest caching does not substitute for trust verification.

### Postconditions
- Operator A has a valid, unexpired manifest for Operator B
- Operator B is confirmed to support federation for the requested currency
- `certificate_url` and `interop_endpoint` are known

### Decision Points

| Outcome | Cause | Action |
|---------|-------|--------|
| Continue to Phase 2 | Manifest valid, federation supported, currency accepted | Proceed |
| Abort: not a federation member | `supports_federation == false` | Routing fails; notify consumer |
| Abort: currency not supported | Currency not in `supported_currencies` | Try alternate operator or fail |
| Abort: amount exceeds limit | `amount > max_transaction_amount_minor` | Try alternate operator or fail |
| Abort: manifest unreachable | HTTP error or TLS failure | Retry up to 3× with exponential backoff; then fail |

---

## Phase 2 — Trust Verification

### Preconditions
- Phase 1 complete: Operator A has a valid manifest with `certificate_url`
- Operator A has a copy of the BANZA root public key (distributed with BANZA SDK; pinned in conformance suite)
- Operator A has a current (< 6 hours old) BANZA Revocation List or can fetch one

### Behavior

This is the 9-step trust establishment protocol from ADR-026.

**Step 2.1 — Fetch the BRL**

If the cached BRL is older than 6 hours (INV-TRUST-006):
```
GET https://banza.network/federation/revocation-list.json
```
Verify BRL signature against BANZA public key (INV-TRUST-005). If verification fails: reject the stale BRL; treat as absent BRL (fail-closed for unknown operators).

**Step 2.2 — Fetch Operator B's certificate**

```
GET {manifest.certificate_url}
```
Default: `GET /.well-known/banza/certificate.json` at Operator B's base URL.

Validate schema against `contracts/federation/operator-certificate.json`.

**Step 2.3 — Verify certificate signature (INV-TRUST-001)**

```
canonical = sort_keys_lexicographic({all fields except "signature"})
verified  = ed25519_verify(BANZA_PUBLIC_KEY[certificate.issuer_key_id], canonical, base64url_decode(certificate.signature))
```
If `verified == false`: abort. Certificate was not issued by BANZA or has been tampered.

**Step 2.4 — Verify certificate expiry (INV-TRUST-002)**

```
if certificate.expires_at < now(): abort
if certificate.issued_at > now(): abort   // clock-skew guard: future-dated cert
```
No grace period. One second past `expires_at` is expired.

**Step 2.5 — Verify certification level**

```
if certificate.certification_level < 3: abort
```
Only L3+ operators may participate in federation routing.

**Step 2.6 — Check the BRL (INV-TRUST-003, INV-FED-007)**

```
if certificate.operator_id in BRL.revoked: abort
```
BRL check precedes capability check. A revoked operator with an otherwise valid certificate is still rejected.

**Step 2.7 — Verify `supports_federation` (INV-TRUST-004)**

```
if manifest.supports_federation != true: abort
if manifest.cross_operator_routing != true: abort
```

**Step 2.8 — Verify `capabilities` in certificate**

```
if "cross_operator_routing" not in certificate.capabilities: abort
```
The manifest declares capabilities; the certificate certifies them. Declaration without certification is insufficient.

**Step 2.9 — Bind certificate to manifest**

```
if certificate.operator_id != manifest.operator_id: abort
```
The certificate and manifest must describe the same operator. A mismatch indicates misconfiguration or a man-in-the-middle.

### Trust Result

If all 9 steps pass: **Operator B is trusted**. Trust result is cacheable for:
```
cache_until = min(certificate.expires_at, BRL.expires_at) - now()
```

If any step fails: **Operator B is not trusted**. The routing request MUST NOT be sent. The consumer is notified that the payment cannot be routed.

### Postconditions
- Operator A has verified Operator B's identity, certification, and current non-revocation
- Operator B's `public_key` from the certificate is held in memory for the duration of this routing attempt
- BRL is refreshed and valid

---

## Phase 3 — Routing Negotiation

### Preconditions
- Phase 2 complete: Operator B is trusted
- Operator A holds a valid certificate for the current flow (its own certificate, for Operator B to verify bidirectionally)
- The payment amount and currency have passed Operator B's declared limits

### Behavior on Operator A (Request Construction)

**Step 3.1 — Assign routing_request_id**

```
routing_request_id = "rr-" + new_uuid_v4()
```

This ID is the idempotency key (INV-FED-004). Operator A stores it immediately before sending, associated with the current payment attempt. If the request must be retried, the same `routing_request_id` is used.

**Step 3.2 — Propagate trace_id**

The `trace_id` for this federation transaction is the trace_id of the originating payment flow that triggered the routing decision. It was assigned when the consumer's payment intent was first recorded on Operator A. It must not be regenerated at any subsequent step (INV-FED-001).

**Step 3.3 — Construct RoutingRequest**

```json
{
  "schema_version": "1",
  "routing_request_id": "rr-<uuid>",
  "trace_id": "<propagated from originating payment>",
  "from_operator_id": "operator-a",
  "to_operator_id": "operator-b",
  "amount": { "minor": <integer>, "currency": "<ISO 4217>" },
  "sender_wallet_id": "<consumer's wallet id on Operator A>",
  "recipient_identifier": "<identifier for payee on Operator B>",
  "recipient_identifier_type": "<wallet_id|handle|phone|account_number>",
  "created_at": "<now() UTC ISO 8601>",
  "certificate_url": "<URL where Operator B can fetch Operator A's certificate>"
}
```

**Step 3.4 — Sign the request**

Operator A signs the request with its own private key:
```
timestamp      = now() as unix seconds
signed_payload = utf8(str(timestamp)) + "." + raw_request_body_bytes
signature      = base64url(ed25519_sign(OPERATOR_A_PRIVATE_KEY, signed_payload))
header         = "Banza-Federation-Signature: t=" + timestamp + ",v1=" + signature
```

**Step 3.5 — Send routing request**

```
POST {manifest.interop_endpoint}/federation/route
Content-Type: application/json
Banza-Federation-Signature: t=<timestamp>,v1=<signature>

<RoutingRequest JSON body>
```

Maximum wait for response: 30 seconds. If no response within 30 seconds: treat as network failure (see Phase 7, F-101).

---

### Behavior on Operator B (Request Processing)

**Step 3.6 — Receive and parse**

Operator B receives the POST. Parse the body against `contracts/federation/federation-routing.json` `RoutingRequest` schema. Reject with HTTP 400 if schema invalid.

**Step 3.7 — Verify to_operator_id**

```
if request.to_operator_id != this.operator_id: reject HTTP 400
```

**Step 3.8 — Verify request signature**

```
timestamp = parse(Banza-Federation-Signature header, field "t")
if abs(now() - timestamp) > 300 seconds: reject HTTP 400  // replay protection
```

Fetch Operator A's certificate:
```
GET {request.certificate_url}
```

Run trust verification (Steps 2.2 through 2.9) on Operator A's certificate. If any step fails:
```
return RoutingResponse { status: "rejected", rejection_code: "operator_trust_failure" }
```

If trust passes: extract `operator_a_public_key = certificate.public_key`.

Verify signature:
```
signed_payload = utf8(str(timestamp)) + "." + raw_request_body_bytes
verified = ed25519_verify(operator_a_public_key, signed_payload, base64url_decode(v1))
if verified == false: reject HTTP 401
```

**Step 3.9 — Resolve recipient**

Resolve `request.recipient_identifier` + `request.recipient_identifier_type` to an internal wallet ID on Operator B.

If not found:
```
return RoutingResponse { status: "rejected", rejection_code: "recipient_not_found" }
```

If found: check wallet status.
- If wallet is suspended: return `rejection_code: "recipient_suspended"`
- If wallet is active: continue

**Step 3.10 — Validate amount and currency**

```
if request.amount.currency not in this.supported_currencies:
  return RoutingResponse { status: "rejected", rejection_code: "currency_not_supported" }

if max_transaction_amount_minor defined and request.amount.minor > max:
  return RoutingResponse { status: "rejected", rejection_code: "amount_above_maximum" }

if request.amount.minor < minimum (if defined):
  return RoutingResponse { status: "rejected", rejection_code: "amount_below_minimum" }
```

**Step 3.11 — Check idempotency**

```
if routing_request_id already exists in Operator B's routing store:
  return the original response (idempotent replay, INV-FED-004)
  // do NOT process again regardless of outcome
```

If the `routing_request_id` exists but the request content differs: this is a protocol violation by Operator A. Return `rejection_code: "duplicate_request"`. Log and report to BANZA.

**Step 3.12 — Credit the payee and accept**

All validations passed. Operator B now atomically:
1. Creates the `interop_transfer_id = "itx-" + new_uuid_v4()`
2. Posts ledger entries (INV-FED-LEDGER-001):
   ```
   DEBIT  federation_receivable:operator-a    amount.minor
   CREDIT payee_wallet                        amount.minor
   ```
3. Records the routing request as `accepted` in the routing store
4. Emits `federation.routing.accepted` event with `trace_id`

If the ledger posting fails (e.g., database error): do not return `accepted`. Return HTTP 500. Operator A will retry (same `routing_request_id`). Operator B must roll back all partial state.

**Step 3.13 — Return RoutingResponse**

```json
{
  "schema_version": "1",
  "routing_request_id": "<echo>",
  "status": "accepted",
  "trace_id": "<echo — must be identical to request trace_id, INV-FED-001>",
  "interop_transfer_id": "itx-<uuid>",
  "accepted_at": "<now() UTC ISO 8601>"
}
```

HTTP 200.

### Postconditions (routing accepted)
- Operator B's payee wallet has been credited
- Operator B holds a permanent record of the accepted routing request
- `interop_transfer_id` is known to both operators
- `trace_id` has been verified to echo correctly (INV-FED-001)
- `federation.routing.accepted` event is on Operator B's event stream

### Decision Points

| Response | Cause | Operator A Action |
|----------|-------|-------------------|
| `status: "accepted"` | All validations passed, payee credited | Proceed to Phase 4 |
| `status: "rejected", rejection_code: "recipient_not_found"` | Payee not on Operator B | Fail routing; notify consumer |
| `status: "rejected", rejection_code: "currency_not_supported"` | Currency mismatch | Try alternate operator or fail |
| `status: "rejected", rejection_code: "operator_trust_failure"` | Operator A's cert failed verification | Check own certificate; alert operations |
| `status: "rejected"` (any code) | Any validation failure | Do NOT debit payer; do NOT record obligation |
| HTTP 500 or timeout | Operator B internal error or network failure | Retry with same `routing_request_id` (Phase 7, F-101) |

---

## Phase 4 — Transfer Execution

### Preconditions
- Phase 3 complete: Operator A has received `status: "accepted"` and holds `interop_transfer_id`
- Operator A has NOT yet debited the payer or recorded the obligation

### Behavior on Operator A

**Step 4.1 — Atomic debit and obligation recording (CRITICAL)**

The following three operations MUST occur in a single database transaction. If any one fails, all roll back:

1. Post ledger entries (INV-FED-LEDGER-001):
   ```
   DEBIT  payer_wallet                       amount.minor
   CREDIT federation_payable:operator-b      amount.minor
   ```
   The idempotency key for this posting: `routing_request_id` (prevents double-debit on retry).

2. Record the obligation (Phase 5 detail below).

3. Advance the payment state machine: `payment_state → "completed_cross_operator"`.

If this transaction commits: the payment is complete on Operator A. The consumer's balance has decreased. The obligation is recorded.

If this transaction fails: the payment state remains `"routing_accepted"`. Operator A MUST retry the atomic step (not re-send the routing request — the routing request has already been accepted). The retry only re-executes the local debit + obligation.

**Step 4.2 — Emit events**

After the transaction commits:
- Emit `federation.payment.initiated` on Operator A's event stream (with `trace_id`, `routing_request_id`, `interop_transfer_id`)
- Operator A may optionally push `federation.payment.initiated` to Operator B's `/federation/events` endpoint

**Step 4.3 — Notify consumer**

The consumer receives confirmation: the payment has been processed. The confirmation message includes the `trace_id` for reference.

### Behavior on Operator B (already complete from Phase 3)

Operator B has already credited the payee wallet at Step 3.12. No additional execution is required.

Operator B emits `federation.payment.completed` on its event stream (with `trace_id`, `interop_transfer_id`).

Operator B notifies the payee (push notification, webhook, etc.).

### Postconditions
- Operator A: payer wallet debited, `federation_payable:operator-b` credited, obligation recorded
- Operator B: `federation_receivable:operator-a` debited, payee wallet credited, events emitted
- Both: `trace_id` appears in all ledger entries, events, and obligation
- Consumer: notified of successful payment
- Merchant: notified of received payment

---

## Phase 5 — Obligation Creation

### Preconditions
- Phase 4 Step 4.1 is executing (obligation creation is part of the atomic transaction)

### Behavior

As part of the Step 4.1 atomic transaction, Operator A creates the obligation:

**Step 5.1 — Construct obligation**

```json
{
  "schema_version": "1",
  "obligation_id": "ob-<uuid>",
  "from_operator_id": "operator-a",
  "to_operator_id": "operator-b",
  "amount": { "minor": <same as routing_request.amount.minor>, "currency": "<same>" },
  "routing_request_id": "<same as routing_request.routing_request_id>",
  "interop_transfer_id": "<from RoutingResponse>",
  "trace_id": "<same trace_id — INV-FED-001>",
  "recorded_at": "<now() UTC ISO 8601>",
  "settlement_state": "pending"
}
```

**INV-FED-005 check (BEFORE signing):**
```
assert obligation.amount.minor == routing_request.amount.minor
assert obligation.amount.currency == routing_request.amount.currency
```
If this assertion fails: the obligation MUST NOT be recorded. This indicates a protocol error in Operator A's own code. Alert immediately.

**Step 5.2 — Sign obligation**

```
canonical = sort_keys_lexicographic({all fields except "obligor_signature"})
obligor_signature = base64url(ed25519_sign(OPERATOR_A_PRIVATE_KEY, canonical))
```

**Step 5.3 — Store obligation**

Store in Operator A's obligation store. Unique constraint on `routing_request_id` prevents duplicate obligations.

Emit `federation.obligation.recorded` event (with `obligation_id`, `trace_id`).

### Postconditions
- One obligation exists for each accepted routing request (INV-FED-002)
- Obligation amount = routing request amount (INV-FED-005)
- Obligation is signed by Operator A (non-repudiable)
- `settlement_state = "pending"`
- `trace_id` matches all other artifacts for this payment (INV-FED-001)

---

## Phase 6 — Netting and Settlement

### When Settlement Is Triggered

Settlement is triggered by the netting cycle. The netting interval is declared by each operator in `federation_capabilities.netting_interval_hours`. The interval is bilateral — both operators must agree on the netting cutoff time in advance (as part of federation onboarding, not as a runtime negotiation).

Default: 24-hour netting cycles with a daily cutoff at 00:00:00 UTC.

### Phase 6A — Obligation Export

**Step 6.1 — Operator A exports obligations for the netting period**

At netting cutoff, Operator A computes:
```
netting_period = current period identifier (e.g., "2026-06-01")
pending_obligations = all obligations where:
  - from_operator_id = "operator-a"
  - to_operator_id = "operator-b"
  - settlement_state = "pending"
  - recorded_at < netting_cutoff_time
```

Operator A advances the `settlement_state` of all included obligations to `"in_netting"` and sets `netting_period`.

Operator A transmits the obligation list (signed) to Operator B:
```
POST {interop_endpoint}/federation/obligations/netting
Content-Type: application/json
Banza-Federation-Signature: ...
Body: { netting_period, obligations: [...] }
```

**Step 6.2 — Operator B exports its obligations to Operator A**

Simultaneously, Operator B does the same for obligations flowing B → A (where Operator B has paid merchants on behalf of consumers on Operator A during the same netting period). This is the bilateral nature of the protocol — obligations flow in both directions.

### Phase 6B — Net Position Computation

**Step 6.3 — Each operator independently computes the gross and net position**

```
gross_A_to_B = sum(all A→B obligations.amount.minor in netting period)
gross_B_to_A = sum(all B→A obligations.amount.minor in netting period)
net           = gross_A_to_B - gross_B_to_A
```

If `net > 0`: Operator A is the net obligor (owes B the net amount).
If `net < 0`: Operator B is the net obligor (owes A the absolute net amount).
If `net == 0`: No bank transfer needed; all obligations marked settled.

**Step 6.4 — Net position agreement**

Both operators must arrive at the same `net` figure before any bank transfer is initiated. The agreement protocol:

1. Operator A sends its computed net position (signed) to Operator B
2. Operator B compares its own computed net against Operator A's
3. If they match: both sign the net position agreement (settlement authorization)
4. If they do not match: netting disagreement — see Phase 7, F-501

### Phase 6C — Settlement Execution

**Step 6.5 — Net obligor initiates bank transfer**

The net obligor (say Operator A) initiates a bank transfer via its `SettlementExecutionProvider`:
- Amount: `net` in the agreed currency
- Recipient: Operator B's designated settlement bank account
- Reference: `settlement_batch_id = "stl-" + netting_period + "-" + uuid`

On Operator A's ledger:
```
DEBIT  federation_payable:operator-b      net
CREDIT federation_settlement_clearing     net
```

On Operator A's ledger (when bank transfer confirms):
```
DEBIT  federation_settlement_clearing     net
CREDIT bank_settlement_account            net   (money leaves A's bank account)
```

**Step 6.6 — Net creditor receives bank transfer**

On Operator B's ledger (when bank transfer confirms):
```
DEBIT  bank_settlement_account            net   (money arrives in B's bank account)
CREDIT federation_settlement_clearing     net
```

Then:
```
DEBIT  federation_settlement_clearing     net
CREDIT federation_receivable:operator-a   net
```

**Step 6.7 — Mark obligations as settled**

Both operators update all obligations in the netting batch:
```
settlement_state  → "settled"
settled_at        → now()
settlement_batch_id → "stl-..."
```

Both emit `federation.settlement.completed` events with `settlement_batch_id`.

### Postconditions
- All pending A→B obligations in the netting period are settled
- All pending B→A obligations in the netting period are settled
- Net bank transfer has occurred (one bank transfer per netting period per counterparty pair)
- Both ledgers are balanced at the federation boundary
- `federation_payable:operator-b` and `federation_receivable:operator-a` are decremented by the net settled amount

---

## Phase 7 — Failure Recovery

This phase documents recovery procedures for each failure mode. See `FEDERATION_FAILURE_SCENARIOS.md` for complete failure taxonomy and recovery runbooks.

### F-101: Routing Request Timeout

**When:** Operator A sends `POST /federation/route`, receives no response within 30 seconds.

**Recovery:**
1. Wait: 2 seconds (first retry)
2. Retry: `POST /federation/route` with the **same** `routing_request_id`
3. If Operator B already processed: idempotent replay returns original response
4. If Operator B did not process: processes normally
5. Maximum 3 retries with exponential backoff (2s, 8s, 32s)
6. If all retries fail: payment fails; payer is NOT debited; no obligation is recorded

**Invariant:** INV-FED-004 guarantees the idempotent retry cannot double-charge.

### F-102: Response Received but Status Ambiguous

**When:** Operator A receives a response but cannot determine if it is `accepted` or `rejected` (e.g., HTTP 200 with malformed body).

**Recovery:**
1. Treat as failure (do not debit payer; do not record obligation)
2. Retry `POST /federation/route` with same `routing_request_id`
3. Operator B returns the idempotent response

### F-401: Operator B Accepts but Internal Ledger Fails

**When:** Operator B returned `status: "accepted"` but its internal ledger posting failed (e.g., database crash between accepting and committing).

**Recovery:**
- Operator B MUST resolve this internally. Having returned `accepted`, Operator B has committed. It must credit the payee from its own reserves and ensure the ledger posting completes.
- Operator A holds a signed routing request and valid `interop_transfer_id`. The obligation stands.
- If Operator B cannot self-recover: BANZA dispute resolution.

### F-402: Operator A Crashes After Acceptance, Before Obligation

**When:** Operator A received `status: "accepted"` but crashed before completing the atomic debit + obligation.

**Recovery:**
On restart, Operator A runs a reconciliation check:
1. Find all routing requests in state `"routing_accepted"` that have no corresponding obligation
2. For each: attempt to complete Phase 4 (atomic debit + obligation)
3. If ledger debit already exists (partial commit): complete obligation only
4. If neither debit nor obligation exists: re-execute Phase 4

This recovery procedure is idempotent because `routing_request_id` is the idempotency key for the ledger posting.

---

## Phase 8 — Revocation Handling

### When Operator B Is Revoked During an Active Flow

**Before routing request is sent (Phase 3, Step 3.5 not yet reached):**
- If BRL check in Phase 2, Step 2.6 catches the revocation: abort. Payment fails. Payer is not debited.

**After routing request is sent, before response:**
- If Operator B processes the request while being revoked mid-process: Operator B's behavior is undefined (it may or may not credit the payee)
- Operator A should receive an error response or timeout
- Operator A treats it as F-101 (timeout recovery); does NOT debit payer

**After routing accepted, before debit+obligation:**
- Operator A received `status: "accepted"` but BRL is refreshed before Step 4.1 and now shows Operator B as revoked
- Operator A MUST still complete the debit + obligation. The routing acceptance is irrevocable. Revocation of Operator B does not void the obligation.
- The obligation will be settled through BANZA dispute resolution.

**After obligation is recorded:**
- Existing obligations survive revocation. They must be settled.
- No new routing requests may be sent to a revoked operator.

### When Operator A Is Revoked

**Effect on Operator B receiving new routing requests from Operator A:**
- Operator B performs bidirectional trust verification (Step 3.8)
- BRL check on Operator A's certificate: revoked → return `rejection_code: "operator_trust_failure"`

**Effect on existing obligations:**
- Operator B still holds obligations that Operator A owes. These survive revocation.
- BANZA coordinates settlement of outstanding obligations before finalizing revocation.

### Suspension vs. Revocation (Behavioral Difference)

| Event | New routing requests | Existing obligations | Certificate | Path to restore |
|-------|---------------------|---------------------|-------------|-----------------|
| Suspension | Rejected (BRL) | Survive; must settle | Valid | BANZA removes from BRL; no re-certification |
| Revocation | Rejected (BRL + invalidated cert) | Survive; settled via BANZA | Invalidated | Full re-certification from L0 |

---

## Phase 9 — Reconciliation

Reconciliation is the process of verifying that Operator A and Operator B agree on the state of all cross-operator payments in a given netting period. It is triggered before each netting cycle and on demand by BanzAI.

### Step 9.1 — Obligation List Exchange

Both operators export their obligation lists for the netting period:
- Operator A exports: all obligations where `from_operator_id = "operator-a"` and `to_operator_id = "operator-b"` in the period
- Operator B exports: all obligations where `to_operator_id = "operator-b"` that it was notified of (via accepted routing requests in the period)

### Step 9.2 — Cross-Reference by routing_request_id

For each `routing_request_id` that Operator B accepted, there should be exactly one obligation on Operator A with matching `routing_request_id` and identical `amount`.

Discrepancy classes:

| Discrepancy | Meaning | Recovery |
|-------------|---------|---------|
| Obligation on A, no matching routing request on B | Obligation recorded for a request B never received | Verify routing request was actually sent; escalate |
| Routing request accepted by B, no obligation on A | Obligation not recorded — recovery procedure F-402 | A must record obligation immediately |
| Amount mismatch | INV-FED-005 violation | Critical — halt netting; escalate to BANZA |
| trace_id mismatch | INV-FED-001 violation | Critical — audit trail broken; escalate to BANZA |

### Step 9.3 — Ledger Cross-Check

For each cross-operator payment with `trace_id = T`:
- Operator A: verify `federation_payable:operator-b` has a CREDIT of `amount.minor` tagged with `trace_id = T`
- Operator B: verify `payee_wallet` has a CREDIT of `amount.minor` tagged with `trace_id = T`
- Verify `amount.minor` is identical on both sides (INV-FED-LEDGER-001)

### Step 9.4 — Reconciliation Report

BanzAI, when run with federation reconciliation mode, produces a report:
```
netting_period:   2026-06-01
operator_pair:    operator-a ↔ operator-b
total_A_to_B:     N obligations, gross M amount
total_B_to_A:     K obligations, gross P amount
net_position:     X (A→B) or Y (B→A)
discrepancies:    list of routing_request_ids with discrepancy type
status:           CLEAN | DISCREPANCIES_FOUND | ESCALATED
```

A `CLEAN` reconciliation report is a prerequisite for settlement execution.

---

## Phase 10 — Completion Criteria

A federated transaction is **provisionally complete** when:
1. Routing request is `status: accepted` on Operator B ✓
2. Payer's wallet is debited on Operator A ✓
3. Payee's wallet is credited on Operator B ✓
4. Obligation is recorded on Operator A with `settlement_state: "pending"` ✓
5. `federation.payment.initiated` emitted on Operator A ✓
6. `federation.payment.completed` emitted on Operator B ✓
7. Both events share the same `trace_id` (INV-FED-001) ✓

A federated transaction is **finally complete** when the obligation is settled:
8. Obligation `settlement_state → "settled"` ✓
9. `settlement_batch_id` assigned ✓
10. Bank transfer confirmed on both sides ✓
11. `federation.settlement.completed` emitted on both operators ✓

Between provisional and final completion, the obligation is an open financial commitment. Operator A owes Operator B. This is similar to the time between a card authorization and its settlement in traditional payment networks.

---

## Complete State Machine

### Payment State Machine (on Operator A)

```
[INITIATED]
    │
    │ Phase 1: manifest fetched, currency accepted
    ▼
[DISCOVERY_COMPLETE]
    │
    │ Phase 2: trust verification passed
    ▼
[TRUSTED]
    │
    │ Phase 3: routing_request_id assigned
    ▼
[ROUTING_PENDING]
    │
    ├──── rejected ──────────────────────────────────▶ [FAILED]
    │
    │ status: accepted, interop_transfer_id received
    ▼
[ROUTING_ACCEPTED]
    │
    │ Phase 4+5: debit + obligation (atomic)
    ▼
[PROVISIONALLY_COMPLETE]
    │
    │ Phase 6: obligation settled in netting cycle
    ▼
[FINALLY_COMPLETE]
```

### Obligation State Machine (on Operator A)

```
(created in Phase 5)
[PENDING]
    │
    │ netting cycle starts
    ▼
[IN_NETTING]
    │
    ├──── disagreement ─────▶ [DISPUTED] ─── BANZA resolves ──▶ [IN_NETTING]
    │
    │ bank transfer confirmed
    ▼
[SETTLED]
```

---

## Behavioral Constraints

These constraints apply to all implementations. They complement the invariants in `FEDERATION_INVARIANTS.md`.

**BC-001 — No debit without acceptance:**
Operator A MUST NOT debit a payer's wallet for a cross-operator payment unless it has received `status: "accepted"` from Operator B.

**BC-002 — No obligation without acceptance:**
Operator A MUST NOT record an obligation unless it has received `status: "accepted"` from Operator B.

**BC-003 — Atomic debit and obligation:**
The payer wallet debit and the obligation recording MUST be in the same database transaction. There is no valid state where one exists without the other.

**BC-004 — Acceptance is irrevocable on Operator B:**
Once Operator B has returned `status: "accepted"`, it has credited the payee and cannot un-accept. It MUST fulfill the obligation during the netting cycle regardless of subsequent events (including Operator A issues).

**BC-005 — Same routing_request_id on retry:**
When retrying a routing request after a network failure, Operator A MUST use the same `routing_request_id`. Generating a new `routing_request_id` on retry is a protocol violation that can result in double payment.

**BC-006 — Trust is re-verified per routing, not per session:**
Operator A MUST re-run Phase 2 trust verification for each new routing decision. Caching trust results is allowed only within the bounds of `min(certificate.expires_at, BRL.expires_at)`.

**BC-007 — Settlement requires clean reconciliation:**
Netting and settlement MUST NOT proceed if the reconciliation report (Phase 9) shows unresolved discrepancies of types `amount_mismatch` or `trace_id_mismatch`.

**BC-008 — Bidirectional trust:**
Before accepting a routing request, Operator B MUST verify Operator A's certificate (Steps 3.7–3.8). Trust is always bidirectional; no routing is accepted from an untrusted peer.

**BC-009 — Events carry trace_id:**
Every federation event emitted as a result of a cross-operator payment MUST carry the `trace_id` of that payment (INV-FED-001).

**BC-010 — Amount immutability:**
The `amount` field in the obligation MUST equal the `amount` field in the routing request. No fees, deductions, or adjustments may be applied inside the cross-operator amount. Fees are separate ledger entries, not reductions of the transferred amount.
