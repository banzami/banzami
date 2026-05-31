# BANZA Federation Contract Surface

**Document ID:** FEDERATION-CONTRACTS-DESIGN-001  
**Date:** 2026-05-31  
**Status:** Canonical — contract definitions. No implementation required to read this document.  
**Authority:** ADR-026 (Federation Trust Model)  
**Produced by:** BANZA-FEDERATION-READINESS-AUDIT-001, Phase 2

---

## Overview

This document defines the five federation contracts that must exist before any L3 Federation Certification work can begin. Each contract is a protocol-layer artifact — it specifies wire formats, field semantics, invariants, and validation requirements independently of any implementation.

**Contract set:**

| Contract | Path | Purpose |
|----------|------|---------|
| `operator-certificate` | `contracts/federation/operator-certificate.json` | BANZA-issued signed certification artifact |
| `federation-routing` | `contracts/federation/federation-routing.json` | Cross-operator routing request/response wire format |
| `federation-obligation` | `contracts/federation/federation-obligation.json` | Obligation recorded per cross-operator payment |
| `federation-event` | `contracts/federation/federation-event.json` | Cross-operator event envelope |
| `federation-manifest` | `contracts/federation/federation-manifest.json` | Federation extension to the operator manifest |

These contracts are **prerequisites** for:
- Federation conformance vectors (GAP-005)
- Manifest signing implementation (GAP-008)
- InteropRoutingEngine implementation (GAP-003)
- L3 Federation Certification (FED-L3-001 through FED-L3-014)

---

## Contract 1: operator-certificate.json

### Purpose

The operator certificate is the central trust artifact of the BANZA federation. It is a signed JSON document issued by BANZA to a certified operator, cryptographically binding the operator's identity (`operator_id`), public key, and certification level. Federation peers use it to verify each other without contacting BANZA at routing time.

This is the artifact that answers: *"Has BANZA certified this operator at the level it claims?"*

### Ownership

| Role | Party | Responsibility |
|------|-------|----------------|
| Issuer | BANZA | Generates and signs the certificate after conformance approval |
| Holder | Certified operator | Serves the certificate at the well-known endpoint; renews before expiry |
| Verifier | Any federation peer | Fetches and verifies the certificate before accepting routing requests |
| Revocation authority | BANZA | Adds operator_id to BRL; issues emergency BRL if needed |

### Lifecycle

```
[Conformance Pass]
      ↓
[BANZA Review + Approval]
      ↓
[BANZA Issues Certificate]  →  expires_at set (max 90 days for L3+)
      ↓
[Operator Serves at /.well-known/banza/certificate.json]
      ↓
    [Valid]
   /       \
[Expired]  [Revoked → BRL]
      ↓           ↓
[Renewal]    [Re-certification required for revocation]
```

States: `issued` → `valid` → `expired` | `revoked` | `suspended`

Renewal: operator submits renewal request with current certificate as proof. BANZA checks for open issues and re-issues without full re-certification if clean. Full re-certification required at most annually.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | yes | Always `"1"` for this certificate model |
| `operator_id` | string | yes | Stable unique operator identifier. Assigned at L0. Never reused. Pattern: `^[a-z0-9][a-z0-9\-]{2,62}[a-z0-9]$` |
| `certification_level` | integer | yes | Current certification level at issuance. Range 0–4. |
| `protocol_version` | string | yes | BANZA protocol version this certification applies to. Pattern: `^\d+\.\d+$` |
| `capabilities` | array[string] | yes | Specific capabilities that have been conformance-tested and certified. See capability registry. |
| `public_key` | string | yes | Operator's ed25519 public key. Format: `"ed25519:<base64url-encoded 32 bytes>"` |
| `issued_at` | string (ISO 8601 UTC) | yes | Timestamp of certificate issuance by BANZA |
| `expires_at` | string (ISO 8601 UTC) | yes | Timestamp of certificate expiry. MUST be ≤ 90 days after `issued_at` for `certification_level >= 3` |
| `issuer` | string | yes | Always the literal string `"BANZA"`. Any other value is invalid. |
| `issuer_key_id` | string | yes | Identifier for the BANZA signing key used. Enables BANZA key rotation without invalidating outstanding certificates. |
| `signature` | string | yes | ed25519 signature by BANZA. Base64url-encoded. Covers canonical JSON of all other fields. |

### JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12",
  "$id": "https://banza.network/contracts/federation/operator-certificate.json",
  "title": "BanzaOperatorCertificate",
  "description": "Signed certification artifact issued by BANZA to a certified operator. Used by federation peers to verify operator identity and certification level without contacting BANZA at routing time.",
  "_spec_version": "1",
  "_status": "canonical",
  "_authority": "ADR-026, INV-TRUST-001",

  "type": "object",
  "required": [
    "schema_version",
    "operator_id",
    "certification_level",
    "protocol_version",
    "capabilities",
    "public_key",
    "issued_at",
    "expires_at",
    "issuer",
    "issuer_key_id",
    "signature"
  ],
  "additionalProperties": false,

  "properties": {
    "schema_version": {
      "type": "string",
      "const": "1",
      "description": "Certificate schema version. Must be '1' for this certificate format."
    },
    "operator_id": {
      "type": "string",
      "minLength": 4,
      "maxLength": 64,
      "pattern": "^[a-z0-9][a-z0-9\\-]{2,62}[a-z0-9]$",
      "description": "Stable unique operator identifier assigned by BANZA at L0. Never reused."
    },
    "certification_level": {
      "type": "integer",
      "minimum": 0,
      "maximum": 4,
      "description": "Certification level at time of issuance. Level 3+ certificates have a 90-day maximum lifetime."
    },
    "protocol_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+$",
      "description": "BANZA protocol version this certification applies to. e.g. '1.0'."
    },
    "capabilities": {
      "type": "array",
      "items": { "type": "string" },
      "uniqueItems": true,
      "description": "Conformance-tested and certified capabilities. A subset of the operator's declared manifest capabilities.",
      "examples": [["cross_operator_routing", "cross_operator_settlement"]]
    },
    "public_key": {
      "type": "string",
      "pattern": "^ed25519:[A-Za-z0-9_-]{43}$",
      "description": "Operator's ed25519 public key in 'ed25519:<base64url>' format. Bound to operator_id by BANZA's signature."
    },
    "issued_at": {
      "type": "string",
      "format": "date-time",
      "description": "UTC timestamp when BANZA issued this certificate."
    },
    "expires_at": {
      "type": "string",
      "format": "date-time",
      "description": "UTC timestamp of certificate expiry. For certification_level >= 3: MUST be within 90 days of issued_at. INV-TRUST-002: certificates MUST NOT be accepted after this time."
    },
    "issuer": {
      "type": "string",
      "const": "BANZA",
      "description": "Always the literal string 'BANZA'. Any other value makes this certificate invalid."
    },
    "issuer_key_id": {
      "type": "string",
      "description": "Identifier for the BANZA signing key that produced this signature. Allows BANZA to rotate its signing key without invalidating outstanding certificates."
    },
    "signature": {
      "type": "string",
      "pattern": "^[A-Za-z0-9_-]{86}$",
      "description": "ed25519 signature by BANZA. Base64url-encoded (86 chars for 64 bytes). Covers the canonical JSON form of all other fields: fields sorted lexicographically, no whitespace, UTF-8 encoded."
    }
  }
}
```

### Signature Requirements

**Algorithm:** ed25519 (RFC 8032)  
**Signed content:** Canonical JSON of all fields except `signature`. Canonical form: fields sorted lexicographically by key, no whitespace, UTF-8 encoding.  
**Signing party:** BANZA (holds root ed25519 private key, offline / HSM)  
**Verification:** Any party holding `BANZA_PUBLIC_KEY` for the corresponding `issuer_key_id`  

Canonical JSON construction:
```
canonical = sort_keys_lexicographic({all fields except "signature"})
           → json_stringify(no whitespace)
           → utf8_encode
signature = base64url(ed25519_sign(BANZA_PRIVATE_KEY, canonical))
```

### Validation Requirements

A certificate is valid if and only if ALL of the following hold:
1. `signature` verifies: `ed25519_verify(BANZA_PUBLIC_KEY[issuer_key_id], canonical_json, base64url_decode(signature))` (INV-TRUST-001)
2. `expires_at > now()` — no grace period (INV-TRUST-002)
3. `issued_at <= now()` — not a future-dated certificate
4. `expires_at - issued_at <= 90 days` when `certification_level >= 3` (INV-TRUST-002)
5. `issuer == "BANZA"` — any other issuer is structurally invalid
6. `operator_id` is not present in the current, valid BANZA Revocation List (INV-TRUST-003)
7. `certification_level >= REQUIRED_LEVEL` for the use case (≥ 3 for federation routing)

### Certification Evidence

| L3 Requirement | Evidence from this contract |
|----------------|----------------------------|
| FED-L3-001 | Certificate exists at `/.well-known/banza/certificate.json` and has `certification_level >= 3` |
| FED-L3-002 | `expires_at > now()` at test time |
| FED-L3-005 | `certificate.operator_id == manifest.operator_id` |

### Served At

`GET /.well-known/banza/certificate.json` — operator's public HTTPS endpoint  
Response: the certificate JSON object. No authentication required. MUST be served over TLS.

---

## Contract 2: federation-routing.json

### Purpose

The routing contract defines the wire format for cross-operator routing — the mechanism by which Operator A instructs Operator B to accept a payment on behalf of a consumer on Operator A. This is the primary inter-operator protocol message.

This contract defines both:
- The **routing request**: Operator A → Operator B
- The **routing response**: Operator B → Operator A

### Ownership

| Role | Party | Responsibility |
|------|-------|----------------|
| Sender | Originating operator (Operator A) | Constructs and signs routing request; retries on network failure with same `routing_request_id` |
| Receiver | Destination operator (Operator B) | Validates request, verifies Operator A's certificate, accepts or rejects, returns idempotent response |
| Idempotency guarantor | Both operators | Same `routing_request_id` MUST produce same result on both sides (INV-FED-004) |

### Lifecycle

```
Operator A selects Operator B as destination
        ↓
Operator A constructs RoutingRequest
        ↓
POST /federation/route (signed)
        ↓
Operator B verifies:
  1. Operator A's signature on request
  2. Operator A's certificate (trust protocol steps 1–9)
  3. Amount within accepted range
  4. Recipient identifiable on Operator B
        ↓
     [accepted]             [rejected]
        ↓                      ↓
