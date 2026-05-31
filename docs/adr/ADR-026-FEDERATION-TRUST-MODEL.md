# ADR-026 — Federation Trust Model

**Status:** Accepted  
**Date:** 2026-05-31  
**Author:** BANZA Protocol  
**Deciders:** Fidel Monteiro (Founder)  
**Supersedes:** None  
**See also:** ADR-018, ADR-019, ADR-025, RFC-0001, RFC-0002, RFC-0005

---

## Context

BANZA-FEDERATION-READINESS-AUDIT-001 identified the federation trust layer as 0% complete and as the top blocker (GAP-001) for L3 Federation Certification. All cross-operator work — routing, settlement, conformance, and the federation certification path itself — depends on a prior decision about how operators prove their identity and certification status to one another.

Without a trust model:
- An operator serving a manifest at `/.well-known/banza/operator.json` cannot be distinguished from an adversary impersonating that operator
- The `certification_level` field in the manifest is informational only — not signed, not verified, not revocable
- No federation transaction can be initiated safely
- No federation conformance suite can be written (FED-001 requires a verifiable certificate)

This ADR makes the canonical trust architecture decision. All subsequent federation ADRs, contracts, and conformance vectors build on this foundation.

---

## Phase 1 — Precise Problem Definitions

### Operator Identity

**Operator identity** is the stable, unique string — the `operator_id` — that identifies a participant in the BANZA network at the protocol layer. It is not an IP address, a domain name, a brand, or a TLS certificate subject. It is assigned by BANZA at L0 certification and never changes for the lifetime of that operator's participation in the network.

Identity answers: *Who is this operator?*

### Operator Authenticity

**Operator authenticity** is cryptographic proof that the party presenting an `operator_id` genuinely controls the private key bound to that identifier by BANZA. Without authenticity, any entity can claim any `operator_id` by serving an unsigned manifest.

Authenticity answers: *Is this operator actually who it claims to be?*

### Operator Certification Proof

**Operator certification proof** is a signed artifact issued by BANZA attesting that a specific `operator_id` has passed protocol conformance at a specific level. This is distinct from identity and authenticity: an operator may be authentic (holds its own private key) but not yet certified (has never passed conformance).

Certification proof answers: *Has BANZA verified that this operator meets the protocol standard for the claimed level?*

### Operator Trust

**Operator trust** is the conjunction of identity + authenticity + certification proof + non-revocation. An operator is trusted by a peer when:

1. The peer can verify `operator_id` is bound to a known public key (authenticity)
2. The peer can verify that BANZA has signed a certificate for that `operator_id` at the required certification level (certification proof)
3. The peer can verify that the certificate has not been revoked or expired (non-revocation)

Trust is transitive through BANZA: if BANZA has certified Operator B, Operator A can trust Operator B without a prior bilateral relationship.

### Operator Suspension

**Operator suspension** is a temporary, reversible withdrawal of federation routing privileges. A suspended operator may hold a valid certificate but is listed in the BANZA Revocation List (BRL). Peers that fetch the BRL reject suspended operators from all routing decisions immediately. Suspension does not require re-certification to lift — BANZA removes the operator from the BRL upon reinstatement.

Suspension is a governance action. It does not imply protocol non-compliance; it may be triggered by regulatory, contractual, or operational events.

### Operator Revocation

**Operator revocation** is the permanent (or indefinite) withdrawal of an operator's certificate. A revoked operator must re-apply for certification and pass a full conformance run before rejoining the federation. Revocation is issued when protocol integrity has been violated or when the operator has become an active threat to the network.

### Why L0–L2 Work Without Federation Trust

Certification levels L0 (Sandbox Operator), L1 (Payment Operator), and L2 (Settlement Operator) operate entirely within a single operator's boundary:

- All transactions originate and complete on the same operator's infrastructure
- All ledger entries, wallets, and postings are local to one operator
- The operator already knows its own identity — there is no external party to verify
- No money crosses an operator boundary in any L0–L2 flow
- Conformance testing at L0–L2 runs against a single URL: `run_tests(operator_url)`

L0–L2 operators can be tested, certified, and fully operational without any PKI infrastructure. BANZA can issue L0–L2 certificates as administrative records without cryptographic signing machinery.

### Why L3 Cannot

