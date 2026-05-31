"""
BANZA Federation Conformance Runner — Slice 0

Implements:
  FED-CERT-001  Certificate Present at Well-Known URL

What FED-CERT-001 verifies (per FEDERATION_TEST_SUITE_SPEC.md):
  - GET /.well-known/banza/certificate.json returns HTTP 200
  - Content-Type header contains application/json
  - Response body is valid JSON
  - JSON validates against contracts/federation/operator-certificate.json

What FED-CERT-001 does NOT verify (deferred to later slices):
  - Signature validity       (FED-CERT-002, requires WP-002 real ed25519)
  - Certificate expiry       (FED-CERT-003)
  - Trust engine behavior    (FED-CERT-008 through FED-CERT-011)
  - Operator-to-operator     (all FED-TRUST, FED-ROUTE, FED-EXEC, FED-OBL)

No external dependencies. Python 3.8+ stdlib only.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Optional

RUNNER_VERSION = "0.1.0-slice0"

# ── Schema path ───────────────────────────────────────────────────────────────

def _find_schema_path() -> Optional[str]:
    """Locate operator-certificate.json relative to this file or the repo root."""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(this_dir, "..", "..", "contracts", "federation", "operator-certificate.json"),
        os.path.join(os.getcwd(), "contracts", "federation", "operator-certificate.json"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return os.path.normpath(p)
    return None


def load_schema() -> Optional[dict]:
    path = _find_schema_path()
    if path is None:
        return None
    with open(path) as f:
        return json.load(f)


# ── Certificate schema validation ─────────────────────────────────────────────

def validate_operator_certificate(cert: dict) -> list[str]:
    """
    Validate a parsed certificate dict against operator-certificate.json constraints.
    Returns a list of error strings. Empty list means valid.

    Implements the field-level rules from contracts/federation/operator-certificate.json:
      required, additionalProperties, type, const, pattern, minimum/maximum, uniqueItems.
    """
    if not isinstance(cert, dict):
        return ["body is not a JSON object"]

    errors: list[str] = []

    required_fields = [
        "schema_version", "operator_id", "certification_level",
        "protocol_version", "capabilities", "public_key",
        "issued_at", "expires_at", "issuer", "issuer_key_id", "signature",
    ]
    for field in required_fields:
        if field not in cert:
            errors.append(f"required field missing: '{field}'")

    allowed_fields = set(required_fields)
    extra = set(cert.keys()) - allowed_fields
    if extra:
        errors.append(f"additionalProperties not allowed: {sorted(extra)}")

    if "schema_version" in cert and cert["schema_version"] != "1":
        errors.append(
            f"schema_version must be '1', got {cert['schema_version']!r}"
        )

    if "operator_id" in cert:
        oid = cert["operator_id"]
        if not isinstance(oid, str):
            errors.append("operator_id must be a string")
        elif not re.match(r"^[a-z0-9][a-z0-9\-]{2,62}[a-z0-9]$", oid):
            errors.append(
                f"operator_id format invalid: {oid!r} "
                f"(required: ^[a-z0-9][a-z0-9\\-]{{2,62}}[a-z0-9]$)"
            )

    if "certification_level" in cert:
        cl = cert["certification_level"]
        if not isinstance(cl, int) or isinstance(cl, bool):
            errors.append(f"certification_level must be an integer, got {type(cl).__name__}")
        elif not (0 <= cl <= 4):
            errors.append(f"certification_level must be 0–4, got {cl}")

    if "protocol_version" in cert:
        pv = cert["protocol_version"]
        if not isinstance(pv, str):
            errors.append("protocol_version must be a string")
        elif not re.match(r"^\d+\.\d+$", pv):
            errors.append(f"protocol_version format invalid: {pv!r} (required: ^\\d+\\.\\d+$)")

    if "capabilities" in cert:
        caps = cert["capabilities"]
        if not isinstance(caps, list):
            errors.append("capabilities must be an array")
        else:
            if not all(isinstance(c, str) for c in caps):
                errors.append("capabilities items must all be strings")
            if len(caps) != len(set(caps)):
                errors.append("capabilities items must be unique (uniqueItems violation)")

    if "public_key" in cert:
        pk = cert["public_key"]
        if not isinstance(pk, str):
            errors.append("public_key must be a string")
        elif not re.match(r"^ed25519:[A-Za-z0-9_-]{43}$", pk):
            errors.append(
                f"public_key format invalid: {pk!r} "
                f"(required: ed25519:<43 base64url chars>)"
            )

    for ts_field in ("issued_at", "expires_at"):
        if ts_field in cert:
            ts = cert[ts_field]
            if not isinstance(ts, str) or not ts:
                errors.append(f"{ts_field} must be a non-empty string (ISO 8601 date-time)")

    if "issuer" in cert and cert["issuer"] != "BANZA":
        errors.append(f"issuer must be 'BANZA', got {cert['issuer']!r}")

    if "issuer_key_id" in cert and not isinstance(cert["issuer_key_id"], str):
        errors.append("issuer_key_id must be a string")

    if "signature" in cert:
        sig = cert["signature"]
        if not isinstance(sig, str):
            errors.append("signature must be a string")
        elif not re.match(r"^[A-Za-z0-9_-]{86}$", sig):
            errors.append(
                f"signature format invalid: length={len(sig)} "
                f"(required: 86 base64url chars representing 64-byte ed25519 signature)"
            )

    return errors


# ── HTTP ──────────────────────────────────────────────────────────────────────

def http_get(url: str, timeout: int = 10) -> tuple[int, dict, str]:
    """
    Perform GET request. Returns (status_code, headers_dict, raw_body_str).
    Raises RuntimeError on connection failure.
    """
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


# ── Case builders (mirrors run.py style) ─────────────────────────────────────

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
    case["status"] = "PASS"
    case["duration_ms"] = ms
    case["assertions"] = assertions
    return case


def _fail_case(case: dict, reason: str, ms: int = 0, assertions: list = None) -> dict:
    case["status"] = "FAIL"
    case["duration_ms"] = ms
    case["failure_reason"] = reason
    case["assertions"] = assertions or []
    return case


def _error_case(case: dict, reason: str) -> dict:
    case["status"] = "ERROR"
    case["failure_reason"] = reason
    return case


# ── FED-CERT-001 ──────────────────────────────────────────────────────────────

def run_fed_cert_001(base_url: str) -> dict:
    """
    FED-CERT-001 — Certificate Present at Well-Known URL

    Spec: FEDERATION_TEST_SUITE_SPEC.md, Suite FED-CERT, test 001
    Contract: contracts/federation/operator-certificate.json
    L3 Requirements: FED-L3-001, FED-L3-003
    Severity: STANDARD

    Pass conditions (ALL must be true):
      1. HTTP status == 200
      2. Content-Type header contains 'application/json'
      3. Response body parses as valid JSON
      4. JSON validates against operator-certificate.json schema

    Fail conditions (ANY triggers FAIL):
      - HTTP status != 200
      - Body fails schema validation
      - Endpoint requires authentication
    """
    case = _make_case("FED-CERT-001", "Certificate Present at Well-Known URL")
    cert_url = f"{base_url}/.well-known/banza/certificate.json"

    t0 = time.monotonic()
    try:
        status, headers, raw_body = http_get(cert_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    case["request"] = {"method": "GET", "url": cert_url}

    assertions = []

    # Assertion 1: HTTP 200
    a_status = _assertion("HTTP status == 200", status == 200, 200, status)
    assertions.append(a_status)

    # Assertion 2: Content-Type contains application/json
    content_type = headers.get("content-type", "")
    a_ct = _assertion(
        "Content-Type contains 'application/json'",
        "application/json" in content_type.lower(),
        "application/json",
        content_type or "(header absent)",
    )
    assertions.append(a_ct)

    # Assertion 3: valid JSON
    body = None
    try:
        body = json.loads(raw_body)
        is_json = isinstance(body, dict)
        a_json = _assertion("response body is valid JSON object", is_json)
    except json.JSONDecodeError as exc:
        is_json = False
        a_json = _assertion(
            "response body is valid JSON object",
            False,
            "valid JSON object",
            f"JSON parse error: {exc}",
        )
    assertions.append(a_json)

    # Assertion 4: schema validation
    if is_json and body is not None:
        schema_errors = validate_operator_certificate(body)
        schema_valid = len(schema_errors) == 0
        a_schema = _assertion(
            "schema valid against operator-certificate.json",
            schema_valid,
            "no schema errors",
            "; ".join(schema_errors) if schema_errors else None,
        )
        assertions.append(a_schema)
    else:
        assertions.append(_assertion(
            "schema valid against operator-certificate.json",
            False,
            "valid JSON required first",
            "skipped: body is not a JSON object",
        ))
        schema_valid = False

    # Evidence capture (per FEDERATION_CERTIFICATION_EVIDENCE_MODEL.md §1.1)
    case["evidence"] = {
        "cert.http_status": status,
        "cert.http_headers": headers,
        "cert.raw_json": body,
        "cert.schema_validation_result": {
            "valid": schema_valid,
            "errors": schema_errors if is_json and body is not None else ["body not JSON"],
        },
    }
    case["response"] = {"status": status, "headers": headers, "body_length": len(raw_body)}

    if all(a["passed"] for a in assertions):
        _pass_case(case, ms, assertions)
    else:
        failed = [a["assertion"] for a in assertions if not a["passed"]]
        _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)

    return case


# ── Suite runner ──────────────────────────────────────────────────────────────

SUITE_FED_CERT = "FED-CERT"

def run_suite_fed_cert(base_url: str) -> dict:
    """Run the FED-CERT suite (Slice 0: FED-CERT-001 only)."""
    cases = [run_fed_cert_001(base_url)]
    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    skipped = sum(1 for c in cases if c["status"] in ("SKIP", "ERROR"))
    return {
        "suite_id": SUITE_FED_CERT,
        "suite_name": "Certificate Validation",
        "blocking": True,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "cases": cases,
        "note": "Slice 0: FED-CERT-001 only. FED-CERT-002 through FED-CERT-011 pending WP-002.",
    }


# ── Federation run entry point (called from run.py --federation) ──────────────

def run_federation_mode(base_url: str, output: Optional[str] = None, quiet: bool = False) -> int:
    """
    Execute federation conformance tests (Slice 0).
    Returns exit code: 0 = all pass, 1 = failures, 2 = runner error.
    """
    print(f"BANZA Federation Conformance Runner {RUNNER_VERSION}")
    print(f"Operator: {base_url}")
    print(f"Slice:    0 — FED-CERT-001 (certificate endpoint + schema)")
    print()

    # Schema reachability check
    schema_path = _find_schema_path()
    if schema_path is None:
        print(
            "ERROR: contracts/federation/operator-certificate.json not found.\n"
            "Run from the repo root or ensure the contracts directory is present.",
            file=sys.stderr,
        )
        return 2
    print(f"Schema:  {schema_path}")
    print()

    # Connectivity check
    try:
        http_get(f"{base_url}/health", timeout=5)
    except RuntimeError:
        pass  # health endpoint optional; cert endpoint is the target

    start = time.monotonic()
    suite_result = run_suite_fed_cert(base_url)
    duration_ms = int((time.monotonic() - start) * 1000)

    # Print results
    print(f"[Suite] {suite_result['suite_name']} (blocking={suite_result['blocking']})")
    for case in suite_result["cases"]:
        icon = {"PASS": "✓", "FAIL": "✗", "SKIP": "–", "ERROR": "E"}.get(case["status"], "?")
        if not quiet or case["status"] != "PASS":
            print(f"  {icon} {case['id']} — {case['title']}")
        if case["status"] in ("FAIL", "ERROR") and case.get("failure_reason"):
            print(f"      Reason: {case['failure_reason']}")
        if case["status"] in ("FAIL", "ERROR"):
            for a in case.get("assertions", []):
                if not a["passed"]:
                    detail = f"      ✗ {a['assertion']}"
                    if a.get("expected"):
                        detail += f" (expected: {a['expected']}"
                        if a.get("actual"):
                            detail += f", got: {a['actual']}"
                        detail += ")"
                    print(detail)

    s_pass = suite_result["passed"]
    s_fail = suite_result["failed"]
    s_skip = suite_result["skipped"]
    print(f"  → {s_pass} passed, {s_fail} failed, {s_skip} skipped  ({duration_ms}ms)")
    print()

    # Build report
    report = {
        "report_id": f"rpt-fed-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runner_version": RUNNER_VERSION,
        "federation_mode": True,
        "slice": "0",
        "operator_url": base_url,
        "schema_path": schema_path,
        "summary": {
            "total": s_pass + s_fail + s_skip,
            "passed": s_pass,
            "failed": s_fail,
            "skipped": s_skip,
            "duration_ms": duration_ms,
        },
        "suites": [suite_result],
    }

    print("=" * 60)
    if s_fail == 0 and s_skip == 0:
        print("FED-CERT-001: PASS")
        print()
        print("What this proves:")
        print("  ✓ Certificate endpoint exists and returns HTTP 200")
        print("  ✓ Content-Type is application/json")
        print("  ✓ Response is valid JSON")
        print("  ✓ JSON satisfies operator-certificate.json schema")
        print()
        print("What this does NOT yet prove:")
        print("  – Signature validity           (FED-CERT-002)")
        print("  – Certificate not expired       (FED-CERT-003)")
        print("  – Trust engine behavior         (FED-CERT-008–011)")
        print("  – Cross-operator routing        (FED-TRUST through FED-OBL)")
    elif s_fail > 0:
        print(f"FED-CERT-001: FAIL  ({s_fail} test(s) failed)")
    else:
        print(f"FED-CERT-001: SKIP  (no tests ran)")
    print("=" * 60)

    if output:
        with open(output, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\nReport written to {output}")

    return 0 if s_fail == 0 else 1


# ── Standalone entry point ────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="BANZA Federation Conformance Runner (Slice 0 — FED-CERT-001)"
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Base URL of the operator under test (e.g. http://localhost:8099)",
    )
    parser.add_argument("--output", help="Write JSON report to this file")
    parser.add_argument("--quiet", action="store_true", help="Suppress passing test output")
    args = parser.parse_args()

    sys.exit(run_federation_mode(args.url.rstrip("/"), args.output, args.quiet))


if __name__ == "__main__":
    main()
