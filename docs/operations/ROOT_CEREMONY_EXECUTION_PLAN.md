# BANZA Root Key Ceremony — Execution Plan

**Document ID:** BANZA-OPS-CEREMONY-EXEC-PLAN-001  
**Date:** 2026-06-01  
**Authority:** ADR-029, ROOT_KEY_CEREMONY_PROCEDURE.md  
**Status:** READY TO EXECUTE — logistics pending  
**Owner:** Fidel Monteiro (Ceremony Officer)

---

## Purpose

This document is the operational execution plan for the BANZA Root Key Ceremony (OPS-001). It translates `ROOT_KEY_CEREMONY_PROCEDURE.md` into a day-by-day schedule, assigns roles, defines physical requirements, and provides the publication sequence that closes M2.

The procedure is the authoritative document. This plan is the execution roadmap.

---

## Ceremony Roles

| Role | Person | Status |
|------|--------|--------|
| **Ceremony Officer** | Fidel Monteiro | ASSIGNED |
| **Ceremony Witness** | *To be assigned* | **UNASSIGNED — BLOCKER** |
| Backup Witness (optional) | *Optional — not required* | N/A |
| Record Custodian | Fidel Monteiro (Officer) | ASSIGNED (implied) |
| GPG Passphrase Custodian | Fidel Monteiro (Officer) | ASSIGNED (implied) |
| Key Custodian 2 (Output USB B) | *To be assigned* | **UNASSIGNED — required for physical separation** |

**Quorum requirement (Procedure §Part I):** 1 Officer + 1 Witness minimum. Ceremony is invalid without both.

**Witness requirements:** Must be physically present for the entire ceremony (Phase 1 through Phase 7 inclusive). Must not touch the ceremony machine or handle private key material. Must countersign the Ceremony Record physically.

---

## Physical Equipment Checklist

Obtain and verify all items before ceremony day.

| Item | Specification | Quantity | Status |
|------|-------------|----------|--------|
| **Output USB A** | ≥8 GB. Freshly formatted as ext4. Verified empty. Label: `BANZA_KEYS_A` | 1 | **NOT PROCURED** |
| **Output USB B** | ≥8 GB. Freshly formatted as ext4. Verified empty. Label: `BANZA_KEYS_B` | 1 | **NOT PROCURED** |
| **Ceremony USB** | ≥8 GB. Write-protected after loading. Contains Python virtualenv + ceremony scripts. | 1 | **NOT PREPARED** |
| **Publication USB** | ≥1 GB. Clean, verified empty. Label: `BANZA_PUB` | 1 | **NOT PROCURED** |
| **Air-gapped machine** | Laptop or desktop. No permanent network interface (WiFi removed/disabled at hardware level, no Ethernet). Linux live OS preferred (Tails or Ubuntu 22.04+ live USB). | 1 | **NOT CONFIRMED** |
| **Offline printer** | No network, no WiFi. Functional. Ink and paper loaded. | 1 | **NOT CONFIRMED** |
| **Camera/recorder** | Witness's camera or phone. Positioned to capture Officer's hands and screen — not close enough to read key bytes. | 1 | NOT ASSESSED |

---

## Ceremony Room Requirements

| Requirement | Specification | Status |
|-------------|-------------|--------|
| **Location** | Private room with lockable door | **NOT IDENTIFIED** |
| **Network isolation** | No wired Ethernet in room during ceremony. No WiFi router in range, or router powered off. | UNKNOWN — room not selected |
| **Window security** | No windows accessible from outside, or windows covered during ceremony | UNKNOWN — room not selected |
| **Physical security** | Door lockable from inside. No unauthorized entry possible during ceremony. | UNKNOWN — room not selected |

---

## Pre-Ceremony Preparation (Day Before)

Estimated duration: **2 hours**

### Step P0.1 — Procure and Format USB Drives

```bash
# Format Output USB A
sudo mkfs.ext4 -L BANZA_KEYS_A /dev/sdX
# Verify empty
ls /media/BANZA_KEYS_A/

# Format Output USB B
sudo mkfs.ext4 -L BANZA_KEYS_B /dev/sdY
# Verify empty
ls /media/BANZA_KEYS_B/

# Format Publication USB
# (any filesystem — FAT32 acceptable for portability)
sudo mkfs.fat -n BANZA_PUB /dev/sdZ
```

### Step P0.2 — Prepare Ceremony USB

```bash
# Install Python virtualenv on Ceremony USB
python3 -m venv /media/ceremony-usb/venv
source /media/ceremony-usb/venv/bin/activate
pip install "cryptography>=41.0.0"
deactivate

# Copy ceremony software
cp ~/banza/tools/banza-conformance/trust_root.py /media/ceremony-usb/
cp ~/banza/tools/root-ceremony/ceremony_script.py /media/ceremony-usb/
```