L3 Federation requires Operator A to route a payment to Operator B — a financial transaction that crosses an operator boundary. Before committing the routing decision:

- Operator A must verify that Operator B is a real BANZA-certified operator, not an adversary
- The verification must be fast enough for routing decisions (not a blocking BANZA round-trip on every transaction)
- The stakes are financial: routing to a fraudulent endpoint means money is delivered to an adversary with no recovery path
- Manifest and certificate data is cached — trust must be verifiable offline, against BANZA's signing key, without real-time BANZA involvement in every payment

**No amount of documentation, protocol design, or conformance testing can substitute for cryptographic trust at the L3 boundary.** This is the irreducible requirement that separates L3 from all prior levels.

---

## Phase 2 — Trust Model Options

### Option A — Central Protocol Authority (CPA)

Every routing decision requires a real-time check against a BANZA-operated central authority service. Operator A sends the target `operator_id` to BANZA; BANZA responds with a trust assertion.

| Dimension | Assessment |
|-----------|------------|
| Security | Very high — BANZA has real-time control over every routing decision; revocation is instant |
| Scalability | Poor — BANZA becomes the bottleneck; every routing decision is a network round-trip to BANZA |
| Decentralization | None — all operators depend on BANZA's central service availability; federation stops if BANZA's service is unavailable |
| Operational complexity | Very high — BANZA must operate a high-availability, globally distributed, low-latency authority service; SLA is the federation SLA |
| Certification impact | Instant revocation; but re-certification must be coordinated with authority availability |

**Fatal flaw:** BANZA's authority service becomes the single point of failure for the entire federation. If it is unavailable, no operator can route any cross-operator payment. This is incompatible with financial infrastructure at scale.

### Option B — Protocol Root + Operator Certificates (PKI)

BANZA holds a root signing key. When an operator reaches a certification level, BANZA issues a signed operator certificate. Operators serve their certificates at a well-known endpoint. Peers verify certificates offline using BANZA's public key, which is distributed with the BANZA SDK and pinned in conformance vectors.

| Dimension | Assessment |
|-----------|------------|
| Security | High — cryptographic verification; offline verification is sound as long as BANZA's signing key is not compromised |
| Scalability | Excellent — certificate verification is O(1); no BANZA round-trip per routing decision |
| Decentralization | Good — BANZA involvement is limited to certificate issuance; routing and settlement operate independently of BANZA's real-time availability |
| Operational complexity | Moderate — BANZA manages signing key security; operators manage certificate lifecycle (renewal, distribution); revocation requires separate mechanism |
| Certification impact | Certificates bind certification level cryptographically; revocation can be fast (see BANZA Revocation List) or slow (certificate expiry only) depending on revocation model choice |

**This model is consistent with the BANZA authority architecture.** BANZA is the trust root. BanzAI verifies trust assertions. Operators present certificates. No operator is in the trust chain above another.

### Option C — Web-of-Trust Federation

Operators sign each other's keys based on mutual verification and peer endorsement. Trust accumulates through a graph of operator signatures. No central authority.

| Dimension | Assessment |
|-----------|------------|
| Security | Weak for financial infrastructure — trust is not transitively consistent; Sybil attacks (adversary controls multiple identities to gain endorsements) are viable; trust graph integrity is undefined |
| Scalability | Poor — trust graph verification grows with network size; resolving a trust path becomes a graph traversal problem |
| Decentralization | Maximum — no central authority |
| Operational complexity | Very high — operators must manage their own trust graphs; conflict resolution between operators is undefined; key revocation cascades through the graph unpredictably |
| Certification impact | No canonical certification semantics — "trust" means different things to different operators; impossible to define a protocol-wide certification standard |

**Rejected.** Web-of-trust provides no deterministic trust semantics and no binding to BANZA's certification standard. Financial infrastructure cannot tolerate trust ambiguity.

### Option D — Multi-Signature Federation Council

A council of N operators co-sign certification artifacts. Any M-of-N council signatures constitute a valid certification (M-of-N threshold signature). New operators are certified by council action, not BANZA unilaterally.

