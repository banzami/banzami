"""
Unit tests for L3 cryptographic integrity hardening.

Covers:
  - BRL ed25519 signing and verification (INV-TRUST-005)
  - Tampered BRL fails closed
  - Evidence package signing and verification
  - Tampered evidence fails verification

Run: python -m pytest tests/unit/test_crypto_integrity.py -v
"""

import importlib
import json
import sys
import os
import pytest

# Allow importing from tools/banza-conformance without installing
_CONFORMANCE_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "tools", "banza-conformance"
)
sys.path.insert(0, os.path.abspath(_CONFORMANCE_DIR))

try:
    import trust_root as _tr
    CRYPTO_AVAILABLE = _tr.CRYPTO_AVAILABLE
except ImportError:
    CRYPTO_AVAILABLE = False

requires_crypto = pytest.mark.skipif(
    not CRYPTO_AVAILABLE,
    reason="cryptography package not installed",
)


# ── BRL signature tests ───────────────────────────────────────────────────────

@requires_crypto
def test_sign_brl_produces_signature():
    """generate_signed_brl() must include a non-empty signature field."""
    priv, pub, kid = _tr.generate_test_root_keypair()
    brl = _tr.generate_signed_brl(priv, kid, revoked=[])
    assert "signature" in brl
    assert len(brl["signature"]) > 0
    assert brl["issuer_key_id"] == kid


@requires_crypto
def test_verify_brl_signature_passes_for_valid_brl():
    """A correctly signed BRL must verify successfully (INV-TRUST-005)."""
    priv, pub, kid = _tr.generate_test_root_keypair()
    brl = _tr.generate_signed_brl(priv, kid, revoked=[])
    ok, detail = _tr.verify_brl_signature(brl, pub)
    assert ok, f"expected BRL signature to verify but got: {detail}"
    assert "valid" in detail.lower()


@requires_crypto
def test_verify_brl_signature_fails_for_tampered_payload():
    """A BRL with a tampered field must fail closed (INV-TRUST-005)."""
    priv, pub, kid = _tr.generate_test_root_keypair()
    brl = _tr.generate_signed_brl(priv, kid, revoked=[])

    # Tamper: add a revocation entry without re-signing
    tampered = dict(brl)
    tampered["revoked"] = [{"operator_id": "injected-operator", "reason": "tampered"}]

    ok, detail = _tr.verify_brl_signature(tampered, pub)
    assert not ok, "tampered BRL must not verify (fail-closed per INV-TRUST-005)"


@requires_crypto
def test_verify_brl_signature_fails_for_wrong_key():
    """BRL signed with key A must not verify against key B."""
    priv_a, pub_a, kid = _tr.generate_test_root_keypair()
    priv_b, pub_b, _ = _tr.generate_test_root_keypair()
    brl = _tr.generate_signed_brl(priv_a, kid, revoked=[])

    ok, detail = _tr.verify_brl_signature(brl, pub_b)
    assert not ok, "BRL signed with key A must not verify against key B"


@requires_crypto
def test_verify_brl_signature_fails_for_placeholder_signature():
    """A BRL with the 'A'*86 placeholder signature must not verify."""
    priv, pub, kid = _tr.generate_test_root_keypair()
    brl = {
        "schema_version": "1",
        "issuer": "BANZA",
        "issuer_key_id": kid,
        "issued_at": "2026-01-01T00:00:00Z",
        "expires_at": "2026-01-01T07:00:00Z",
        "revoked": [],
        "signature": "A" * 86,
    }
    ok, detail = _tr.verify_brl_signature(brl, pub)
    assert not ok, "placeholder 'A'*86 signature must not verify"


@requires_crypto
def test_verify_brl_signature_fails_for_missing_signature():
    """A BRL with no signature field must not verify (unsigned BRL = absent BRL)."""
    priv, pub, kid = _tr.generate_test_root_keypair()
    brl = {
        "schema_version": "1",
        "issuer": "BANZA",
        "issuer_key_id": kid,
        "issued_at": "2026-01-01T00:00:00Z",
        "expires_at": "2026-01-01T07:00:00Z",
        "revoked": [],
    }
    ok, detail = _tr.verify_brl_signature(brl, pub)
    assert not ok, "BRL without signature field must not verify"


@requires_crypto
def test_brl_with_revoked_entries_signs_and_verifies():
    """BRL with revocation entries signs and verifies correctly."""
    priv, pub, kid = _tr.generate_test_root_keypair()
    revoked = [
        {"operator_id": "op-bad-001", "reason": "fraud", "permanent": True,
         "since": "2026-01-01T00:00:00Z"}
    ]
    brl = _tr.generate_signed_brl(priv, kid, revoked=revoked)
    ok, detail = _tr.verify_brl_signature(brl, pub)
    assert ok, f"BRL with revocations must verify: {detail}"
    assert brl["revoked"][0]["operator_id"] == "op-bad-001"


# ── Evidence package signature tests ─────────────────────────────────────────

