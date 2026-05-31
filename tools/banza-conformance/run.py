#!/usr/bin/env python3
"""
the reference operator Conformance Runner v1.0

Connects to a running a BANZA operator and executes conformance suites.
Produces a JSON report and exits with a non-zero code if any required
suite fails.

Usage:
    python3 run.py --url http://localhost:3000 [--level 1] [--suite operators] [--output report.json]

Requires:
    Python 3.8+ — stdlib only, no pip dependencies.
"""

import argparse
import json
import sys
import time
import uuid
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from typing import Any, Optional

RUNNER_VERSION = "1.0.0"
PROTOCOL_VERSION = "1.0"

# ─── HTTP helpers ─────────────────────────────────────────────────────────────

def http_request(
    url: str,
    method: str = "GET",
    body: Optional[dict] = None,
    headers: Optional[dict] = None,
    timeout: int = 10,
) -> tuple[int, Any]:
    data = json.dumps(body).encode() if body is not None else None
    req_headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, raw
    except Exception as exc:
        raise RuntimeError(f"HTTP {method} {url} failed: {exc}") from exc


# ─── Result builders ──────────────────────────────────────────────────────────

def make_case(case_id: str, title: str) -> dict:
    return {
        "id": case_id,
        "title": title,
        "status": "SKIP",
        "duration_ms": 0,
        "request": None,
        "response": None,
        "failure_reason": None,
        "assertions": [],
    }


def pass_case(case: dict, duration_ms: int, assertions: list) -> dict:
    case["status"] = "PASS"
    case["duration_ms"] = duration_ms
    case["assertions"] = assertions
    return case


def fail_case(case: dict, reason: str, duration_ms: int = 0, assertions: list = None) -> dict:
    case["status"] = "FAIL"
    case["duration_ms"] = duration_ms
    case["failure_reason"] = reason
    case["assertions"] = assertions or []
    return case


def error_case(case: dict, reason: str) -> dict:
    case["status"] = "ERROR"
    case["failure_reason"] = reason
    return case


def assertion(name: str, passed: bool, expected=None, actual=None) -> dict:
    r = {"assertion": name, "passed": passed}
    if expected is not None:
        r["expected"] = expected
    if actual is not None:
        r["actual"] = actual
    return r


def check_field(body: Any, field: str, expected: Any = None) -> tuple[bool, dict]:
    if not isinstance(body, dict):
        return False, assertion(f"response is object", False, actual=type(body).__name__)
    present = field in body and body[field] is not None
    if not present:
        return False, assertion(f"field '{field}' present", False, actual=None)
    if expected is not None and body[field] != expected:
        return False, assertion(f"field '{field}' == {expected!r}", False, expected=expected, actual=body[field])
    return True, assertion(f"field '{field}' present" + (f" == {expected!r}" if expected is not None else ""), True)


# ─── Suite runners ────────────────────────────────────────────────────────────

def run_health(base_url: str) -> list:
    cases = []

    # HEALTH-001
    c = make_case("HEALTH-001", "GET /health returns 200 with status ok")
    t0 = time.monotonic()
    try:
        status, body = http_request(f"{base_url}/health")
        ms = int((time.monotonic() - t0) * 1000)
        assertions = [
            assertion("status == 200", status == 200, 200, status),
            assertion("body.status == 'ok'", isinstance(body, dict) and body.get("status") == "ok", "ok", body.get("status") if isinstance(body, dict) else None),
        ]
        c["request"] = {"method": "GET", "path": "/health"}
        c["response"] = {"status": status, "body": body}
        if all(a["passed"] for a in assertions):
            pass_case(c, ms, assertions)
        else:
            fail_case(c, "health check failed", ms, assertions)
    except Exception as exc:
        error_case(c, str(exc))
    cases.append(c)

    # HEALTH-002
    c = make_case("HEALTH-002", "Health response declares simulated=true and production_allowed=false")
    t0 = time.monotonic()
    try:
        status, body = http_request(f"{base_url}/health")
        ms = int((time.monotonic() - t0) * 1000)
        assertions = [
            assertion("status == 200", status == 200, 200, status),
        ]
        for field, expected in [("simulated", True), ("production_allowed", False), ("environment", "sandbox")]:
            ok, a = check_field(body, field, expected)
            assertions.append(a)
        c["request"] = {"method": "GET", "path": "/health"}
        c["response"] = {"status": status, "body": body}
        if all(a["passed"] for a in assertions):
            pass_case(c, ms, assertions)
        else:
            fail_case(c, "sandbox invariant check failed", ms, assertions)
    except Exception as exc:
        error_case(c, str(exc))
    cases.append(c)

    return cases


