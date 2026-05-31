"""
BANZA Federation Test Trust Root

Ephemeral ed25519 keypair generation and certificate signing for the
conformance runner. A fresh keypair is generated per runner invocation —
this keypair IS the "test BANZA root" for that run.

Requires: cryptography>=41.0.0 (pip install cryptography)
  Only FED-CERT-002 (signature verification) requires this package.
  FED-CERT-001, 003–007 work without it.

Per ADR-026 canonical signing rule:
  payload  = all cert fields EXCEPT "signature", sorted lexicographically
  bytes    = json.dumps(payload, sort_keys=True, separators=(',',':')).encode('utf-8')
  sig      = base64url_no_padding(ed25519_sign(root_private_key, bytes))
"""

import base64
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
    Generate a BANZA Revocation List dict.

    revoked: list of dicts, each with {"operator_id": str, "reason": str,
             "permanent": bool, "since": str (ISO 8601)}.
    Omit or pass None for an empty (no-revocations) BRL.

    The signature field is a placeholder — BRL signature verification
    is tested in FED-TRUST-003, not FED-CERT-008 to 011.
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


def generate_key_manifest(keys: dict) -> dict:
    """
    Generate a BANZA-KEY-MANIFEST dict.

    keys: dict of {key_id: public_key_bytes (bytes, 32)}.
    Returns the manifest JSON structure from FEDERATION_FIXTURE_CATALOG.md.
    """
    now = datetime.now(timezone.utc)
    return {
        "schema_version": "1",
        "published_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "keys": [
            {
                "key_id": kid,
                "public_key": f"ed25519:{b64url_encode(pub)}",
                "active_since": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status": "active",
            }
            for kid, pub in keys.items()
        ],
    }


def generate_test_certificate(
    operator_id: str = OPERATOR_A_ID,
    certification_level: int = 3,
    lifetime_days: int = 89,
    issuer_key_id: str = None,
    root_private_key=None,
    operator_public_key_bytes: bytes = None,
    issued_at_override: "datetime | None" = None,
    expires_at_override: "datetime | None" = None,
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
        "capabilities": ["cross_operator_routing", "cross_operator_settlement"],
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