| Dimension | Assessment |
|-----------|------------|
| Security | Good for council key compromise resistance; M-of-N makes single-key compromise insufficient |
| Scalability | Moderate — council coordination is bounded by council size; adding operators requires council action |
| Decentralization | Partial — authority is distributed among council members, but council itself is a centralization vector; council membership is a governance problem |
| Operational complexity | High — multi-party key ceremony for council formation; coordination overhead for every certification decision; council rotation adds further complexity |
| Certification impact | Bootstrapping problem: who certifies the first council members? BANZA must bootstrap the council, which means BANZA is the de-facto root authority anyway |

**Rejected for initial implementation.** The bootstrapping problem forces BANZA to be the root authority regardless. The council layer adds complexity without eliminating centralization. It is a viable upgrade path after federation is established (see Consequences).

---

## Phase 3 — Authority Alignment

The BANZA dependency graph is:

```
       Operators
           ↑
         BanzAI
           ↑
         BANZA
```

This graph is permanent and non-negotiable (ADR-018, ADR-019, ADR-025). Any trust model must respect it.

**Option A (CPA):** Consistent with the authority model — BANZA controls all routing decisions. But it makes BANZA operationally mandatory in the hot path of every transaction, which exceeds BANZA's intended role as a protocol authority (not an operational dependency).

**Option B (PKI):** Consistent with the authority model — BANZA is the trust root (signing key), BanzAI is the evaluator (verification logic), operators are participants (certificate holders). BANZA's operational involvement is bounded to certificate issuance and revocation list publication — both are async, offline operations relative to the routing hot path.

**Option C (Web-of-Trust):** Violates the authority model — operators would be co-equal trust authorities. No canonical authority exists.

**Option D (Multi-Sig Council):** Partially violates the authority model — council member operators are elevated to a governance role that belongs to BANZA. Introduces a class of "authority operators," which the operator-neutrality principle (ADR-019, CLAUDE.md) explicitly forbids.

**Conclusion:** Option B is the only option that satisfies the BANZA authority architecture without operational compromise.

---

## Decision

**Selected architecture: Option B — Protocol Root + Operator Certificates (PKI)**

BANZA is the trust root. BANZA issues signed operator certificates. Certificates are verified offline by peers using BANZA's public key. A BANZA Revocation List (BRL) provides timely revocation without real-time BANZA involvement in the routing hot path.

---

## Phase 4 — Certificate Model

### Operator Certificate Fields

```json
{
  "schema_version": "1",
  "operator_id": "<stable string, unique in BANZA network>",
  "certification_level": 3,
  "protocol_version": "1.0",
  "capabilities": ["cross_operator_routing", "cross_operator_settlement"],
  "public_key": "ed25519:<base64url-encoded 32-byte public key>",
  "issued_at": "2026-05-31T00:00:00Z",
  "expires_at": "2026-08-29T00:00:00Z",
  "issuer": "BANZA",
  "issuer_key_id": "<BANZA signing key identifier>",
  "signature": "<ed25519 signature over canonical JSON of the above fields>"
}
```

**Field semantics:**

| Field | Description |
|-------|-------------|
| `schema_version` | Certificate schema version. Must be `"1"` for this certificate model. |
| `operator_id` | Stable, unique operator identifier assigned by BANZA at L0. Never reused, never changed. |
| `certification_level` | Integer 0–4. The certification level at time of issuance. |
| `protocol_version` | The BANZA protocol version this certification applies to. Certificates issued against older protocol versions are invalid for newer protocol features. |
| `capabilities` | The specific capabilities that have been conformance-tested and certified. An operator may declare capabilities in its manifest that are not yet certified — certified capabilities are those listed in the certificate. |
| `public_key` | The operator's ed25519 public key, base64url-encoded. Operators generate their own keypair. The public key is submitted to BANZA during certification and bound into the certificate by BANZA's signature. |
| `issued_at` | UTC timestamp of certificate issuance. |
| `expires_at` | UTC timestamp of certificate expiry. Maximum 90 days from `issued_at`. |
| `issuer` | Always the string `"BANZA"`. Any other value is invalid. |
| `issuer_key_id` | Identifier for the BANZA signing key used to produce this certificate. Enables key rotation without invalidating outstanding certificates. |
| `signature` | ed25519 signature by BANZA over the canonical JSON encoding of all other fields. The canonical form is the JSON object with fields sorted lexicographically, no whitespace. |

### Cryptographic Algorithm

**Algorithm: ed25519 (RFC 8032)**