def run_wallets(base_url: str, ctx: dict) -> list:
    cases = []
    wallet_id = None

    # WLT-001 — create wallet
    c = make_case("WLT-001", "POST /wallets creates a wallet and returns wallet_id")
    t0 = time.monotonic()
    try:
        label = f"conformance-wlt-{uuid.uuid4().hex[:8]}"
        payload = {"label": label, "currency": "AOA"}
        status, body = http_request(f"{base_url}/wallets", "POST", payload)
        ms = int((time.monotonic() - t0) * 1000)
        assertions = [
            assertion("status == 201", status == 201, 201, status),
        ]
        for field in ["id", "label", "currency", "balance_minor"]:
            ok, a = check_field(body, field)
            assertions.append(a)
        c["request"] = {"method": "POST", "path": "/wallets", "body": payload}
        c["response"] = {"status": status, "body": body}
        if all(a["passed"] for a in assertions):
            pass_case(c, ms, assertions)
            wallet_id = body.get("id") if isinstance(body, dict) else None
            ctx["wallet_a"] = wallet_id
        else:
            fail_case(c, "wallet creation failed", ms, assertions)
    except Exception as exc:
        error_case(c, str(exc))
    cases.append(c)

    # WLT-002 — create second wallet
    c = make_case("WLT-002", "POST /wallets creates a second wallet (merchant)")
    t0 = time.monotonic()
    try:
        label = f"conformance-merchant-{uuid.uuid4().hex[:8]}"
        payload = {"label": label, "currency": "AOA"}
        status, body = http_request(f"{base_url}/wallets", "POST", payload)
        ms = int((time.monotonic() - t0) * 1000)
        assertions = [
            assertion("status == 201", status == 201, 201, status),
        ]
        ok, a = check_field(body, "id")
        assertions.append(a)
        c["request"] = {"method": "POST", "path": "/wallets", "body": payload}
        c["response"] = {"status": status, "body": body}
        if all(a["passed"] for a in assertions):
            pass_case(c, ms, assertions)
            ctx["wallet_b"] = body.get("id") if isinstance(body, dict) else None
        else:
            fail_case(c, "second wallet creation failed", ms, assertions)
    except Exception as exc:
        error_case(c, str(exc))
    cases.append(c)

    # WLT-004 — GET wallet
    c = make_case("WLT-004", "GET /wallets/:id returns the wallet")
    if not ctx.get("wallet_a"):
        c["failure_reason"] = "skipped: wallet_a not available"
        cases.append(c)
    else:
        t0 = time.monotonic()
        try:
            status, body = http_request(f"{base_url}/wallets/{ctx['wallet_a']}")
            ms = int((time.monotonic() - t0) * 1000)
            assertions = [
                assertion("status == 200", status == 200, 200, status),
            ]
            for field in ["id", "balance_minor"]:
                ok, a = check_field(body, field)
                assertions.append(a)
            c["request"] = {"method": "GET", "path": f"/wallets/{ctx['wallet_a']}"}
            c["response"] = {"status": status, "body": body}
            if all(a["passed"] for a in assertions):
                pass_case(c, ms, assertions)
            else:
                fail_case(c, "wallet GET failed", ms, assertions)
        except Exception as exc:
            error_case(c, str(exc))
        cases.append(c)

    # WLT-005 — GET unknown wallet → 404
    c = make_case("WLT-005", "GET /wallets/:id for unknown wallet returns 404")
    t0 = time.monotonic()
    try:
        status, body = http_request(f"{base_url}/wallets/wallet-does-not-exist")
        ms = int((time.monotonic() - t0) * 1000)
        assertions = [assertion("status == 404", status == 404, 404, status)]
        c["request"] = {"method": "GET", "path": "/wallets/wallet-does-not-exist"}
        c["response"] = {"status": status, "body": body}
        if all(a["passed"] for a in assertions):
            pass_case(c, ms, assertions)
        else:
            fail_case(c, "expected 404 for unknown wallet", ms, assertions)
    except Exception as exc:
        error_case(c, str(exc))
    cases.append(c)

    return cases