### Step P0.3 — Record Software Hashes

```bash
sha256sum /media/ceremony-usb/trust_root.py > /media/ceremony-usb/SOFTWARE_HASHES.txt
sha256sum /media/ceremony-usb/ceremony_script.py >> /media/ceremony-usb/SOFTWARE_HASHES.txt
python3 -c "import cryptography; print('cryptography', cryptography.__version__)" >> /media/ceremony-usb/SOFTWARE_HASHES.txt
cat /media/ceremony-usb/SOFTWARE_HASHES.txt
```

Record the three hash/version values in the Ceremony Record Template (Section 4) before printing it.

### Step P0.4 — Print Documents

Print the following, on the offline printer or any printer (not sensitive yet — no key material exists):

| Document | Copies |
|----------|--------|
| `ROOT_KEY_CEREMONY_CHECKLIST.md` | 1 |
| `ROOT_KEY_CEREMONY_RECORD_TEMPLATE.md` | 1 |
| This execution plan (optional reference) | 1 |

### Step P0.5 — Confirm Participants

- Officer and Witness confirm availability and arrival time.
- Both have read `ROOT_KEY_CEREMONY_PROCEDURE.md` in full.
- Officer has reviewed all ceremony commands.
- GPG passphrase agreed upon and secured (NOT written anywhere accessible — verbal or separate sealed document).
- Key custodian for Output USB B identified (physically separate storage location agreed).

---

## Ceremony Day Schedule

Estimated total duration: **90 minutes** (including buffer)

| Phase | Content | Estimated time |
|-------|---------|---------------|
| Phase 0 — Opening | Participant assembly, identity verification, mobile devices secured, door locked, camera started | 5 min |
| Phase 1 — Environment audit | Network isolation confirmed, software hashes verified, ceremony start time recorded | 5 min |
| Phase 2 — Key ID determination | Key IDs printed and recorded by Witness | 2 min |
| Phase 3 — Root keypair generation | Root key generated; fingerprint read aloud, recorded | 5 min |
| Phase 4 — Issuing keypair generation | 3 issuing keys generated; all fingerprints recorded | 5 min |
| Phase 5 — Key Manifest construction | Manifest built, signed, in-memory verification | 10 min |
| Phase 6 — Initial BRL construction | BRL built and signed | 5 min |
| Phase 7 — Key material storage | Write to USB A, GPG encryption, clone to USB B, paper backup printed and signed | 15 min |
| Phase 8 — Public artifact preparation | Export to Publication USB, create ceremony-record.json | 5 min |
| Phase 9 — Final verification | `--verify-artifacts` — all 10 checks | 10 min |
| Phase 10 — Ceremony close | Memory zeroing, machine poweroff, USB custody, close declaration | 10 min |
| **Total** | | **77 min + 13 min buffer** |

### Execution Commands (on the air-gapped machine)

```bash
cd /media/ceremony-usb
source venv/bin/activate
WORKDIR=/media/BANZA_KEYS_A/ceremony-session

# Phase 2.1–2.2 — Root key
python3 ceremony_script.py --workdir $WORKDIR --generate-root

# Phase 2.3–2.5 — Issuing keys
python3 ceremony_script.py --workdir $WORKDIR --generate-issuing-keys

# Phase 3.1–3.2 — Key Manifest (signs + verifies in-memory)
python3 ceremony_script.py --workdir $WORKDIR --generate-key-manifest

# Phase 3.3 — Initial BRL
python3 ceremony_script.py --workdir $WORKDIR --generate-initial-brl

# Phase 4.5 + 5.2 — Ceremony record + paper backup
python3 ceremony_script.py --workdir $WORKDIR --create-record
# → Print paper_backup.txt → Officer + Witness sign physically

# Phase 5.1 — Export to Publication USB
python3 ceremony_script.py --workdir $WORKDIR --export-public /media/BANZA_PUB/publish/

# Phase 6 — Final verification (MUST pass before Phase 7)
python3 ceremony_script.py --workdir $WORKDIR --verify-artifacts
# Exit 0 = ALL PASS → proceed to Phase 7 (ceremony close)
# Exit 1 = FAIL → STOP — follow failure procedure (Procedure §Part VI)
```

After `--verify-artifacts` exits 0:

```bash
# Phase 7.1 — GPG encrypt private key directory
tar -czf /tmp/private_keys.tar.gz -C $WORKDIR private/
gpg --cipher-algo AES256 --symmetric --output $WORKDIR/private_keys_encrypted.gpg /tmp/private_keys.tar.gz
shred -u /tmp/private_keys.tar.gz
rm -rf $WORKDIR/private/

# Phase 4.4 — Clone to Output USB B
mkdir -p /media/BANZA_KEYS_B/ceremony-session/
cp -r $WORKDIR/public/ /media/BANZA_KEYS_B/ceremony-session/public/
cp $WORKDIR/private_keys_encrypted.gpg /media/BANZA_KEYS_B/ceremony-session/
```

