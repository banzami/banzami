"""
BANZA Federation Runner Infrastructure

Two embedded HTTP servers used exclusively by the conformance runner:

  SimBServer      — Simulated Operator B
      GET  /.well-known/banza/operator.json     configurable manifest
      GET  /.well-known/banza/certificate.json  configurable cert
      POST /federation/route                    routing wire protocol (FED-ROUTE)
      GET  /wallets/{wallet_id}                 wallet balance queries

  TrustRootServer — BANZA trust root endpoints
      GET /federation/revocation-list.json     configurable BRL
      GET /federation/public-keys.json         configurable key manifest

State is updated by the runner between tests using RunnerInfra methods.
Both servers are thread-safe; each is started in its own daemon thread.
"""

import base64
import hashlib
import http.server
import json
import socket
import threading
import uuid
from datetime import datetime, timedelta, timezone

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.exceptions import InvalidSignature
    _SIM_B_CRYPTO = True
except ImportError:
    _SIM_B_CRYPTO = False

# ── Module-level helpers ──────────────────────────────────────────────────────

def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def _b64url_decode(s: str) -> bytes:
    pad = (4 - len(s) % 4) % 4
    return base64.urlsafe_b64decode(s + "=" * pad)


def _parse_sig_header(header: str):
    """Parse Banza-Federation-Signature: t=<int>,v1=<base64url>. Returns (t_int, sig_b64) or (None, None)."""
    t_val = None
    sig_b64 = None
    for part in header.split(","):
        part = part.strip()
        if part.startswith("t="):
            try:
                t_val = int(part[2:])
            except ValueError:
                pass
        elif part.startswith("v1="):
            sig_b64 = part[3:]
    return t_val, sig_b64


