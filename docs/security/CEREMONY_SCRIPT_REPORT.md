# BANZA Root Key Ceremony Script — Automation Report

**Document ID:** BANZA-ROOT-KEY-CEREMONY-AUTOMATION-001  
**Date:** 2026-06-01  
**Authority:** ADR-029, ROOT_KEY_CEREMONY_PROCEDURE.md  
**Status:** COMPLETE — Dry-run verified  
**Script:** `tools/root-ceremony/ceremony_script.py`

---

## Executive Summary

The ceremony script automates all deterministic cryptographic steps of the BANZA Root Key Ceremony. Human steps — identity verification, environment audit, physical storage handling, and witness signatures — remain manual and are not automated.

**Gap OPS-001-G1 from M2_PRODUCTION_TRUST_TRACKER.md:** RESOLVED.

| Question | Answer |
|----------|--------|
| Does the script implement all phases from the Procedure? | **YES** — Phases 2–6 fully automated |
| Does the dry-run complete successfully? | **YES** — all verifications PASS |
| Are all artifact structures ADR-029 compliant? | **YES** |
| Does the script exit non-zero on verification failure? | **YES** |
| Does it protect private keys from the publication directory? | **YES** — verified in Phase 6.5 |
| Is the script portable to an air-gapped machine? | **YES** — stdlib + cryptography only |

---

## Script Location

```
tools/root-ceremony/ceremony_script.py
```

The script must be copied to the Ceremony USB before the ceremony:

```bash
cp ~/banza/tools/root-ceremony/ceremony_script.py /media/ceremony-usb/
```

---

## Commands

| Command | Procedure Phase | Description |
|---------|----------------|-------------|
| `--generate-root` | Phase 2.1–2.2 | Determine key IDs; generate root ed25519 keypair |
| `--generate-issuing-keys` | Phase 2.3–2.5 | Generate cert, brl, evidence issuing keypairs |
| `--generate-key-manifest` | Phase 3.1–3.2 | Construct, sign, and verify Key Manifest |
| `--generate-initial-brl` | Phase 3.3 | Construct and sign initial BRL (7h expiry) |
| `--verify-artifacts` | Phase 6 | Full disk verification of all artifacts |
| `--export-public DIR` | Phase 5.1 | Export public artifacts to Publication USB |
| `--create-record` | Phase 4.5 + 5.2 | Generate ceremony-record.json + paper backup |
| `--print-state` | Anytime | Print session state summary |

**Options:**

| Option | Description |
|--------|-------------|
| `--workdir DIR` | Ceremony work directory (default: `ceremony-workdir-YYYYMMDD`) |
| `--dry-run` | Use `test-` key IDs — DRY RUN ONLY, never for production |

---

## Ceremony Execution Workflow

### Setup (Day Before)

```bash
# On any machine — record software hashes
sha256sum tools/root-ceremony/ceremony_script.py
sha256sum tools/banza-conformance/trust_root.py
```

Copy to Ceremony USB:

```bash
cp tools/root-ceremony/ceremony_script.py /media/ceremony-usb/
cp tools/banza-conformance/trust_root.py /media/ceremony-usb/
```

### On the Air-Gapped Ceremony Machine

```bash
cd /media/ceremony-usb
source venv/bin/activate
WORKDIR=/media/output-usb-a/ceremony-session

# Phase 2.1-2.2 — Root key generation
python3 ceremony_script.py --workdir $WORKDIR --generate-root

# Phase 2.3-2.5 — Issuing key generation
python3 ceremony_script.py --workdir $WORKDIR --generate-issuing-keys

# Phase 3.1-3.2 — Key Manifest construction + signing
python3 ceremony_script.py --workdir $WORKDIR --generate-key-manifest

# Phase 3.3 — Initial BRL construction + signing
python3 ceremony_script.py --workdir $WORKDIR --generate-initial-brl

# Phase 5.2 + 4.5 — Ceremony record + paper backup
python3 ceremony_script.py --workdir $WORKDIR --create-record
# → Print paper_backup.txt on offline printer → Officer + Witness sign

# Phase 6 — Final verification (must pass before Phase 7)
python3 ceremony_script.py --workdir $WORKDIR --verify-artifacts
# → Exit 0 = ALL PASS → proceed to Phase 7
# → Exit 1 = FAIL → abort per Procedure §Part VI

# Phase 5.1 — Export public artifacts to Publication USB
python3 ceremony_script.py --workdir $WORKDIR --export-public /media/pub-usb/publish/

# Anytime — print current state
python3 ceremony_script.py --workdir $WORKDIR --print-state
```

After Phase 7 (storage and encryption) — executed manually per Procedure §Phase 4:

