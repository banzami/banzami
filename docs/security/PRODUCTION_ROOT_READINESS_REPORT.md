# BANZA Production Root Readiness Report

**Document ID:** BANZA-PRODUCTION-ROOT-ARCHITECTURE-001  
**Date:** 2026-05-31  
**Authority:** ADR-029 (Production Root Architecture)  
**Status:** FINAL  

---

## Executive Summary

| Question | Answer |
|----------|--------|
| Is the production root architecture frozen? | **YES** — ADR-029 accepted |
| Can BANZA safely issue production operator certificates today? | **NO — root key does not yet exist** |
| Is the architecture sound for production issuance? | **YES** |
| What remains before first certificate issuance? | **5 operational items (no code blockers)** |

The architecture is complete. The blocker is not design — it is the offline key generation ceremony that must happen before any issuing keys can be activated.

---

## Phase 1 — Current State Audit

### What exists today

| Component | State | Notes |
|-----------|-------|-------|
| Certificate schema (`contracts/federation/operator-certificate.json`) | Complete | `issuer_key_id` field ready for production key IDs |
| Certificate signing (`trust_root.py` — `sign_certificate`) | Test-mode | Ephemeral keypair per run; test key ID format |
| BRL signing (`trust_root.py` — `sign_brl`, `generate_signed_brl`) | Test-mode | Same ephemeral keypair; test key ID format |
| Evidence signing (`trust_root.py` — `sign_evidence_package`) | Test-mode | Same ephemeral keypair |
| Key manifest generation (`trust_root.py` — `generate_key_manifest`) | Stub | Structure correct; not published anywhere |
| `issuer_key_id` convention | Test only | `test-banza-key-YYYY-MM`; no production convention defined |
| BANZA root key | **Does not exist** | No HSM, no ceremony, no key material |
| BANZA cert-issuing key | **Does not exist** | Blocked by root key |
| BANZA BRL-issuing key | **Does not exist** | Blocked by root key |
| BANZA conformance key | **Does not exist** | Blocked by root key |
| Key Manifest endpoint | **Does not exist** | Blocked by root key |
| BRL endpoint (`banza.network/federation/revocation-list.json`) | **Does not exist** | Blocked by BRL-issuing key |
| Production `issuer_key_id` convention | **Now frozen** | ADR-029 D-004: `banza-{domain}-{YYYYMM}` |

### What the current test-mode root does well

The ephemeral test root in `trust_root.py` is the correct model for the production root — just without persistence or HSM storage:

- ed25519 algorithm (correct)
- Canonical JSON signing (correct, per ADR-026)
- `issuer_key_id` embedded in all signed artifacts (correct)
- Separate sign/verify functions for certs, BRLs, and evidence (correct)
- `generate_key_manifest()` exists with the correct structure (correct)

The production root requires the same logic with persistence, HSM storage, and publication.

### Production gaps identified

| Gap | Severity | Blocks |
|-----|----------|--------|
| No root key exists | CRITICAL | Everything |
| No issuing keys exist | CRITICAL | All certificate issuance |
| No Key Manifest published | CRITICAL | Offline operator verification |
| No BRL endpoint | HIGH | Federation revocation enforcement |
| No production `issuer_key_id` in any SDK | HIGH | Production certificate verification |
| `INV-ROOT-001` not enforced in conformance runner | MEDIUM | Production vs test key separation |
| Key Manifest schema not a contract in `contracts/` | LOW | Formal contract coverage |

---

## Phase 2 — Root Authority Model (Frozen)

The following boundaries are established by ADR-029 and are non-negotiable:

### BANZA is the sole trust authority

```
Operators
    ↑
  BanzAI    ← verifies trust, evaluates conformance
    ↑
  BANZA     ← issues certificates, signs BRLs, controls root
```

No operator participates in trust issuance. BanzAI evaluates but never authorizes.

### The Root key never touches the runtime path

The Root key signs Key Manifests only. Operator certificate verification proceeds:

```
operator cert → issuer_key_id → Key Manifest → issuing public key → verify signature
```

The Root key is never present in this path. It only appears when the Key Manifest needs to be updated (issuing key rotation, ~every 6 months).

### What BANZA signs vs what BANZA delegates

