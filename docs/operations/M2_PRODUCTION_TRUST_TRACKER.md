# M2 — Production Trust Established: Execution Tracker

**Document ID:** BANZA-OPS-M2-TRACKER-001  
**Date:** 2026-06-01  
**Authority:** BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md  
**Status:** ACTIVE  
**Owner:** Fidel Monteiro  
**Milestone:** M2 — Production Trust Established  
**Prerequisite milestone:** M1 — Protocol Complete (ACHIEVED 2026-06-01)

---

## M2 Completion Criterion

M2 is complete when all of the following are simultaneously true:

1. Root key exists and is secured offline
2. `banza-cert-YYYYMM`, `banza-brl-YYYYMM`, `banza-evidence-YYYYMM` exist and are secured
3. Key Manifest is live at `https://banza.network/.well-known/banza/key-manifest.json`
4. BRL is live at `https://banza.network/federation/revocation-list.json`
5. BANZA SDK v1.0 is released with Key Manifest pinned and production `issuer_key_id` verification
6. `INV-ROOT-001` is enforced in the conformance runner (test- key IDs rejected in production mode)

---

## Task Status

### OPS-001 — Root Key Generation Ceremony

| Field | Value |
|-------|-------|
| **Status** | READY TO SCHEDULE |
| **Classification** | READY |
| **Owner** | Fidel Monteiro (Ceremony Officer) |
| **Target date** | TBD — first available date after pre-ceremony checklist complete |
| **Depends on** | Nothing — this is the first unblocked action in the entire backlog |
| **Blocks** | OPS-002, OPS-003, OPS-004, OPS-005 (final pin), OPS-006 (full test) |

#### Pre-execution readiness

| Item | Status | Notes |
|------|--------|-------|
| `ROOT_KEY_CEREMONY_PROCEDURE.md` | COMPLETE | Approved for execution |
| `ROOT_KEY_CEREMONY_CHECKLIST.md` | COMPLETE | Print on ceremony day |
| `ROOT_KEY_CEREMONY_RECORD_TEMPLATE.md` | COMPLETE | Print on ceremony day |
| `trust_root.py` — ceremony software base | COMPLETE | Verified correct algorithm |
| `ceremony_script.py` — ceremony wrapper | **MISSING** | Must be created before ceremony day (see Gap OPS-001-G1) |
| Air-gapped ceremony machine | **NOT CONFIRMED** | Need to identify and verify machine |
| Output USB A (`BANZA_KEYS_A`) | **NOT PROCURED** | ≥8 GB, freshly formatted |
| Output USB B (`BANZA_KEYS_B`) | **NOT PROCURED** | ≥8 GB, freshly formatted |
| Publication USB (`BANZA_PUB`) | **NOT PROCURED** | ≥1 GB, freshly formatted |
| Ceremony USB (software) | **NOT PREPARED** | Depends on ceremony_script.py |
| Offline printer | **NOT CONFIRMED** | Verify before ceremony day |
| Ceremony Officer assigned | ASSIGNED | Fidel Monteiro |
| Ceremony Witness assigned | **UNASSIGNED** | Must assign before scheduling |
| Secure ceremony room | **NOT IDENTIFIED** | Lockable, no external network |

#### Pre-ceremony gaps (must resolve before scheduling)

| ID | Gap | Effort | Unblocked? |
|----|-----|--------|-----------|
| OPS-001-G1 | ~~Create `ceremony_script.py`~~ — **RESOLVED** (`tools/root-ceremony/ceremony_script.py`, dry-run verified, see CEREMONY_SCRIPT_REPORT.md) | ~~1 day~~ — DONE | — |
| OPS-001-G2 | Assign Ceremony Witness | Hours | Yes — immediately |
| OPS-001-G3 | Procure and format 4 USB drives | Hours | Yes — immediately |
| OPS-001-G4 | Identify and verify air-gapped machine | Hours | Yes — immediately |
| OPS-001-G5 | Confirm offline printer functional | Minutes | Yes — immediately |
| OPS-001-G6 | Identify and book secure ceremony room | Hours | Yes — immediately |

**OPS-001-G1 is resolved.** All remaining gaps are physical/logistical.

#### Evidence of completion

- [ ] Ceremony Record signed (Officer + Witness physical signatures)
- [ ] ROOT_KEY_ID recorded: `banza-root-YYYY`
- [ ] ROOT_FINGERPRINT recorded (first 16 hex of SHA-256)
- [ ] Ceremony Record scanned and stored in governance repository
- [ ] All 4 fingerprints confirmed on paper backup

---

### OPS-002 — Generate Issuing Keys

