# BANZA Root Key Ceremony — Readiness Report

**Document ID:** BANZA-OPS-CEREMONY-READINESS-001  
**Date:** 2026-06-01  
**Authority:** ADR-029, ROOT_KEY_CEREMONY_PROCEDURE.md  
**Assessment basis:** ROOT_KEY_CEREMONY_PROCEDURE.md, ROOT_KEY_CEREMONY_CHECKLIST.md, ROOT_KEY_CEREMONY_RECORD_TEMPLATE.md, CEREMONY_SCRIPT_REPORT.md, M2_PRODUCTION_TRUST_TRACKER.md  
**Status:** ACTIVE — schedule pending

---

## Executive Summary

The BANZA Root Key Ceremony (OPS-001) is technically complete and verified. All software is built, all documents are approved, and the dry-run completed with 10/10 verifications passing. No technical uncertainty remains.

The ceremony cannot be executed today for logistical reasons only: the Ceremony Witness has not been assigned, four USB drives have not been procured, an air-gapped machine has not been identified, and the ceremony room has not been booked. All remaining blockers are resolved with hours of effort, not days.

**The ceremony can be scheduled for 2026-06-02** if all logistics are resolved on 2026-06-01.

---

## Phase 2 — Readiness Matrix

### Personnel

| Item | Classification | Detail |
|------|--------------|--------|
| Ceremony Officer | **READY** | Fidel Monteiro assigned |
| Ceremony Witness | **BLOCKED** | Not assigned — ceremony invalid without a Witness (quorum = 1 Officer + 1 Witness) |
| Backup Witness | N/A | Optional; not required for initial ceremony |
| GPG Passphrase Custodian | **PARTIAL** | Implied to be Officer — passphrase not yet decided or secured |
| Key Custodian 2 (USB B) | **PARTIAL** | No second custodian identified; physically separate storage location not confirmed |
| Record Custodian | **PARTIAL** | Implied to be Officer; governance repository storage location not confirmed |

### Equipment

| Item | Classification | Detail |
|------|--------------|--------|
| Air-gapped ceremony machine | **BLOCKED** | Not identified or verified |
| Output USB A (BANZA_KEYS_A, ≥8GB) | **BLOCKED** | Not procured |
| Output USB B (BANZA_KEYS_B, ≥8GB) | **BLOCKED** | Not procured |
| Ceremony USB (software, ≥8GB) | **PARTIAL** | ceremony_script.py exists; virtualenv not yet loaded onto USB |
| Publication USB (BANZA_PUB, ≥1GB) | **BLOCKED** | Not procured |
| Offline printer | **PARTIAL** | Not confirmed functional; required for paper backup and document printing |
| Camera/recorder | NOT ASSESSED | Recommended by Procedure; availability not confirmed |

### Environment

| Item | Classification | Detail |
|------|--------------|--------|
| Secure ceremony room | **BLOCKED** | Not identified; must have lockable door, no external window access |
| Network isolation capability | **PARTIAL** | Unknown — depends on room selection |
| Physical security | **PARTIAL** | Unknown — depends on room selection |
| Document printing ready | **PARTIAL** | Offline printer not confirmed |

### Software

| Item | Classification | Detail |
|------|--------------|--------|
| `ceremony_script.py` | **READY** | `tools/root-ceremony/ceremony_script.py` — dry-run 10/10 PASS |
| `trust_root.py` | **READY** | Correct algorithm; all functions verified |
| Python 3.9+ | **PARTIAL** | Available on dev machines; not confirmed on ceremony machine |
| `cryptography >= 41.0.0` | **PARTIAL** | Available on dev machines; virtualenv not yet loaded on Ceremony USB |
| `SOFTWARE_HASHES.txt` on Ceremony USB | **BLOCKED** | Not yet recorded — requires Ceremony USB to be prepared |
| ADR-029 version consistency | **READY** | All four documents consistent with same ADR-029 version |

### Documentation

