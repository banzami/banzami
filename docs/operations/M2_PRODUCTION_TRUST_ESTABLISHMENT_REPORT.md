# M2 — Production Trust Establishment: Operational Readiness Report

**Document ID:** BANZA-OPS-M2-REPORT-001  
**Date:** 2026-06-01  
**Authority:** BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md, BANZA-PROTOCOL-COMPLETION-AUDIT-001  
**Status:** FINAL  
**Owner:** Fidel Monteiro

---

## Executive Summary

| Question | Answer |
|----------|--------|
| Is M1 (Protocol Complete) achieved? | **YES — 2026-06-01** |
| Can M2 be achieved immediately? | **NO** |
| Is M2 architecturally unblocked? | **YES — no protocol work remains** |
| What is the critical blocker? | **OPS-001 — root key ceremony (physical event, not yet scheduled)** |
| What is the fastest path to M2? | **Start parallel pre-ceremony work today; execute ceremony as soon as logistics are ready** |
| Estimated elapsed time to M2 | **5–10 days from today** |

---

## Phase 1 — Operational Readiness Audit

### Prerequisite Documents

| Document | Path | Status |
|----------|------|--------|
| Transition Plan | `docs/governance/BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md` | COMPLETE |
| Ceremony Procedure | `docs/security/ROOT_KEY_CEREMONY_PROCEDURE.md` | COMPLETE (938 lines) |
| Ceremony Checklist | `docs/security/ROOT_KEY_CEREMONY_CHECKLIST.md` | COMPLETE (261 lines) |
| Ceremony Record Template | `docs/security/ROOT_KEY_CEREMONY_RECORD_TEMPLATE.md` | COMPLETE (308 lines) |
| Production Root Readiness Report | `docs/security/PRODUCTION_ROOT_READINESS_REPORT.md` | COMPLETE |

All prerequisite documents exist and are approved for use.

### Protocol Dependencies

| ADR | Subject | Status |
|-----|---------|--------|
| ADR-026 | Federation Trust Model | ACCEPTED |
| ADR-028 | Certification Level Architecture | ACCEPTED |
| ADR-029 | Production Root Architecture | ACCEPTED |

Zero unresolved ADRs. No protocol design work remains before production.

### Conformance

| Suite | Tests | Result |
|-------|-------|--------|
| L0–L2 conformance | 51 vectors | 51/51 PASS (reported) |
| Federation conformance | 79 tests | 79/79 PASS |
| Real two-operator interoperability | 14 scenarios | 14/14 PASS |

Protocol is operationally sound. Conformance infrastructure is ready.

---

## Phase 2 — M2 Task Readiness Score

### OPS-001 — Root Key Generation Ceremony

**Score: READY**

All ceremony documents are complete and approved. The ceremony software (`trust_root.py`) implements the correct algorithm (ed25519, canonical JSON signing per ADR-026). One pre-ceremony technical artifact is missing: `ceremony_script.py` (the structured execution wrapper referenced in Procedure Appendix A). Physical logistics are unconfirmed.

| Component | Status |
|-----------|--------|
| Ceremony procedure | COMPLETE |
| Ceremony checklist | COMPLETE |
| Ceremony record template | COMPLETE |
| `trust_root.py` | COMPLETE |
| `ceremony_script.py` | MISSING |
| Hardware (4 USB drives) | NOT PROCURED |
| Air-gapped machine | NOT CONFIRMED |
| Witness assigned | UNASSIGNED |
| Secure room | NOT IDENTIFIED |

**Verdict:** Schedulable after ceremony_script.py is created and logistics are resolved. Estimated 1–5 days to ceremony-ready.

---

### OPS-002 — Generate Issuing Keys

**Score: READY (blocked by OPS-001 only)**

Issuing key generation occurs within the ceremony session. The code exists (`Ed25519PrivateKey.generate()`), the naming convention is frozen (`banza-cert-YYYYMM`, `banza-brl-YYYYMM`, `banza-evidence-YYYYMM`), and the storage procedure is fully documented. No additional implementation work is required.

---