```bash
# Encrypt private key directory
tar -czf /tmp/private_keys.tar.gz -C $WORKDIR private/
gpg --cipher-algo AES256 --symmetric --output $WORKDIR/private_keys_encrypted.gpg /tmp/private_keys.tar.gz
shred -u /tmp/private_keys.tar.gz
rm -rf $WORKDIR/private/
```

---

## Generated Artifacts

### From Dry-Run Session (2026-05-31)

```
ceremony-workdir/
├── ceremony_state.json       # Session state (key IDs, public keys, fingerprints, hashes)
├── paper_backup.txt          # Printable paper backup (no private key material)
├── private/                  # PRIVATE — encrypt before leaving ceremony machine
│   ├── test-banza-root-2026.private
│   ├── test-banza-cert-202605.private
│   ├── test-banza-brl-202605.private
│   └── test-banza-evidence-202605.private
└── public/                   # PUBLIC — safe to export
    ├── key-manifest.json
    ├── initial-brl.json
    ├── ceremony-record.json
    ├── test-banza-root-2026.public
    ├── test-banza-cert-202605.public
    ├── test-banza-brl-202605.public
    └── test-banza-evidence-202605.public
```

### key-manifest.json (dry-run output)

```json
{
  "expires_at": "2028-05-30T22:58:15Z",
  "keys": [
    {
      "active_since": "2026-05-31T22:58:15Z",
      "domain": "certification",
      "expires_at": "2026-11-30T22:58:15Z",
      "key_id": "test-banza-cert-202605",
      "public_key": "ed25519:0ZT7ncyIgXvqdbKQegwSM_61895PwqHSOO11s0ldnnY",
      "status": "active"
    },
    {
      "active_since": "2026-05-31T22:58:15Z",
      "domain": "revocation",
      "expires_at": "2026-11-30T22:58:15Z",
      "key_id": "test-banza-brl-202605",
      "public_key": "ed25519:k2p2zNPsHHgoKEQZCHxnrFWX1cyKkWYMgcptifOjUcI",
      "status": "active"
    },
    {
      "active_since": "2026-05-31T22:58:15Z",
      "domain": "conformance-evidence",
      "expires_at": "2026-11-30T22:58:15Z",
      "key_id": "test-banza-evidence-202605",
      "public_key": "ed25519:U5kPb_ZKyEndHhl1V25RBdR0b02FCCtdVHkMkW2MklA",
      "status": "active"
    }
  ],
  "manifest_signature": "...(86 chars, ed25519 over canonical JSON)...",
  "published_at": "2026-05-31T22:58:15Z",
  "root_key_id": "test-banza-root-2026",
  "root_public_key": "ed25519:j_OmIwELAyuDHHEFQv9z40Cee8qHKsP_5tjWPQhJfmE",
  "schema_version": "1"
}
```

### initial-brl.json (dry-run output)

```json
{
  "expires_at": "2026-06-01T05:58:22Z",
  "issued_at": "2026-05-31T22:58:22Z",
  "issuer": "BANZA",
  "issuer_key_id": "test-banza-brl-202605",
  "revoked": [],
  "schema_version": "1",
  "signature": "...(86 chars, ed25519 over canonical JSON)..."
}
```

---

## Dry-Run Verification Output

```
Step 6.1 — Disk Key Manifest Signature Verification
  ✓ Manifest signature (ed25519): PASS
  ✓ Manifest SHA-256 matches state: PASS

Step 6.2 — Disk BRL Signature Verification
  ✓ BRL signature (ed25519): PASS
  ✓ BRL SHA-256 matches state: PASS

Step 6.3 — Key ID Format Check (INV-ROOT-001)
  ✓ Key ID format [test-banza-root-2026]: PASS  (DRY RUN — test- prefix expected)
  ✓ Key ID format [test-banza-cert-202605]: PASS  (DRY RUN — test- prefix expected)
  ✓ Key ID format [test-banza-brl-202605]: PASS  (DRY RUN — test- prefix expected)
  ✓ Key ID format [test-banza-evidence-202605]: PASS  (DRY RUN — test- prefix expected)

Step 6.4 — Issuing Key Validity Check (INV-ROOT-006)
  ✓ Issuing key validity [test-banza-cert-202605]: PASS  (183 days ≤ 184)
  ✓ Issuing key validity [test-banza-brl-202605]: PASS  (183 days ≤ 184)
  ✓ Issuing key validity [test-banza-evidence-202605]: PASS  (183 days ≤ 184)

Step 6.5 — Publication Directory Private Key Exclusion
  ✓ Publication directory has no .private files: PASS

ALL VERIFICATIONS PASS
```

---

## Procedure Coverage