def run_transfers(base_url: str, ctx: dict) -> list:
    cases = []

    def seed_funds(wallet_id: str, amount: int):
        http_request(f"{base_url}/wallets/{wallet_id}/seed", "POST", {"amount_minor": amount, "currency": "AOA"})

    if ctx.get("wallet_a"):
        seed_funds(ctx["wallet_a"], 1_000_000)

    # TRF-001 — basic transfer
    c = make_case("TRF-001", "POST /transfers — basic success")
    if not (ctx.get("wallet_a") and ctx.get("wallet_b")):
        c["failure_reason"] = "skipped: wallets not available"
        cases.append(c)
    else:
        t0 = time.monotonic()
        try:
            idem = f"conformance-TRF-001-{uuid.uuid4().hex[:8]}"
            payload = {
                "from_wallet_id": ctx["wallet_a"],
                "to_wallet_id": ctx["wallet_b"],
                "amount_minor": 50000,
                "currency": "AOA",
                "idempotency_key": idem,
            }
            status, body = http_request(f"{base_url}/transfers", "POST", payload)
            ms = int((time.monotonic() - t0) * 1000)
            assertions = [
                assertion("status == 201", status == 201, 201, status),
            ]
            for field in ["id", "from_wallet_id", "to_wallet_id", "amount_minor", "currency"]:
                ok, a = check_field(body, field)
                assertions.append(a)
            id_ok = isinstance(body, dict) and isinstance(body.get("id"), str) and body.get("id", "").startswith("txfr-")
            assertions.append(assertion("id starts with 'txfr-'", id_ok))
            c["request"] = {"method": "POST", "path": "/transfers", "body": payload}
            c["response"] = {"status": status, "body": body}
            if all(a["passed"] for a in assertions):
                pass_case(c, ms, assertions)
                ctx["transfer_id"] = body.get("id") if isinstance(body, dict) else None
                ctx["transfer_trace_id"] = body.get("trace_id") if isinstance(body, dict) else None
            else:
                fail_case(c, "transfer creation failed", ms, assertions)
        except Exception as exc:
            error_case(c, str(exc))
        cases.append(c)

    # TRF-002 — idempotency
    c = make_case("TRF-002", "Same idempotency key returns same result")
    if not ctx.get("transfer_id"):
        c["failure_reason"] = "skipped: no transfer from TRF-001"
        cases.append(c)
    else:
        t0 = time.monotonic()
        try:
            idem = f"conformance-TRF-002-idem"
            payload = {
                "from_wallet_id": ctx["wallet_a"],
                "to_wallet_id": ctx["wallet_b"],
                "amount_minor": 10000,
                "currency": "AOA",
                "idempotency_key": idem,
            }
            _, first = http_request(f"{base_url}/transfers", "POST", payload)
            status, second = http_request(f"{base_url}/transfers", "POST", payload)
            ms = int((time.monotonic() - t0) * 1000)
            first_id = first.get("id") if isinstance(first, dict) else None
            second_id = second.get("id") if isinstance(second, dict) else None
            assertions = [
                assertion("status == 200 or 201 on second call", status in (200, 201), "200 or 201", status),
                assertion("same id returned", first_id == second_id and first_id is not None, first_id, second_id),
            ]
            c["response"] = {"status": status, "body": second}
            if all(a["passed"] for a in assertions):
                pass_case(c, ms, assertions)
            else:
                fail_case(c, "idempotency failed", ms, assertions)
        except Exception as exc:
            error_case(c, str(exc))
        cases.append(c)

    # TRF-003 — insufficient funds
    c = make_case("TRF-003", "Insufficient funds returns 422")
    if not (ctx.get("wallet_a") and ctx.get("wallet_b")):
        c["failure_reason"] = "skipped: wallets not available"
        cases.append(c)
    else:
        t0 = time.monotonic()
        try:
            payload = {
                "from_wallet_id": ctx["wallet_a"],
                "to_wallet_id": ctx["wallet_b"],
                "amount_minor": 999_000_000_000,
                "currency": "AOA",
            }
            status, body = http_request(f"{base_url}/transfers", "POST", payload)
            ms = int((time.monotonic() - t0) * 1000)
            assertions = [assertion("status == 422", status == 422, 422, status)]
            c["request"] = {"method": "POST", "path": "/transfers", "body": payload}
            c["response"] = {"status": status, "body": body}
            if all(a["passed"] for a in assertions):
                pass_case(c, ms, assertions)
            else:
                fail_case(c, "expected 422 for insufficient funds", ms, assertions)
        except Exception as exc:
            error_case(c, str(exc))
        cases.append(c)

    # TRF-008 — trace_id on transfer response (Level 2)
    c = make_case("TRF-008", "Transfer response includes trace_id starting with tr-")
    if not ctx.get("transfer_id"):
        c["failure_reason"] = "skipped: no transfer available"
        cases.append(c)
    else:
        t0 = time.monotonic()
        try:
            status, body = http_request(f"{base_url}/transfers/{ctx['transfer_id']}")
            ms = int((time.monotonic() - t0) * 1000)
            trace_id = body.get("trace_id") if isinstance(body, dict) else None
            assertions = [
                assertion("status == 200", status == 200, 200, status),
                assertion("trace_id present", trace_id is not None),
                assertion("trace_id starts with 'tr-'", isinstance(trace_id, str) and trace_id.startswith("tr-")),
            ]
            c["response"] = {"status": status, "body": body}
            if all(a["passed"] for a in assertions):
                pass_case(c, ms, assertions)
            else:
                fail_case(c, "trace_id missing or malformed", ms, assertions)
        except Exception as exc:
            error_case(c, str(exc))
        cases.append(c)

    return cases


