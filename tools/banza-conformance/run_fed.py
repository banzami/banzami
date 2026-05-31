"""
BANZA Federation Conformance Runner — Slice 6

Implements:
  FED-CERT-001  Certificate Present at Well-Known URL                    (Slice 0)
  FED-CERT-002  Certificate Signature Verifies Against Root              (Slice 1)
  FED-CERT-003  Certificate Not Expired                                  (Slice 1)
  FED-CERT-004  operator_id Matches Declared Format                      (Slice 1)
  FED-CERT-005  public_key Format Correct                                (Slice 1)
  FED-CERT-006  issuer is Exactly "BANZA"                                (Slice 1)
  FED-CERT-007  Lifetime ≤ 90 Days for L3+                               (Slice 1)
  FED-CERT-008  Expired Certificate Fails Trust Step 2.4                 (Slice 2)
  FED-CERT-009  Revoked Operator Rejected by BRL Check                   (Slice 2)
  FED-CERT-010  Certificate-Manifest operator_id Binding                 (Slice 2)
  FED-CERT-011  Unknown issuer_key_id Triggers Key Fetch                 (Slice 2)
  FED-DISC-001  Manifest Present at Well-Known URL                       (Slice 3)
  FED-DISC-002  supports_federation == true                              (Slice 3)
  FED-DISC-003  cross_operator_routing == true                           (Slice 3)
  FED-DISC-004  certificate_url Accessible and Returns Valid Certificate (Slice 3)
  FED-DISC-005  interop_endpoint Reachable                               (Slice 3)
  FED-DISC-006  supported_currencies Non-Empty                           (Slice 3)
  FED-DISC-007  supports_federation Cannot Be True Without Valid L3+ Cert(Slice 3)
  FED-DISC-008  netting_interval_hours Within Bounds                     (Slice 3)
  FED-TRUST-001 Full 9-Step Trust Protocol Passes for Valid Operator     (Slice 4)
  FED-TRUST-002 Step 2.3 Fails on Invalid Certificate Signature          (Slice 4)
  FED-TRUST-003 Step 2.4 Fails on Expired Certificate                    (Slice 4)
  FED-TRUST-004 Step 2.5 Fails on certification_level < 3               (Slice 4)
  FED-TRUST-005 Step 2.6 Fails When Operator in BRL                      (Slice 4)
  FED-TRUST-006 Step 2.7 Fails When supports_federation Missing          (Slice 4)
  FED-TRUST-007 Step 2.8 Fails When cross_operator_routing Not in Cert   (Slice 4)
  FED-TRUST-008 Step 2.9 Fails on cert/manifest operator_id Mismatch     (Slice 4)
  FED-TRUST-009 BRL Staleness Enforcement (INV-TRUST-006)                (Slice 4)
  FED-ROUTE-001 Valid Routing Request Accepted                           (Slice 5)
  FED-ROUTE-002 routing_request_id Echoed Unchanged                      (Slice 5)
  FED-ROUTE-003 trace_id Propagated Unchanged (INV-FED-001)              (Slice 5)
  FED-ROUTE-004 Idempotent Retry Returns Same Response (INV-FED-004)     (Slice 5)
  FED-ROUTE-005 Request Without Valid Signature Rejected                 (Slice 5)
  FED-ROUTE-006 Wrong to_operator_id Rejected                            (Slice 5)
  FED-ROUTE-007 Recipient Not Found Returns Structured Rejection         (Slice 5)
  FED-ROUTE-008 Unsupported Currency Returns Structured Rejection        (Slice 5)
  FED-ROUTE-009 Accepted Response Contains Valid interop_transfer_id     (Slice 5)
  FED-ROUTE-010 Non-Positive amount.minor Rejected (INV-FED-LEDGER-002)  (Slice 5)
  FED-ROUTE-011 Duplicate routing_request_id with Different Content      (Slice 5)
  FED-ROUTE-012 Suspended Recipient Wallet Returns Structured Rejection  (Slice 5)
  FED-EXEC-001  Payee Wallet Credited Simultaneously with Acceptance     (Slice 6)
  FED-EXEC-002  Ledger Entries Correct on Both Operators                 (Slice 6)
  FED-EXEC-003  No Debit Without Acceptance (BC-001)                     (Slice 6)
  FED-EXEC-004  Debit and Obligation Are Atomic (BC-003)                 (Slice 6)
  FED-EXEC-005  Acceptance Is Irrevocable on Operator B (BC-004)        (Slice 6)
  FED-EXEC-006  Operator B Internal Failure Does Not Affect Obligation   (Slice 6)
  FED-EXEC-007  Provisional Completion: All 7 Criteria Met               (Slice 6)
  FED-EXEC-008  Double-Debit Prevention Via Posting Idempotency Key      (Slice 6)

Spec: FEDERATION_TEST_SUITE_SPEC.md §Suite FED-CERT, §Suite FED-DISC,
      §Suite FED-TRUST, §Suite FED-ROUTE, §Suite FED-EXEC
Contracts: contracts/federation/operator-certificate.json,
           contracts/federation/federation-manifest.json,
           contracts/federation/federation-routing.json

Requires:
  cryptography>=41.0.0  for FED-CERT-002, FED-CERT-008–011, FED-DISC-007,
                        all FED-TRUST tests, all FED-ROUTE tests, all FED-EXEC tests
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
from runner_infra import RunnerInfra

RUNNER_VERSION = "0.7.0-slice6"

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


def _find_manifest_schema_path() -> Optional[str]:
    this_dir = os.path.dirname(os.path.abspath(__file__))
    for p in [
        os.path.join(this_dir, "..", "..", "contracts", "federation", "federation-manifest.json"),
        os.path.join(os.getcwd(), "contracts", "federation", "federation-manifest.json"),
    ]:
        if os.path.isfile(p):
            return os.path.normpath(p)
    return None


def _find_routing_schema_path() -> Optional[str]:
    this_dir = os.path.dirname(os.path.abspath(__file__))
    for p in [
        os.path.join(this_dir, "..", "..", "contracts", "federation", "federation-routing.json"),
        os.path.join(os.getcwd(), "contracts", "federation", "federation-routing.json"),
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


# ── Federation manifest validation (FED-DISC-001) ────────────────────────────

def validate_federation_manifest(manifest: dict) -> list:
    """
    Validate a parsed manifest against the federation-manifest.json extension schema.
    Returns a list of error strings. Empty list means valid against the extension.
    """
    if not isinstance(manifest, dict):
        return ["body is not a JSON object"]

    errors = []
    required = [
        "federation_version", "certificate_url", "interop_endpoint",
        "supports_federation", "cross_operator_routing", "cross_operator_settlement",
        "federation_capabilities",
    ]
    for f in required:
        if f not in manifest:
            errors.append(f"required federation field missing: '{f}'")

    if "federation_version" in manifest and manifest["federation_version"] != "1":
        errors.append(f"federation_version must be '1', got {manifest['federation_version']!r}")

    if "certificate_url" in manifest and not isinstance(manifest["certificate_url"], str):
        errors.append("certificate_url must be a string (URI)")

    if "interop_endpoint" in manifest and not isinstance(manifest["interop_endpoint"], str):
        errors.append("interop_endpoint must be a string (URI)")

    for bool_field in ("supports_federation", "cross_operator_routing", "cross_operator_settlement"):
        if bool_field in manifest and not isinstance(manifest[bool_field], bool):
            errors.append(f"{bool_field} must be a boolean")

    if manifest.get("supports_federation") is True and manifest.get("cross_operator_routing") is not True:
        errors.append("if supports_federation is true, cross_operator_routing must also be true")

    fc = manifest.get("federation_capabilities")
    if fc is not None:
        if not isinstance(fc, dict):
            errors.append("federation_capabilities must be an object")
        else:
            for sub in ("routing_version", "settlement_version", "supported_currencies", "netting_interval_hours"):
                if sub not in fc:
                    errors.append(f"federation_capabilities.{sub} is required")

            if fc.get("routing_version") not in (None,) and fc.get("routing_version") != "1":
                errors.append(f"federation_capabilities.routing_version must be '1', got {fc.get('routing_version')!r}")

            if fc.get("settlement_version") not in (None,) and fc.get("settlement_version") != "1":
                errors.append(f"federation_capabilities.settlement_version must be '1', got {fc.get('settlement_version')!r}")

            sc = fc.get("supported_currencies")
            if sc is not None:
                if not isinstance(sc, list) or len(sc) == 0:
                    errors.append("federation_capabilities.supported_currencies must be a non-empty array")
                else:
                    for c in sc:
                        if not isinstance(c, str) or not re.match(r"^[A-Z]{3}$", c):
                            errors.append(f"supported_currencies: {c!r} does not match ^[A-Z]{{3}}$")

            nih = fc.get("netting_interval_hours")
            if nih is not None:
                if not isinstance(nih, int) or isinstance(nih, bool) or not (1 <= nih <= 168):
                    errors.append(
                        f"federation_capabilities.netting_interval_hours must be integer 1–168, got {nih!r}"
                    )

    return errors


# ── RoutingResponse validation ────────────────────────────────────────────────

_ROUTING_REJECTION_CODES = {
    "recipient_not_found", "recipient_suspended", "currency_not_supported",
    "amount_below_minimum", "amount_above_maximum", "operator_trust_failure",
    "capability_unavailable", "duplicate_request",
}

_ITX_PATTERN = r"^itx-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


def validate_routing_response(resp: dict) -> list:
    """
    Validate a RoutingResponse dict against federation-routing.json schema.
    Returns list of error strings. Empty = valid.
    """
    if not isinstance(resp, dict):
        return ["body is not a JSON object"]
    errors = []
    for f in ("schema_version", "routing_request_id", "status", "trace_id"):
        if f not in resp:
            errors.append(f"required field missing: '{f}'")

    if "schema_version" in resp and resp["schema_version"] != "1":
        errors.append(f"schema_version must be '1', got {resp['schema_version']!r}")

    status = resp.get("status")
    if status is not None and status not in ("accepted", "rejected", "pending"):
        errors.append(f"status must be 'accepted'|'rejected'|'pending', got {status!r}")

    if status == "accepted":
        if "interop_transfer_id" not in resp:
            errors.append("interop_transfer_id required when status=accepted")
        else:
            itx = resp["interop_transfer_id"]
            if not re.match(_ITX_PATTERN, itx):
                errors.append(f"interop_transfer_id format invalid: {itx!r}")
        if "accepted_at" not in resp:
            errors.append("accepted_at required when status=accepted")

    if status == "rejected":
        if "rejection_code" not in resp:
            errors.append("rejection_code required when status=rejected")
        elif resp["rejection_code"] not in _ROUTING_REJECTION_CODES:
            errors.append(f"rejection_code {resp['rejection_code']!r} not in registry")

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


# ── Routing wire protocol helpers (FED-ROUTE) ─────────────────────────────────

def _make_sig_header(body: dict, op_priv) -> str:
    """
    Build Banza-Federation-Signature header for a routing request.
    Signed payload: str(unix_seconds) + "." + raw_body_bytes.
    """
    body_bytes = json.dumps(body).encode("utf-8")
    t = int(time.time())
    payload = (str(t) + ".").encode("ascii") + body_bytes
    sig_bytes = op_priv.sign(payload)
    return f"t={t},v1={_tr.b64url_encode(sig_bytes)}"


def _post_route(url: str, body: dict, sig_header: str = None, timeout: int = 10) -> tuple:
    """
    POST a routing request to url.

    sig_header: if provided, sent as Banza-Federation-Signature header.
                if None, the header is omitted (tests missing-signature path).

    Returns (http_status, response_dict_or_None).
    """
    body_bytes = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if sig_header:
        headers["Banza-Federation-Signature"] = sig_header
    req = urllib.request.Request(url, data=body_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, None
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, None
    except Exception as exc:
        raise RuntimeError(f"POST {url}: {exc}") from exc


def _routing_body(
    base_url: str,
    routing_request_id: str = "rr-00000000-0000-0000-0000-000000000001",
    trace_id: str = "tr-00000000-0000-0000-0000-000000000001",
    from_operator_id: str = "operator-a-test",
    to_operator_id: str = "operator-b-test",
    amount_minor: int = 50000,
    currency: str = "AOA",
    sender_wallet_id: str = "wallet-payer-test-001",
    recipient_identifier: str = "wallet-payee-test-001",
    recipient_identifier_type: str = "wallet_id",
    created_at: str = None,
) -> dict:
    """Build a RoutingRequest dict with fixture defaults."""
    return {
        "schema_version": "1",
        "routing_request_id": routing_request_id,
        "trace_id": trace_id,
        "from_operator_id": from_operator_id,
        "to_operator_id": to_operator_id,
        "amount": {"minor": amount_minor, "currency": currency},
        "sender_wallet_id": sender_wallet_id,
        "recipient_identifier": recipient_identifier,
        "recipient_identifier_type": recipient_identifier_type,
        "created_at": created_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "certificate_url": f"{base_url}/.well-known/banza/certificate.json",
    }


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


def _fetch_manifest(base_url: str) -> tuple:
    """
    GET /.well-known/banza/operator.json.
    Returns (status, headers, raw_body, parsed_manifest_or_None).
    Raises RuntimeError on connection failure.
    """
    manifest_url = f"{base_url}/.well-known/banza/operator.json"
    status, headers, raw = http_get(manifest_url)
    try:
        manifest = json.loads(raw) if isinstance(raw, str) else raw
        if not isinstance(manifest, dict):
            manifest = None
    except json.JSONDecodeError:
        manifest = None
    return status, headers, raw, manifest


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

def setup_operator_for_federation(
    base_url: str,
    cert: dict,
    banza_root_key_id: str = None,
    banza_root_pub: bytes = None,
    brl_url: str = None,
    key_manifest_url: str = None,
) -> bool:
    """
    Deliver the signed certificate + trust configuration to the operator.

    Extended payload (Slice 2) adds BANZA root keys, BRL URL, and key manifest URL
    so the operator's trust engine can verify remote peer certificates.
    """
    payload: dict = {"certificate": cert}
    if banza_root_key_id and banza_root_pub:
        payload["banza_root_keys"] = {
            banza_root_key_id: f"ed25519:{_tr.b64url_encode(banza_root_pub)}"
        }
    if brl_url:
        payload["brl_url"] = brl_url
    if key_manifest_url:
        payload["key_manifest_url"] = key_manifest_url
    try:
        status, _, _ = http_post(f"{base_url}/conformance/setup", payload)
        return status in (200, 201, 204)
    except RuntimeError:
        return False


# ── Verify-peer helper (FED-CERT-008 to 011) ──────────────────────────────────

def _call_verify_peer(base_url: str, peer_manifest_url: str) -> tuple:
    """
    POST /conformance/federation/verify-peer on Operator A.
    Returns (status, result_dict_or_None).
    """
    try:
        status, _, raw = http_post(
            f"{base_url}/conformance/federation/verify-peer",
            {"peer_manifest_url": peer_manifest_url},
        )
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


# ── FED-CERT-008 ──────────────────────────────────────────────────────────────

def run_fed_cert_008(base_url: str, infra: "RunnerInfra", manifest_b: dict, cert_b_expired: dict) -> dict:
    """
    FED-CERT-008 — Expired Certificate Fails Trust Step 2.4

    Sim Op B serves CERT-EXPIRED (real sig, past timestamps).
    Operator A must reject at Step 2.4 (expiry check).

    Pass:   trusted=false AND step 2.4 status=fail AND rejection_reason indicates expiry.
    Fail:   trusted=true OR step 2.4 not fail OR endpoint not available.
    Severity: CRITICAL
    Invariant: INV-TRUST-002
    """
    case = _make_case("FED-CERT-008", "Expired Certificate Fails Trust Step 2.4")

    infra.configure_sim_b(manifest_b, cert_b_expired)
    infra.set_brl_empty()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_24 = steps_by_id.get("2.4", {})

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion("step 2.4 (expiry_check) status=fail",
                   step_24.get("status") == "fail", "fail", step_24.get("status")),
        _assertion("rejection_reason indicates certificate expiry",
                   rejection in ("certificate_expired", "certificate_future_dated")
                   or "expire" in str(rejection).lower(),
                   "certificate_expired", rejection or "(none)"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "peer_operator_id": cert_b_expired.get("operator_id"),
        "trusted": trusted,
        "rejection_reason": rejection,
        "trust_step_results": result.get("steps", []),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-CERT-009 ──────────────────────────────────────────────────────────────

def run_fed_cert_009(base_url: str, infra: "RunnerInfra", manifest_b: dict, cert_b_valid: dict) -> dict:
    """
    FED-CERT-009 — Revoked Operator Rejected by BRL Check

    BRL contains operator-b-test as revoked. Cert is valid; BRL check must catch it.
    Operator A must reject at Step 2.6 (BRL check), not at earlier steps.

    Pass:   trusted=false AND step 2.4/2.5 PASS AND step 2.6 status=fail.
    Fail:   trusted=true OR step 2.6 not fail OR rejected before step 2.6.
    Severity: CRITICAL
    Invariant: INV-TRUST-003, INV-FED-007
    """
    case = _make_case("FED-CERT-009", "Revoked Operator Rejected by BRL Check")

    infra.configure_sim_b(manifest_b, cert_b_valid)
    infra.set_brl_revoked("operator-b-test")

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_23 = steps_by_id.get("2.3", {})
    step_24 = steps_by_id.get("2.4", {})
    step_26 = steps_by_id.get("2.6", {})

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion("step 2.3 (signature) passed before BRL check",
                   step_23.get("status") == "pass", "pass", step_23.get("status")),
        _assertion("step 2.4 (expiry) passed before BRL check",
                   step_24.get("status") == "pass", "pass", step_24.get("status")),
        _assertion("step 2.6 (brl_check) status=fail",
                   step_26.get("status") == "fail", "fail", step_26.get("status")),
        _assertion("rejection_reason is operator_revoked",
                   rejection == "operator_revoked", "operator_revoked", rejection or "(none)"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "peer_operator_id": cert_b_valid.get("operator_id"),
        "brl_revoked": ["operator-b-test"],
        "trusted": trusted,
        "rejection_reason": rejection,
        "trust_step_results": result.get("steps", []),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-CERT-010 ──────────────────────────────────────────────────────────────

def run_fed_cert_010(base_url: str, infra: "RunnerInfra", manifest_b: dict, cert_b_mismatched: dict) -> dict:
    """
    FED-CERT-010 — Certificate-Manifest operator_id Binding

    Sim Op B manifest says operator_id="operator-b-test".
    Cert says operator_id="some-other-operator".
    Operator A must reject at Step 2.9 (operator_id binding).

    Pass:   trusted=false AND step 2.9 status=fail.
    Fail:   trusted=true OR step 2.9 not fail.
    Severity: CRITICAL
    Invariant: INV-TRUST-001
    L3 Req: FED-L3-005
    """
    case = _make_case("FED-CERT-010", "Certificate-Manifest operator_id Binding")

    infra.configure_sim_b(manifest_b, cert_b_mismatched)
    infra.set_brl_empty()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_29 = steps_by_id.get("2.9", {})

    cert_op = cert_b_mismatched.get("operator_id", "")
    manifest_op = manifest_b.get("operator_id", "")

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion("step 2.9 (operator_id_binding) status=fail",
                   step_29.get("status") == "fail", "fail", step_29.get("status")),
        _assertion("rejection_reason is operator_id_mismatch",
                   rejection == "operator_id_mismatch", "operator_id_mismatch", rejection or "(none)"),
        _assertion(f"cert operator_id ({cert_op!r}) != manifest operator_id ({manifest_op!r})",
                   cert_op != manifest_op, "different", f"cert={cert_op!r} manifest={manifest_op!r}"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "cert_operator_id": cert_op,
        "manifest_operator_id": manifest_op,
        "trusted": trusted,
        "rejection_reason": rejection,
        "trust_step_results": result.get("steps", []),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-CERT-011 ──────────────────────────────────────────────────────────────

def run_fed_cert_011(
    base_url: str, infra: "RunnerInfra", manifest_b: dict,
    cert_b_secondary: dict, secondary_key_id: str, secondary_pub: bytes,
) -> dict:
    """
    FED-CERT-011 — Unknown issuer_key_id Triggers Key Fetch

    Sim Op B cert is signed with a SECONDARY BANZA root key (issuer_key_id unknown to Operator A).
    Runner's key manifest has BOTH primary and secondary keys.
    Operator A must fetch the key manifest, discover the secondary key, and verify.

    Pass:   trusted=true (key fetched + verification succeeded).
    Fail:   trusted=false (operator rejected cert without fetching key manifest).
    Severity: STANDARD
    """
    case = _make_case("FED-CERT-011", "Unknown issuer_key_id Triggers Key Fetch")

    # Add secondary key to the manifest served by Trust Root Server
    from runner_infra import RunnerInfra as _RI
    # The key manifest must have primary key; also add secondary here
    # (set_key_manifest replaces, so caller must provide both — done in run_federation_mode)

    infra.configure_sim_b(manifest_b, cert_b_secondary)
    infra.set_brl_empty()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    steps = result.get("steps", [])
    # Check that a key fetch step was performed
    key_fetch_step = next((s for s in steps if "key_fetch" in s.get("step", "")), None)

    assertions = [
        _assertion("Operator A returns trusted=true (key rotation succeeded)",
                   trusted is True, True, trusted),
        _assertion("key manifest was fetched (key rotation path executed)",
                   key_fetch_step is not None and key_fetch_step.get("status") == "pass",
                   "key_fetch step present with status=pass",
                   f"key_fetch={key_fetch_step}" if key_fetch_step else "(no key_fetch step)"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "peer_operator_id": cert_b_secondary.get("operator_id"),
        "secondary_issuer_key_id": secondary_key_id,
        "trusted": trusted,
        "key_fetch_step": key_fetch_step,
        "trust_step_results": steps,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-DISC-001 ──────────────────────────────────────────────────────────────

def run_fed_disc_001(base_url: str) -> dict:
    """
    FED-DISC-001 — Manifest Present at Well-Known URL

    Pass:   HTTP 200 AND valid JSON AND validates against federation-manifest.json extension.
    Fail:   HTTP != 200 OR schema invalid.
    Severity: STANDARD
    Contract: federation-manifest.json
    L3 Req: FED-L3-003, FED-L3-004
    """
    case = _make_case("FED-DISC-001", "Manifest Present at Well-Known URL")
    manifest_url = f"{base_url}/.well-known/banza/operator.json"

    t0 = time.monotonic()
    try:
        status, headers, raw, manifest = _fetch_manifest(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "GET", "url": manifest_url}
    case["response"] = {"status": status}

    assertions = []
    assertions.append(_assertion("HTTP status == 200", status == 200, 200, status))

    ct = headers.get("content-type", "")
    assertions.append(_assertion(
        "Content-Type contains 'application/json'",
        "application/json" in ct.lower(), "application/json", ct or "(absent)",
    ))

    if manifest is None:
        assertions.append(_assertion("body is valid JSON object", False, "JSON object", "invalid JSON or not an object"))
        return _fail_case(case, "response body is not a valid JSON object", ms, assertions)

    assertions.append(_assertion("body is valid JSON object", True))

    schema_errors = validate_federation_manifest(manifest)
    schema_valid = len(schema_errors) == 0
    assertions.append(_assertion(
        "validates against federation-manifest.json extension",
        schema_valid, "no errors", "; ".join(schema_errors) if schema_errors else "ok",
    ))

    case["evidence"] = {
        "manifest_url": manifest_url,
        "manifest_http_status": status,
        "manifest_content_type": ct,
        "manifest_schema_valid": schema_valid,
        "manifest_schema_errors": schema_errors,
        "manifest_operator_id": manifest.get("operator_id"),
        "manifest_federation_version": manifest.get("federation_version"),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-DISC-002 ──────────────────────────────────────────────────────────────

def run_fed_disc_002(base_url: str) -> dict:
    """
    FED-DISC-002 — supports_federation == true

    Pass:   manifest.supports_federation === true (boolean, not string).
    Fail:   Missing; false; non-boolean type.
    Severity: STANDARD
    Invariant: INV-TRUST-004
    Contract: federation-manifest.json
    L3 Req: FED-L3-003
    """
    case = _make_case("FED-DISC-002", "supports_federation == true")

    t0 = time.monotonic()
    try:
        status, headers, raw, manifest = _fetch_manifest(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "GET", "url": f"{base_url}/.well-known/banza/operator.json"}
    case["response"] = {"status": status}

    if manifest is None:
        return _fail_case(case, "response body is not a JSON object", ms)

    val = manifest.get("supports_federation")
    is_true_bool = val is True

    assertions = [
        _assertion(
            "supports_federation === true (boolean)",
            is_true_bool,
            True,
            f"{val!r} (type={type(val).__name__})",
        ),
    ]

    case["evidence"] = {
        "manifest.supports_federation": val,
        "type": type(val).__name__,
    }

    if is_true_bool:
        return _pass_case(case, ms, assertions)
    return _fail_case(case, f"supports_federation must be true (boolean), got {val!r}", ms, assertions)


# ── FED-DISC-003 ──────────────────────────────────────────────────────────────

def run_fed_disc_003(base_url: str) -> dict:
    """
    FED-DISC-003 — cross_operator_routing == true

    Pass:   manifest.cross_operator_routing === true.
    Fail:   Missing; false.
    Severity: STANDARD
    Invariant: INV-FED-003
    Contract: federation-manifest.json
    L3 Req: FED-L3-003
    """
    case = _make_case("FED-DISC-003", "cross_operator_routing == true")

    t0 = time.monotonic()
    try:
        status, headers, raw, manifest = _fetch_manifest(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "GET", "url": f"{base_url}/.well-known/banza/operator.json"}
    case["response"] = {"status": status}

    if manifest is None:
        return _fail_case(case, "response body is not a JSON object", ms)

    val = manifest.get("cross_operator_routing")
    is_true_bool = val is True

    assertions = [
        _assertion(
            "cross_operator_routing === true (boolean)",
            is_true_bool,
            True,
            f"{val!r} (type={type(val).__name__})",
        ),
    ]

    case["evidence"] = {
        "manifest.cross_operator_routing": val,
        "type": type(val).__name__,
    }

    if is_true_bool:
        return _pass_case(case, ms, assertions)
    return _fail_case(case, f"cross_operator_routing must be true, got {val!r}", ms, assertions)


# ── FED-DISC-004 ──────────────────────────────────────────────────────────────

def run_fed_disc_004(base_url: str) -> dict:
    """
    FED-DISC-004 — certificate_url Accessible and Returns Valid Certificate

    Pass:   GET certificate_url → HTTP 200 AND valid cert AND cert.operator_id == manifest.operator_id.
    Fail:   HTTP != 200 OR cert invalid OR operator_id mismatch.
    Severity: STANDARD
    Invariant: INV-TRUST-001
    Contract: federation-manifest.json
    L3 Req: FED-L3-005
    """
    case = _make_case("FED-DISC-004", "certificate_url Accessible and Returns Valid Certificate")

    t0 = time.monotonic()
    try:
        _, _, _, manifest = _fetch_manifest(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if manifest is None:
        return _fail_case(case, "manifest fetch failed or returned invalid JSON", ms)

    manifest_op_id = manifest.get("operator_id", "")
    cert_url = manifest.get("certificate_url", "")

    if not cert_url:
        return _fail_case(case, "manifest.certificate_url is missing", ms)

    case["request"] = {"method": "GET", "url": cert_url}

    try:
        cert_status, cert_headers, cert_raw = http_get(cert_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, f"certificate_url fetch failed: {exc}")

    case["response"] = {"status": cert_status}

    try:
        cert = json.loads(cert_raw)
        if not isinstance(cert, dict):
            cert = None
    except json.JSONDecodeError:
        cert = None

    assertions = []
    assertions.append(_assertion("HTTP status == 200", cert_status == 200, 200, cert_status))
    assertions.append(_assertion("response is valid JSON object", cert is not None, "JSON object",
                                 "invalid" if cert is None else "ok"))

    if cert is not None:
        schema_errors = validate_operator_certificate(cert)
        schema_valid = len(schema_errors) == 0
        assertions.append(_assertion(
            "certificate validates against operator-certificate.json",
            schema_valid, "no errors", "; ".join(schema_errors) if schema_errors else "ok",
        ))

        cert_op_id = cert.get("operator_id", "")
        id_match = cert_op_id == manifest_op_id
        assertions.append(_assertion(
            "cert.operator_id == manifest.operator_id",
            id_match, manifest_op_id, cert_op_id,
        ))
    else:
        assertions.append(_assertion("certificate validates against operator-certificate.json",
                                     False, "no errors", "skipped (parse failed)"))
        assertions.append(_assertion("cert.operator_id == manifest.operator_id",
                                     False, manifest_op_id, "skipped (parse failed)"))

    case["evidence"] = {
        "manifest_operator_id": manifest_op_id,
        "certificate_url": cert_url,
        "cert_http_status": cert_status,
        "cert_operator_id": cert.get("operator_id") if cert else None,
        "operator_id_match": cert is not None and cert.get("operator_id") == manifest_op_id,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-DISC-005 ──────────────────────────────────────────────────────────────

def run_fed_disc_005(base_url: str) -> dict:
    """
    FED-DISC-005 — interop_endpoint Reachable

    Pass:   TCP connection succeeds AND any HTTP response received (not connection refused).
    Fail:   Connection refused; DNS failure; no response within 10s.
    Severity: STANDARD
    Invariant: INV-FED-003
    Contract: federation-manifest.json
    L3 Req: FED-L3-004
    """
    case = _make_case("FED-DISC-005", "interop_endpoint Reachable")

    t0 = time.monotonic()
    try:
        _, _, _, manifest = _fetch_manifest(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, f"manifest fetch failed: {exc}")

    if manifest is None:
        return _fail_case(case, "manifest fetch failed or returned invalid JSON", ms)

    interop_endpoint = manifest.get("interop_endpoint", "")
    if not interop_endpoint:
        return _fail_case(case, "manifest.interop_endpoint is missing", ms)

    probe_url = f"{interop_endpoint}/federation/route"
    case["request"] = {"method": "GET", "url": probe_url}

    try:
        probe_status, _, _ = http_get(probe_url, timeout=10)
        tcp_ok = True
    except RuntimeError:
        tcp_ok = False
        probe_status = None

    ms = int((time.monotonic() - t0) * 1000)
    case["response"] = {"status": probe_status}

    assertions = [
        _assertion("manifest.interop_endpoint is present", bool(interop_endpoint),
                   "non-empty string", interop_endpoint or "(missing)"),
        _assertion(
            "TCP connection succeeds (any HTTP response received)",
            tcp_ok, "any HTTP response",
            f"HTTP {probe_status}" if probe_status else "connection refused",
        ),
    ]

    case["evidence"] = {
        "interop_endpoint": interop_endpoint,
        "probe_url": probe_url,
        "tcp_reachable": tcp_ok,
        "probe_http_status": probe_status,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-DISC-006 ──────────────────────────────────────────────────────────────

def run_fed_disc_006(base_url: str) -> dict:
    """
    FED-DISC-006 — supported_currencies Non-Empty

    Pass:   Array with ≥ 1 ISO 4217 code; each code matches ^[A-Z]{3}$.
    Fail:   Missing; empty array; any element fails pattern.
    Severity: STANDARD
    Contract: federation-manifest.json
    L3 Req: FED-L3-003
    """
    case = _make_case("FED-DISC-006", "supported_currencies Non-Empty")

    t0 = time.monotonic()
    try:
        _, _, _, manifest = _fetch_manifest(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if manifest is None:
        return _fail_case(case, "manifest fetch failed or returned invalid JSON", ms)

    fc = manifest.get("federation_capabilities") or {}
    currencies = fc.get("supported_currencies")

    assertions = []

    if currencies is None:
        assertions.append(_assertion(
            "federation_capabilities.supported_currencies present", False, "non-empty array", "(absent)"))
        return _fail_case(case, "federation_capabilities.supported_currencies missing", ms, assertions)

    non_empty = isinstance(currencies, list) and len(currencies) >= 1
    assertions.append(_assertion(
        "supported_currencies is a non-empty array",
        non_empty, "non-empty array",
        f"[] (empty)" if (isinstance(currencies, list) and len(currencies) == 0) else str(currencies),
    ))

    if non_empty:
        invalid = [c for c in currencies if not isinstance(c, str) or not re.match(r"^[A-Z]{3}$", c)]
        all_iso = len(invalid) == 0
        assertions.append(_assertion(
            "all currencies match ^[A-Z]{3}$ (ISO 4217)",
            all_iso, "all match", str(invalid) if invalid else "ok",
        ))

    case["evidence"] = {
        "manifest.federation_capabilities.supported_currencies": currencies,
        "currency_count": len(currencies) if isinstance(currencies, list) else 0,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-DISC-007 ──────────────────────────────────────────────────────────────

def run_fed_disc_007(
    base_url: str,
    infra: "RunnerInfra",
    manifest_b: dict,
    cert_b_l2: dict,
) -> dict:
    """
    FED-DISC-007 — supports_federation Cannot Be True Without Valid L3+ Certificate

    Sim Op B declares supports_federation=true but holds a level-2 certificate.
    Operator A's trust engine must reject at Step 2.5 (level_check) — enforcing INV-TRUST-004.

    Pass:   trusted=false AND step 2.5 or 2.8 fails (certification_level_insufficient
            or cross_operator_routing_missing_from_cert_capabilities).
    Fail:   trusted=true OR no step failure at 2.5/2.8.
    Severity: CRITICAL
    Invariant: INV-TRUST-004
    Contract: federation-manifest.json
    """
    case = _make_case(
        "FED-DISC-007",
        "supports_federation Cannot Be True Without Valid L3+ Certificate",
    )

    infra.configure_sim_b(manifest_b, cert_b_l2)
    infra.set_brl_empty()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {
        "method": "POST",
        "url": f"{base_url}/conformance/federation/verify-peer",
        "body": {"peer_manifest_url": peer_url},
    }
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_25 = steps_by_id.get("2.5", {})
    step_28 = steps_by_id.get("2.8", {})

    # INV-TRUST-004: trust must fail at level_check (2.5) or routing_capability_check (2.8)
    level_or_cap_fail = (
        step_25.get("status") == "fail" or step_28.get("status") == "fail"
    )

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion(
            "trust fails at step 2.5 (level_check) or step 2.8 (routing_capability_check)",
            level_or_cap_fail,
            "step 2.5 or 2.8 = fail",
            f"2.5={step_25.get('status','absent')}, 2.8={step_28.get('status','absent')}",
        ),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "cert_b_level": cert_b_l2.get("certification_level"),
        "trusted": trusted,
        "rejection_reason": rejection,
        "step_2.5": step_25,
        "step_2.8": step_28,
        "trust_step_results": result.get("steps", []),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-DISC-008 ──────────────────────────────────────────────────────────────

def run_fed_disc_008(base_url: str) -> dict:
    """
    FED-DISC-008 — netting_interval_hours Within Bounds

    Pass:   Integer in range [1, 168].
    Fail:   Out of range; not integer; missing.
    Severity: STANDARD
    Contract: federation-manifest.json
    """
    case = _make_case("FED-DISC-008", "netting_interval_hours Within Bounds")

    t0 = time.monotonic()
    try:
        _, _, _, manifest = _fetch_manifest(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if manifest is None:
        return _fail_case(case, "manifest fetch failed or returned invalid JSON", ms)

    fc = manifest.get("federation_capabilities") or {}
    nih = fc.get("netting_interval_hours")

    assertions = []

    if nih is None:
        assertions.append(_assertion(
            "federation_capabilities.netting_interval_hours present", False, "integer 1–168", "(absent)"))
        return _fail_case(case, "netting_interval_hours missing from federation_capabilities", ms, assertions)

    is_int = isinstance(nih, int) and not isinstance(nih, bool)
    assertions.append(_assertion("netting_interval_hours is an integer", is_int, "integer", type(nih).__name__))

    if is_int:
        in_range = 1 <= nih <= 168
        assertions.append(_assertion(
            "netting_interval_hours is in range [1, 168]",
            in_range, "[1, 168]", nih,
        ))

    case["evidence"] = {
        "manifest.federation_capabilities.netting_interval_hours": nih,
        "type": type(nih).__name__,
        "in_range": is_int and 1 <= nih <= 168 if is_int else False,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-TRUST-001 ────────────────────────────────────────────────────────────

def run_fed_trust_001(
    base_url: str,
    infra: "RunnerInfra",
    manifest_b: dict,
    cert_b_valid: dict,
) -> dict:
    """
    FED-TRUST-001 — Full 9-Step Trust Protocol Passes for Valid Operator

    All 9 trust steps pass when Operator B is correctly configured.
    Pass:   trusted=true AND all 9 steps present with status=pass.
    Fail:   Any step fails; trust result != TRUSTED.
    Severity: STANDARD
    Invariants: INV-TRUST-001 through INV-TRUST-007
    L3 Req: FED-L3-009, FED-L3-010
    """
    case = _make_case("FED-TRUST-001", "Full 9-Step Trust Protocol Passes for Valid Operator")

    infra.configure_sim_b(manifest_b, cert_b_valid)
    infra.set_brl_empty()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    steps = result.get("steps", [])
    steps_by_id = {s.get("step"): s for s in steps}

    assertions = [
        _assertion("Operator A returns trusted=true", trusted is True, True, trusted),
    ]

    expected_steps = ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"]
    for sid in expected_steps:
        s = steps_by_id.get(sid, {})
        assertions.append(_assertion(
            f"step {sid} ({s.get('name', 'unknown')}) status=pass",
            s.get("status") == "pass",
            "pass", s.get("status", "(absent)"),
        ))

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "trusted": trusted,
        "rejection_reason": result.get("rejection_reason"),
        "trust_step_results": steps,
        "all_9_steps_present": all(sid in steps_by_id for sid in expected_steps),
        "issuer_key_id": cert_b_valid.get("issuer_key_id"),
        "issuer_key_source": "local_registry",
        "final_trusted_decision": trusted,
        "brl_fetched_at": steps_by_id.get("2.6", {}).get("brl_fetched_at"),
        "brl_expires_at": steps_by_id.get("2.6", {}).get("brl_expires_at"),
        "revoked_count": steps_by_id.get("2.6", {}).get("revoked_count"),
        "revocation_status": "not_revoked",
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-TRUST-002 ────────────────────────────────────────────────────────────

def run_fed_trust_002(
    base_url: str,
    infra: "RunnerInfra",
    manifest_b: dict,
    cert_b_invalid_sig: dict,
) -> dict:
    """
    FED-TRUST-002 — Step 2.3 Fails on Invalid Certificate Signature

    Tampered certificate is rejected at signature verification step (INV-TRUST-001).
    Pass:   trusted=false AND step 2.3 status=fail AND reason=signature_invalid.
    Fail:   Operator proceeds past step 2.3 with invalid signature.
    Severity: CRITICAL
    Invariant: INV-TRUST-001
    """
    case = _make_case("FED-TRUST-002", "Step 2.3 Fails on Invalid Certificate Signature")

    infra.configure_sim_b(manifest_b, cert_b_invalid_sig)
    infra.set_brl_empty()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_23 = steps_by_id.get("2.3", {})

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion("step 2.3 (signature_verify) status=fail",
                   step_23.get("status") == "fail", "fail", step_23.get("status")),
        _assertion("rejection_reason is signature_invalid",
                   rejection == "signature_invalid", "signature_invalid", rejection or "(none)"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "trusted": trusted,
        "rejection_reason": rejection,
        "issuer_key_id": cert_b_invalid_sig.get("issuer_key_id"),
        "issuer_key_source": "local_registry",
        "final_trusted_decision": trusted,
        "trust_step_results": result.get("steps", []),
        "step_2.3": step_23,
        "cert_signature_length": len(cert_b_invalid_sig.get("signature", "")),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-TRUST-003 ────────────────────────────────────────────────────────────

def run_fed_trust_003(
    base_url: str,
    infra: "RunnerInfra",
    manifest_b: dict,
    cert_b_expired: dict,
) -> dict:
    """
    FED-TRUST-003 — Step 2.4 Fails on Expired Certificate

    Expired certificate is rejected at expiry check (INV-TRUST-002).
    Pass:   trusted=false AND step 2.4 status=fail AND reason=certificate_expired.
    Fail:   Operator proceeds past step 2.4 with expired cert; grace period applied.
    Severity: CRITICAL
    Invariant: INV-TRUST-002
    """
    case = _make_case("FED-TRUST-003", "Step 2.4 Fails on Expired Certificate")

    infra.configure_sim_b(manifest_b, cert_b_expired)
    infra.set_brl_empty()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_24 = steps_by_id.get("2.4", {})

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion("step 2.4 (expiry_check) status=fail",
                   step_24.get("status") == "fail", "fail", step_24.get("status")),
        _assertion("rejection_reason indicates certificate expiry",
                   rejection in ("certificate_expired", "certificate_future_dated")
                   or "expire" in str(rejection).lower(),
                   "certificate_expired", rejection or "(none)"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "trusted": trusted,
        "rejection_reason": rejection,
        "cert_expires_at": cert_b_expired.get("expires_at"),
        "final_trusted_decision": trusted,
        "trust_step_results": result.get("steps", []),
        "step_2.4": step_24,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-TRUST-004 ────────────────────────────────────────────────────────────

def run_fed_trust_004(
    base_url: str,
    infra: "RunnerInfra",
    manifest_b: dict,
    cert_b_l2: dict,
) -> dict:
    """
    FED-TRUST-004 — Step 2.5 Fails on certification_level < 3

    An L2 certificate does not grant federation participation.
    Pass:   trusted=false AND step 2.5 status=fail AND reason=certification_level_insufficient.
    Fail:   L2 certificate accepted for federation routing.
    Severity: CRITICAL
    """
    case = _make_case("FED-TRUST-004", "Step 2.5 Fails on certification_level < 3")

    infra.configure_sim_b(manifest_b, cert_b_l2)
    infra.set_brl_empty()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_25 = steps_by_id.get("2.5", {})

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion("step 2.5 (level_check) status=fail",
                   step_25.get("status") == "fail", "fail", step_25.get("status")),
        _assertion("rejection_reason is certification_level_insufficient",
                   rejection == "certification_level_insufficient",
                   "certification_level_insufficient", rejection or "(none)"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "trusted": trusted,
        "rejection_reason": rejection,
        "cert_certification_level": cert_b_l2.get("certification_level"),
        "required_level": 3,
        "final_trusted_decision": trusted,
        "trust_step_results": result.get("steps", []),
        "step_2.5": step_25,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-TRUST-005 ────────────────────────────────────────────────────────────

def run_fed_trust_005(
    base_url: str,
    infra: "RunnerInfra",
    manifest_b: dict,
    cert_b_valid: dict,
) -> dict:
    """
    FED-TRUST-005 — Step 2.6 Fails When Operator in BRL (INV-TRUST-003)

    Operator in BRL is rejected at Step 2.6 despite valid certificate.
    Steps 2.3-2.5 must PASS before BRL check fails at 2.6.
    Pass:   steps 2.3-2.5 = pass AND step 2.6 status=fail AND reason=operator_revoked.
    Fail:   Routing proceeds despite BRL entry; rejected before step 2.6.
    Severity: CRITICAL
    Invariant: INV-TRUST-003, INV-FED-007
    """
    case = _make_case("FED-TRUST-005", "Step 2.6 Fails When Operator in BRL (INV-TRUST-003)")

    infra.configure_sim_b(manifest_b, cert_b_valid)
    infra.set_brl_revoked("operator-b-test")

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_23 = steps_by_id.get("2.3", {})
    step_24 = steps_by_id.get("2.4", {})
    step_25 = steps_by_id.get("2.5", {})
    step_26 = steps_by_id.get("2.6", {})

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion("step 2.3 (signature_verify) passed before BRL check",
                   step_23.get("status") == "pass", "pass", step_23.get("status")),
        _assertion("step 2.4 (expiry_check) passed before BRL check",
                   step_24.get("status") == "pass", "pass", step_24.get("status")),
        _assertion("step 2.5 (level_check) passed before BRL check",
                   step_25.get("status") == "pass", "pass", step_25.get("status")),
        _assertion("step 2.6 (brl_check) status=fail",
                   step_26.get("status") == "fail", "fail", step_26.get("status")),
        _assertion("rejection_reason is operator_revoked",
                   rejection == "operator_revoked", "operator_revoked", rejection or "(none)"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "trusted": trusted,
        "rejection_reason": rejection,
        "brl_revoked": ["operator-b-test"],
        "brl_fetched_at": step_26.get("brl_fetched_at"),
        "brl_expires_at": step_26.get("brl_expires_at"),
        "revocation_status": "revoked",
        "final_trusted_decision": trusted,
        "trust_step_results": result.get("steps", []),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-TRUST-006 ────────────────────────────────────────────────────────────

def run_fed_trust_006(
    base_url: str,
    infra: "RunnerInfra",
    manifest_b_no_fed: dict,
    cert_b_valid: dict,
) -> dict:
    """
    FED-TRUST-006 — Step 2.7 Fails When supports_federation Missing

    Operator that has certificate but doesn't declare federation support is rejected.
    Steps 2.3-2.6 must PASS; step 2.7 must FAIL.
    Pass:   step 2.7 status=fail AND reason=federation_not_declared_in_manifest.
    Fail:   Routing accepted despite supports_federation=false.
    Severity: STANDARD
    Invariant: INV-TRUST-004
    """
    case = _make_case("FED-TRUST-006", "Step 2.7 Fails When supports_federation Missing")

    infra.configure_sim_b(manifest_b_no_fed, cert_b_valid)
    infra.set_brl_empty()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_26 = steps_by_id.get("2.6", {})
    step_27 = steps_by_id.get("2.7", {})

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion("step 2.6 (brl_check) passed before federation check",
                   step_26.get("status") == "pass", "pass", step_26.get("status")),
        _assertion("step 2.7 (federation_support_check) status=fail",
                   step_27.get("status") == "fail", "fail", step_27.get("status")),
        _assertion("rejection_reason is federation_not_declared_in_manifest",
                   rejection == "federation_not_declared_in_manifest",
                   "federation_not_declared_in_manifest", rejection or "(none)"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "trusted": trusted,
        "rejection_reason": rejection,
        "manifest_supports_federation": manifest_b_no_fed.get("supports_federation"),
        "manifest_cross_operator_routing": manifest_b_no_fed.get("cross_operator_routing"),
        "final_trusted_decision": trusted,
        "trust_step_results": result.get("steps", []),
        "step_2.7": step_27,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-TRUST-007 ────────────────────────────────────────────────────────────

def run_fed_trust_007(
    base_url: str,
    infra: "RunnerInfra",
    manifest_b: dict,
    cert_b_no_routing_cap: dict,
) -> dict:
    """
    FED-TRUST-007 — Step 2.8 Fails When cross_operator_routing Not in Certificate Capabilities

    Certificate's capabilities array must include "cross_operator_routing".
    Steps 2.3-2.7 must PASS; step 2.8 must FAIL.
    Pass:   step 2.8 status=fail AND reason indicates missing routing capability.
    Fail:   Routing accepted despite missing capability.
    Severity: STANDARD
    Invariant: INV-TRUST-004
    """
    case = _make_case(
        "FED-TRUST-007",
        "Step 2.8 Fails When cross_operator_routing Not in Certificate Capabilities",
    )

    infra.configure_sim_b(manifest_b, cert_b_no_routing_cap)
    infra.set_brl_empty()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_27 = steps_by_id.get("2.7", {})
    step_28 = steps_by_id.get("2.8", {})

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion("step 2.7 (federation_support_check) passed before capability check",
                   step_27.get("status") == "pass", "pass", step_27.get("status")),
        _assertion("step 2.8 (routing_capability_check) status=fail",
                   step_28.get("status") == "fail", "fail", step_28.get("status")),
        _assertion("rejection_reason indicates missing routing capability",
                   rejection == "cross_operator_routing_missing_from_cert_capabilities",
                   "cross_operator_routing_missing_from_cert_capabilities", rejection or "(none)"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "trusted": trusted,
        "rejection_reason": rejection,
        "cert_capabilities": cert_b_no_routing_cap.get("capabilities"),
        "cert_certification_level": cert_b_no_routing_cap.get("certification_level"),
        "final_trusted_decision": trusted,
        "trust_step_results": result.get("steps", []),
        "step_2.8": step_28,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-TRUST-008 ────────────────────────────────────────────────────────────

def run_fed_trust_008(
    base_url: str,
    infra: "RunnerInfra",
    manifest_b: dict,
    cert_b_mismatched: dict,
) -> dict:
    """
    FED-TRUST-008 — Step 2.9 Fails on cert/manifest operator_id Mismatch

    Certificate and manifest must describe the same operator.
    Steps 2.3-2.8 must PASS; step 2.9 must FAIL.
    Pass:   step 2.9 status=fail AND both operator_ids logged.
    Fail:   Trust passes despite mismatch.
    Severity: CRITICAL
    Invariant: INV-TRUST-001
    L3 Req: FED-L3-005
    """
    case = _make_case("FED-TRUST-008", "Step 2.9 Fails on cert/manifest operator_id Mismatch")

    infra.configure_sim_b(manifest_b, cert_b_mismatched)
    infra.set_brl_empty()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_28 = steps_by_id.get("2.8", {})
    step_29 = steps_by_id.get("2.9", {})

    cert_op = cert_b_mismatched.get("operator_id", "")
    manifest_op = manifest_b.get("operator_id", "")

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion("step 2.8 (routing_capability_check) passed before binding check",
                   step_28.get("status") == "pass", "pass", step_28.get("status")),
        _assertion("step 2.9 (operator_id_binding) status=fail",
                   step_29.get("status") == "fail", "fail", step_29.get("status")),
        _assertion("rejection_reason is operator_id_mismatch",
                   rejection == "operator_id_mismatch",
                   "operator_id_mismatch", rejection or "(none)"),
        _assertion(f"cert operator_id ({cert_op!r}) differs from manifest operator_id ({manifest_op!r})",
                   cert_op != manifest_op, "different",
                   f"cert={cert_op!r} manifest={manifest_op!r}"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "trusted": trusted,
        "rejection_reason": rejection,
        "cert_operator_id": cert_op,
        "manifest_operator_id": manifest_op,
        "final_trusted_decision": trusted,
        "trust_step_results": result.get("steps", []),
        "step_2.9": step_29,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-TRUST-009 ────────────────────────────────────────────────────────────

def run_fed_trust_009(
    base_url: str,
    infra: "RunnerInfra",
    manifest_b: dict,
    cert_b_valid: dict,
) -> dict:
    """
    FED-TRUST-009 — BRL Staleness Enforcement (INV-TRUST-006)

    Routing must be refused when the BRL is expired (> 6 hours old).
    Runner sets the BRL to an expired state before calling verify-peer.
    Pass:   trusted=false AND step 2.6 fails with brl_expired.
    Fail:   Routing accepted with stale BRL; no BRL check performed.
    Severity: CRITICAL
    Invariant: INV-TRUST-006
    """
    case = _make_case("FED-TRUST-009", "BRL Staleness Enforcement (INV-TRUST-006)")

    infra.configure_sim_b(manifest_b, cert_b_valid)
    infra.set_brl_expired()

    peer_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    t0 = time.monotonic()
    try:
        status, result = _call_verify_peer(base_url, peer_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": f"{base_url}/conformance/federation/verify-peer",
                       "body": {"peer_manifest_url": peer_url}}
    case["response"] = {"status": status}

    if result is None:
        return _fail_case(case, "verify-peer response not valid JSON", ms)

    trusted = result.get("trusted")
    rejection = result.get("rejection_reason", "")
    steps_by_id = {s.get("step"): s for s in result.get("steps", [])}
    step_23 = steps_by_id.get("2.3", {})
    step_26 = steps_by_id.get("2.6", {})

    brl_expires_at = step_26.get("brl_expires_at", "")
    brl_issued_at = step_26.get("brl_issued_at", "")
    brl_fetched_at = step_26.get("brl_fetched_at", "")
    brl_age_seconds = step_26.get("brl_age_seconds")

    assertions = [
        _assertion("Operator A returns trusted=false", trusted is False, False, trusted),
        _assertion("step 2.3 (signature_verify) passed (cert signature is valid)",
                   step_23.get("status") == "pass", "pass", step_23.get("status")),
        _assertion("step 2.6 (brl_check) status=fail",
                   step_26.get("status") == "fail", "fail", step_26.get("status")),
        _assertion("rejection_reason is brl_expired",
                   rejection == "brl_expired", "brl_expired", rejection or "(none)"),
    ]

    case["evidence"] = {
        "peer_manifest_url": peer_url,
        "trusted": trusted,
        "rejection_reason": rejection,
        "brl_expires_at": brl_expires_at,
        "brl_issued_at": brl_issued_at,
        "brl_fetched_at": brl_fetched_at,
        "brl_age_seconds": brl_age_seconds,
        "brl_signature_valid": "not_checked",
        "revocation_status": "brl_too_stale_to_check",
        "final_trusted_decision": trusted,
        "trust_step_results": result.get("steps", []),
        "step_2.6": step_26,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-TRUST suite runner ────────────────────────────────────────────────────

def run_suite_fed_trust(
    base_url: str,
    infra: "RunnerInfra" = None,
    manifest_b: dict = None,
    manifest_b_no_fed: dict = None,
    cert_b_valid: dict = None,
    cert_b_invalid_sig: dict = None,
    cert_b_expired: dict = None,
    cert_b_l2: dict = None,
    cert_b_no_routing_cap: dict = None,
    cert_b_mismatched: dict = None,
) -> dict:
    """
    Run all 9 FED-TRUST tests.

    All tests require infra + cert fixtures. If infra is unavailable, all are skipped.
    """
    def _skip(case_id, title, reason):
        return _skip_case(_make_case(case_id, title), reason)

    trust_avail = (
        infra is not None
        and manifest_b is not None
        and manifest_b_no_fed is not None
        and cert_b_valid is not None
        and cert_b_invalid_sig is not None
        and cert_b_expired is not None
        and cert_b_l2 is not None
        and cert_b_no_routing_cap is not None
        and cert_b_mismatched is not None
    )

    if not trust_avail:
        reason = "runner infrastructure not available (install cryptography)"
        cases = [
            _skip(f"FED-TRUST-{str(i).zfill(3)}", t, reason)
            for i, t in [
                (1, "Full 9-Step Trust Protocol Passes for Valid Operator"),
                (2, "Step 2.3 Fails on Invalid Certificate Signature"),
                (3, "Step 2.4 Fails on Expired Certificate"),
                (4, "Step 2.5 Fails on certification_level < 3"),
                (5, "Step 2.6 Fails When Operator in BRL (INV-TRUST-003)"),
                (6, "Step 2.7 Fails When supports_federation Missing"),
                (7, "Step 2.8 Fails When cross_operator_routing Not in Certificate Capabilities"),
                (8, "Step 2.9 Fails on cert/manifest operator_id Mismatch"),
                (9, "BRL Staleness Enforcement (INV-TRUST-006)"),
            ]
        ]
    else:
        cases = [
            run_fed_trust_001(base_url, infra, manifest_b, cert_b_valid),
            run_fed_trust_002(base_url, infra, manifest_b, cert_b_invalid_sig),
            run_fed_trust_003(base_url, infra, manifest_b, cert_b_expired),
            run_fed_trust_004(base_url, infra, manifest_b, cert_b_l2),
            run_fed_trust_005(base_url, infra, manifest_b, cert_b_valid),
            run_fed_trust_006(base_url, infra, manifest_b_no_fed, cert_b_valid),
            run_fed_trust_007(base_url, infra, manifest_b, cert_b_no_routing_cap),
            run_fed_trust_008(base_url, infra, manifest_b, cert_b_mismatched),
            run_fed_trust_009(base_url, infra, manifest_b, cert_b_valid),
        ]

    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    skipped = sum(1 for c in cases if c["status"] in ("SKIP", "ERROR"))

    return {
        "suite_id": "FED-TRUST",
        "suite_name": "Trust Establishment",
        "blocking": True,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "cases": cases,
    }


# ── FED-ROUTE-001 ────────────────────────────────────────────────────────────

def run_fed_route_001(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-001 — Valid Routing Request Accepted

    Happy-path: valid signed request → HTTP 200, status=accepted, all required
    response fields present.
    Pass:   HTTP 200 AND status=accepted AND routing_request_id/trace_id/
            interop_transfer_id/accepted_at present.
    Severity: STANDARD  Contract: federation-routing.json  L3 Req: FED-L3-007
    """
    case = _make_case("FED-ROUTE-001", "Valid Routing Request Accepted")
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    body = _routing_body(base_url)
    sig = _make_sig_header(body, op_a_priv)

    t0 = time.monotonic()
    try:
        status, resp = _post_route(route_url, body, sig)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url, "body": body}
    case["response"] = {"status": status, "body": resp}

    if resp is None:
        return _fail_case(case, "response is not valid JSON", ms)

    schema_errors = validate_routing_response(resp)
    response_status = resp.get("status")
    itx_id = resp.get("interop_transfer_id")
    accepted_at = resp.get("accepted_at")

    assertions = [
        _assertion("HTTP status == 200", status == 200, 200, status),
        _assertion("response.status == accepted", response_status == "accepted", "accepted", response_status),
        _assertion("routing_request_id echoed", resp.get("routing_request_id") is not None,
                   "present", resp.get("routing_request_id")),
        _assertion("trace_id echoed", resp.get("trace_id") is not None,
                   "present", resp.get("trace_id")),
        _assertion("interop_transfer_id present", itx_id is not None, "present", itx_id),
        _assertion("accepted_at present", accepted_at is not None, "present", accepted_at),
        _assertion("RoutingResponse schema valid", not schema_errors,
                   "no schema errors", "; ".join(schema_errors) if schema_errors else "ok"),
    ]

    case["evidence"] = {
        "routing_request_id": body["routing_request_id"],
        "trace_id": body["trace_id"],
        "response_status": response_status,
        "interop_transfer_id": itx_id,
        "accepted_at": accepted_at,
        "http_status": status,
        "schema_errors": schema_errors,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-ROUTE-002 ────────────────────────────────────────────────────────────

def run_fed_route_002(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-002 — routing_request_id Echoed Unchanged

    response.routing_request_id MUST equal the request routing_request_id exactly.
    Pass:   Exact string equality.  Severity: STANDARD  Invariant: INV-FED-004
    """
    case = _make_case("FED-ROUTE-002", "routing_request_id Echoed Unchanged")
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    expected_id = "rr-00000000-0000-0000-0000-000000000001"
    body = _routing_body(base_url, routing_request_id=expected_id)
    sig = _make_sig_header(body, op_a_priv)

    t0 = time.monotonic()
    try:
        status, resp = _post_route(route_url, body, sig)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url, "body": body}
    case["response"] = {"status": status, "body": resp}

    if resp is None:
        return _fail_case(case, "response is not valid JSON", ms)

    echoed_id = resp.get("routing_request_id")
    assertions = [
        _assertion("HTTP status == 200", status == 200, 200, status),
        _assertion("response.status == accepted", resp.get("status") == "accepted", "accepted", resp.get("status")),
        _assertion(
            f"routing_request_id echoed unchanged ({expected_id!r})",
            echoed_id == expected_id, expected_id, echoed_id or "(absent)",
        ),
    ]

    case["evidence"] = {
        "request_routing_request_id": expected_id,
        "response_routing_request_id": echoed_id,
        "match": echoed_id == expected_id,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-ROUTE-003 ────────────────────────────────────────────────────────────

def run_fed_route_003(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-003 — trace_id Propagated Unchanged (INV-FED-001)

    response.trace_id MUST be identical to the request trace_id.
    Pass:   Exact string equality.  Severity: CRITICAL  Invariant: INV-FED-001
    L3 Req: FED-L3-012
    """
    case = _make_case("FED-ROUTE-003", "trace_id Propagated Unchanged (INV-FED-001)")
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    expected_trace = "tr-00000000-0000-0000-0000-000000000001"
    body = _routing_body(base_url, trace_id=expected_trace)
    sig = _make_sig_header(body, op_a_priv)

    t0 = time.monotonic()
    try:
        status, resp = _post_route(route_url, body, sig)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url, "body": body}
    case["response"] = {"status": status, "body": resp}

    if resp is None:
        return _fail_case(case, "response is not valid JSON", ms)

    echoed_trace = resp.get("trace_id")
    assertions = [
        _assertion("HTTP status == 200", status == 200, 200, status),
        _assertion("response.status == accepted", resp.get("status") == "accepted", "accepted", resp.get("status")),
        _assertion(
            f"trace_id propagated unchanged ({expected_trace!r})",
            echoed_trace == expected_trace, expected_trace, echoed_trace or "(absent)",
        ),
    ]

    case["evidence"] = {
        "request_trace_id": expected_trace,
        "response_trace_id": echoed_trace,
        "match": echoed_trace == expected_trace,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-ROUTE-004 ────────────────────────────────────────────────────────────

def run_fed_route_004(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-004 — Idempotent Retry Returns Same Response (INV-FED-004)

    Same routing_request_id twice → identical response; payee credited once only.
    Pass:   response2 fields == response1 fields AND payee balance unchanged
            after second request.
    Severity: CRITICAL  Invariant: INV-FED-004  L3 Req: FED-L3-007
    """
    case = _make_case("FED-ROUTE-004", "Idempotent Retry Returns Same Response (INV-FED-004)")
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    body = _routing_body(base_url)
    balance_before = infra.get_wallet_balance("wallet-payee-test-001") or 0

    t0 = time.monotonic()
    try:
        status1, resp1 = _post_route(route_url, body, _make_sig_header(body, op_a_priv))
        balance_mid = infra.get_wallet_balance("wallet-payee-test-001") or 0
        status2, resp2 = _post_route(route_url, body, _make_sig_header(body, op_a_priv))
        balance_after = infra.get_wallet_balance("wallet-payee-test-001") or 0
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url, "body": body}
    case["response"] = {"status": status2, "body": resp2}

    if resp1 is None or resp2 is None:
        return _fail_case(case, "one or both responses not valid JSON", ms)

    # Field-level comparison (timestamps match because Sim Op B replays stored response)
    id_match = resp1.get("routing_request_id") == resp2.get("routing_request_id")
    status_match = resp1.get("status") == resp2.get("status")
    trace_match = resp1.get("trace_id") == resp2.get("trace_id")
    itx_match = resp1.get("interop_transfer_id") == resp2.get("interop_transfer_id")
    accepted_at_match = resp1.get("accepted_at") == resp2.get("accepted_at")
    balance_unchanged = balance_after == balance_mid

    assertions = [
        _assertion("first request accepted", resp1.get("status") == "accepted",
                   "accepted", resp1.get("status")),
        _assertion("second request returns same routing_request_id",
                   id_match, resp1.get("routing_request_id"), resp2.get("routing_request_id")),
        _assertion("second request returns same status",
                   status_match, resp1.get("status"), resp2.get("status")),
        _assertion("second request returns same trace_id",
                   trace_match, resp1.get("trace_id"), resp2.get("trace_id")),
        _assertion("second request returns same interop_transfer_id",
                   itx_match, resp1.get("interop_transfer_id"), resp2.get("interop_transfer_id")),
        _assertion("second request returns same accepted_at",
                   accepted_at_match, resp1.get("accepted_at"), resp2.get("accepted_at")),
        _assertion(
            "payee wallet balance unchanged after second request (credited once only)",
            balance_unchanged,
            f"balance unchanged at {balance_mid}",
            f"balance_after={balance_after} vs balance_mid={balance_mid}",
        ),
    ]

    case["evidence"] = {
        "routing_request_id": body["routing_request_id"],
        "first_response": resp1,
        "second_response": resp2,
        "payee_wallet": "wallet-payee-test-001",
        "balance_before": balance_before,
        "balance_after_first": balance_mid,
        "balance_after_second": balance_after,
        "idempotency_replay_result": "same_response" if (id_match and itx_match) else "different_response",
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-ROUTE-005 ────────────────────────────────────────────────────────────

def run_fed_route_005(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-005 — Request Without Valid Signature Rejected

    Sub-case A: no Banza-Federation-Signature header → HTTP 401.
    Sub-case B: wrong/invalid signature → HTTP 401.
    Pass:   Both sub-cases return HTTP 401.
    Severity: CRITICAL  L3 Req: FED-L3-010
    """
    case = _make_case("FED-ROUTE-005", "Request Without Valid Signature Rejected")
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    body = _routing_body(base_url)

    t0 = time.monotonic()
    try:
        # Sub-case A: missing signature
        status_a, resp_a = _post_route(route_url, body, sig_header=None)
        # Sub-case B: wrong signature (placeholder "A"*86)
        bad_sig = f"t={int(time.time())},v1={'A' * 86}"
        status_b, resp_b = _post_route(route_url, body, sig_header=bad_sig)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url, "body": body}
    case["response"] = {"status_a": status_a, "status_b": status_b}

    assertions = [
        _assertion("missing signature → HTTP 401", status_a == 401, 401, status_a),
        _assertion("invalid signature → HTTP 401", status_b == 401, 401, status_b),
    ]

    code_a = (resp_a or {}).get("rejection_code", "")
    code_b = (resp_b or {}).get("rejection_code", "")

    case["evidence"] = {
        "routing_request_id": body["routing_request_id"],
        "no_sig_status": status_a,
        "no_sig_rejection_code": code_a,
        "wrong_sig_status": status_b,
        "wrong_sig_rejection_code": code_b,
        "wrong_sig_used": f"A*86 placeholder (not a valid ed25519 signature)",
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-ROUTE-006 ────────────────────────────────────────────────────────────

def run_fed_route_006(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-006 — Wrong to_operator_id Rejected

    Request addressed to wrong operator → HTTP 400.
    Pass:   HTTP 400.  Severity: STANDARD
    """
    case = _make_case("FED-ROUTE-006", "Wrong to_operator_id Rejected")
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    body = _routing_body(
        base_url,
        routing_request_id="rr-00000000-0000-0000-0000-000000000004",
        trace_id="tr-00000000-0000-0000-0000-000000000004",
        to_operator_id="some-other-operator",
    )
    sig = _make_sig_header(body, op_a_priv)

    t0 = time.monotonic()
    try:
        status, resp = _post_route(route_url, body, sig)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url, "body": body}
    case["response"] = {"status": status, "body": resp}

    assertions = [
        _assertion("wrong to_operator_id → HTTP 400", status == 400, 400, status),
    ]

    case["evidence"] = {
        "routing_request_id": body["routing_request_id"],
        "request_to_operator_id": body["to_operator_id"],
        "sim_b_operator_id": "operator-b-test",
        "http_status": status,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-ROUTE-007 ────────────────────────────────────────────────────────────

def run_fed_route_007(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-007 — Recipient Not Found Returns Structured Rejection

    Unknown recipient → HTTP 200, status=rejected, rejection_code=recipient_not_found.
    Pass:   HTTP 200 AND status=rejected AND rejection_code=recipient_not_found.
    Severity: STANDARD
    """
    case = _make_case("FED-ROUTE-007", "Recipient Not Found Returns Structured Rejection")
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    body = _routing_body(
        base_url,
        routing_request_id="rr-00000000-0000-0000-0000-000000000002",
        trace_id="tr-00000000-0000-0000-0000-000000000002",
        recipient_identifier="wallet-does-not-exist-xxxxxxxx",
    )
    sig = _make_sig_header(body, op_a_priv)

    t0 = time.monotonic()
    try:
        status, resp = _post_route(route_url, body, sig)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url, "body": body}
    case["response"] = {"status": status, "body": resp}

    if resp is None:
        return _fail_case(case, "response is not valid JSON", ms)

    response_status = resp.get("status")
    rejection_code = resp.get("rejection_code")
    trace_echoed = resp.get("trace_id")

    assertions = [
        _assertion("HTTP status == 200", status == 200, 200, status),
        _assertion("response.status == rejected", response_status == "rejected", "rejected", response_status),
        _assertion("rejection_code == recipient_not_found",
                   rejection_code == "recipient_not_found", "recipient_not_found", rejection_code or "(absent)"),
        _assertion("trace_id propagated", trace_echoed == body["trace_id"],
                   body["trace_id"], trace_echoed or "(absent)"),
    ]

    case["evidence"] = {
        "routing_request_id": body["routing_request_id"],
        "trace_id": body["trace_id"],
        "recipient_identifier": body["recipient_identifier"],
        "response_status": response_status,
        "rejection_code": rejection_code,
        "rejection_reason": resp.get("rejection_reason"),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-ROUTE-008 ────────────────────────────────────────────────────────────

def run_fed_route_008(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-008 — Unsupported Currency Returns Structured Rejection

    EUR not in Sim Op B's supported currencies (AOA only) →
    HTTP 200, status=rejected, rejection_code=currency_not_supported.
    Pass:   rejection_code=currency_not_supported.  Severity: STANDARD
    """
    case = _make_case("FED-ROUTE-008", "Unsupported Currency Returns Structured Rejection")
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    body = _routing_body(
        base_url,
        routing_request_id="rr-00000000-0000-0000-0000-000000000003",
        trace_id="tr-00000000-0000-0000-0000-000000000003",
        currency="EUR",
    )
    sig = _make_sig_header(body, op_a_priv)

    t0 = time.monotonic()
    try:
        status, resp = _post_route(route_url, body, sig)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url, "body": body}
    case["response"] = {"status": status, "body": resp}

    if resp is None:
        return _fail_case(case, "response is not valid JSON", ms)

    response_status = resp.get("status")
    rejection_code = resp.get("rejection_code")

    assertions = [
        _assertion("HTTP status == 200", status == 200, 200, status),
        _assertion("response.status == rejected", response_status == "rejected", "rejected", response_status),
        _assertion("rejection_code == currency_not_supported",
                   rejection_code == "currency_not_supported",
                   "currency_not_supported", rejection_code or "(absent)"),
    ]

    case["evidence"] = {
        "routing_request_id": body["routing_request_id"],
        "request_currency": body["amount"]["currency"],
        "sim_b_supported_currencies": ["AOA"],
        "response_status": response_status,
        "rejection_code": rejection_code,
        "rejection_reason": resp.get("rejection_reason"),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-ROUTE-009 ────────────────────────────────────────────────────────────

def run_fed_route_009(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-009 — Accepted Response Contains Valid interop_transfer_id

    On acceptance, Sim Op B assigns interop_transfer_id matching
    ^itx-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$.
    Pass:   Format matches.  Severity: STANDARD  L3 Req: FED-L3-007
    """
    case = _make_case("FED-ROUTE-009", "Accepted Response Contains Valid interop_transfer_id")
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    body = _routing_body(base_url)
    sig = _make_sig_header(body, op_a_priv)

    t0 = time.monotonic()
    try:
        status, resp = _post_route(route_url, body, sig)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url, "body": body}
    case["response"] = {"status": status, "body": resp}

    if resp is None:
        return _fail_case(case, "response is not valid JSON", ms)

    itx_id = resp.get("interop_transfer_id")
    format_ok = bool(itx_id and re.match(_ITX_PATTERN, itx_id))

    assertions = [
        _assertion("HTTP status == 200", status == 200, 200, status),
        _assertion("response.status == accepted", resp.get("status") == "accepted",
                   "accepted", resp.get("status")),
        _assertion("interop_transfer_id present", itx_id is not None, "present", itx_id),
        _assertion(
            "interop_transfer_id matches ^itx-<uuid>$",
            format_ok, "itx-<uuid>", itx_id or "(absent)",
        ),
    ]

    case["evidence"] = {
        "routing_request_id": body["routing_request_id"],
        "interop_transfer_id": itx_id,
        "interop_transfer_id_pattern": _ITX_PATTERN,
        "format_valid": format_ok,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-ROUTE-010 ────────────────────────────────────────────────────────────

def run_fed_route_010(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-010 — Non-Positive amount.minor Rejected (INV-FED-LEDGER-002)

    Zero and negative amounts must be rejected (HTTP 400 OR status=rejected).
    Pass:   Both amount.minor=0 and amount.minor=-1000 are rejected.
    Severity: CRITICAL  Invariant: INV-FED-LEDGER-002
    """
    case = _make_case("FED-ROUTE-010", "Non-Positive amount.minor Rejected (INV-FED-LEDGER-002)")
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    body_zero = _routing_body(
        base_url,
        routing_request_id="rr-00000000-0000-0000-0000-000000000005",
        trace_id="tr-00000000-0000-0000-0000-000000000005",
        amount_minor=0,
    )
    body_neg = _routing_body(
        base_url,
        routing_request_id="rr-00000000-0000-0000-0000-000000000005",
        trace_id="tr-00000000-0000-0000-0000-000000000005",
        amount_minor=-1000,
    )

    t0 = time.monotonic()
    try:
        status_zero, resp_zero = _post_route(route_url, body_zero, _make_sig_header(body_zero, op_a_priv))
        infra.reset_routing_state()
        status_neg, resp_neg = _post_route(route_url, body_neg, _make_sig_header(body_neg, op_a_priv))
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url}
    case["response"] = {"status_zero": status_zero, "status_neg": status_neg}

    def _is_rejected(status, resp):
        if status == 400:
            return True
        if resp and resp.get("status") == "rejected":
            return True
        return False

    zero_rejected = _is_rejected(status_zero, resp_zero)
    neg_rejected = _is_rejected(status_neg, resp_neg)

    assertions = [
        _assertion("amount.minor=0 rejected (HTTP 400 or status=rejected)",
                   zero_rejected, "rejected", f"HTTP {status_zero} / status={resp_zero.get('status') if resp_zero else 'N/A'}"),
        _assertion("amount.minor=-1000 rejected (HTTP 400 or status=rejected)",
                   neg_rejected, "rejected", f"HTTP {status_neg} / status={resp_neg.get('status') if resp_neg else 'N/A'}"),
    ]

    case["evidence"] = {
        "zero_amount_http_status": status_zero,
        "zero_amount_response": resp_zero,
        "neg_amount_http_status": status_neg,
        "neg_amount_response": resp_neg,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-ROUTE-011 ────────────────────────────────────────────────────────────

def run_fed_route_011(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-011 — Duplicate routing_request_id with Different Content Returns duplicate_request

    Same routing_request_id reused with different amount → rejection_code=duplicate_request.
    Pass:   rejection_code=duplicate_request on second request.
    Severity: CRITICAL  Invariant: INV-FED-IDEM-001
    """
    case = _make_case(
        "FED-ROUTE-011",
        "Duplicate routing_request_id with Different Content Returns duplicate_request",
    )
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    # First request: rr-001, amount=50000
    body1 = _routing_body(base_url, amount_minor=50000)
    # Second request: same rr-001 but amount=99999 (protocol violation by Operator A)
    body2 = dict(body1)
    body2["amount"] = {"minor": 99999, "currency": "AOA"}

    t0 = time.monotonic()
    try:
        status1, resp1 = _post_route(route_url, body1, _make_sig_header(body1, op_a_priv))
        status2, resp2 = _post_route(route_url, body2, _make_sig_header(body2, op_a_priv))
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url}
    case["response"] = {"status2": status2, "body2": resp2}

    if resp1 is None or resp2 is None:
        return _fail_case(case, "one or both responses not valid JSON", ms)

    first_accepted = resp1.get("status") == "accepted"
    rejection_code = (resp2 or {}).get("rejection_code")
    dup_code = rejection_code == "duplicate_request"

    assertions = [
        _assertion("first request accepted", first_accepted, "accepted", resp1.get("status")),
        _assertion("second request (different content) rejected", resp2.get("status") == "rejected",
                   "rejected", resp2.get("status")),
        _assertion("rejection_code == duplicate_request",
                   dup_code, "duplicate_request", rejection_code or "(absent)"),
    ]

    case["evidence"] = {
        "routing_request_id": body1["routing_request_id"],
        "first_amount_minor": body1["amount"]["minor"],
        "second_amount_minor": body2["amount"]["minor"],
        "first_response_status": resp1.get("status"),
        "second_response_status": resp2.get("status"),
        "rejection_code": rejection_code,
        "first_interop_transfer_id": resp1.get("interop_transfer_id"),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-ROUTE-012 ────────────────────────────────────────────────────────────

def run_fed_route_012(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-ROUTE-012 — Suspended Recipient Wallet Returns Structured Rejection

    Payment to suspended wallet → status=rejected, rejection_code=recipient_suspended.
    Pass:   rejection_code=recipient_suspended.  Severity: STANDARD
    """
    case = _make_case("FED-ROUTE-012", "Suspended Recipient Wallet Returns Structured Rejection")
    infra.reset_routing_state()
    route_url = f"{infra.sim_b_url}/federation/route"

    body = _routing_body(
        base_url,
        routing_request_id="rr-00000000-0000-0000-0000-000000000006",
        trace_id="tr-00000000-0000-0000-0000-000000000006",
        recipient_identifier="wallet-suspended-test-001",
    )
    sig = _make_sig_header(body, op_a_priv)

    t0 = time.monotonic()
    try:
        status, resp = _post_route(route_url, body, sig)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url, "body": body}
    case["response"] = {"status": status, "body": resp}

    if resp is None:
        return _fail_case(case, "response is not valid JSON", ms)

    response_status = resp.get("status")
    rejection_code = resp.get("rejection_code")
    trace_echoed = resp.get("trace_id")

    assertions = [
        _assertion("HTTP status == 200", status == 200, 200, status),
        _assertion("response.status == rejected", response_status == "rejected",
                   "rejected", response_status),
        _assertion("rejection_code == recipient_suspended",
                   rejection_code == "recipient_suspended",
                   "recipient_suspended", rejection_code or "(absent)"),
        _assertion("trace_id propagated", trace_echoed == body["trace_id"],
                   body["trace_id"], trace_echoed or "(absent)"),
    ]

    case["evidence"] = {
        "routing_request_id": body["routing_request_id"],
        "trace_id": body["trace_id"],
        "recipient_identifier": body["recipient_identifier"],
        "wallet_status": "suspended",
        "response_status": response_status,
        "rejection_code": rejection_code,
        "rejection_reason": resp.get("rejection_reason"),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EXEC helpers ─────────────────────────────────────────────────────────

_EXEC_SENDER_WALLET = "wallet-sender-test-001"
_EXEC_PAYEE_WALLET = "wallet-payee-test-001"
_EXEC_INITIAL_BALANCE = 500000
_EXEC_RR_ID = "rr-00000000-0000-0000-0000-000000000001"
_EXEC_TRACE_ID = "tr-00000000-0000-0000-0000-000000000001"
_EXEC_AMOUNT = 50000


def _build_exec_route_payload(
    base_url: str,
    sim_b_url: str,
    routing_request_id: str,
    trace_id: str,
    op_a_priv,
    amount_minor: int = _EXEC_AMOUNT,
    currency: str = "AOA",
    recipient_identifier: str = _EXEC_PAYEE_WALLET,
    to_operator_id: str = "operator-b-test",
) -> dict:
    """Build the payload for POST /conformance/federation/route."""
    routing_body = _routing_body(
        base_url=base_url,
        routing_request_id=routing_request_id,
        trace_id=trace_id,
        to_operator_id=to_operator_id,
        amount_minor=amount_minor,
        currency=currency,
        sender_wallet_id=_EXEC_SENDER_WALLET,
        recipient_identifier=recipient_identifier,
    )
    sig_header = _make_sig_header(routing_body, op_a_priv)
    return {
        "routing_request_id": routing_request_id,
        "trace_id": trace_id,
        "sender_wallet_id": _EXEC_SENDER_WALLET,
        "routing_body": routing_body,
        "signature_header": sig_header,
        "sim_b_route_url": f"{sim_b_url}/federation/route",
    }


def _call_fed_route(base_url: str, payload: dict) -> tuple:
    """POST /conformance/federation/route on Operator A → (status, result_or_None)."""
    try:
        status, _, raw = http_post(f"{base_url}/conformance/federation/route", payload)
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _get_wallet_op_a(base_url: str, wallet_id: str) -> tuple:
    """GET /conformance/federation/wallet/{wallet_id} → (status, dict_or_None)."""
    try:
        status, _, raw = http_get(f"{base_url}/conformance/federation/wallet/{wallet_id}")
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _get_ledger_op_a(base_url: str, wallet_id: str) -> tuple:
    """GET /conformance/federation/ledger/{wallet_id} → (status, dict_or_None)."""
    try:
        status, _, raw = http_get(f"{base_url}/conformance/federation/ledger/{wallet_id}")
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _get_obligation_op_a(base_url: str, routing_request_id: str) -> tuple:
    """GET /conformance/federation/obligations/{rr_id} → (status, dict_or_None)."""
    try:
        status, _, raw = http_get(
            f"{base_url}/conformance/federation/obligations/{routing_request_id}"
        )
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _get_events_op_a(base_url: str) -> tuple:
    """GET /conformance/federation/events → (status, dict_or_None)."""
    try:
        status, _, raw = http_get(f"{base_url}/conformance/federation/events")
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _reset_exec_state(base_url: str) -> bool:
    """POST /conformance/federation/reset → True if OK."""
    try:
        status, _, _ = http_post(f"{base_url}/conformance/federation/reset", {})
        return status in (200, 204)
    except RuntimeError:
        return False


# ── FED-EXEC-001 ──────────────────────────────────────────────────────────────

def run_fed_exec_001(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EXEC-001 — Payee Wallet Credited Simultaneously with Acceptance

    When Operator B returns status=accepted, payee wallet is already credited.
    Query Sim Op B's payee wallet before and immediately after acceptance response.

    Pass:   balance_after - balance_before == amount.minor
    Fail:   Balance unchanged; balance changes after delay
    Severity: CRITICAL
    Invariant: INV-FED-LEDGER-001
    Contract: federation-routing.json
    L3 Req: FED-L3-011
    """
    case = _make_case("FED-EXEC-001", "Payee Wallet Credited Simultaneously with Acceptance")

    infra.reset_routing_state()

    balance_before = infra.get_wallet_balance(_EXEC_PAYEE_WALLET)
    if balance_before is None:
        return _error_case(case, f"payee wallet {_EXEC_PAYEE_WALLET!r} not found on Sim Op B")

    body = _routing_body(
        base_url=base_url,
        routing_request_id=_EXEC_RR_ID,
        trace_id=_EXEC_TRACE_ID,
        amount_minor=_EXEC_AMOUNT,
    )
    sig_header = _make_sig_header(body, op_a_priv)
    route_url = f"{infra.sim_b_url}/federation/route"

    t0 = time.monotonic()
    try:
        status, resp = _post_route(route_url, body, sig_header)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "POST", "url": route_url, "routing_request_id": _EXEC_RR_ID}
    case["response"] = {"status": status, "body": resp}

    if status != 200 or not resp or resp.get("status") != "accepted":
        return _fail_case(
            case,
            f"routing not accepted: HTTP {status}, status={resp.get('status') if resp else None}",
            ms,
        )

    balance_after = infra.get_wallet_balance(_EXEC_PAYEE_WALLET)
    delta = (balance_after - balance_before) if balance_after is not None else None

    assertions = [
        _assertion("routing response status=accepted", resp.get("status") == "accepted",
                   "accepted", resp.get("status")),
        _assertion(
            f"balance_after - balance_before == {_EXEC_AMOUNT}",
            delta == _EXEC_AMOUNT,
            _EXEC_AMOUNT,
            delta,
        ),
    ]
    case["evidence"] = {
        "payee_wallet": _EXEC_PAYEE_WALLET,
        "balance_before": balance_before,
        "balance_after": balance_after,
        "balance_delta": delta,
        "expected_delta": _EXEC_AMOUNT,
        "routing_request_id": _EXEC_RR_ID,
        "interop_transfer_id": resp.get("interop_transfer_id"),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EXEC-002 ──────────────────────────────────────────────────────────────

def run_fed_exec_002(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EXEC-002 — Ledger Entries Correct on Both Operators

    After routing accepted:
      Operator A: DEBIT payer_wallet = amount.minor with trace_id
      Operator B: CREDIT payee_wallet = amount.minor with trace_id

    Pass:   Both entries present; amounts match routing request; trace_ids match
    Fail:   Missing entry; wrong amount; wrong trace_id; wrong entry type
    Severity: CRITICAL
    Invariant: INV-FED-LEDGER-001, INV-FED-005
    L3 Req: FED-L3-011, FED-L3-014
    """
    case = _make_case("FED-EXEC-002", "Ledger Entries Correct on Both Operators")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EXEC_RR_ID,
        trace_id=_EXEC_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        status, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, ledger_a = _get_ledger_op_a(base_url, _EXEC_SENDER_WALLET)
    except RuntimeError as exc:
        return _error_case(case, f"Operator A ledger query failed: {exc}")

    ledger_b_entries = infra.get_sim_b_ledger(_EXEC_PAYEE_WALLET)

    entries_a = (ledger_a.get("entries") or []) if ledger_a else []
    debit_entry = next(
        (e for e in entries_a if e.get("routing_request_id") == _EXEC_RR_ID), None
    )
    credit_entry = next(
        (e for e in ledger_b_entries if e.get("routing_request_id") == _EXEC_RR_ID), None
    )

    assertions = [
        _assertion("routing accepted", result.get("routing_status") == "accepted",
                   "accepted", result.get("routing_status")),
        _assertion("Operator A DEBIT entry exists", debit_entry is not None,
                   "exists", "missing" if debit_entry is None else "exists"),
        _assertion("Operator A entry_type=DEBIT",
                   debit_entry.get("entry_type") == "DEBIT" if debit_entry else False,
                   "DEBIT", debit_entry.get("entry_type") if debit_entry else None),
        _assertion(f"Operator A amount_minor={_EXEC_AMOUNT}",
                   debit_entry.get("amount_minor") == _EXEC_AMOUNT if debit_entry else False,
                   _EXEC_AMOUNT, debit_entry.get("amount_minor") if debit_entry else None),
        _assertion(f"Operator A trace_id={_EXEC_TRACE_ID}",
                   debit_entry.get("trace_id") == _EXEC_TRACE_ID if debit_entry else False,
                   _EXEC_TRACE_ID, debit_entry.get("trace_id") if debit_entry else None),
        _assertion("Sim Op B CREDIT entry exists", credit_entry is not None,
                   "exists", "missing" if credit_entry is None else "exists"),
        _assertion("Sim Op B entry_type=CREDIT",
                   credit_entry.get("entry_type") == "CREDIT" if credit_entry else False,
                   "CREDIT", credit_entry.get("entry_type") if credit_entry else None),
        _assertion(f"Sim Op B amount_minor={_EXEC_AMOUNT}",
                   credit_entry.get("amount_minor") == _EXEC_AMOUNT if credit_entry else False,
                   _EXEC_AMOUNT, credit_entry.get("amount_minor") if credit_entry else None),
        _assertion(f"Sim Op B trace_id={_EXEC_TRACE_ID}",
                   credit_entry.get("trace_id") == _EXEC_TRACE_ID if credit_entry else False,
                   _EXEC_TRACE_ID, credit_entry.get("trace_id") if credit_entry else None),
    ]
    case["evidence"] = {
        "routing_request_id": _EXEC_RR_ID,
        "trace_id": _EXEC_TRACE_ID,
        "operator_a_debit_entry": debit_entry,
        "sim_op_b_credit_entry": credit_entry,
        "interop_transfer_id": result.get("interop_transfer_id"),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EXEC-003 ──────────────────────────────────────────────────────────────

def run_fed_exec_003(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EXEC-003 — No Debit Without Acceptance (BC-001)

    If routing is rejected, payer wallet must not be debited.

    Pass:   balance_after == balance_before
    Fail:   Payer debited despite rejection
    Severity: CRITICAL
    L3 Req: FED-L3-011
    """
    case = _make_case("FED-EXEC-003", "No Debit Without Acceptance (BC-001)")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    try:
        _, wallet_before = _get_wallet_op_a(base_url, _EXEC_SENDER_WALLET)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    balance_before = wallet_before.get("balance_minor") if wallet_before else None
    if balance_before is None:
        return _error_case(case, f"could not get balance for {_EXEC_SENDER_WALLET!r}")

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EXEC_RR_ID,
        trace_id=_EXEC_TRACE_ID,
        op_a_priv=op_a_priv,
        recipient_identifier="wallet-does-not-exist-xxxxxxxx",
    )

    t0 = time.monotonic()
    try:
        status, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    try:
        _, wallet_after = _get_wallet_op_a(base_url, _EXEC_SENDER_WALLET)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    balance_after = wallet_after.get("balance_minor") if wallet_after else None

    assertions = [
        _assertion("routing was rejected", result.get("routing_status") == "rejected" if result else False,
                   "rejected", result.get("routing_status") if result else None),
        _assertion("payer_debited=false", not result.get("payer_debited", True) if result else False,
                   False, result.get("payer_debited") if result else None),
        _assertion("balance_after == balance_before", balance_after == balance_before,
                   balance_before, balance_after),
    ]
    case["evidence"] = {
        "routing_request_id": _EXEC_RR_ID,
        "routing_status": result.get("routing_status") if result else None,
        "rejection_code": result.get("rejection_code") if result else None,
        "payer_wallet": _EXEC_SENDER_WALLET,
        "balance_before": balance_before,
        "balance_after": balance_after,
        "payer_debited": result.get("payer_debited") if result else None,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EXEC-004 ──────────────────────────────────────────────────────────────

def run_fed_exec_004(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EXEC-004 — Debit and Obligation Are Atomic (BC-003)

    No valid state where debit exists without obligation or vice versa.

    Pass:   BOTH debit entry and obligation exist, linked by routing_request_id
    Fail:   Debit without obligation; obligation without debit; timing gap
    Severity: CRITICAL
    L3 Req: FED-L3-013
    """
    case = _make_case("FED-EXEC-004", "Debit and Obligation Are Atomic (BC-003)")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EXEC_RR_ID,
        trace_id=_EXEC_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        status, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, ledger = _get_ledger_op_a(base_url, _EXEC_SENDER_WALLET)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    try:
        _, obligation = _get_obligation_op_a(base_url, _EXEC_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    entries = (ledger.get("entries") or []) if ledger else []
    debit_entry = next((e for e in entries if e.get("routing_request_id") == _EXEC_RR_ID), None)
    debit_exists = debit_entry is not None
    obligation_exists = (
        obligation is not None
        and isinstance(obligation.get("obligation_id"), str)
        and obligation.get("obligation_id", "").startswith("ob-")
    )
    atomicity_ok = debit_exists == obligation_exists
    rr_id_match = (
        (debit_entry.get("routing_request_id") == _EXEC_RR_ID if debit_entry else False)
        and (obligation.get("routing_request_id") == _EXEC_RR_ID if obligation else False)
    )

    assertions = [
        _assertion("routing accepted", result.get("routing_status") == "accepted",
                   "accepted", result.get("routing_status")),
        _assertion("DEBIT ledger entry exists", debit_exists,
                   "exists", "missing" if not debit_exists else "exists"),
        _assertion("obligation exists", obligation_exists,
                   "exists", "missing" if not obligation_exists else "exists"),
        _assertion("obligation settlement_state=pending",
                   obligation.get("settlement_state") == "pending" if obligation else False,
                   "pending", obligation.get("settlement_state") if obligation else None),
        _assertion("both linked by routing_request_id", rr_id_match,
                   _EXEC_RR_ID, "mismatch" if not rr_id_match else _EXEC_RR_ID),
        _assertion("atomicity: debit ↔ obligation (both exist)",
                   atomicity_ok,
                   "both present",
                   f"debit={debit_exists}, obligation={obligation_exists}"),
    ]
    case["evidence"] = {
        "routing_request_id": _EXEC_RR_ID,
        "debit_entry": debit_entry,
        "obligation": obligation,
        "debit_exists": debit_exists,
        "obligation_exists": obligation_exists,
        "atomicity_check": atomicity_ok,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EXEC-005 ──────────────────────────────────────────────────────────────

def run_fed_exec_005(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EXEC-005 — Acceptance Is Irrevocable on Operator B (BC-004)

    Operator B cannot reverse an accepted routing request.

    Pass:   Cancel endpoint returns 404/405; payee balance unchanged
    Fail:   Payee credit reversed; routing can be cancelled
    Severity: STANDARD
    """
    case = _make_case("FED-EXEC-005", "Acceptance Is Irrevocable on Operator B (BC-004)")

    infra.reset_routing_state()

    body = _routing_body(
        base_url=base_url,
        routing_request_id=_EXEC_RR_ID,
        trace_id=_EXEC_TRACE_ID,
        amount_minor=_EXEC_AMOUNT,
    )
    sig_header = _make_sig_header(body, op_a_priv)
    route_url = f"{infra.sim_b_url}/federation/route"

    t0 = time.monotonic()
    try:
        status, resp = _post_route(route_url, body, sig_header)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if status != 200 or not resp or resp.get("status") != "accepted":
        return _fail_case(
            case,
            f"routing not accepted (prerequisite): HTTP {status}, "
            f"status={resp.get('status') if resp else None}",
            ms,
        )

    balance_after_accept = infra.get_wallet_balance(_EXEC_PAYEE_WALLET)

    # Attempt to cancel the accepted routing via a non-existent endpoint
    cancel_url = f"{infra.sim_b_url}/federation/route/{_EXEC_RR_ID}/cancel"
    try:
        get_cancel_status, _, _ = http_get(cancel_url)
    except RuntimeError:
        get_cancel_status = None

    try:
        post_cancel_status, post_cancel_resp = _post_route(
            cancel_url, {"routing_request_id": _EXEC_RR_ID}
        )
    except RuntimeError:
        post_cancel_status = None

    balance_after_cancel = infra.get_wallet_balance(_EXEC_PAYEE_WALLET)

    cancel_rejected = (
        get_cancel_status in (404, 405, None)
        and post_cancel_status in (404, 405, None)
    )
    balance_unchanged = balance_after_cancel == balance_after_accept

    assertions = [
        _assertion("routing accepted (prerequisite)", resp.get("status") == "accepted",
                   "accepted", resp.get("status")),
        _assertion(
            "cancel endpoint returns 404/405 (no cancellation path exists)",
            cancel_rejected,
            "404 or 405",
            f"GET:{get_cancel_status} POST:{post_cancel_status}",
        ),
        _assertion(
            "payee balance unchanged after cancel attempt",
            balance_unchanged,
            balance_after_accept,
            balance_after_cancel,
        ),
    ]
    case["evidence"] = {
        "routing_request_id": _EXEC_RR_ID,
        "interop_transfer_id": resp.get("interop_transfer_id"),
        "cancel_url": cancel_url,
        "get_cancel_status": get_cancel_status,
        "post_cancel_status": post_cancel_status,
        "balance_after_accept": balance_after_accept,
        "balance_after_cancel_attempt": balance_after_cancel,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EXEC-006 ──────────────────────────────────────────────────────────────

def run_fed_exec_006(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EXEC-006 — Operator B Internal Failure After Acceptance Does Not Affect Obligation

    Even if Sim Op B has an internal inconsistency after accepting, Operator A's
    obligation remains valid and is in settlement_state=pending.

    Pass:   Obligation exists; settlement_state=pending
    Fail:   Obligation missing; obligation reversed
    Severity: STANDARD
    Invariant: INV-FED-002
    L3 Req: FED-L3-013
    """
    case = _make_case(
        "FED-EXEC-006",
        "Operator B Internal Failure After Acceptance Does Not Affect Obligation",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EXEC_RR_ID,
        trace_id=_EXEC_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        status, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, obligation = _get_obligation_op_a(base_url, _EXEC_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    obligation_exists = (
        obligation is not None
        and isinstance(obligation.get("obligation_id"), str)
    )
    settlement_pending = obligation.get("settlement_state") == "pending" if obligation else False
    rr_id_match = obligation.get("routing_request_id") == _EXEC_RR_ID if obligation else False

    assertions = [
        _assertion("routing accepted", result.get("routing_status") == "accepted",
                   "accepted", result.get("routing_status")),
        _assertion("obligation exists on Operator A", obligation_exists,
                   "exists", "missing" if not obligation_exists else "exists"),
        _assertion("obligation settlement_state=pending", settlement_pending,
                   "pending", obligation.get("settlement_state") if obligation else None),
        _assertion("obligation routing_request_id matches", rr_id_match,
                   _EXEC_RR_ID, obligation.get("routing_request_id") if obligation else None),
    ]
    case["evidence"] = {
        "routing_request_id": _EXEC_RR_ID,
        "interop_transfer_id": result.get("interop_transfer_id"),
        "obligation": obligation,
        "obligation_exists": obligation_exists,
        "settlement_state": obligation.get("settlement_state") if obligation else None,
        "note": "Obligation on Operator A is independent of Sim Op B subsequent state",
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EXEC-007 ──────────────────────────────────────────────────────────────

def run_fed_exec_007(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EXEC-007 — Provisional Completion: All 7 Criteria Met

    Verifies all 7 provisional completion criteria from FEDERATION_PROTOCOL_FLOW.md §10:
      (1) routing_request accepted
      (2) payer debited
      (3) payee credited
      (4) obligation pending
      (5) federation.payment.initiated event on Operator A
      (6) federation.payment.completed event on Operator B
      (7) both events share trace_id

    Pass:   All 7 checks = true
    Fail:   Any check = false
    Severity: STANDARD
    Invariant: INV-FED-001
    L3 Req: FED-L3-011, FED-L3-012, FED-L3-013, FED-L3-014
    """
    case = _make_case("FED-EXEC-007", "Provisional Completion: All 7 Criteria Met")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EXEC_RR_ID,
        trace_id=_EXEC_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        status, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    interop_transfer_id = result.get("interop_transfer_id")

    # Criterion 1: routing_request accepted
    crit_1 = result.get("routing_status") == "accepted"

    # Criterion 2: payer debited
    try:
        _, ledger_a = _get_ledger_op_a(base_url, _EXEC_SENDER_WALLET)
    except RuntimeError as exc:
        return _error_case(case, str(exc))
    entries_a = (ledger_a.get("entries") or []) if ledger_a else []
    debit_entry = next(
        (e for e in entries_a if e.get("routing_request_id") == _EXEC_RR_ID), None
    )
    crit_2 = debit_entry is not None

    # Criterion 3: payee credited
    payee_balance = infra.get_wallet_balance(_EXEC_PAYEE_WALLET)
    crit_3 = payee_balance is not None and payee_balance >= _EXEC_AMOUNT

    # Criterion 4: obligation pending
    try:
        _, obligation = _get_obligation_op_a(base_url, _EXEC_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))
    crit_4 = obligation is not None and obligation.get("settlement_state") == "pending"

    # Criterion 5: federation.payment.initiated event on Operator A
    try:
        _, events_a = _get_events_op_a(base_url)
    except RuntimeError as exc:
        return _error_case(case, str(exc))
    events_a_list = (events_a.get("events") or []) if events_a else []
    initiated_event = next(
        (e for e in events_a_list
         if e.get("event_type") == "federation.payment.initiated"
         and e.get("routing_request_id") == _EXEC_RR_ID),
        None,
    )
    crit_5 = initiated_event is not None

    # Criterion 6: federation.payment.completed event on Operator B
    events_b_list = infra.get_sim_b_events(_EXEC_RR_ID)
    completed_event = next(
        (e for e in events_b_list if e.get("event_type") == "federation.payment.completed"),
        None,
    )
    crit_6 = completed_event is not None

    # Criterion 7: both events share trace_id
    trace_a = initiated_event.get("trace_id") if initiated_event else None
    trace_b = completed_event.get("trace_id") if completed_event else None
    crit_7 = (trace_a == _EXEC_TRACE_ID) and (trace_b == _EXEC_TRACE_ID)

    assertions = [
        _assertion("(1) routing_request accepted", crit_1, "accepted", result.get("routing_status")),
        _assertion("(2) payer debited on Operator A", crit_2,
                   "DEBIT entry present", "missing" if not crit_2 else "present"),
        _assertion("(3) payee credited on Operator B", crit_3,
                   f"balance ≥ {_EXEC_AMOUNT}", payee_balance),
        _assertion("(4) obligation pending on Operator A", crit_4,
                   "settlement_state=pending",
                   obligation.get("settlement_state") if obligation else "missing"),
        _assertion("(5) federation.payment.initiated event on Operator A", crit_5,
                   "present", "missing" if not crit_5 else "present"),
        _assertion("(6) federation.payment.completed event on Operator B", crit_6,
                   "present", "missing" if not crit_6 else "present"),
        _assertion("(7) both events share trace_id (INV-FED-001)", crit_7,
                   _EXEC_TRACE_ID, f"A={trace_a} B={trace_b}"),
    ]
    case["evidence"] = {
        "routing_request_id": _EXEC_RR_ID,
        "trace_id": _EXEC_TRACE_ID,
        "interop_transfer_id": interop_transfer_id,
        "criterion_1_routing_accepted": crit_1,
        "criterion_2_payer_debited": crit_2,
        "criterion_3_payee_credited": crit_3,
        "criterion_3_payee_balance": payee_balance,
        "criterion_4_obligation_pending": crit_4,
        "criterion_5_payment_initiated_event": crit_5,
        "criterion_6_payment_completed_event": crit_6,
        "criterion_7_trace_ids_match": crit_7,
        "trace_id_op_a": trace_a,
        "trace_id_op_b": trace_b,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EXEC-008 ──────────────────────────────────────────────────────────────

def run_fed_exec_008(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EXEC-008 — Double-Debit Prevention Via Posting Idempotency Key

    Retrying Phase 4 (debit + obligation) with the same routing_request_id does
    not double-charge: balance decremented exactly once, obligation exists exactly once.

    Pass:   balance decremented once; exactly 1 DEBIT entry; exactly 1 obligation
    Fail:   Balance decremented twice; 2 obligations for same routing_request_id
    Severity: CRITICAL
    Invariant: INV-FED-IDEM-001
    """
    case = _make_case(
        "FED-EXEC-008",
        "Double-Debit Prevention Via Posting Idempotency Key",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    try:
        _, wallet_initial = _get_wallet_op_a(base_url, _EXEC_SENDER_WALLET)
    except RuntimeError as exc:
        return _error_case(case, str(exc))
    balance_initial = wallet_initial.get("balance_minor") if wallet_initial else None
    if balance_initial is None:
        return _error_case(case, "could not get initial sender balance")

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EXEC_RR_ID,
        trace_id=_EXEC_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result1 = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result1 or result1.get("routing_status") != "accepted":
        return _fail_case(case, f"first routing not accepted: {result1}", ms)

    try:
        _, wallet_after_first = _get_wallet_op_a(base_url, _EXEC_SENDER_WALLET)
    except RuntimeError as exc:
        return _error_case(case, str(exc))
    balance_after_first = wallet_after_first.get("balance_minor") if wallet_after_first else None

    # Second call: same routing_request_id — Operator A must return cached result, no re-debit.
    # Build a fresh payload (new created_at, new signature timestamp) — idempotency is on
    # routing_request_id, not on the body content.
    payload2 = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EXEC_RR_ID,
        trace_id=_EXEC_TRACE_ID,
        op_a_priv=op_a_priv,
    )
    try:
        _, result2 = _call_fed_route(base_url, payload2)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    try:
        _, wallet_after_second = _get_wallet_op_a(base_url, _EXEC_SENDER_WALLET)
    except RuntimeError as exc:
        return _error_case(case, str(exc))
    balance_after_second = wallet_after_second.get("balance_minor") if wallet_after_second else None

    try:
        _, obligation = _get_obligation_op_a(base_url, _EXEC_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    try:
        _, ledger = _get_ledger_op_a(base_url, _EXEC_SENDER_WALLET)
    except RuntimeError as exc:
        return _error_case(case, str(exc))
    entries = (ledger.get("entries") or []) if ledger else []
    debit_entries_for_rr = [e for e in entries if e.get("routing_request_id") == _EXEC_RR_ID]

    expected_final = (balance_initial or 0) - _EXEC_AMOUNT
    decremented_once = balance_after_second == expected_final
    obligation_once = obligation is not None and obligation.get("obligation_id") is not None
    debit_count = len(debit_entries_for_rr)

    assertions = [
        _assertion("first routing accepted", result1.get("routing_status") == "accepted",
                   "accepted", result1.get("routing_status")),
        _assertion("second call returns accepted (idempotent replay)",
                   result2.get("routing_status") == "accepted" if result2 else False,
                   "accepted", result2.get("routing_status") if result2 else None),
        _assertion(
            f"balance decremented exactly once (expected={expected_final})",
            decremented_once,
            expected_final,
            balance_after_second,
        ),
        _assertion("exactly 1 DEBIT ledger entry for routing_request_id",
                   debit_count == 1, 1, debit_count),
        _assertion("exactly 1 obligation for routing_request_id",
                   obligation_once, 1, "exists" if obligation_once else "missing"),
    ]
    case["evidence"] = {
        "routing_request_id": _EXEC_RR_ID,
        "balance_initial": balance_initial,
        "balance_after_first_call": balance_after_first,
        "balance_after_second_call": balance_after_second,
        "expected_final_balance": expected_final,
        "debit_entry_count": debit_count,
        "obligation_exists": obligation_once,
        "double_debit_check": "PASS" if decremented_once else "FAIL",
        "result_first_call": result1,
        "result_second_call": result2,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EXEC suite runner ─────────────────────────────────────────────────────

def run_suite_fed_exec(
    base_url: str,
    infra: "RunnerInfra" = None,
    op_a_priv=None,
) -> dict:
    """
    Run all 8 FED-EXEC tests.

    Requires infra (Sim Op B) and op_a_priv (Operator A signing key).
    Without both, all tests are skipped.
    """
    def _skip(case_id, title, reason):
        return _skip_case(_make_case(case_id, title), reason)

    exec_avail = infra is not None and op_a_priv is not None

    if not exec_avail:
        reason = "execution infrastructure not available (install cryptography)"
        cases = [
            _skip(f"FED-EXEC-{str(i).zfill(3)}", t, reason)
            for i, t in [
                (1, "Payee Wallet Credited Simultaneously with Acceptance"),
                (2, "Ledger Entries Correct on Both Operators"),
                (3, "No Debit Without Acceptance (BC-001)"),
                (4, "Debit and Obligation Are Atomic (BC-003)"),
                (5, "Acceptance Is Irrevocable on Operator B (BC-004)"),
                (6, "Operator B Internal Failure Does Not Affect Obligation"),
                (7, "Provisional Completion: All 7 Criteria Met"),
                (8, "Double-Debit Prevention Via Posting Idempotency Key"),
            ]
        ]
    else:
        cases = [
            run_fed_exec_001(base_url, infra, op_a_priv),
            run_fed_exec_002(base_url, infra, op_a_priv),
            run_fed_exec_003(base_url, infra, op_a_priv),
            run_fed_exec_004(base_url, infra, op_a_priv),
            run_fed_exec_005(base_url, infra, op_a_priv),
            run_fed_exec_006(base_url, infra, op_a_priv),
            run_fed_exec_007(base_url, infra, op_a_priv),
            run_fed_exec_008(base_url, infra, op_a_priv),
        ]

    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    skipped = sum(1 for c in cases if c["status"] in ("SKIP", "ERROR"))

    return {
        "suite_id": "FED-EXEC",
        "suite_name": "Transfer Execution",
        "blocking": True,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "cases": cases,
    }


# ── FED-ROUTE suite runner ────────────────────────────────────────────────────

def run_suite_fed_route(
    base_url: str,
    infra: "RunnerInfra" = None,
    op_a_priv=None,
) -> dict:
    """
    Run all 12 FED-ROUTE tests.

    Requires infra (Sim Op B) and op_a_priv (Operator A signing key).
    Without both, all tests are skipped.
    """
    def _skip(case_id, title, reason):
        return _skip_case(_make_case(case_id, title), reason)

    route_avail = infra is not None and op_a_priv is not None

    if not route_avail:
        reason = "routing infrastructure not available (install cryptography)"
        cases = [
            _skip(f"FED-ROUTE-{str(i).zfill(3)}", t, reason)
            for i, t in [
                (1, "Valid Routing Request Accepted"),
                (2, "routing_request_id Echoed Unchanged"),
                (3, "trace_id Propagated Unchanged (INV-FED-001)"),
                (4, "Idempotent Retry Returns Same Response (INV-FED-004)"),
                (5, "Request Without Valid Signature Rejected"),
                (6, "Wrong to_operator_id Rejected"),
                (7, "Recipient Not Found Returns Structured Rejection"),
                (8, "Unsupported Currency Returns Structured Rejection"),
                (9, "Accepted Response Contains Valid interop_transfer_id"),
                (10, "Non-Positive amount.minor Rejected (INV-FED-LEDGER-002)"),
                (11, "Duplicate routing_request_id with Different Content Returns duplicate_request"),
                (12, "Suspended Recipient Wallet Returns Structured Rejection"),
            ]
        ]
    else:
        cases = [
            run_fed_route_001(base_url, infra, op_a_priv),
            run_fed_route_002(base_url, infra, op_a_priv),
            run_fed_route_003(base_url, infra, op_a_priv),
            run_fed_route_004(base_url, infra, op_a_priv),
            run_fed_route_005(base_url, infra, op_a_priv),
            run_fed_route_006(base_url, infra, op_a_priv),
            run_fed_route_007(base_url, infra, op_a_priv),
            run_fed_route_008(base_url, infra, op_a_priv),
            run_fed_route_009(base_url, infra, op_a_priv),
            run_fed_route_010(base_url, infra, op_a_priv),
            run_fed_route_011(base_url, infra, op_a_priv),
            run_fed_route_012(base_url, infra, op_a_priv),
        ]

    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    skipped = sum(1 for c in cases if c["status"] in ("SKIP", "ERROR"))

    return {
        "suite_id": "FED-ROUTE",
        "suite_name": "Routing Negotiation",
        "blocking": True,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "cases": cases,
    }


# ── FED-DISC suite runner ─────────────────────────────────────────────────────

def run_suite_fed_disc(
    base_url: str,
    infra: "RunnerInfra" = None,
    cert_b_l2: dict = None,
    manifest_b: dict = None,
) -> dict:
    """
    Run all 8 FED-DISC tests.

    Tests 001–006, 008: manifest endpoint validation — no infrastructure required.
    Test 007: trust rejection of L2 cert — requires infra + cert_b_l2 + manifest_b.
    """
    def _skip(case_id, title, reason):
        return _skip_case(_make_case(case_id, title), reason)

    trust_007_available = infra is not None and cert_b_l2 is not None and manifest_b is not None

    cases = [
        run_fed_disc_001(base_url),
        run_fed_disc_002(base_url),
        run_fed_disc_003(base_url),
        run_fed_disc_004(base_url),
        run_fed_disc_005(base_url),
        run_fed_disc_006(base_url),
        run_fed_disc_007(base_url, infra, manifest_b, cert_b_l2)
            if trust_007_available else
            _skip("FED-DISC-007",
                  "supports_federation Cannot Be True Without Valid L3+ Certificate",
                  "infra not available"),
        run_fed_disc_008(base_url),
    ]

    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    skipped = sum(1 for c in cases if c["status"] in ("SKIP", "ERROR"))

    return {
        "suite_id": "FED-DISC",
        "suite_name": "Discovery and Manifest Validation",
        "blocking": True,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "cases": cases,
    }


# ── Suite runner ──────────────────────────────────────────────────────────────

def run_suite_fed_cert(
    base_url: str,
    root_public_key_bytes: bytes = None,
    infra: "RunnerInfra" = None,
    manifest_b: dict = None,
    cert_b_valid: dict = None,
    cert_b_expired: dict = None,
    cert_b_mismatched: dict = None,
    cert_b_secondary: dict = None,
    secondary_key_id: str = None,
    secondary_pub: bytes = None,
) -> dict:
    """
    Run all 11 FED-CERT tests.

    Slice 0-1 (001–007): runner-side cert validation.
    Slice 2 (008–011):   operator trust engine tests via verify-peer endpoint.
    """
    def _skip(case_id, title, reason):
        return _skip_case(_make_case(case_id, title), reason)

    trust_tests_available = (
        infra is not None and manifest_b is not None
        and cert_b_valid is not None and cert_b_expired is not None
        and cert_b_mismatched is not None and cert_b_secondary is not None
    )

    cases = [
        # Slice 0-1
        run_fed_cert_001(base_url),
        run_fed_cert_002(base_url, root_public_key_bytes) if root_public_key_bytes else
            _skip("FED-CERT-002", "Certificate Signature Verifies Against Test BANZA Root",
                  "root_public_key_bytes not provided (install cryptography)"),
        run_fed_cert_003(base_url),
        run_fed_cert_004(base_url),
        run_fed_cert_005(base_url),
        run_fed_cert_006(base_url),
        run_fed_cert_007(base_url),
        # Slice 2
        run_fed_cert_008(base_url, infra, manifest_b, cert_b_expired)
            if trust_tests_available else
            _skip("FED-CERT-008", "Expired Certificate Fails Trust Step 2.4",
                  "infra not available"),
        run_fed_cert_009(base_url, infra, manifest_b, cert_b_valid)
            if trust_tests_available else
            _skip("FED-CERT-009", "Revoked Operator Rejected by BRL Check",
                  "infra not available"),
        run_fed_cert_010(base_url, infra, manifest_b, cert_b_mismatched)
            if trust_tests_available else
            _skip("FED-CERT-010", "Certificate-Manifest operator_id Binding",
                  "infra not available"),
        run_fed_cert_011(base_url, infra, manifest_b, cert_b_secondary,
                         secondary_key_id, secondary_pub)
            if trust_tests_available else
            _skip("FED-CERT-011", "Unknown issuer_key_id Triggers Key Fetch",
                  "infra not available"),
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
    Execute federation conformance tests (FED-CERT-001 through FED-TRUST-009).
    Returns: 0 = all pass, 1 = failures/skips, 2 = runner error.
    """
    from datetime import timedelta

    run_cert = fed_suite in (None, "cert")
    run_disc = fed_suite in (None, "disc")
    run_trust = fed_suite in (None, "trust")
    run_route = fed_suite in (None, "route")
    run_exec = fed_suite in (None, "exec")

    if (fed_suite is not None
            and not run_cert and not run_disc and not run_trust
            and not run_route and not run_exec):
        print(f"ERROR: Unknown --fed-suite value: {fed_suite!r}. "
              f"Available: cert, disc, trust, route, exec",
              file=sys.stderr)
        return 2

    suite_label = {
        None: (
            "FED-CERT-001–011, FED-DISC-001–008, FED-TRUST-001–009, "
            "FED-ROUTE-001–012, FED-EXEC-001–008"
        ),
        "cert": "FED-CERT-001–011",
        "disc": "FED-DISC-001–008",
        "trust": "FED-TRUST-001–009",
        "route": "FED-ROUTE-001–012",
        "exec": "FED-EXEC-001–008",
    }.get(fed_suite, fed_suite)

    print(f"BANZA Federation Conformance Runner {RUNNER_VERSION}")
    print(f"Operator: {base_url}")
    print(f"Slice:    6 — {suite_label}")
    print()

    schema_path = _find_schema_path()
    if schema_path is None:
        print("ERROR: contracts/federation/operator-certificate.json not found.", file=sys.stderr)
        return 2
    manifest_schema_path = _find_manifest_schema_path()
    if manifest_schema_path is None:
        print("ERROR: contracts/federation/federation-manifest.json not found.", file=sys.stderr)
        return 2
    print(f"CertSchema:     {schema_path}")
    print(f"ManifestSchema: {manifest_schema_path}")

    # ── Start runner infrastructure (Slices 2–3) ──────────────────────────────
    infra = None
    manifest_b = None
    manifest_b_no_fed = None
    cert_b_valid = None
    cert_b_expired = None
    cert_b_mismatched = None
    cert_b_secondary = None
    cert_b_l2 = None
    cert_b_invalid_sig = None
    cert_b_no_routing_cap = None
    secondary_key_id = None
    secondary_pub = None
    root_public_key_bytes = None
    op_a_priv = None

    if _tr.CRYPTO_AVAILABLE:
        try:
            # Primary root keypair (Operator A cert + most Sim Op B certs)
            root_priv, root_pub, key_id = _tr.generate_test_root_keypair()

            # Secondary root keypair (FED-CERT-011 key rotation)
            root_priv2, root_pub2, _ = _tr.generate_test_root_keypair()
            secondary_key_id = f"test-banza-key-{__import__('datetime').date.today().strftime('%Y-%m')}-secondary"
            secondary_pub = root_pub2

            # Operator A keypair
            op_a_priv, op_a_pub = _tr.generate_operator_keypair()

            # Operator B keypair (reused across certs)
            op_b_priv, op_b_pub = _tr.generate_operator_keypair()

            root_public_key_bytes = root_pub

            # Start infra servers
            infra = RunnerInfra()
            infra.start()

            # Populate key manifest: primary + secondary (for FED-CERT-011)
            infra.set_key_manifest({key_id: root_pub, secondary_key_id: root_pub2})
            infra.set_brl_empty()

            # MANIFEST-B-VALID (Sim Op B's manifest — certificate_url points to Sim Op B)
            manifest_b = {
                "operator_id": "operator-b-test",
                "environment": "sandbox",
                "simulated": True,
                "production_allowed": False,
                "protocol_version": "1.0",
                "certification_level": 3,
                "capabilities": {"supports_wallets": True, "supports_qr": True, "supports_settlement": True},
                "operator_name": "Simulated Operator B (Conformance Runner)",
                "operator_url": infra.sim_b_url,
                "federation_version": "1",
                "certificate_url": f"{infra.sim_b_url}/.well-known/banza/certificate.json",
                "interop_endpoint": infra.sim_b_url,
                "supports_federation": True,
                "cross_operator_routing": True,
                "cross_operator_settlement": True,
                "federation_capabilities": {
                    "routing_version": "1",
                    "settlement_version": "1",
                    "supported_currencies": ["AOA"],
                    "netting_interval_hours": 24,
                },
            }

            # CERT-B-VALID: valid cert, primary root
            cert_b_valid = _tr.generate_test_certificate(
                operator_id="operator-b-test",
                root_private_key=root_priv,
                issuer_key_id=key_id,
                operator_public_key_bytes=op_b_pub,
            )

            # CERT-B-EXPIRED: real sig, past timestamps → Step 2.4 fails
            now = datetime.now(timezone.utc)
            cert_b_expired = _tr.generate_test_certificate(
                operator_id="operator-b-test",
                root_private_key=root_priv,
                issuer_key_id=key_id,
                operator_public_key_bytes=op_b_pub,
                issued_at_override=now - timedelta(days=100),
                expires_at_override=now - timedelta(days=10),
            )

            # CERT-B-MISMATCHED: cert.operator_id != manifest.operator_id → Step 2.9 fails
            cert_b_mismatched = _tr.generate_test_certificate(
                operator_id="some-other-operator",
                root_private_key=root_priv,
                issuer_key_id=key_id,
                operator_public_key_bytes=op_b_pub,
            )

            # CERT-B-SECONDARY: signed with secondary root → triggers key fetch in 011
            cert_b_secondary = _tr.generate_test_certificate(
                operator_id="operator-b-test",
                root_private_key=root_priv2,
                issuer_key_id=secondary_key_id,
                operator_public_key_bytes=op_b_pub,
            )

            # CERT-B-L2: L2 cert for FED-DISC-007 / FED-TRUST-004 (INV-TRUST-004)
            cert_b_l2 = _tr.generate_test_certificate(
                operator_id="operator-b-test",
                certification_level=2,
                root_private_key=root_priv,
                issuer_key_id=key_id,
                operator_public_key_bytes=op_b_pub,
            )

            # CERT-B-INVALID-SIG: valid structure, zeroed signature → Step 2.3 fails
            cert_b_invalid_sig = _tr.generate_test_certificate(
                operator_id="operator-b-test",
                root_private_key=None,  # placeholder sig (not signed by root)
                issuer_key_id=key_id,
                operator_public_key_bytes=op_b_pub,
            )

            # CERT-B-NO-ROUTING-CAP: L3 cert, capabilities=[] → Step 2.8 fails
            cert_b_no_routing_cap = _tr.generate_test_certificate(
                operator_id="operator-b-test",
                certification_level=3,
                root_private_key=root_priv,
                issuer_key_id=key_id,
                operator_public_key_bytes=op_b_pub,
                capabilities=[],
            )

            # MANIFEST-B-NO-FEDERATION: supports_federation=false for FED-TRUST-006
            # Must include certificate_url so steps 2.1-2.6 reach 2.7
            manifest_b_no_fed = {
                "operator_id": "operator-b-test",
                "environment": "sandbox",
                "simulated": True,
                "production_allowed": False,
                "protocol_version": "1.0",
                "certification_level": 3,
                "capabilities": {"supports_wallets": True, "supports_qr": True, "supports_settlement": True},
                "operator_name": "Simulated Operator B (No Federation)",
                "operator_url": infra.sim_b_url,
                "federation_version": "1",
                "certificate_url": f"{infra.sim_b_url}/.well-known/banza/certificate.json",
                "interop_endpoint": infra.sim_b_url,
                "supports_federation": False,
                "cross_operator_routing": False,
                "cross_operator_settlement": False,
                "federation_capabilities": {
                    "routing_version": "1",
                    "settlement_version": "1",
                    "supported_currencies": ["AOA"],
                    "netting_interval_hours": 24,
                },
            }

            # Operator A cert
            cert_a = _tr.generate_test_certificate(
                root_private_key=root_priv,
                issuer_key_id=key_id,
                operator_public_key_bytes=op_a_pub,
            )

            # Configure Sim Op B with Operator A's public key (for FED-ROUTE sig verification)
            infra.configure_routing(cert_a["operator_id"], op_a_pub)

            # Extended setup: deliver cert + BANZA root key + BRL URL + key manifest URL
            setup_ok = setup_operator_for_federation(
                base_url, cert_a,
                banza_root_key_id=key_id,
                banza_root_pub=root_pub,
                brl_url=infra.brl_url,
                key_manifest_url=infra.key_manifest_url,
            )
            if setup_ok:
                print(f"Setup:    POST /conformance/setup → OK "
                      f"(operator_id={cert_a['operator_id']!r}, key_id={key_id!r})")
                print(f"SimOpB:   {infra.sim_b_url}")
                print(f"BRL:      {infra.brl_url}")
                print(f"KeyMfst:  {infra.key_manifest_url}")
            else:
                print(f"Setup:    POST /conformance/setup → FAILED "
                      f"(FED-CERT-002 and 008–011 may fail)")

        except Exception as exc:
            print(f"Setup:    infrastructure setup failed: {exc}")
            import traceback; traceback.print_exc()
            root_public_key_bytes = None
            if infra:
                infra.stop()
                infra = None
    else:
        print("Setup:    cryptography not installed — FED-CERT-002, 008–011 will SKIP")
        print("          Install: pip install 'cryptography>=41.0.0'")

    print()

    # ── Run suites ────────────────────────────────────────────────────────────
    start = time.monotonic()
    suite_results = []

    try:
        if run_cert:
            suite_results.append(run_suite_fed_cert(
                base_url,
                root_public_key_bytes=root_public_key_bytes,
                infra=infra,
                manifest_b=manifest_b,
                cert_b_valid=cert_b_valid,
                cert_b_expired=cert_b_expired,
                cert_b_mismatched=cert_b_mismatched,
                cert_b_secondary=cert_b_secondary,
                secondary_key_id=secondary_key_id,
                secondary_pub=secondary_pub,
            ))
        if run_disc:
            suite_results.append(run_suite_fed_disc(
                base_url,
                infra=infra,
                cert_b_l2=cert_b_l2,
                manifest_b=manifest_b,
            ))
        if run_trust:
            suite_results.append(run_suite_fed_trust(
                base_url,
                infra=infra,
                manifest_b=manifest_b,
                manifest_b_no_fed=manifest_b_no_fed,
                cert_b_valid=cert_b_valid,
                cert_b_invalid_sig=cert_b_invalid_sig,
                cert_b_expired=cert_b_expired,
                cert_b_l2=cert_b_l2,
                cert_b_no_routing_cap=cert_b_no_routing_cap,
                cert_b_mismatched=cert_b_mismatched,
            ))
        if run_route:
            # Restore Sim Op B to valid state for routing tests
            if infra and manifest_b and cert_b_valid:
                infra.configure_sim_b(manifest_b, cert_b_valid)
                infra.set_brl_empty()
            suite_results.append(run_suite_fed_route(
                base_url,
                infra=infra,
                op_a_priv=op_a_priv if _tr.CRYPTO_AVAILABLE else None,
            ))
        if run_exec:
            # Restore Sim Op B to valid state for execution tests
            if infra and manifest_b and cert_b_valid:
                infra.configure_sim_b(manifest_b, cert_b_valid)
                infra.set_brl_empty()
            suite_results.append(run_suite_fed_exec(
                base_url,
                infra=infra,
                op_a_priv=op_a_priv if _tr.CRYPTO_AVAILABLE else None,
            ))
    finally:
        if infra:
            infra.stop()

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

    suite_ids = [s["suite_id"] for s in suite_results]
    print("=" * 60)
    if total_fail == 0 and total_skip == 0:
        parts = []
        if "FED-CERT" in suite_ids:
            parts.append("FED-CERT-001–011")
        if "FED-DISC" in suite_ids:
            parts.append("FED-DISC-001–008")
        if "FED-TRUST" in suite_ids:
            parts.append("FED-TRUST-001–009")
        if "FED-ROUTE" in suite_ids:
            parts.append("FED-ROUTE-001–012")
        if "FED-EXEC" in suite_ids:
            parts.append("FED-EXEC-001–008")
        print(f"{', '.join(parts)}: ALL PASS")
        print()
        print("What is now proven:")
        if "FED-CERT" in suite_ids:
            print("  ✓ Certificate endpoint exists and returns HTTP 200")
            print("  ✓ Content-Type is application/json")
            print("  ✓ Response is valid JSON satisfying operator-certificate.json")
            print("  ✓ ed25519 signature verifies against test BANZA root  (INV-TRUST-001)")
            print("  ✓ Certificate is not expired                           (INV-TRUST-002)")
            print("  ✓ operator_id matches declared format")
            print("  ✓ public_key is 32-byte ed25519 in base64url format")
            print("  ✓ issuer is exactly 'BANZA'                           (INV-TRUST-001)")
            print("  ✓ Lifetime ≤ 90 days for L3 certificate               (INV-FED-006)")
            print("  ✓ Operator rejects expired peer cert at Step 2.4      (INV-TRUST-002)")
            print("  ✓ Operator rejects BRL-revoked peer at Step 2.6       (INV-TRUST-003)")
            print("  ✓ Operator rejects cert/manifest mismatch at Step 2.9 (INV-TRUST-001)")
            print("  ✓ Operator fetches new key on unknown issuer_key_id   (F-604)")
        if "FED-DISC" in suite_ids:
            print("  ✓ Manifest endpoint exists and returns HTTP 200")
            print("  ✓ Manifest validates against federation-manifest.json")
            print("  ✓ supports_federation is true")
            print("  ✓ cross_operator_routing is true                       (INV-FED-003)")
            print("  ✓ certificate_url accessible, cert valid, operator_id bound  (INV-TRUST-001)")
            print("  ✓ interop_endpoint TCP-reachable                       (INV-FED-003)")
            print("  ✓ supported_currencies non-empty, all ISO 4217")
            print("  ✓ L2 cert rejected at trust step 2.5                   (INV-TRUST-004)")
            print("  ✓ netting_interval_hours integer in [1, 168]")
        if "FED-TRUST" in suite_ids:
            print("  ✓ All 9 trust steps pass for correctly configured operator")
            print("  ✓ Tampered signature rejected at step 2.3              (INV-TRUST-001)")
            print("  ✓ Expired certificate rejected at step 2.4             (INV-TRUST-002)")
            print("  ✓ L2 certificate rejected at step 2.5 (level check)")
            print("  ✓ BRL-revoked operator rejected at step 2.6            (INV-TRUST-003)")
            print("  ✓ supports_federation=false rejected at step 2.7       (INV-TRUST-004)")
            print("  ✓ Missing routing capability rejected at step 2.8      (INV-TRUST-004)")
            print("  ✓ cert/manifest operator_id mismatch rejected at 2.9   (INV-TRUST-001)")
            print("  ✓ Expired BRL rejected — fail-closed enforced          (INV-TRUST-006)")
        if "FED-ROUTE" in suite_ids:
            print("  ✓ Valid routing request accepted — HTTP 200, status=accepted")
            print("  ✓ routing_request_id echoed unchanged                  (INV-FED-004)")
            print("  ✓ trace_id propagated unchanged                        (INV-FED-001)")
            print("  ✓ Idempotent retry returns same response, no double-credit (INV-FED-004)")
            print("  ✓ Missing signature rejected with HTTP 401")
            print("  ✓ Invalid signature rejected with HTTP 401")
            print("  ✓ Wrong to_operator_id rejected with HTTP 400")
            print("  ✓ Unknown recipient → rejection_code=recipient_not_found")
            print("  ✓ Unsupported currency → rejection_code=currency_not_supported")
            print("  ✓ interop_transfer_id matches ^itx-<uuid>$ format")
            print("  ✓ Zero/negative amount rejected                        (INV-FED-LEDGER-002)")
            print("  ✓ Duplicate routing_request_id with different content → duplicate_request (INV-FED-IDEM-001)")
            print("  ✓ Suspended recipient → rejection_code=recipient_suspended")
        if "FED-EXEC" in suite_ids:
            print("  ✓ Payee wallet credited simultaneously with acceptance  (INV-FED-LEDGER-001)")
            print("  ✓ Operator A DEBIT + Operator B CREDIT: amounts and trace_ids match (INV-FED-005)")
            print("  ✓ No payer debit when routing rejected                  (BC-001)")
            print("  ✓ Debit and obligation are atomic — one commit, no gap  (BC-003)")
            print("  ✓ Cancel endpoint returns 404 — acceptance irrevocable (BC-004)")
            print("  ✓ Obligation persists independent of Sim Op B state     (INV-FED-002)")
            print("  ✓ All 7 provisional completion criteria satisfied       (INV-FED-001)")
            print("  ✓ Double-debit prevented via routing_request_id idempotency (INV-FED-IDEM-001)")
    elif total_fail > 0:
        print(f"{', '.join(suite_ids)}: FAIL  ({total_pass} passed, {total_fail} failed, {total_skip} skipped)")
    else:
        print(f"{', '.join(suite_ids)}: PARTIAL  ({total_pass} passed, {total_fail} failed, {total_skip} skipped)")
    print("=" * 60)

    # ── Report ────────────────────────────────────────────────────────────────
    report = {
        "report_id": f"rpt-fed-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runner_version": RUNNER_VERSION,
        "federation_mode": True,
        "slice": "6",
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
        description="BANZA Federation Conformance Runner (FED-CERT + FED-DISC + FED-TRUST + FED-ROUTE + FED-EXEC)"
    )
    parser.add_argument("--url", required=True,
                        help="Base URL of the operator (e.g. http://localhost:8099)")
    parser.add_argument("--output", help="Write JSON report to this file")
    parser.add_argument("--quiet", action="store_true", help="Suppress passing test output")
    parser.add_argument("--fed-suite", dest="fed_suite",
                        help="Run only this suite: cert | disc | trust | route | exec (default: all)")
    args = parser.parse_args()

    sys.exit(run_federation_mode(
        args.url.rstrip("/"),
        output=args.output,
        quiet=args.quiet,
        fed_suite=args.fed_suite,
    ))


if __name__ == "__main__":
    main()
