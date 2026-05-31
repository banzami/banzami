# BANZA Federation Invariant Registry

**Document ID:** FEDERATION-CONTRACTS-DESIGN-001  
**Date:** 2026-05-31  
**Status:** Canonical — authoritative source for all federation-layer invariants.  
**Authority:** ADR-026 (Federation Trust Model)  
**Extends:** BANZA core invariant registry (`INV-LEDGER-*`, `INV-WALLET-*`, `INV-SETTLE-*`, `INV-IDEM-*`, `INV-RECON-*`, `INV-QR-*`)

---

## Invariant Taxonomy

The BANZA federation invariant set is organized into three groups:

| Group | Prefix | Origin | Concern |
|-------|--------|--------|---------|
| Trust invariants | `INV-TRUST-*` | ADR-026 | Certificate validity, key management, revocation |
| Federation invariants | `INV-FED-*` | ADR-026 + this document | Cross-operator protocol correctness |
| Federation extensions of core invariants | `INV-FED-LEDGER-*` | This document | Core invariants extended to cross-operator scope |

**Invariant severity levels:**

- **CRITICAL** — Violation is a protocol error. Implementation MUST prevent it. Conformance FAIL.
- **HIGH** — Violation is a security or financial integrity risk. Implementation MUST prevent it. Conformance FAIL.
- **MEDIUM** — Violation degrades reliability or observability. Conformance WARNING or FAIL depending on context.

---

## Group 1: Trust Invariants (INV-TRUST-*)

Defined in ADR-026. Reproduced here with implementation notes and conformance vector mapping.

---

### INV-TRUST-001 — Certificate Signature Validity

**Severity:** CRITICAL  
**Definition:** A certificate is valid if and only if its `signature` field verifies against the BANZA root public key for the corresponding `issuer_key_id`.

**Formal statement:**
```
∀ certificate C:
  C is valid ⟺ ed25519_verify(BANZA_PUBLIC_KEY[C.issuer_key_id], canonical_json(C \ {signature}), base64url_decode(C.signature)) = true
```

**Violation consequence:** A certificate that fails signature verification MUST be treated as if it does not exist. All routing decisions that relied on an invalid certificate must be reversed if discovered post-facto.

**Implementation requirements:**
- Verification MUST use constant-time ed25519 implementation
- BANZA_PUBLIC_KEY must be loaded from a trusted source (BANZA SDK, pinned in conformance suite), never from the certificate itself
- Canonical JSON: all fields except `signature`, sorted lexicographically by key, no whitespace, UTF-8

**Enforced by:** `operator-certificate.json` (definition); `federation-routing.json` (enforcement at routing time); BanzAI trust verification module

**Conformance vectors:** FED-CERT-002, FED-CERT-008

---

### INV-TRUST-002 — Certificate Expiry Enforcement

**Severity:** CRITICAL  
**Definition:** A certificate MUST NOT be accepted after its `expires_at` timestamp. No grace period is permitted. Additionally, for `certification_level >= 3`, `expires_at - issued_at` MUST NOT exceed 90 days.

**Formal statement:**
```
∀ certificate C, time T:
  C is valid at T ⟺ C.issued_at ≤ T < C.expires_at

∀ certificate C where C.certification_level ≥ 3:
  (C.expires_at - C.issued_at) ≤ 90 days
```

**Violation consequence:** An expired certificate MUST be treated as untrusted. Cached certificates must be checked against the current time at every use, not only at fetch time.

**Implementation requirements:**
- Clock source for time comparison must be monotonic and not manipulable by the remote party
- Certificate expiry check happens at Step 5 of the trust establishment protocol
- Implementations MUST NOT add tolerance windows to expiry (unlike TLS which often adds small grace)

**Enforced by:** `operator-certificate.json` (schema constraint); `federation-routing.json` (Step 5 check); BanzAI trust module

**Conformance vectors:** FED-CERT-003, FED-CERT-008

---

### INV-TRUST-003 — Revoked Operator Rejection