Operator B creates        Returns rejection_code
interop_transfer_id       + rejection_reason
        ↓
Obligation recorded by Operator A
        ↓
Payment completes on Operator B
```

States: `pending` (async processing) | `accepted` | `rejected`

### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | yes | Always `"1"` |
| `routing_request_id` | string | yes | Globally unique idempotency key. Format: `"rr-<uuid>"`. Operator A assigns. MUST be stable across retries. |
| `trace_id` | string | yes | Causal trace identifier from originating transaction. MUST propagate unchanged (INV-FED-001). |
| `from_operator_id` | string | yes | `operator_id` of the originating operator (Operator A) |
| `to_operator_id` | string | yes | `operator_id` of the destination operator (Operator B) |
| `amount` | object | yes | Payment amount. See `Amount` schema. |
| `amount.minor` | integer | yes | Amount in currency minor units. MUST be > 0. MUST use integer arithmetic (INV-LEDGER-003). |
| `amount.currency` | string | yes | ISO 4217 currency code. e.g. `"AOA"`. |
| `sender_wallet_id` | string | yes | Wallet ID of the payer on Operator A. |
| `recipient_identifier` | string | yes | How to identify the payment recipient on Operator B. |
| `recipient_identifier_type` | string | yes | Type of identifier. Enum: `"wallet_id"` \| `"handle"` \| `"phone"` \| `"account_number"` |
| `created_at` | string (ISO 8601 UTC) | yes | When Operator A created this routing request. |
| `certificate_url` | string | yes | URL where Operator B can fetch Operator A's certificate for bidirectional trust verification. |

### Response Fields

| Field | Type | Presence | Description |
|-------|------|----------|-------------|
| `schema_version` | string | always | Always `"1"` |
| `routing_request_id` | string | always | Echo of the request's `routing_request_id` |
| `status` | string | always | `"accepted"` \| `"rejected"` \| `"pending"` |
| `trace_id` | string | always | Echo of the request's `trace_id`. MUST be identical (INV-FED-001). |
| `interop_transfer_id` | string | if accepted | Operator B's internal transfer identifier. Format: `"itx-<uuid>"`. |
| `accepted_at` | string (ISO 8601 UTC) | if accepted | When Operator B accepted the routing request. |
| `rejection_code` | string | if rejected | Structured rejection reason. See rejection code registry. |
| `rejection_reason` | string | if rejected | Human-readable rejection explanation (English). |
| `estimated_completion_at` | string (ISO 8601 UTC) | if pending | Estimated completion time for async routing. |

### Rejection Code Registry

| Code | Meaning |
|------|---------|
| `recipient_not_found` | No wallet matching `recipient_identifier` on Operator B |
| `recipient_suspended` | Recipient wallet is suspended |
| `currency_not_supported` | Operator B does not accept `amount.currency` in cross-operator payments |
| `amount_below_minimum` | Amount is below Operator B's cross-operator minimum |
| `amount_above_maximum` | Amount exceeds Operator B's cross-operator limit |
| `operator_trust_failure` | Operator B could not verify Operator A's certificate |
| `capability_unavailable` | Operator B is temporarily unable to accept cross-operator payments |
| `duplicate_request` | `routing_request_id` already processed with different content (invariant violation by Operator A) |

### JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12",
  "$id": "https://banza.network/contracts/federation/federation-routing.json",
  "title": "BanzaFederationRouting",
  "description": "Wire format for cross-operator routing requests and responses. Defines how Operator A initiates a payment on Operator B.",
  "_spec_version": "1",
  "_status": "canonical",
  "_authority": "ADR-026, RFC-0001, INV-FED-001, INV-FED-004",

  "$defs": {
    "Amount": {
      "type": "object",
      "required": ["minor", "currency"],
      "additionalProperties": false,
      "properties": {
        "minor": {
          "type": "integer",
          "minimum": 1,
          "description": "Amount in currency minor units. MUST be positive. INV-LEDGER-003: integer arithmetic only."
        },
        "currency": {
          "type": "string",
          "pattern": "^[A-Z]{3}$",
          "description": "ISO 4217 three-letter currency code."
        }
      }
    },

    "RoutingRequest": {
      "type": "object",
      "required": [
        "schema_version",
        "routing_request_id",
        "trace_id",
        "from_operator_id",
        "to_operator_id",
        "amount",
        "sender_wallet_id",
        "recipient_identifier",
        "recipient_identifier_type",
        "created_at",
        "certificate_url"
      ],
      "additionalProperties": false,
      "properties": {
        "schema_version": { "type": "string", "const": "1" },
        "routing_request_id": {
          "type": "string",
          "pattern": "^rr-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
          "description": "Globally unique idempotency key. Stable across retries. INV-FED-004."
        },
        "trace_id": {
          "type": "string",
          "description": "Causal trace identifier. MUST propagate unchanged across all federation artifacts. INV-FED-001."
        },
        "from_operator_id": {
          "type": "string",
          "description": "operator_id of the originating operator."
        },
        "to_operator_id": {
          "type": "string",
          "description": "operator_id of the destination operator."
        },
        "amount": { "$ref": "#/$defs/Amount" },
        "sender_wallet_id": {
          "type": "string",
          "description": "Wallet ID of the payer on the originating operator."
        },
        "recipient_identifier": {
          "type": "string",
          "description": "Identifier for the payment recipient on the destination operator."
        },
        "recipient_identifier_type": {
          "type": "string",
          "enum": ["wallet_id", "handle", "phone", "account_number"],
          "description": "Type of recipient identifier."
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "UTC timestamp when Operator A created this routing request."
        },
        "certificate_url": {
          "type": "string",
          "format": "uri",
          "description": "URL where Operator B can fetch Operator A's certificate for bidirectional trust verification."
        }
      }
    },

    "RoutingResponse": {
      "type": "object",
      "required": ["schema_version", "routing_request_id", "status", "trace_id"],
      "additionalProperties": false,
      "properties": {
        "schema_version": { "type": "string", "const": "1" },
        "routing_request_id": {
          "type": "string",
          "description": "Echo of the request routing_request_id."
        },
        "status": {
          "type": "string",
          "enum": ["accepted", "rejected", "pending"],
          "description": "Routing decision by Operator B."
        },
        "trace_id": {
          "type": "string",
          "description": "Echo of the request trace_id. MUST be identical to request. INV-FED-001."
        },
        "interop_transfer_id": {
          "type": "string",
          "pattern": "^itx-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
          "description": "Operator B's internal transfer identifier. Present only if status=accepted."
        },
        "accepted_at": {
          "type": "string",
          "format": "date-time",
          "description": "UTC timestamp of acceptance. Present only if status=accepted."
        },
        "rejection_code": {
          "type": "string",
          "enum": [
            "recipient_not_found",
            "recipient_suspended",
            "currency_not_supported",
            "amount_below_minimum",
            "amount_above_maximum",
            "operator_trust_failure",
            "capability_unavailable",
            "duplicate_request"
          ],
          "description": "Structured rejection code. Present only if status=rejected."
        },
        "rejection_reason": {
          "type": "string",
          "description": "Human-readable rejection explanation. Present only if status=rejected."
        },
        "estimated_completion_at": {
          "type": "string",
          "format": "date-time",
          "description": "Estimated completion time. Present only if status=pending."
        }
      }
    }
  }
}
```