| Field | Value |
|-------|-------|
| **Status** | READY (blocked by OPS-001 only) |
| **Classification** | READY |
| **Owner** | Fidel Monteiro (Ceremony Officer) |
| **Target date** | Same session as OPS-001 (issuing keys are generated during the ceremony) |
| **Depends on** | OPS-001 (root key must exist before issuing keys are generated and endorsed in the Key Manifest) |
| **Blocks** | OPS-003, OPS-004, OPS-005 (final pin) |

#### What happens in OPS-002

The ceremony generates all four keys in a single session:

| Key variable | Key ID format | Example | Max validity |
|-------------|---------------|---------|--------------|
| Root | `banza-root-YYYY` | `banza-root-2026` | 24 months |
| Cert-issuing | `banza-cert-YYYYMM` | `banza-cert-202606` | 6 months |
| BRL-issuing | `banza-brl-YYYYMM` | `banza-brl-202606` | 6 months |
| Evidence-issuing | `banza-evidence-YYYYMM` | `banza-evidence-202606` | 6 months |

Key generation code: `Ed25519PrivateKey.generate()` in `trust_root.py` — correct and verified.  
Key naming convention: frozen in ADR-029 §D-004.  
Storage: encrypted USB (GPG/AES-256) → Output USB A + B.  

No additional implementation work required. The ceremony procedure defines the exact steps.

#### Evidence of completion

- [ ] CERT_KEY_ID recorded in Ceremony Record
- [ ] BRL_KEY_ID recorded in Ceremony Record
- [ ] EVID_KEY_ID recorded in Ceremony Record
- [ ] All 3 issuing public key fingerprints recorded
- [ ] Issuing key validity ≤ 6 months confirmed (ceremony verification check)

---

### OPS-003 — Key Manifest Signed and Published

| Field | Value |
|-------|-------|
| **Status** | PARTIAL |
| **Classification** | PARTIAL |
| **Owner** | Fidel Monteiro |
| **Target date** | Same day as ceremony (publication sequence) |
| **Depends on** | OPS-002 |
| **Blocks** | INFRA-001, OPS-005 (final pin), OPS-007 |

#### Implementation gaps (can be resolved before OPS-001)

| ID | Gap | Effort | Unblocked? |
|----|-----|--------|-----------|
| OPS-003-G1 | `trust_root.py` `generate_key_manifest()` is missing required fields: `root_key_id`, manifest-level `expires_at`, per-key `expires_at`, per-key `domain`, `manifest_signature` | ~0.5 day | Yes — can do today |
| OPS-003-G2 | `contracts/federation/key-manifest.json` does not exist (PROTO-003) | ~0.5 day | Yes — can do today |
| OPS-003-G3 | `banza.network` hosting infrastructure readiness — confirm static file serving + Cache-Control header capability | ~0.5 day | Yes — can do today |

#### Current `generate_key_manifest()` output (INCOMPLETE)

```json
{
  "schema_version": "1",
  "published_at": "...",
  "keys": [{"key_id": "...", "public_key": "...", "active_since": "...", "status": "active"}]
}
```

#### Required Key Manifest structure (ADR-029 §Phase 6)

```json
{
  "schema_version": "1",
  "published_at": "...",
  "root_key_id": "banza-root-2026",
  "expires_at": "...",
  "keys": [
    {
      "key_id": "banza-cert-YYYYMM",
      "domain": "cert",
      "public_key": "ed25519:...",
      "active_since": "...",
      "expires_at": "...",
      "status": "active"
    }
  ],
  "manifest_signature": "..."
}
```

Missing in current code: `root_key_id`, manifest `expires_at`, per-key `expires_at`, per-key `domain`, `manifest_signature`.

#### Evidence of completion

- [ ] `key-manifest.json` accessible at `https://banza.network/.well-known/banza/key-manifest.json`
- [ ] `schema_version: "1"`, `root_key_id` present, `manifest_signature` present
- [ ] Cache-Control response header: `max-age=86400`
- [ ] Signature verifiable against root public key
- [ ] SHA-256 of published file recorded in Ceremony Record Section 7

---

### OPS-004 — BRL Endpoint Live

| Field | Value |
|-------|-------|
| **Status** | READY (blocked by OPS-002 only) |
| **Classification** | READY |
| **Owner** | Fidel Monteiro |
| **Target date** | Same day as ceremony (publication sequence) |
| **Depends on** | OPS-002 (BRL-issuing key must exist) |
| **Blocks** | INFRA-002, OPS-007 |

#### No implementation gaps

