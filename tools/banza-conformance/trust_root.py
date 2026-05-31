"""
BANZA Federation Test Trust Root — Slice 0

Provides test certificate generation for the conformance runner.
This slice uses placeholder cryptographic values (valid schema format, not real signatures).
Real ed25519 signing is added in WP-002 (FED-CERT-002 implementation).

No external dependencies. Python 3.8+ stdlib only.
"""

from datetime import datetime, timedelta, timezone

OPERATOR_A_ID = "operator-a-test"
OPERATOR_B_ID = "operator-b-test"
ISSUER_KEY_ID = "test-banza-key-2026-05"

# Placeholder ed25519 public key: prefix + 43 base64url chars (represents 32 bytes).
# Satisfies schema pattern ^ed25519:[A-Za-z0-9_-]{43}$
# NOT a real public key — FED-CERT-002 replaces this with generated keypair.
_PLACEHOLDER_PUBLIC_KEY = "ed25519:" + "A" * 43

# Placeholder signature: 86 base64url chars (represents 64 bytes).
# Satisfies schema pattern ^[A-Za-z0-9_-]{86}$
# NOT a real ed25519 signature — FED-CERT-002 replaces this with a real signature.
_PLACEHOLDER_SIGNATURE = "A" * 86


def generate_test_certificate(
    operator_id: str = OPERATOR_A_ID,
    certification_level: int = 3,
    lifetime_days: int = 89,
    issuer_key_id: str = ISSUER_KEY_ID,
) -> dict:
    """
    Generate a certificate dict that satisfies operator-certificate.json schema validation.

    Slice 0: the signature field is a placeholder. FED-CERT-001 only validates
    schema structure — signature verification is FED-CERT-002 (requires WP-002).

    Returns a dict suitable for serving at /.well-known/banza/certificate.json.
    """
    now = datetime.now(timezone.utc)
    issued_at = (now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    expires_at = (now + timedelta(days=lifetime_days)).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "schema_version": "1",
        "operator_id": operator_id,
        "certification_level": certification_level,
        "protocol_version": "1.0",
        "capabilities": ["cross_operator_routing", "cross_operator_settlement"],
        "public_key": _PLACEHOLDER_PUBLIC_KEY,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "issuer": "BANZA",
        "issuer_key_id": issuer_key_id,
        "signature": _PLACEHOLDER_SIGNATURE,
    }
