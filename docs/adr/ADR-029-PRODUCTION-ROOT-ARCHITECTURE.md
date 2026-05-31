# ADR-029 — BANZA Production Root Architecture

**Status:** Accepted  
**Date:** 2026-05-31  
**Author:** BANZA Protocol  
**Deciders:** Fidel Monteiro (Founder)  
**Supersedes:** None  
**Extends:** ADR-026 (Federation Trust Model)  
**See also:** ADR-018, ADR-019, ADR-025, ADR-026, ADR-028

---

## Context

ADR-026 selected Option B (Protocol Root + Operator Certificates / PKI) as the canonical trust architecture. It specified that:

- BANZA holds an ed25519 root signing key
- Certificates are verified offline using BANZA's public key
- The private key is "held offline (hardware security module or air-gapped signing environment)"
- `issuer_key_id` enables key rotation
- BRLs are signed by BANZA

ADR-026 deferred the precise key hierarchy, key lifecycle procedures, compromise recovery, and publication model to a subsequent ADR. This is that ADR.

The current state of the protocol is:

- `tools/banza-conformance/trust_root.py` generates an **ephemeral** ed25519 keypair per runner invocation
- `key_id` is `test-banza-key-YYYY-MM` — a test-only, per-month string
- The public key is known only within a single test run — it is never published, never pinned, never stable
- Certificate, BRL, and evidence signatures use the same ephemeral keypair
- No key manifest publication endpoint exists
- No offline signing ceremony is defined
- No compromise recovery procedures exist

This state is correct and sufficient for L3 conformance testing. It is a production blocker for certificate issuance.

This ADR freezes the production root architecture. All future operator certification, federation trust, and BRL distribution depends on it.

---

## Phase 1 — Precise Problem Statement

### What ADR-026 Decided

ADR-026 decided **what** signs what:

- BANZA root key signs operator certificates
- BANZA root key signs BRLs
- `issuer_key_id` binds signatures to specific key versions

### What ADR-026 Left Open

ADR-026 did not decide:

1. Whether BANZA uses a single key or a hierarchy of keys
2. Which key is used for which artifact type
3. How the root key is stored and protected
4. How issuing keys are activated, rotated, and retired
5. What format the `issuer_key_id` takes
6. How the BANZA public key is distributed to operators and SDK users
7. What happens if the root key is compromised
8. How BanzAI interacts with the trust infrastructure without becoming a trust authority

These are the decisions this ADR makes.

---

## Phase 2 — What BANZA Root Is

### Authority Boundaries

The BANZA ecosystem has four layers:

```
Operators
    ↑
  BanzAI
    ↑
  BANZA
```

Within BANZA, trust authority is further divided:

| Layer | Role | What it does |
|-------|------|--------------|
| **BANZA Root** | Offline trust anchor | Signs key manifests. Never signs certificates, BRLs, or evidence directly. |
| **BANZA Issuing Keys** | Online signing agents | Sign operator certificates, BRLs, and evidence packages by domain. |
| **BANZA Certification Authority** | Human-gated process | Reviews conformance results, approves certificates. Operates the certification issuing key. |
| **BanzAI** | Evaluator | Verifies trust, runs conformance, generates evidence. NEVER signs production artifacts. |
| **Operators** | Participants | Hold their own keypairs, present certificates issued by BANZA. |

### What the Root Signs

The BANZA Root key signs **exactly one thing**: the BANZA Key Manifest.

The Key Manifest lists all active issuing keys with their domains and validity periods. The root signature on the Key Manifest is the sole basis for trusting any issuing key. An issuing key that does not appear in a valid, root-signed Key Manifest is not a BANZA key.

The root NEVER signs operator certificates, BRLs, or evidence packages directly. This is intentional: if the root key signed routine artifacts, it would need to be present in online systems. Keeping the root offline protects it.

### What the Root Is NOT

The root is not:
- A web server or an accessible online service
- The key used to sign individual operator certificates
- A component of BanzAI
- Operated by any operator (including the reference operator)
- The key embedded in individual certificates as the verifying key

---

## Phase 3 — Key Hierarchy