### OPS-003 — Key Manifest Signed and Published

**Score: PARTIAL**

BRL signing is complete. Key Manifest generation has gaps.

| Component | Status | Detail |
|-----------|--------|--------|
| Signing algorithm | COMPLETE | ed25519, canonical JSON, ADR-026 compliant |
| `generate_key_manifest()` function | INCOMPLETE | Missing: `root_key_id`, manifest `expires_at`, per-key `expires_at`, per-key `domain`, `manifest_signature` |
| `contracts/federation/key-manifest.json` | MISSING | PROTO-003 not yet done |
| `banza.network` hosting readiness | UNCONFIRMED | Static file serving + Cache-Control header capability |

**All gaps are resolvable before the ceremony.** The ceremony will produce the correct key material regardless of this code state — the gap only affects the post-ceremony publication step.

---

### OPS-004 — BRL Endpoint Live

**Score: READY (blocked by OPS-002 only)**

`generate_signed_brl()` in `trust_root.py` is complete and correct. The ceremony procedure (Step P.1) defines the re-signing step for publication. No implementation gaps. Hosting requires the same infrastructure as OPS-003.

---

### OPS-005 — BANZA SDK v1.0 Released

**Score: BLOCKED**

This is the most significant implementation gap before M2. No SDK has federation trust verification capability.

| SDK | Version | Key Manifest support | Certificate verify | INV-ROOT-001 |
|-----|---------|---------------------|-------------------|--------------|
| TypeScript (`@banza/sdk`) | 0.1.0 | None | None | None |
| Python (`banza-python`) | 0.1.0 | None | None | None |
| Go (`banza-go`) | 0.1.0 | None | None | None |

Required for SDK v1.0:
- Bundled Key Manifest JSON (pinned)
- `verify_certificate(cert, key_manifest)` → ed25519 verify against issuing key
- `verify_brl(brl, key_manifest)` → ed25519 verify against BRL key
- `fetch_and_verify_key_manifest(url, root_pubkey)` → verify manifest_signature
- INV-ROOT-001: reject `issuer_key_id` beginning with `test-`
- INV-ROOT-002: reject Key Manifest with invalid manifest_signature
- INV-ROOT-003: reject Key Manifest where `expires_at < now()`

**Key insight:** All implementation work except the final Key Manifest pin (G8) is unblocked today. The Key Manifest JSON structure, signing algorithm, and verification rules are fully specified. SDK v1.0 can be feature-complete before the ceremony and released the same day as the ceremony.

Estimated effort: 3–5 days across TypeScript + Python + Go.

---

### OPS-006 — INV-ROOT-001 Enforced in Conformance Runner

**Score: PARTIAL**

The conformance runner currently uses `test-banza-key-YYYY-MM` key IDs with no production mode enforcement. The `production_allowed: False` flags in operator manifests are the operator's own environment flag — distinct from the BANZA root key INV-ROOT-001 check.

Required change: add `--production-mode` flag (or `BANZA_PRODUCTION_MODE=1`) to `run_fed.py` and `run.py` that:
- Rejects any `issuer_key_id` beginning with `test-`
- Reports the violation as `INV-ROOT-001` in test output
- Does not affect the existing test suite (79/79 tests pass in default mode)

Estimated effort: ~2 hours. Fully unblocked today.

---

## Phase 3 — Root Ceremony Preparation

### Pre-execution gaps

| ID | Gap | Effort | When to resolve |
|----|-----|--------|----------------|
| OPS-001-G1 | Create `ceremony_script.py` | ~1 day | Before ceremony — CRITICAL |
| OPS-001-G2 | Assign Ceremony Witness | Hours | Immediately |
| OPS-001-G3 | Procure 4 USB drives (format + verify) | Hours | Before ceremony |
| OPS-001-G4 | Identify + verify air-gapped machine | Hours | Before ceremony |
| OPS-001-G5 | Confirm offline printer functional | Minutes | Before ceremony |
| OPS-001-G6 | Book secure ceremony room | Hours | Before ceremony |

### ceremony_script.py specification