| Item | Classification | Detail |
|------|--------------|--------|
| `ROOT_KEY_CEREMONY_PROCEDURE.md` | **READY** | FINAL, approved for execution; procedure path defect fixed (see Phase 5) |
| `ROOT_KEY_CEREMONY_CHECKLIST.md` | **READY** | Ready to print |
| `ROOT_KEY_CEREMONY_RECORD_TEMPLATE.md` | **READY** | Ready to print |
| `CEREMONY_SCRIPT_REPORT.md` | **READY** | Dry-run output documented |
| Documents printed | **BLOCKED** | Not yet printed; depends on printer confirmation |
| Pre-ceremony software hashes recorded in template | **BLOCKED** | Not yet done — requires Ceremony USB preparation first |

### Recovery

| Item | Classification | Detail |
|------|--------------|--------|
| Failure procedures | **READY** | Documented in ROOT_KEY_CEREMONY_PROCEDURE.md §Part VI |
| Ceremony suspension procedures | **READY** | Documented in Procedure §Part VI |
| Network breach procedures | **READY** | Documented in Procedure §Part VI |
| GPG passphrase backup plan | **PARTIAL** | No second custodian or storage method decided |
| USB B separate storage location | **PARTIAL** | No physically separate location identified for custodian 2 |

---

## Phase 3 — Ceremony Role Assignments

| Role | Requirement (Procedure §Part I) | Assigned Person | Status |
|------|-------------------------------|----------------|--------|
| **Ceremony Officer** | 1 required. Executes all commands. Sole custody of ceremony machine. Records all outputs. | **Fidel Monteiro** | **ASSIGNED** |
| **Ceremony Witness** | 1 required minimum. Observes all steps. Countersigns Ceremony Record. Does NOT touch ceremony machine. | *Not assigned* | **UNASSIGNED — HARD BLOCKER** |
| Backup Witness | Optional. Same rules as Witness. | — | Not required |

**Quorum rule:** A ceremony executed by 1 person with no Witness is invalid per Procedure §Part I. This is a hard requirement — the ceremony cannot begin without an assigned, present Witness.

**Witness constraints:**
- Must be physically present for the entire ceremony (Phases 1 through 7)
- Must not leave the room between key generation and key storage completion
- Must not touch the ceremony machine or handle private key material
- Must sign the Ceremony Record physically

---

## Phase 4 — Physical Requirements Verification

| Item | Required per Procedure | Current status |
|------|----------------------|---------------|
| Air-gapped machine | Laptop/desktop, no network interface (hardware-disabled), Linux live OS | **NOT CONFIRMED** |
| Output USB A | ≥8 GB, freshly formatted ext4, verified empty, labeled `BANZA_KEYS_A` | **NOT PROCURED** |
| Output USB B | ≥8 GB, freshly formatted ext4, verified empty, labeled `BANZA_KEYS_B` | **NOT PROCURED** |
| Ceremony USB | ≥8 GB, write-protected after loading, Python venv + scripts | **NOT PREPARED** |
| Publication USB | ≥1 GB, clean, labeled `BANZA_PUB` | **NOT PROCURED** |
| Offline printer | No network, functional, ink loaded | **NOT CONFIRMED** |
| Camera/recorder | Witness-controlled, positioned to capture process not screen details | **NOT ASSESSED** |
| Ceremony room | Lockable door, no external network, covered/secure windows | **NOT IDENTIFIED** |

**Minimum procurement:** 4 USB drives (≥8GB × 3 + ≥1GB × 1). Any standard USB drives from a consumer electronics store suffice.

**Air-gapped machine options:**
1. An existing laptop with WiFi hardware-disabled (BIOS setting or physical switch)
2. A Tails OS live USB booted on any machine — Tails disables all persistent network by default
3. An older machine with its network card physically removed

---

## Phase 5 — Execution Package Verification

Cross-reference of `ceremony_script.py` commands against `ROOT_KEY_CEREMONY_PROCEDURE.md` phases, verifying all four documents reference the same ADR-029 version.

