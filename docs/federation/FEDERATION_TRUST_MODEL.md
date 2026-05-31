# BANZA Federation Trust Model

**Audit ID:** BANZA-FEDERATION-READINESS-AUDIT-001  
**Date:** 2026-05-31  
**Status:** Design document — no implementation

---

## Current State

**No federation trust model exists.**

RFC-0005 mentions cryptographic signing (`"public_key": "ed25519:base64..."`) in prose only. No code signs or verifies operator manifests. The `certification_level` field in the manifest is informational — not signed, not verified, not revocable.

---

## What a Federation Trust Model Requires

For Operator A to safely route a payment to Operator B, it needs to answer three questions:

1. **Is Operator B who they claim to be?** (Identity)
2. **Has Operator B been certified by BANZA?** (Certification attestation)
3. **Is Operator B still valid?** (Non-revocation)

None of these can be answered with the current infrastructure.

---

## Proposed Trust Architecture

### Trust Anchor

BANZA is the trust anchor. The chain of trust is:

```
BANZA (root — holds signing key)
  ↓ signs
Operator Certificate (issued to each certified operator)
  ↓ verified by
Federation Peers (when establishing routing relationships)
```

No operator is in the trust chain above another operator. All operators receive certificates directly from BANZA.

**Operator-neutrality note:** This model is consistent with the architectural invariant. BANZA is the trust authority. BanzAI verifies trust assertions. No operator controls another operator's trust status.

---

## Operator Certificate Specification

### What it is

A signed data structure issued by BANZA to a certified operator. Serves as proof of certification status within the federation.

### Minimum fields

```json
{
  "operator_id": "stable identifier, unique within BANZA network",
  "certification_level": 3,
  "protocol_version": "1.0",
  "issued_at": "2026-05-31T00:00:00Z",
  "expires_at": "2027-05-31T00:00:00Z",
  "issuer": "BANZA",
  "public_key": "ed25519:<base64>",
  "signature": "<BANZA signature over canonical JSON of above fields>"
}
```

### Key considerations

- **Algorithm:** ed25519 (fast verification, small key size)
- **Expiry:** 12-month maximum. Certification must be renewed annually.
- **Binding:** `operator_id` is bound to `public_key`. Operators cannot share keys.
- **Revocation:** BANZA maintains a revocation list. See below.

---

## Certificate Distribution

### How Operator B serves its certificate

Option A — Well-known endpoint:
```
GET /.well-known/banza/certificate.json
```
Returns the operator's current BANZA-issued certificate.

Option B — Embedded in manifest:
The operator manifest (`/.well-known/banza/operator.json`) includes a `certificate` field containing the signed artifact.

**Recommendation:** Option A. Separate endpoints keep manifests small and allow certificate rotation without manifest update.

---

## Revocation

### Why revocation is critical

An operator that loses certification (protocol violation, security breach, suspension) must be immediately excluded from federation routing. Operators cache manifests and certificates. Without revocation, a revoked operator continues to be trusted by cached state.

### Revocation model

**Option A — BANZA Revocation List (BRL):** A periodically published list of revoked operator_ids, signed by BANZA. All federation members fetch this list on a defined schedule (e.g., every 6 hours). Simple but introduces latency.

**Option B — OCSP-style real-time check:** Each operator makes a real-time query to a BANZA revocation endpoint before routing. Zero latency on revocation but adds runtime BANZA dependency.

**Option C — Short-lived certificates (no revocation list):** Certificates expire after 24–48 hours. No revocation needed — expired certificates are simply not refreshed for revoked operators. No centralized revocation list, but requires frequent BANZA interaction.

**Recommendation:** Option C (short-lived certificates) for the initial federation pilot. It avoids the complexity of a revocation infrastructure while preserving the invariant that revoked operators cannot route payments indefinitely.

---

## Trust Establishment Protocol

How Operator A establishes trust with Operator B before routing:

```
Step 1: Operator A fetches Operator B's manifest
  GET https://api.operator-b.example/.well-known/banza/operator.json

Step 2: Operator A fetches Operator B's certificate
  GET https://api.operator-b.example/.well-known/banza/certificate.json

Step 3: Operator A verifies the certificate signature
  ed25519_verify(BANZA_PUBLIC_KEY, certificate_canonical_json, certificate.signature)
  → If invalid: reject Operator B

Step 4: Operator A checks certificate expiry
  If certificate.expires_at < now: reject Operator B (certificate expired)

Step 5: Operator A checks certification level
  If certificate.certification_level < 3: reject (not a federation member)

Step 6: Operator A verifies capability compatibility
  manifest.capabilities.supports_federation == true
  manifest.capabilities.cross_operator_routing == true
  → If missing: reject

Step 7: Trust established — Operator A may route to Operator B
```

---

## Trust Verification in BanzAI

BanzAI's role in the trust model:

- **Evaluates** federation readiness by verifying all trust steps above
- **Reports** trust verification results to operators running BanzAI conformance checks
- **Does NOT issue** certificates (BANZA does)
- **Does NOT manage** the BANZA signing key (BANZA holds it)
- **Does NOT approve** federation membership (BANZA certification grants this)

This is consistent with the architectural invariant: BanzAI evaluates; BANZA authorizes.

---

## What is Required to Implement This Model

| Artifact | Owner | Status |
|----------|-------|--------|
| BANZA signing key (ed25519) | BANZA | Not yet generated |
| Operator certificate schema | BANZA (contracts/) | Missing — GAP-001 |
| Certificate issuance process | BANZA | Not defined |
| Certificate distribution endpoint | Operators | Not implemented |
| Manifest signing code | `banza-capabilities` crate | Not implemented |
| Signature verification code | `banza-capabilities` crate | Not implemented |
| Revocation policy | BANZA | Not defined |
| Certificate expiry conformance test | `conformance/federation/` | Missing |
| BanzAI trust verification tool | `~/banzai` | Not implemented |

---

## Open Questions (for ADR)

1. **Who holds the BANZA signing key?** Options: BANZA foundation, multi-sig, threshold signature scheme, decentralized PKI.

2. **How does certification translate to cryptographic evidence?** Does passing conformance automatically trigger certificate issuance, or is there a manual approval step?

3. **What is the minimum revocation latency the protocol will guarantee?** This determines whether Option A, B, or C is appropriate.

4. **Should operator certificates be public?** A public registry of certified operators enables discovery without a centralized directory.

5. **How does an operator rotate its public key?** Key rotation is inevitable — it must not require decertification.

These questions require an ADR before implementation can begin.