Rationale:
- 32-byte public key, 64-byte signature — minimal overhead in certificate payloads
- Constant-time verification — important for the routing hot path where certificates are verified repeatedly
- No parameter selection vulnerability — unlike ECDSA, there is no curve choice or nonce management that could be misconfigured
- Widely implemented across all target languages (Rust: `ring`, `ed25519-dalek`; TypeScript: `@noble/curves`; Go: `crypto/ed25519`; Python: `cryptography`)
- Used in TLS 1.3, SSH, Signal Protocol, and Tor — battle-tested in adversarial environments

**BANZA signing key management:**
- BANZA holds one ed25519 root signing key per protocol version
- The private key is held offline (hardware security module or air-gapped signing environment)
- The corresponding public key is distributed with every BANZA SDK release and pinned in conformance vector files
- `issuer_key_id` allows BANZA to rotate its signing key without immediately invalidating all outstanding certificates

### Certificate Lifecycle

#### Issuance

1. Operator completes conformance run at the target level (L0–L4)
2. BanzAI certifies conformance results and submits to BANZA
3. BANZA reviews and approves the certification
4. BANZA signs the operator certificate and delivers it to the operator
5. Operator serves the certificate at `GET /.well-known/banza/certificate.json`

Certification does not automatically trigger certificate issuance — there is a mandatory human approval step at BANZA. BanzAI evaluates; BANZA authorizes.

#### Expiry

Certificates have a maximum lifetime of **90 days** for federation certificates (certification_level ≥ 3). This is intentional:

- Forces periodic re-verification of conformance (operators cannot be certified once and forgotten)
- Limits the blast radius of a key compromise — a stolen operator private key becomes useless after 90 days without BANZA re-issuance
- Short enough to make certificate rotation a routine operational concern rather than an exceptional event

L0–L2 administrative certificates may have longer lifetimes (up to 12 months) because they do not gate federation routing decisions.

#### Renewal

Operators renew certificates before expiry:

1. Operator submits renewal request to BANZA with its current valid certificate as proof of prior authorization
2. BANZA verifies that the operator has no open conformance failures or governance issues since the last issuance
3. If clean: BANZA issues a new certificate without requiring a full conformance re-run
4. If issues exist: BANZA requires a new conformance run before renewal

A full re-certification (complete conformance run) is required at most annually for all active federation operators.

#### Suspension

1. BANZA adds the `operator_id` to the BANZA Revocation List (BRL) with `reason: "suspended"`
2. Federation peers that fetch the BRL (every 6 hours) immediately stop routing to the suspended operator
3. The operator's certificate itself remains mathematically valid until expiry — but BRL check precedes certificate signature verification in the trust protocol
4. To lift suspension: BANZA removes the `operator_id` from the BRL; no certificate re-issuance required

#### Revocation

1. BANZA adds the `operator_id` to the BRL with `reason: "revoked"` and sets `permanent: true`
2. Federation peers reject the operator immediately upon BRL refresh
3. The operator's existing certificate is invalidated — BANZA adds the certificate's `issuer_key_id` + `operator_id` + `issued_at` tuple to the revoked certificates list
4. To rejoin: operator must re-certify from L0, including a full conformance run at each level

#### Key Rotation

Operators rotate their keypair without losing certification:

1. Operator generates a new ed25519 keypair
2. Operator submits the new public key to BANZA, authenticated by signing the request with the current private key (the one bound in the current certificate)
3. BANZA issues a new certificate binding the `operator_id` to the new public key; expiry is reset to 90 days
4. The old certificate remains valid until its original expiry or until the operator replaces it
5. Operators SHOULD rotate keys annually at minimum

Key rotation does not require a new conformance run.

### BANZA Revocation List (BRL)

**Format:**
```json
{
  "schema_version": "1",
  "issued_at": "<ISO 8601 UTC>",
  "expires_at": "<ISO 8601 UTC — must be fetched before this time>",
  "revoked": [
    {
      "operator_id": "<string>",
      "reason": "suspended | revoked",
      "permanent": false,
      "since": "<ISO 8601 UTC>"
    }
  ],
  "signature": "<BANZA ed25519 signature over canonical JSON of above>"
}
```

**Distribution:**
- Published at `https://banza.network/federation/revocation-list.json` (authoritative)
- Also embedded in each BANZA SDK release for offline use during development and testing
- Operators MUST fetch a fresh BRL at least every 6 hours
- Operators MUST NOT route to an operator appearing in a valid, non-expired BRL