| Procedure phase | ceremony_script.py command | Consistency |
|----------------|--------------------------|------------|
| Phase 2.1–2.2 — Determine key IDs + generate root | `--generate-root` | ✓ Identical key ID format: `banza-root-YYYY`, `banza-cert-YYYYMM`, etc. |
| Phase 2.3–2.5 — Generate issuing keys | `--generate-issuing-keys` | ✓ 3 issuing keys, same names |
| Phase 3.1–3.2 — Construct + sign Key Manifest | `--generate-key-manifest` | ✓ Identical structure: `schema_version`, `published_at`, `root_key_id`, `root_public_key`, `expires_at` (730 days), `keys` array with `domain`/`active_since`/`expires_at`/`status`, `manifest_signature` |
| Phase 3.3 — Construct initial BRL | `--generate-initial-brl` | ✓ Identical structure: `schema_version`, `issuer`, `issuer_key_id`, `issued_at`, `expires_at` (7h), `revoked: []`, `signature` |
| Phase 4.5 — Paper backup | `--create-record` | ✓ Same fields: all 4 key IDs, all 4 fingerprints, MANIFEST_HASH, BRL_HASH |
| Phase 5.1 — Export to Publication USB | `--export-public DIR` | ✓ Private key exclusion check in both |
| Phase 5.2 — Ceremony record JSON | `--create-record` | ✓ Same JSON structure: `ceremony_id`, `root_key_id`, `root_key_fingerprint`, `root_public_key`, `issuing_keys`, hashes, `officer`, `witness` |
| Phase 6 — Final verification | `--verify-artifacts` | ✓ 10 checks: manifest sig, BRL sig, hash integrity, INV-ROOT-001, INV-ROOT-006, publication dir |

**Invariant enforcement consistency:**

| Invariant | Procedure | ceremony_script.py | Match |
|-----------|-----------|-------------------|-------|
| INV-ROOT-001 | §6.3: key IDs must not start with `test-` | Step 6.3: `assert not key_id.startswith("test-")` (production mode) | ✓ |
| INV-ROOT-002 | §3.2: verify manifest_signature before proceeding | `--generate-key-manifest` verifies in-memory + `--verify-artifacts` verifies from disk | ✓ |
| INV-ROOT-004 | §3.1: root key signs Key Manifest only; BRL signed by `brl_priv` | Root key used only in `--generate-key-manifest`; BRL uses BRL key | ✓ |
| INV-ROOT-006 | §6.4: issuing key validity ≤ 184 days | Step 6.4: `assert days <= 184`; uses 183 days in generation | ✓ |

**ADR-026 canonical JSON rule:** Both procedure and script use `json.dumps(payload, sort_keys=True, separators=(',',':')).encode('utf-8')` for all signing operations. ✓

**Domain values:** Procedure §3.1 uses `"certification"`, `"revocation"`, `"conformance-evidence"`. Script uses identical values. ✓

**Procedure path defect (FIXED):** Step 0.1 referenced `tools/banza-conformance/ceremony_script.py`. The correct path is `tools/root-ceremony/ceremony_script.py`. Fixed in this session.

**All four documents are consistent with ADR-029. The execution package is verified.** ✓

---

## Phase 6 — Ceremony Schedule Proposal

### Duration Estimates

| Period | Content | Duration |
|--------|---------|----------|
| **Preparation (day before)** | USB formatting, Ceremony USB prep, hash recording, document printing, participant confirmation | **~2 hours** |
| **Ceremony execution** | Phases 0–10 (see execution plan schedule) | **~77 minutes** |
| **Verification** | `--verify-artifacts` (included in Phase 9 above) | included |
| **Publication preparation** | BRL re-sign, Key Manifest upload, BRL upload, endpoint verification | **~1 hour** |
| **SDK pin + release** | Pin Key Manifest in SDK code; release v1.0.0 (if framework built in advance) | **~2–4 hours** |

### Proposed Schedule

```
Day 0 — TODAY (2026-06-01)
  ├── Assign Ceremony Witness                     [hours — CRITICAL]
  ├── Procure 4 USB drives                        [hours — CRITICAL]
  ├── Identify air-gapped machine                 [hours — CRITICAL]
  ├── Book ceremony room                          [hours — CRITICAL]
  ├── Confirm offline printer                     [minutes — HIGH]
  └── Decide GPG passphrase custody              [minutes — HIGH]

Day 1 — CEREMONY DAY (2026-06-02, earliest)
  ├── Morning (2h): Prepare Ceremony USB, print documents, record hashes
  ├── Ceremony (2h): Execute Phases 0–10 per procedure
  └── Afternoon (2h): Publication sequence P.1–P.5 + SDK pin → M2 COMPLETE
```