**Severity:** CRITICAL  
**Definition:** An operator whose `operator_id` appears in a valid, non-expired BANZA Revocation List (BRL) MUST be rejected from all routing decisions, regardless of certificate validity.

**Formal statement:**
```
∀ routing decision R targeting operator B:
  if B.operator_id ∈ BRL.revoked → reject R
  (certificate validity is irrelevant if operator_id is in BRL)
```

**Violation consequence:** A revoked operator that succeeds in receiving a routing decision has bypassed protocol enforcement. Any financial obligation created post-revocation is disputed and unenforceable.

**Implementation requirements:**
- BRL check (Step 7) precedes capability verification (Step 8) but follows certificate signature verification (Step 4)
- If BRL cannot be fetched and cached BRL is older than 6 hours, reject all routing to unknown operators (fail-closed)
- BRL MUST itself be signature-verified (INV-TRUST-005) before being applied

**Enforced by:** BRL check logic; `federation-routing.json` (Step 7); BanzAI trust module

**Conformance vectors:** FED-CERT-009

---

### INV-TRUST-004 — Federation Flag Requires Certification

**Severity:** HIGH  
**Definition:** An operator MUST NOT declare `supports_federation: true` in its manifest unless it holds a valid, non-expired, non-revoked BANZA certificate at `certification_level >= 3`.

**Formal statement:**
```
∀ operator O:
  O.manifest.supports_federation = true
  ⟹
  ∃ valid certificate C such that:
    C.operator_id = O.operator_id
    ∧ C.certification_level ≥ 3
    ∧ C.expires_at > now()
    ∧ C.operator_id ∉ BRL.revoked
```

**Violation consequence:** An operator that declares federation capability without certification is making a false protocol claim. Peers that relied on this claim may route payments to an uncertified operator. This is a protocol violation by the declaring operator.

**Implementation requirements:**
- BanzAI must flag this condition during manifest evaluation
- Conformance runner must test: if `supports_federation=true`, is there a valid certificate?
- Self-reporting is not enough — peers must independently verify via trust protocol

**Enforced by:** `federation-manifest.json` (declarative constraint); conformance vector FED-MAN-007; BanzAI manifest evaluation

**Conformance vectors:** FED-MAN-002, FED-MAN-007

---

### INV-TRUST-005 — BRL Must Be Signed

**Severity:** HIGH  
**Definition:** A BANZA Revocation List MUST be signed by BANZA using the root signing key. An unsigned or unverifiable BRL MUST be rejected as if it were expired.

**Formal statement:**
```
∀ BRL B:
  B is valid ⟺ ed25519_verify(BANZA_PUBLIC_KEY[B.issuer_key_id], canonical_json(B \ {signature}), B.signature) = true
```

**Violation consequence:** An attacker that can serve an unsigned BRL could clear the revocation list, allowing revoked operators to participate in federation. A BRL that fails verification must be treated as absent (no BRL), not as an empty revocation list.

**Implementation requirements:**
- BRL verification uses the same key distribution mechanism as certificate verification
- Failed BRL fetch or failed BRL signature → use cached BRL if within 6 hours; reject all routing if cache expired
- "No BRL" is not the same as "empty BRL" — absent BRL is fail-closed for new operators

**Enforced by:** BRL fetch logic; BanzAI trust module

**Conformance vectors:** (BRL signing conformance vector — TBD in BRL contract)

---

### INV-TRUST-006 — Maximum BRL Staleness

**Severity:** HIGH  
**Definition:** A routing decision MUST NOT be made against a BRL older than 6 hours.

**Formal statement:**
```
∀ routing decision R at time T:
  T - BRL.fetched_at ≤ 6 hours
```

**Violation consequence:** A stale BRL may fail to reflect recent revocations. A routing decision made with a stale BRL may deliver money to a revoked operator.

**Implementation requirements:**
- BRL cache must store `fetched_at` timestamp alongside the BRL content
- At each routing decision, compute staleness before applying BRL
- If stale: attempt BRL refresh; if refresh fails and staleness > 6h, reject routing or fall back to degraded mode as defined by operator policy
- Emergency BRL (with `expires_at` set to 1 hour) triggers accelerated refresh