def _canonical_body_hash(body_bytes: bytes) -> str:
    """Canonical hash for idempotency: parse JSON, sort keys, re-serialize, then SHA-256."""
    try:
        parsed = json.loads(body_bytes)
        canonical = json.dumps(parsed, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except Exception:
        canonical = body_bytes
    return hashlib.sha256(canonical).hexdigest()


# ── Simulated Operator B ──────────────────────────────────────────────────────

def _make_sim_b_handler(state: dict, lock: threading.Lock):
    class SimBHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass  # suppress per-request logs

        # ── Response helper ───────────────────────────────────────────────────

        def _json(self, status: int, body: dict) -> None:
            data = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        # ── GET ───────────────────────────────────────────────────────────────

        def do_GET(self):
            if self.path == "/.well-known/banza/operator.json":
                with lock:
                    body = json.dumps(state["manifest"], indent=2).encode("utf-8") \
                        if state["manifest"] else b'{"error":"not configured"}'
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            elif self.path == "/.well-known/banza/certificate.json":
                with lock:
                    body = json.dumps(state["cert"], indent=2).encode("utf-8") \
                        if state["cert"] else b'{"error":"not configured"}'
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            elif self.path.startswith("/wallets/"):
                wallet_id = self.path[len("/wallets/"):]
                with lock:
                    wallet = state["wallets"].get(wallet_id)
                if wallet is None:
                    self._json(404, {"error": "not_found", "wallet_id": wallet_id})
                else:
                    self._json(200, {
                        "wallet_id": wallet_id,
                        "status": wallet["status"],
                        "balance_minor": wallet["balance_minor"],
                    })

            elif self.path == "/federation/events":
                # FED-EXEC-007: federation events emitted by Sim Op B
                with lock:
                    events = list(state["events"])
                self._json(200, {"events": events})

            elif self.path.startswith("/ledger/"):
                # FED-EXEC-002: payee ledger entries on Sim Op B
                wallet_id = self.path[len("/ledger/"):]
                with lock:
                    entries = [e for e in state["ledger"] if e.get("wallet_id") == wallet_id]
                self._json(200, {"wallet_id": wallet_id, "entries": entries})

            else:
                self._json(404, {"error": "not_found", "path": self.path})

        # ── POST ──────────────────────────────────────────────────────────────

        def do_POST(self):
            if self.path == "/federation/route":
                self._handle_route()
            else:
                self._json(404, {"error": "not_found", "path": self.path})

        def _handle_route(self):
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)

            # Parse body first — needed for all responses
            try:
                req = json.loads(body_bytes)
                if not isinstance(req, dict):
                    raise ValueError("body is not a JSON object")
            except Exception:
                self._json(400, {"error": "invalid_json"})
                return

            routing_id = req.get("routing_request_id", "")
            trace_id = req.get("trace_id", "")

            # ── Failure injection (FED-FAIL suite) ───────────────────────────
            with lock:
                drop_count = state.get("drop_next_route_count", 0)
                malformed = state.get("malformed_response_once", False)
                trust_fail = state.get("trust_failure_override_once", False)

            if drop_count > 0:
                with lock:
                    state["drop_next_route_count"] = max(0, drop_count - 1)
                self._json(503, {
                    "error": "service_unavailable",
                    "routing_request_id": routing_id,
                })
                return

            if malformed:
                with lock:
                    state["malformed_response_once"] = False
                raw_bad = b"this is not valid json <<<malformed_response>>>"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(raw_bad)))
                self.end_headers()
                self.wfile.write(raw_bad)
                return

            if trust_fail:
                with lock:
                    state["trust_failure_override_once"] = False
                now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                self._json(200, {
                    "schema_version": "1",
                    "routing_request_id": routing_id,
                    "status": "rejected",
                    "trace_id": trace_id,
                    "rejection_code": "operator_trust_failure",
                    "rejection_reason": "Operator A certificate trust verification failed (FED-FAIL-004)",
                })
                return
            # ─────────────────────────────────────────────────────────────────

            # Read shared state once
            with lock:
                manifest = state.get("manifest") or {}
                my_op_id = manifest.get("operator_id", "operator-b-test")
                fc = manifest.get("federation_capabilities") or {}
                supported_currencies = fc.get("supported_currencies", ["AOA"])
                op_a_pub_key = state.get("op_a_public_key")
                routing_store = state["routing_store"]
                wallets = state["wallets"]

            # 1. Validate to_operator_id
            to_op_id = req.get("to_operator_id", "")
            if to_op_id != my_op_id:
                self._json(400, {
                    "schema_version": "1",
                    "routing_request_id": routing_id,
                    "status": "rejected",
                    "trace_id": trace_id,
                    "rejection_code": "capability_unavailable",
                    "rejection_reason": (
                        f"to_operator_id {to_op_id!r} does not match this operator ({my_op_id!r})"
                    ),
                })
                return

            # 2. Verify Banza-Federation-Signature
            sig_header = self.headers.get("Banza-Federation-Signature", "")
            if not sig_header:
                self._json(401, {
                    "schema_version": "1",
                    "routing_request_id": routing_id,
                    "status": "rejected",
                    "trace_id": trace_id,
                    "rejection_code": "operator_trust_failure",
                    "rejection_reason": "Missing Banza-Federation-Signature header",
                })
                return

            t_val, sig_b64 = _parse_sig_header(sig_header)
            sig_valid = False
            if t_val is not None and sig_b64 and op_a_pub_key and _SIM_B_CRYPTO:
                try:
                    payload = (str(t_val) + ".").encode("ascii") + body_bytes
                    sig_bytes = _b64url_decode(sig_b64)
                    pub = Ed25519PublicKey.from_public_bytes(op_a_pub_key)
                    pub.verify(sig_bytes, payload)
                    sig_valid = True
                except (InvalidSignature, Exception):
                    sig_valid = False

            if not sig_valid:
                self._json(401, {
                    "schema_version": "1",
                    "routing_request_id": routing_id,
                    "status": "rejected",
                    "trace_id": trace_id,
                    "rejection_code": "operator_trust_failure",
                    "rejection_reason": "Signature verification failed",
                })
                return

            # 3. Validate amount.minor > 0 (INV-FED-LEDGER-002)
            amount = req.get("amount") or {}
            amount_minor = amount.get("minor", 0)
            if not isinstance(amount_minor, int) or isinstance(amount_minor, bool) or amount_minor <= 0:
                self._json(400, {
                    "schema_version": "1",
                    "routing_request_id": routing_id,
                    "status": "rejected",
                    "trace_id": trace_id,
                    "rejection_code": "amount_below_minimum",
                    "rejection_reason": "amount.minor must be a positive integer",
                })
                return

            # 4. Idempotency check (INV-FED-004)
            body_hash = _canonical_body_hash(body_bytes)
            with lock:
                if routing_id in state["routing_store"]:
                    stored = state["routing_store"][routing_id]
                    if stored["body_hash"] != body_hash:
                        dup_resp = {
                            "schema_version": "1",
                            "routing_request_id": routing_id,
                            "status": "rejected",
                            "trace_id": trace_id,
                            "rejection_code": "duplicate_request",
                            "rejection_reason": (
                                "routing_request_id already processed with different content"
                            ),
                        }
                        self._json(200, dup_resp)
                        return
                    else:
                        # Same content → replay original response
                        self._json(200, stored["response"])
                        return

            # 5. Validate currency
            currency = amount.get("currency", "")
            if currency not in supported_currencies:
                resp = {
                    "schema_version": "1",
                    "routing_request_id": routing_id,
                    "status": "rejected",
                    "trace_id": trace_id,
                    "rejection_code": "currency_not_supported",
                    "rejection_reason": (
                        f"Currency {currency!r} is not supported. "
                        f"Supported: {supported_currencies}"
                    ),
                }
                with lock:
                    state["routing_store"][routing_id] = {"body_hash": body_hash, "response": resp}
                self._json(200, resp)
                return

            # 6. Validate recipient
            recipient_id = req.get("recipient_identifier", "")
            with lock:
                wallet = state["wallets"].get(recipient_id)

            if wallet is None:
                resp = {
                    "schema_version": "1",
                    "routing_request_id": routing_id,
                    "status": "rejected",
                    "trace_id": trace_id,
                    "rejection_code": "recipient_not_found",
                    "rejection_reason": f"No wallet matching identifier {recipient_id!r}",
                }
                with lock:
                    state["routing_store"][routing_id] = {"body_hash": body_hash, "response": resp}
                self._json(200, resp)
                return

            if wallet["status"] == "suspended":
                resp = {
                    "schema_version": "1",
                    "routing_request_id": routing_id,
                    "status": "rejected",
                    "trace_id": trace_id,
                    "rejection_code": "recipient_suspended",
                    "rejection_reason": f"Wallet {recipient_id!r} is suspended",
                }
                with lock:
                    state["routing_store"][routing_id] = {"body_hash": body_hash, "response": resp}
                self._json(200, resp)
                return

            # 7. Accept — credit payee, assign interop_transfer_id
            itx_id = f"itx-{uuid.uuid4()}"
            now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            resp = {
                "schema_version": "1",
                "routing_request_id": routing_id,
                "status": "accepted",
                "trace_id": trace_id,
                "interop_transfer_id": itx_id,
                "accepted_at": now_str,
            }
            currency = amount.get("currency", "AOA")
            ledger_entry = {
                "wallet_id": recipient_id,
                "entry_type": "CREDIT",
                "amount_minor": amount_minor,
                "currency": currency,
                "trace_id": trace_id,
                "routing_request_id": routing_id,
                "interop_transfer_id": itx_id,
                "recorded_at": now_str,
            }
            from_op_id = req.get("from_operator_id", "operator-a-test")
            with lock:
                state["wallets"][recipient_id]["balance_minor"] += amount_minor
                state["routing_store"][routing_id] = {"body_hash": body_hash, "response": resp}
                state["ledger"].append(ledger_entry)
                state["events"].append({
                    "id": f"evt-{uuid.uuid4()}",
                    "event_type": "federation.routing.accepted",
                    "aggregate_type": "federation_payment",
                    "aggregate_id": routing_id,
                    "trace_id": trace_id,
                    "correlation_id": routing_id,
                    "payload": {},
                    "created_at": now_str,
                    "federation_version": "1",
                    "origin_operator_id": my_op_id,
                    "destination_operator_id": from_op_id,
                    "routing_request_id": routing_id,
                    "interop_transfer_id": itx_id,
                })
                state["events"].append({
                    "id": f"evt-{uuid.uuid4()}",
                    "event_type": "federation.payment.completed",
                    "aggregate_type": "federation_payment",
                    "aggregate_id": routing_id,
                    "trace_id": trace_id,
                    "correlation_id": routing_id,
                    "payload": {},
                    "created_at": now_str,
                    "federation_version": "1",
                    "origin_operator_id": my_op_id,
                    "destination_operator_id": from_op_id,
                    "routing_request_id": routing_id,
                    "interop_transfer_id": itx_id,
                })
            self._json(200, resp)

    return SimBHandler