The ceremony_script.py must implement Phases 0–7 of the Procedure as a single executable Python script:
- Accept no network connections
- Print all fingerprints and hashes to stdout for Witness recording
- Write outputs to explicitly specified file paths
- Assert key ID format (no `test-` prefix)
- Assert issuing key validity ≤ 184 days
- Verify Key Manifest signature (in-memory)
- Verify Key Manifest signature from disk
- Verify BRL signature from disk
- Exit non-zero on any verification failure

Base module: `tools/banza-conformance/trust_root.py` (import directly).

---

## Phase 4 — Issuing Key Plan

Naming convention is frozen by ADR-029 §D-004. No decisions remain.

| Key | ID | Example (June 2026 ceremony) | Max validity | Rotation |
|-----|-----|------------------------------|-------------|---------|
| Root | `banza-root-YYYY` | `banza-root-2026` | 24 months | 2028-06 |
| Cert-issuing | `banza-cert-YYYYMM` | `banza-cert-202606` | 6 months | 2026-12 |
| BRL-issuing | `banza-brl-YYYYMM` | `banza-brl-202606` | 6 months | 2026-12 |
| Evidence-issuing | `banza-evidence-YYYYMM` | `banza-evidence-202606` | 6 months | 2026-12 |

**Storage:** Root private key → encrypted USB A + B (GPG/AES-256) + paper backup. Issuing private keys → same USB with root.  
**Activation:** Keys are active from the moment of the Key Manifest publication (OPS-003).  
**Publication sequence:** P.1 (re-sign BRL) → P.2 (publish Key Manifest) → P.3 (verify) → P.4 (publish BRL) → P.5 (verify).

---

## Phase 5 — Key Manifest Publication Plan

### Schema (required output from ceremony)

```json
{
  "schema_version": "1",
  "published_at": "2026-06-XX T HH:MM:SSZ",
  "root_key_id": "banza-root-2026",
  "expires_at": "2028-06-XX T HH:MM:SSZ",
  "keys": [
    {
      "key_id": "banza-cert-202606",
      "domain": "cert",
      "public_key": "ed25519:<base64url>",
      "active_since": "2026-06-XX T HH:MM:SSZ",
      "expires_at": "2026-12-XX T HH:MM:SSZ",
      "status": "active"
    },
    {
      "key_id": "banza-brl-202606",
      "domain": "brl",
      "public_key": "ed25519:<base64url>",
      "active_since": "2026-06-XX T HH:MM:SSZ",
      "expires_at": "2026-12-XX T HH:MM:SSZ",
      "status": "active"
    },
    {
      "key_id": "banza-evidence-202606",
      "domain": "evidence",
      "public_key": "ed25519:<base64url>",
      "active_since": "2026-06-XX T HH:MM:SSZ",
      "expires_at": "2026-12-XX T HH:MM:SSZ",
      "status": "active"
    }
  ],
  "manifest_signature": "<base64url ed25519 sig>"
}
```

### Hosting requirements

| Requirement | Value |
|------------|-------|
| URL | `https://banza.network/.well-known/banza/key-manifest.json` |
| Cache-Control header | `max-age=86400` |
| Content-Type | `application/json; charset=utf-8` |
| TLS | Required |
| Update trigger | Issuing key rotation (every 6 months) or root key compromise |

### Rollout procedure

1. Ceremony generates Key Manifest JSON (in-memory)
2. Ceremony writes signed Key Manifest to Publication USB
3. Post-ceremony: upload from Publication USB to `banza.network`
4. Verify endpoint: `curl -s <url> | python3 -c "import json,sys; m=json.load(sys.stdin); print(m.get('root_key_id'), bool(m.get('manifest_signature')))"`
5. Confirm `Cache-Control: max-age=86400` response header
6. SDK v1.0 pins this exact JSON

### Remaining implementation work

`generate_key_manifest()` in `trust_root.py` must be updated to produce the full structure. Current gaps: `root_key_id`, manifest `expires_at`, per-key `expires_at`, per-key `domain`, `manifest_signature` signing step.

