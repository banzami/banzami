"""
BANZA Federation Test Trust Root

Ephemeral ed25519 keypair generation and certificate signing for the
conformance runner. A fresh keypair is generated per runner invocation —
this keypair IS the "test BANZA root" for that run.

Requires: cryptography>=41.0.0 (pip install cryptography)
  Only FED-CERT-002 (signature verification) requires this package.
  FED-CERT-001, 003–007 work without it.

Per ADR-026 canonical signing rule (applies to certs, BRLs, and evidence):
  payload  = all fields EXCEPT "signature", sorted lexicographically
  bytes    = json.dumps(payload, sort_keys=True, separators=(',',':')).encode('utf-8')
  sig      = base64url_no_padding(ed25519_sign(root_private_key, bytes))

BRL structure (signed):
  {schema_version, issuer, issuer_key_id, issued_at, expires_at, revoked, signature}
  INV-TRUST-005: unsigned or unverifiable BRL = absent BRL (fail-closed)

Evidence package signing:
  report minus {package_signature, evidence_hash} → canonical JSON → ed25519 sign
  evidence_hash = sha256(canonical_bytes).hexdigest()
"""

import base64
import hashlib
import json
from datetime import datetime, date, timedelta, timezone

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey,
        Ed25519PublicKey,
    )
    from cryptography.exceptions import InvalidSignature
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

OPERATOR_A_ID = "operator-a-test"
OPERATOR_B_ID = "operator-b-test"


# ── Base64url helpers (stdlib only) ───────────────────────────────────────────