**Enforced by:** BRL cache logic; routing engine pre-checks

**Conformance vectors:** (staleness conformance vector — TBD)

---

### INV-TRUST-007 — Key Rotation Authentication

**Severity:** HIGH  
**Definition:** A key rotation MUST be authenticated by signing the rotation request with the currently-bound private key. Key rotation authenticated by any other means is invalid.

**Formal statement:**
```
∀ key rotation request R for operator O:
  R is valid ⟺
    R is signed with private_key(O.current_certificate.public_key)
```

**Violation consequence:** An attacker that can submit an unauthenticated key rotation request could replace a legitimate operator's public key with its own, allowing it to impersonate the operator.

**Implementation requirements:**
- BANZA's certificate issuance process must verify the rotation request signature before issuing a new certificate
- The rotation request is an out-of-band process (not defined in these contracts); this invariant governs its security requirement
- BanzAI does not participate in key rotation; this is a BANZA-to-operator bilateral process

**Enforced by:** BANZA certificate issuance process (out-of-band)

**Conformance vectors:** (key rotation conformance — TBD in certificate management spec)

---

## Group 2: Federation Protocol Invariants (INV-FED-*)

Defined in ADR-026 and extended by this document.

---

### INV-FED-001 — Trace Identity Across Operator Boundaries

**Severity:** CRITICAL  
**Definition:** A federation transaction MUST carry the same `trace_id` in every artifact it produces on both the originating and receiving operator.

**Formal statement:**
```
∀ cross-operator payment P:
  ∀ artifacts A produced by P (routing_request, routing_response, obligation, events on A and B):
    A.trace_id = P.trace_id
```

**Violation consequence:** A federation payment with mismatched trace_ids cannot be audited or reconciled across operator boundaries. The obligation created by Operator A cannot be matched to the transfer created by Operator B. This breaks INV-RECON-* across the federation.

**Implementation requirements:**
- `trace_id` MUST be copied from the originating transaction (not regenerated) at every federation step
- Operator B MUST echo the `trace_id` from the RoutingRequest in the RoutingResponse
- All federation events emitted for a payment MUST use the same `trace_id`
- The obligation's `trace_id` MUST equal the routing request's `trace_id`

**Enforced by:** `federation-routing.json` (echo in response), `federation-obligation.json` (trace field), `federation-event.json` (trace field)

**Conformance vectors:** FED-ROUTE-003, FED-OBL-003, FED-EVT-002

---

### INV-FED-002 — Obligation Per Accepted Routing Request

**Severity:** CRITICAL  
**Definition:** Every accepted cross-operator routing request MUST produce exactly one `InteropObligation` in the originating operator. No accepted routing request may exist without a corresponding obligation. No obligation may exist without a corresponding accepted routing request.

**Formal statement:**
```
∀ routing_request R where R.status = "accepted":
  ∃! obligation O such that O.routing_request_id = R.routing_request_id

∀ obligation O:
  ∃ routing_request R such that R.routing_request_id = O.routing_request_id ∧ R.status = "accepted"
```

**Violation consequence:** A missing obligation means money has moved (Operator B has processed a payment) but Operator A has no record of what it owes. This is an undischarged financial liability — equivalent to an unbalanced ledger entry.

**Implementation requirements:**
- Obligation recording MUST be atomic with the routing request state transition to `accepted`
- If obligation recording fails, the routing request state MUST roll back to `pending` or the routing MUST be rejected
- The unique constraint on `routing_request_id` in the obligations store prevents duplicate obligations

**Enforced by:** `federation-obligation.json` (UNIQUE on routing_request_id); implementation must use atomic transaction

**Conformance vectors:** FED-OBL-001, FED-OBL-004

---

### INV-FED-003 — Federation Capability Declaration Integrity

**Severity:** HIGH  
**Definition:** A federation member MUST NOT declare `supports_federation: true` unless it can actually service federation routing requests at the declared `interop_endpoint`.