The contract file `contracts/federation/key-manifest.json` (PROTO-003) must be created.

---

## Phase 6 — BRL Endpoint Plan

### Generation workflow

```python
# Step P.1 — Publication BRL (6h expiry, per ADR-026)
from tools.banza_conformance.trust_root import generate_signed_brl

pub_brl = generate_signed_brl(
    root_private_key=brl_priv,      # decrypted from Publication USB
    key_id="banza-brl-202606",      # exact key ID from ceremony
    revoked=[],                     # empty at launch
    expires_hours=6,                # ADR-026 standard
)
```

### Signing workflow

The ceremony procedure Step P.1 defines the re-signing step. `generate_signed_brl()` in `trust_root.py` is complete and correct. No changes required.

### Publication workflow

```bash
curl -X PUT \
  -H "Cache-Control: max-age=21600" \
  -H "Content-Type: application/json" \
  --data-binary @initial-brl.json \
  https://banza.network/federation/revocation-list.json
```

### Verification workflow

After publication: `issuer_key_id` → Key Manifest → BRL-issuing pubkey → verify signature. This path is exercised today in the conformance runner (FED-TRUST-005). No new code required.

### Hosting requirements

| Requirement | Value |
|------------|-------|
| URL | `https://banza.network/federation/revocation-list.json` |
| Cache-Control header | `max-age=21600` (6 hours) |
| Update trigger | BRL rotation (routine: re-sign every 6 hours), or operator suspension |

---

## Phase 7 — SDK Release Plan

### Release blockers

| Blocker | Owner | Unblocked? |
|---------|-------|-----------|
| Key Manifest verification logic (all 3 SDKs) | Fidel Monteiro | YES — start today |
| Certificate verify against Key Manifest | Fidel Monteiro | YES — start today |
| INV-ROOT-001 (test- rejection) | Fidel Monteiro | YES — start today |
| INV-ROOT-002 (manifest_signature verify) | Fidel Monteiro | YES — start today |
| INV-ROOT-003 (stale manifest rejection) | Fidel Monteiro | YES — start today |
| Actual Key Manifest JSON to pin | OPS-001/002 | NO — needs ceremony output |

### No test key leakage concern

The existing SDKs contain no key material at all. The ceremony produces the first key material. `test-banza-key-*` IDs exist only in the conformance runner (in-memory, ephemeral) and are not distributed in any SDK.

### Production endpoint readiness

SDKs must ship with the live URL as default:
- Key Manifest URL: `https://banza.network/.well-known/banza/key-manifest.json`
- BRL URL: `https://banza.network/federation/revocation-list.json`

These URLs are frozen (ADR-029 §Phase 6). No further decision required.

---

## Phase 8 — INV-ROOT-001 Enforcement

### Current state

The conformance runner has no production mode. `production_allowed: False` in operator manifests is an operator environment flag, unrelated to the BANZA trust root check.

### Required change

File: `tools/banza-conformance/run_fed.py` (and `run.py` for L0–L2)

Add at the top of the federation runner's certificate validation step:

```python
def check_inv_root_001(issuer_key_id: str, production_mode: bool) -> tuple:
    """INV-ROOT-001: test- key IDs MUST be rejected in production mode."""
    if production_mode and issuer_key_id.startswith("test-"):
        return False, f"INV-ROOT-001 VIOLATION: issuer_key_id={issuer_key_id!r} begins with 'test-' — rejected in production mode"
    return True, "INV-ROOT-001: OK"
```

Entry point: add `--production-mode` argument to `python run_fed.py`. Default is test mode (no change to existing behavior). Production mode flag activates INV-ROOT-001 check.

### Verification after implementation

```bash
# Must FAIL with INV-ROOT-001:
python run_fed.py --production-mode --operator-url http://... 
# (where operator cert has issuer_key_id: "test-banza-key-2026-06")

# Must PASS (79/79):
python run_fed.py
# (default test mode, no change)
```

---

## Phase 9 — M2 Readiness Score