def run_traces(base_url: str, ctx: dict) -> list:
    cases = []

    # TRF-009 — GET /traces/:id returns trace view
    c = make_case("TRF-009", "GET /traces/:id returns trace view for transfer")
    trace_id = ctx.get("transfer_trace_id")
    if not trace_id:
        c["failure_reason"] = "skipped: no trace_id available (run transfers suite first)"
        cases.append(c)
    else:
        t0 = time.monotonic()
        try:
            status, body = http_request(f"{base_url}/traces/{trace_id}")
            ms = int((time.monotonic() - t0) * 1000)
            assertions = [
                assertion("status == 200", status == 200, 200, status),
            ]
            for field in ["trace_id", "timeline"]:
                ok, a = check_field(body, field)
                assertions.append(a)
            has_entries = isinstance(body, dict) and isinstance(body.get("timeline"), list) and len(body.get("timeline", [])) > 0
            assertions.append(assertion("timeline has at least one entry", has_entries))
            c["request"] = {"method": "GET", "path": f"/traces/{trace_id}"}
            c["response"] = {"status": status, "body": body}
            if all(a["passed"] for a in assertions):
                pass_case(c, ms, assertions)
            else:
                fail_case(c, "trace view incomplete", ms, assertions)
        except Exception as exc:
            error_case(c, str(exc))
        cases.append(c)

    # EVT-004 — events include trace_id
    c = make_case("EVT-004", "Events include trace_id, correlation_id")
    t0 = time.monotonic()
    try:
        status, body = http_request(f"{base_url}/events/history?limit=10")
        ms = int((time.monotonic() - t0) * 1000)
        events = body.get("events", []) if isinstance(body, dict) else (body if isinstance(body, list) else [])
        if not events:
            c["failure_reason"] = "no events available to inspect"
            cases.append(c)
        else:
            evt = events[0]
            assertions = [
                assertion("status == 200", status == 200, 200, status),
                assertion("event has trace_id", isinstance(evt, dict) and "trace_id" in evt),
                assertion("event has correlation_id", isinstance(evt, dict) and "correlation_id" in evt),
            ]
            c["response"] = {"status": status, "body": {"events_count": len(events)}}
            if all(a["passed"] for a in assertions):
                pass_case(c, ms, assertions)
            else:
                fail_case(c, "events missing trace fields", ms, assertions)
            cases.append(c)
    except Exception as exc:
        error_case(c, str(exc))
        cases.append(c)

    return cases