### Signature Requirements

**Purpose:** Authenticate the routing request. Operator B must verify that the request genuinely came from Operator A.  
**Algorithm:** ed25519  
**Signing party:** Operator A (using the private key corresponding to the public key in its certificate)  
**HTTP Header:** `Banza-Federation-Signature: t=<unix_seconds>,v1=<ed25519_base64url>`  
**Signed payload:** `utf8(str(unix_seconds)) + "." + raw_request_body_bytes`

Operator B verifies:
1. Fetch Operator A's certificate from `certificate_url`
2. Verify certificate (trust protocol Steps 4–9)
3. Extract `certificate.public_key`
4. Reconstruct signed payload
5. Verify ed25519 signature against `certificate.public_key`

### Validation Requirements

Operator B MUST reject the request if:
- Signature verification fails
- `to_operator_id != this operator's operator_id`
- `from_operator_id` certificate trust fails (any trust protocol step fails)
- `amount.minor <= 0`
- Same `routing_request_id` received with different content (report `duplicate_request`)
- `created_at` is more than 300 seconds in the past or future

### Certification Evidence

| L3 Requirement | Evidence from this contract |
|----------------|----------------------------|
| FED-L3-007 | `POST /federation/route` returns valid RoutingResponse |
| FED-L3-009/010 | Bidirectional trust verification via `certificate_url` in request |
| FED-L3-011 | accepted routing request → payment completes on Operator B |
| FED-L3-012 | `trace_id` in response matches request (INV-FED-001) |

### Served At

`POST /federation/route` — on the destination operator's `interop_endpoint`  
Authentication: `Banza-Federation-Signature` header required  
TLS: required

---

## Contract 3: federation-obligation.json

### Purpose

The obligation contract defines the record created when a cross-operator payment is accepted. An obligation represents the debt that Operator A owes Operator B as a result of a routed payment. Obligations are the input to the cross-operator netting and settlement process (RFC-0002).

This is the answer to the question: *"How does Operator A discharge what it owes Operator B?"*

### Ownership

| Role | Party | Responsibility |
|------|-------|----------------|
| Creator | Originating operator (Operator A) | Records obligation upon receiving `status=accepted` response; signs it |
| Counterparty | Destination operator (Operator B) | Receives obligations during netting; disputes if amount mismatches |
| Netting authority | Both operators jointly | Exchange and reconcile obligation lists; compute net position |
| Verifier | Any auditor | Can verify obligation signatures without operator involvement |

### Lifecycle

```
[RoutingResponse.status = "accepted"]
        ↓
[Operator A records InteropObligation]
  obligation_id assigned
  settlement_state = "pending"
        ↓
[Netting cycle begins]
  settlement_state = "in_netting"
        ↓
[Net position computed and agreed]
        ↓
[Settlement executed via bank rail]
  settlement_state = "settled"
  settled_at = now()
  settlement_batch_id assigned
```

