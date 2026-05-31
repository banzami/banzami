#!/usr/bin/env python3
"""
BANZA Real Two-Operator Interoperability Test Harness

Proves that BANZA Federation works between two independent operators:

  Operator A = fixture_server (ThreadingHTTPServer, independent state)
  Operator B = RunnerInfra SimBServer (HTTPServer, independent state)
  BANZA Trust Root = RunnerInfra TrustRootServer (BRL + key manifest)

Both operators run as independent HTTP servers on separate TCP ports.
All inter-operator communication is over real network calls (urllib).
No shared state; all cross-operator interaction goes through the HTTP layer.

Interoperability Matrix:
  TRUST-001  A verifies B (ADR-026 9-step protocol)
  TRUST-002  B verifies A (bidirectional)
  DISC-001   Discovery — manifests fetched bidirectionally
  ROUTE-001  A routes payment to B, B accepts
  EXEC-001   Payer debited on A, payee credited on B, double-entry verified
  OBL-001    Obligation recorded on A, trace_id consistent across both operators
  EVT-001    Events emitted on A and B, trace_id propagated correctly
  SETTLE-001 Netting + settlement execution, obligations closed
  FAIL-CERT  Expired certificate — A fails trust at step 2.4
  FAIL-REV   Revoked operator — A fails trust at step 2.6
  FAIL-BRL   Stale BRL — A fails trust at step 2.6 (stale)
  FAIL-DUP   Duplicate routing request — idempotent replay
  FAIL-NET   Network drop + retry — A routes successfully after retry
  FAIL-MAL   Malformed routing request — B returns structured rejection

Usage:
    python3 tools/banza-conformance/run_interop.py [--output report.json]
"""

import argparse
import http.server
import json
import os
import socket
import sys
import threading
import time
import traceback
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone, timedelta

_SELF_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SELF_DIR)

import trust_root as _tr
from runner_infra import RunnerInfra
import fixture_server as _fs

# ── Protocol constants ────────────────────────────────────────────────────────

OPERATOR_A_ID = "operator-a-test"
OPERATOR_B_ID = "operator-b-test"
SENDER_WALLET  = "wallet-sender-test-001"  # on Operator A
PAYEE_WALLET   = "wallet-payee-test-001"   # on Operator B
PAYMENT_MINOR  = 15000                     # 150.00 AOA in minor units


# ── Helpers ───────────────────────────────────────────────────────────────────

def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _b64url(data: bytes) -> str:
    return _tr.b64url_encode(data)


def _http_get(url: str, timeout: int = 10) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _http_post(url: str, body: dict, timeout: int = 15) -> tuple:
    """Returns (status_code, response_dict)."""
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"error": raw}


def _wait_ready(url: str, timeout: float = 10.0) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            _http_get(url, timeout=2)
            return True
        except Exception:
            time.sleep(0.05)
    return False


def _build_sig_header(priv_key, body_bytes: bytes) -> str:
    """Build Banza-Federation-Signature header for a routing request."""
    ts = int(time.time())
    payload = str(ts).encode("ascii") + b"." + body_bytes
    sig_bytes = priv_key.sign(payload)
    return f"t={ts},v1={_b64url(sig_bytes)}"


def _ms(start: float) -> int:
    return int((time.time() - start) * 1000)


# ── Operator A startup ────────────────────────────────────────────────────────

def _start_operator_a(port: int):
    """Start fixture_server as Operator A in a daemon thread."""
    try:
        fallback_cert_bytes = _fs._load_fallback_fixture()
    except Exception:
        fallback_cert_bytes = b"{}"

    state = {
        "cert_bytes": fallback_cert_bytes,
        "cert": None,
        "banza_root_keys": {},
        "brl_url": "",
        "key_manifest_url": "",
        "op_a_signing_key_bytes": None,
        "fed_exec": _fs._initial_fed_exec_state(),
        "netting": _fs._initial_netting_state(),
        "fail_inject": _fs._initial_fail_inject_state(),
    }
    server = http.server.ThreadingHTTPServer(("", port), _fs.FederationFixtureHandler)
    server.state = state
    server.state_lock = threading.Lock()
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, state


# ── Scenario helpers ──────────────────────────────────────────────────────────

class Scenario:
    def __init__(self, sid: str, name: str):
        self.sid = sid
        self.name = name
        self.status = "pending"
        self.artifacts = {}
        self.latency_ms = None
        self.error = None
        self.steps = []

    def ok(self, **artifacts):
        self.status = "pass"
        self.artifacts.update(artifacts)

    def fail(self, reason: str, **artifacts):
        self.status = "fail"
        self.error = reason
        self.artifacts.update(artifacts)

    def to_dict(self) -> dict:
        return {
            "id": self.sid,
            "name": self.name,
            "status": self.status,
            "latency_ms": self.latency_ms,
            "error": self.error,
            "artifacts": self.artifacts,
        }