**If logistics are resolved today, M2 can be achieved on 2026-06-02.**

---

## Outstanding Action Items

All items in this table are blocking or partially blocking. All are executable within 1 day.

| Priority | ID | Action | Effort | Unblocked? |
|----------|----|--------|--------|-----------|
| **CRITICAL** | ROLE-W | Assign Ceremony Witness | Hours | Yes — immediately |
| **CRITICAL** | EQUIP-USB | Procure 4 USB drives | Hours | Yes — immediately |
| **CRITICAL** | EQUIP-MACHINE | Identify and verify air-gapped machine | Hours | Yes — immediately |
| **CRITICAL** | ENV-ROOM | Book ceremony room | Hours | Yes — immediately |
| HIGH | EQUIP-PRINT | Confirm offline printer functional | Minutes | Yes — immediately |
| HIGH | ROLE-GPG | Decide GPG passphrase and custody method | Minutes | Yes — immediately |
| HIGH | ROLE-CUST2 | Identify Key Custodian 2 + separate storage location for Output USB B | Hours | Yes — immediately |
| MEDIUM | SOFT-VENV | Prepare Ceremony USB virtualenv | 1 hour | Yes — do day before ceremony |
| MEDIUM | DOC-PRINT | Print Checklist and Record Template | Minutes | Yes — do day before ceremony |
| LOW | REF-RECORD | Confirm BANZA governance repository storage location for Ceremony Record | Hours | Yes |

---

## Phase 9 — Final Verdict

### Can the BANZA Root Key Ceremony be scheduled today?

**YES — the ceremony can be scheduled today for a date as early as 2026-06-02.**

### Can the ceremony be executed today (2026-06-01)?

**NO.** Seven prerequisites are not yet satisfied:

| # | Blocker | Classification |
|---|---------|--------------|
| 1 | Ceremony Witness not assigned | HARD BLOCKER — ceremony is invalid without Witness |
| 2 | Air-gapped machine not identified | HARD BLOCKER — ceremony machine is required |
| 3 | Output USB A not procured | HARD BLOCKER — key material cannot be stored without it |
| 4 | Output USB B not procured | HARD BLOCKER — redundant backup required |
| 5 | Publication USB not procured | HARD BLOCKER — public artifacts cannot be transported |
| 6 | Ceremony room not identified | HARD BLOCKER — physical isolation required |
| 7 | Ceremony USB not prepared | SOFT BLOCKER — requires ~1h prep day before |

### What is ready

| Category | Status |
|----------|--------|
| Ceremony software (`ceremony_script.py`) | COMPLETE — dry-run verified 10/10 |
| Ceremony procedure | COMPLETE — FINAL, approved, path defect fixed |
| Ceremony checklist | COMPLETE — ready to print |
| Ceremony record template | COMPLETE — ready to print |
| Ceremony Officer | ASSIGNED — Fidel Monteiro |
| All cryptographic design decisions | FINALIZED — ADR-029 accepted |
| All invariants (INV-ROOT-001 through 006) | DOCUMENTED and enforced in ceremony script |
| Failure procedures | DOCUMENTED — Procedure §Part VI |
| Publication sequence | DOCUMENTED — Procedure §Part VII |
| Post-ceremony M2 completion path | DOCUMENTED — OPS-003, OPS-004, OPS-005, OPS-006 all unblocked |

### What remains

All remaining items are **operational logistics**, not technical work. No code needs to be written. No design decisions remain open. The ceremony can execute as soon as the physical prerequisites are assembled.

**Minimum path to ceremony execution:**
1. Assign Witness → today
2. Procure 4 USB drives → today
3. Identify air-gapped machine → today
4. Book ceremony room → today
5. Confirm printer → today
6. Prepare Ceremony USB → morning of ceremony day

**Earliest achievable ceremony date: 2026-06-02**  
**M2 achievable: 2026-06-02** (same day, if SDK framework is pre-built)

---

*No technical uncertainty remains. Only operational execution remains.*