States: `pending` → `in_netting` → `settled`

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | yes | Always `"1"` |
| `obligation_id` | string | yes | Globally unique obligation identifier. Format: `"ob-<uuid>"`. Assigned by Operator A. |
| `from_operator_id` | string | yes | Operator that owes the money (the routing requestor). |
| `to_operator_id` | string | yes | Operator that is owed the money (the routing acceptor). |
| `amount` | object | yes | Amount owed. Same schema as RoutingRequest.amount. MUST match exactly. |
| `routing_request_id` | string | yes | The routing request that created this obligation. One-to-one (UNIQUE). |
| `interop_transfer_id` | string | yes | Operator B's transfer ID from the RoutingResponse. |
| `trace_id` | string | yes | Causal trace identifier. MUST match the originating payment (INV-FED-001). |
| `recorded_at` | string (ISO 8601 UTC) | yes | When Operator A recorded this obligation. |
| `settlement_state` | string | yes | Enum: `"pending"` \| `"in_netting"` \| `"settled"` |
| `netting_period` | string | no | Identifier for the netting cycle (e.g., `"2026-06-01"`). Set when entering `in_netting`. |
| `settled_at` | string (ISO 8601 UTC) | no | When this obligation was settled. Present only when `settlement_state = "settled"`. |
| `settlement_batch_id` | string | no | Settlement batch identifier. Present only when `settlement_state = "settled"`. |
| `obligor_signature` | string | yes | ed25519 signature by Operator A over canonical JSON of obligation fields (excluding `obligor_signature`). Prevents Operator A from disputing the amount at netting time. |

### JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12",
  "$id": "https://banza.network/contracts/federation/federation-obligation.json",
  "title": "BanzaFederationObligation",
  "description": "Obligation created by the originating operator when a cross-operator payment is accepted. Input to the cross-operator netting and settlement process.",
  "_spec_version": "1",
  "_status": "canonical",
  "_authority": "ADR-026, RFC-0002, INV-FED-002, INV-FED-005",

  "type": "object",
  "required": [
    "schema_version",
    "obligation_id",
    "from_operator_id",
    "to_operator_id",
    "amount",
    "routing_request_id",
    "interop_transfer_id",
    "trace_id",
    "recorded_at",
    "settlement_state",
    "obligor_signature"
  ],
  "additionalProperties": false,

  "properties": {
    "schema_version": { "type": "string", "const": "1" },

    "obligation_id": {
      "type": "string",
      "pattern": "^ob-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
      "description": "Globally unique obligation identifier. Assigned by Operator A."
    },

    "from_operator_id": {
      "type": "string",
      "description": "operator_id of the operator that owes the money."
    },

    "to_operator_id": {
      "type": "string",
      "description": "operator_id of the operator that is owed the money."
    },

    "amount": {
      "type": "object",
      "required": ["minor", "currency"],
      "additionalProperties": false,
      "properties": {
        "minor": {
          "type": "integer",
          "minimum": 1,
          "description": "Amount in minor units. MUST equal the amount in the routing request. INV-FED-005."
        },
        "currency": {
          "type": "string",
          "pattern": "^[A-Z]{3}$"
        }
      }
    },

    "routing_request_id": {
      "type": "string",
      "pattern": "^rr-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
      "description": "The routing request that generated this obligation. UNIQUE — one obligation per routing request."
    },

    "interop_transfer_id": {
      "type": "string",
      "pattern": "^itx-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
      "description": "Operator B's transfer ID from the RoutingResponse. Corroborates the obligation."
    },

    "trace_id": {
      "type": "string",
      "description": "Causal trace identifier. MUST match the originating payment trace_id. INV-FED-001."
    },

    "recorded_at": {
      "type": "string",
      "format": "date-time",
      "description": "UTC timestamp when Operator A recorded this obligation."
    },

    "settlement_state": {
      "type": "string",
      "enum": ["pending", "in_netting", "settled"],
      "description": "Current state in the obligation lifecycle."
    },

    "netting_period": {
      "type": "string",
      "description": "Netting cycle identifier. Set when settlement_state transitions to 'in_netting'. e.g. '2026-06-01'."
    },

    "settled_at": {
      "type": "string",
      "format": "date-time",
      "description": "UTC timestamp of settlement. Present only when settlement_state = 'settled'."
    },

    "settlement_batch_id": {
      "type": "string",
      "description": "Settlement batch identifier. Present only when settlement_state = 'settled'."
    },

    "obligor_signature": {
      "type": "string",
      "pattern": "^[A-Za-z0-9_-]{86}$",
      "description": "ed25519 signature by Operator A over canonical JSON of all fields except obligor_signature. Prevents amount disputes at netting time."
    }
  },

  "if": { "properties": { "settlement_state": { "const": "settled" } }, "required": ["settlement_state"] },
  "then": { "required": ["settled_at", "settlement_batch_id"] }
}
```

### Signature Requirements

**Algorithm:** ed25519  
**Signing party:** Operator A (`from_operator_id`) — using the private key corresponding to its certificate  
**Signed content:** Canonical JSON of all fields except `obligor_signature`  
**Verification:** Counterparty (Operator B) or any auditor, using Operator A's certificate public key

This signature makes the obligation non-repudiable: Operator A cannot dispute the amount at netting time because it signed it when the obligation was recorded.

### Validation Requirements

Obligation is valid if:
1. `obligor_signature` verifies against Operator A's certificate `public_key`
2. `amount` exactly matches the `amount` in the referenced routing request
3. `routing_request_id` refers to a routing request that received `status=accepted`
4. `trace_id` matches the originating payment's `trace_id`
5. `from_operator_id` matches the routing request's `from_operator_id`
6. `to_operator_id` matches the routing request's `to_operator_id`
7. `settlement_state` follows valid transitions: `pending` → `in_netting` → `settled` only

### Certification Evidence

| L3 Requirement | Evidence from this contract |
|----------------|----------------------------|
| FED-L3-008 | `GET /federation/obligations` returns valid obligations |
| FED-L3-013 | Obligation recorded immediately upon routing acceptance (INV-FED-002) |
| FED-L3-014 | `amount.minor` in obligation = `amount.minor` in routing request (INV-FED-005) |

### Served At

`GET /federation/obligations` — list all obligations (filterable by `settlement_state`, `to_operator_id`)  
`GET /federation/obligations/{obligation_id}` — get specific obligation  
Authentication: operator-to-operator mutual authentication (Banza-Federation-Signature)

---

## Contract 4: federation-event.json

### Purpose

Federation events are the protocol's cross-operator observability mechanism. When a payment crosses operator boundaries, events must be emitted on both sides — and the event on Operator B must be traceable to the event on Operator A via the shared `trace_id`. This contract extends the existing `contracts/events/envelope.schema.json` with federation-specific fields.

This contract does not replace the single-operator event envelope. It extends it: every federation event IS a valid base event envelope, with additional required fields.

### Ownership

| Role | Party | Responsibility |
|------|-------|----------------|
| Emitter | The operator where the state change occurred | Emits event on its own event stream; delivers to counterparty if applicable |
| Consumer | Counterparty operator or audit/observability consumer | Subscribes to `GET /federation/events` or receives pushed events |
| Authority | BANZA (protocol) | Defines event type registry; conformance tests verify event presence |

### Event Type Registry

All federation event types follow the namespace `federation.*`:

| Event Type | Emitted By | Trigger |
|------------|------------|---------|
| `federation.routing.received` | Operator B | Routing request received from Operator A |
| `federation.routing.accepted` | Operator B | Routing request accepted; `interop_transfer_id` assigned |
| `federation.routing.rejected` | Operator B | Routing request rejected; `rejection_code` set |
| `federation.payment.initiated` | Operator A | Cross-operator routing request sent |
| `federation.payment.completed` | Operator B | Payment credited on Operator B; obligation due |
| `federation.payment.failed` | Operator A or B | Payment failed mid-flight |
| `federation.obligation.recorded` | Operator A | Obligation recorded after routing acceptance |
| `federation.obligation.settled` | Operator A | Obligation settled in a batch |
| `federation.settlement.initiated` | Operator A | Netting cycle started |
| `federation.settlement.completed` | Operator A | Net settlement executed; obligations marked settled |

### Fields

All fields from `contracts/events/envelope.schema.json` (`id`, `event_type`, `aggregate_type`, `aggregate_id`, `trace_id`, `correlation_id`, `payload`, `created_at`) are inherited and remain required.

Additional required fields for federation events:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `federation_version` | string | yes | Always `"1"`. Marks this as a federation event. |
| `origin_operator_id` | string | yes | `operator_id` of the operator that emitted this event. |
| `destination_operator_id` | string | yes | `operator_id` of the operator this event concerns (may differ from origin). |
| `routing_request_id` | string | conditional | The routing request this event relates to. Required for `routing.*` and `payment.*` event types. |
| `interop_transfer_id` | string | conditional | The interop transfer this event relates to. Required after routing acceptance. |
| `obligation_id` | string | conditional | The obligation this event relates to. Required for `obligation.*` and `settlement.*` event types. |

The `aggregate_type` for all federation events is `"federation_payment"`.

### JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12",
  "$id": "https://banza.network/contracts/federation/federation-event.json",
  "title": "BanzaFederationEvent",
  "description": "Event envelope for events that cross operator boundaries. Extends contracts/events/envelope.schema.json with federation-specific fields. Every federation event is a valid base event envelope.",
  "_spec_version": "1",
  "_status": "canonical",
  "_authority": "ADR-026, INV-FED-001",
  "_extends": "contracts/events/envelope.schema.json",

  "allOf": [
    { "$ref": "https://banza.network/contracts/events/envelope.schema.json" },
    {
      "type": "object",
      "required": ["federation_version", "origin_operator_id", "destination_operator_id"],
      "properties": {
        "federation_version": {
          "type": "string",
          "const": "1",
          "description": "Federation protocol version. Always '1'. Marks this as a federation event."
        },
        "origin_operator_id": {
          "type": "string",
          "description": "operator_id of the operator that emitted this event."
        },
        "destination_operator_id": {
          "type": "string",
          "description": "operator_id of the operator this event concerns."
        },
        "routing_request_id": {
          "type": "string",
          "pattern": "^rr-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
          "description": "Routing request this event relates to. Required for federation.routing.* and federation.payment.* event types."
        },
        "interop_transfer_id": {
          "type": "string",
          "pattern": "^itx-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
          "description": "Interop transfer ID from Operator B. Required after routing acceptance."
        },
        "obligation_id": {
          "type": "string",
          "pattern": "^ob-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
          "description": "Obligation this event relates to. Required for federation.obligation.* and federation.settlement.* event types."
        },
        "event_type": {
          "type": "string",
          "enum": [
            "federation.routing.received",
            "federation.routing.accepted",
            "federation.routing.rejected",
            "federation.payment.initiated",
            "federation.payment.completed",
            "federation.payment.failed",
            "federation.obligation.recorded",
            "federation.obligation.settled",
            "federation.settlement.initiated",
            "federation.settlement.completed"
          ],
          "description": "Federation event type. Overrides the base event_type to restrict to federation namespace."
        },
        "aggregate_type": {
          "type": "string",
          "const": "federation_payment",
          "description": "Aggregate type for all federation events."
        }
      }
    }
  ]
}
```