@requires_crypto
def test_sign_evidence_package_adds_required_fields():
    """sign_evidence_package() must add package_signature and evidence_hash."""
    priv, pub, kid = _tr.generate_test_root_keypair()
    report = {"report_id": "rpt-test-001", "passed": 79, "failed": 0}
    signed = _tr.sign_evidence_package(report, priv, kid, pub)

    assert "evidence_hash" in signed
    assert "package_signature" in signed

    pkg = signed["package_signature"]
    assert pkg["algorithm"] == "ed25519"
    assert pkg["issuer"] == "BANZA_TEST_ROOT"
    assert pkg["issuer_key_id"] == kid
    assert "signature" in pkg
    assert "signed_at" in pkg


@requires_crypto
def test_verify_evidence_package_signature_passes_for_valid_report():
    """A freshly signed evidence package must verify successfully."""
    priv, pub, kid = _tr.generate_test_root_keypair()
    report = {"report_id": "rpt-test-002", "suite": "FED-CERT", "passed": 11}
    signed = _tr.sign_evidence_package(report, priv, kid, pub)

    ok, detail = _tr.verify_evidence_package_signature(signed, pub)
    assert ok, f"expected evidence signature to verify but got: {detail}"


@requires_crypto
def test_verify_evidence_package_fails_for_tampered_field():
    """Mutating any evidence field after signing must fail verification."""
    priv, pub, kid = _tr.generate_test_root_keypair()
    report = {"report_id": "rpt-test-003", "passed": 79, "failed": 0}
    signed = _tr.sign_evidence_package(report, priv, kid, pub)

    # Tamper: flip pass count
    tampered = dict(signed)
    tampered["passed"] = 999

    ok, detail = _tr.verify_evidence_package_signature(tampered, pub)
    assert not ok, "tampered evidence package must not verify"


@requires_crypto
def test_verify_evidence_package_fails_for_wrong_key():
    """Evidence signed with key A must not verify against key B."""
    priv_a, pub_a, kid = _tr.generate_test_root_keypair()
    priv_b, pub_b, _ = _tr.generate_test_root_keypair()
    report = {"report_id": "rpt-test-004", "data": "sensitive"}
    signed = _tr.sign_evidence_package(report, priv_a, kid, pub_a)

    ok, detail = _tr.verify_evidence_package_signature(signed, pub_b)
    assert not ok, "evidence signed with key A must not verify against key B"


@requires_crypto
def test_evidence_hash_matches_canonical_payload():
    """evidence_hash must be SHA-256 of the canonical JSON (excl. package_signature/evidence_hash)."""
    import hashlib
    priv, pub, kid = _tr.generate_test_root_keypair()
    report = {"report_id": "rpt-test-005", "suites": [{"suite_id": "FED-CERT", "passed": 11}]}
    signed = _tr.sign_evidence_package(report, priv, kid, pub)

    payload = {k: v for k, v in signed.items() if k not in ("package_signature", "evidence_hash")}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    expected_hash = hashlib.sha256(canonical).hexdigest()

    assert signed["evidence_hash"] == expected_hash


@requires_crypto
def test_verify_evidence_fails_when_package_signature_missing():
    """A report without package_signature must not verify."""
    _, pub, _ = _tr.generate_test_root_keypair()
    report = {"report_id": "rpt-test-006", "passed": 79}
    ok, detail = _tr.verify_evidence_package_signature(report, pub)
    assert not ok
    assert "package_signature" in detail.lower()


# ── RunnerInfra auto-signing tests ───────────────────────────────────────────

@requires_crypto
def test_runner_infra_auto_signs_brl_after_configure_signing_keys():
    """After configure_signing_keys(), all set_brl_* calls produce signed BRLs."""
    import json
    sys.path.insert(0, os.path.abspath(_CONFORMANCE_DIR))
    from runner_infra import RunnerInfra

    priv, pub, kid = _tr.generate_test_root_keypair()
    infra = RunnerInfra()
    infra.configure_signing_keys(priv, kid)
    infra.set_brl_empty()

    with infra._lock:
        brl = infra._trust_root_state["brl"]

    assert brl.get("issuer_key_id") == kid
    ok, detail = _tr.verify_brl_signature(brl, pub)
    assert ok, f"infra auto-signed BRL must verify: {detail}"


@requires_crypto
def test_runner_infra_bad_signature_brl_does_not_verify():
    """set_brl_bad_signature() must produce a BRL whose signature does NOT verify."""
    from runner_infra import RunnerInfra

    priv, pub, kid = _tr.generate_test_root_keypair()
    infra = RunnerInfra()
    infra.configure_signing_keys(priv, kid)
    infra.set_brl_bad_signature()  # uses stored key_id, but A*86 signature

    with infra._lock:
        brl = infra._trust_root_state["brl"]

    assert brl.get("issuer_key_id") == kid
    ok, detail = _tr.verify_brl_signature(brl, pub)
    assert not ok, "bad-signature BRL must not verify (fail-closed per INV-TRUST-005)"