**Formal statement:**
```
∀ operator O where O.manifest.supports_federation = true:
  POST O.interop_endpoint + "/federation/route" with valid RoutingRequest
  ⟹ HTTP 200 | 202 (not 404, not 500, not connection refused)
```

**Violation consequence:** An operator that declares federation capability but cannot service routing requests will cause routing failures that are invisible until routing is attempted. This breaks the routing guarantee and wastes federation resources.

**Implementation requirements:**
- Before setting `supports_federation=true`, the operator MUST have a running, conformance-passing federation API
- BanzAI conformance runner tests the endpoint reachability as FED-MAN-005

**Enforced by:** `federation-manifest.json` (declarative; verified by conformance); FED-MAN-005 conformance vector

**Conformance vectors:** FED-MAN-003, FED-MAN-005

---

### INV-FED-004 — Cross-Operator Routing Idempotency

**Severity:** CRITICAL  
**Definition:** Cross-operator routing MUST be idempotent. The same `routing_request_id` MUST produce the same result regardless of how many times it is submitted.

**Formal statement:**
```
∀ routing_request R₁, R₂ where R₁.routing_request_id = R₂.routing_request_id:
  response(R₁) = response(R₂)

∀ routing_request R where n submissions with same routing_request_id:
  exactly 1 interop_transfer_id created on Operator B
  exactly 1 obligation created on Operator A
```

**Violation consequence:** Without idempotency, network retries (which are mandatory for reliability) could duplicate a payment. A consumer could be charged twice; a merchant could receive double credit.

**Implementation requirements:**
- `routing_request_id` MUST have a UNIQUE database constraint in Operator B's routing store
- On receiving a duplicate `routing_request_id` with identical content: return the original response
- On receiving a duplicate `routing_request_id` with different content: return `rejection_code = "duplicate_request"` (invariant violation by Operator A — report to BANZA)
- Obligation store MUST also have UNIQUE constraint on `routing_request_id` (Operator A side)

**Extends:** INV-IDEM-001 (single-operator idempotency) to cross-operator scope

**Enforced by:** `federation-routing.json` (`routing_request_id` field); `federation-obligation.json` (UNIQUE constraint); FED-ROUTE-004

**Conformance vectors:** FED-ROUTE-004

---

### INV-FED-005 — Value Conservation Across Operator Boundaries

**Severity:** CRITICAL  
**Definition:** No money may be created or destroyed in a federation transaction. The total value deducted from the payer's wallet on Operator A must equal the total value credited to the payee's wallet on Operator B.

**Formal statement:**
```
∀ cross-operator payment P:
  debit(Operator_A_ledger, P) = credit(Operator_B_ledger, P)
  = obligation(P).amount.minor
  = routing_request(P).amount.minor
```

**Violation consequence:** Value creation is financial fraud. Value destruction is financial loss with no legal basis. Both are catastrophic violations of the protocol's integrity guarantees.

**Implementation requirements:**
- Obligation `amount.minor` MUST be validated to equal routing request `amount.minor` before recording
- Operator B's ledger CREDIT must equal the routing request `amount.minor` (no fees taken from the transfer amount — fees are a separate ledger entry if applicable)
- Conformance test FED-OBL-002 verifies the obligation amount; the end-to-end vector FED-ROUTE-001 verifies both ledgers

**Extends:** INV-LEDGER-001 (zero-sum double-entry) to cross-operator scope

**Enforced by:** `federation-obligation.json` (amount equals routing request amount); `federation-routing.json` (amount field definition); conformance vector FED-OBL-002

**Conformance vectors:** FED-OBL-002, FED-ROUTE-001 (end-to-end)

---

### INV-FED-006 — Certificate Expiry Is Mandatory

**Severity:** HIGH  
**Definition:** An operator certificate MUST expire. Perpetual certification is forbidden. Certificates without `expires_at` are structurally invalid.

**Formal statement:**
```
∀ certificate C:
  C.expires_at is defined
  ∧ C.expires_at > C.issued_at
  ∧ C.certification_level ≥ 3 ⟹ (C.expires_at - C.issued_at) ≤ 90 days
```