---

## Publication Sequence (Post-Ceremony)

Execute on an online machine using the Publication USB. This is the final step before M2.

| Step | Action | Required before |
|------|--------|----------------|
| P.1 | Decrypt BRL-issuing key from Output USB A; re-sign BRL with 6h expiry | P.4 |
| P.2 | Upload `key-manifest.json` to `banza.network/.well-known/banza/key-manifest.json` | P.3, SDK v1.0 |
| P.3 | Verify Key Manifest endpoint (schema, `root_key_id`, `manifest_signature` present) | — |
| P.4 | Upload re-signed BRL to `banza.network/federation/revocation-list.json` | P.5 |
| P.5 | Verify BRL endpoint (issuer, 0 revoked, correct `issuer_key_id`) | — |
| P.6 | Pin Key Manifest in SDK; release SDK v1.0.0 | M2 |
| P.7 | Record M2 complete in `BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md` | — |

### P.1 — Re-sign BRL for Publication

The ceremony BRL has a 7-hour expiry. Re-sign immediately before publishing:

```python
# On a secure online machine — load BRL-issuing private key from decrypted backup
from tools.banza_conformance.trust_root import generate_signed_brl
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption

# Load brl_priv_bytes from decrypted Output USB A backup
brl_priv = Ed25519PrivateKey.from_private_bytes(brl_priv_bytes)

pub_brl = generate_signed_brl(
    brl_private_key=brl_priv,
    key_id="banza-brl-YYYYMM",   # actual key ID from ceremony
    revoked=[],
    expires_hours=6
)
```

### P.2 — Verify endpoints

```bash
# Key Manifest
curl -s https://banza.network/.well-known/banza/key-manifest.json | \
  python3 -c "import json,sys; m=json.load(sys.stdin); print('schema_version:', m['schema_version']); print('root_key_id:', m['root_key_id']); print('signature present:', bool(m.get('manifest_signature')))"

# BRL
curl -s https://banza.network/federation/revocation-list.json | \
  python3 -c "import json,sys; b=json.load(sys.stdin); print('issuer:', b['issuer']); print('issuer_key_id:', b['issuer_key_id']); print('revoked:', len(b['revoked']))"
```

---

## Outstanding Actions Before Scheduling

All items below must be completed before a ceremony date can be set. All are executable today.

| Priority | Action | Effort | Owner |
|----------|--------|--------|-------|
| **CRITICAL** | Assign Ceremony Witness | Hours | Fidel Monteiro |
| **CRITICAL** | Procure 4 USB drives (≥8GB × 3, ≥1GB × 1) | Hours | Fidel Monteiro |
| **CRITICAL** | Identify and verify air-gapped machine | Hours | Fidel Monteiro |
| **CRITICAL** | Identify and book ceremony room | Hours | Fidel Monteiro |
| HIGH | Confirm offline printer functional | Minutes | Fidel Monteiro |
| HIGH | Agree GPG passphrase and custody method | Minutes | Fidel Monteiro |
| HIGH | Identify Key Custodian 2 (Output USB B separate location) | Hours | Fidel Monteiro |
| MEDIUM | Prepare Ceremony USB (virtualenv + scripts + hashes) | 1 hour | Fidel Monteiro (day before) |

---

## Earliest Execution Date

**Day 0 (today, 2026-06-01):** Resolve all CRITICAL items above (Witness, USB drives, machine, room).  
**Day 1 (2026-06-02):** Prepare Ceremony USB; print documents; confirm participants. Execute ceremony.

**Minimum elapsed time to ceremony:** 1 day from today, if all logistics resolved today.  
**Realistic estimate:** 1–3 days from today.

After ceremony, M2 can close **same day** (publication sequence takes ~1 hour, SDK pin takes hours if framework is pre-built).

---

## Companion Documents

| Document | Location |
|----------|----------|
| Procedure | `docs/security/ROOT_KEY_CEREMONY_PROCEDURE.md` |
| Checklist (print on ceremony day) | `docs/security/ROOT_KEY_CEREMONY_CHECKLIST.md` |
| Record Template (print on ceremony day) | `docs/security/ROOT_KEY_CEREMONY_RECORD_TEMPLATE.md` |
| Ceremony script | `tools/root-ceremony/ceremony_script.py` |
| Script report | `docs/security/CEREMONY_SCRIPT_REPORT.md` |
| M2 tracker | `docs/operations/M2_PRODUCTION_TRUST_TRACKER.md` |
| Readiness report | `docs/operations/ROOT_CEREMONY_READINESS_REPORT.md` |
