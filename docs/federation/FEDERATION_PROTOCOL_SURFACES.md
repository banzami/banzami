# BANZA Federation Protocol Surfaces

**Audit ID:** BANZA-FEDERATION-READINESS-AUDIT-001  
**Date:** 2026-05-31

---

## Currently Defined Federation Contracts

### Existing

| Contract | Path | Status | What It Covers |
|----------|------|--------|----------------|
| Operator Manifest Schema | `conformance/manifests/schema.json` | ✓ Complete | Operator identity, capabilities, safety invariants |
| Capability Schema | `conformance/capabilities/schema.json` | ✓ Complete | Per-capability certification level mapping |
| Webhook Signature Spec | `contracts/webhooks/signature.json` | ✓ Complete | Outbound event signing — reusable for federation |
| Event Envelope Schema | `contracts/events/envelope.schema.json` | ✓ Complete | Internal event format — reusable for federation |
| QR Payload Format | `contracts/qr/payload-format.json` | ✓ Complete | QR encoding — operator-agnostic by design |

---

## Required Federation Contracts

These do not yet exist. They are the protocol surfaces that must be specified before L3 can be certifiable.

### `contracts/federation/operator-certificate.json`

**Purpose:** Schema for the signed artifact that BANZA issues when an operator reaches a certification level. Used by federation peers to verify each other's certification status.

**Minimum fields:**
```json
{
  "operator_id": "string — stable, unique operator identifier",
  "certification_level": "integer 0–4",
  "issued_at": "ISO 8601 timestamp",
  "expires_at": "ISO 8601 timestamp",
  "issuer": "string — always 'BANZA'",
  "protocol_version": "string — e.g. '1.0'",
  "public_key": "string — ed25519 base64-encoded public key",
  "signature": "string — BANZA's signature over the above fields"
}
```

**Authority note:** BANZA issues this certificate. BanzAI verifies it. Operators present it during federation onboarding.

---

### `contracts/federation/federation-routing.json`

**Purpose:** Wire format for the cross-operator routing request/response protocol. Defines how Operator A communicates a routing decision to Operator B.

**Minimum fields — request:**
```json
{
  "routing_request_id": "string — idempotency key",
  "trace_id": "string — must propagate to all artifacts",
  "from_operator_id": "string",
  "to_operator_id": "string",
  "amount": { "minor": "integer", "currency": "ISO 4217" },
  "sender_wallet_id": "string",
  "recipient_wallet_id": "string",
  "created_at": "ISO 8601"
}
```

**Minimum fields — response:**
```json
{
  "routing_request_id": "string — echo",
  "status": "accepted | rejected | pending",
  "rejection_reason": "string? — if rejected",
  "interop_transfer_id": "string? — if accepted",
  "trace_id": "string — same as request"
}
```

---

### `contracts/federation/federation-obligation.json`

**Purpose:** Schema for the obligation created when a payment crosses operator boundaries. Used by `InteropObligation` struct (RFC-0002).

**Minimum fields:**
```json
{
  "obligation_id": "string — globally unique",
  "from_operator_id": "string — operator that owes",
  "to_operator_id": "string — operator that is owed",
  "amount": { "minor": "integer", "currency": "ISO 4217" },
  "payment_ref": "string — originating payment or transfer ID",
  "trace_id": "string",
  "recorded_at": "ISO 8601",
  "settled_at": "ISO 8601? — null until settled",
  "settlement_batch_id": "string? — null until settled"
}
```

---

### `contracts/federation/federation-event.json`

**Purpose:** Schema for events that cross operator boundaries. Extends the existing event envelope with federation-specific fields.

**Minimum fields (extends `contracts/events/envelope.schema.json`):**
```json
{
  "type": "federation.payment.initiated | federation.payment.completed | ...",
  "origin_operator_id": "string",
  "destination_operator_id": "string",
  "trace_id": "string — same across both operators",
  "payload": { ... }
}
```

---

### `contracts/federation/federation-trust.json`

**Purpose:** Protocol spec for trust establishment between operators. Defines how Operator A verifies that Operator B is a legitimate BANZA federation member.

**Minimum fields — trust assertion:**
```json
{
  "verifier_operator_id": "string — who is verifying",
  "verified_operator_id": "string — who is being verified",
  "manifest_url": "string — /.well-known/banza/operator.json at verified operator",
  "certificate_url": "string? — where to fetch the operator certificate",
  "verification_result": "trusted | untrusted | expired | revoked",
  "verified_at": "ISO 8601",
  "certified_at": "ISO 8601? — when operator was certified",
  "certification_level": "integer 0–4"
}
```

---

## Protocol Surfaces — Endpoint Map

These are the HTTP endpoints that must exist on a Federation Member (L3+) operator:

| Endpoint | Method | Required At | Purpose |
|----------|--------|-------------|---------|
| `/.well-known/banza/operator.json` | GET | L3 | Manifest — already required at L3 |
| `/.well-known/banza/certificate.json` | GET | L3 | Signed certification artifact (new) |
| `/federation/route` | POST | L3 | Accept cross-operator routing request (new) |
| `/federation/obligations` | GET | L3 | List outstanding cross-operator obligations (new) |
| `/federation/obligations/{id}` | GET | L3 | Get specific obligation (new) |
| `/federation/events` | POST/SSE | L3 | Receive/emit cross-operator events (new) |
| `/federation/net-position` | GET | L4 | Net settlement position per counterparty (new) |
| `/federation/settle` | POST | L4 | Initiate bilateral settlement (new) |

---

## Invariants for Federation

These invariants must hold across operator boundaries:

| Invariant | Definition |
|-----------|------------|
| **INV-FED-001** | A federation transaction MUST carry the same `trace_id` in both the originating and receiving operator |
| **INV-FED-002** | Every cross-operator payment MUST produce one `InteropObligation` in the originating operator |
| **INV-FED-003** | A federation member MUST NOT declare `supports_federation: true` unless it holds L3 certification |
| **INV-FED-004** | Cross-operator routing MUST be idempotent — same `routing_request_id` produces same result |
| **INV-FED-005** | No money may be created or destroyed in a federation transaction — INV-LEDGER-001 applies across federation boundaries |
| **INV-FED-006** | An operator certificate MUST expire — perpetual certification is forbidden |
| **INV-FED-007** | A revoked operator MUST be rejected from all routing decisions immediately |

---

## RFC Status for Federation Surfaces

| RFC | Surface | Status | ADR Required? |
|-----|---------|--------|---------------|
| RFC-0001 | Cross-operator routing | Draft | Yes — before implementation |
| RFC-0002 | Cross-operator settlement | Draft | Yes — before implementation |
| RFC-0003 | Wallet capabilities | Draft | No — already in use |
| RFC-0004 | Provider capability negotiation | Draft | No — already in use |
| RFC-0005 | Operator discovery | Draft | Yes — before signing implementation |
| RFC-0006 | Offline payment support | Draft | No — post-federation |
| — | Trust / PKI model | Not written | Yes — needed first |
| — | Federation event propagation | Not written | Yes |
| — | Federation conformance | Not written | Yes |
