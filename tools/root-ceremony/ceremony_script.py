#!/usr/bin/env python3
"""
BANZA Root Key Ceremony Script
ADR-029 — Production Root Architecture
Document: BANZA-ROOT-KEY-CEREMONY-PROCEDURE-001

Automates the deterministic cryptographic steps of the BANZA Root Key Ceremony.
ROOT_KEY_CEREMONY_PROCEDURE.md remains the authoritative procedure document.
This script does not replace human steps: identity verification, environment
audit, physical storage, and witness signatures are not automated.

This script MUST run on a machine with no network access.

Usage:
  python3 ceremony_script.py [--workdir DIR] [--dry-run] COMMAND

Commands:
  --generate-root          Phase 2.1-2.2: determine key IDs, generate root keypair
  --generate-issuing-keys  Phase 2.3-2.5: generate cert, brl, evidence keypairs
  --generate-key-manifest  Phase 3.1-3.2: construct and sign Key Manifest
  --generate-initial-brl   Phase 3.3: construct and sign initial BRL
  --verify-artifacts       Phase 6: full verification of all artifacts from disk
  --export-public DIR      Phase 5: export public artifacts to publication directory
  --create-record          Phase 5.2 + 4.5: ceremony record JSON + paper backup
  --print-state            Print current ceremony session state summary

Options:
  --workdir DIR            Ceremony work directory (default: ceremony-workdir-YYYYMMDD)
  --dry-run                Use test- key IDs (DRY RUN ONLY — never for production)

Exit codes:
  0 = success / all verifications pass
  1 = verification failure or operational error
  2 = prerequisite not met
"""

import argparse
import base64
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone, timedelta

# ── Dependency check ──────────────────────────────────────────────────────────

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey,
        Ed25519PublicKey,
    )
    from cryptography.hazmat.primitives.serialization import (
        Encoding, PrivateFormat, PublicFormat, NoEncryption,
    )
    from cryptography.exceptions import InvalidSignature
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


# ── Constants ──────────────────────────────────────��──────────────────────────

STATE_FILE = "ceremony_state.json"
PRIVATE_DIR = "private"
PUBLIC_DIR = "public"

SEPARATOR = "=" * 70
SECTION   = "-" * 70


# ── Helpers ───────────��───────────────────────────────────────────────────────

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(s: str) -> bytes:
    pad = (4 - len(s) % 4) % 4
    return base64.urlsafe_b64decode(s + "=" * pad)


def fingerprint(pub_bytes: bytes) -> str:
    """SHA-256 of raw public key bytes, first 16 hex characters."""
    return hashlib.sha256(pub_bytes).hexdigest()[:16]