### Evaluated Options

#### Option A — Single Root Key

One key signs all artifacts: certificates, BRLs, evidence.

| Dimension | Assessment |
|-----------|------------|
| Operational simplicity | High — one key to manage |
| Security | Poor — root must be online for routine certificate issuance; root compromise = total trust collapse with no recovery path |
| Blast radius | Total — single key compromise invalidates all outstanding certificates, all BRLs |
| Rotation complexity | High — rotating the root requires re-issuing all outstanding certificates and updating all SDK pins |

**Rejected.** A key that signs routine artifacts cannot remain offline. An online root is indefensible.

#### Option B — Root + Issuing Keys (Selected)

Root key is offline. Issuing keys are online. Root signs the Key Manifest, which endorses issuing keys. Issuing keys sign the actual protocol artifacts (certificates, BRLs, evidence).

| Dimension | Assessment |
|-----------|------------|
| Operational simplicity | Moderate — two tiers; root ceremonies are rare (key manifest rotation only) |
| Security | High — root stays offline permanently; issuing key compromise does not require root key usage to recover |
| Blast radius | Bounded by domain — issuing key compromise affects only certificates, BRLs, or evidence (depending on which key is compromised), not all three |
| Rotation complexity | Low — rotate issuing key, publish new key manifest (root ceremony), SDK update optional until old issuing key expires |

**Selected.** This is the standard model for financial PKI. The root's role is limited to key endorsement; it is never exposed in the runtime verification path.

#### Option C — Root + Intermediate CA

Full X.509-style three-tier hierarchy: root signs intermediate CA certificate; intermediate CA certificate is embedded in issued certificates; peers verify the chain.

| Dimension | Assessment |
|-----------|------------|
| Protocol compatibility | Poor — the current operator certificate schema (`contracts/federation/operator-certificate.json`) contains no chain field; adding one is a breaking contract change |
| Complexity | High — certificate chain verification logic in every SDK, in the conformance runner, and in the fixture server |
| Benefit over Option B | Marginal — intermediate key rotation is equivalent to issuing key rotation in Option B without the chain embedding |

**Rejected.** No benefit justifies a breaking change to the certificate schema. Option B achieves the same separation with a simpler verification path.

#### Option D — Root + Multiple Domain-Specific Keys (Combined with B)

This is Option B extended: each issuing key is specific to one domain (certification, revocation, conformance-evidence). This is the selected sub-variant within Option B.

**Adopted as part of Option B.** Domain separation limits the blast radius of an issuing key compromise to that key's domain.

### Selected Architecture

```
BANZA Root Key
  (offline — HSM or air-gapped)
  (maximum validity: 24 months)
  (signs Key Manifests only)
         │
         ▼
  BANZA Key Manifest
  (published at banza.network)
  (signed by root)
  (contains all active issuing public keys)
         │
    ┌────┴──────────────────────────────┐
    │                                   │
    ▼                                   ▼
BANZA Cert-Issuing Key          BANZA BRL-Issuing Key
  (online in BANZA                (online in BANZA
   certification system)           revocation system)
  (domain: certification)         (domain: revocation)
  (max validity: 6 months)        (max validity: 6 months)
  (signs: operator certificates)  (signs: BRLs)
                │
                ▼
      BANZA Conformance Key
        (online in conformance
         runner infrastructure)
        (domain: conformance-evidence)
        (max validity: 6 months)
        (signs: evidence packages)
```

### Why Three Issuing Domains

| Domain | Key | Compromise blast radius |
|--------|-----|------------------------|
| `certification` | Cert-Issuing Key | Attacker can issue fake operator certificates for new operators. Existing operators are unaffected. Emergency response: publish new cert-issuing key + add all potentially-affected operators to BRL pending re-verification. |
| `revocation` | BRL-Issuing Key | Attacker can publish a fake BRL — either adding operators (causing a federation disruption) or removing operators (allowing revoked operators to appear valid). Emergency response: publish new BRL-issuing key + publish an empty BRL with the new key to flush stale BRLs. |
| `conformance-evidence` | Conformance Key | Attacker can fabricate conformance evidence. No direct impact on live federation trust (evidence is reviewed by BANZA humans). Emergency response: invalidate all evidence packages from the compromised key's validity period. |