| Artifact | BANZA Root | BANZA Cert-Issuing | BANZA BRL-Issuing | BANZA Conformance | BanzAI |
|----------|:----------:|:------------------:|:-----------------:|:-----------------:|:------:|
| Key Manifest | **YES** | No | No | No | Never |
| Operator certificate | No | **YES** | No | No | Never |
| BANZA Revocation List | No | No | **YES** | No | Never |
| Evidence package | No | No | No | **YES** | Never |

---

## Phase 3 — Key Hierarchy (Frozen)

```
BANZA Root Key (offline, HSM, 24-month max)
    │
    └── signs → BANZA Key Manifest
                    │
                    ├── banza-cert-YYYYMM    → operator certificates
                    ├── banza-brl-YYYYMM     → BANZA Revocation Lists
                    └── banza-evidence-YYYYMM → conformance evidence packages
```

**Selected:** Root + Domain Issuing Keys (ADR-029 §Phase 3, Option B + D)

**Rejected alternatives:**
- Single Root Key: root would need to be online for routine certificate issuance; rejected
- Full CA chain in certificates: requires breaking changes to `operator-certificate.json` schema; rejected
- Multi-Sig Council (D): bootstrapping problem + governance complexity; deferred to future ADR (ADR-031)

---

## Phase 4 — Key Lifecycle (Frozen)

| Key | Max validity | Routine rotation | Emergency rotation |
|-----|-------------|-----------------|-------------------|
| Root | 24 months | Every 24 months | On compromise |
| Cert-issuing | 6 months | Every 6 months | On compromise |
| BRL-issuing | 6 months | Every 6 months | On compromise |
| Conformance | 6 months | Every 6 months | On compromise |
| Operator certificates (L3+) | 90 days | Before expiry | BRL suspension |
| Operator certificates (L0–L2) | 12 months | Before expiry | BRL suspension |

### `issuer_key_id` naming convention (frozen)

| Context | Format | Example |
|---------|--------|---------|
| Production root | `banza-root-YYYY` | `banza-root-2026` |
| Production cert-issuing | `banza-cert-YYYYMM` | `banza-cert-202608` |
| Production BRL-issuing | `banza-brl-YYYYMM` | `banza-brl-202608` |
| Production conformance | `banza-evidence-YYYYMM` | `banza-evidence-202608` |
| Test (all contexts) | `test-banza-key-YYYY-MM` | `test-banza-key-2026-05` |

**INV-ROOT-001:** Any `issuer_key_id` beginning with `test-` MUST be rejected by production certificate verification.

---

## Phase 5 — Signing Authority Matrix (Frozen)

| Artifact | Signing key | `issuer_key_id` | Verified against |
|----------|-------------|-----------------|-----------------|
| Operator certificate | banza-cert-YYYYMM | cert | Key Manifest issuing pubkey |
| BANZA Revocation List | banza-brl-YYYYMM | brl | Key Manifest issuing pubkey |
| Conformance evidence package | banza-evidence-YYYYMM | evidence | Key Manifest issuing pubkey |
| BANZA Key Manifest | banza-root-YYYY | root | Root pubkey (SDK-pinned) |
| Operator key rotation request | operator's own current key | n/a | Operator's cert pubkey |

---

## Phase 6 — Publication Model (Frozen)

| Resource | URL | Cache TTL | Update trigger |
|----------|-----|-----------|----------------|
| Key Manifest | `https://banza.network/.well-known/banza/key-manifest.json` | 24 hours | Issuing key rotation |
| Key Archive | `https://banza.network/.well-known/banza/key-archive.json` | Immutable per version | Historical verification |
| BRL | `https://banza.network/federation/revocation-list.json` | 6 hours (ADR-026) | Revocation / suspension |
| Emergency BRL | Same URL, `expires_at` set to 1 hour | 1 hour | Issuing key compromise |

Key Manifests are also bundled in BANZA SDK releases and pinned in the conformance runner. Offline verification does not require network access.

---

## Phase 7 — Compromise Recovery (Frozen)