**Revocation latency guarantee:**
- Maximum revocation propagation time: 6 hours (one BRL fetch cycle)
- Emergency revocation (security breach): BANZA can issue an emergency BRL with `expires_at` set to 1 hour, forcing accelerated refresh

---

## Phase 5 — Discovery and Trust Protocol

### How Operator A Verifies Operator B

The trust establishment protocol proceeds as follows. Every step is mandatory. Any failure terminates the trust establishment and prevents routing.

```
STEP 1 — Discover Operator B

  Operator A resolves operator_id → manifest URL via one of:
    (a) DNS TXT record: _banza.operator-b.example  →  "banza-manifest=<URL>"
    (b) Known manifest URL (pre-configured or from prior discovery)
    (c) BANZA Federation Registry (future — RFC-0010)

  Input:  operator_id (string)
  Output: manifest URL

STEP 2 — Fetch and parse manifest

  GET <manifest_url>/.well-known/banza/operator.json
  → Validate schema against conformance/manifests/schema.json
  → Verify manifest.operator_id == expected operator_id

  On failure: reject. Operator B is not reachable or manifest is invalid.

STEP 3 — Fetch operator certificate

  GET <manifest_url>/.well-known/banza/certificate.json
  → Validate schema against contracts/federation/operator-certificate.json

  On failure: reject. Operator B is not a federation member.

STEP 4 — Verify certificate signature

  Load BANZA_PUBLIC_KEY (from BANZA SDK or pinned in conformance suite)
  Compute canonical_json(certificate — all fields except "signature")
  Verify: ed25519_verify(BANZA_PUBLIC_KEY, canonical_json, certificate.signature)

  On failure: reject. Certificate was not issued by BANZA or has been tampered with.

STEP 5 — Verify certificate expiry

  if certificate.expires_at < now(): reject
  if certificate.issued_at > now(): reject  (clock skew / future-dated certificate)

  On failure: reject. Certificate is expired or invalid.

STEP 6 — Verify certification level

  if certificate.certification_level < REQUIRED_LEVEL: reject

  For federation routing: REQUIRED_LEVEL = 3

  On failure: reject. Operator B is not certified for federation.

STEP 7 — Check BANZA Revocation List

  Load current BRL (cached, max 6 hours old, BRL signature verified)
  if certificate.operator_id in BRL.revoked: reject
  if BRL.expires_at < now(): reject (stale BRL — must fetch fresh)

  On failure: reject. Operator B is suspended or revoked.

STEP 8 — Verify federation capabilities

  manifest.capabilities.supports_federation == true
  manifest.capabilities.cross_operator_routing == true

  On failure: reject. Operator B has not declared federation capability.

STEP 9 — Bind certificate to manifest

  certificate.operator_id == manifest.operator_id

  On failure: reject. Certificate and manifest describe different operators.

→ TRUST ESTABLISHED
  Operator A may route payments to Operator B.
  Trust result is cacheable for min(certificate.expires_at, BRL.expires_at) - now().
```

### Trust Without Operator Branding

The trust protocol references no operator brand, no commercial name, and no human-readable description. Trust is based entirely on:
- `operator_id` — protocol-level identifier
- `public_key` — cryptographic binding
- `certification_level` — protocol compliance attestation
- `signature` — BANZA cryptographic proof

An operator can be trusted or rejected purely from its certificate and a copy of BANZA's public key. No external knowledge about who the operator is, what it is called, or who owns it is required.

---

## Phase 6 — L3 Federation Certification Requirements

For Operator A ↔ Operator B to achieve L3 Federation Certification, both operators must independently satisfy the following, and must together demonstrate cross-operator interoperability.

### Per-Operator Requirements (each operator independently)

| ID | Requirement | Evidence |
|----|-------------|----------|
| FED-L3-001 | Valid BANZA-issued certificate at `certification_level >= 3` | Certificate signature verifies against BANZA public key |
| FED-L3-002 | Certificate not expired | `certificate.expires_at > now()` at test time |
| FED-L3-003 | Certificate served at `/.well-known/banza/certificate.json` | HTTP 200 with valid schema |
| FED-L3-004 | Manifest declares `supports_federation: true` and `cross_operator_routing: true` | Manifest conformance vector CAP-FED-001 |
| FED-L3-005 | `certificate.operator_id` matches `manifest.operator_id` | Step 9 of trust protocol |
| FED-L3-006 | Operator not present in current BRL | BRL check passes |
| FED-L3-007 | `POST /federation/route` endpoint is available and returns valid response | Routing conformance vector FED-004 |
| FED-L3-008 | `GET /federation/obligations` endpoint is available | Settlement conformance vector FED-005 |