Separating these three domains means an attacker who compromises the conformance infrastructure cannot forge operator certificates or fake BRLs.

---

## Phase 4 — `issuer_key_id` Convention

### Production Key IDs

| Key | Format | Example |
|-----|--------|---------|
| Root key | `banza-root-YYYY` | `banza-root-2026` |
| Cert-issuing key | `banza-cert-YYYYMM` | `banza-cert-202608` |
| BRL-issuing key | `banza-brl-YYYYMM` | `banza-brl-202608` |
| Conformance key | `banza-evidence-YYYYMM` | `banza-evidence-202608` |

`YYYYMM` is the UTC activation month (when the key first became active). It is not the creation month or the rotation-trigger month.

### Test Key IDs

The existing test convention is retained:

```
test-banza-key-YYYY-MM
```

where `YYYY-MM` is the current UTC month at runner invocation time. This convention is already established in `trust_root.py` and all conformance fixtures. **It must never appear in a production Key Manifest.** Any `issuer_key_id` beginning with `test-` MUST be rejected by production certificate verification.

### Invariant: INV-ROOT-001

> A certificate, BRL, or evidence package whose `issuer_key_id` begins with `test-` MUST NOT be accepted as production-valid. The `test-` prefix identifies conformance-only keys.

---

## Phase 5 — Key Lifecycle

### Root Key

| Phase | Procedure |
|-------|-----------|
| **Creation** | Offline ceremony. Air-gapped environment. Ed25519 key generation using `ring` or `ed25519-dalek`. Private key bytes split across 2 HSM modules (different physical locations). Paper backup in sealed, dated, tamper-evident envelope. Public key bytes published in initial Key Manifest. |
| **Activation** | Upon creation. Key Manifest published. SDK releases pinned to new Key Manifest. |
| **Maximum validity** | 24 months from activation. |
| **Rotation trigger** | Expiry approaching (30 days before expiry) or compromise. |
| **Rotation procedure** | New root key generated in offline ceremony. New Key Manifest signed by NEW root key. Old root key endorses new root via transition manifest (signed by old root, listing new root as successor). SDK update required to pin new Key Manifest. |
| **Retirement** | After all issuing keys signed by the old root have expired. Old root public key retained in archive manifest for historical verification. |

### Issuing Keys (Cert, BRL, Conformance)

| Phase | Procedure |
|-------|-----------|
| **Creation** | Controlled environment. Ed25519 key generated. Private key stored in BANZA's HSM (for cert and BRL keys) or in secure environment (for conformance key). Public key submitted for root ceremony. |
| **Activation** | Root ceremony: root key signs updated Key Manifest including the new issuing key's public key with `status: "active"`. Key Manifest published. |
| **Maximum validity** | 6 months from activation date. |
| **Routine rotation** | Every 6 months. New key activated; old key remains in Key Manifest with `status: "retiring"` until all artifacts signed by it expire. |
| **Retirement** | After all artifacts signed by the retiring key have expired. Key removed from Key Manifest in next root ceremony. |
| **Emergency rotation** | See Phase 7 (Compromise Recovery). |

### Key Manifest Rotation Schedule

| Event | Trigger | Root key used? |
|-------|---------|----------------|
| Issuing key activation | Every 6 months (routine) | Yes |
| Issuing key retirement | After old issuing key artifacts expire | Yes |
| Root key rotation | Every 24 months or on compromise | Old root (or OOBC for compromise) |
| Emergency BRL response | Issuing key compromise | Yes |

Root ceremonies require physical presence of keyholders. They are scheduled events, not ad-hoc.

---

## Phase 6 — Key Manifest Format

The Key Manifest is the trust anchor distribution mechanism. It replaces "distributing the root public key" — SDK users and conformance runners verify issuing keys via the manifest, not via the root key directly.

### Structure