| Scenario | Recovery path | Federation disruption |
|----------|--------------|----------------------|
| Conformance key compromise | Rotate key, invalidate affected evidence, re-run conformance | None (evidence only) |
| BRL-issuing key compromise | Rotate key, publish emergency BRL with new key | 1–6 hours |
| Cert-issuing key compromise | Rotate key, suspend affected operators pending re-verification | Days |
| Root key compromise | Full trust reset: new root, new issuing keys, new manifest, SDK update, ALL L3+ re-certify | Days–weeks |

Full step-by-step procedures are defined in ADR-029 §Phase 8.

---

## Phase 8 — BanzAI Alignment (Frozen)

BanzAI may verify trust. BanzAI may never grant it.

| Action | BanzAI permitted |
|--------|:----------------:|
| Verify operator certificate signature | Yes |
| Execute ADR-026 trust protocol (Steps 1–9) | Yes |
| Fetch and verify BRL | Yes |
| Run conformance suite | Yes |
| Generate signed evidence packages (via BANZA conformance infrastructure) | Yes |
| Issue operator certificates | **No** |
| Sign BRLs | **No** |
| Hold any production BANZA private key | **No** |
| Make certification approval decisions | **No** |

This boundary is permanent. It follows from ADR-018 (BANZA as protocol authority) and ADR-019 (operator separation). An AI system that can grant trust is a trust authority — BANZA does not delegate trust authority.

---

## Phase 9 — Production Readiness Verdict

### Can BANZA safely issue production operator certificates?

**Not yet. The root key does not exist.**

The architecture is sound, complete, and frozen. The protocol contracts are ready. The conformance runner is ready. The only blocker is the offline key generation ceremony, which has not yet occurred.

### What remains before first certificate issuance

The following 5 items must be completed in the order listed. Each depends on the previous.

| # | Item | Type | Owner | Depends on |
|---|------|------|-------|-----------|
| **1** | Root key generation ceremony | Operational event | BANZA | Nothing — this is the unblocked starting point |
| **2** | Cert-issuing, BRL-issuing, and conformance keys generated and endorsed in initial Key Manifest (root-signed) | Operational + artifact | BANZA | Item 1 |
| **3** | Key Manifest published at `banza.network/.well-known/banza/key-manifest.json` and BRL endpoint live at `banza.network/federation/revocation-list.json` | Infrastructure | BANZA | Item 2 |
| **4** | BANZA SDK v1.0 released with pinned Key Manifest and production `issuer_key_id` in verification logic | SDK release | BANZA | Item 2 |
| **5** | `INV-ROOT-001` enforced in conformance runner: reject `test-` key IDs in production mode | Code change | BANZA | Item 2 |

After these 5 items are complete, BANZA can safely issue the first production operator certificate.

### What is NOT required before first certificate issuance

- No ADR changes (ADR-029 is the final word)
- No contract changes (the certificate schema already supports production `issuer_key_id`)
- No conformance test changes (the conformance suite already tests everything it needs to test)
- No BanzAI changes (BanzAI already verifies signatures correctly)

---

## Phase 10 — Updated Production Blockers

After ADR-029:

| Blocker | Before | After |
|---------|--------|-------|
| #1 ADR-028 — certification level architecture | Resolved (prior session) | — |
| #2 Production BANZA Root key establishment | **Architecture undefined** | **Architecture frozen (ADR-029)** |
| #3 Real two-operator interoperability test | Open | Open — not addressed in this task |

**Blocker #2 status change:** From "architecture undefined, cannot proceed" to "architecture frozen, 5 operational items remain."

The 5 operational items blocking first production issuance are all in BANZA's hands. No protocol changes are required. No further ADR is required before beginning the key ceremony.

---

## Appendix — ADR-029 Invariants Summary

| ID | Statement |
|----|-----------|
| INV-ROOT-001 | `test-` prefixed `issuer_key_id` MUST be rejected in production |
| INV-ROOT-002 | Key Manifest MUST be root-signed; unsigned manifest = rejected |
| INV-ROOT-003 | Stale Key Manifest (`expires_at < now()`) MUST NOT be used |
| INV-ROOT-004 | Root key MUST NOT sign certificates, BRLs, or evidence |
| INV-ROOT-005 | Issuing key not in a valid Key Manifest MUST NOT be used for verification |
| INV-ROOT-006 | Issuing key max validity: 6 months. Root key max validity: 24 months |

These extend the INV-TRUST-* series from ADR-026.