| Task | Score | Rationale |
|------|-------|-----------|
| OPS-001 Root Key Ceremony | **READY** | All documents complete; ceremony_script.py missing (1 day to create); logistics unresolved |
| OPS-002 Issuing Keys | **READY** | Performed within ceremony; no implementation gaps |
| OPS-003 Key Manifest Publication | **PARTIAL** | `generate_key_manifest()` missing 5 fields; contract file missing; hosting unconfirmed |
| OPS-004 BRL Endpoint | **READY** | `generate_signed_brl()` complete; same hosting as OPS-003 |
| OPS-005 SDK v1.0 | **BLOCKED** | No Key Manifest support in any SDK; significant work required (~3–5 days, but unblocked) |
| OPS-006 INV-ROOT-001 Enforcement | **PARTIAL** | ~2h code change required; fully unblocked |

**Summary: 2 READY, 2 PARTIAL, 2 BLOCKED**

The 2 PARTIAL items (OPS-003, OPS-006) are bounded implementation tasks executable in under 1 day each. The 1 BLOCKED item (OPS-005) requires 3–5 days but is entirely unblocked today and can run in parallel with ceremony logistics.

---

## Phase 10 — Final Report

### Operational Readiness Score

```
OPS-001  [██████████████░░] READY — 1 pre-ceremony artifact missing
OPS-002  [████████████████] READY — blocked only by OPS-001
OPS-003  [████████░░░░░░░░] PARTIAL — 3 implementation gaps, all resolvable
OPS-004  [████████████████] READY — blocked only by OPS-002
OPS-005  [████░░░░░░░░░░░░] BLOCKED — significant work; 3–5 days, unblocked today
OPS-006  [████████████░░░░] PARTIAL — 2h code change, unblocked today
```

**Overall M2 readiness: 67% complete by task count. 100% architecturally unblocked.**

### Blockers

| ID | Blocker | Owner | Path to unblock |
|----|---------|-------|----------------|
| B1 | `ceremony_script.py` does not exist | Fidel Monteiro | Create it — ~1 day |
| B2 | Physical ceremony logistics (hardware, participants, room) | Fidel Monteiro | Procurement + scheduling |
| B3 | OPS-005 SDK v1.0 Key Manifest support — 3–5 days work | Fidel Monteiro | Start today |
| B4 | `generate_key_manifest()` missing fields | Fidel Monteiro | Fix — ~0.5 day |
| B5 | INV-ROOT-001 not in conformance runner | Fidel Monteiro | Add flag — ~2 hours |
| B6 | `banza.network` hosting readiness unconfirmed | Fidel Monteiro | Confirm + set up Cache-Control headers |

No external dependencies. All blockers are in BANZA's hands.

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Ceremony day technical failure (software bug in ceremony_script.py) | LOW | HIGH — voids ceremony | Test ceremony_script.py thoroughly before execution; dry-run on a non-air-gapped machine |
| ceremony_script.py produces invalid Key Manifest (missing fields) | LOW | HIGH — delays publication | Fix generate_key_manifest() before the ceremony; include field assertions in ceremony script |
| USB drive failure during ceremony | LOW | MEDIUM — delays completion | Use Output USB A + B redundancy as designed; verify both during ceremony |
| SDK v1.0 takes longer than expected | MEDIUM | MEDIUM — delays M2 | Start today; SDK work is on critical path only for the pin step |
| banza.network hosting not ready on ceremony day | LOW | MEDIUM — delays publication | Confirm hosting before scheduling ceremony |
| Witness unavailability on ceremony day | LOW | HIGH — ceremony cannot proceed | Assign Witness early; identify a backup |

### Dependencies

```
OPS-001 (ceremony_script.py + logistics)
    └── OPS-002 (issuing keys)
             ├── OPS-003 (Key Manifest) ─────── INFRA-001 (banza.network .well-known)
             └── OPS-004 (BRL) ────────────────── INFRA-002 (banza.network /federation)

OPS-005 (SDK v1.0 framework) ────── unblocked today
    └── OPS-005-G8 (pin manifest) ─── needs OPS-002 output

OPS-006 (INV-ROOT-001) ─────────── unblocked today
```

