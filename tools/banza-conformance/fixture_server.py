"""
BANZA Federation Fixture Server

Minimal local HTTP server for running federation conformance tests without
a full operator deployment.

The runner generates a signed test certificate at startup and delivers it
via POST /conformance/setup. The server stores it in memory and serves it
at the well-known certificate endpoint.

Routes:
  POST /conformance/setup               → accept signed cert JSON from runner
  GET  /.well-known/banza/certificate.json → serve current cert (setup or static fallback)
  GET  /health                          → sandbox health response
  * → 404

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


def _find_fallback_fixture() -> bytes:
    """Locate CERT-A-VALID.json for use when no setup has been called."""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(this_dir, "..", "..", "conformance", "fixtures", "federation", "CERT-A-VALID.json"),
        os.path.join(os.getcwd(), "conformance", "fixtures", "federation", "CERT-A-VALID.json"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            with open(p) as f:
                data = json.load(f)
            return json.dumps(data, indent=2).encode("utf-8")
    raise FileNotFoundError(
        "CERT-A-VALID.json not found. Run from the repo root."
    )


class FederationFixtureHandler(http.server.BaseHTTPRequestHandler):
    """
    Handles federation conformance fixture requests.

    State is held in self.server.state (a dict) to support per-request
    updates from POST /conformance/setup.
    """

    def log_message(self, fmt, *args):
        print(f"  fixture-server [{self.command} {self.path}]: {fmt % args}")

    # ── GET ───────────────────────────────────────────────────────────────────

    def do_GET(self):
        if self.path == "/.well-known/banza/certificate.json":
            self._serve_cert()
        elif self.path == "/health":
            self._serve_health()
        else:
            self._not_found()

    def _serve_cert(self):
        body = self.server.state["cert_bytes"]
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_health(self):
        body = json.dumps({
            "status": "ok",
            "simulated": True,
            "production_allowed": False,
            "environment": "sandbox",
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
        else:
            self._not_found()

    def _handle_setup(self):
        """
        Accept a signed certificate (and optional config) from the conformance runner.

        Body: {"certificate": {...cert JSON...}}

        On success: stores the cert; returns HTTP 200 {"ok": true}.
        On error: returns HTTP 400 with error detail.
        """
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            payload = json.loads(raw)
        except Exception as exc:
            return self._respond_json(400, {"ok": False, "error": f"parse error: {exc}"})

        cert = payload.get("certificate")
        if not isinstance(cert, dict):
            return self._respond_json(400, {"ok": False, "error": "'certificate' field required (JSON object)"})

        cert_bytes = json.dumps(cert, indent=2).encode("utf-8")

        with self.server.state_lock:
            self.server.state["cert_bytes"] = cert_bytes
            self.server.state["cert"] = cert

        print(f"  fixture-server: cert updated — operator_id={cert.get('operator_id')!r} "
              f"issuer_key_id={cert.get('issuer_key_id')!r}")

        self._respond_json(200, {"ok": True, "operator_id": cert.get("operator_id")})

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _respond_json(self, status: int, body: dict):
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _not_found(self):
        self._respond_json(404, {"error": "not_found", "path": self.path})


def run_server(port: int) -> None:
    fallback_cert = _find_fallback_fixture()

    state = {
        "cert_bytes": fallback_cert,
        "cert": None,
    }

    server = http.server.HTTPServer(("", port), FederationFixtureHandler)
    server.state = state
    server.state_lock = threading.Lock()

    print(f"BANZA Federation Fixture Server")
    print(f"Port:    {port}")
    print(f"Cert:    http://localhost:{port}/.well-known/banza/certificate.json")
    print(f"Setup:   POST http://localhost:{port}/conformance/setup")
    print(f"Health:  http://localhost:{port}/health")
    print(f"Serving: static CERT-A-VALID fallback (until POST /conformance/setup)")
    print(f"Stop:    Ctrl+C")
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