### Cross-Operator Requirements (both operators together)

| ID | Requirement | Evidence |
|----|-------------|----------|
| FED-L3-009 | Operator A can successfully complete trust establishment for Operator B (Steps 1–9) | Trust protocol vector FED-002 |
| FED-L3-010 | Operator B can successfully complete trust establishment for Operator A (Steps 1–9) | Trust protocol vector FED-002 (reversed) |
| FED-L3-011 | Cross-operator payment completes: Operator A ledger DEBIT, Operator B ledger CREDIT | End-to-end vector FED-006 |
| FED-L3-012 | `trace_id` is identical in both operators' artifacts for the same cross-operator payment | INV-FED-001 |
| FED-L3-013 | Obligation is recorded in Operator A upon routing acceptance | INV-FED-002 |
| FED-L3-014 | No money created or destroyed: sum of all BANZA-network entries is zero | INV-FED-005 (cross-operator extension of INV-LEDGER-001) |

---

## Phase 7 — Consequences

### Positive

**Protocol authority is preserved.** BANZA is the sole issuer of certificates. No operator can self-certify or certify another operator.

**Operator neutrality is preserved.** All operators are equal peers. No operator is in the trust chain above another. The trust path is always: BANZA → certificate → operator.

**Federation scales independently of BANZA's runtime.** Certificate verification is a fast offline cryptographic operation. Routing decisions do not require BANZA's real-time availability.

**Revocation is fast enough for financial infrastructure.** The 6-hour BRL refresh cycle limits the maximum time a revoked operator can remain trusted by caching peers. Emergency BRL issuance can reduce this to 1 hour.

**Key rotation is safe.** Operators can rotate their keypair without re-certification. `issuer_key_id` allows BANZA to rotate its own signing key without invalidating outstanding certificates.

**The trust model is operator-count invariant.** Adding the 100th operator to the federation is identical in complexity to adding the 2nd. There is no scaling cliff.

### Negative (managed)

**BANZA must operate a signing infrastructure.** The BANZA root signing key must be held securely (HSM or air-gapped signing ceremony). This is a permanent operational responsibility.

**Certificate renewal adds operational overhead for operators.** Operators must renew certificates before 90-day expiry. This is a feature (forces conformance continuity) but requires operational tooling and monitoring.

**BRL distribution is a new BANZA-operated service.** `https://banza.network/federation/revocation-list.json` must be available. Its availability does not block routing (cached BRL can be used) but a stale BRL that cannot be refreshed creates a maximum-6-hour window of uncertainty.

**Maximum revocation latency is 6 hours.** An operator that is compromised at 00:00 may continue to receive cross-operator payments until 06:00 if peers have not yet refreshed their BRL. This is acceptable for the initial federation pilot; emergency BRL issuance mitigates the worst cases.

### Migration Implications

**Impact on existing L0–L2 operators:** None. L0–L2 certification does not require certificates or BRL participation. Existing operators continue without change.

**Impact on conformance suite:** Significant. The federation conformance suite (GAP-005) must be written against this trust model. All federation vectors (FED-001 through FED-006) depend on the certificate model defined here.

**Impact on RFC-0005 (Operator Discovery):** RFC-0005 must be updated to reflect that certificate verification (Steps 4–9 of the trust protocol) is mandatory before a discovered operator can be trusted, not optional.

**Impact on BanzAI:** BanzAI must implement the trust protocol (Steps 1–9) as part of its Federation Intelligence module. BanzAI verifies; it does not issue certificates.

**Path to Multi-Signature Authority (future):** Option D (Multi-Sig Council) is a viable upgrade path once the federation has a stable set of participating operators. BANZA's root signing key could be replaced with an M-of-N threshold signature scheme operated by BANZA and N long-standing certified operators. This upgrade does not invalidate the certificate format — only the `issuer` and `issuer_key_id` semantics would change. Any such upgrade requires a separate ADR.

