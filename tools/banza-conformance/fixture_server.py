"""
BANZA Federation Fixture Server

Minimal local HTTP server that acts as "Operator A" in federation conformance tests.

Routes:
  POST /conformance/setup                      accept cert + trust config from runner
  POST /conformance/federation/verify-peer     run ADR-026 trust protocol against a peer
  GET  /.well-known/banza/certificate.json     serve current operator certificate
  GET  /.well-known/banza/operator.json        serve federation manifest (FED-DISC)
  GET  /health                                 sandbox health response
  *    → 404

The trust engine (POST /conformance/federation/verify-peer) implements the
9-step ADR-026 trust verification protocol. It uses the BANZA root keys, BRL URL,
and key manifest URL provided via the setup endpoint.

Usage:
    # Terminal 1
    python3 tools/banza-conformance/fixture_server.py --port 8099

    # Terminal 2
    python3 tools/banza-conformance/run.py --federation --url http://localhost:8099

Stop with Ctrl+C.
"""

import argparse
import http.server
import json
import os
import sys
import threading
import urllib.request
import urllib.error
from datetime import datetime, timezone

# ── Crypto (optional — only needed for trust engine signature verification) ───

try:
    import trust_root as _tr
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


# ── Static fixture loader ─────────────────────────────────────────────────────

def _load_fallback_fixture() -> bytes:
    this_dir = os.path.dirname(os.path.abspath(__file__))
    for p in [
        os.path.join(this_dir, "..", "..", "conformance", "fixtures", "federation", "CERT-A-VALID.json"),
        os.path.join(os.getcwd(), "conformance", "fixtures", "federation", "CERT-A-VALID.json"),
    ]:
        if os.path.isfile(p):
            with open(p) as f:
                return json.dumps(json.load(f), indent=2).encode("utf-8")
    raise FileNotFoundError("CERT-A-VALID.json not found. Run from the repo root.")


# ── Trust engine (ADR-026 9-step protocol) ────────────────────────────────────

def _fetch_json(url: str, timeout: int = 10) -> dict:
    """Fetch and parse JSON from a URL. Raises RuntimeError on failure."""
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _b64url_decode(s: str) -> bytes:
    import base64
    pad = (4 - len(s) % 4) % 4
    return base64.urlsafe_b64decode(s + "=" * pad)


def _verify_sig(cert: dict, pub_bytes: bytes) -> tuple:
    """Verify cert signature. Returns (verified: bool, detail: str)."""
    if not CRYPTO_AVAILABLE:
        return False, "cryptography package not installed"
    return _tr.verify_certificate_signature(cert, pub_bytes)