| Procedure Phase | Automated? | Command | Notes |
|----------------|:----------:|---------|-------|
| Phase 0 — Pre-ceremony preparation | Partial | (setup only) | USB formatting, hash recording: manual |
| Phase 1 — Ceremony opening | No | — | Identity verification, environment audit, software hash check: manual |
| Phase 2.1 — Determine key IDs | Yes | `--generate-root` | Computed from UTC clock |
| Phase 2.2 — Generate root keypair | Yes | `--generate-root` | ed25519, stored to workdir |
| Phase 2.3 — Generate cert-issuing keypair | Yes | `--generate-issuing-keys` | ed25519, stored to workdir |
| Phase 2.4 — Generate BRL-issuing keypair | Yes | `--generate-issuing-keys` | ed25519, stored to workdir |
| Phase 2.5 — Generate evidence-issuing keypair | Yes | `--generate-issuing-keys` | ed25519, stored to workdir |
| Phase 3.1 — Construct Key Manifest | Yes | `--generate-key-manifest` | Full ADR-029 structure |
| Phase 3.2 — Verify manifest signature (in-memory) | Yes | `--generate-key-manifest` | Abort on failure |
| Phase 3.3 — Construct initial BRL | Yes | `--generate-initial-brl` | 7h expiry (re-sign before publish) |
| Phase 4.1 — Write private keys to USB A | Partial | (workdir/private/) | GPG encryption step: manual |
| Phase 4.2 — Verify USB A hashes | Yes | `--verify-artifacts` | SHA-256 match verified |
| Phase 4.3 — Encrypt USB A | No | — | GPG passphrase: manual (human custody) |
| Phase 4.4 — Clone to USB B | No | — | Filesystem copy: manual |
| Phase 4.5 — Paper backup | Yes | `--create-record` | Printed text; physical signatures: manual |
| Phase 5.1 — Export to Publication USB | Yes | `--export-public DIR` | Private key exclusion verified |
| Phase 5.2 — Create ceremony-record.json | Yes | `--create-record` | Skeleton; officer/witness names: manual |
| Phase 6 — Final verification | Yes | `--verify-artifacts` | All 5 checks; exit 0/1 |
| Phase 7 — Ceremony close | No | — | Machine wipe, USB custody: manual |

**Steps intentionally not automated:**
- Identity verification (human attestation required)
- Environment audit (physical inspection required)
- Software hash comparison (manual comparison is the security check)
- GPG encryption (passphrase must not appear in script output)
- USB cloning to USB B (manual file copy on air-gapped machine)
- Machine wipe (OS-level operation, site-specific)
- Physical signatures (legal attestation requires human execution)

---

## Security Properties

| Property | Implementation |
|----------|---------------|
| No network access | Script uses no network calls; stdlib + cryptography only |
| Exit non-zero on failure | All verification steps: `sys.exit(1)` on any FAIL |
| Private keys never in stdout | Fingerprints printed; raw key bytes never logged |
| Publication USB private key check | `--verify-artifacts` step 6.5; `--export-public` checks for `.private` files |
| Dry-run distinct from production | `--dry-run` uses `test-` prefix; production mode checks `not key_id.startswith("test-")` |
| State persisted between phases | `ceremony_state.json` in workdir — public-key material only; private keys in `private/` |
| Idempotent phase protection | `--generate-root` aborts if root key already generated in session |

---

## Invariants Enforced

| Invariant | Check |
|-----------|-------|
| INV-ROOT-001 | Production mode: key IDs must NOT start with `test-` |
| INV-ROOT-002 | Key Manifest signature verified before and after disk write |
| INV-ROOT-004 | Root key signs Key Manifest only — not certificates or BRLs |
| INV-ROOT-006 | Issuing key validity ≤ 184 days (6 months) asserted in Phase 6.4 |

---

## Ceremony Workflow Map

```
Day before:
  SHA-256 ceremony_script.py → record in Ceremony Record (manual)
  SHA-256 trust_root.py      → record in Ceremony Record (manual)
  Format 4 USB drives        → manual

Ceremony day:
  Phase 1: Environment audit → manual (Procedure §Phase 1)
  Phase 2: --generate-root → automated
           --generate-issuing-keys → automated
  Phase 3: --generate-key-manifest → automated (signs + verifies in-memory)
           --generate-initial-brl → automated
  Phase 4: private key directory → workdir/private/ (automated)
           --create-record → paper_backup.txt (automated; print + sign: manual)
           GPG encryption → manual (passphrase custody)
           USB B clone → manual
  Phase 5: --export-public /media/pub-usb/publish/ → automated
  Phase 6: --verify-artifacts → automated (exit 0 = ALL PASS)
  Phase 7: Machine wipe, USB custody → manual

Post-ceremony:
  Step P.1: Re-sign BRL (6h expiry) → manual Python command
  Step P.2: Publish Key Manifest → manual upload
  Step P.3: Verify Key Manifest endpoint → manual curl
  Step P.4: Publish BRL → manual upload
  Step P.5: Verify BRL endpoint → manual curl
```