### Signature Requirements

Federation events follow the same signing model as base events. They are served over the authenticated `/federation/events` endpoint. No additional per-event signature is required beyond the transport-level authentication (`Banza-Federation-Signature` header).

### Validation Requirements

A federation event is valid if:
1. It is a valid base event envelope (validates against `contracts/events/envelope.schema.json`)
2. `federation_version == "1"`
3. `trace_id` matches the `trace_id` of the originating payment on both operators (INV-FED-001)
4. `origin_operator_id` and `destination_operator_id` are non-empty
5. `routing_request_id` is present for `federation.routing.*` and `federation.payment.*` events
6. `obligation_id` is present for `federation.obligation.*` and `federation.settlement.*` events

### Certification Evidence

| L3 Requirement | Evidence from this contract |
|----------------|----------------------------|
| FED-L3-012 | `trace_id` is identical across Operator A and Operator B events for the same payment (INV-FED-001) |
| FED-L3-011 | `federation.payment.completed` event on Operator B confirms receipt |

### Served At

`GET /federation/events` — SSE stream or polling endpoint for cross-operator events  
`POST /federation/events` — inbound event delivery from counterparty operator  
Authentication: `Banza-Federation-Signature` header required

---

## Contract 5: federation-manifest.json

### Purpose

The federation manifest contract defines the additional fields that must be present in an operator's manifest (`/.well-known/banza/operator.json`) for the operator to be a valid federation participant. It is an **extension** to the base manifest schema (`conformance/manifests/schema.json`), not a replacement.

A federation-capable manifest is a base manifest that also satisfies this extension schema.

This contract answers: *"What must an operator declare in its manifest to participate in federation?"*

### Ownership

| Role | Party | Responsibility |
|------|-------|----------------|
| Author | Each operator | Publishes its own manifest including federation extension fields |
| Validator | Federation peers | Verify federation extension fields before establishing routing relationships |
| Schema authority | BANZA (protocol) | Defines which fields are required and their constraints |
| Conformance evaluator | BanzAI | Validates manifest against both base schema and federation extension |

### Lifecycle

The manifest lifecycle is inherited from the base manifest. The federation extension fields have additional constraints:

- `supports_federation` MUST be `false` until the operator holds a valid certificate at `certification_level >= 3` (INV-TRUST-004)
- `certificate_url` MUST point to an accessible, valid certificate before `supports_federation` is set to `true`
- `interop_endpoint` MUST be the base URL of a running federation API before `supports_federation` is set to `true`

### Fields

Fields are additional to the base manifest schema (`conformance/manifests/schema.json`):

| Field | Type | Required for L3 | Description |
|-------|------|-----------------|-------------|
| `federation_version` | string | yes | Federation protocol version supported. Always `"1"` for this protocol. |
| `certificate_url` | string (URI) | yes | URL where peers can fetch this operator's BANZA-issued certificate. Default: `{operator_url}/.well-known/banza/certificate.json` |
| `interop_endpoint` | string (URI) | yes | Base URL for this operator's federation API endpoints (e.g., `POST /federation/route` is at `{interop_endpoint}/federation/route`) |
| `supports_federation` | boolean | yes | MUST be `true` for federation participation. MUST NOT be `true` unless `certification_level >= 3` in certificate. INV-TRUST-004. |
| `cross_operator_routing` | boolean | yes | This operator can accept routing requests from other operators. |
| `cross_operator_settlement` | boolean | yes | This operator participates in cross-operator netting and settlement. |
| `federation_capabilities` | object | yes | Detailed federation capability declaration. |
| `federation_capabilities.routing_version` | string | yes | Which federation routing protocol version. Always `"1"`. |
| `federation_capabilities.settlement_version` | string | yes | Which federation settlement protocol version. Always `"1"`. |
| `federation_capabilities.supported_currencies` | array[string] | yes | ISO 4217 currency codes accepted in cross-operator payments. Must be non-empty. |
| `federation_capabilities.netting_interval_hours` | integer | yes | How often this operator runs netting cycles. e.g. `24` for daily netting. |
| `federation_capabilities.max_transaction_amount_minor` | integer | no | Per-transaction maximum for cross-operator payments in the primary currency's minor units. Absent = no limit declared. |

### JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12",
  "$id": "https://banza.network/contracts/federation/federation-manifest.json",
  "title": "BanzaFederationManifestExtension",
  "description": "Extension schema for federation-capable operator manifests. A federation manifest is a base operator manifest that also validates against this extension. Served at /.well-known/banza/operator.json alongside the base manifest fields.",
  "_spec_version": "1",
  "_status": "canonical",
  "_authority": "ADR-026, RFC-0005, INV-TRUST-004, INV-FED-003",
  "_extends": "conformance/manifests/schema.json",

  "type": "object",
  "required": [
    "federation_version",
    "certificate_url",
    "interop_endpoint",
    "supports_federation",
    "cross_operator_routing",
    "cross_operator_settlement",
    "federation_capabilities"
  ],

  "properties": {
    "federation_version": {
      "type": "string",
      "const": "1",
      "description": "Federation protocol version supported by this operator."
    },

    "certificate_url": {
      "type": "string",
      "format": "uri",
      "description": "URL where federation peers can fetch this operator's BANZA-issued certificate. MUST be accessible over TLS without authentication."
    },

    "interop_endpoint": {
      "type": "string",
      "format": "uri",
      "description": "Base URL for this operator's federation API. POST /federation/route, GET /federation/obligations, etc. are all relative to this base."
    },

    "supports_federation": {
      "type": "boolean",
      "description": "True if this operator participates in federation. INV-TRUST-004: MUST NOT be true unless the operator holds a valid L3+ certificate. INV-FED-003: setting this true without certification is a protocol violation."
    },

    "cross_operator_routing": {
      "type": "boolean",
      "description": "True if this operator can accept POST /federation/route requests from other certified operators."
    },

    "cross_operator_settlement": {
      "type": "boolean",
      "description": "True if this operator participates in cross-operator netting and settlement (RFC-0002). Required for L4."
    },

    "federation_capabilities": {
      "type": "object",
      "required": [
        "routing_version",
        "settlement_version",
        "supported_currencies",
        "netting_interval_hours"
      ],
      "additionalProperties": false,
      "properties": {
        "routing_version": {
          "type": "string",
          "const": "1",
          "description": "Federation routing protocol version. Must be '1'."
        },
        "settlement_version": {
          "type": "string",
          "const": "1",
          "description": "Federation settlement protocol version. Must be '1'."
        },
        "supported_currencies": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"
          },
          "minItems": 1,
          "uniqueItems": true,
          "description": "ISO 4217 currency codes accepted in cross-operator payments by this operator."
        },
        "netting_interval_hours": {
          "type": "integer",
          "minimum": 1,
          "maximum": 168,
          "description": "How often this operator runs netting cycles (in hours). Maximum 168h (7 days). e.g. 24 for daily netting."
        },
        "max_transaction_amount_minor": {
          "type": "integer",
          "minimum": 1,
          "description": "Per-transaction maximum for cross-operator payments in the primary currency's minor units. Absent means no per-transaction limit declared by this operator."
        }
      }
    }
  },

  "if": {
    "properties": { "supports_federation": { "const": true } },
    "required": ["supports_federation"]
  },
  "then": {
    "properties": {
      "cross_operator_routing": { "const": true }
    },
    "description": "If supports_federation is true, cross_operator_routing MUST also be true. A federation member that cannot route is not a federation member."
  }
}
```

### Signature Requirements

The manifest as a whole must be signed by BANZA. Manifest signing is specified in GAP-008 (not yet implemented). The signing mechanism will:
- Compute canonical JSON of the manifest (all fields, sorted lexicographically)
- Produce an ed25519 signature using the BANZA root signing key
- The signature will be added as a `manifest_signature` field (spec to be defined in manifest signing ADR)

Until manifest signing is implemented, the manifest's federation fields are informational only — peers MUST rely on the certificate (Contract 1) for cryptographic trust, not on unsigned manifest declarations.

### Validation Requirements

A federation manifest is valid if:
1. It satisfies the base manifest schema (`conformance/manifests/schema.json`)
2. All federation extension fields listed above are present with correct types
3. `supports_federation == true` only if the operator's certificate is valid and `certification_level >= 3` (INV-TRUST-004)
4. `certificate_url` is accessible and returns a valid certificate
5. `interop_endpoint` is accessible and `POST /federation/route` returns HTTP 200 or 405 (endpoint exists)
6. If `cross_operator_settlement == true`, `cross_operator_routing` MUST also be true

### Certification Evidence

| L3 Requirement | Evidence from this contract |
|----------------|----------------------------|
| FED-L3-003 | `supports_federation == true` and `cross_operator_routing == true` |
| FED-L3-004 | `interop_endpoint` points to working federation API |
| FED-L3-005 | `certificate_url` accessible and `certificate.operator_id == manifest.operator_id` |

### Served At

`GET /.well-known/banza/operator.json` — same endpoint as the base manifest  
The federation extension fields are merged into the single manifest document. No separate endpoint.

---

## Contract Dependency Map

```
federation-manifest.json
        │
        ├── references → operator-certificate.json (certificate_url)
        └── enables → federation-routing.json (interop_endpoint)
                            │
                            ├── creates → federation-obligation.json
                            │                      │
                            │                      └── closes → federation-event.json
                            │                                   (obligation.settled)
                            └── emits → federation-event.json
                                        (routing.accepted/rejected)
```

All five contracts share:
- `trace_id` — propagated across all artifacts for a given cross-operator payment
- `operator_id` — BANZA-assigned stable identifier, the common key across all contracts
- `schema_version: "1"` — all contracts start at version 1
- ed25519 as the canonical signing algorithm
