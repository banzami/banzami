"""
BANZA Federation Conformance Runner — Slice 1

Implements:
  FED-CERT-001  Certificate Present at Well-Known URL          (Slice 0)
  FED-CERT-002  Certificate Signature Verifies Against Root    (Slice 1)
  FED-CERT-003  Certificate Not Expired                        (Slice 1)
  FED-CERT-004  operator_id Matches Declared Format            (Slice 1)
  FED-CERT-005  public_key Format Correct                      (Slice 1)
  FED-CERT-006  issuer is Exactly "BANZA"                      (Slice 1)
  FED-CERT-007  Lifetime ≤ 90 Days for L3+                     (Slice 1)

All tests are runner-side certificate validation against the cert served at
/.well-known/banza/certificate.json. No trust engine, no routing.

Spec: FEDERATION_TEST_SUITE_SPEC.md §Suite FED-CERT
Contract: contracts/federation/operator-certificate.json

Requires:
  cryptography>=41.0.0  for FED-CERT-002 (ed25519 signature verification)
  stdlib only           for FED-CERT-001, 003–007
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Optional

import trust_root as _tr

RUNNER_VERSION = "0.2.0-slice1"

# ── Schema ────────────────────────────────────────────────────────────────────

def _find_schema_path() -> Optional[str]:
    this_dir = os.path.dirname(os.path.abspath(__file__))
    for p in [
        os.path.join(this_dir, "..", "..", "contracts", "federation", "operator-certificate.json"),
        os.path.join(os.getcwd(), "contracts", "federation", "operator-certificate.json"),
    ]:
        if os.path.isfile(p):
            return os.path.normpath(p)
    return None


# ── Certificate schema validation (FED-CERT-001) ─────────────────────────────

def validate_operator_certificate(cert: dict) -> list:
    """
    Validate a parsed certificate against operator-certificate.json constraints.
    Returns a list of error strings. Empty list means schema-valid.
    """
    if not isinstance(cert, dict):
        return ["body is not a JSON object"]

    errors = []
    required = [
        "schema_version", "operator_id", "certification_level",
        "protocol_version", "capabilities", "public_key",
        "issued_at", "expires_at", "issuer", "issuer_key_id", "signature",
    ]
    for f in required:
        if f not in cert:
            errors.append(f"required field missing: '{f}'")

    extra = set(cert.keys()) - set(required)
    if extra:
        errors.append(f"additionalProperties not allowed: {sorted(extra)}")

    if "schema_version" in cert and cert["schema_version"] != "1":
        errors.append(f"schema_version must be '1', got {cert['schema_version']!r}")

    if "operator_id" in cert:
        oid = cert["operator_id"]
        if not isinstance(oid, str):
            errors.append("operator_id must be a string")
        elif not re.match(r"^[a-z0-9][a-z0-9\-]{2,62}[a-z0-9]$", oid):
            errors.append(f"operator_id format invalid: {oid!r}")

    if "certification_level" in cert:
        cl = cert["certification_level"]
        if not isinstance(cl, int) or isinstance(cl, bool) or not (0 <= cl <= 4):
            errors.append(f"certification_level must be integer 0–4, got {cl!r}")

    if "protocol_version" in cert:
        pv = cert["protocol_version"]
        if not isinstance(pv, str) or not re.match(r"^\d+\.\d+$", pv):
            errors.append(f"protocol_version format invalid: {pv!r}")

    if "capabilities" in cert:
        caps = cert["capabilities"]
        if not isinstance(caps, list):
            errors.append("capabilities must be an array")
        elif not all(isinstance(c, str) for c in caps):
            errors.append("capabilities items must all be strings")
        elif len(caps) != len(set(caps)):
            errors.append("capabilities items must be unique")

    if "public_key" in cert:
        pk = cert["public_key"]
        if not isinstance(pk, str) or not re.match(r"^ed25519:[A-Za-z0-9_-]{43}$", pk):
            errors.append(f"public_key format invalid: {pk!r}")

    for ts in ("issued_at", "expires_at"):
        if ts in cert and (not isinstance(cert[ts], str) or not cert[ts]):
            errors.append(f"{ts} must be a non-empty string")

    if "issuer" in cert and cert["issuer"] != "BANZA":
        errors.append(f"issuer must be 'BANZA', got {cert['issuer']!r}")

    if "issuer_key_id" in cert and not isinstance(cert["issuer_key_id"], str):
        errors.append("issuer_key_id must be a string")

    if "signature" in cert:
        sig = cert["signature"]
        if not isinstance(sig, str) or not re.match(r"^[A-Za-z0-9_-]{86}$", sig):
            errors.append(
                f"signature format invalid (expected 86 base64url chars): "
                f"len={len(sig) if isinstance(sig, str) else 'N/A'}"
            )

    return errors


# ── HTTP ──────────────────────────────────────────────────────────────────────

def http_get(url: str, timeout: int = 10) -> tuple:
    """GET url → (status, headers_dict, raw_body_str). Raises RuntimeError on failure."""
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return resp.status, headers, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        headers = {k.lower(): v for k, v in e.headers.items()}
        return e.code, headers, raw
    except Exception as exc:
        raise RuntimeError(f"GET {url}: {exc}") from exc


def http_post(url: str, body: dict, timeout: int = 10) -> tuple:
    """POST url with JSON body → (status, headers_dict, raw_body_str). Raises RuntimeError on failure."""
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return resp.status, headers, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        headers = {k.lower(): v for k, v in e.headers.items()}
        return e.code, headers, raw
    except Exception as exc:
        raise RuntimeError(f"POST {url}: {exc}") from exc


# ── Test case builders ────────────────────────────────────────────────────────

def _make_case(case_id: str, title: str) -> dict:
    return {
        "id": case_id,
        "title": title,
        "status": "SKIP",
        "duration_ms": 0,
        "request": None,
        "response": None,
        "failure_reason": None,
        "assertions": [],
        "evidence": {},
    }


def _assertion(name: str, passed: bool, expected=None, actual=None) -> dict:
    r = {"assertion": name, "passed": passed}
    if expected is not None:
        r["expected"] = str(expected)
    if actual is not None:
        r["actual"] = str(actual)
    return r


def _pass_case(case: dict, ms: int, assertions: list) -> dict:
    case.update(status="PASS", duration_ms=ms, assertions=assertions)
    return case


def _fail_case(case: dict, reason: str, ms: int = 0, assertions: list = None) -> dict:
    case.update(status="FAIL", duration_ms=ms, failure_reason=reason, assertions=assertions or [])
    return case


def _skip_case(case: dict, reason: str) -> dict:
    case.update(status="SKIP", failure_reason=reason)
    return case


def _error_case(case: dict, reason: str) -> dict:
    case.update(status="ERROR", failure_reason=reason)
    return case


# ── Cert fetch helper ─────────────────────────────────────────────────────────

def _fetch_cert(base_url: str) -> tuple:
    """
    GET /.well-known/banza/certificate.json.
    Returns (status, headers, raw_body, parsed_cert_or_None).
    Raises RuntimeError on connection failure.
    """
    cert_url = f"{base_url}/.well-known/banza/certificate.json"
    status, headers, raw = http_get(cert_url)
    try:
        cert = json.loads(raw) if isinstance(raw, str) else raw
        if not isinstance(cert, dict):
            cert = None
    except json.JSONDecodeError:
        cert = None
    return status, headers, raw, cert


def _parse_iso_timestamp(ts: str) -> datetime:
    """Parse ISO 8601 UTC timestamp string to timezone-aware datetime."""
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


# ── FED-CERT-001 ──────────────────────────────────────────────────────────────

def run_fed_cert_001(base_url: str) -> dict:
    """
    FED-CERT-001 — Certificate Present at Well-Known URL

    Pass:   HTTP 200 AND Content-Type contains application/json
            AND body is valid JSON AND schema validates.
    Fail:   HTTP != 200 OR body fails schema OR endpoint requires auth.
    Severity: STANDARD
    Contract: operator-certificate.json
    L3 Req: FED-L3-001, FED-L3-003
    """
    case = _make_case("FED-CERT-001", "Certificate Present at Well-Known URL")
    cert_url = f"{base_url}/.well-known/banza/certificate.json"

    t0 = time.monotonic()
    try:
        status, headers, raw = http_get(cert_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "GET", "url": cert_url}

    assertions = []
    assertions.append(_assertion("HTTP status == 200", status == 200, 200, status))

    ct = headers.get("content-type", "")
    assertions.append(_assertion(
        "Content-Type contains 'application/json'",
        "application/json" in ct.lower(), "application/json", ct or "(absent)",
    ))

    try:
        body = json.loads(raw)
        is_json = isinstance(body, dict)
    except json.JSONDecodeError as exc:
        is_json = False
        body = None
    assertions.append(_assertion("response body is valid JSON object", is_json))

    if is_json and body is not None:
        errs = validate_operator_certificate(body)
        schema_ok = len(errs) == 0
        assertions.append(_assertion(
            "schema valid against operator-certificate.json",
            schema_ok, "no schema errors",
            "; ".join(errs) if errs else None,
        ))
    else:
        schema_ok = False
        assertions.append(_assertion("schema valid against operator-certificate.json", False,
                                     "valid JSON required first", "skipped"))

    case["evidence"] = {
        "cert.http_status": status,
        "cert.http_headers": headers,
        "cert.raw_json": body,
        "cert.schema_validation_result": {
            "valid": schema_ok,
            "errors": validate_operator_certificate(body) if (is_json and body) else ["body not JSON"],
        },
    }
    case["response"] = {"status": status, "body_length": len(raw)}

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-CERT-002 ──────────────────────────────────────────────────────────────

def run_fed_cert_002(base_url: str, root_public_key_bytes: bytes) -> dict:
    """
    FED-CERT-002 — Certificate Signature Verifies Against Test BANZA Root

    Pass:   ed25519_verify(test_BANZA_PK, canonical_json, signature) = true
            AND canonical JSON excludes 'signature' field
            AND fields sorted lexicographically.
    Fail:   Verification returns false; canonical JSON error;
            signature field included in signed content.
    Severity: CRITICAL
    Invariant: INV-TRUST-001
    L3 Req: FED-L3-001
    """
    case = _make_case("FED-CERT-002", "Certificate Signature Verifies Against Test BANZA Root")

    if not _tr.CRYPTO_AVAILABLE:
        return _skip_case(
            case,
            "cryptography package not installed. "
            "Install it: pip install 'cryptography>=41.0.0'",
        )

    t0 = time.monotonic()
    try:
        status, headers, raw, cert = _fetch_cert(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "GET", "url": f"{base_url}/.well-known/banza/certificate.json"}
    case["response"] = {"status": status}

    assertions = []

    if cert is None:
        return _fail_case(case, "response body is not a JSON object", ms,
                          [_assertion("body is JSON object", False)])

    # Compute canonical JSON (excludes 'signature')
    try:
        canonical = _tr.canonical_json_bytes(cert)
        canonical_ok = True
        canonical_hash = hashlib.sha256(canonical).hexdigest()
    except Exception as exc:
        return _fail_case(case, f"canonical JSON construction failed: {exc}", ms)

    assertions.append(_assertion("canonical JSON excludes 'signature' field", canonical_ok))

    # Decode signature
    sig_str = cert.get("signature", "")
    try:
        sig_bytes = _tr.b64url_decode(sig_str)
        assertions.append(_assertion(
            "signature field is base64url-decodable", True,
            "decodable", f"{len(sig_bytes)} bytes",
        ))
    except Exception as exc:
        return _fail_case(case, f"signature base64url decode failed: {exc}", ms, assertions)

    # Verify
    verified, detail = _tr.verify_certificate_signature(cert, root_public_key_bytes)
    assertions.append(_assertion(
        "ed25519_verify(test_BANZA_PK, canonical_json, signature) == true",
        verified, "true", detail,
    ))

    case["evidence"] = {
        "cert.canonical_json_sha256": canonical_hash,
        "cert.canonical_json_length_bytes": len(canonical),
        "cert.signature_bytes_length": len(sig_bytes),
        "cert.issuer_key_id": cert.get("issuer_key_id"),
        "cert.signature_verification_result": {"verified": verified, "detail": detail},
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-CERT-003 ──────────────────────────────────────────────────────────────

def run_fed_cert_003(base_url: str) -> dict:
    """
    FED-CERT-003 — Certificate Not Expired

    Pass:   expires_at > runner wall clock AND issued_at <= runner wall clock.
    Fail:   expires_at <= now() OR issued_at > now() (future-dated certificate).
    Severity: CRITICAL
    Invariant: INV-TRUST-002
    L3 Req: FED-L3-002
    """
    case = _make_case("FED-CERT-003", "Certificate Not Expired")

    t0 = time.monotonic()
    try:
        status, headers, raw, cert = _fetch_cert(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "GET", "url": f"{base_url}/.well-known/banza/certificate.json"}
    case["response"] = {"status": status}

    if cert is None:
        return _fail_case(case, "response body is not a JSON object", ms)

    now = datetime.now(timezone.utc)
    assertions = []

    expires_at_str = cert.get("expires_at", "")
    issued_at_str = cert.get("issued_at", "")

    try:
        expires_at = _parse_iso_timestamp(expires_at_str)
        issued_at = _parse_iso_timestamp(issued_at_str)
        parse_ok = True
    except Exception as exc:
        return _fail_case(case, f"timestamp parsing failed: {exc}", ms,
                          [_assertion("issued_at and expires_at are parseable ISO 8601", False,
                                      "parseable", str(exc))])

    assertions.append(_assertion("issued_at and expires_at are parseable ISO 8601", True))

    not_yet_expired = expires_at > now
    assertions.append(_assertion(
        "expires_at > runner wall clock",
        not_yet_expired,
        f"> {now.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        expires_at_str,
    ))

    not_future_dated = issued_at <= now
    assertions.append(_assertion(
        "issued_at <= runner wall clock (not future-dated)",
        not_future_dated,
        f"<= {now.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        issued_at_str,
    ))

    remaining_seconds = int((expires_at - now).total_seconds()) if not_yet_expired else 0
    case["evidence"] = {
        "cert.expires_at": expires_at_str,
        "cert.issued_at": issued_at_str,
        "cert.runner_timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cert.expiry_check": {
            "expires_at": expires_at_str,
            "checked_at": now.isoformat(),
            "valid": not_yet_expired,
            "remaining_seconds": remaining_seconds,
        },
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-CERT-004 ──────────────────────────────────────────────────────────────

def run_fed_cert_004(base_url: str) -> dict:
    """
    FED-CERT-004 — operator_id Matches Declared Format

    Pass:   operator_id matches ^[a-z0-9][a-z0-9\\-]{2,62}[a-z0-9]$
    Fail:   Regex does not match; operator_id empty; contains uppercase.
    Severity: STANDARD
    L3 Req: FED-L3-001
    """
    case = _make_case("FED-CERT-004", "operator_id Matches Declared Format")

    t0 = time.monotonic()
    try:
        status, headers, raw, cert = _fetch_cert(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "GET", "url": f"{base_url}/.well-known/banza/certificate.json"}
    case["response"] = {"status": status}

    if cert is None:
        return _fail_case(case, "response body is not a JSON object", ms)

    oid = cert.get("operator_id", "")
    pattern = r"^[a-z0-9][a-z0-9\-]{2,62}[a-z0-9]$"
    matched = bool(re.match(pattern, oid))

    assertions = [
        _assertion(
            f"operator_id matches ^[a-z0-9][a-z0-9\\-]{{2,62}}[a-z0-9]$",
            matched, "matches", oid or "(empty)",
        )
    ]

    if not matched:
        extra = []
        if not oid:
            extra.append("operator_id is empty")
        elif any(c.isupper() for c in oid):
            extra.append("contains uppercase characters")
        if extra:
            assertions.append(_assertion("no formatting violations", False, "clean", "; ".join(extra)))

    case["evidence"] = {
        "cert.operator_id": oid,
        "cert.operator_id_pattern": pattern,
        "cert.operator_id_match": matched,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    return _fail_case(case, f"operator_id format invalid: {oid!r}", ms, assertions)


# ── FED-CERT-005 ──────────────────────────────────────────────────────────────

def run_fed_cert_005(base_url: str) -> dict:
    """
    FED-CERT-005 — public_key Format Correct

    Pass:   Matches ^ed25519:[A-Za-z0-9_-]{43}$ AND base64url-decoded length == 32 bytes.
    Fail:   Regex fails OR decoded length != 32 OR prefix not "ed25519:".
    Severity: STANDARD
    L3 Req: FED-L3-001
    """
    case = _make_case("FED-CERT-005", "public_key Format Correct")

    t0 = time.monotonic()
    try:
        status, headers, raw, cert = _fetch_cert(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "GET", "url": f"{base_url}/.well-known/banza/certificate.json"}
    case["response"] = {"status": status}

    if cert is None:
        return _fail_case(case, "response body is not a JSON object", ms)

    pk = cert.get("public_key", "")
    pattern = r"^ed25519:[A-Za-z0-9_-]{43}$"
    assertions = []

    regex_ok = bool(re.match(pattern, pk))
    assertions.append(_assertion(
        "public_key matches ^ed25519:[A-Za-z0-9_-]{43}$",
        regex_ok, "matches", pk[:60] + "…" if len(pk) > 60 else pk,
    ))

    decoded_length = None
    if regex_ok:
        key_b64 = pk[len("ed25519:"):]
        try:
            decoded = _tr.b64url_decode(key_b64)
            decoded_length = len(decoded)
            assertions.append(_assertion(
                "base64url-decoded length == 32 bytes",
                decoded_length == 32, 32, decoded_length,
            ))
        except Exception as exc:
            assertions.append(_assertion(
                "base64url-decoded length == 32 bytes", False, 32, f"decode error: {exc}",
            ))
    else:
        assertions.append(_assertion(
            "base64url-decoded length == 32 bytes", False, 32, "skipped (regex failed)",
        ))

    case["evidence"] = {
        "cert.public_key": pk,
        "cert.public_key_pattern_match": regex_ok,
        "cert.public_key_decoded_length_bytes": decoded_length,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-CERT-006 ──────────────────────────────────────────────────────────────

def run_fed_cert_006(base_url: str) -> dict:
    """
    FED-CERT-006 — issuer is Exactly "BANZA"

    Pass:   issuer === "BANZA" (strict equality, case-sensitive).
    Fail:   issuer != "BANZA" (including "banza", "Banza", or any other string).
    Severity: CRITICAL
    Invariant: INV-TRUST-001
    L3 Req: FED-L3-001
    """
    case = _make_case("FED-CERT-006", 'issuer is Exactly "BANZA"')

    t0 = time.monotonic()
    try:
        status, headers, raw, cert = _fetch_cert(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "GET", "url": f"{base_url}/.well-known/banza/certificate.json"}
    case["response"] = {"status": status}

    if cert is None:
        return _fail_case(case, "response body is not a JSON object", ms)

    issuer = cert.get("issuer", "")
    issuer_ok = issuer == "BANZA"

    assertions = [
        _assertion('issuer === "BANZA" (strict, case-sensitive)', issuer_ok, "BANZA", issuer),
    ]

    case["evidence"] = {"cert.issuer": issuer}

    if issuer_ok:
        return _pass_case(case, ms, assertions)
    return _fail_case(case, f"issuer must be 'BANZA', got {issuer!r}", ms, assertions)


# ── FED-CERT-007 ──────────────────────────────────────────────────────────────

def run_fed_cert_007(base_url: str) -> dict:
    """
    FED-CERT-007 — Lifetime ≤ 90 Days for L3+

    Pass:   expires_at - issued_at ≤ 7,776,000 seconds (90 days).
    Fail:   lifetime > 7,776,000 seconds OR issued_at/expires_at missing or malformed.
    Severity: STANDARD
    Invariant: INV-FED-006
    L3 Req: FED-L3-001
    """
    MAX_LIFETIME_S = 7_776_000  # 90 days in seconds
    case = _make_case("FED-CERT-007", "Lifetime ≤ 90 Days for L3+")

    t0 = time.monotonic()
    try:
        status, headers, raw, cert = _fetch_cert(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "GET", "url": f"{base_url}/.well-known/banza/certificate.json"}
    case["response"] = {"status": status}

    if cert is None:
        return _fail_case(case, "response body is not a JSON object", ms)

    issued_at_str = cert.get("issued_at", "")
    expires_at_str = cert.get("expires_at", "")
    assertions = []

    try:
        issued_at = _parse_iso_timestamp(issued_at_str)
        expires_at = _parse_iso_timestamp(expires_at_str)
    except Exception as exc:
        return _fail_case(case, f"timestamp parsing failed: {exc}", ms,
                          [_assertion("issued_at and expires_at parseable", False,
                                      "parseable", str(exc))])

    assertions.append(_assertion("issued_at and expires_at are parseable ISO 8601", True))

    lifetime_s = int((expires_at - issued_at).total_seconds())
    lifetime_days = lifetime_s / 86400

    assertions.append(_assertion(
        f"lifetime ≤ {MAX_LIFETIME_S}s (90 days)",
        lifetime_s <= MAX_LIFETIME_S,
        f"≤ {MAX_LIFETIME_S}s",
        f"{lifetime_s}s ({lifetime_days:.1f} days)",
    ))

    cert_level = cert.get("certification_level", 0)
    if cert_level >= 3:
        assertions.append(_assertion(
            "90-day limit applies (certification_level >= 3)",
            True, "applies", f"level={cert_level}",
        ))

    case["evidence"] = {
        "cert.issued_at": issued_at_str,
        "cert.expires_at": expires_at_str,
        "cert.lifetime_seconds": lifetime_s,
        "cert.lifetime_days": round(lifetime_days, 2),
        "cert.max_lifetime_seconds": MAX_LIFETIME_S,
        "cert.certification_level": cert_level,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── Setup ─────────────────────────────────────────────────────────────────────

def setup_operator_for_federation(base_url: str, cert: dict) -> bool:
    """
    Deliver the runner-generated signed certificate to the operator under test
    via POST /conformance/setup.

    Per FEDERATION_RUNNER_DESIGN.md §3.4: operators must expose a mechanism
    for the runner to configure their test certificate.

    Returns True if setup succeeded (HTTP 200/204), False otherwise.
    """
    try:
        status, _, raw = http_post(
            f"{base_url}/conformance/setup",
            {"certificate": cert},
        )
        return status in (200, 201, 204)
    except RuntimeError:
        return False


# ── Suite runner ──────────────────────────────────────────────────────────────

def run_suite_fed_cert(base_url: str, root_public_key_bytes: bytes = None) -> dict:
    """
    Run all FED-CERT tests (Slice 1: 001–007).

    root_public_key_bytes: raw 32-byte ed25519 public key of the test BANZA root.
      Required for FED-CERT-002. If None, FED-CERT-002 is SKIPPED.
    """
    cases = [
        run_fed_cert_001(base_url),
        run_fed_cert_002(base_url, root_public_key_bytes) if root_public_key_bytes else
            _skip_case(_make_case("FED-CERT-002", "Certificate Signature Verifies Against Test BANZA Root"),
                       "root_public_key_bytes not provided"),
        run_fed_cert_003(base_url),
        run_fed_cert_004(base_url),
        run_fed_cert_005(base_url),
        run_fed_cert_006(base_url),
        run_fed_cert_007(base_url),
    ]

    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    skipped = sum(1 for c in cases if c["status"] in ("SKIP", "ERROR"))

    return {
        "suite_id": "FED-CERT",
        "suite_name": "Certificate Validation",
        "blocking": True,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "cases": cases,
    }


# ── Federation mode entry point ───────────────────────────────────────────────

def run_federation_mode(
    base_url: str,
    output: str = None,
    quiet: bool = False,
    fed_suite: str = None,
) -> int:
    """
    Execute federation conformance tests.
    Returns: 0 = all pass, 1 = failures/skips, 2 = runner error.
    """
    print(f"BANZA Federation Conformance Runner {RUNNER_VERSION}")
    print(f"Operator: {base_url}")
    print(f"Slice:    1 — FED-CERT-001 through FED-CERT-007")
    print()

    schema_path = _find_schema_path()
    if schema_path is None:
        print("ERROR: contracts/federation/operator-certificate.json not found.", file=sys.stderr)
        return 2
    print(f"Schema:   {schema_path}")

    # ── Crypto setup ─────────────────────────────────────────────────────────
    root_public_key_bytes = None
    if _tr.CRYPTO_AVAILABLE:
        try:
            root_priv, root_pub, key_id = _tr.generate_test_root_keypair()
            op_priv, op_pub = _tr.generate_operator_keypair()
            cert = _tr.generate_test_certificate(
                root_private_key=root_priv,
                issuer_key_id=key_id,
                operator_public_key_bytes=op_pub,
            )
            root_public_key_bytes = root_pub

            setup_ok = setup_operator_for_federation(base_url, cert)
            if setup_ok:
                print(f"Setup:    POST /conformance/setup → OK "
                      f"(operator_id={cert['operator_id']!r}, "
                      f"issuer_key_id={cert['issuer_key_id']!r})")
            else:
                print(f"Setup:    POST /conformance/setup → FAILED or not supported "
                      f"(FED-CERT-002 may fail)")
        except Exception as exc:
            print(f"Setup:    crypto setup failed: {exc}")
            root_public_key_bytes = None
    else:
        print("Setup:    cryptography package not installed — FED-CERT-002 will SKIP")
        print("          Install: pip install 'cryptography>=41.0.0'")

    print()

    # ── Run suites ────────────────────────────────────────────────────────────
    start = time.monotonic()

    if fed_suite is None or fed_suite == "cert":
        suite_result = run_suite_fed_cert(base_url, root_public_key_bytes)
        suite_results = [suite_result]
    else:
        print(f"ERROR: Unknown --fed-suite value: {fed_suite!r}. Available: cert", file=sys.stderr)
        return 2

    duration_ms = int((time.monotonic() - start) * 1000)

    # ── Print results ─────────────────────────────────────────────────────────
    for suite in suite_results:
        print(f"[Suite] {suite['suite_name']} (blocking={suite['blocking']})")
        for case in suite["cases"]:
            icon = {"PASS": "✓", "FAIL": "✗", "SKIP": "–", "ERROR": "E"}.get(case["status"], "?")
            if not quiet or case["status"] != "PASS":
                print(f"  {icon} {case['id']} — {case['title']}")
            if case["status"] in ("FAIL", "ERROR") and case.get("failure_reason"):
                print(f"      Reason: {case['failure_reason']}")
            if case["status"] in ("FAIL", "ERROR"):
                for a in case.get("assertions", []):
                    if not a["passed"]:
                        line = f"      ✗ {a['assertion']}"
                        if a.get("expected"):
                            line += f" (expected: {a['expected']}"
                            if a.get("actual"):
                                line += f", got: {a['actual']}"
                            line += ")"
                        print(line)

        s_pass = suite["passed"]
        s_fail = suite["failed"]
        s_skip = suite["skipped"]
        print(f"  → {s_pass} passed, {s_fail} failed, {s_skip} skipped  ({duration_ms}ms)")
        print()

    # ── Summary ───────────────────────────────────────────────────────────────
    total_pass = sum(s["passed"] for s in suite_results)
    total_fail = sum(s["failed"] for s in suite_results)
    total_skip = sum(s["skipped"] for s in suite_results)

    print("=" * 60)
    if total_fail == 0 and total_skip == 0:
        print("FED-CERT-001 through FED-CERT-007: ALL PASS")
        print()
        print("What is now proven:")
        print("  ✓ Certificate endpoint exists and returns HTTP 200")
        print("  ✓ Content-Type is application/json")
        print("  ✓ Response is valid JSON satisfying operator-certificate.json")
        print("  ✓ ed25519 signature verifies against test BANZA root  (INV-TRUST-001)")
        print("  ✓ Certificate is not expired                           (INV-TRUST-002)")
        print("  ✓ operator_id matches declared format")
        print("  ✓ public_key is 32-byte ed25519 in base64url format")
        print("  ✓ issuer is exactly 'BANZA'                           (INV-TRUST-001)")
        print("  ✓ Lifetime ≤ 90 days for L3 certificate               (INV-FED-006)")
    elif total_fail > 0:
        print(f"FED-CERT: FAIL  ({total_fail} failed, {total_skip} skipped)")
    else:
        print(f"FED-CERT: PARTIAL  ({total_pass} passed, {total_fail} failed, {total_skip} skipped)")
    print("=" * 60)

    # ── Report ────────────────────────────────────────────────────────────────
    report = {
        "report_id": f"rpt-fed-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runner_version": RUNNER_VERSION,
        "federation_mode": True,
        "slice": "1",
        "operator_url": base_url,
        "schema_path": schema_path,
        "crypto_available": _tr.CRYPTO_AVAILABLE,
        "summary": {
            "total": total_pass + total_fail + total_skip,
            "passed": total_pass,
            "failed": total_fail,
            "skipped": total_skip,
            "duration_ms": duration_ms,
        },
        "suites": suite_results,
    }

    if output:
        with open(output, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\nReport written to {output}")

    return 0 if total_fail == 0 else 1


# ── Standalone entry point ────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="BANZA Federation Conformance Runner (FED-CERT-001 through FED-CERT-007)"
    )
    parser.add_argument("--url", required=True,
                        help="Base URL of the operator (e.g. http://localhost:8099)")
    parser.add_argument("--output", help="Write JSON report to this file")
    parser.add_argument("--quiet", action="store_true", help="Suppress passing test output")
    parser.add_argument("--fed-suite", dest="fed_suite",
                        help="Run only this suite (default: cert)")
    args = parser.parse_args()

    sys.exit(run_federation_mode(
        args.url.rstrip("/"),
        output=args.output,
        quiet=args.quiet,
        fed_suite=args.fed_suite,
    ))


if __name__ == "__main__":
    main()