def b64url_encode(data: bytes) -> str:
    """Encode bytes to base64url without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(s: str) -> bytes:
    """Decode a base64url string (with or without padding) to bytes."""
    pad = (4 - len(s) % 4) % 4
    return base64.urlsafe_b64decode(s + "=" * pad)


# ── Canonical JSON (ADR-026 §Phase 4) ────────────────────────────────────────

def canonical_json_bytes(cert: dict) -> bytes:
    """
    Canonical JSON form for ed25519 signing.

    Rules (per ADR-026):
      - Include all fields EXCEPT 'signature'
      - Sort keys lexicographically
      - No whitespace (separators=(',', ':'))
      - UTF-8 encoded
    """
    payload = {k: v for k, v in cert.items() if k != "signature"}
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


# ── Keypair generation ────────────────────────────────────────────────────────

def generate_test_root_keypair() -> tuple:
    """
    Generate an ephemeral test BANZA root ed25519 keypair.

    Returns:
        (private_key, public_key_bytes: bytes, key_id: str)

    The private_key is an Ed25519PrivateKey object. The public_key_bytes are
    the raw 32-byte public key. The key_id is a stable string for this month.

    Raises ImportError if the 'cryptography' package is not installed.
    """
    if not CRYPTO_AVAILABLE:
        raise ImportError(
            "The 'cryptography' package is required for FED-CERT-002.\n"
            "Install it: pip install 'cryptography>=41.0.0'"
        )
    private_key = Ed25519PrivateKey.generate()
    public_key_bytes = private_key.public_key().public_bytes_raw()
    key_id = f"test-banza-key-{date.today().strftime('%Y-%m')}"
    return private_key, public_key_bytes, key_id


def generate_operator_keypair() -> tuple:
    """
    Generate an ephemeral operator ed25519 keypair.

    Returns:
        (private_key, public_key_bytes: bytes)
    """
    if not CRYPTO_AVAILABLE:
        raise ImportError("The 'cryptography' package is required.")
    private_key = Ed25519PrivateKey.generate()
    public_key_bytes = private_key.public_key().public_bytes_raw()
    return private_key, public_key_bytes


# ── Certificate signing ───────────────────────────────────────────────────────

def sign_certificate(cert_template: dict, root_private_key) -> dict:
    """
    Sign a certificate template with the test BANZA root private key.

    The 'signature' field is computed over canonical_json_bytes(cert_template)
    and replaces any existing 'signature' field in the returned dict.

    Returns a new dict (the template is not mutated).
    """
    cert = {k: v for k, v in cert_template.items() if k != "signature"}
    canonical = canonical_json_bytes(cert)
    sig_bytes = root_private_key.sign(canonical)
    cert["signature"] = b64url_encode(sig_bytes)
    return cert


def verify_certificate_signature(cert: dict, root_public_key_bytes: bytes) -> tuple:
    """
    Verify the certificate's ed25519 signature against the test BANZA root public key.

    Returns:
        (verified: bool, detail: str)

    The 'signature' field is decoded from base64url. The signed payload is
    canonical_json_bytes(cert) — i.e., all fields except 'signature'.
    """
    if not CRYPTO_AVAILABLE:
        return False, "cryptography package not installed"

    try:
        public_key = Ed25519PublicKey.from_public_bytes(root_public_key_bytes)
        sig_str = cert.get("signature", "")
        sig_bytes = b64url_decode(sig_str)
        canonical = canonical_json_bytes(cert)
        public_key.verify(sig_bytes, canonical)
        return True, "signature valid"
    except InvalidSignature:
        return False, "InvalidSignature: signature does not verify against test BANZA root"
    except Exception as exc:
        return False, f"verification error: {exc}"


# ── Certificate generation ────────────────────────────────────────────────────

def generate_brl(revoked: list = None) -> dict:
    """
    Generate an UNSIGNED BANZA Revocation List dict (placeholder signature).

    Used for backward-compatible initialization when no signing key is yet available.
    For signed BRLs (required when crypto is available), use generate_signed_brl().
    """
    now = datetime.now(timezone.utc)
    issued_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    expires_at = (now + timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "schema_version": "1",
        "issued_at": issued_at,
        "expires_at": expires_at,
        "revoked": revoked or [],
        "signature": "A" * 86,
    }


# ── BRL signing (INV-TRUST-005) ───────────────────────────────────────────────

def sign_brl(brl: dict, root_private_key) -> dict:
    """
    Sign a BRL dict with the test BANZA root key (INV-TRUST-005).

    Canonical form: all fields EXCEPT 'signature', sorted lexicographically.
    Returns a new dict with the 'signature' field set.
    """
    brl_copy = {k: v for k, v in brl.items() if k != "signature"}
    canonical = json.dumps(brl_copy, sort_keys=True, separators=(",", ":")).encode("utf-8")
    sig_bytes = root_private_key.sign(canonical)
    brl_copy["signature"] = b64url_encode(sig_bytes)
    return brl_copy


def verify_brl_signature(brl: dict, root_public_key_bytes: bytes) -> tuple:
    """
    Verify BRL ed25519 signature against the test BANZA root public key (INV-TRUST-005).

    Returns:
        (verified: bool, detail: str)

    The signed payload is all BRL fields EXCEPT 'signature', sorted lexicographically.
    Per INV-TRUST-005: an unverifiable BRL MUST be treated as absent (fail-closed).
    """
    if not CRYPTO_AVAILABLE:
        return False, "cryptography package not installed"
    try:
        public_key = Ed25519PublicKey.from_public_bytes(root_public_key_bytes)
        sig_str = brl.get("signature", "")
        if not sig_str:
            return False, "BRL has no signature field (unsigned BRL = absent BRL per INV-TRUST-005)"
        sig_bytes = b64url_decode(sig_str)
        brl_payload = {k: v for k, v in brl.items() if k != "signature"}
        canonical = json.dumps(brl_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        public_key.verify(sig_bytes, canonical)
        return True, "BRL signature valid"
    except InvalidSignature:
        return False, "InvalidSignature: BRL signature does not verify against test BANZA root"
    except Exception as exc:
        return False, f"BRL verification error: {exc}"


def generate_signed_brl(
    root_private_key,
    key_id: str,
    revoked: list = None,
    expires_hours: int = 7,
    issued_delta_hours: int = 0,
) -> dict:
    """
    Generate a cryptographically signed BANZA Revocation List.

    The BRL includes issuer_key_id so the verifier can select the correct
    public key for verification. Signature covers all fields except 'signature'.

    issued_delta_hours: offset from now for issued_at (negative = in the past).
    """
    now = datetime.now(timezone.utc)
    brl = {
        "schema_version": "1",
        "issuer": "BANZA",
        "issuer_key_id": key_id,
        "issued_at": (now + timedelta(hours=issued_delta_hours)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expires_at": (now + timedelta(hours=expires_hours)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "revoked": revoked or [],
    }
    return sign_brl(brl, root_private_key)


# ── Evidence package signing ──────────────────────────────────────────────────

def sign_evidence_package(
    report: dict,
    root_private_key,
    key_id: str,
    root_public_key_bytes: bytes,
) -> dict:
    """
    Sign the evidence report, adding package_signature and evidence_hash fields.

    Signed payload: canonical JSON of report minus {package_signature, evidence_hash}.
    evidence_hash:  SHA-256 hex digest of the canonical payload bytes.
    signature:      ed25519 signature of the canonical payload bytes.

    Returns a new dict (the input is not mutated).
    """
    report_to_sign = {
        k: v for k, v in report.items()
        if k not in ("package_signature", "evidence_hash")
    }
    canonical = json.dumps(
        report_to_sign, sort_keys=True, separators=(",", ":"), default=str
    ).encode("utf-8")
    evidence_hash = hashlib.sha256(canonical).hexdigest()
    sig_bytes = root_private_key.sign(canonical)

    signed = dict(report)
    signed["evidence_hash"] = evidence_hash
    signed["package_signature"] = {
        "algorithm": "ed25519",
        "issuer": "BANZA_TEST_ROOT",
        "issuer_key_id": key_id,
        "runner_public_key": f"ed25519:{b64url_encode(root_public_key_bytes)}",
        "signature": b64url_encode(sig_bytes),
        "signed_at": datetime.now(timezone.utc).isoformat(),
        "signed_payload": "canonical_json_sha256",
    }
    return signed


def verify_evidence_package_signature(report: dict, root_public_key_bytes: bytes) -> tuple:
    """
    Verify the package_signature in an evidence report.

    The verification recomputes the canonical JSON of the report (excluding
    package_signature and evidence_hash), verifies the ed25519 signature, and
    checks the evidence_hash matches the computed hash.

    Returns:
        (verified: bool, detail: str)
    """
    if not CRYPTO_AVAILABLE:
        return False, "cryptography package not installed"

    pkg_sig = report.get("package_signature")
    if not pkg_sig or not isinstance(pkg_sig, dict):
        return False, "no package_signature field in report"

    sig_str = pkg_sig.get("signature", "")
    if not sig_str:
        return False, "package_signature.signature is missing"

    report_to_verify = {
        k: v for k, v in report.items()
        if k not in ("package_signature", "evidence_hash")
    }
    canonical = json.dumps(
        report_to_verify, sort_keys=True, separators=(",", ":"), default=str
    ).encode("utf-8")

    try:
        public_key = Ed25519PublicKey.from_public_bytes(root_public_key_bytes)
        sig_bytes = b64url_decode(sig_str)
        public_key.verify(sig_bytes, canonical)
    except InvalidSignature:
        return False, "InvalidSignature: evidence package signature does not verify"
    except Exception as exc:
        return False, f"evidence verification error: {exc}"

    # Also verify evidence_hash matches
    computed_hash = hashlib.sha256(canonical).hexdigest()
    reported_hash = report.get("evidence_hash")
    if reported_hash and computed_hash != reported_hash:
        return False, (
            f"evidence_hash mismatch: "
            f"computed={computed_hash[:16]}… != reported={reported_hash[:16]}…"
        )

    return True, "evidence package signature valid"


def generate_key_manifest(
    keys: dict,
    root_key_id: str = None,
    root_expires_days: int = 730,
    issuing_expires_days: int = 180,
    key_domains: dict = None,
    root_private_key=None,
) -> dict:
    """
    Generate a BANZA Key Manifest dict (ADR-029 §Phase 6).

    keys: {key_id: public_key_bytes (bytes, 32)} — all issuing keys to include.
    root_key_id: ID of the root key that signs this manifest (e.g. "banza-root-2026").
    root_expires_days: validity of the root key in days (default 730 = 24 months).
    issuing_expires_days: validity of each issuing key in days (default 180 = 6 months).
    key_domains: {key_id: domain_string} — maps each key to its domain
                 ("cert", "brl", "evidence"). Inferred from key_id prefix if omitted.
    root_private_key: Ed25519PrivateKey — if provided, signs the manifest (production use).
                      If None, manifest_signature is set to "" (test/stub use).

    Returns the full manifest dict. If root_private_key is provided, manifest_signature
    is a real base64url ed25519 signature over canonical JSON (all fields except
    manifest_signature, sorted lexicographically, per ADR-029 signing rule).
    """
    now = datetime.now(timezone.utc)
    published_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    root_expires_at = (now + timedelta(days=root_expires_days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    issuing_expires_at = (now + timedelta(days=issuing_expires_days)).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _infer_domain(kid: str) -> str:
        if "cert" in kid:
            return "cert"
        if "brl" in kid:
            return "brl"
        if "evidence" in kid:
            return "evidence"
        return "cert"

    key_entries = []
    for kid, pub in keys.items():
        domain = (key_domains or {}).get(kid) or _infer_domain(kid)
        key_entries.append({
            "key_id": kid,
            "domain": domain,
            "public_key": f"ed25519:{b64url_encode(pub)}",
            "active_since": published_at,
            "expires_at": issuing_expires_at,
            "status": "active",
        })

    manifest = {
        "schema_version": "1",
        "published_at": published_at,
        "root_key_id": root_key_id or "banza-root-test",
        "expires_at": root_expires_at,
        "keys": key_entries,
    }

    if root_private_key is not None:
        canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
        sig_bytes = root_private_key.sign(canonical)
        manifest["manifest_signature"] = b64url_encode(sig_bytes)
    else:
        manifest["manifest_signature"] = ""

    return manifest


def verify_key_manifest_signature(manifest: dict, root_public_key_bytes: bytes) -> tuple:
    """
    Verify the manifest_signature field of a BANZA Key Manifest (INV-ROOT-002).

    Signed payload: all fields EXCEPT manifest_signature, sorted lexicographically.
    Returns (verified: bool, detail: str).
    Per INV-ROOT-002: unsigned or unverifiable manifest MUST be rejected.
    """
    if not CRYPTO_AVAILABLE:
        return False, "cryptography package not installed"

    sig_str = manifest.get("manifest_signature", "")
    if not sig_str:
        return False, "manifest_signature is absent or empty (INV-ROOT-002: unsigned manifest rejected)"

    payload = {k: v for k, v in manifest.items() if k != "manifest_signature"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

    try:
        public_key = Ed25519PublicKey.from_public_bytes(root_public_key_bytes)
        sig_bytes = b64url_decode(sig_str)
        public_key.verify(sig_bytes, canonical)
        return True, "manifest_signature valid"
    except InvalidSignature:
        return False, "InvalidSignature: manifest_signature does not verify against root key (INV-ROOT-002)"
    except Exception as exc:
        return False, f"manifest verification error: {exc}"


def generate_test_certificate(
    operator_id: str = OPERATOR_A_ID,
    certification_level: int = 3,
    lifetime_days: int = 89,
    issuer_key_id: str = None,
    root_private_key=None,
    operator_public_key_bytes: bytes = None,
    issued_at_override: "datetime | None" = None,
    expires_at_override: "datetime | None" = None,
    capabilities: list = None,
) -> dict:
    """
    Generate a test certificate dict.

    When root_private_key is provided:
        Certificate is signed with a real ed25519 signature (required for FED-CERT-002).

    When root_private_key is None (Slice 0 fallback):
        Certificate uses a placeholder signature ('A' * 86). Schema-valid but
        cryptographically meaningless. FED-CERT-002 will SKIP in this mode.

    When operator_public_key_bytes is provided:
        Uses the real 32-byte ed25519 public key.

    When operator_public_key_bytes is None:
        Uses a placeholder public key ('A' * 43 base64url). Still satisfies
        FED-CERT-005 schema pattern (but not real cryptographic identity).
    """
    now = datetime.now(timezone.utc)

    if issuer_key_id is None:
        issuer_key_id = f"test-banza-key-{date.today().strftime('%Y-%m')}"

    if operator_public_key_bytes is not None:
        public_key = f"ed25519:{b64url_encode(operator_public_key_bytes)}"
    else:
        public_key = "ed25519:" + "A" * 43

    if issued_at_override is not None:
        issued_at = issued_at_override.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        issued_at = (now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    if expires_at_override is not None:
        expires_at = expires_at_override.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        expires_at = (now + timedelta(days=lifetime_days)).strftime("%Y-%m-%dT%H:%M:%SZ")

    cert = {
        "schema_version": "1",
        "operator_id": operator_id,
        "certification_level": certification_level,
        "protocol_version": "1.0",
        "capabilities": capabilities if capabilities is not None else ["cross_operator_routing", "cross_operator_settlement"],
        "public_key": public_key,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "issuer": "BANZA",
        "issuer_key_id": issuer_key_id,
    }

    if root_private_key is not None:
        return sign_certificate(cert, root_private_key)

    cert["signature"] = "A" * 86
    return cert