`generate_signed_brl()` in `trust_root.py` is complete and correct:
- Produces fully signed BRL with `issuer_key_id`, `issued_at`, `expires_at`, `revoked`, `signature`
- Canonical JSON signing per ADR-026
- `expires_hours=6` is the standard publication value (ceremony uses 7h; Step P.1 re-signs at 6h)

Publication steps are fully defined in ROOT_KEY_CEREMONY_PROCEDURE.md §Part VII (P.1–P.5).  
The only dependency is the BRL-issuing private key from OPS-001/002.

#### Evidence of completion

- [ ] `revocation-list.json` accessible at `https://banza.network/federation/revocation-list.json`
- [ ] `issuer: "BANZA"`, `issuer_key_id: "banza-brl-YYYYMM"`, `revoked: []`
- [ ] Cache-Control response header: `max-age=21600`
- [ ] Signature verifiable against Key Manifest BRL-issuing pubkey
- [ ] Endpoint responds within 500ms

---

### OPS-005 — BANZA SDK v1.0 Released

| Field | Value |
|-------|-------|
| **Status** | BLOCKED |
| **Classification** | BLOCKED |
| **Owner** | Fidel Monteiro |
| **Target date** | TBD — after framework work complete; pin after OPS-002 |
| **Depends on** | OPS-002 (needs real Key Manifest to pin); framework work unblocked today |
| **Blocks** | OPS-007, M2 |

#### Implementation gaps

| ID | Gap | Effort | Unblocked? |
|----|-----|--------|-----------|
| OPS-005-G1 | TypeScript SDK: no Key Manifest fetch, verify, or cache | ~1 day | Yes — start today |
| OPS-005-G2 | Python SDK: no Key Manifest fetch, verify, or cache | ~1 day | Yes — start today |
| OPS-005-G3 | Go SDK: no Key Manifest fetch, verify, or cache | ~1 day | Yes — start today |
| OPS-005-G4 | All SDKs: no `verify_certificate()` against Key Manifest | ~0.5 day each | Yes — start today |
| OPS-005-G5 | All SDKs: INV-ROOT-001 rejection (test- key IDs) | ~0.5 day total | Yes — start today |
| OPS-005-G6 | All SDKs: INV-ROOT-002 (verify manifest_signature with pinned root pubkey) | ~0.5 day total | Yes — start today |
| OPS-005-G7 | All SDKs: INV-ROOT-003 (reject stale Key Manifest) | ~0.5 day total | Yes — start today |
| OPS-005-G8 | All SDKs: pin actual Key Manifest JSON after ceremony | Hours — after OPS-002 | No — needs ceremony output |
| OPS-005-G9 | Version bump: 0.1.0 → 1.0.0 across all SDKs | Hours | Yes — do at release |

#### Current SDK state

| SDK | Version | Key Manifest | Certificate verify | test- rejection |
|-----|---------|-------------|-------------------|----------------|
| TypeScript (`@banza/sdk`) | 0.1.0 | None | None | None |
| Python (`banza-python`) | 0.1.0 | None | None | None |
| Go (`banza-go`) | 0.1.0 | None | None | None |
| PHP | 0.1.0 | None | None | None |

**Key insight:** All framework work (G1–G7) is unblocked today. Only the final manifest pin (G8) needs ceremony output. SDK v1.0 can be feature-complete before the ceremony and released the same day.

#### What SDK v1.0 must include

1. Bundled Key Manifest JSON (`BANZA_KEY_MANIFEST` constant — pinned at release time)
2. `verify_certificate(cert, key_manifest)` — verifies ed25519 signature against Key Manifest issuing key
3. `verify_brl(brl, key_manifest)` — verifies BRL signature against Key Manifest BRL key
4. `fetch_and_verify_key_manifest(url, root_pubkey)` — fetch + verify manifest_signature
5. INV-ROOT-001: reject `issuer_key_id` starting with `test-` in non-test mode
6. INV-ROOT-002: reject Key Manifest with invalid manifest_signature
7. INV-ROOT-003: reject Key Manifest where `expires_at < now()`

#### Evidence of completion

- [ ] SDK v1.0.0 published (TypeScript, Python, Go)
- [ ] `BANZA_KEY_MANIFEST` constant contains real Key Manifest (not test fixture)
- [ ] `verify_certificate()` passes against production cert signed by `banza-cert-YYYYMM`
- [ ] `issuer_key_id: "test-..."` → rejected with INV-ROOT-001 error (in production mode)
- [ ] Release notes confirm Key Manifest pinned at commit hash

---

### OPS-006 — INV-ROOT-001 Enforced in Conformance Runner

| Field | Value |
|-------|-------|
| **Status** | PARTIAL |
| **Classification** | PARTIAL |
| **Owner** | Fidel Monteiro |
| **Target date** | Can complete today (unblocked) |
| **Depends on** | OPS-002 (for full production test); code change unblocked today |
| **Blocks** | OPS-007 |