```json
{
  "schema_version": "1",
  "published_at": "2026-08-01T00:00:00Z",
  "root_key_id": "banza-root-2026",
  "expires_at": "2026-11-01T00:00:00Z",
  "keys": [
    {
      "key_id": "banza-cert-202608",
      "public_key": "ed25519:<base64url>",
      "domain": "certification",
      "active_since": "2026-08-01T00:00:00Z",
      "expires_at": "2027-02-01T00:00:00Z",
      "status": "active"
    },
    {
      "key_id": "banza-brl-202608",
      "public_key": "ed25519:<base64url>",
      "domain": "revocation",
      "active_since": "2026-08-01T00:00:00Z",
      "expires_at": "2027-02-01T00:00:00Z",
      "status": "active"
    },
    {
      "key_id": "banza-evidence-202608",
      "public_key": "ed25519:<base64url>",
      "domain": "conformance-evidence",
      "active_since": "2026-08-01T00:00:00Z",
      "expires_at": "2027-02-01T00:00:00Z",
      "status": "active"
    }
  ],
  "manifest_signature": "<ed25519 by banza-root-2026 over canonical JSON of all other fields>"
}
```

### Signing Rule

Identical to the ADR-026 canonical signing rule:
- Payload: all fields except `manifest_signature`, sorted lexicographically
- Encoding: `json.dumps(payload, sort_keys=True, separators=(',',':')).encode('utf-8')`
- Signature: ed25519 by the root key, base64url no padding

### Publication Endpoints

| Endpoint | Contents | Cache TTL |
|----------|----------|-----------|
| `https://banza.network/.well-known/banza/key-manifest.json` | Current active Key Manifest | 24 hours |
| `https://banza.network/.well-known/banza/key-archive.json` | Historical Key Manifests (for verifying old artifacts) | immutable per manifest version |
| BANZA SDK (bundled) | Current Key Manifest at SDK release time | Until SDK update |
| BANZA conformance runner | Key Manifest pinned at conformance suite release | Until conformance suite update |

### Key Manifest Verification Protocol

Before using any key from the Key Manifest:

1. Fetch key manifest
2. Verify `manifest_signature` against the root public key (pinned in SDK)
3. Verify `expires_at > now()` (stale manifest = reject)
4. Look up `issuer_key_id` in manifest `keys` array
5. Verify the key's `status == "active"` and `expires_at > now()`
6. Use the key's `public_key` for signature verification

If the `issuer_key_id` is not found in the current manifest, attempt `key-archive.json`. If not found there either, reject the artifact.

### Distribution and Pinning

| Distribution channel | Usage | Update mechanism |
|---------------------|-------|-----------------|
| SDK embedded | Offline verification, development | SDK release update |
| Conformance runner embedded | Test mode | Conformance suite update |
| HTTPS endpoint | Online verification, production operators | HTTP fetch with 24h cache |

An operator MAY operate with only the SDK-pinned manifest. They SHOULD fetch the live endpoint to pick up issuing key rotations within 24 hours.

---

## Phase 7 — Signing Authority Matrix

All protocol artifacts, their authorized signers, and their verification paths:

| Artifact | Signed by | Key domain | `issuer_key_id` format | Verified by | Verification key source |
|----------|-----------|-----------|----------------------|-------------|------------------------|
| Operator certificate | Cert-Issuing Key | `certification` | `banza-cert-YYYYMM` | Peer operators, conformance runner | Key Manifest (issuing pubkey) |
| BANZA Revocation List | BRL-Issuing Key | `revocation` | `banza-brl-YYYYMM` | Peer operators, conformance runner | Key Manifest (issuing pubkey) |
| Conformance evidence package | Conformance Key | `conformance-evidence` | `banza-evidence-YYYYMM` | BANZA certification review | Key Manifest (issuing pubkey) |
| BANZA Key Manifest | Root Key | `root` | `banza-root-YYYY` | SDK consumers, manifest verifiers | Root public key (SDK-pinned) |
| Future: operator key rotation request | Operator (own current key) | operator | operator-specific | BANZA | Operator's certificate public key |

### What is NEVER signed by the root key directly

- Operator certificates
- BRLs
- Evidence packages
- Webhook events
- API responses