def file_sha256(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def canonical_json(obj: dict, exclude: str = None) -> bytes:
    """Canonical JSON per ADR-026/ADR-029: sorted keys, no whitespace, UTF-8."""
    payload = {k: v for k, v in obj.items() if k != exclude} if exclude else obj
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def abort(msg: str, code: int = 1) -> None:
    print(f"\nABORT: {msg}", file=sys.stderr)
    sys.exit(code)


def step(label: str) -> None:
    print(f"\n{SECTION}")
    print(f"  {label}")
    print(SECTION)


def witness_prompt(instruction: str) -> None:
    print(f"\n  ► WITNESS: {instruction}")


def officer_prompt(instruction: str) -> None:
    print(f"\n  ► OFFICER: {instruction}")


# ── State management ────────���─────────────────────────────────────────────────

def load_state(workdir: str) -> dict:
    path = os.path.join(workdir, STATE_FILE)
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def save_state(workdir: str, state: dict) -> None:
    path = os.path.join(workdir, STATE_FILE)
    with open(path, "w") as f:
        json.dump(state, f, indent=2, sort_keys=True)


def require_state_keys(state: dict, *keys: str, phase: str) -> None:
    missing = [k for k in keys if k not in state]
    if missing:
        abort(
            f"Phase prerequisite not met for {phase}. "
            f"Missing state: {', '.join(missing)}. "
            f"Run preceding phases first.",
            code=2,
        )


def load_private_key(workdir: str, key_id: str) -> "Ed25519PrivateKey":
    path = os.path.join(workdir, PRIVATE_DIR, f"{key_id}.private")
    if not os.path.exists(path):
        abort(f"Private key file not found: {path}", code=2)
    with open(path) as f:
        raw_b64 = f.read().strip()
    raw_bytes = b64url_decode(raw_b64)
    return Ed25519PrivateKey.from_private_bytes(raw_bytes)


def save_private_key(workdir: str, key_id: str, priv: "Ed25519PrivateKey") -> None:
    private_dir = os.path.join(workdir, PRIVATE_DIR)
    os.makedirs(private_dir, mode=0o700, exist_ok=True)
    raw_bytes = priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    path = os.path.join(private_dir, f"{key_id}.private")
    with open(path, "w") as f:
        f.write(b64url_encode(raw_bytes) + "\n")
    os.chmod(path, 0o600)


def save_public_key(workdir: str, key_id: str, pub_encoded: str) -> None:
    public_dir = os.path.join(workdir, PUBLIC_DIR)
    os.makedirs(public_dir, exist_ok=True)
    path = os.path.join(public_dir, f"{key_id}.public")
    with open(path, "w") as f:
        f.write(pub_encoded + "\n")


# ── Phase helpers ────��──────────────────────────────��─────────────────────────

def determine_key_ids(dry_run: bool) -> dict:
    now = datetime.now(timezone.utc)
    if dry_run:
        root_key_id = f"test-banza-root-{now.year}"
        cert_key_id = f"test-banza-cert-{now.strftime('%Y%m')}"
        brl_key_id  = f"test-banza-brl-{now.strftime('%Y%m')}"
        evid_key_id = f"test-banza-evidence-{now.strftime('%Y%m')}"
    else:
        root_key_id = f"banza-root-{now.year}"
        cert_key_id = f"banza-cert-{now.strftime('%Y%m')}"
        brl_key_id  = f"banza-brl-{now.strftime('%Y%m')}"
        evid_key_id = f"banza-evidence-{now.strftime('%Y%m')}"
    return {
        "ceremony_date": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root_key_id": root_key_id,
        "cert_key_id": cert_key_id,
        "brl_key_id":  brl_key_id,
        "evid_key_id": evid_key_id,
    }


# ── Commands ────��──────────────────────���──────────────────────────────────────

def cmd_generate_root(workdir: str, dry_run: bool) -> int:
    """Phase 2.1-2.2: determine key IDs and generate root keypair."""
    if not CRYPTO_AVAILABLE:
        abort("cryptography package not installed. Run: pip install 'cryptography>=41.0.0'", code=2)

    state = load_state(workdir)
    if "root_public_key" in state:
        abort(
            "Root key already generated in this session. "
            "To regenerate, delete the ceremony workdir and start a new session.",
            code=1,
        )

    print(SEPARATOR)
    print("  BANZA ROOT KEY CEREMONY — Phase 2: Key Generation")
    if dry_run:
        print("  *** DRY RUN — test- key IDs — NOT FOR PRODUCTION ***")
    print(SEPARATOR)

    # Step 2.1 — Determine key IDs
    step("Step 2.1 — Determine Key IDs (Procedure §Phase 2, Step 2.1)")
    ids = determine_key_ids(dry_run)
    print()
    print(f"  CEREMONY_DATE : {ids['ceremony_date']}")
    print(f"  ROOT_KEY_ID   : {ids['root_key_id']}")
    print(f"  CERT_KEY_ID   : {ids['cert_key_id']}")
    print(f"  BRL_KEY_ID    : {ids['brl_key_id']}")
    print(f"  EVID_KEY_ID   : {ids['evid_key_id']}")
    officer_prompt("Read all five values aloud.")
    witness_prompt("Record all five values verbatim in the Ceremony Record Section 5.")

    # Step 2.2 — Generate root keypair
    step("Step 2.2 — Generate Root Keypair (Procedure §Phase 2, Step 2.2)")
    root_priv = Ed25519PrivateKey.generate()
    root_pub_bytes = root_priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    root_pub_encoded = f"ed25519:{b64url_encode(root_pub_bytes)}"
    root_fp = fingerprint(root_pub_bytes)

    print()
    print(f"  ROOT PUBLIC KEY  : {root_pub_encoded}")
    print(f"  ROOT FINGERPRINT : {root_fp}")
    print()
    print("  Root private key → saved to workdir/private/ (DO NOT EXPORT)")
    officer_prompt("Read ROOT FINGERPRINT aloud.")
    witness_prompt("Record ROOT FINGERPRINT in Ceremony Record Section 6.1.")

    # Persist
    save_private_key(workdir, ids["root_key_id"], root_priv)
    save_public_key(workdir, ids["root_key_id"], root_pub_encoded)

    state.update(ids)
    state["root_public_key"] = root_pub_encoded
    state["root_fingerprint"] = root_fp
    save_state(workdir, state)

    print()
    print("  ✓ Step 2.2 COMPLETE")
    print(f"  State saved to: {os.path.join(workdir, STATE_FILE)}")
    return 0


def cmd_generate_issuing_keys(workdir: str, dry_run: bool) -> int:
    """Phase 2.3-2.5: generate cert, brl, evidence issuing keypairs."""
    if not CRYPTO_AVAILABLE:
        abort("cryptography package not installed. Run: pip install 'cryptography>=41.0.0'", code=2)

    state = load_state(workdir)
    require_state_keys(state, "root_key_id", "cert_key_id", "brl_key_id", "evid_key_id",
                       phase="--generate-issuing-keys")

    if "cert_public_key" in state:
        abort(
            "Issuing keys already generated in this session. "
            "To regenerate, delete the ceremony workdir and start a new session.",
            code=1,
        )

    print(SEPARATOR)
    print("  BANZA ROOT KEY CEREMONY — Phase 2: Issuing Key Generation")
    if dry_run:
        print("  *** DRY RUN — test- key IDs — NOT FOR PRODUCTION ***")
    print(SEPARATOR)

    def _gen_issuing(key_id: str, label: str) -> tuple:
        step(f"{label} (Procedure §Phase 2)")
        priv = Ed25519PrivateKey.generate()
        pub_bytes = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        pub_encoded = f"ed25519:{b64url_encode(pub_bytes)}"
        fp = fingerprint(pub_bytes)
        print()
        print(f"  KEY ID       : {key_id}")
        print(f"  PUBLIC KEY   : {pub_encoded}")
        print(f"  FINGERPRINT  : {fp}")
        save_private_key(workdir, key_id, priv)
        save_public_key(workdir, key_id, pub_encoded)
        return pub_encoded, fp

    # Step 2.3 — Cert-issuing keypair
    cert_pub, cert_fp = _gen_issuing(state["cert_key_id"], "Step 2.3 — Generate Cert-Issuing Keypair")

    # Step 2.4 — BRL-issuing keypair
    brl_pub, brl_fp = _gen_issuing(state["brl_key_id"], "Step 2.4 �� Generate BRL-Issuing Keypair")

    # Step 2.5 — Evidence-issuing keypair
    evid_pub, evid_fp = _gen_issuing(state["evid_key_id"], "Step 2.5 — Generate Evidence-Issuing Keypair")

    print()
    print(SECTION)
    print("  ALL ISSUING FINGERPRINTS — Read aloud to Witness")
    print(SECTION)
    print(f"  ROOT      : {state['root_fingerprint']}")
    print(f"  CERT      : {cert_fp}")
    print(f"  BRL       : {brl_fp}")
    print(f"  EVIDENCE  : {evid_fp}")
    officer_prompt("Read all four fingerprints aloud.")
    witness_prompt("Record all four fingerprints in Ceremony Record Sections 6.1–6.4.")

    state.update({
        "cert_public_key": cert_pub,
        "cert_fingerprint": cert_fp,
        "brl_public_key": brl_pub,
        "brl_fingerprint": brl_fp,
        "evid_public_key": evid_pub,
        "evid_fingerprint": evid_fp,
    })
    save_state(workdir, state)

    print()
    print("  ✓ Steps 2.3–2.5 COMPLETE — 4 keypairs generated")
    return 0


def cmd_generate_key_manifest(workdir: str, dry_run: bool) -> int:
    """Phase 3.1-3.2: construct and sign Key Manifest, verify in-memory."""
    if not CRYPTO_AVAILABLE:
        abort("cryptography package not installed.", code=2)

    state = load_state(workdir)
    require_state_keys(
        state,
        "root_key_id", "cert_key_id", "brl_key_id", "evid_key_id",
        "root_public_key", "cert_public_key", "brl_public_key", "evid_public_key",
        phase="--generate-key-manifest",
    )

    print(SEPARATOR)
    print("  BANZA ROOT KEY CEREMONY — Phase 3.1: Key Manifest Construction")
    if dry_run:
        print("  *** DRY RUN ***")
    print(SEPARATOR)

    # Step 3.1 — Construct Key Manifest body
    step("Step 3.1 — Construct and Sign Key Manifest (Procedure §Phase 3, Step 3.1)")

    now = datetime.now(timezone.utc)
    published_at    = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    root_expires_at = (now + timedelta(days=730)).strftime("%Y-%m-%dT%H:%M:%SZ")
    issuing_expires = (now + timedelta(days=183)).strftime("%Y-%m-%dT%H:%M:%SZ")

    manifest_body = {
        "schema_version": "1",
        "published_at": published_at,
        "root_key_id": state["root_key_id"],
        "root_public_key": state["root_public_key"],
        "expires_at": root_expires_at,
        "keys": [
            {
                "key_id":      state["cert_key_id"],
                "public_key":  state["cert_public_key"],
                "domain":      "certification",
                "active_since": published_at,
                "expires_at":  issuing_expires,
                "status":      "active",
            },
            {
                "key_id":      state["brl_key_id"],
                "public_key":  state["brl_public_key"],
                "domain":      "revocation",
                "active_since": published_at,
                "expires_at":  issuing_expires,
                "status":      "active",
            },
            {
                "key_id":      state["evid_key_id"],
                "public_key":  state["evid_public_key"],
                "domain":      "conformance-evidence",
                "active_since": published_at,
                "expires_at":  issuing_expires,
                "status":      "active",
            },
        ],
    }

    # Sign with root key (ADR-029 §Phase 6 + ADR-026 canonical JSON rule)
    root_priv = load_private_key(workdir, state["root_key_id"])
    canonical_bytes = canonical_json(manifest_body)
    sig_bytes = root_priv.sign(canonical_bytes)
    manifest_signature = b64url_encode(sig_bytes)

    key_manifest = dict(manifest_body)
    key_manifest["manifest_signature"] = manifest_signature

    manifest_json = json.dumps(key_manifest, indent=2, sort_keys=True)
    manifest_hash = hashlib.sha256(manifest_json.encode("utf-8")).hexdigest()

    # Step 3.2 — Verify signature in-memory
    step("Step 3.2 — In-Memory Manifest Signature Verification (Procedure §Phase 3, Step 3.2)")

    root_pub_raw = b64url_decode(state["root_public_key"].split(":")[1])
    verify_result = _verify_manifest_sig(key_manifest, root_pub_raw)
    if not verify_result:
        abort("MANIFEST SIGNATURE VERIFICATION: FAIL — ceremony is invalid. Discard all key material.", code=1)

    print()
    print(f"  KEY MANIFEST SHA-256           : {manifest_hash}")
    print(f"  Manifest root_key_id           : {key_manifest['root_key_id']}")
    print(f"  Manifest expires_at            : {key_manifest['expires_at']}")
    print(f"  Issuing keys (3)               : {[k['key_id'] for k in key_manifest['keys']]}")
    print(f"  MANIFEST SIGNATURE VERIFICATION: PASS")
    officer_prompt("Read KEY MANIFEST SHA-256 aloud.")
    witness_prompt("Record KEY MANIFEST SHA-256 in Ceremony Record Section 7.")

    # Save to workdir/public/key-manifest.json
    public_dir = os.path.join(workdir, PUBLIC_DIR)
    os.makedirs(public_dir, exist_ok=True)
    manifest_path = os.path.join(public_dir, "key-manifest.json")
    with open(manifest_path, "w") as f:
        f.write(manifest_json)

    state["manifest_hash"] = manifest_hash
    state["manifest_published_at"] = published_at
    state["manifest_expires_at"] = root_expires_at
    state["issuing_expires_at"] = issuing_expires
    state["manifest_sig_verified_in_memory"] = True
    save_state(workdir, state)

    print()
    print(f"  ✓ Key Manifest written to: {manifest_path}")
    print("  ✓ Step 3.1–3.2 COMPLETE")
    return 0


def cmd_generate_initial_brl(workdir: str, dry_run: bool) -> int:
    """Phase 3.3: construct and sign initial BRL."""
    if not CRYPTO_AVAILABLE:
        abort("cryptography package not installed.", code=2)

    state = load_state(workdir)
    require_state_keys(
        state, "brl_key_id", "brl_public_key",
        phase="--generate-initial-brl",
    )

    print(SEPARATOR)
    print("  BANZA ROOT KEY CEREMONY — Phase 3.3: Initial BRL Construction")
    if dry_run:
        print("  *** DRY RUN ***")
    print(SEPARATOR)

    step("Step 3.3 �� Construct and Sign Initial BRL (Procedure §Phase 3, Step 3.3)")

    now = datetime.now(timezone.utc)
    brl_expires = (now + timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

    brl_body = {
        "schema_version": "1",
        "issuer": "BANZA",
        "issuer_key_id": state["brl_key_id"],
        "issued_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expires_at": brl_expires,
        "revoked": [],
    }

    # Sign with BRL-issuing key
    brl_priv = load_private_key(workdir, state["brl_key_id"])
    brl_canonical = canonical_json(brl_body)
    brl_sig_bytes = brl_priv.sign(brl_canonical)

    initial_brl = dict(brl_body)
    initial_brl["signature"] = b64url_encode(brl_sig_bytes)

    brl_json = json.dumps(initial_brl, indent=2, sort_keys=True)
    brl_hash = hashlib.sha256(brl_json.encode("utf-8")).hexdigest()

    print()
    print(f"  issuer_key_id  : {initial_brl['issuer_key_id']}")
    print(f"  issued_at      : {initial_brl['issued_at']}")
    print(f"  expires_at     : {initial_brl['expires_at']}")
    print(f"  revoked        : [] (zero operators)")
    print(f"  INITIAL BRL SHA-256 : {brl_hash}")
    print()
    print("  NOTE: This BRL expires in 7 hours. Re-sign with 6-hour expiry before")
    print("  publication (see ROOT_KEY_CEREMONY_PROCEDURE.md §Part VII, Step P.1).")
    officer_prompt("Read INITIAL BRL SHA-256 aloud.")
    witness_prompt("Record INITIAL BRL SHA-256 in Ceremony Record Section 7.")

    # Save to workdir/public/initial-brl.json
    public_dir = os.path.join(workdir, PUBLIC_DIR)
    os.makedirs(public_dir, exist_ok=True)
    brl_path = os.path.join(public_dir, "initial-brl.json")
    with open(brl_path, "w") as f:
        f.write(brl_json)

    state["brl_hash"] = brl_hash
    state["brl_issued_at"] = initial_brl["issued_at"]
    state["brl_expires_at"] = initial_brl["expires_at"]
    save_state(workdir, state)

    print()
    print(f"  ✓ Initial BRL written to: {brl_path}")
    print("  ✓ Step 3.3 COMPLETE")
    return 0


def cmd_verify_artifacts(workdir: str, dry_run: bool) -> int:
    """Phase 6: full verification of all artifacts from disk."""
    if not CRYPTO_AVAILABLE:
        abort("cryptography package not installed.", code=2)

    state = load_state(workdir)
    require_state_keys(
        state,
        "root_key_id", "cert_key_id", "brl_key_id", "evid_key_id",
        "root_public_key", "brl_public_key",
        "manifest_hash", "brl_hash",
        phase="--verify-artifacts",
    )

    print(SEPARATOR)
    print("  BANZA ROOT KEY CEREMONY — Phase 6: Final Verification")
    if dry_run:
        print("  *** DRY RUN ***")
    print(SEPARATOR)

    manifest_path = os.path.join(workdir, PUBLIC_DIR, "key-manifest.json")
    brl_path      = os.path.join(workdir, PUBLIC_DIR, "initial-brl.json")

    results = []

    def check(label: str, passed: bool, detail: str = "") -> None:
        status = "PASS" if passed else "FAIL"
        results.append((label, status, detail))
        icon = "✓" if passed else "✗"
        line = f"  {icon} {label}: {status}"
        if detail:
            line += f"  ({detail})"
        print(line)

    # 6.1 — Re-verify Key Manifest from disk
    step("Step 6.1 — Disk Key Manifest Signature Verification")
    if not os.path.exists(manifest_path):
        check("Key Manifest file exists", False, f"not found: {manifest_path}")
    else:
        with open(manifest_path) as f:
            manifest_disk = json.load(f)

        root_pub_raw = b64url_decode(state["root_public_key"].split(":")[1])
        sig_ok = _verify_manifest_sig(manifest_disk, root_pub_raw)
        check("Manifest signature (ed25519)", sig_ok)

        disk_hash = file_sha256(manifest_path)
        hash_ok = disk_hash == state["manifest_hash"]
        check(
            "Manifest SHA-256 matches state",
            hash_ok,
            f"disk={disk_hash[:16]}… state={state['manifest_hash'][:16]}…",
        )

    # 6.2 — Re-verify BRL from disk
    step("Step 6.2 — Disk BRL Signature Verification")
    if not os.path.exists(brl_path):
        check("Initial BRL file exists", False, f"not found: {brl_path}")
    else:
        with open(brl_path) as f:
            brl_disk = json.load(f)

        brl_pub_raw = b64url_decode(state["brl_public_key"].split(":")[1])
        brl_sig_ok = _verify_brl_sig(brl_disk, brl_pub_raw)
        check("BRL signature (ed25519)", brl_sig_ok)

        disk_brl_hash = file_sha256(brl_path)
        brl_hash_ok = disk_brl_hash == state["brl_hash"]
        check(
            "BRL SHA-256 matches state",
            brl_hash_ok,
            f"disk={disk_brl_hash[:16]}… state={state['brl_hash'][:16]}…",
        )

    # 6.3 — Key ID format check (no test- prefix in production)
    step("Step 6.3 — Key ID Format Check (INV-ROOT-001)")
    all_key_ids = [
        state["root_key_id"], state["cert_key_id"],
        state["brl_key_id"], state["evid_key_id"],
    ]
    for kid in all_key_ids:
        if dry_run:
            check(
                f"Key ID format [{kid}]",
                kid.startswith("test-"),
                "DRY RUN — test- prefix expected",
            )
        else:
            no_test_prefix = not kid.startswith("test-")
            check(f"Key ID format [{kid}]", no_test_prefix, "no test- prefix")

    # 6.4 — Issuing key validity ≤ 6 months (184 days)
    step("Step 6.4 — Issuing Key Validity Check (INV-ROOT-006)")
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            manifest_for_validity = json.load(f)
        for entry in manifest_for_validity.get("keys", []):
            expires = datetime.fromisoformat(entry["expires_at"].replace("Z", "+00:00"))
            active  = datetime.fromisoformat(entry["active_since"].replace("Z", "+00:00"))
            days = (expires - active).days
            ok = days <= 184
            check(f"Issuing key validity [{entry['key_id']}]", ok, f"{days} days ≤ 184")

    # 6.5 — Publication USB: no private files present
    step("Step 6.5 — Publication Directory Private Key Exclusion")
    pub_dir = os.path.join(workdir, PUBLIC_DIR)
    if os.path.exists(pub_dir):
        priv_files = []
        for fn in os.listdir(pub_dir):
            if ".private" in fn:
                priv_files.append(fn)
        check(
            "Publication directory has no .private files",
            len(priv_files) == 0,
            f"found: {priv_files}" if priv_files else "",
        )
    else:
        check("Publication directory exists", False, pub_dir)

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print(SEPARATOR)
    all_passed = all(r[1] == "PASS" for r in results)

    if all_passed:
        print("  ALL VERIFICATIONS PASS")
        officer_prompt("Read 'ALL VERIFICATIONS PASS' aloud.")
        witness_prompt("Initial the verification results in Ceremony Record Section 8.")
        state["all_verifications_passed"] = True
    else:
        failed_checks = [r[0] for r in results if r[1] != "PASS"]
        print(f"  VERIFICATION FAILED: {len(failed_checks)} check(s) failed")
        for f_check in failed_checks:
            print(f"  ✗ {f_check}")
        print()
        print("  Per Procedure §Part VI: STOP. Do not proceed to Phase 7.")
        print("  Record the failure in the Ceremony Record.")
        print("  Discard all generated key material.")
        print("  Schedule a new ceremony after root cause is resolved.")
        state["all_verifications_passed"] = False

    save_state(workdir, state)
    return 0 if all_passed else 1


def cmd_export_public(workdir: str, publication_dir: str, dry_run: bool) -> int:
    """Phase 5: export public artifacts to the Publication USB directory."""
    state = load_state(workdir)
    require_state_keys(
        state, "manifest_hash", "brl_hash",
        phase="--export-public",
    )

    if not state.get("all_verifications_passed"):
        abort(
            "Verification has not been completed or failed. "
            "Run --verify-artifacts before --export-public.",
            code=2,
        )

    print(SEPARATOR)
    print("  BANZA ROOT KEY CEREMONY — Phase 5: Public Artifact Export")
    if dry_run:
        print("  *** DRY RUN ***")
    print(SEPARATOR)

    step(f"Exporting to: {publication_dir}")

    os.makedirs(publication_dir, exist_ok=True)

    public_dir = os.path.join(workdir, PUBLIC_DIR)
    artifacts_to_export = ["key-manifest.json", "initial-brl.json"]
    exported = []

    for artifact in artifacts_to_export:
        src = os.path.join(public_dir, artifact)
        dst = os.path.join(publication_dir, artifact)
        if not os.path.exists(src):
            abort(f"Source artifact not found: {src}", code=2)
        shutil.copy2(src, dst)
        exported.append(artifact)
        print(f"  ✓ Copied: {artifact}")

    # Confirm no private files in publication directory
    priv_files = [fn for fn in os.listdir(publication_dir) if ".private" in fn]
    if priv_files:
        abort(
            f"SECURITY: Private key files found in publication directory: {priv_files}. "
            "Remove them immediately.",
            code=1,
        )

    print()
    print(f"  Publication directory contents:")
    for fn in sorted(os.listdir(publication_dir)):
        fpath = os.path.join(publication_dir, fn)
        fhash = file_sha256(fpath)
        print(f"    {fn}  {fhash[:16]}…")

    print()
    print("  ✓ PUBLICATION DIRECTORY VERIFIED: NO PRIVATE KEY FILES")
    officer_prompt("Physically inspect the Publication USB before sealing.")
    witness_prompt("Confirm contents match the list above. Initial Ceremony Record Section 9.")

    return 0


def cmd_create_record(workdir: str, dry_run: bool) -> int:
    """Phase 5.2 + 4.5: generate ceremony-record.json and paper backup text."""
    state = load_state(workdir)
    required = [
        "ceremony_date", "root_key_id", "root_key_id",
        "cert_key_id", "brl_key_id", "evid_key_id",
        "root_public_key", "root_fingerprint",
        "cert_public_key", "cert_fingerprint",
        "brl_public_key", "brl_fingerprint",
        "evid_public_key", "evid_fingerprint",
        "manifest_hash", "brl_hash",
    ]
    require_state_keys(state, *required, phase="--create-record")

    print(SEPARATOR)
    print("  BANZA ROOT KEY CEREMONY — Phase 5.2: Ceremony Record Generation")
    if dry_run:
        print("  *** DRY RUN ***")
    print(SEPARATOR)

    ceremony_date = state["ceremony_date"]
    date_short = ceremony_date[:10]

    # ceremony-record.json (public record)
    record = {
        "schema_version": "1",
        "ceremony_date": ceremony_date,
        "ceremony_id": f"BANZA-ROOT-CEREMONY-{date_short}",
        "root_key_id": state["root_key_id"],
        "root_key_fingerprint": state["root_fingerprint"],
        "root_public_key": state["root_public_key"],
        "issuing_keys": [
            {
                "key_id": state["cert_key_id"],
                "domain": "certification",
                "fingerprint": state["cert_fingerprint"],
            },
            {
                "key_id": state["brl_key_id"],
                "domain": "revocation",
                "fingerprint": state["brl_fingerprint"],
            },
            {
                "key_id": state["evid_key_id"],
                "domain": "conformance-evidence",
                "fingerprint": state["evid_fingerprint"],
            },
        ],
        "key_manifest_sha256": state["manifest_hash"],
        "initial_brl_sha256": state["brl_hash"],
        "officer": "[CEREMONY OFFICER NAME — fill in before signing]",
        "witness": "[CEREMONY WITNESS NAME — fill in before signing]",
    }
    record_json = json.dumps(record, indent=2, sort_keys=True)
    record_hash = hashlib.sha256(record_json.encode("utf-8")).hexdigest()

    # Save ceremony-record.json to public dir
    public_dir = os.path.join(workdir, PUBLIC_DIR)
    os.makedirs(public_dir, exist_ok=True)
    record_path = os.path.join(public_dir, "ceremony-record.json")
    with open(record_path, "w") as f:
        f.write(record_json)

    # Paper backup
    paper_backup = f"""
{"=" * 60}
BANZA ROOT KEY CEREMONY PAPER BACKUP
{"=" * 60}
Ceremony Date  : {ceremony_date}
Ceremony ID    : BANZA-ROOT-CEREMONY-{date_short}

Ceremony Officer : ___________________________________
Ceremony Witness : ___________________________________

{"=" * 60}
KEY IDENTIFIERS AND FINGERPRINTS
{"=" * 60}
ROOT KEY ID      : {state['root_key_id']}
ROOT FINGERPRINT : {state['root_fingerprint']}
ROOT PUBLIC KEY  : {state['root_public_key']}

CERT KEY ID      : {state['cert_key_id']}
CERT FINGERPRINT : {state['cert_fingerprint']}

BRL KEY ID       : {state['brl_key_id']}
BRL FINGERPRINT  : {state['brl_fingerprint']}

EVIDENCE KEY ID  : {state['evid_key_id']}
EVID FINGERPRINT : {state['evid_fingerprint']}

{"=" * 60}
ARTIFACT HASHES
{"=" * 60}
KEY MANIFEST SHA-256   : {state['manifest_hash']}
INITIAL BRL SHA-256    : {state['brl_hash']}
CEREMONY RECORD SHA-256: {record_hash}

{"=" * 60}
PRIVATE KEY STORAGE
{"=" * 60}
ENCRYPTION METHOD : GPG AES-256 symmetric
PRIVATE KEY ENCRYPTION PASSPHRASE: [STORED SEPARATELY — NOT ON THIS PAGE]
Output USB A custodian: ___________________________________
Output USB B custodian: ___________________________________

{"=" * 60}
SIGNATURES
{"=" * 60}
This page contains no private key material.
It is safe to store with the Ceremony Record.

Officer signature: ___________________ Date: ___________
Witness signature: ___________________ Date: ___________
{"=" * 60}
"""

    # Save paper backup text
    paper_path = os.path.join(workdir, "paper_backup.txt")
    with open(paper_path, "w") as f:
        f.write(paper_backup)

    print()
    print(f"  CEREMONY RECORD SHA-256 : {record_hash}")
    print()
    print(f"  ✓ ceremony-record.json written to: {record_path}")
    print(f"  ✓ paper_backup.txt written to: {paper_path}")
    print()
    print("  ─── PAPER BACKUP ─────────────────────────────────────────────────")
    print(paper_backup)
    print("  ─── END PAPER BACKUP ─────────────────────────────────────────────")
    officer_prompt("Print paper_backup.txt on the offline printer and sign it.")
    witness_prompt(
        "Sign the paper backup. Confirm all fingerprints and hashes are legible. "
        "Record CEREMONY RECORD SHA-256 in Ceremony Record Section 7."
    )

    state["record_hash"] = record_hash
    save_state(workdir, state)

    return 0


def cmd_print_state(workdir: str) -> int:
    """Print a summary of the current ceremony session state."""
    state = load_state(workdir)
    if not state:
        print(f"  No ceremony state found in: {workdir}")
        return 0

    print(SEPARATOR)
    print("  BANZA Root Key Ceremony — Session State")
    print(SEPARATOR)

    fields_ordered = [
        ("ceremony_date",    "Ceremony Date"),
        ("root_key_id",      "Root Key ID"),
        ("cert_key_id",      "Cert Key ID"),
        ("brl_key_id",       "BRL Key ID"),
        ("evid_key_id",      "Evidence Key ID"),
        ("root_fingerprint", "Root Fingerprint"),
        ("cert_fingerprint", "Cert Fingerprint"),
        ("brl_fingerprint",  "BRL Fingerprint"),
        ("evid_fingerprint", "Evid Fingerprint"),
        ("manifest_hash",    "Manifest SHA-256"),
        ("brl_hash",         "BRL SHA-256"),
        ("record_hash",      "Record SHA-256"),
        ("manifest_sig_verified_in_memory", "Manifest sig (in-memory)"),
        ("all_verifications_passed",        "All verifications"),
    ]

    for key, label in fields_ordered:
        val = state.get(key, "—")
        if isinstance(val, bool):
            val = "PASS" if val else "FAIL"
        print(f"  {label:<34}: {val}")

    private_dir = os.path.join(workdir, PRIVATE_DIR)
    if os.path.exists(private_dir):
        priv_files = sorted(os.listdir(private_dir))
        print(f"\n  Private keys in workdir/private/ ({len(priv_files)}):")
        for fn in priv_files:
            print(f"    {fn}")
    else:
        print("\n  Private key directory: not yet created")

    public_dir = os.path.join(workdir, PUBLIC_DIR)
    if os.path.exists(public_dir):
        pub_files = sorted(os.listdir(public_dir))
        print(f"\n  Public artifacts in workdir/public/ ({len(pub_files)}):")
        for fn in pub_files:
            print(f"    {fn}")

    return 0


# ── Internal verification helpers ───────────���─────────────────────────────────

def _verify_manifest_sig(manifest: dict, root_pub_raw: bytes) -> bool:
    try:
        payload = {k: v for k, v in manifest.items() if k != "manifest_signature"}
        verify_bytes = canonical_json(payload)
        sig_str = manifest.get("manifest_signature", "")
        if not sig_str:
            return False
        sig_bytes = b64url_decode(sig_str)
        pub_key = Ed25519PublicKey.from_public_bytes(root_pub_raw)
        pub_key.verify(sig_bytes, verify_bytes)
        return True
    except (InvalidSignature, Exception):
        return False


def _verify_brl_sig(brl: dict, brl_pub_raw: bytes) -> bool:
    try:
        payload = {k: v for k, v in brl.items() if k != "signature"}
        verify_bytes = canonical_json(payload)
        sig_str = brl.get("signature", "")
        if not sig_str:
            return False
        sig_bytes = b64url_decode(sig_str)
        pub_key = Ed25519PublicKey.from_public_bytes(brl_pub_raw)
        pub_key.verify(sig_bytes, verify_bytes)
        return True
    except (InvalidSignature, Exception):
        return False


# ── Entry point ────────────���──────────────────────────────────────────────────

def main() -> None:
    if not CRYPTO_AVAILABLE:
        print(
            "FATAL: The 'cryptography' package is not installed.\n"
            "Install it: pip install 'cryptography>=41.0.0'\n"
            "Or use the ceremony virtualenv: source /media/ceremony-usb/venv/bin/activate",
            file=sys.stderr,
        )
        sys.exit(2)

    parser = argparse.ArgumentParser(
        description="BANZA Root Key Ceremony Script (ADR-029)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Commands
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--generate-root",          action="store_true",
                       help="Phase 2.1-2.2: determine key IDs + generate root keypair")
    group.add_argument("--generate-issuing-keys",  action="store_true",
                       help="Phase 2.3-2.5: generate cert, brl, evidence keypairs")
    group.add_argument("--generate-key-manifest",  action="store_true",
                       help="Phase 3.1-3.2: construct and sign Key Manifest")
    group.add_argument("--generate-initial-brl",   action="store_true",
                       help="Phase 3.3: construct and sign initial BRL")
    group.add_argument("--verify-artifacts",       action="store_true",
                       help="Phase 6: full verification of all artifacts from disk")
    group.add_argument("--export-public",          metavar="DIR",
                       help="Phase 5: export public artifacts to publication directory")
    group.add_argument("--create-record",          action="store_true",
                       help="Phase 5.2+4.5: ceremony record JSON + paper backup")
    group.add_argument("--print-state",            action="store_true",
                       help="Print current ceremony session state")

    # Options
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    parser.add_argument("--workdir", default=f"ceremony-workdir-{today}",
                        help=f"Ceremony work directory (default: ceremony-workdir-{today})")
    parser.add_argument("--dry-run", action="store_true",
                        help="DRY RUN: use test- key IDs (never for production)")

    args = parser.parse_args()

    # Workdir setup
    workdir = os.path.abspath(args.workdir)
    os.makedirs(workdir, mode=0o700, exist_ok=True)

    if args.dry_run:
        print()
        print("╔" + "═" * 68 + "╗")
        print("║  *** DRY RUN MODE — NOT FOR PRODUCTION ***                      ║")
        print("║  Key IDs will use test- prefix. No production keys generated.   ║")
        print("╚" + "═" * 68 + "╝")
        print()

    # Dispatch
    if args.generate_root:
        sys.exit(cmd_generate_root(workdir, args.dry_run))
    elif args.generate_issuing_keys:
        sys.exit(cmd_generate_issuing_keys(workdir, args.dry_run))
    elif args.generate_key_manifest:
        sys.exit(cmd_generate_key_manifest(workdir, args.dry_run))
    elif args.generate_initial_brl:
        sys.exit(cmd_generate_initial_brl(workdir, args.dry_run))
    elif args.verify_artifacts:
        sys.exit(cmd_verify_artifacts(workdir, args.dry_run))
    elif args.export_public:
        sys.exit(cmd_export_public(workdir, os.path.abspath(args.export_public), args.dry_run))
    elif args.create_record:
        sys.exit(cmd_create_record(workdir, args.dry_run))
    elif args.print_state:
        sys.exit(cmd_print_state(workdir))


if __name__ == "__main__":
    main()