**Violation consequence:** A certificate without expiry cannot be revoked by inaction. It must be explicitly revoked, which requires BANZA action for every operator exit. Short-lived certificates make inaction (not renewing) the natural revocation path.

**Implementation requirements:**
- JSON Schema for operator-certificate enforces `expires_at` as required
- Certificate issuance process at BANZA must enforce the 90-day maximum for L3+
- Conformance runner checks `expires_at` presence and validity (FED-CERT-003)

**Enforced by:** `operator-certificate.json` (required field, schema constraint)

**Conformance vectors:** FED-CERT-003

---

### INV-FED-007 — Revoked Operator Excluded from All Routing

**Severity:** CRITICAL  
**Definition:** A revoked operator MUST be rejected from all routing decisions immediately upon BRL propagation (within 6 hours).

**Formal statement:**
```
∀ operator O where O.operator_id ∈ BRL.revoked:
  ∀ routing decision R targeting O: reject(R)
  propagation_delay ≤ 6 hours (from BRL publication to all peers applying rejection)
```

**Violation consequence:** A revoked operator that continues to receive routed payments may be operating fraudulently. Any obligation created after revocation is disputed and BANZA will not honor it in dispute resolution.

**Implementation requirements:**
- BRL refresh frequency must be at most 6 hours (INV-TRUST-006 defines this as a complementary invariant)
- Emergency BRL issuance reduces propagation to ≤ 1 hour
- Routing engine must check BRL at Step 7 before every routing decision (not only at startup)

**Enforced by:** BRL check logic; `federation-routing.json` (Step 7 mandatory)

**Conformance vectors:** FED-CERT-009

---

## Group 3: Federation Extensions of Core Invariants (INV-FED-LEDGER-*)

These invariants extend existing BANZA core invariants to cover cross-operator scope. They do not replace the core invariants — they extend them.

---

### INV-FED-LEDGER-001 — Cross-Operator Double-Entry

**Severity:** CRITICAL  
**Extends:** INV-LEDGER-001 (zero-sum ledger)  
**Definition:** For every cross-operator payment, the combined ledger entries across both operators must sum to zero. The DEBIT on Operator A's settlement account and the CREDIT on Operator B's settlement account are the cross-operator counterparts.

**Formal statement:**
```
∀ cross-operator payment P:
  Operator_A_ledger.DEBIT(P) + Operator_B_ledger.CREDIT(P) = 0
  (in a unified accounting view of the federation)
```

**Violation consequence:** If DEBIT and CREDIT don't match across operators, money has been created or destroyed. This is equivalent to a single-operator posting that doesn't balance — a CRITICAL violation.

**Implementation requirements:**
- The obligation amount (what A owes B) is the accounting bridge between the two ledgers
- Settlement closes this open obligation: DEBIT on A's settlement account, CREDIT on B's settlement account
- Netting computation must be independently verifiable by both operators before settlement is executed

**Conformance vectors:** FED-OBL-002, end-to-end conformance (FED-ROUTE-001 extended)

---

### INV-FED-LEDGER-002 — Cross-Operator Integer Arithmetic

**Severity:** CRITICAL  
**Extends:** INV-LEDGER-003 (no floating point)  
**Definition:** All monetary values in federation artifacts MUST use integer minor units. No floating point representation at any stage of cross-operator communication.

**Formal statement:**
```
∀ federation artifact A with amount field:
  A.amount.minor ∈ ℤ (integer)
  floating_point(A.amount.minor) is forbidden
```

**Violation consequence:** Floating point representation of currency amounts introduces rounding errors. In cross-operator settlement, rounding errors accumulate and create irreconcilable net positions.

**Implementation requirements:**
- All schemas define `amount.minor` as `"type": "integer"` (never `"type": "number"`)
- Rust implementations use `i64` or `u64` for all amount fields
- No SDK or implementation may convert amount to float at any point in the federation pipeline

**Enforced by:** `federation-routing.json` (schema), `federation-obligation.json` (schema)