The root key touches the Key Manifest only. Everything else is an issuing key.

### What BanzAI may sign

- Evidence packages generated by the BANZA conformance runner infrastructure (using the conformance issuing key, under BANZA's infrastructure)

### What BanzAI may NEVER sign

- Operator certificates (requires human BANZA review)
- BRLs (requires BANZA governance process)
- Key Manifests (requires root key)
- Operator identity binding

---

## Phase 8 — Compromise Recovery

### Scenario A — Conformance Key Compromise

**Impact:** Attacker can fabricate conformance evidence packages. No impact on live federation trust.

**Response:**
1. Rotate conformance key immediately (offline root ceremony for new key manifest)
2. Publish updated Key Manifest removing the compromised key
3. All future evidence packages use the new conformance key
4. BANZA certification review board invalidates all evidence packages signed by the compromised key's `issuer_key_id` from its activation date forward
5. Operators whose evidence was signed during the compromised period must re-run conformance

**Recovery time:** Hours (key manifest publication) + operator re-run lead time.

---

### Scenario B — BRL-Issuing Key Compromise

**Impact:** Attacker can publish a fake BRL — adding or removing operators from the revoked list.

**Response:**
1. **Immediate:** Rotate BRL-issuing key (offline root ceremony)
2. Publish updated Key Manifest removing the compromised key
3. **Emergency BRL:** Publish an authoritative empty BRL (or full-state BRL) signed with the new key immediately
4. Operators MUST flush their BRL cache and fetch the new signed BRL (emergency BRL sets `expires_at` to 1 hour to force rapid refresh per ADR-026 §emergency revocation)
5. Audit the compromised period: determine if any fake BRL entries were served and to which operators

**Recovery time:** 1–6 hours (emergency BRL forces refresh cycle).

---

### Scenario C — Cert-Issuing Key Compromise

**Impact:** Attacker can issue fraudulent operator certificates binding arbitrary operator IDs to attacker-controlled public keys.

**Response:**
1. **Immediate:** Rotate cert-issuing key (offline root ceremony)
2. Publish updated Key Manifest removing the compromised key
3. **Emergency BRL:** Add all operator IDs for which fraudulent certificates may have been issued to the BRL as `reason: "suspended"` pending re-verification
4. BANZA contacts all operators certified during the compromised period for re-verification
5. Operators who re-verify with valid conformance receive new certificates signed by the new cert-issuing key
6. After re-verification: remove legitimate operators from BRL

**Recovery time:** Days (re-certification is human-gated). Federation is disrupted for operators in the BRL during re-verification.

---

### Scenario D — Root Key Compromise

**Impact:** Total trust collapse. Attacker can issue fake Key Manifests endorsing any key, breaking all offline trust verification.

**Response:**

This is the catastrophic scenario. The recovery procedure is:

1. **Immediate public disclosure:** BANZA publicly announces root key compromise through all channels (status page, SDK changelog, operator notification, security advisories)
2. **Root key revocation:** Publish a `BANZA_ROOT_REVOCATION_NOTICE.json` at `https://banza.network/.well-known/banza/root-revocation.json` signed by the known-good root key (if accessible) **AND** via out-of-band channels (signed git tag in the BANZA public repository, signed announcement in BANZA governance channels)
3. **New root ceremony:** Generate new root key in offline environment with new witnesses
4. **New Key Manifest:** Publish new Key Manifest signed by new root. This is the new trust anchor.
5. **SDK emergency update:** All BANZA SDK versions must be updated with the new root public key pinned. Operators using old SDK versions cannot verify certificates until they update.
6. **Full re-certification:** ALL L3+ operators must re-obtain operator certificates from BANZA after the new root is established. Existing certificates are mathematically invalid (signed by a compromised root's issuing chain).
7. **Incident disclosure:** Full post-mortem published within 72 hours

**Recovery time:** Days to weeks (SDK distribution + operator re-certification).

**Prevention:** Root key never touches online systems. Root key ceremony requires 2+ keyholders present. Key material is split across 2 HSM modules in different physical locations.

---

### Recovery Decision Matrix

| Compromised artifact | Rotate key | Emergency BRL | Operator re-cert required | SDK update required | Recovery time |
|---------------------|-----------|---------------|--------------------------|---------------------|---------------|
| Conformance key | Yes | No | Partial (re-run only) | No | Hours |
| BRL-issuing key | Yes | Yes (empty BRL) | No | No | 1–6 hours |
| Cert-issuing key | Yes | Yes (suspend affected) | Yes (affected operators) | No | Days |
| Root key | Yes | Implicit (full reset) | Yes (ALL L3+) | Yes (all SDK versions) | Days–weeks |

---

## Phase 9 — BanzAI Authority Boundaries

BanzAI is the Protocol Operating System. Its role in the trust architecture is:

### BanzAI MAY

- Verify operator certificates using the published issuing public key
- Execute the trust protocol (Steps 1–9 of ADR-026 §Phase 5)
- Fetch and verify BRLs (verify signature, check expiry, check revocation status)
- Run the BANZA conformance suite and generate evidence packages (using the conformance issuing key, in BANZA's conformance infrastructure)
- Evaluate operator readiness and simulate the L3 trust path
- Report trust verification results to human reviewers

### BanzAI MAY NOT

- Hold any production BANZA issuing private key
- Issue, sign, or approve operator certificates
- Publish a BANZA Revocation List
- Modify the Key Manifest
- Make certification decisions (BanzAI evaluates; BANZA authorizes)
- Become a trust authority for any operator under any circumstance

This boundary is permanent. It follows directly from the BANZA dependency graph (ADR-018, ADR-019):

```
Operators
    ↑
  BanzAI    ← verifies trust, does not grant it
    ↑
  BANZA     ← sole trust authority
```

BanzAI is a protocol consumer of trust. It is not a trust issuer.

---

## Decisions

| ID | Decision |
|----|----------|
| **D-001** | Key hierarchy is Root + Domain Issuing Keys. Not a single root. Not a full CA chain. |
| **D-002** | The BANZA Root key NEVER signs operator certificates, BRLs, or evidence packages directly. It signs Key Manifests only. |
| **D-003** | Three issuing domains: `certification`, `revocation`, `conformance-evidence`. Domain separation limits compromise blast radius. |
| **D-004** | Production `issuer_key_id` format: `banza-{domain}-{YYYYMM}`. Test format: `test-banza-key-{YYYY-MM}`. These namespaces MUST NOT overlap. |
| **D-005** | The BANZA Key Manifest is the trust anchor distribution mechanism. It is published at `https://banza.network/.well-known/banza/key-manifest.json` and bundled in every BANZA SDK release. |
| **D-006** | Key Manifests are signed by the Root key using the ADR-026 canonical signing rule (all fields except `manifest_signature`, sorted lexicographically). |
| **D-007** | Root key maximum validity: 24 months. Issuing key maximum validity: 6 months. |
| **D-008** | A `test-` prefixed `issuer_key_id` MUST be rejected by production certificate verification (INV-ROOT-001). |
| **D-009** | BanzAI is NOT a signing authority for any production artifact. BanzAI evaluates; BANZA authorizes. |
| **D-010** | Root key compromise triggers full trust reset: new root, new issuing keys, new manifest, ALL L3+ operators re-certify, SDK emergency update. |
| **D-011** | Issuing key compromise triggers: key rotation, new Key Manifest, emergency BRL (for cert and BRL issuing key compromise), targeted operator re-verification. |

---

## Protocol Invariants (Root Architecture)

These invariants extend the INV-TRUST-* series from ADR-026:

| ID | Invariant |
|----|-----------|
| **INV-ROOT-001** | A certificate, BRL, or evidence package whose `issuer_key_id` begins with `test-` MUST NOT be accepted as production-valid. |
| **INV-ROOT-002** | A Key Manifest MUST be signed by the BANZA Root key. An unsigned or root-unverifiable Key Manifest MUST be rejected. |
| **INV-ROOT-003** | A Key Manifest MUST be fetched with `expires_at > now()` before any issuing key within it is used for verification. A stale Key Manifest MUST NOT be used to verify production artifacts. |
| **INV-ROOT-004** | The Root key MUST NOT sign any artifact other than Key Manifests. A certificate or BRL signed directly by a root key `issuer_key_id` is invalid. |
| **INV-ROOT-005** | An issuing key that does not appear in a valid, root-signed Key Manifest with `status: "active"` MUST NOT be used for any verification. |
| **INV-ROOT-006** | Issuing key validity MUST NOT exceed 6 months from activation. Root key validity MUST NOT exceed 24 months. |

---

## Consequences

### Positive

**The root key is never online.** It cannot be stolen from an online system because it is never in one. Root key compromise requires physical access to the HSM facility — a controlled, auditable event.

**Domain separation limits blast radius.** Compromising the conformance infrastructure does not affect live federation trust.

**Certificate verification path is unchanged.** The operator certificate schema (`contracts/federation/operator-certificate.json`) requires no changes. Peers already use `issuer_key_id` to look up the verifying key — they now look it up in the Key Manifest rather than consulting a single pinned key.

**Key rotation is routine.** Issuing keys rotate every 6 months. The Key Manifest handles the transition. No SDK emergency update is required for routine issuing key rotation.

**All prior conformance tests remain valid.** The conformance runner's `test-banza-key-YYYY-MM` convention is unchanged. Test and production key namespaces are distinct.

### Negative (managed)

**Root ceremonies are scheduled operational events.** Activating a new issuing key requires an offline root ceremony. These are quarterly events at most, but they require planning and physical presence of keyholders.

**SDK pinning introduces a distribution dependency.** When the root key rotates (every 24 months), all SDK versions must be updated. This is manageable at the current operator count; it becomes more complex as the network grows.

**Key Manifest availability is a weak dependency.** Operators with stale SDK-pinned manifests will not pick up new issuing keys until they update. During the 24-hour cache window, some operators may attempt to verify against an old key. This is mitigated by overlapping key validity: the new issuing key is published in the manifest at least 30 days before the old one expires.

### Future Path

Once the federation has a stable set of long-standing L3+ certified operators (target: 10+), the root architecture can be upgraded to a multi-signature model (N-of-M keyholders from BANZA and senior certified operators) per ADR-026 §Phase 7. This requires a separate ADR. The Key Manifest format supports this by making `root_key_id` a string rather than a hardcoded structure — the multi-sig upgrade changes who signs the manifest, not the manifest format itself.

---

## Artifacts Required

| Artifact | Type | Blocks | Status |
|----------|------|--------|--------|
| Root key generation ceremony | Operational event | All production certificate issuance | **OPEN** |
| Initial cert-issuing key | Key material | Operator certificate issuance | **OPEN** |
| Initial BRL-issuing key | Key material | Production BRL publication | **OPEN** |
| Initial conformance key | Key material | Evidence package production signing | **OPEN** |
| Initial Key Manifest (all 3 issuing keys) | JSON artifact | SDK pinning, operator verification | **OPEN** |
| `banza.network/.well-known/banza/key-manifest.json` | Operated endpoint | Online verification | **OPEN** |
| `banza.network/federation/revocation-list.json` | Operated endpoint (ADR-026) | BRL distribution | **OPEN** |
| `contracts/federation/key-manifest.json` | JSON Schema | Key Manifest contract | **OPEN** |
| BANZA SDK v1.0 with pinned Key Manifest | SDK artifact | Offline operator verification | **OPEN** |
| Key Manifest verification in conformance runner | Code change | Production mode conformance | **OPEN** |

---

## Related ADRs

- **ADR-018** — Open Financial Kernel: BANZA as protocol authority
- **ADR-019** — Operator Separation: operator-neutrality invariant
- **ADR-026** — Federation Trust Model: PKI architecture, certificate model, `issuer_key_id`
- **ADR-028** — Certification Level Architecture: L3 as federation threshold
- **ADR-030** (future) — Key Manifest Contract: JSON Schema for the Key Manifest
- **ADR-031** (future) — Multi-Signature Root Authority: upgrade path for mature federation