---

## Phase 8 — Selected Architecture Rationale

> **What trust architecture best preserves protocol authority, operator neutrality, federation scalability, and certification integrity while avoiding centralization?**

**Answer: Option B — Protocol Root + Operator Certificates with a hybrid revocation model.**

The hybrid revocation model is: 90-day maximum certificate lifetime (short enough to function as a soft revocation ceiling without a BRL), combined with a 6-hour BRL for explicit and timely revocation.

This architecture satisfies every constraint:

| Constraint | How Option B Satisfies It |
|------------|---------------------------|
| Protocol authority | BANZA holds the root signing key; no certificate is valid without BANZA's signature |
| Operator neutrality | All operators receive the same certificate format; no operator is in another operator's trust chain |
| Federation scalability | Certificate verification is O(1) and offline; adding operators has no scaling cost |
| Certification integrity | The certificate cryptographically binds operator_id, public key, and certification level; forgery requires compromising BANZA's signing key |
| Avoids centralization | Routing and settlement do not require BANZA's real-time availability; BANZA's role is bounded to certificate issuance and BRL publication |

Option A was rejected because BANZA-in-the-hot-path is a centralization failure mode incompatible with financial infrastructure at scale.

Options C and D were rejected because they violate the operator-neutrality principle or introduce irresolvable governance bootstrapping problems.

---

## Artifacts Required

This ADR authorizes the following artifacts. They do not yet exist and must be produced before L3 Federation Certification is certifiable.

| Artifact | Type | Owner | Blocks |
|----------|------|-------|--------|
| `contracts/federation/operator-certificate.json` | JSON Schema | BANZA | FED-L3-001, FED-002 |
| `contracts/federation/federation-trust.json` | Protocol Spec | BANZA | FED-002, routing implementation |
| BANZA root signing key (ed25519) | Key material | BANZA | All certificate issuance |
| BRL endpoint `banza.network/federation/revocation-list.json` | Operated service | BANZA | FED-L3-006 |
| `contracts/federation/revocation-list.json` | JSON Schema | BANZA | BRL implementation |
| Manifest signing implementation | Rust — `banza-capabilities` | BANZA | GAP-008, MAN-005 |
| Certificate verification implementation | Rust — `banza-capabilities` | BANZA | Trust protocol, conformance suite |
| BRL fetch + cache implementation | Rust — `banza-capabilities` | BANZA | Step 7 of trust protocol |
| `conformance/vectors/federation-trust.json` | Conformance vectors | BANZA | FED-001, FED-002 |
| BanzAI trust verification module | BanzAI | BanzAI | Federation Intelligence capability |

---

## Protocol Invariants (Federation Trust Layer)

These invariants are added to the BANZA protocol invariant registry:

| ID | Invariant |
|----|-----------|
| **INV-TRUST-001** | A certificate is valid if and only if its `signature` field verifies against the BANZA root public key for the corresponding `issuer_key_id`. |
| **INV-TRUST-002** | A certificate MUST NOT be accepted after its `expires_at` timestamp. No grace period is permitted. |
| **INV-TRUST-003** | An operator whose `operator_id` appears in a valid, non-expired BRL MUST be rejected from all routing decisions, regardless of certificate validity. |
| **INV-TRUST-004** | An operator MUST NOT declare `supports_federation: true` in its manifest unless it holds a valid, non-expired, non-revoked certificate at `certification_level >= 3`. |
| **INV-TRUST-005** | A BRL MUST be signed by BANZA. An unsigned or unverifiable BRL MUST be rejected as if it were expired. |
| **INV-TRUST-006** | A routing decision MUST NOT be made against a BRL older than 6 hours. |
| **INV-TRUST-007** | Key rotation MUST be performed by signing the rotation request with the currently-bound private key. A key rotation authenticated by any other means is invalid. |

---

## Related ADRs

- **ADR-018** — Open Financial Kernel: establishes BANZA's role as protocol authority
- **ADR-019** — Operator Separation: establishes operator-neutrality principle
- **ADR-025** — Ecosystem Naming Inversion: canonical ecosystem identity terminology
- **ADR-027** (pending) — Federation Wire Protocol: inter-operator HTTP protocol and request authentication
- **ADR-028** (pending) — Certification Level Revision: L3 → Federation Operator, L4 → Infrastructure Operator