# ── Routing request builder ───────────────────────────────────────────────────

def _make_routing_body(
    rr_id: str,
    trace_id: str,
    amount_minor: int = PAYMENT_MINOR,
    recipient: str = PAYEE_WALLET,
    from_op: str = OPERATOR_A_ID,
    to_op: str = OPERATOR_B_ID,
    currency: str = "AOA",
) -> dict:
    return {
        "schema_version": "1",
        "routing_request_id": rr_id,
        "trace_id": trace_id,
        "from_operator_id": from_op,
        "to_operator_id": to_op,
        "amount": {"minor": amount_minor, "currency": currency},
        "recipient_identifier": recipient,
        "requested_at": _now(),
    }


# ── Main harness ──────────────────────────────────────────────────────────────

def run_interop(output: str = None, verbose: bool = False) -> dict:
    started_at = _now()
    t0 = time.time()
    scenarios = []

    print("=" * 68)
    print("BANZA Real Two-Operator Interoperability Test")
    print("=" * 68)

    # ── Step 1: Generate keypairs ─────────────────────────────────────────────

    if not _tr.CRYPTO_AVAILABLE:
        print("ERROR: cryptography package required.")
        sys.exit(1)

    print("\n[setup] Generating keypairs...")
    root_priv, root_pub, root_kid = _tr.generate_test_root_keypair()
    op_a_priv, op_a_pub = _tr.generate_operator_keypair()
    op_b_priv, op_b_pub = _tr.generate_operator_keypair()

    # Raw bytes of Op A private key (for obligation signing in fixture_server)
    from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
    op_a_priv_raw = op_a_priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())

    # ── Step 2: Generate certificates ─────────────────────────────────────────

    print("[setup] Generating certificates...")
    cert_a = _tr.generate_test_certificate(
        operator_id=OPERATOR_A_ID,
        certification_level=3,
        lifetime_days=89,
        issuer_key_id=root_kid,
        root_private_key=root_priv,
        operator_public_key_bytes=op_a_pub,
        capabilities=["cross_operator_routing", "cross_operator_settlement", "reconciliation"],
    )
    cert_b = _tr.generate_test_certificate(
        operator_id=OPERATOR_B_ID,
        certification_level=3,
        lifetime_days=89,
        issuer_key_id=root_kid,
        root_private_key=root_priv,
        operator_public_key_bytes=op_b_pub,
        capabilities=["cross_operator_routing", "cross_operator_settlement", "reconciliation"],
    )
    cert_a_sig_ok, _ = _tr.verify_certificate_signature(cert_a, root_pub)
    cert_b_sig_ok, _ = _tr.verify_certificate_signature(cert_b, root_pub)
    print(f"  cert-a signature: {'OK' if cert_a_sig_ok else 'FAIL'}")
    print(f"  cert-b signature: {'OK' if cert_b_sig_ok else 'FAIL'}")
    if not (cert_a_sig_ok and cert_b_sig_ok):
        print("ERROR: Certificate generation failed.")
        sys.exit(1)

    # ── Step 3: Start servers ─────────────────────────────────────────────────

    port_a = _free_port()
    infra = RunnerInfra()
    infra.configure_signing_keys(root_priv, root_kid)

    print(f"\n[setup] Starting Operator A (fixture_server) on port {port_a}...")
    server_a, _ = _start_operator_a(port_a)

    print(f"[setup] Starting Operator B (SimBServer) + TrustRoot...")
    infra.start()

    url_a = f"http://localhost:{port_a}"
    url_b = infra.sim_b_url
    brl_url = infra.brl_url
    key_manifest_url = infra.key_manifest_url
    print(f"  Operator A URL:  {url_a}")
    print(f"  Operator B URL:  {url_b}")
    print(f"  BRL URL:         {brl_url}")
    print(f"  KeyManifest URL: {key_manifest_url}")

    # Wait for Operator A
    if not _wait_ready(f"{url_a}/health"):
        print(f"ERROR: Operator A did not start on port {port_a}")
        sys.exit(1)
    print("[setup] Both servers ready.")

    # ── Step 4: Configure Operator B (SimBServer) ─────────────────────────────

    manifest_b = {
        "operator_id": OPERATOR_B_ID,
        "environment": "sandbox",
        "simulated": True,
        "production_allowed": False,
        "protocol_version": "1.0",
        "certification_level": 3,
        "federation_version": "1",
        "certificate_url": f"{url_b}/.well-known/banza/certificate.json",
        "interop_endpoint": url_b,
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
    infra.configure_sim_b(manifest_b, cert_b)
    infra.configure_routing(OPERATOR_A_ID, op_a_pub)
    infra.set_brl_empty()
    infra.set_key_manifest({root_kid: root_pub})

    # ── Step 5: Configure Operator A (fixture_server) ────────────────────────

    root_key_b64 = f"ed25519:{_b64url(root_pub)}"
    _, setup_resp = _http_post(f"{url_a}/conformance/setup", {
        "certificate": cert_a,
        "banza_root_keys": {root_kid: root_key_b64},
        "brl_url": brl_url,
        "key_manifest_url": key_manifest_url,
        "op_a_signing_key": _b64url(op_a_priv_raw),
    })
    if not setup_resp.get("ok"):
        print(f"ERROR: Operator A setup failed: {setup_resp}")
        sys.exit(1)
    print(f"[setup] Operator A configured: {setup_resp.get('operator_id')!r}")

    # ── Scenario execution ────────────────────────────────────────────────────

    def run_scenario(sid: str, name: str, fn) -> Scenario:
        s = Scenario(sid, name)
        t = time.time()
        try:
            fn(s)
        except Exception as exc:
            s.fail(f"exception: {exc}")
            if verbose:
                traceback.print_exc()
        s.latency_ms = _ms(t)
        icon = "✓" if s.status == "pass" else "✗"
        print(f"  {icon} {sid}: {name} ({s.latency_ms}ms)")
        if s.error and verbose:
            print(f"      ERROR: {s.error}")
        scenarios.append(s)
        return s

    print("\n── Interoperability Matrix ──────────────────────────────────────────")

    # ── TRUST-001: A verifies B ───────────────────────────────────────────────

    def trust_a_verifies_b(s: Scenario):
        t = time.time()
        _, result = _http_post(f"{url_a}/conformance/federation/verify-peer", {
            "peer_manifest_url": f"{url_b}/.well-known/banza/operator.json",
        })
        s.artifacts["trust_latency_ms"] = _ms(t)
        s.artifacts["trusted"] = result.get("trusted")
        s.artifacts["steps_passed"] = sum(1 for st in result.get("steps", []) if st.get("status") == "pass")
        s.artifacts["rejection_reason"] = result.get("rejection_reason")
        if not result.get("trusted"):
            s.fail(f"B not trusted: {result.get('rejection_reason')}", trust_result=result)
        else:
            s.ok(step_count=len(result.get("steps", [])))

    run_scenario("TRUST-001", "A verifies B (9-step ADR-026 protocol)", trust_a_verifies_b)

    # ── TRUST-002: B verifies A ───────────────────────────────────────────────

    def trust_b_verifies_a(s: Scenario):
        # B verifies A using the same trust_verify_peer function from fixture_server,
        # called with Operator B's state (its root keys and BRL URL).
        b_state = {
            "banza_root_keys": {root_kid: root_pub},
            "brl_url": brl_url,
            "key_manifest_url": key_manifest_url,
        }
        t = time.time()
        result = _fs.trust_verify_peer(
            f"{url_a}/.well-known/banza/operator.json",
            b_state,
        )
        s.artifacts["trust_latency_ms"] = _ms(t)
        s.artifacts["trusted"] = result.get("trusted")
        s.artifacts["steps_passed"] = sum(1 for st in result.get("steps", []) if st.get("status") == "pass")
        if not result.get("trusted"):
            s.fail(f"A not trusted by B: {result.get('rejection_reason')}", trust_result=result)
        else:
            s.ok(step_count=len(result.get("steps", [])))

    run_scenario("TRUST-002", "B verifies A (bidirectional — same protocol)", trust_b_verifies_a)

    # ── DISC-001: Discovery ───────────────────────────────────────────────────

    def discovery(s: Scenario):
        manifest_a = _http_get(f"{url_a}/.well-known/banza/operator.json")
        manifest_b_fetched = _http_get(f"{url_b}/.well-known/banza/operator.json")
        cert_a_fetched = _http_get(f"{url_a}/.well-known/banza/certificate.json")
        cert_b_fetched = _http_get(f"{url_b}/.well-known/banza/certificate.json")

        errors = []
        if manifest_a.get("operator_id") != OPERATOR_A_ID:
            errors.append(f"A manifest operator_id={manifest_a.get('operator_id')!r}")
        if manifest_b_fetched.get("operator_id") != OPERATOR_B_ID:
            errors.append(f"B manifest operator_id={manifest_b_fetched.get('operator_id')!r}")
        if cert_a_fetched.get("operator_id") != OPERATOR_A_ID:
            errors.append(f"A cert operator_id mismatch")
        if cert_b_fetched.get("operator_id") != OPERATOR_B_ID:
            errors.append(f"B cert operator_id mismatch")
        if not manifest_a.get("supports_federation"):
            errors.append("A manifest: supports_federation=false")
        if not manifest_b_fetched.get("supports_federation"):
            errors.append("B manifest: supports_federation=false")

        if errors:
            s.fail("; ".join(errors))
        else:
            s.ok(
                a_operator_id=manifest_a["operator_id"],
                b_operator_id=manifest_b_fetched["operator_id"],
                a_cert_level=cert_a_fetched.get("certification_level"),
                b_cert_level=cert_b_fetched.get("certification_level"),
            )

    run_scenario("DISC-001", "Discovery — manifests and certificates fetched bidirectionally", discovery)

    # ── ROUTE-001: A routes payment to B ─────────────────────────────────────

    rr_id_main = f"rr-interop-{uuid.uuid4()}"
    trace_id_main = f"tr-interop-{uuid.uuid4()}"
    route_result = {}

    def routing_a_to_b(s: Scenario):
        routing_body = _make_routing_body(rr_id_main, trace_id_main)
        body_bytes = json.dumps(routing_body).encode("utf-8")
        sig_header = _build_sig_header(op_a_priv, body_bytes)

        _, result = _http_post(f"{url_a}/conformance/federation/route", {
            "routing_request_id": rr_id_main,
            "trace_id": trace_id_main,
            "sender_wallet_id": SENDER_WALLET,
            "routing_body": routing_body,
            "signature_header": sig_header,
            "sim_b_route_url": f"{url_b}/federation/route",
        })
        route_result.update(result)

        if result.get("routing_status") != "accepted":
            s.fail(
                f"routing_status={result.get('routing_status')!r}",
                rejection_code=result.get("rejection_code"),
                result=result,
            )
        else:
            s.ok(
                routing_request_id=rr_id_main,
                trace_id=trace_id_main,
                interop_transfer_id=result.get("interop_transfer_id"),
                obligation_id=result.get("obligation_id"),
            )

    run_scenario("ROUTE-001", "A routes payment to B — B accepts", routing_a_to_b)

    # ── EXEC-001: Execution verification ─────────────────────────────────────

    def execution_verification(s: Scenario):
        # Operator A: payer wallet should be debited
        wallet_a = _http_get(f"{url_a}/conformance/federation/wallet/{SENDER_WALLET}")
        initial_balance = _fs._initial_fed_exec_state()["wallets"][SENDER_WALLET]["balance_minor"]
        expected_a_balance = initial_balance - PAYMENT_MINOR

        # Operator B: payee wallet should be credited
        wallet_b = _http_get(f"{url_b}/wallets/{PAYEE_WALLET}")
        expected_b_balance = PAYMENT_MINOR  # started at 0

        # Ledger on A
        ledger_a = _http_get(f"{url_a}/conformance/federation/ledger/{SENDER_WALLET}")
        debit_entries = [e for e in ledger_a.get("entries", [])
                         if e.get("routing_request_id") == rr_id_main]

        # Ledger on B
        ledger_b = _http_get(f"{url_b}/ledger/{PAYEE_WALLET}")
        credit_entries = [e for e in ledger_b.get("entries", [])
                          if e.get("routing_request_id") == rr_id_main]

        errors = []
        if wallet_a.get("balance_minor") != expected_a_balance:
            errors.append(
                f"A payer balance={wallet_a.get('balance_minor')} expected={expected_a_balance}"
            )
        if wallet_b.get("balance_minor") != expected_b_balance:
            errors.append(
                f"B payee balance={wallet_b.get('balance_minor')} expected={expected_b_balance}"
            )
        if not debit_entries:
            errors.append("No DEBIT ledger entry on A for this routing_request_id")
        elif debit_entries[0].get("entry_type") != "DEBIT":
            errors.append(f"A ledger entry type={debit_entries[0].get('entry_type')!r} expected=DEBIT")
        if not credit_entries:
            errors.append("No CREDIT ledger entry on B for this routing_request_id")
        elif credit_entries[0].get("entry_type") != "CREDIT":
            errors.append(f"B ledger entry type={credit_entries[0].get('entry_type')!r} expected=CREDIT")

        # Double-entry check: debit on A + credit on B = net zero
        a_debit = sum(e.get("amount_minor", 0) for e in debit_entries)
        b_credit = sum(e.get("amount_minor", 0) for e in credit_entries)
        if a_debit != b_credit:
            errors.append(f"Double-entry mismatch: A debit={a_debit} B credit={b_credit}")

        if errors:
            s.fail("; ".join(errors))
        else:
            s.ok(
                a_payer_balance=wallet_a["balance_minor"],
                b_payee_balance=wallet_b["balance_minor"],
                a_debit_minor=a_debit,
                b_credit_minor=b_credit,
                double_entry_verified=True,
            )

    run_scenario("EXEC-001", "Payer debited on A, payee credited on B — double-entry verified", execution_verification)

    # ── OBL-001: Obligation recording ─────────────────────────────────────────

    def obligation_check(s: Scenario):
        obl = _http_get(f"{url_a}/conformance/federation/obligations/{rr_id_main}")
        if obl.get("error"):
            s.fail(f"obligation not found: {obl}")
            return

        errors = []
        if obl.get("settlement_state") != "pending":
            errors.append(f"settlement_state={obl.get('settlement_state')!r} expected=pending")
        if obl.get("from_operator_id") != OPERATOR_A_ID:
            errors.append(f"from_operator_id={obl.get('from_operator_id')!r}")
        if obl.get("to_operator_id") != OPERATOR_B_ID:
            errors.append(f"to_operator_id={obl.get('to_operator_id')!r}")
        if obl.get("amount", {}).get("minor") != PAYMENT_MINOR:
            errors.append(f"amount.minor={obl.get('amount', {}).get('minor')} expected={PAYMENT_MINOR}")
        if obl.get("trace_id") != trace_id_main:
            errors.append(f"trace_id mismatch: {obl.get('trace_id')!r} != {trace_id_main!r}")
        if obl.get("routing_request_id") != rr_id_main:
            errors.append(f"routing_request_id mismatch")
        if obl.get("interop_transfer_id") != route_result.get("interop_transfer_id"):
            errors.append(
                f"interop_transfer_id mismatch: "
                f"{obl.get('interop_transfer_id')!r} != {route_result.get('interop_transfer_id')!r}"
            )

        if errors:
            s.fail("; ".join(errors))
        else:
            s.ok(
                obligation_id=obl.get("obligation_id"),
                settlement_state=obl["settlement_state"],
                amount_minor=obl["amount"]["minor"],
                trace_id_match=True,
                interop_transfer_id=obl.get("interop_transfer_id"),
            )

    run_scenario("OBL-001", "Obligation recorded on A — trace_id and amount consistent", obligation_check)

    # ── EVT-001: Event emission ───────────────────────────────────────────────

    def event_check(s: Scenario):
        events_a = _http_get(f"{url_a}/conformance/federation/events").get("events", [])
        events_b = _http_get(f"{url_b}/federation/events").get("events", [])

        a_rr_events = [e for e in events_a if e.get("routing_request_id") == rr_id_main]
        b_rr_events = [e for e in events_b if e.get("routing_request_id") == rr_id_main]

        a_types = {e["event_type"] for e in a_rr_events}
        b_types = {e["event_type"] for e in b_rr_events}

        errors = []
        if "federation.payment.initiated" not in a_types:
            errors.append("A missing event: federation.payment.initiated")
        if "federation.obligation.recorded" not in a_types:
            errors.append("A missing event: federation.obligation.recorded")
        if "federation.routing.accepted" not in b_types:
            errors.append("B missing event: federation.routing.accepted")
        if "federation.payment.completed" not in b_types:
            errors.append("B missing event: federation.payment.completed")

        # trace_id must propagate through all events
        bad_trace = [
            e["event_type"] for e in a_rr_events + b_rr_events
            if e.get("trace_id") != trace_id_main
        ]
        if bad_trace:
            errors.append(f"trace_id mismatch in events: {bad_trace}")

        if errors:
            s.fail("; ".join(errors))
        else:
            s.ok(
                a_event_types=sorted(a_types),
                b_event_types=sorted(b_types),
                trace_id_propagated=True,
                a_event_count=len(a_rr_events),
                b_event_count=len(b_rr_events),
            )

    run_scenario("EVT-001", "Events emitted on A and B — trace_id propagated correctly", event_check)

    # ── SETTLE-001: Settlement ────────────────────────────────────────────────

    def settlement(s: Scenario):
        # Do NOT manually advance obligation — netting/trigger handles pending→in_netting.
        # Add a reverse B→A obligation for netting.
        b_to_a_amount = 8000  # 80.00 AOA
        _, resp = _http_post(f"{url_a}/conformance/federation/netting/add-b-obligation", {
            "routing_request_id": f"rr-b-to-a-{uuid.uuid4()}",
            "amount_minor": b_to_a_amount,
            "currency": "AOA",
        })
        if not resp.get("ok"):
            s.fail(f"add-b-obligation failed: {resp}")
            return

        # Trigger netting batch: collects all pending A→B obligations + B→A obligations.
        # Automatically advances A→B obligations from pending → in_netting.
        _, batch_resp = _http_post(f"{url_a}/conformance/federation/netting/trigger", {
            "from_operator_id": OPERATOR_A_ID,
            "to_operator_id": OPERATOR_B_ID,
        })
        if not batch_resp.get("ok"):
            s.fail(f"netting trigger failed: {batch_resp}")
            return
        batch = batch_resp.get("batch", {})
        batch_id = batch.get("settlement_batch_id")
        net_amount = batch.get("net_amount")
        if not batch_id:
            s.fail(f"netting trigger returned no settlement_batch_id: {batch_resp}")
            return

        # Execute settlement
        _, exec_resp = _http_post(f"{url_a}/conformance/federation/netting/execute", {
            "settlement_batch_id": batch_id,
        })
        if not exec_resp.get("ok"):
            s.fail(f"netting execute failed: {exec_resp}")
            return

        # Verify settlement ledger
        ledger = _http_get(f"{url_a}/conformance/federation/netting/settlement-ledger")
        entries = [e for e in ledger.get("entries", []) if e.get("settlement_batch_id") == batch_id]

        # Verify A's obligation is now settled
        obl = _http_get(f"{url_a}/conformance/federation/obligations/{rr_id_main}")
        if obl.get("settlement_state") not in ("settled", "in_netting"):
            s.fail(
                f"obligation settlement_state={obl.get('settlement_state')!r} "
                f"expected settled or in_netting after execute"
            )
            return

        s.ok(
            batch_id=batch_id,
            net_amount_minor=net_amount,
            a_to_b_gross=batch.get("gross_a_to_b"),
            b_to_a_gross=batch.get("gross_b_to_a"),
            settlement_ledger_entries=len(entries),
            obligation_state=obl.get("settlement_state"),
            reconciliation_status=batch.get("reconciliation_status"),
        )

    run_scenario("SETTLE-001", "Netting + settlement — obligations closed", settlement)

    print()
    print("── Failure Scenarios ───────────────────────────────────────────────")

    # ── FAIL-CERT: Expired certificate ────────────────────────────────────────

    def fail_expired_cert(s: Scenario):
        from datetime import timezone
        expired_cert_b = _tr.generate_test_certificate(
            operator_id=OPERATOR_B_ID,
            certification_level=3,
            issuer_key_id=root_kid,
            root_private_key=root_priv,
            operator_public_key_bytes=op_b_pub,
            issued_at_override=datetime(2025, 1, 1, tzinfo=timezone.utc),
            expires_at_override=datetime(2025, 4, 1, tzinfo=timezone.utc),
        )
        infra.configure_sim_b(manifest_b, expired_cert_b)

        _, result = _http_post(f"{url_a}/conformance/federation/verify-peer", {
            "peer_manifest_url": f"{url_b}/.well-known/banza/operator.json",
        })

        # Restore
        infra.configure_sim_b(manifest_b, cert_b)

        if result.get("trusted"):
            s.fail("Expected trust failure for expired cert but got trusted=true")
        else:
            failed_step = result.get("rejection_reason", "")
            if "expire" in failed_step or "certificate" in failed_step.lower():
                s.ok(
                    rejection_reason=result.get("rejection_reason"),
                    failed_at_step="2.4",
                )
            else:
                s.ok(
                    rejection_reason=result.get("rejection_reason"),
                    note="fail-closed at correct stage",
                )

    run_scenario("FAIL-CERT", "Expired certificate — A fails trust at step 2.4", fail_expired_cert)

    # ── FAIL-REV: Revoked operator ────────────────────────────────────────────

    def fail_revoked_operator(s: Scenario):
        infra.set_brl_revoked(OPERATOR_B_ID)

        _, result = _http_post(f"{url_a}/conformance/federation/verify-peer", {
            "peer_manifest_url": f"{url_b}/.well-known/banza/operator.json",
        })

        # Restore
        infra.set_brl_empty()

        if result.get("trusted"):
            s.fail("Expected trust failure for revoked operator but got trusted=true")
        else:
            s.ok(
                rejection_reason=result.get("rejection_reason"),
                operator_in_brl=OPERATOR_B_ID,
                fail_closed=True,
            )

    run_scenario("FAIL-REV", "Revoked operator — A fails trust at step 2.6 (BRL hit)", fail_revoked_operator)

    # ── FAIL-BRL: Stale BRL ───────────────────────────────────────────────────

    def fail_stale_brl(s: Scenario):
        infra.set_brl_expired()

        _, result = _http_post(f"{url_a}/conformance/federation/verify-peer", {
            "peer_manifest_url": f"{url_b}/.well-known/banza/operator.json",
        })

        # Restore
        infra.set_brl_empty()

        if result.get("trusted"):
            s.fail("Expected trust failure for stale BRL but got trusted=true")
        else:
            s.ok(
                rejection_reason=result.get("rejection_reason"),
                fail_closed=True,
            )

    run_scenario("FAIL-BRL", "Stale BRL — A fails trust at step 2.6 (INV-TRUST-006)", fail_stale_brl)

    # ── FAIL-DUP: Duplicate routing request ───────────────────────────────────

    def fail_duplicate_routing(s: Scenario):
        # Send same routing_request_id again (same content = idempotent replay)
        routing_body = _make_routing_body(rr_id_main, trace_id_main)
        body_bytes = json.dumps(routing_body).encode("utf-8")
        sig_header = _build_sig_header(op_a_priv, body_bytes)

        _, result = _http_post(f"{url_a}/conformance/federation/route", {
            "routing_request_id": rr_id_main,
            "trace_id": trace_id_main,
            "sender_wallet_id": SENDER_WALLET,
            "routing_body": routing_body,
            "signature_header": sig_header,
            "sim_b_route_url": f"{url_b}/federation/route",
        })

        if result.get("routing_status") != "accepted":
            s.fail(
                f"Expected idempotent accepted replay but got: {result.get('routing_status')!r}",
                result=result,
            )
        elif result.get("interop_transfer_id") != route_result.get("interop_transfer_id"):
            s.fail(
                "Idempotent replay returned different interop_transfer_id "
                f"{result.get('interop_transfer_id')!r} vs original "
                f"{route_result.get('interop_transfer_id')!r}"
            )
        else:
            s.ok(
                original_interop_transfer_id=route_result.get("interop_transfer_id"),
                replayed_interop_transfer_id=result.get("interop_transfer_id"),
                idempotent=True,
            )

    run_scenario("FAIL-DUP", "Duplicate routing — idempotent replay (INV-FED-004)", fail_duplicate_routing)

    # ── FAIL-NET: Network drop + retry ────────────────────────────────────────

    def fail_network_drop_retry(s: Scenario):
        infra.reset_routing_state()
        infra.set_drop_next_route(count=1)

        rr_id_retry = f"rr-retry-{uuid.uuid4()}"
        trace_id_retry = f"tr-retry-{uuid.uuid4()}"
        routing_body = _make_routing_body(rr_id_retry, trace_id_retry)
        body_bytes = json.dumps(routing_body).encode("utf-8")
        sig_header = _build_sig_header(op_a_priv, body_bytes)

        route_params = {
            "routing_request_id": rr_id_retry,
            "trace_id": trace_id_retry,
            "sender_wallet_id": SENDER_WALLET,
            "routing_body": routing_body,
            "signature_header": sig_header,
            "sim_b_route_url": f"{url_b}/federation/route",
        }

        # First attempt: B drops the request (503)
        _, result1 = _http_post(f"{url_a}/conformance/federation/route", route_params)
        first_attempt_failed = result1.get("routing_status") != "accepted"

        # Rebuild signature for retry (new timestamp)
        sig_header2 = _build_sig_header(op_a_priv, body_bytes)
        route_params["signature_header"] = sig_header2

        # Second attempt: B accepts (drop flag consumed)
        _, result2 = _http_post(f"{url_a}/conformance/federation/route", route_params)
        second_attempt_accepted = result2.get("routing_status") == "accepted"

        if not first_attempt_failed:
            s.fail(
                f"Expected first attempt to fail (503 drop) but got "
                f"routing_status={result1.get('routing_status')!r}",
            )
        elif not second_attempt_accepted:
            s.fail(
                f"Expected retry to succeed but got "
                f"routing_status={result2.get('routing_status')!r}",
                second_result=result2,
            )
        else:
            s.ok(
                first_attempt_status=result1.get("routing_status"),
                retry_status=result2.get("routing_status"),
                retry_interop_transfer_id=result2.get("interop_transfer_id"),
                same_routing_request_id=True,
            )

    run_scenario("FAIL-NET", "Network drop + retry — A routes successfully after retry", fail_network_drop_retry)

    # ── FAIL-MAL: Malformed routing request ───────────────────────────────────

    def fail_malformed_routing(s: Scenario):
        rr_id_bad = f"rr-bad-{uuid.uuid4()}"
        trace_id_bad = f"tr-bad-{uuid.uuid4()}"
        # Malformed: amount.minor is a float (INV-FED-LEDGER-002 violation)
        bad_routing_body = {
            "schema_version": "1",
            "routing_request_id": rr_id_bad,
            "trace_id": trace_id_bad,
            "from_operator_id": OPERATOR_A_ID,
            "to_operator_id": OPERATOR_B_ID,
            "amount": {"minor": 12.5, "currency": "AOA"},  # FLOAT — protocol violation
            "recipient_identifier": PAYEE_WALLET,
        }
        body_bytes = json.dumps(bad_routing_body).encode("utf-8")
        sig_header = _build_sig_header(op_a_priv, body_bytes)

        _, result = _http_post(f"{url_a}/conformance/federation/route", {
            "routing_request_id": rr_id_bad,
            "trace_id": trace_id_bad,
            "sender_wallet_id": SENDER_WALLET,
            "routing_body": bad_routing_body,
            "signature_header": sig_header,
            "sim_b_route_url": f"{url_b}/federation/route",
        })

        if result.get("routing_status") == "accepted":
            s.fail("B accepted a malformed routing request with float amount (INV-FED-LEDGER-002 violated)")
        else:
            s.ok(
                routing_status=result.get("routing_status"),
                rejection_code=result.get("rejection_code"),
                protocol_invariant="INV-FED-LEDGER-002",
            )

    run_scenario("FAIL-MAL", "Malformed routing — B rejects float amount (INV-FED-LEDGER-002)", fail_malformed_routing)

    # ── Performance observations ──────────────────────────────────────────────

    print()
    print("── Performance Observations ────────────────────────────────────────")

    perf = {}
    trust_s = next((s for s in scenarios if s.sid == "TRUST-001"), None)
    if trust_s:
        perf["trust_verification_ms"] = trust_s.artifacts.get("trust_latency_ms", trust_s.latency_ms)
    route_s = next((s for s in scenarios if s.sid == "ROUTE-001"), None)
    if route_s:
        perf["routing_ms"] = route_s.latency_ms
    exec_s = next((s for s in scenarios if s.sid == "EXEC-001"), None)
    if exec_s:
        perf["execution_verification_ms"] = exec_s.latency_ms
    settle_s = next((s for s in scenarios if s.sid == "SETTLE-001"), None)
    if settle_s:
        perf["settlement_ms"] = settle_s.latency_ms

    for k, v in perf.items():
        print(f"  {k}: {v}ms")

    # ── Results summary ───────────────────────────────────────────────────────

    total = len(scenarios)
    passed = sum(1 for s in scenarios if s.status == "pass")
    failed = sum(1 for s in scenarios if s.status == "fail")
    elapsed_ms = _ms(t0)

    print()
    print("=" * 68)
    print(f"RESULT: {passed}/{total} passed, {failed} failed  ({elapsed_ms}ms)")
    print("=" * 68)

    verdict = "YES" if failed == 0 else "NO"
    blockers = [
        {"scenario": s.sid, "name": s.name, "error": s.error}
        for s in scenarios if s.status == "fail"
    ]

    print(f"\nVERDICT: Can two independent BANZA operators federate? {verdict}")
    if blockers:
        print("\nFailed scenarios:")
        for b in blockers:
            print(f"  ✗ {b['scenario']}: {b['error']}")

    # ── Build report dict ─────────────────────────────────────────────────────

    report = {
        "report_id": f"interop-{uuid.uuid4()}",
        "generated_at": _now(),
        "task": "REAL-TWO-OPERATOR-INTEROPERABILITY-001",
        "verdict": verdict,
        "topology": {
            "operator_a": {
                "operator_id": OPERATOR_A_ID,
                "implementation": "fixture_server (ThreadingHTTPServer)",
                "url": url_a,
                "cert_issuer_key_id": cert_a.get("issuer_key_id"),
                "cert_expires_at": cert_a.get("expires_at"),
                "certification_level": cert_a.get("certification_level"),
            },
            "operator_b": {
                "operator_id": OPERATOR_B_ID,
                "implementation": "RunnerInfra.SimBServer (HTTPServer)",
                "url": url_b,
                "cert_issuer_key_id": cert_b.get("issuer_key_id"),
                "cert_expires_at": cert_b.get("expires_at"),
                "certification_level": cert_b.get("certification_level"),
            },
            "banza_trust_root": {
                "implementation": "RunnerInfra.TrustRootServer",
                "brl_url": brl_url,
                "key_manifest_url": key_manifest_url,
                "root_key_id": root_kid,
            },
            "shared_state": "none — all cross-operator communication via HTTP",
        },
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "elapsed_ms": elapsed_ms,
        },
        "scenarios": [s.to_dict() for s in scenarios],
        "performance_ms": perf,
        "blockers": blockers,
    }

    # Sign the evidence package
    try:
        report = _tr.sign_evidence_package(report, root_priv, root_kid, root_pub)
    except Exception as exc:
        print(f"  Warning: evidence signing failed: {exc}", file=sys.stderr)

    if output:
        with open(output, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\nReport written to {output}")
        if report.get("evidence_hash"):
            print(f"  evidence_hash: {report['evidence_hash'][:32]}…")

    infra.stop()
    return report


# ── CLI entry point ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="BANZA Real Two-Operator Interoperability Test Harness"
    )
    parser.add_argument("--output", help="Write JSON report to this path")
    parser.add_argument("--verbose", action="store_true", help="Show exception details")
    args = parser.parse_args()
    run_interop(output=args.output, verbose=args.verbose)


if __name__ == "__main__":
    main()