def trust_verify_peer(peer_manifest_url: str, state: dict) -> dict:
    """
    ADR-026 9-step trust verification protocol.

    State must contain:
      banza_root_keys  dict {key_id: pub_bytes}
      brl_url          str
      key_manifest_url str

    Returns:
      {
        "trusted": bool,
        "steps": [{"step": "2.x", "name": str, "status": "pass"|"fail", ...}],
        "rejection_reason": str | None,
      }
    """
    steps = []
    banza_root_keys = dict(state.get("banza_root_keys") or {})
    brl_url = state.get("brl_url", "")
    key_manifest_url = state.get("key_manifest_url", "")

    def _fail(step_id, name, reason, **extra):
        steps.append({"step": step_id, "name": name, "status": "fail", "reason": reason, **extra})
        return {"trusted": False, "steps": steps, "rejection_reason": reason}

    def _pass(step_id, name, **extra):
        steps.append({"step": step_id, "name": name, "status": "pass", **extra})

    # Step 2.1 — Fetch manifest
    try:
        manifest = _fetch_json(peer_manifest_url)
        manifest_op_id = manifest.get("operator_id", "")
        _pass("2.1", "manifest_fetch", operator_id=manifest_op_id)
    except Exception as exc:
        return _fail("2.1", "manifest_fetch", "manifest_fetch_failed", detail=str(exc))

    # Step 2.2 — Fetch certificate
    cert_url = manifest.get("certificate_url", "")
    if not cert_url:
        return _fail("2.2", "certificate_fetch", "certificate_url_missing_from_manifest")
    try:
        cert = _fetch_json(cert_url)
        _pass("2.2", "certificate_fetch", certificate_url=cert_url)
    except Exception as exc:
        return _fail("2.2", "certificate_fetch", "certificate_fetch_failed", detail=str(exc))

    # Step 2.3 — Verify certificate signature
    key_id = cert.get("issuer_key_id", "")
    if key_id not in banza_root_keys and key_manifest_url:
        # Key rotation path (FED-CERT-011): unknown key_id → fetch key manifest
        try:
            km = _fetch_json(key_manifest_url)
            for entry in km.get("keys", []):
                if entry.get("key_id") == key_id and entry.get("status") == "active":
                    pk_str = entry.get("public_key", "")
                    if pk_str.startswith("ed25519:"):
                        banza_root_keys[key_id] = _b64url_decode(pk_str[8:])
                        steps.append({
                            "step": "2.3_key_fetch", "name": "key_manifest_fetch",
                            "status": "pass", "key_id": key_id,
                        })
                        break
        except Exception as exc:
            steps.append({
                "step": "2.3_key_fetch", "name": "key_manifest_fetch",
                "status": "fail", "detail": str(exc),
            })

    if key_id in banza_root_keys:
        verified, detail = _verify_sig(cert, banza_root_keys[key_id])
    else:
        verified, detail = False, f"unknown issuer_key_id: {key_id!r}"

    if not verified:
        return _fail("2.3", "signature_verify", "signature_invalid", detail=detail)
    _pass("2.3", "signature_verify", key_id=key_id)

    # Step 2.4 — Expiry check
    now = datetime.now(timezone.utc)
    try:
        expires_at = _parse_iso(cert.get("expires_at", ""))
        issued_at = _parse_iso(cert.get("issued_at", ""))
    except Exception as exc:
        return _fail("2.4", "expiry_check", "timestamp_parse_error", detail=str(exc))

    if expires_at <= now:
        return _fail("2.4", "expiry_check", "certificate_expired",
                     expires_at=cert.get("expires_at"), now=now.strftime("%Y-%m-%dT%H:%M:%SZ"))
    if issued_at > now:
        return _fail("2.4", "expiry_check", "certificate_future_dated",
                     issued_at=cert.get("issued_at"))
    _pass("2.4", "expiry_check", expires_at=cert.get("expires_at"))

    # Step 2.5 — Certification level
    level = cert.get("certification_level", 0)
    if level < 3:
        return _fail("2.5", "level_check", "certification_level_insufficient",
                     certification_level=level, required=3)
    _pass("2.5", "level_check", certification_level=level)

    # Step 2.6 — BRL check (INV-TRUST-003, INV-TRUST-006)
    if not brl_url:
        return _fail("2.6", "brl_check", "brl_url_not_configured")
    try:
        brl = _fetch_json(brl_url)
        brl_fetched_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        brl_expires_str = brl.get("expires_at", "")
        brl_issued_str = brl.get("issued_at", "")

        # INV-TRUST-006: BRL must not be older than 6 hours (expired BRL = stale)
        if brl_expires_str:
            try:
                brl_exp = _parse_iso(brl_expires_str)
                if brl_exp <= now:
                    brl_age_s = int((now - _parse_iso(brl_issued_str)).total_seconds()) \
                        if brl_issued_str else None
                    return _fail("2.6", "brl_check", "brl_expired",
                                 brl_expires_at=brl_expires_str,
                                 brl_issued_at=brl_issued_str,
                                 brl_fetched_at=brl_fetched_at,
                                 brl_age_seconds=brl_age_s,
                                 now=now.strftime("%Y-%m-%dT%H:%M:%SZ"))
            except Exception as exc:
                return _fail("2.6", "brl_check", "brl_timestamp_invalid",
                             brl_expires_at=brl_expires_str, detail=str(exc))

        revoked_ids = {r.get("operator_id") for r in brl.get("revoked", [])}
        cert_op_id = cert.get("operator_id", "")
        if cert_op_id in revoked_ids:
            return _fail("2.6", "brl_check", "operator_revoked",
                         operator_id=cert_op_id,
                         brl_expires_at=brl_expires_str,
                         brl_fetched_at=brl_fetched_at)
        _pass("2.6", "brl_check",
              brl_expires_at=brl_expires_str,
              brl_issued_at=brl_issued_str,
              brl_fetched_at=brl_fetched_at,
              revoked_count=len(revoked_ids))
    except Exception as exc:
        return _fail("2.6", "brl_check", "brl_fetch_failed", detail=str(exc))

    # Step 2.7 — supports_federation (manifest)
    if not manifest.get("supports_federation"):
        return _fail("2.7", "federation_support_check", "federation_not_declared_in_manifest")
    _pass("2.7", "federation_support_check")

    # Step 2.8 — routing capability in certificate
    caps = cert.get("capabilities", [])
    if "cross_operator_routing" not in caps:
        return _fail("2.8", "routing_capability_check",
                     "cross_operator_routing_missing_from_cert_capabilities",
                     cert_capabilities=caps)
    _pass("2.8", "routing_capability_check")

    # Step 2.9 — cert.operator_id == manifest.operator_id
    cert_op = cert.get("operator_id", "")
    manifest_op = manifest.get("operator_id", "")
    if cert_op != manifest_op:
        return _fail("2.9", "operator_id_binding", "operator_id_mismatch",
                     cert_operator_id=cert_op, manifest_operator_id=manifest_op)
    _pass("2.9", "operator_id_binding", operator_id=cert_op)

    return {"trusted": True, "steps": steps, "rejection_reason": None}


