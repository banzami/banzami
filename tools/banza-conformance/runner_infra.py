"""
BANZA Federation Runner Infrastructure

Two embedded HTTP servers used exclusively by the conformance runner:

  SimBServer      — Simulated Operator B
      GET /.well-known/banza/operator.json     configurable manifest
      GET /.well-known/banza/certificate.json  configurable cert

  TrustRootServer — BANZA trust root endpoints
      GET /federation/revocation-list.json     configurable BRL
      GET /federation/public-keys.json         configurable key manifest

State is updated by the runner between tests using RunnerInfra methods.
Both servers are thread-safe; each is started in its own daemon thread.
"""

import http.server
import json
import socket
import threading
from datetime import datetime, timezone


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


# ── Simulated Operator B ──────────────────────────────────────────────────────

def _make_sim_b_handler(state: dict, lock: threading.Lock):
    class SimBHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass  # suppress per-request logs

        def do_GET(self):
            if self.path == "/.well-known/banza/operator.json":
                with lock:
                    body = json.dumps(state["manifest"], indent=2).encode("utf-8") \
                        if state["manifest"] else b'{"error":"not configured"}'
            elif self.path == "/.well-known/banza/certificate.json":
                with lock:
                    body = json.dumps(state["cert"], indent=2).encode("utf-8") \
                        if state["cert"] else b'{"error":"not configured"}'
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
            infra.set_brl_empty()
            # ... run tests ...
        finally:
            infra.stop()
    """

    def __init__(self):
        self._sim_b_port = _free_port()
        self._trust_root_port = _free_port()
        self._lock = threading.Lock()

        self._sim_b_state = {"manifest": None, "cert": None}
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

    # ── BRL configuration ─────────────────────────────────────────────────────

    def set_brl_empty(self) -> None:
        """BRL with no revocations (happy-path tests)."""
        with self._lock:
            self._trust_root_state["brl"] = self._empty_brl()

    def set_brl_expired(self) -> None:
        """BRL that expired 1 hour ago (for FED-TRUST-009 — INV-TRUST-006)."""
        now = datetime.now(timezone.utc)
        from datetime import timedelta
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

    def set_brl_revoked(self, operator_id: str) -> None:
        """BRL that lists operator_id as revoked (FED-CERT-009)."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        from datetime import timedelta
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
        from datetime import timedelta
        return {
            "schema_version": "1",
            "issued_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "expires_at": (now + timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "revoked": [],
            "signature": "A" * 86,
        }