**Conformance vectors:** FED-ROUTE-010 (negative test: non-integer amount rejected)

---

### INV-FED-IDEM-001 — Federation Idempotency Scope

**Severity:** CRITICAL  
**Extends:** INV-IDEM-001 (single-operator idempotency key scope)  
**Definition:** Federation idempotency keys (`routing_request_id`) are globally unique across all operators and all time. No two routing requests from any operator may share a `routing_request_id`.

**Formal statement:**
```
∀ routing_request R₁ from Operator_X, R₂ from Operator_Y:
  R₁ ≠ R₂ ⟹ R₁.routing_request_id ≠ R₂.routing_request_id
```

**Violation consequence:** ID collision between operators would allow a routing request from Operator X to be confused with a routing request from Operator Y, enabling idempotency bypass attacks.

**Implementation requirements:**
- `routing_request_id` format: `rr-<uuid>` where uuid is UUIDv4 (128 bits of randomness)
- The probability of collision with UUIDv4 is negligible (1 in 5.3 × 10³⁶ per pair)
- The database constraint on `routing_request_id` at Operator B includes the `from_operator_id` to prevent cross-operator key collision attacks

**Enforced by:** `federation-routing.json` (UUID format), database constraint at Operator B

**Conformance vectors:** FED-ROUTE-004

---

### INV-FED-RECON-001 — Cross-Operator Reconcilability

**Severity:** HIGH  
**Extends:** INV-RECON-* (internal reconciliation)  
**Definition:** Every cross-operator payment must be traceable from Operator A's ledger entry through the obligation to Operator B's ledger entry via the shared `trace_id`. Cross-operator payments must be independently auditable without cooperation from either operator.

**Formal statement:**
```
∀ cross-operator payment P:
  ∃ ledger_entry_A where ledger_entry_A.trace_id = P.trace_id (on Operator A)
  ∃ routing_request where routing_request.trace_id = P.trace_id
  ∃ obligation where obligation.trace_id = P.trace_id
  ∃ ledger_entry_B where ledger_entry_B.trace_id = P.trace_id (on Operator B)
  
  These four artifacts form a verifiable audit chain.
```

**Violation consequence:** A payment that cannot be traced across operators is unauditable. In regulatory contexts (AML, financial reporting), unauditable cross-operator payments are a compliance failure.

**Implementation requirements:**
- `trace_id` must be present in all four artifact types (INV-FED-001 enforces propagation)
- Operators must expose `trace_id` in their obligation and event query APIs
- BanzAI's audit capability can reconstruct the cross-operator payment chain from `trace_id` alone

**Enforced by:** INV-FED-001 (trace propagation); all federation contracts (trace_id field)

**Conformance vectors:** FED-EVT-002, FED-OBL-003

---

## Invariant Quick Reference

| ID | Group | Severity | One-Line Definition |
|----|-------|----------|---------------------|
| INV-TRUST-001 | Trust | CRITICAL | Certificate is valid only if its signature verifies against BANZA root key |
| INV-TRUST-002 | Trust | CRITICAL | Certificate expires at `expires_at`; no grace period; max 90d for L3+ |
| INV-TRUST-003 | Trust | CRITICAL | BRL entry → reject from all routing regardless of certificate |
| INV-TRUST-004 | Trust | HIGH | `supports_federation=true` requires valid L3+ certificate |
| INV-TRUST-005 | Trust | HIGH | BRL must be signed by BANZA; unsigned BRL = absent BRL |
| INV-TRUST-006 | Trust | HIGH | BRL must not be older than 6 hours for routing decisions |
| INV-TRUST-007 | Trust | HIGH | Key rotation authenticated only by current private key signature |
| INV-FED-001 | Federation | CRITICAL | `trace_id` is identical in every artifact for a given cross-operator payment |
| INV-FED-002 | Federation | CRITICAL | Every accepted routing request produces exactly one obligation |
| INV-FED-003 | Federation | HIGH | `supports_federation=true` ⟹ routing endpoint actually works |
| INV-FED-004 | Federation | CRITICAL | Same `routing_request_id` always produces the same result |
| INV-FED-005 | Federation | CRITICAL | Value deducted from Operator A = value credited on Operator B |
| INV-FED-006 | Federation | HIGH | Every certificate has `expires_at`; perpetual certification forbidden |
| INV-FED-007 | Federation | CRITICAL | Revoked operator rejected from routing within 6 hours of BRL publication |
| INV-FED-LEDGER-001 | Extension | CRITICAL | Cross-operator ledger entries sum to zero (double-entry extends across boundary) |
| INV-FED-LEDGER-002 | Extension | CRITICAL | All federation monetary values in integer minor units (no float) |
| INV-FED-IDEM-001 | Extension | CRITICAL | `routing_request_id` globally unique across all operators and all time |
| INV-FED-RECON-001 | Extension | HIGH | Every cross-operator payment traceable by `trace_id` across all four artifact types |