def run_manifest(base_url: str) -> list:
    cases = []

    # MAN-001
    c = make_case("MAN-001", "Operator manifest responds at /.well-known/banza/operator.json")
    t0 = time.monotonic()
    try:
        status, body = http_request(f"{base_url}/.well-known/banza/operator.json")
        ms = int((time.monotonic() - t0) * 1000)
        assertions = [assertion("status == 200", status == 200, 200, status)]
        for field in ["operator_id", "environment", "simulated", "production_allowed", "capabilities"]:
            ok, a = check_field(body, field)
            assertions.append(a)
        c["request"] = {"method": "GET", "path": "/.well-known/banza/operator.json"}
        c["response"] = {"status": status, "body": body}
        if all(a["passed"] for a in assertions):
            pass_case(c, ms, assertions)
        else:
            fail_case(c, "manifest missing required fields", ms, assertions)
    except Exception as exc:
        error_case(c, str(exc))
    cases.append(c)

    # MAN-002
    c = make_case("MAN-002", "Sandbox operator declares simulated=true, production_allowed=false")
    t0 = time.monotonic()
    try:
        status, body = http_request(f"{base_url}/.well-known/banza/operator.json")
        ms = int((time.monotonic() - t0) * 1000)
        assertions = [assertion("status == 200", status == 200, 200, status)]
        for field, expected in [("simulated", True), ("production_allowed", False), ("environment", "sandbox")]:
            ok, a = check_field(body, field, expected)
            assertions.append(a)
        c["response"] = {"status": status, "body": body}
        if all(a["passed"] for a in assertions):
            pass_case(c, ms, assertions)
        else:
            fail_case(c, "sandbox safety invariant violation in manifest", ms, assertions)
    except Exception as exc:
        error_case(c, str(exc))
    cases.append(c)

    # MAN-003
    c = make_case("MAN-003", "Manifest capabilities includes required fields")
    t0 = time.monotonic()
    try:
        status, body = http_request(f"{base_url}/.well-known/banza/operator.json")
        ms = int((time.monotonic() - t0) * 1000)
        caps = body.get("capabilities", {}) if isinstance(body, dict) else {}
        assertions = [assertion("status == 200", status == 200, 200, status)]
        for cap in ["supports_wallets", "supports_qr", "supports_settlement"]:
            assertions.append(assertion(f"capabilities.{cap} present", cap in caps))
        c["response"] = {"status": status, "body": body}
        if all(a["passed"] for a in assertions):
            pass_case(c, ms, assertions)
        else:
            fail_case(c, "capabilities missing required fields", ms, assertions)
    except Exception as exc:
        error_case(c, str(exc))
    cases.append(c)

    return cases


# ─── Suite registry ───────────────────────────────────────────────────────────

SUITES = {
    "health": {
        "id": "health",
        "name": "Health",
        "certification_level": 0,
        "runner": run_health,
        "needs_ctx": False,
    },
    "wallets": {
        "id": "wallets",
        "name": "Wallet management",
        "certification_level": 0,
        "runner": run_wallets,
        "needs_ctx": True,
    },
    "transfers": {
        "id": "transfers",
        "name": "Transfer basics",
        "certification_level": 0,
        "runner": run_transfers,
        "needs_ctx": True,
    },
    "traces": {
        "id": "traces",
        "name": "Financial traceability",
        "certification_level": 2,
        "runner": run_traces,
        "needs_ctx": True,
    },
    "manifest": {
        "id": "manifest",
        "name": "Operator manifest",
        "certification_level": 3,
        "runner": run_manifest,
        "needs_ctx": False,
    },
}

LEVEL_SUITES = {
    0: ["health", "wallets", "transfers"],
    1: ["health", "wallets", "transfers"],
    2: ["health", "wallets", "transfers", "traces"],
    3: ["health", "wallets", "transfers", "traces", "manifest"],
    4: ["health", "wallets", "transfers", "traces", "manifest"],
}


# ─── Report builder ───────────────────────────────────────────────────────────

def build_suite_result(suite_def: dict, case_results: list) -> dict:
    passed = sum(1 for c in case_results if c["status"] == "PASS")
    failed = sum(1 for c in case_results if c["status"] == "FAIL")
    skipped = sum(1 for c in case_results if c["status"] in ("SKIP", "ERROR"))
    return {
        "suite_id": suite_def["id"],
        "suite_name": suite_def["name"],
        "certification_level": suite_def["certification_level"],
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "cases": case_results,
    }


def compute_certification_level(suite_results: list) -> int:
    passed_suites = {s["suite_id"] for s in suite_results if s["failed"] == 0}
    level = -1
    for lvl in range(5):
        required = LEVEL_SUITES.get(lvl, [])
        if all(s in passed_suites for s in required):
            level = lvl
        else:
            break
    return level