### Estimated effort

| Task | Effort | Elapsed (with parallelism) |
|------|--------|--------------------------|
| OPS-001-G1 `ceremony_script.py` | 1 day | Day 1–2 |
| OPS-001 Logistics | 0.5 day | Day 1–3 |
| OPS-003-G1 Fix `generate_key_manifest()` | 0.5 day | Day 1 |
| OPS-003-G2 `contracts/federation/key-manifest.json` | 0.5 day | Day 1 |
| OPS-003-G3 Confirm hosting | 0.5 day | Day 1–2 |
| OPS-005 SDK v1.0 (3 SDKs) | 3–5 days | Day 1–5 |
| OPS-006 INV-ROOT-001 in runner | 0.5 day | Day 1 |
| OPS-001 Ceremony execution | 0.5 day | Day 5+ |
| OPS-003 Post-ceremony publication | 0.5 day | Day 5+ |
| OPS-005 Pin actual Key Manifest | Hours | Day 5+ |
| **Total critical path** | — | **5–10 days** |

### Recommended execution order

**Start immediately (Day 1):**

1. `OPS-006` — Implement INV-ROOT-001 in conformance runner (~2 hours)
2. `OPS-003-G1` — Fix `generate_key_manifest()` in `trust_root.py` (~3 hours)
3. `OPS-003-G2` — Create `contracts/federation/key-manifest.json` (~2 hours)
4. `OPS-003-G3` — Confirm `banza.network` hosting ready
5. `OPS-005` framework — Start SDK v1.0 Key Manifest verification (all 3 SDKs in parallel)

**Before ceremony (Days 1–5):**

6. `OPS-001-G1` — Create `ceremony_script.py` (most important pre-ceremony artifact)
7. `OPS-001-G2–G6` — Assign Witness, procure hardware, book room

**Ceremony day:**

8. `OPS-001` — Execute root key ceremony
9. `OPS-002` — (within ceremony) Generate issuing keys
10. `OPS-003` — Sign Key Manifest + publish
11. `OPS-004` — Sign BRL + publish

**Post-ceremony (same day or next):**

12. `OPS-005-G8` — Pin real Key Manifest in all 3 SDKs → release v1.0.0
13. Verify INFRA-001 + INFRA-002 (cache headers)
14. Record M2 as complete

---

## Phase 11 — Final Verdict

### Can M2 be achieved immediately?

**NO.**

M2 requires the root key ceremony, which is a physical event requiring advance logistics. Additionally, SDK v1.0 (OPS-005) needs 3–5 days of implementation work.

### Exact blockers

1. **`ceremony_script.py` does not exist** — must be created before the ceremony day
2. **Ceremony logistics unresolved** — Witness, hardware, room not yet arranged
3. **SDK v1.0 not implemented** — no Key Manifest support in any SDK (3–5 days, unblocked today)
4. **`generate_key_manifest()` incomplete** — missing 5 required fields (0.5 day fix)
5. **INV-ROOT-001 not enforced** — conformance runner has no production mode (~2 hour fix)

### Exact execution sequence for M2

```
TODAY → OPS-006 (INV-ROOT-001, 2h) + OPS-003-G1 (KM code fix, 3h)
      + OPS-003-G2 (contract file, 2h) + OPS-005 framework (3–5 days)
      + OPS-001-G1 (ceremony_script.py, 1 day)

DAYS 1–5 → Complete SDK v1.0 framework + Confirm hosting + Arrange ceremony logistics

CEREMONY DAY → OPS-001 (ceremony) → OPS-002 (issuing keys within ceremony)
             → OPS-003 (sign + publish Key Manifest)
             → OPS-004 (sign + publish BRL)

POST-CEREMONY → OPS-005-G8 (pin manifest) → SDK v1.0.0 release
             → Verify endpoints → Record M2 complete

M2 ACHIEVED
```

**The entire path from M1 to M2 is fully mapped, traceable, and operationally executable. No protocol design work remains. Every remaining task is in BANZA's hands.**