---

## Conformance Fail Criteria

A certification run MUST produce FAIL (not warning) if any of the following are true:

| Condition | Invariant | Contract |
|-----------|-----------|---------|
| Certificate signature does not verify | INV-TRUST-001 | operator-certificate |
| Certificate is expired | INV-TRUST-002 | operator-certificate |
| Operator appears in BRL | INV-TRUST-003 | BRL check |
| `supports_federation=true` without valid L3 cert | INV-TRUST-004 | federation-manifest |
| BRL is unsigned | INV-TRUST-005 | BRL contract |
| Routing accepted without obligation recorded | INV-FED-002 | federation-obligation |
| `routing_request_id` is not idempotent | INV-FED-004 | federation-routing |
| Obligation amount ≠ routing request amount | INV-FED-005 | federation-obligation |
| Ledger DEBIT on A ≠ Ledger CREDIT on B | INV-FED-LEDGER-001 | (end-to-end) |
| `trace_id` differs between Operator A and B artifacts | INV-FED-001 | all |
| `amount.minor` is floating point | INV-FED-LEDGER-002 | federation-routing, federation-obligation |

---

## Invariant Ownership Matrix

Each invariant is owned by the party responsible for enforcing it.

| Invariant | BANZA (protocol) | Operator A (originator) | Operator B (destination) | BanzAI (evaluator) |
|-----------|-----------------|------------------------|--------------------------|-------------------|
| INV-TRUST-001 | defines key | verifies | **enforces** | tests |
| INV-TRUST-002 | defines policy | verifies | **enforces** | tests |
| INV-TRUST-003 | **publishes BRL** | verifies | **enforces** | tests |
| INV-TRUST-004 | defines policy | **enforces** | checks | tests |
| INV-TRUST-005 | **signs BRL** | verifies | verifies | tests |
| INV-TRUST-006 | defines interval | **enforces** | **enforces** | tests |
| INV-TRUST-007 | **enforces** (issuance process) | generates rotation | n/a | n/a |
| INV-FED-001 | defines | **enforces** (propagates trace) | **enforces** (echoes trace) | tests |
| INV-FED-002 | defines | **enforces** (records obligation) | n/a | tests |
| INV-FED-003 | defines | n/a | **enforces** (endpoint must work) | tests |
| INV-FED-004 | defines | **enforces** (stable request_id) | **enforces** (idempotent handler) | tests |
| INV-FED-005 | defines | **enforces** (obligation amount) | **enforces** (credit amount) | tests |
| INV-FED-006 | **enforces** (issuance) | renews before expiry | checks before routing | tests |
| INV-FED-007 | **publishes BRL** | **enforces** (checks BRL) | **enforces** (checks BRL) | tests |
| INV-FED-LEDGER-001 | defines | **enforces** (DEBIT) | **enforces** (CREDIT) | tests end-to-end |
| INV-FED-LEDGER-002 | defines in schema | **enforces** | **enforces** | tests |
| INV-FED-IDEM-001 | defines format | **enforces** (generates UUIDs) | **enforces** (unique constraint) | tests |
| INV-FED-RECON-001 | defines | **enforces** (trace propagation) | **enforces** (trace propagation) | audits |