def build_report(
    operator_url: str,
    operator_id: Optional[str],
    suite_results: list,
    start_time: float,
) -> dict:
    total = sum(s["passed"] + s["failed"] + s["skipped"] for s in suite_results)
    passed = sum(s["passed"] for s in suite_results)
    failed = sum(s["failed"] for s in suite_results)
    skipped = sum(s["skipped"] for s in suite_results)
    duration_ms = int((time.monotonic() - start_time) * 1000)

    return {
        "report_id": f"rpt-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runner_version": RUNNER_VERSION,
        "operator_url": operator_url,
        "operator_id": operator_id,
        "protocol_version": PROTOCOL_VERSION,
        "certification_level_achieved": compute_certification_level(suite_results),
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration_ms": duration_ms,
        },
        "suites": suite_results,
        "invariant_results": [],
        "errors": [],
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="the reference operator Conformance Runner")
    parser.add_argument("--url", required=True, help="Base URL of the operator (e.g. http://localhost:3000)")
    parser.add_argument("--level", type=int, default=4, help="Maximum certification level to test (0–4, default 4)")
    parser.add_argument("--suite", help="Run a single suite by ID (health, wallets, transfers, traces, manifest)")
    parser.add_argument("--output", help="Write JSON report to this file")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-case output")
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    start_time = time.monotonic()

    print(f"the reference operator Conformance Runner {RUNNER_VERSION}")
    print(f"Operator: {base_url}")
    print(f"Level:    {args.level}")
    print()

    # Determine suites to run
    if args.suite:
        if args.suite not in SUITES:
            print(f"Unknown suite: {args.suite}. Available: {', '.join(SUITES)}", file=sys.stderr)
            sys.exit(2)
        suites_to_run = [args.suite]
    else:
        suites_to_run = LEVEL_SUITES.get(args.level, list(SUITES.keys()))

    # Probe connectivity
    try:
        http_request(f"{base_url}/health", timeout=5)
    except Exception as exc:
        print(f"ERROR: Cannot reach operator at {base_url}: {exc}", file=sys.stderr)
        sys.exit(2)

    # Try to get operator_id from manifest
    operator_id = None
    try:
        _, manifest = http_request(f"{base_url}/.well-known/banza/operator.json")
        if isinstance(manifest, dict):
            operator_id = manifest.get("operator_id")
    except Exception:
        pass

    ctx: dict = {}
    suite_results = []

    for suite_id in suites_to_run:
        suite_def = SUITES[suite_id]
        print(f"[Suite] {suite_def['name']} (Level {suite_def['certification_level']})")

        try:
            if suite_def["needs_ctx"]:
                cases = suite_def["runner"](base_url, ctx)
            else:
                cases = suite_def["runner"](base_url)
        except Exception as exc:
            cases = [error_case(make_case(suite_id, suite_def["name"]), str(exc))]

        for c in cases:
            icon = {"PASS": "✓", "FAIL": "✗", "SKIP": "–", "ERROR": "E"}.get(c["status"], "?")
            if not args.quiet or c["status"] != "PASS":
                print(f"  {icon} {c['id']} — {c['title']}")
                if c["status"] in ("FAIL", "ERROR") and c.get("failure_reason"):
                    print(f"      {c['failure_reason']}")

        result = build_suite_result(suite_def, cases)
        suite_results.append(result)
        s_pass = result["passed"]
        s_fail = result["failed"]
        s_skip = result["skipped"]
        print(f"  → {s_pass} passed, {s_fail} failed, {s_skip} skipped")
        print()

    report = build_report(base_url, operator_id, suite_results, start_time)
    level = report["certification_level_achieved"]
    total = report["summary"]["total"]
    passed = report["summary"]["passed"]
    failed = report["summary"]["failed"]

    level_names = {-1: "None", 0: "Reference-compatible", 1: "Protocol-compatible", 2: "Trace-compatible", 3: "Federation-ready", 4: "Settlement-compatible"}
    print(f"{'=' * 60}")
    print(f"Certification level achieved: {level} — {level_names.get(level, 'Unknown')}")
    print(f"Total: {total}  Passed: {passed}  Failed: {failed}")
    print(f"{'=' * 60}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"Report written to {args.output}")
    else:
        print(json.dumps(report, indent=2, default=str))

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