# ── Trust Root Server ─────────────────────────────────────────────────────────

def _make_trust_root_handler(state: dict, lock: threading.Lock):
    class TrustRootHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def do_GET(self):
            if self.path == "/federation/revocation-list.json":
                with lock:
                    body = json.dumps(state["brl"], indent=2).encode("utf-8")
            elif self.path == "/federation/public-keys.json":
                with lock:
                    body = json.dumps(state["key_manifest"], indent=2).encode("utf-8")
            else:
                body = json.dumps({"error": "not_found"}).encode("utf-8")
                self.send_response(404)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return TrustRootHandler


# ── RunnerInfra ───────────────────────────────────────────────────────────────

class RunnerInfra:
    """
    Manages Simulated Operator B and Trust Root Server for federation tests.

    Usage:
        infra = RunnerInfra()
        infra.start()
        try:
            infra.configure_sim_b(manifest, cert)
            infra.configure_routing("operator-a-test", op_a_pub_bytes)
            infra.set_brl_empty()
            # ... run tests ...
        finally:
            infra.stop()
    """

    def __init__(self):
        self._sim_b_port = _free_port()
        self._trust_root_port = _free_port()
        self._lock = threading.Lock()

        self._sim_b_state = {
            "manifest": None,
            "cert": None,
            # FED-ROUTE: Operator A credentials for routing signature verification
            "op_a_public_key": None,
            "op_a_operator_id": None,
            # FED-ROUTE: in-memory routing store (idempotency cache)
            "routing_store": {},
            # FED-ROUTE: pre-configured wallets on Simulated Operator B
            "wallets": {
                "wallet-payee-test-001": {"status": "active", "balance_minor": 0},
                "wallet-suspended-test-001": {"status": "suspended", "balance_minor": 0},
            },
            # FED-EXEC: payee ledger entries (CREDIT on acceptance)
            "ledger": [],
            # FED-EXEC: federation events emitted on acceptance
            "events": [],
            # FED-FAIL: failure injection controls
            "drop_next_route_count": 0,      # return 503 for this many next requests
            "malformed_response_once": False, # return non-JSON 200 once
            "trust_failure_override_once": False, # return operator_trust_failure once
        }
        self._trust_root_state = {
            "brl": self._empty_brl(),
            "key_manifest": {"schema_version": "1", "published_at": "", "keys": []},
        }

        self._sim_b_server = None
        self._trust_root_server = None

    # ── URLs ─────────────────────────────────────────────────────────────────

    @property
    def sim_b_url(self) -> str:
        return f"http://localhost:{self._sim_b_port}"

    @property
    def brl_url(self) -> str:
        return f"http://localhost:{self._trust_root_port}/federation/revocation-list.json"

    @property
    def key_manifest_url(self) -> str:
        return f"http://localhost:{self._trust_root_port}/federation/public-keys.json"

    # ── Sim B configuration ───────────────────────────────────────────────────

    def configure_sim_b(self, manifest: dict, cert: dict) -> None:
        """Set the manifest and certificate served by Simulated Operator B."""
        with self._lock:
            self._sim_b_state["manifest"] = manifest
            self._sim_b_state["cert"] = cert

    def configure_routing(self, op_a_operator_id: str, op_a_public_key: bytes) -> None:
        """
        Configure Sim Op B with Operator A's ed25519 public key for routing
        signature verification (FED-ROUTE suite).
        """
        with self._lock:
            self._sim_b_state["op_a_operator_id"] = op_a_operator_id
            self._sim_b_state["op_a_public_key"] = op_a_public_key

    def reset_routing_state(self) -> None:
        """
        Clear routing request store, reset wallet balances, clear ledger and events.
        Call before each FED-ROUTE / FED-EXEC test to ensure test isolation (Section 6.1).
        """
        with self._lock:
            self._sim_b_state["routing_store"] = {}
            self._sim_b_state["wallets"] = {
                "wallet-payee-test-001": {"status": "active", "balance_minor": 0},
                "wallet-suspended-test-001": {"status": "suspended", "balance_minor": 0},
            }
            self._sim_b_state["ledger"] = []
            self._sim_b_state["events"] = []
            self._sim_b_state["drop_next_route_count"] = 0
            self._sim_b_state["malformed_response_once"] = False
            self._sim_b_state["trust_failure_override_once"] = False

    def get_wallet_balance(self, wallet_id: str):
        """Return current balance_minor for wallet_id, or None if not found."""
        with self._lock:
            wallet = self._sim_b_state["wallets"].get(wallet_id)
        return wallet["balance_minor"] if wallet is not None else None

    def get_sim_b_events(self, routing_request_id: str = None) -> list:
        """Return events emitted by Sim Op B, optionally filtered by routing_request_id."""
        with self._lock:
            events = list(self._sim_b_state["events"])
        if routing_request_id is not None:
            events = [e for e in events if e.get("routing_request_id") == routing_request_id]
        return events

    def get_sim_b_ledger(self, wallet_id: str) -> list:
        """Return ledger entries for the given wallet_id on Sim Op B."""
        with self._lock:
            return [e for e in self._sim_b_state["ledger"] if e.get("wallet_id") == wallet_id]

    def get_sim_b_accepted_routing_ids(self) -> list:
        """Return routing_request_ids that Sim Op B has accepted."""
        with self._lock:
            return [
                rr_id for rr_id, data in self._sim_b_state["routing_store"].items()
                if data.get("response", {}).get("status") == "accepted"
            ]

    # ── Failure injection (FED-FAIL suite) ───────────────────────────────────

    def set_drop_next_route(self, count: int = 1) -> None:
        """Make Sim Op B return HTTP 503 for the next N routing requests (F-101 / F-104)."""
        with self._lock:
            self._sim_b_state["drop_next_route_count"] = count

    def set_malformed_response_once(self) -> None:
        """Make Sim Op B return HTTP 200 with non-JSON body on next routing request (F-102)."""
        with self._lock:
            self._sim_b_state["malformed_response_once"] = True

    def set_trust_failure_once(self) -> None:
        """Make Sim Op B return rejection_code=operator_trust_failure on next routing (F-204)."""
        with self._lock:
            self._sim_b_state["trust_failure_override_once"] = True

    def inject_accepted_routing_on_b(
        self,
        routing_request_id: str,
        amount_minor: int,
        trace_id: str,
        currency: str = "AOA",
        interop_transfer_id: str = None,
    ) -> dict:
        """
        Directly inject an accepted routing into Sim Op B's routing_store without routing
        through the fixture server. Used to simulate crash scenarios (FED-SETTLE-009,
        FED-FAIL-005): Op B accepted a routing that Op A never committed.
        """
        itx_id = interop_transfer_id or f"itx-{uuid.uuid4()}"
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        resp = {
            "schema_version": "1",
            "routing_request_id": routing_request_id,
            "status": "accepted",
            "trace_id": trace_id,
            "interop_transfer_id": itx_id,
            "accepted_at": now_str,
        }
        body_hash = hashlib.sha256(routing_request_id.encode()).hexdigest()
        with self._lock:
            self._sim_b_state["routing_store"][routing_request_id] = {
                "body_hash": body_hash,
                "response": resp,
            }
        return resp

    # ── BRL configuration ─────────────────────────────────────────────────────

    def set_brl_empty(self) -> None:
        """BRL with no revocations (happy-path tests)."""
        with self._lock:
            self._trust_root_state["brl"] = self._empty_brl()

    def set_brl_expired(self) -> None:
        """BRL that expired 1 hour ago (for FED-TRUST-009 — INV-TRUST-006)."""
        now = datetime.now(timezone.utc)
        issued_at = (now - timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%SZ")
        expires_at = (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        with self._lock:
            self._trust_root_state["brl"] = {
                "schema_version": "1",
                "issued_at": issued_at,
                "expires_at": expires_at,
                "revoked": [],
                "signature": "A" * 86,
            }

    def set_brl_very_stale(self, stale_hours: int = 13) -> None:
        """BRL that expired stale_hours ago (for FED-FAIL-006 — F-602 >12h outage)."""
        now = datetime.now(timezone.utc)
        issued_at = (now - timedelta(hours=stale_hours + 1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        expires_at = (now - timedelta(hours=stale_hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
        with self._lock:
            self._trust_root_state["brl"] = {
                "schema_version": "1",
                "issued_at": issued_at,
                "expires_at": expires_at,
                "revoked": [],
                "signature": "A" * 86,
            }

    def set_brl_revoked(self, operator_id: str) -> None:
        """BRL that lists operator_id as revoked (FED-CERT-009)."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        expires = (datetime.now(timezone.utc) + timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
        with self._lock:
            self._trust_root_state["brl"] = {
                "schema_version": "1",
                "issued_at": now,
                "expires_at": expires,
                "revoked": [{
                    "operator_id": operator_id,
                    "reason": "revoked",
                    "permanent": True,
                    "since": now,
                }],
                "signature": "A" * 86,
            }

    # ── Key manifest configuration ────────────────────────────────────────────

    def set_key_manifest(self, keys: dict) -> None:
        """
        Update the key manifest served at /federation/public-keys.json.

        keys: dict of {key_id: public_key_bytes (bytes, 32)}.
        """
        from trust_root import b64url_encode
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        entries = [
            {
                "key_id": kid,
                "public_key": f"ed25519:{b64url_encode(pub)}",
                "active_since": now,
                "status": "active",
            }
            for kid, pub in keys.items()
        ]
        with self._lock:
            self._trust_root_state["key_manifest"] = {
                "schema_version": "1",
                "published_at": now,
                "keys": entries,
            }

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Start both embedded servers in daemon threads."""
        sim_b_handler = _make_sim_b_handler(self._sim_b_state, self._lock)
        self._sim_b_server = http.server.HTTPServer(("", self._sim_b_port), sim_b_handler)

        trust_root_handler = _make_trust_root_handler(self._trust_root_state, self._lock)
        self._trust_root_server = http.server.HTTPServer(("", self._trust_root_port), trust_root_handler)

        for srv in (self._sim_b_server, self._trust_root_server):
            t = threading.Thread(target=srv.serve_forever, daemon=True)
            t.start()

    def stop(self) -> None:
        """Shut down both embedded servers."""
        for srv in (self._sim_b_server, self._trust_root_server):
            if srv:
                srv.shutdown()

    # ── Internal helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _empty_brl() -> dict:
        now = datetime.now(timezone.utc)
        return {
            "schema_version": "1",
            "issued_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "expires_at": (now + timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "revoked": [],
            "signature": "A" * 86,
        }
