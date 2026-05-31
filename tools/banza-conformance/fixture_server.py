"""
BANZA Federation Fixture Server

Minimal local HTTP server for running federation conformance tests without
a full operator deployment. Serves the CERT-A-VALID fixture at the well-known
certificate endpoint so FED-CERT-001 can execute and pass locally.

Usage:
    python tools/banza-conformance/fixture_server.py [--port 8099]

Then in another terminal:
    python tools/banza-conformance/run.py --federation --url http://localhost:8099

Or standalone:
    python tools/banza-conformance/run_fed.py --url http://localhost:8099

Stop the server with Ctrl+C.
"""

import argparse
import http.server
import json
import os
import sys
from http.server import BaseHTTPRequestHandler


def _find_fixture_path() -> str:
    """Locate CERT-A-VALID.json relative to this file or the repo root."""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(this_dir, "..", "..", "conformance", "fixtures", "federation", "CERT-A-VALID.json"),
        os.path.join(os.getcwd(), "conformance", "fixtures", "federation", "CERT-A-VALID.json"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return os.path.normpath(p)
    raise FileNotFoundError(
        "CERT-A-VALID.json not found. Run from the repo root or ensure "
        "conformance/fixtures/federation/ exists."
    )


def _load_fixture() -> bytes:
    path = _find_fixture_path()
    with open(path) as f:
        data = json.load(f)
    return json.dumps(data, indent=2).encode("utf-8")


class FederationFixtureHandler(BaseHTTPRequestHandler):
    """
    Serves federation test fixtures at well-known endpoints.

    Routes:
      GET /.well-known/banza/certificate.json  → CERT-A-VALID fixture
      GET /health                               → {"status": "ok", "simulated": true}
    """

    def log_message(self, fmt, *args):
        print(f"  fixture-server: {fmt % args}")

    def do_GET(self):
        if self.path == "/.well-known/banza/certificate.json":
            self._serve_certificate()
        elif self.path == "/health":
            self._serve_health()
        else:
            self._not_found()

    def _serve_certificate(self):
        body = self.server.cert_fixture
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

    def _not_found(self):
        body = json.dumps({"error": "not_found"}).encode("utf-8")
        self.send_response(404)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(port: int) -> None:
    cert_fixture = _load_fixture()
    print(f"BANZA Federation Fixture Server")
    print(f"Port:     {port}")
    print(f"Endpoint: http://localhost:{port}/.well-known/banza/certificate.json")
    print(f"Fixture:  {_find_fixture_path()}")
    print(f"Stop:     Ctrl+C")
    print()

    server = http.server.HTTPServer(("", port), FederationFixtureHandler)
    server.cert_fixture = cert_fixture
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