# ── HTTP handler ──────────────────────────────────────────────────────────────

class FederationFixtureHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"  fixture-server [{self.command} {self.path}]: {fmt % args}")

    # ── GET ───────────────────────────────────────────────────────────────────

    def do_GET(self):
        if self.path == "/.well-known/banza/certificate.json":
            self._serve_cert()
        elif self.path == "/.well-known/banza/operator.json":
            self._serve_manifest()
        elif self.path == "/health":
            self._serve_health()
        else:
            self._respond_json(404, {"error": "not_found", "path": self.path})

    def _serve_cert(self):
        body = self.server.state["cert_bytes"]
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_manifest(self):
        with self.server.state_lock:
            cert = self.server.state.get("cert") or {}

        op_id = cert.get("operator_id", "operator-a-test")
        cert_level = cert.get("certification_level", 3)

        host = self.headers.get("Host", "localhost")
        base_url = f"http://{host}"

        manifest = {
            "operator_id": op_id,
            "environment": "sandbox",
            "simulated": True,
            "production_allowed": False,
            "protocol_version": "1.0",
            "certification_level": cert_level,
            "capabilities": {
                "supports_wallets": True,
                "supports_qr": True,
                "supports_settlement": True,
            },
            "operator_name": "Operator A (Conformance Test)",
            "operator_url": base_url,
            "federation_version": "1",
            "certificate_url": f"{base_url}/.well-known/banza/certificate.json",
            "interop_endpoint": base_url,
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

        body = json.dumps(manifest, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_health(self):
        body = json.dumps({
            "status": "ok", "simulated": True,
            "production_allowed": False, "environment": "sandbox",
        }).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # ── POST ──────────────────────────────────────────────────────────────────

    def do_POST(self):
        if self.path == "/conformance/setup":
            self._handle_setup()
        elif self.path == "/conformance/federation/verify-peer":
            self._handle_verify_peer()
        else:
            self._respond_json(404, {"error": "not_found", "path": self.path})

    def _handle_setup(self):
        """
        POST /conformance/setup

        Body:
          {
            "certificate": {...},                    operator's test cert
            "banza_root_keys": {"key-id": "ed25519:<base64url>"},
            "brl_url": "http://...",
            "key_manifest_url": "http://..."
          }
        """
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
        except Exception as exc:
            return self._respond_json(400, {"ok": False, "error": str(exc)})

        cert = payload.get("certificate")
        if not isinstance(cert, dict):
            return self._respond_json(400, {"ok": False, "error": "'certificate' required"})

        # Decode banza_root_keys from "ed25519:<base64url>" strings to bytes
        raw_keys = payload.get("banza_root_keys") or {}
        decoded_keys = {}
        for kid, pk_str in raw_keys.items():
            if isinstance(pk_str, str) and pk_str.startswith("ed25519:"):
                try:
                    decoded_keys[kid] = _b64url_decode(pk_str[8:])
                except Exception:
                    pass

        cert_bytes = json.dumps(cert, indent=2).encode("utf-8")
        with self.server.state_lock:
            self.server.state["cert_bytes"] = cert_bytes
            self.server.state["cert"] = cert
            self.server.state["banza_root_keys"] = decoded_keys
            self.server.state["brl_url"] = payload.get("brl_url", "")
            self.server.state["key_manifest_url"] = payload.get("key_manifest_url", "")

        print(f"  fixture-server: setup OK — operator_id={cert.get('operator_id')!r} "
              f"keys={list(decoded_keys.keys())} brl={bool(self.server.state['brl_url'])}")

        self._respond_json(200, {
            "ok": True,
            "operator_id": cert.get("operator_id"),
            "banza_root_keys": list(decoded_keys.keys()),
        })

    def _handle_verify_peer(self):
        """
        POST /conformance/federation/verify-peer

        Body: {"peer_manifest_url": "http://..."}

        Runs the ADR-026 9-step trust protocol against the peer.
        Returns structured step results and a trusted/untrusted decision.
        """
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
        except Exception as exc:
            return self._respond_json(400, {"error": str(exc)})

        peer_manifest_url = payload.get("peer_manifest_url", "")
        if not peer_manifest_url:
            return self._respond_json(400, {"error": "'peer_manifest_url' required"})

        with self.server.state_lock:
            state_snapshot = {
                "banza_root_keys": dict(self.server.state.get("banza_root_keys") or {}),
                "brl_url": self.server.state.get("brl_url", ""),
                "key_manifest_url": self.server.state.get("key_manifest_url", ""),
            }

        try:
            result = trust_verify_peer(peer_manifest_url, state_snapshot)
        except Exception as exc:
            return self._respond_json(500, {"error": f"trust engine error: {exc}"})

        result["peer_manifest_url"] = peer_manifest_url
        self._respond_json(200, result)

    # ── Response helper ───────────────────────────────────────────────────────

    def _respond_json(self, status: int, body: dict):
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


# ── Server startup ────────────────────────────────────────────────────────────

def run_server(port: int) -> None:
    fallback_cert = _load_fallback_fixture()

    state = {
        "cert_bytes": fallback_cert,
        "cert": None,
        "banza_root_keys": {},
        "brl_url": "",
        "key_manifest_url": "",
    }

    # ThreadingHTTPServer: each request in its own thread, preventing deadlock
    # when the trust engine makes outbound HTTP requests during request handling.
    server = http.server.ThreadingHTTPServer(("", port), FederationFixtureHandler)
    server.state = state
    server.state_lock = threading.Lock()

    print(f"BANZA Federation Fixture Server")
    print(f"Port:         {port}")
    print(f"Manifest:     http://localhost:{port}/.well-known/banza/operator.json")
    print(f"Cert:         http://localhost:{port}/.well-known/banza/certificate.json")
    print(f"Setup:        POST http://localhost:{port}/conformance/setup")
    print(f"Verify peer:  POST http://localhost:{port}/conformance/federation/verify-peer")
    print(f"Health:       http://localhost:{port}/health")
    print(f"Stop:         Ctrl+C")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nfixture-server: stopped")


def main() -> None:
    parser = argparse.ArgumentParser(description="BANZA Federation Fixture Server")
    parser.add_argument("--port", type=int, default=8099, help="Port to listen on (default: 8099)")
    args = parser.parse_args()
    run_server(args.port)


if __name__ == "__main__":
    main()