#### Current state

The conformance runner (`tools/banza-conformance/run_fed.py`) uses `test-banza-key-YYYY-MM` key IDs everywhere. There is no `--production-mode` flag and no check that rejects `test-` prefixed `issuer_key_id` values.

The `production_allowed: False` flags in manifests are the *operator's own* environment flag — not the BANZA root key check required by INV-ROOT-001.

#### Required code change

Add a `--production-mode` flag (or `BANZA_PRODUCTION_MODE=1` env variable) to the conformance runner that:

1. Rejects any `issuer_key_id` beginning with `test-` with a FAIL result
2. Reports the violation as `INV-ROOT-001` in the test output
3. Exits non-zero if any certificate in the submission uses a test key ID

Location: `tools/banza-conformance/run_fed.py` (and `run.py` for L0–L2 tests)

Estimated effort: ~2 hours

#### Evidence of completion

- [ ] `python run_fed.py --production-mode` flag exists
- [ ] `test-banza-key-*` `issuer_key_id` → FAIL with `INV-ROOT-001` in production mode
- [ ] `banza-cert-YYYYMM` `issuer_key_id` → not rejected
- [ ] Existing test suite (79/79) still passes in default (test) mode

---

## Pre-Ceremony Work Summary

All items below are **unblocked today**. Completing them before the ceremony means M2 is achievable in one day after the ceremony.

| Task | Description | Effort | Priority |
|------|-------------|--------|---------|
| OPS-001-G1 | ~~Create `ceremony_script.py`~~ | **DONE** | ~~CRITICAL~~ — resolved |
| OPS-001-G2–G6 | Hardware + participants + room | Hours | CRITICAL — required before ceremony |
| OPS-003-G1 | Fix `generate_key_manifest()` in `trust_root.py` | ~0.5 day | HIGH — needed on ceremony day |
| OPS-003-G2 | Create `contracts/federation/key-manifest.json` (PROTO-003) | ~0.5 day | HIGH |
| OPS-003-G3 | Confirm `banza.network` hosting readiness | ~0.5 day | HIGH |
| OPS-005-G1–G7 | SDK v1.0 framework (all SDKs — minus actual manifest pin) | ~3–5 days | HIGH — start immediately |
| OPS-006 | INV-ROOT-001 in conformance runner | ~2 hours | MEDIUM — straightforward change |

---

## Execution Timeline

### Recommended sequence

```
TODAY (Day 1)
  ├── Start OPS-005 framework (SDK v1.0 key verification logic) — 3–5 days
  ├── Start OPS-006 (INV-ROOT-001 enforcement) — 2 hours
  ├── Fix generate_key_manifest() (OPS-003-G1) — 0.5 day
  ├── Create contracts/federation/key-manifest.json (OPS-003-G2) — 0.5 day
  └── Create ceremony_script.py (OPS-001-G1) — 1 day

DAYS 2–5
  ├── Complete SDK v1.0 framework
  ├── Confirm banza.network hosting (OPS-003-G3)
  └── Resolve ceremony logistics (hardware, participants, room)

CEREMONY DAY (TBD — earliest Day 5+)
  ├── OPS-001 — Execute root key ceremony
  │     └── OPS-002 (done within ceremony) — generate issuing keys
  ├── OPS-003 — Sign and publish Key Manifest (publication sequence)
  └── OPS-004 — Sign and publish initial BRL

POST-CEREMONY (same day or next day)
  ├── OPS-005-G8 — Pin real Key Manifest in SDKs → release v1.0
  └── INFRA-001 / INFRA-002 — verify endpoint cache headers

M2 COMPLETE
```

**Minimum elapsed time from today to M2:** 5–10 days (ceremony logistics are the bottleneck)  
**Minimum elapsed time after ceremony:** 0–1 day (if SDK work is done in advance)

---

## Completion Declaration

M2 is complete when:

- [ ] OPS-001 Ceremony Record signed and filed
- [ ] OPS-002 All 4 key IDs and fingerprints recorded
- [ ] OPS-003 Key Manifest live and endpoint verified (schema + signature + cache headers)
- [ ] OPS-004 BRL live and endpoint verified (0 revoked, correct issuer_key_id, cache headers)
- [ ] OPS-005 SDK v1.0.0 released (TypeScript + Python + Go minimum)
- [ ] OPS-006 INV-ROOT-001 enforced in conformance runner

When all 6 boxes above are checked: record M2 as complete and update BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md.

**M2 completion enables M3** (First Operator Certified). M3 can begin immediately after M2.
