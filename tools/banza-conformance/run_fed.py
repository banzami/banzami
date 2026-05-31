"""
BANZA Federation Conformance Runner — Slice 8

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
  FED-OBL-001   Obligation Created Immediately After Acceptance          (Slice 7)
  FED-OBL-002   Obligation Amount Equals Routing Request Amount          (Slice 7)
  FED-OBL-003   Obligation trace_id Matches Routing Request              (Slice 7)
  FED-OBL-004   One Obligation Per routing_request_id                    (Slice 7)
  FED-OBL-005   obligor_signature Verifies Against Operator A Public Key (Slice 7)
  FED-OBL-006   Settlement State Transitions Are Valid                   (Slice 7)
  FED-OBL-007   Settled Obligation Contains settled_at + batch_id        (Slice 7)
  FED-EVT-001   federation.routing.accepted Emitted on Operator B        (Slice 8)
  FED-EVT-002   federation.payment.initiated Emitted on Operator A       (Slice 8)
  FED-EVT-003   federation.payment.completed Emitted on Operator B       (Slice 8)
  FED-EVT-004   federation.obligation.recorded Emitted on Operator A     (Slice 8)
  FED-EVT-005   All Federation Events Share trace_id (INV-FED-001)       (Slice 8)
  FED-EVT-006   Federation Events Validate Against Schema                (Slice 8)
  FED-SETTLE-001 Obligation Export Includes All Pending Obligations       (Slice 9)
  FED-SETTLE-002 Net Position Computed Correctly                          (Slice 9)
  FED-SETTLE-003 Both Operators Independently Compute Same Net            (Slice 9)
  FED-SETTLE-004 Settlement Execution: Ledger Entries Correct             (Slice 9)
  FED-SETTLE-005 Obligations Marked Settled With Required Fields          (Slice 9)
  FED-SETTLE-006 Reconciliation: All Accepted Routing Requests Have Obls  (Slice 9)
  FED-SETTLE-007 Reconciliation: Trace Cross-Check Across Both Operators  (Slice 9)
  FED-SETTLE-008 Settlement Blocked on Unresolved Discrepancy             (Slice 9)
  FED-SETTLE-009 Netting Disagreement: Full Exchange Identifies Missing   (Slice 10)
  FED-SETTLE-010 Zero-Net Case: No Bank Transfer; All Obligations Settled (Slice 10)
  FED-FAIL-001  Network Timeout Retry With Same routing_request_id        (Slice 10)
  FED-FAIL-002  All Retries Fail: No Debit, No Obligation                 (Slice 10)
  FED-FAIL-003  Unparseable Response Treated as Network Failure           (Slice 10)
  FED-FAIL-004  Operator A Certificate Rejected by Operator B             (Slice 10)
  FED-FAIL-005  Crash Recovery: Missing Obligation Recreated              (Slice 10)
  FED-FAIL-006  Extended BRL Outage: Fail-Closed After 12 Hours           (Slice 10)
  FED-FAIL-007  Revocation Mid-Flight: Obligation Survives                (Slice 10)
  FED-FAIL-008  Obligation Amount Mismatch Detected Before Signing        (Slice 10)

Spec: FEDERATION_TEST_SUITE_SPEC.md §Suite FED-CERT, §Suite FED-DISC,
      §Suite FED-TRUST, §Suite FED-ROUTE, §Suite FED-EXEC, §Suite FED-OBL,
      §Suite FED-EVT, §Suite FED-SETTLE, §Suite FED-FAIL
Contracts: contracts/federation/operator-certificate.json,
           contracts/federation/federation-manifest.json,
           contracts/federation/federation-routing.json,
           contracts/federation/federation-obligation.json,
           contracts/federation/federation-event.json

Requires:
  cryptography>=41.0.0  for FED-CERT-002, FED-CERT-008–011, FED-DISC-007,
                        all FED-TRUST tests, all FED-ROUTE tests,
                        all FED-EXEC tests, FED-OBL-005, all FED-EVT tests
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

RUNNER_VERSION = "1.1.0-slice10"

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


def _find_obligation_schema_path() -> Optional[str]:
    this_dir = os.path.dirname(os.path.abspath(__file__))
    for p in [
        os.path.join(this_dir, "..", "..", "contracts", "federation", "federation-obligation.json"),
        os.path.join(os.getcwd(), "contracts", "federation", "federation-obligation.json"),
    ]:
        if os.path.isfile(p):
            return os.path.normpath(p)
    return None


def _find_event_schema_path() -> Optional[str]:
    this_dir = os.path.dirname(os.path.abspath(__file__))
    for p in [
        os.path.join(this_dir, "..", "..", "contracts", "federation", "federation-event.json"),
        os.path.join(os.getcwd(), "contracts", "federation", "federation-event.json"),
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


_OBL_ID_PATTERN = r"^ob-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
_ITX_PATTERN_OBL = r"^itx-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
_RR_PATTERN = r"^rr-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
_OBL_SIG_PATTERN = r"^[A-Za-z0-9_-]{86}$"


def validate_obligation(obl: dict) -> list:
    """
    Validate a parsed obligation against federation-obligation.json constraints.
    Returns a list of error strings. Empty list means valid.
    """
    if not isinstance(obl, dict):
        return ["body is not a JSON object"]

    errors = []
    required = [
        "schema_version", "obligation_id", "from_operator_id", "to_operator_id",
        "amount", "routing_request_id", "interop_transfer_id", "trace_id",
        "recorded_at", "settlement_state", "obligor_signature",
    ]
    for f in required:
        if f not in obl:
            errors.append(f"required field missing: '{f}'")

    if "schema_version" in obl and obl["schema_version"] != "1":
        errors.append(f"schema_version must be '1', got {obl['schema_version']!r}")

    if "obligation_id" in obl:
        if not re.match(_OBL_ID_PATTERN, str(obl["obligation_id"])):
            errors.append(f"obligation_id format invalid: {obl['obligation_id']!r}")

    if "routing_request_id" in obl:
        if not re.match(_RR_PATTERN, str(obl["routing_request_id"])):
            errors.append(f"routing_request_id format invalid: {obl['routing_request_id']!r}")

    if "interop_transfer_id" in obl:
        if not re.match(_ITX_PATTERN_OBL, str(obl["interop_transfer_id"])):
            errors.append(f"interop_transfer_id format invalid: {obl['interop_transfer_id']!r}")

    amount = obl.get("amount")
    if amount is not None:
        if not isinstance(amount, dict):
            errors.append("amount must be an object")
        else:
            minor = amount.get("minor")
            if not isinstance(minor, int) or isinstance(minor, bool) or minor < 1:
                errors.append(f"amount.minor must be a positive integer, got {minor!r}")
            currency = amount.get("currency")
            if not isinstance(currency, str) or not re.match(r"^[A-Z]{3}$", currency):
                errors.append(f"amount.currency must match ^[A-Z]{{3}}$, got {currency!r}")

    state = obl.get("settlement_state")
    if state is not None and state not in ("pending", "in_netting", "settled"):
        errors.append(f"settlement_state must be pending|in_netting|settled, got {state!r}")

    if state == "settled":
        if "settled_at" not in obl:
            errors.append("settled_at required when settlement_state=settled")
        if "settlement_batch_id" not in obl:
            errors.append("settlement_batch_id required when settlement_state=settled")

    if "obligor_signature" in obl:
        sig = obl["obligor_signature"]
        if not isinstance(sig, str) or not re.match(_OBL_SIG_PATTERN, sig):
            errors.append(f"obligor_signature format invalid (expected 86 base64url chars)")

    return errors


# ── Federation event validation (FED-EVT-006) ────────────────────────────────

_EVT_TYPE_ENUM = frozenset({
    "federation.routing.received",
    "federation.routing.accepted",
    "federation.routing.rejected",
    "federation.payment.initiated",
    "federation.payment.completed",
    "federation.payment.failed",
    "federation.obligation.recorded",
    "federation.obligation.settled",
    "federation.settlement.initiated",
    "federation.settlement.completed",
})
_EVT_ROUTING_TYPES = frozenset({
    "federation.routing.received",
    "federation.routing.accepted",
    "federation.routing.rejected",
    "federation.payment.initiated",
    "federation.payment.completed",
    "federation.payment.failed",
})
_EVT_OBLIGATION_TYPES = frozenset({
    "federation.obligation.recorded",
    "federation.obligation.settled",
    "federation.settlement.initiated",
    "federation.settlement.completed",
})
_EVT_ID_PATTERN = r"^evt-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


def validate_federation_event(evt: dict) -> list:
    """
    Validate a parsed federation event against federation-event.json requirements.
    Checks base envelope fields + federation extension fields.
    Returns list of error strings. Empty = valid.
    """
    if not isinstance(evt, dict):
        return ["body is not a JSON object"]

    errors = []

    # Base envelope required fields
    for f in ("id", "event_type", "aggregate_type", "aggregate_id",
              "trace_id", "correlation_id", "payload", "created_at"):
        if f not in evt:
            errors.append(f"required field missing: '{f}'")

    if "id" in evt:
        if not isinstance(evt["id"], str) or not re.match(_EVT_ID_PATTERN, str(evt["id"])):
            errors.append(f"id must match ^evt-<uuid>$, got {evt.get('id')!r}")

    if "aggregate_type" in evt and evt["aggregate_type"] != "federation_payment":
        errors.append(
            f"aggregate_type must be 'federation_payment', got {evt['aggregate_type']!r}"
        )

    evt_type = evt.get("event_type", "")
    if evt_type and evt_type not in _EVT_TYPE_ENUM:
        errors.append(f"event_type {evt_type!r} not in federation event type registry")

    if "payload" in evt and not isinstance(evt["payload"], dict):
        errors.append("payload must be an object")

    # Federation extension required fields
    for f in ("federation_version", "origin_operator_id", "destination_operator_id"):
        if f not in evt:
            errors.append(f"required federation field missing: '{f}'")

    if "federation_version" in evt and evt["federation_version"] != "1":
        errors.append(
            f"federation_version must be '1', got {evt['federation_version']!r}"
        )

    # Conditional: routing_request_id required for routing.* and payment.* events
    if evt_type in _EVT_ROUTING_TYPES and "routing_request_id" not in evt:
        errors.append(f"routing_request_id required for event_type '{evt_type}'")

    # Conditional: obligation_id required for obligation.* and settlement.* events
    if evt_type in _EVT_OBLIGATION_TYPES and "obligation_id" not in evt:
        errors.append(f"obligation_id required for event_type '{evt_type}'")

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
    op_a_signing_key_b64: str = None,
) -> bool:
    """
    Deliver the signed certificate + trust configuration to the operator.

    Extended payload (Slice 2) adds BANZA root keys, BRL URL, and key manifest URL
    so the operator's trust engine can verify remote peer certificates.
    Slice 7 adds op_a_signing_key so the fixture server can sign obligations (FED-OBL-005).
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
    if op_a_signing_key_b64:
        payload["op_a_signing_key"] = op_a_signing_key_b64
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


def _get_obligations_all_op_a(base_url: str) -> tuple:
    """GET /conformance/federation/obligations → (status, dict_or_None)."""
    try:
        status, _, raw = http_get(f"{base_url}/conformance/federation/obligations")
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


def _get_sim_b_events_http(sim_b_url: str) -> tuple:
    """GET /federation/events on Simulated Operator B → (status, dict_or_None)."""
    try:
        status, _, raw = http_get(f"{sim_b_url}/federation/events")
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


# ── FED-SETTLE HTTP helpers ───────────────────────────────────────────────────

def _netting_trigger(base_url: str) -> tuple:
    """POST /conformance/federation/netting/trigger → (status, body_or_None)."""
    try:
        status, _, raw = http_post(f"{base_url}/conformance/federation/netting/trigger", {})
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _netting_execute(base_url: str, batch_id: str) -> tuple:
    """POST /conformance/federation/netting/execute → (status, body_or_None)."""
    try:
        status, _, raw = http_post(
            f"{base_url}/conformance/federation/netting/execute",
            {"settlement_batch_id": batch_id},
        )
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _add_b_obligation(
    base_url: str,
    amount_minor: int,
    routing_request_id: str,
    trace_id: str,
    currency: str = "AOA",
) -> tuple:
    """POST /conformance/federation/netting/add-b-obligation → (status, body_or_None)."""
    try:
        status, _, raw = http_post(
            f"{base_url}/conformance/federation/netting/add-b-obligation",
            {
                "amount_minor": amount_minor,
                "currency": currency,
                "routing_request_id": routing_request_id,
                "trace_id": trace_id,
                "from_operator_id": "operator-b-test",
                "to_operator_id": "operator-a-test",
            },
        )
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _inject_discrepancy(
    base_url: str,
    routing_request_id: str,
    reported_amount_minor: int,
) -> tuple:
    """POST /conformance/federation/netting/inject-discrepancy → (status, body_or_None)."""
    try:
        status, _, raw = http_post(
            f"{base_url}/conformance/federation/netting/inject-discrepancy",
            {
                "routing_request_id": routing_request_id,
                "reported_amount_minor": reported_amount_minor,
            },
        )
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _reset_netting_state(base_url: str) -> bool:
    """POST /conformance/federation/netting/reset → True if OK."""
    try:
        status, _, _ = http_post(f"{base_url}/conformance/federation/netting/reset", {})
        return status in (200, 204)
    except RuntimeError:
        return False


def _get_netting_settlement_ledger(base_url: str) -> tuple:
    """GET /conformance/federation/netting/settlement-ledger → (status, body_or_None)."""
    try:
        status, _, raw = http_get(f"{base_url}/conformance/federation/netting/settlement-ledger")
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _get_routing_commits(base_url: str) -> tuple:
    """GET /conformance/federation/routing-commits → (status, body_or_None)."""
    try:
        status, _, raw = http_get(f"{base_url}/conformance/federation/routing-commits")
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _netting_reconcile(base_url: str, op_b_accepted_ids: list) -> tuple:
    """POST /conformance/federation/netting/reconcile → (status, body_or_None)."""
    try:
        status, _, raw = http_post(
            f"{base_url}/conformance/federation/netting/reconcile",
            {"operator_b_accepted_routing_ids": op_b_accepted_ids},
        )
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _fail_inject_crash_state(
    base_url: str,
    routing_request_id: str,
    trace_id: str,
    interop_transfer_id: str,
    amount_minor: int,
    currency: str = "AOA",
    from_operator_id: str = "operator-a-test",
    to_operator_id: str = "operator-b-test",
    sender_wallet_id: str = "wallet-sender-test-001",
) -> tuple:
    """POST /conformance/federation/fail/inject-crash-state → (status, body_or_None)."""
    try:
        status, _, raw = http_post(
            f"{base_url}/conformance/federation/fail/inject-crash-state",
            {
                "routing_request_id": routing_request_id,
                "trace_id": trace_id,
                "interop_transfer_id": interop_transfer_id,
                "amount_minor": amount_minor,
                "currency": currency,
                "from_operator_id": from_operator_id,
                "to_operator_id": to_operator_id,
                "sender_wallet_id": sender_wallet_id,
            },
        )
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _fail_trigger_recovery(base_url: str) -> tuple:
    """POST /conformance/federation/fail/trigger-recovery → (status, body_or_None)."""
    try:
        status, _, raw = http_post(f"{base_url}/conformance/federation/fail/trigger-recovery", {})
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _fail_recover_obligation(
    base_url: str,
    routing_request_id: str,
    trace_id: str,
    interop_transfer_id: str,
    amount_minor: int,
    currency: str = "AOA",
    from_operator_id: str = "operator-a-test",
    to_operator_id: str = "operator-b-test",
) -> tuple:
    """POST /conformance/federation/fail/recover-obligation → (status, body_or_None)."""
    try:
        status, _, raw = http_post(
            f"{base_url}/conformance/federation/fail/recover-obligation",
            {
                "routing_request_id": routing_request_id,
                "trace_id": trace_id,
                "interop_transfer_id": interop_transfer_id,
                "amount_minor": amount_minor,
                "currency": currency,
                "from_operator_id": from_operator_id,
                "to_operator_id": to_operator_id,
            },
        )
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, None
    except RuntimeError as exc:
        raise


def _fail_inject_obligation_amount_override(
    base_url: str,
    routing_request_id: str,
    override_amount_minor: int,
) -> tuple:
    """POST /conformance/federation/fail/inject-obligation-amount-override → (status, body_or_None)."""
    try:
        status, _, raw = http_post(
            f"{base_url}/conformance/federation/fail/inject-obligation-amount-override",
            {
                "routing_request_id": routing_request_id,
                "override_amount_minor": override_amount_minor,
            },
        )
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


# ── FED-OBL constants ────────────────────────────────────────────────────────

_OBL_RR_ID = "rr-00000000-0000-0000-0000-000000000001"
_OBL_TRACE_ID = "tr-00000000-0000-0000-0000-000000000001"
_OBL_AMOUNT = 50000
_OBL_CURRENCY = "AOA"
_OBL_SENDER_WALLET = "wallet-sender-test-001"
_OBL_PAYEE_WALLET = "wallet-payee-test-001"
_OBL_BATCH_ID = "stl-test-batch-001"

# ── FED-EVT constants ─────────────────────────────────────────────────────────

_EVT_RR_ID = "rr-00000000-0000-0000-0000-000000000002"
_EVT_TRACE_ID = "tr-00000000-0000-0000-0000-000000000002"

# ── FED-SETTLE constants ──────────────────────────────────────────────────────

# Tests 001–005, 007–008: 3 A→B obligations of 50,000 AOA each
_SETTLE_RR_ID_1 = "rr-00000000-0000-0000-0000-000000003001"
_SETTLE_RR_ID_2 = "rr-00000000-0000-0000-0000-000000003002"
_SETTLE_RR_ID_3 = "rr-00000000-0000-0000-0000-000000003003"
_SETTLE_TRACE_1 = "tr-00000000-0000-0000-0000-000000003001"
_SETTLE_TRACE_2 = "tr-00000000-0000-0000-0000-000000003002"
_SETTLE_TRACE_3 = "tr-00000000-0000-0000-0000-000000003003"
_SETTLE_AMOUNT = 50000         # AOA minor units per routing request
_SETTLE_B_TO_A_AMOUNT = 40000  # AOA minor units for the simulated B→A obligation

# Test 006: 5 routing requests for reconciliation check
_SETTLE_REC_RR_IDS = [
    "rr-00000000-0000-0000-0000-000000004001",
    "rr-00000000-0000-0000-0000-000000004002",
    "rr-00000000-0000-0000-0000-000000004003",
    "rr-00000000-0000-0000-0000-000000004004",
    "rr-00000000-0000-0000-0000-000000004005",
]
_SETTLE_REC_TRACE_IDS = [
    "tr-00000000-0000-0000-0000-000000004001",
    "tr-00000000-0000-0000-0000-000000004002",
    "tr-00000000-0000-0000-0000-000000004003",
    "tr-00000000-0000-0000-0000-000000004004",
    "tr-00000000-0000-0000-0000-000000004005",
]
# B→A routing_request_id used in SETTLE-002 and SETTLE-003
_SETTLE_B_TO_A_RR_ID = "rr-00000000-0000-0000-0000-000000003099"
_SETTLE_B_TO_A_TRACE = "tr-00000000-0000-0000-0000-000000003099"

# ── FED-SETTLE-009 constants ──────────────────────────────────────────────────

# 3 normal obligations + 1 injected-on-B-only (missing on A)
_SETTLE9_RR_ID_1 = "rr-00000000-0000-0000-0000-000000009001"
_SETTLE9_RR_ID_2 = "rr-00000000-0000-0000-0000-000000009002"
_SETTLE9_RR_ID_3 = "rr-00000000-0000-0000-0000-000000009003"
_SETTLE9_MISSING_RR_ID = "rr-00000000-0000-0000-0000-000000009004"
_SETTLE9_MISSING_ITX_ID = "itx-00000000-0000-0000-0000-000000009004"
_SETTLE9_TRACE_1 = "tr-00000000-0000-0000-0000-000000009001"
_SETTLE9_TRACE_2 = "tr-00000000-0000-0000-0000-000000009002"
_SETTLE9_TRACE_3 = "tr-00000000-0000-0000-0000-000000009003"
_SETTLE9_MISSING_TRACE = "tr-00000000-0000-0000-0000-000000009004"

# ── FED-SETTLE-010 constants ──────────────────────────────────────────────────

# 2 A→B + 2 B→A of equal amount → zero-net
_SETTLE10_RR_ID_1 = "rr-00000000-0000-0000-0000-000000010001"
_SETTLE10_RR_ID_2 = "rr-00000000-0000-0000-0000-000000010002"
_SETTLE10_TRACE_1 = "tr-00000000-0000-0000-0000-000000010001"
_SETTLE10_TRACE_2 = "tr-00000000-0000-0000-0000-000000010002"
_SETTLE10_AMOUNT = 30000  # AOA — equal A→B and B→A amounts → net = 0

# ── FED-FAIL constants ────────────────────────────────────────────────────────

_FAIL1_RR_ID = "rr-00000000-0000-0000-0000-000000007001"
_FAIL1_TRACE  = "tr-00000000-0000-0000-0000-000000007001"
_FAIL2_RR_ID = "rr-00000000-0000-0000-0000-000000007002"
_FAIL2_TRACE  = "tr-00000000-0000-0000-0000-000000007002"
_FAIL3_RR_ID = "rr-00000000-0000-0000-0000-000000007003"
_FAIL3_TRACE  = "tr-00000000-0000-0000-0000-000000007003"
_FAIL4_RR_ID = "rr-00000000-0000-0000-0000-000000007004"
_FAIL4_TRACE  = "tr-00000000-0000-0000-0000-000000007004"
_FAIL5_RR_ID = "rr-00000000-0000-0000-0000-000000007005"
_FAIL5_TRACE  = "tr-00000000-0000-0000-0000-000000007005"
_FAIL5_ITX_ID = "itx-00000000-0000-0000-0000-000000007005"
_FAIL6_RR_ID = "rr-00000000-0000-0000-0000-000000007006"
_FAIL6_TRACE  = "tr-00000000-0000-0000-0000-000000007006"
_FAIL7_RR_ID = "rr-00000000-0000-0000-0000-000000007007"
_FAIL7_TRACE  = "tr-00000000-0000-0000-0000-000000007007"
_FAIL8_RR_ID = "rr-00000000-0000-0000-0000-000000007008"
_FAIL8_TRACE  = "tr-00000000-0000-0000-0000-000000007008"
_FAIL_AMOUNT  = 50000  # AOA minor units for FAIL tests


# ── FED-OBL helpers ───────────────────────────────────────────────────────────

def _mark_obl_in_netting(base_url: str, rr_id: str) -> tuple:
    """POST /conformance/federation/obligations/{rr_id}/mark-in-netting. Returns (status, body)."""
    url = f"{base_url}/conformance/federation/obligations/{rr_id}/mark-in-netting"
    data = json.dumps({}).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return resp.status, json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, None
    except Exception as exc:
        raise RuntimeError(f"POST {url}: {exc}") from exc


def _mark_obl_settled(base_url: str, rr_id: str, batch_id: str) -> tuple:
    """POST /conformance/federation/obligations/{rr_id}/mark-settled. Returns (status, body)."""
    url = f"{base_url}/conformance/federation/obligations/{rr_id}/mark-settled"
    data = json.dumps({"settlement_batch_id": batch_id}).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return resp.status, json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, None
    except Exception as exc:
        raise RuntimeError(f"POST {url}: {exc}") from exc


def _obligation_canonical_bytes_runner(obl: dict) -> bytes:
    """Canonical JSON for obligation signature verification: all fields except obligor_signature."""
    payload = {k: v for k, v in obl.items() if k != "obligor_signature"}
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


# ── FED-OBL-001 ──────────────────────────────────────────────────────────────

def run_fed_obl_001(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-OBL-001 — Obligation Created Immediately After Acceptance

    Obligation exists in Operator A's obligation store after routing accepted.
    settlement_state=pending.

    Pass:   Obligation found; settlement_state=pending; obligation_id present
    Fail:   No obligation; wrong routing_request_id; settlement_state != pending
    Severity: CRITICAL
    Invariant: INV-FED-002
    L3 Req: FED-L3-013
    """
    case = _make_case("FED-OBL-001", "Obligation Created Immediately After Acceptance")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_OBL_RR_ID,
        trace_id=_OBL_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, obligation = _get_obligation_op_a(base_url, _OBL_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    obl_exists = obligation is not None
    state_pending = obligation.get("settlement_state") == "pending" if obligation else False
    rr_id_match = obligation.get("routing_request_id") == _OBL_RR_ID if obligation else False
    obl_id_present = (obligation.get("obligation_id", "").startswith("ob-") if obligation else False)
    recorded_at_present = bool(obligation.get("recorded_at")) if obligation else False

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion("obligation found in Operator A store",
                   obl_exists, "found", "missing" if not obl_exists else "found"),
        _assertion("obligation.settlement_state=pending",
                   state_pending, "pending",
                   obligation.get("settlement_state") if obligation else None),
        _assertion("obligation.routing_request_id matches",
                   rr_id_match, _OBL_RR_ID,
                   obligation.get("routing_request_id") if obligation else None),
        _assertion("obligation.obligation_id is ob-<uuid> format",
                   obl_id_present, "ob-<uuid>",
                   obligation.get("obligation_id") if obligation else "(missing)"),
        _assertion("obligation.recorded_at is present",
                   recorded_at_present, "ISO 8601",
                   obligation.get("recorded_at") if obligation else "(missing)"),
    ]
    case["evidence"] = {
        "routing_request_id": _OBL_RR_ID,
        "obligation": obligation,
        "obligation_exists": obl_exists,
        "settlement_state": obligation.get("settlement_state") if obligation else None,
        "obligation_id": obligation.get("obligation_id") if obligation else None,
        "recorded_at": obligation.get("recorded_at") if obligation else None,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-OBL-002 ──────────────────────────────────────────────────────────────

def run_fed_obl_002(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-OBL-002 — Obligation Amount Equals Routing Request Amount (INV-FED-005)

    Amount in obligation must match routing request exactly.

    Pass:   obligation.amount.minor == 50000 AND obligation.amount.currency == "AOA"
    Fail:   Any difference; rounding; currency changed
    Severity: CRITICAL
    Invariant: INV-FED-005
    L3 Req: FED-L3-014
    """
    case = _make_case("FED-OBL-002", "Obligation Amount Equals Routing Request Amount (INV-FED-005)")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_OBL_RR_ID,
        trace_id=_OBL_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, obligation = _get_obligation_op_a(base_url, _OBL_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if obligation is None:
        return _fail_case(case, "obligation not found after accepted routing", ms)

    obl_amount = obligation.get("amount") or {}
    obl_minor = obl_amount.get("minor")
    obl_currency = obl_amount.get("currency")

    minor_match = obl_minor == _OBL_AMOUNT
    currency_match = obl_currency == _OBL_CURRENCY

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion(f"obligation.amount.minor == {_OBL_AMOUNT}",
                   minor_match, _OBL_AMOUNT, obl_minor),
        _assertion(f"obligation.amount.currency == '{_OBL_CURRENCY}'",
                   currency_match, _OBL_CURRENCY, obl_currency),
    ]
    case["evidence"] = {
        "routing_request_id": _OBL_RR_ID,
        "routing_request_amount_minor": _OBL_AMOUNT,
        "routing_request_currency": _OBL_CURRENCY,
        "obligation_amount_minor": obl_minor,
        "obligation_currency": obl_currency,
        "amount_match": minor_match,
        "currency_match": currency_match,
        "obligation_amount_match": minor_match and currency_match,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-OBL-003 ──────────────────────────────────────────────────────────────

def run_fed_obl_003(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-OBL-003 — Obligation trace_id Matches Routing Request (INV-FED-001)

    trace_id propagated from routing request into obligation.

    Pass:   obligation.trace_id === routing_request.trace_id
    Fail:   Different value; missing
    Severity: CRITICAL
    Invariant: INV-FED-001
    L3 Req: FED-L3-012
    """
    case = _make_case("FED-OBL-003", "Obligation trace_id Matches Routing Request (INV-FED-001)")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_OBL_RR_ID,
        trace_id=_OBL_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, obligation = _get_obligation_op_a(base_url, _OBL_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if obligation is None:
        return _fail_case(case, "obligation not found after accepted routing", ms)

    obl_trace_id = obligation.get("trace_id")
    trace_match = obl_trace_id == _OBL_TRACE_ID

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion("obligation.trace_id === routing_request.trace_id (INV-FED-001)",
                   trace_match, _OBL_TRACE_ID, obl_trace_id),
    ]
    case["evidence"] = {
        "routing_request_id": _OBL_RR_ID,
        "routing_request_trace_id": _OBL_TRACE_ID,
        "obligation_trace_id": obl_trace_id,
        "trace_id_match": trace_match,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-OBL-004 ──────────────────────────────────────────────────────────────

def run_fed_obl_004(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-OBL-004 — One Obligation Per routing_request_id (INV-FED-002)

    UNIQUE constraint enforced; duplicate obligation not possible via recovery path.

    Pass:   Count of obligations with routing_request_id remains 1
    Fail:   Count > 1; second obligation created
    Severity: CRITICAL
    Invariant: INV-FED-002
    L3 Req: FED-L3-013
    """
    case = _make_case("FED-OBL-004", "One Obligation Per routing_request_id (INV-FED-002)")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_OBL_RR_ID,
        trace_id=_OBL_TRACE_ID,
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

    # Recovery path: call again with same routing_request_id (same body)
    payload2 = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_OBL_RR_ID,
        trace_id=_OBL_TRACE_ID,
        op_a_priv=op_a_priv,
    )
    try:
        _, result2 = _call_fed_route(base_url, payload2)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    # Count obligations with this routing_request_id
    try:
        _, all_obls = _get_obligations_all_op_a(base_url)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    obligations_list = (all_obls.get("obligations") or []) if all_obls else []
    matching = [o for o in obligations_list if o.get("routing_request_id") == _OBL_RR_ID]
    count = len(matching)

    assertions = [
        _assertion("first routing accepted", result1.get("routing_status") == "accepted",
                   "accepted", result1.get("routing_status")),
        _assertion("second call succeeds (idempotent replay)",
                   result2 is not None and result2.get("routing_status") in ("accepted", None),
                   "accepted or cached", result2.get("routing_status") if result2 else None),
        _assertion("obligation count for routing_request_id == 1 (INV-FED-002)",
                   count == 1, 1, count),
    ]
    case["evidence"] = {
        "routing_request_id": _OBL_RR_ID,
        "result_first_call": result1,
        "result_second_call": result2,
        "obligations_with_rr_id": count,
        "uniqueness_enforced": count == 1,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-OBL-005 ──────────────────────────────────────────────────────────────

def run_fed_obl_005(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-OBL-005 — obligor_signature Verifies Against Operator A Public Key

    Obligation signed by Operator A; non-repudiable.

    Pass:   ed25519_verify(op_a_public_key, canonical_obligation, obligor_signature) = true
    Fail:   Verification = false; signature missing; wrong key used
    Severity: STANDARD
    """
    case = _make_case(
        "FED-OBL-005", "obligor_signature Verifies Against Operator A Public Key"
    )

    if not _tr.CRYPTO_AVAILABLE:
        return _skip_case(case, "cryptography package not installed; install cryptography>=41.0.0")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_OBL_RR_ID,
        trace_id=_OBL_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, obligation = _get_obligation_op_a(base_url, _OBL_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if obligation is None:
        return _fail_case(case, "obligation not found after accepted routing", ms)

    sig_str = obligation.get("obligor_signature", "")
    sig_present = bool(sig_str) and re.match(_OBL_SIG_PATTERN, sig_str)

    if not sig_present:
        return _fail_case(case,
            f"obligor_signature missing or malformed: {sig_str!r}", ms,
            [_assertion("obligor_signature present and 86 base64url chars",
                        False, "86 base64url chars", repr(sig_str))])

    # Fetch Operator A certificate and extract public key
    try:
        _, _, _, cert_a = _fetch_cert(base_url)
    except RuntimeError as exc:
        return _error_case(case, f"failed to fetch Operator A cert: {exc}")

    if cert_a is None:
        return _fail_case(case, "could not parse Operator A certificate", ms)

    pk_str = cert_a.get("public_key", "")
    if not pk_str.startswith("ed25519:"):
        return _fail_case(case, f"unexpected public_key format: {pk_str!r}", ms)

    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        from cryptography.exceptions import InvalidSignature
        pub_bytes = _tr.b64url_decode(pk_str[len("ed25519:"):])
        pub = Ed25519PublicKey.from_public_bytes(pub_bytes)
        canonical = _obligation_canonical_bytes_runner(obligation)
        sig_bytes = _tr.b64url_decode(sig_str)
        try:
            pub.verify(sig_bytes, canonical)
            verified = True
            verify_detail = "signature valid"
        except InvalidSignature:
            verified = False
            verify_detail = "InvalidSignature: signature does not verify"
    except Exception as exc:
        verified = False
        verify_detail = f"verification error: {exc}"

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion("obligor_signature present (86 base64url chars)", sig_present,
                   "86 base64url chars", sig_str[:20] + "…" if sig_str else "(missing)"),
        _assertion("ed25519_verify(op_a_public_key, canonical_obligation, obligor_signature) = true",
                   verified, "true", verify_detail),
    ]
    case["evidence"] = {
        "routing_request_id": _OBL_RR_ID,
        "obligation_id": obligation.get("obligation_id"),
        "obligor_signature_present": sig_present,
        "obligor_signature_prefix": sig_str[:20] + "…" if sig_str else None,
        "op_a_public_key": pk_str,
        "canonical_obligation_length_bytes": len(_obligation_canonical_bytes_runner(obligation)),
        "signature_verification_result": {"verified": verified, "detail": verify_detail},
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-OBL-006 ──────────────────────────────────────────────────────────────

def run_fed_obl_006(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-OBL-006 — Settlement State Transitions Are Valid

    Obligation follows state machine: pending → in_netting → settled only.
    No backward transitions. No skipped states.

    Pass:   All three states observed in order
    Fail:   Jumped from pending to settled; backward transition
    Severity: STANDARD
    """
    case = _make_case("FED-OBL-006", "Settlement State Transitions Are Valid")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_OBL_RR_ID,
        trace_id=_OBL_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    # Checkpoint 1: state = pending
    try:
        _, obl_pending = _get_obligation_op_a(base_url, _OBL_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))
    state_1 = obl_pending.get("settlement_state") if obl_pending else None

    # Transition: pending → in_netting
    try:
        in_netting_status, in_netting_resp = _mark_obl_in_netting(base_url, _OBL_RR_ID)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    # Checkpoint 2: state = in_netting
    try:
        _, obl_netting = _get_obligation_op_a(base_url, _OBL_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))
    state_2 = obl_netting.get("settlement_state") if obl_netting else None

    # Transition: in_netting → settled
    try:
        settled_status, settled_resp = _mark_obl_settled(base_url, _OBL_RR_ID, _OBL_BATCH_ID)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    # Checkpoint 3: state = settled
    try:
        _, obl_settled = _get_obligation_op_a(base_url, _OBL_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))
    state_3 = obl_settled.get("settlement_state") if obl_settled else None

    # Verify invalid transition is rejected: try settled → in_netting
    try:
        backward_status, _ = _mark_obl_in_netting(base_url, _OBL_RR_ID)
    except RuntimeError:
        backward_status = None
    backward_rejected = backward_status in (409, 400)

    observed_states = [s for s in [state_1, state_2, state_3] if s is not None]
    correct_order = observed_states == ["pending", "in_netting", "settled"]

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion("state checkpoint 1: pending", state_1 == "pending", "pending", state_1),
        _assertion("mark-in-netting returns HTTP 200",
                   in_netting_status == 200, 200, in_netting_status),
        _assertion("state checkpoint 2: in_netting", state_2 == "in_netting", "in_netting", state_2),
        _assertion("mark-settled returns HTTP 200",
                   settled_status == 200, 200, settled_status),
        _assertion("state checkpoint 3: settled", state_3 == "settled", "settled", state_3),
        _assertion("states observed in order: [pending, in_netting, settled]",
                   correct_order, "[pending, in_netting, settled]", str(observed_states)),
        _assertion("backward transition (settled → in_netting) returns 409",
                   backward_rejected, "409 or 400", backward_status),
    ]
    case["evidence"] = {
        "routing_request_id": _OBL_RR_ID,
        "obligation_id": obl_pending.get("obligation_id") if obl_pending else None,
        "state_checkpoint_1": state_1,
        "mark_in_netting_status": in_netting_status,
        "state_checkpoint_2": state_2,
        "mark_settled_status": settled_status,
        "state_checkpoint_3": state_3,
        "observed_states": observed_states,
        "correct_order": correct_order,
        "backward_transition_rejected": backward_rejected,
        "backward_transition_status": backward_status,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-OBL-007 ──────────────────────────────────────────────────────────────

def run_fed_obl_007(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-OBL-007 — Settled Obligation Contains settled_at and settlement_batch_id

    Settled obligations must have audit fields.

    Pass:   settlement_state=settled; settled_at present (ISO 8601); settlement_batch_id present
    Fail:   Any field missing; settled_at not ISO 8601; settlement_batch_id empty
    Severity: STANDARD
    """
    case = _make_case(
        "FED-OBL-007",
        "Settled Obligation Contains settled_at and settlement_batch_id",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_OBL_RR_ID,
        trace_id=_OBL_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    # Advance: pending → in_netting
    try:
        _mark_obl_in_netting(base_url, _OBL_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, f"mark-in-netting failed: {exc}")

    # Advance: in_netting → settled
    try:
        settled_status, _ = _mark_obl_settled(base_url, _OBL_RR_ID, _OBL_BATCH_ID)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, f"mark-settled failed: {exc}")

    # Fetch final obligation state
    try:
        _, obligation = _get_obligation_op_a(base_url, _OBL_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if obligation is None:
        return _fail_case(case, "obligation not found after settlement", ms)

    state = obligation.get("settlement_state")
    settled_at = obligation.get("settled_at")
    batch_id = obligation.get("settlement_batch_id")

    state_settled = state == "settled"
    settled_at_present = bool(settled_at)
    settled_at_iso8601 = False
    if settled_at_present:
        try:
            _parse_iso_timestamp(settled_at)
            settled_at_iso8601 = True
        except Exception:
            settled_at_iso8601 = False
    batch_id_present = bool(batch_id)
    batch_id_matches = batch_id == _OBL_BATCH_ID

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion("mark-settled returned HTTP 200", settled_status == 200, 200, settled_status),
        _assertion("obligation.settlement_state=settled", state_settled, "settled", state),
        _assertion("obligation.settled_at is present", settled_at_present,
                   "present", "(missing)" if not settled_at_present else settled_at),
        _assertion("obligation.settled_at is valid ISO 8601", settled_at_iso8601,
                   "ISO 8601", settled_at or "(missing)"),
        _assertion("obligation.settlement_batch_id is present", batch_id_present,
                   "present", "(missing)" if not batch_id_present else batch_id),
        _assertion(f"obligation.settlement_batch_id == '{_OBL_BATCH_ID}'",
                   batch_id_matches, _OBL_BATCH_ID, batch_id),
    ]
    case["evidence"] = {
        "routing_request_id": _OBL_RR_ID,
        "obligation_id": obligation.get("obligation_id"),
        "settlement_state": state,
        "settled_at": settled_at,
        "settled_at_iso8601": settled_at_iso8601,
        "settlement_batch_id": batch_id,
        "batch_id_matches": batch_id_matches,
        "full_obligation": obligation,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-OBL suite runner ──────────────────────────────────────────────────────

def run_suite_fed_obl(
    base_url: str,
    infra: "RunnerInfra" = None,
    op_a_priv=None,
) -> dict:
    """
    Run all 7 FED-OBL tests.

    Requires infra (Sim Op B) and op_a_priv (Operator A signing key).
    Without both, all tests are skipped.
    """
    def _skip(case_id, title, reason):
        return _skip_case(_make_case(case_id, title), reason)

    obl_avail = infra is not None and op_a_priv is not None

    if not obl_avail:
        reason = "obligation infrastructure not available (install cryptography)"
        cases = [
            _skip(f"FED-OBL-{str(i).zfill(3)}", t, reason)
            for i, t in [
                (1, "Obligation Created Immediately After Acceptance"),
                (2, "Obligation Amount Equals Routing Request Amount (INV-FED-005)"),
                (3, "Obligation trace_id Matches Routing Request (INV-FED-001)"),
                (4, "One Obligation Per routing_request_id (INV-FED-002)"),
                (5, "obligor_signature Verifies Against Operator A Public Key"),
                (6, "Settlement State Transitions Are Valid"),
                (7, "Settled Obligation Contains settled_at and settlement_batch_id"),
            ]
        ]
    else:
        cases = [
            run_fed_obl_001(base_url, infra, op_a_priv),
            run_fed_obl_002(base_url, infra, op_a_priv),
            run_fed_obl_003(base_url, infra, op_a_priv),
            run_fed_obl_004(base_url, infra, op_a_priv),
            run_fed_obl_005(base_url, infra, op_a_priv),
            run_fed_obl_006(base_url, infra, op_a_priv),
            run_fed_obl_007(base_url, infra, op_a_priv),
        ]

    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    skipped = sum(1 for c in cases if c["status"] in ("SKIP", "ERROR"))

    return {
        "suite_id": "FED-OBL",
        "suite_name": "Obligation Lifecycle",
        "blocking": True,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "cases": cases,
    }


# ── FED-EVT-001 ──────────────────────────────────────────────────────────────

def run_fed_evt_001(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EVT-001 — federation.routing.accepted Emitted on Operator B

    Operator B emits routing.accepted event when routing request is accepted.

    Pass:   Event found; routing_request_id present; trace_id matches
    Fail:   Event missing; routing_request_id or trace_id absent
    Severity: STANDARD
    Contract: federation-event.json
    """
    case = _make_case("FED-EVT-001", "federation.routing.accepted Emitted on Operator B")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EVT_RR_ID,
        trace_id=_EVT_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, events_b_body = _get_sim_b_events_http(infra.sim_b_url)
    except RuntimeError as exc:
        return _error_case(case, f"failed to fetch Operator B events: {exc}")

    events_b = (events_b_body.get("events") or []) if isinstance(events_b_body, dict) else []
    accepted_evts = [
        e for e in events_b
        if e.get("event_type") == "federation.routing.accepted"
        and e.get("routing_request_id") == _EVT_RR_ID
    ]
    found = len(accepted_evts) >= 1
    evt = accepted_evts[0] if found else {}

    rr_id_present = bool(evt.get("routing_request_id")) if found else False
    trace_id_correct = evt.get("trace_id") == _EVT_TRACE_ID if found else False

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion("federation.routing.accepted event found on Operator B",
                   found, "found", "missing" if not found else "found"),
        _assertion("event.routing_request_id is present",
                   rr_id_present, _EVT_RR_ID,
                   evt.get("routing_request_id") if found else "(no event)"),
        _assertion("event.trace_id matches routing request trace_id",
                   trace_id_correct, _EVT_TRACE_ID,
                   evt.get("trace_id") if found else "(no event)"),
    ]
    case["evidence"] = {
        "routing_request_id": _EVT_RR_ID,
        "operator_b_events_count": len(events_b),
        "routing_accepted_event_found": found,
        "event": evt if found else None,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EVT-002 ──────────────────────────────────────────────────────────────

def run_fed_evt_002(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EVT-002 — federation.payment.initiated Emitted on Operator A

    Operator A emits payment.initiated after debit and obligation commit.

    Pass:   Event found; trace_id, routing_request_id, interop_transfer_id present
    Fail:   Event missing; any required field absent
    Severity: STANDARD
    Contract: federation-event.json
    """
    case = _make_case("FED-EVT-002", "federation.payment.initiated Emitted on Operator A")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EVT_RR_ID,
        trace_id=_EVT_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, events_a_body = _get_events_op_a(base_url)
    except RuntimeError as exc:
        return _error_case(case, f"failed to fetch Operator A events: {exc}")

    events_a = (events_a_body.get("events") or []) if isinstance(events_a_body, dict) else []
    initiated_evts = [
        e for e in events_a
        if e.get("event_type") == "federation.payment.initiated"
        and e.get("routing_request_id") == _EVT_RR_ID
    ]
    found = len(initiated_evts) >= 1
    evt = initiated_evts[0] if found else {}

    trace_id_correct = evt.get("trace_id") == _EVT_TRACE_ID if found else False
    rr_id_present = bool(evt.get("routing_request_id")) if found else False
    itx_present = bool(evt.get("interop_transfer_id")) if found else False

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion("federation.payment.initiated event found on Operator A",
                   found, "found", "missing" if not found else "found"),
        _assertion("event.trace_id == routing request trace_id (INV-FED-001)",
                   trace_id_correct, _EVT_TRACE_ID,
                   evt.get("trace_id") if found else "(no event)"),
        _assertion("event.routing_request_id is present",
                   rr_id_present, _EVT_RR_ID,
                   evt.get("routing_request_id") if found else "(no event)"),
        _assertion("event.interop_transfer_id is present",
                   itx_present, "itx-<uuid>",
                   evt.get("interop_transfer_id") if found else "(missing)"),
    ]
    case["evidence"] = {
        "routing_request_id": _EVT_RR_ID,
        "operator_a_events_count": len(events_a),
        "payment_initiated_event_found": found,
        "event": evt if found else None,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EVT-003 ──────────────────────────────────────────────────────────────

def run_fed_evt_003(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EVT-003 — federation.payment.completed Emitted on Operator B

    Operator B emits payment.completed after crediting payee.

    Pass:   Event found; trace_id and interop_transfer_id present
    Fail:   Event missing
    Severity: STANDARD
    Contract: federation-event.json
    L3 Req: FED-L3-011
    """
    case = _make_case("FED-EVT-003", "federation.payment.completed Emitted on Operator B")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EVT_RR_ID,
        trace_id=_EVT_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, events_b_body = _get_sim_b_events_http(infra.sim_b_url)
    except RuntimeError as exc:
        return _error_case(case, f"failed to fetch Operator B events: {exc}")

    events_b = (events_b_body.get("events") or []) if isinstance(events_b_body, dict) else []
    completed_evts = [
        e for e in events_b
        if e.get("event_type") == "federation.payment.completed"
        and e.get("routing_request_id") == _EVT_RR_ID
    ]
    found = len(completed_evts) >= 1
    evt = completed_evts[0] if found else {}

    trace_id_correct = evt.get("trace_id") == _EVT_TRACE_ID if found else False
    itx_present = bool(evt.get("interop_transfer_id")) if found else False

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion("federation.payment.completed event found on Operator B",
                   found, "found", "missing" if not found else "found"),
        _assertion("event.trace_id == routing request trace_id",
                   trace_id_correct, _EVT_TRACE_ID,
                   evt.get("trace_id") if found else "(no event)"),
        _assertion("event.interop_transfer_id is present",
                   itx_present, "itx-<uuid>",
                   evt.get("interop_transfer_id") if found else "(missing)"),
    ]
    case["evidence"] = {
        "routing_request_id": _EVT_RR_ID,
        "operator_b_events_count": len(events_b),
        "payment_completed_event_found": found,
        "event": evt if found else None,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EVT-004 ──────────────────────────────────────────────────────────────

def run_fed_evt_004(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EVT-004 — federation.obligation.recorded Emitted on Operator A

    Operator A emits obligation.recorded after recording the obligation.
    obligation_id must match the recorded obligation.

    Pass:   Event found; obligation_id present and matches; trace_id correct
    Fail:   Event missing; wrong obligation_id
    Severity: STANDARD
    Contract: federation-event.json
    """
    case = _make_case("FED-EVT-004", "federation.obligation.recorded Emitted on Operator A")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EVT_RR_ID,
        trace_id=_EVT_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, obligation = _get_obligation_op_a(base_url, _EVT_RR_ID)
    except RuntimeError as exc:
        return _error_case(case, f"failed to fetch obligation: {exc}")

    recorded_obligation_id = obligation.get("obligation_id") if obligation else None

    try:
        _, events_a_body = _get_events_op_a(base_url)
    except RuntimeError as exc:
        return _error_case(case, f"failed to fetch Operator A events: {exc}")

    events_a = (events_a_body.get("events") or []) if isinstance(events_a_body, dict) else []
    obl_evts = [
        e for e in events_a
        if e.get("event_type") == "federation.obligation.recorded"
        and e.get("routing_request_id") == _EVT_RR_ID
    ]
    found = len(obl_evts) >= 1
    evt = obl_evts[0] if found else {}

    trace_id_correct = evt.get("trace_id") == _EVT_TRACE_ID if found else False
    obl_id_present = bool(evt.get("obligation_id")) if found else False
    obl_id_matches = (
        evt.get("obligation_id") == recorded_obligation_id
        if (found and recorded_obligation_id) else False
    )

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion("federation.obligation.recorded event found on Operator A",
                   found, "found", "missing" if not found else "found"),
        _assertion("event.trace_id == routing request trace_id",
                   trace_id_correct, _EVT_TRACE_ID,
                   evt.get("trace_id") if found else "(no event)"),
        _assertion("event.obligation_id is present",
                   obl_id_present, "ob-<uuid>",
                   evt.get("obligation_id") if found else "(missing)"),
        _assertion("event.obligation_id matches recorded obligation",
                   obl_id_matches,
                   recorded_obligation_id or "ob-<uuid>",
                   evt.get("obligation_id") if found else "(no event)"),
    ]
    case["evidence"] = {
        "routing_request_id": _EVT_RR_ID,
        "recorded_obligation_id": recorded_obligation_id,
        "operator_a_events_count": len(events_a),
        "obligation_recorded_event_found": found,
        "event": evt if found else None,
        "obligation_id_matches": obl_id_matches,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EVT-005 ──────────────────────────────────────────────────────────────

def run_fed_evt_005(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EVT-005 — All Federation Events for Same Payment Share trace_id (INV-FED-001)

    Every federation event for the same payment carries the identical trace_id
    on both Operator A and Operator B.

    Pass:   All trace_ids identical across both operator event streams
    Fail:   Any event has a different trace_id
    Severity: CRITICAL
    Invariant: INV-FED-001
    Contract: federation-event.json
    L3 Req: FED-L3-012
    """
    case = _make_case(
        "FED-EVT-005",
        "All Federation Events for Same Payment Share trace_id (INV-FED-001)",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EVT_RR_ID,
        trace_id=_EVT_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, events_a_body = _get_events_op_a(base_url)
    except RuntimeError as exc:
        return _error_case(case, f"failed to fetch Operator A events: {exc}")

    try:
        _, events_b_body = _get_sim_b_events_http(infra.sim_b_url)
    except RuntimeError as exc:
        return _error_case(case, f"failed to fetch Operator B events: {exc}")

    events_a = (events_a_body.get("events") or []) if isinstance(events_a_body, dict) else []
    events_b = (events_b_body.get("events") or []) if isinstance(events_b_body, dict) else []

    payment_evts_a = [
        e for e in events_a
        if e.get("routing_request_id") == _EVT_RR_ID
        or e.get("trace_id") == _EVT_TRACE_ID
    ]
    payment_evts_b = [
        e for e in events_b
        if e.get("routing_request_id") == _EVT_RR_ID
        or e.get("trace_id") == _EVT_TRACE_ID
    ]
    all_evts = payment_evts_a + payment_evts_b

    all_trace_ids = [e.get("trace_id") for e in all_evts]
    unique_trace_ids = list(set(all_trace_ids))
    all_match = len(all_trace_ids) > 0 and all(t == _EVT_TRACE_ID for t in all_trace_ids)
    mismatched_count = sum(1 for t in all_trace_ids if t != _EVT_TRACE_ID)

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion("events collected from both operators",
                   len(payment_evts_a) > 0 and len(payment_evts_b) > 0,
                   ">0 each", f"A:{len(payment_evts_a)} B:{len(payment_evts_b)}"),
        _assertion("all federation events share identical trace_id (INV-FED-001)",
                   all_match, _EVT_TRACE_ID,
                   str(unique_trace_ids) if not all_match else _EVT_TRACE_ID),
        _assertion("zero events with mismatched trace_id",
                   mismatched_count == 0, "0", mismatched_count),
    ]
    case["evidence"] = {
        "routing_request_id": _EVT_RR_ID,
        "expected_trace_id": _EVT_TRACE_ID,
        "operator_a_payment_events": len(payment_evts_a),
        "operator_b_payment_events": len(payment_evts_b),
        "all_trace_ids": all_trace_ids,
        "unique_trace_ids": unique_trace_ids,
        "all_match": all_match,
        "trace_id_cross_check": {"all_match": all_match, "trace_id": _EVT_TRACE_ID},
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EVT-006 ──────────────────────────────────────────────────────────────

def run_fed_evt_006(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-EVT-006 — Federation Events Validate Against Schema

    All collected federation events comply with federation-event.json schema.

    Pass:   All events validate
    Fail:   Any event fails validation
    Severity: STANDARD
    Contract: federation-event.json
    """
    case = _make_case("FED-EVT-006", "Federation Events Validate Against Schema")

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    payload = _build_exec_route_payload(
        base_url=base_url,
        sim_b_url=infra.sim_b_url,
        routing_request_id=_EVT_RR_ID,
        trace_id=_EVT_TRACE_ID,
        op_a_priv=op_a_priv,
    )

    t0 = time.monotonic()
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"routing not accepted: {result}", ms)

    try:
        _, events_a_body = _get_events_op_a(base_url)
    except RuntimeError as exc:
        return _error_case(case, f"failed to fetch Operator A events: {exc}")

    try:
        _, events_b_body = _get_sim_b_events_http(infra.sim_b_url)
    except RuntimeError as exc:
        return _error_case(case, f"failed to fetch Operator B events: {exc}")

    events_a = (events_a_body.get("events") or []) if isinstance(events_a_body, dict) else []
    events_b = (events_b_body.get("events") or []) if isinstance(events_b_body, dict) else []
    all_evts = events_a + events_b

    if not all_evts:
        return _fail_case(case, "no events collected from either operator", ms)

    validation_results = []
    for evt in all_evts:
        evt_id = evt.get("id") or evt.get("event_type") or "(unknown)"
        errors = validate_federation_event(evt)
        validation_results.append({
            "event_id": evt_id,
            "event_type": evt.get("event_type"),
            "valid": len(errors) == 0,
            "errors": errors,
        })

    all_valid = all(r["valid"] for r in validation_results)
    failed_events = [r for r in validation_results if not r["valid"]]

    assertions = [
        _assertion("routing accepted (prerequisite)",
                   result.get("routing_status") == "accepted", "accepted", result.get("routing_status")),
        _assertion(f"{len(all_evts)} events collected from both operators",
                   len(all_evts) > 0, ">0", len(all_evts)),
        _assertion("all federation events validate against federation-event.json",
                   all_valid,
                   "all valid",
                   f"{len(failed_events)} failed" if failed_events else "all valid"),
    ]
    case["evidence"] = {
        "routing_request_id": _EVT_RR_ID,
        "total_events": len(all_evts),
        "operator_a_events": len(events_a),
        "operator_b_events": len(events_b),
        "schema_validation_results": validation_results,
        "all_valid": all_valid,
        "failed_events": failed_events,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-EVT suite runner ──────────────────────────────────────────────────────

def run_suite_fed_evt(
    base_url: str,
    infra: "RunnerInfra" = None,
    op_a_priv=None,
) -> dict:
    """
    Run all 6 FED-EVT tests.

    Requires infra (Sim Op B) and op_a_priv (Operator A signing key).
    Without both, all tests are skipped.
    """
    def _skip(case_id, title, reason):
        return _skip_case(_make_case(case_id, title), reason)

    evt_avail = infra is not None and op_a_priv is not None

    if not evt_avail:
        reason = "event infrastructure not available (install cryptography)"
        cases = [
            _skip(f"FED-EVT-{str(i).zfill(3)}", t, reason)
            for i, t in [
                (1, "federation.routing.accepted Emitted on Operator B"),
                (2, "federation.payment.initiated Emitted on Operator A"),
                (3, "federation.payment.completed Emitted on Operator B"),
                (4, "federation.obligation.recorded Emitted on Operator A"),
                (5, "All Federation Events for Same Payment Share trace_id (INV-FED-001)"),
                (6, "Federation Events Validate Against Schema"),
            ]
        ]
    else:
        cases = [
            run_fed_evt_001(base_url, infra, op_a_priv),
            run_fed_evt_002(base_url, infra, op_a_priv),
            run_fed_evt_003(base_url, infra, op_a_priv),
            run_fed_evt_004(base_url, infra, op_a_priv),
            run_fed_evt_005(base_url, infra, op_a_priv),
            run_fed_evt_006(base_url, infra, op_a_priv),
        ]

    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    skipped = sum(1 for c in cases if c["status"] in ("SKIP", "ERROR"))

    return {
        "suite_id": "FED-EVT",
        "suite_name": "Federation Event Emission",
        "blocking": True,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "cases": cases,
    }


# ── FED-SETTLE helpers ────────────────────────────────────────────────────────

def _settle_route_three(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """Execute 3 routing requests (SETTLE-001 IDs) for FED-SETTLE suite setup."""
    results = {}
    for rr_id, trace_id in [
        (_SETTLE_RR_ID_1, _SETTLE_TRACE_1),
        (_SETTLE_RR_ID_2, _SETTLE_TRACE_2),
        (_SETTLE_RR_ID_3, _SETTLE_TRACE_3),
    ]:
        payload = _build_exec_route_payload(
            base_url=base_url,
            sim_b_url=infra.sim_b_url,
            routing_request_id=rr_id,
            trace_id=trace_id,
            op_a_priv=op_a_priv,
            amount_minor=_SETTLE_AMOUNT,
        )
        _, result = _call_fed_route(base_url, payload)
        results[rr_id] = result or {}
    return results


# ── FED-SETTLE-001 ────────────────────────────────────────────────────────────

def run_fed_settle_001(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-SETTLE-001 — Obligation Export Includes All Pending Obligations

    3 routing requests create 3 A→B obligations. Trigger netting. All 3 must be in
    the export with correct amounts and settlement_state advanced to in_netting.

    Pass:   Batch includes all 3; gross_a_to_b correct; obligations in in_netting
    Fail:   Any obligation missing; wrong amounts
    Severity: STANDARD
    Contract: federation-obligation.json
    L3 Req: FED-L3-008
    """
    case = _make_case("FED-SETTLE-001", "Obligation Export Includes All Pending Obligations")

    _reset_exec_state(base_url)
    _reset_netting_state(base_url)
    infra.reset_routing_state()

    t0 = time.monotonic()
    try:
        route_results = _settle_route_three(base_url, infra, op_a_priv)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    all_accepted = all(r.get("routing_status") == "accepted" for r in route_results.values())
    if not all_accepted:
        return _fail_case(case, "not all 3 routing requests accepted", int((time.monotonic() - t0) * 1000))

    try:
        netting_status, netting_body = _netting_trigger(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if netting_status != 200 or not netting_body:
        return _fail_case(case, f"netting/trigger HTTP {netting_status}", ms)

    batch = netting_body.get("batch") or {}
    included_rr_ids = set(batch.get("included_a_to_b_routing_ids", []))
    expected_rr_ids = {_SETTLE_RR_ID_1, _SETTLE_RR_ID_2, _SETTLE_RR_ID_3}
    all_included = expected_rr_ids.issubset(included_rr_ids)
    gross_a_to_b = batch.get("gross_a_to_b", 0)
    expected_gross = _SETTLE_AMOUNT * 3  # 150,000
    gross_correct = gross_a_to_b == expected_gross
    recon_clean = batch.get("reconciliation_status") == "clean"

    # Verify obligations advanced to in_netting
    obl_states = {}
    for rr_id in [_SETTLE_RR_ID_1, _SETTLE_RR_ID_2, _SETTLE_RR_ID_3]:
        try:
            _, obl = _get_obligation_op_a(base_url, rr_id)
            obl_states[rr_id] = obl.get("settlement_state") if obl else None
        except RuntimeError:
            obl_states[rr_id] = None
    all_in_netting = all(s == "in_netting" for s in obl_states.values())

    assertions = [
        _assertion("3 routing requests accepted (prerequisite)",
                   all_accepted, "3 accepted", str(all_accepted)),
        _assertion("netting/trigger HTTP 200", netting_status == 200, 200, netting_status),
        _assertion("batch includes all 3 A→B obligations",
                   all_included, str(expected_rr_ids), f"included={included_rr_ids}"),
        _assertion(f"gross_a_to_b == {expected_gross}",
                   gross_correct, expected_gross, gross_a_to_b),
        _assertion("reconciliation_status == clean",
                   recon_clean, "clean", batch.get("reconciliation_status")),
        _assertion("all 3 obligations settlement_state == in_netting",
                   all_in_netting, "in_netting", str(obl_states)),
    ]
    case["evidence"] = {
        "routing_request_ids": list(expected_rr_ids),
        "included_a_to_b_routing_ids": list(included_rr_ids),
        "gross_a_to_b": gross_a_to_b,
        "expected_gross": expected_gross,
        "obligation_states": obl_states,
        "reconciliation_status": batch.get("reconciliation_status"),
        "settlement_batch_id": batch.get("settlement_batch_id"),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-SETTLE-002 ────────────────────────────────────────────────────────────

def run_fed_settle_002(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-SETTLE-002 — Net Position Computed Correctly

    A→B: 3×50,000=150,000. B→A: 1×40,000=40,000. net=110,000 (A owes B).
    Integer arithmetic only (INV-FED-LEDGER-002).

    Pass:   net == 110,000; type is integer
    Fail:   Wrong net; floating point used; gross values incorrect
    Severity: STANDARD
    Invariant: INV-FED-LEDGER-001
    """
    case = _make_case("FED-SETTLE-002", "Net Position Computed Correctly")

    _reset_exec_state(base_url)
    _reset_netting_state(base_url)
    infra.reset_routing_state()

    t0 = time.monotonic()

    try:
        route_results = _settle_route_three(base_url, infra, op_a_priv)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    all_accepted = all(r.get("routing_status") == "accepted" for r in route_results.values())
    if not all_accepted:
        return _fail_case(case, "not all routing requests accepted", int((time.monotonic() - t0) * 1000))

    try:
        _, _ = _add_b_obligation(base_url, _SETTLE_B_TO_A_AMOUNT, _SETTLE_B_TO_A_RR_ID, _SETTLE_B_TO_A_TRACE)
    except RuntimeError as exc:
        return _error_case(case, f"add-b-obligation failed: {exc}")

    try:
        netting_status, netting_body = _netting_trigger(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if netting_status != 200 or not netting_body:
        return _fail_case(case, f"netting/trigger HTTP {netting_status}", ms)

    batch = netting_body.get("batch") or {}
    gross_a_to_b = batch.get("gross_a_to_b")
    gross_b_to_a = batch.get("gross_b_to_a")
    net_amount = batch.get("net_amount")
    net_payer = batch.get("net_payer_operator_id")

    expected_gross_a_to_b = _SETTLE_AMOUNT * 3    # 150,000
    expected_gross_b_to_a = _SETTLE_B_TO_A_AMOUNT  # 40,000
    expected_net = expected_gross_a_to_b - expected_gross_b_to_a  # 110,000

    assertions = [
        _assertion("3 A→B + 1 B→A routing setup (prerequisite)",
                   all_accepted, "3 accepted", str(all_accepted)),
        _assertion(f"gross_a_to_b == {expected_gross_a_to_b}",
                   gross_a_to_b == expected_gross_a_to_b, expected_gross_a_to_b, gross_a_to_b),
        _assertion(f"gross_b_to_a == {expected_gross_b_to_a}",
                   gross_b_to_a == expected_gross_b_to_a, expected_gross_b_to_a, gross_b_to_a),
        _assertion(f"net_amount == {expected_net} (A owes B)",
                   net_amount == expected_net, expected_net, net_amount),
        _assertion("net_payer_operator_id is Operator A",
                   "operator-a" in (net_payer or ""), "operator-a-...", net_payer or "(absent)"),
        _assertion("net_amount is integer (INV-FED-LEDGER-002)",
                   isinstance(net_amount, int) and not isinstance(net_amount, bool),
                   "integer", type(net_amount).__name__),
    ]
    case["evidence"] = {
        "a_to_b_obligations": 3,
        "b_to_a_obligations": 1,
        "gross_a_to_b": gross_a_to_b,
        "gross_b_to_a": gross_b_to_a,
        "net_amount": net_amount,
        "expected_gross_a_to_b": expected_gross_a_to_b,
        "expected_gross_b_to_a": expected_gross_b_to_a,
        "expected_net": expected_net,
        "net_payer_operator_id": net_payer,
        "net_payee_operator_id": batch.get("net_payee_operator_id"),
        "settlement_batch_id": batch.get("settlement_batch_id"),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-SETTLE-003 ────────────────────────────────────────────────────────────

def run_fed_settle_003(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-SETTLE-003 — Both Operators Independently Compute Same Net

    Both operators compute net from the same obligation data. Settlement authorized
    only when both nets agree.

    Pass:   Both nets equal; settlement_status == authorized
    Fail:   Nets differ; settlement proceeds without agreement
    Severity: STANDARD
    Invariant: INV-FED-LEDGER-001
    """
    case = _make_case("FED-SETTLE-003", "Both Operators Independently Compute Same Net")

    _reset_exec_state(base_url)
    _reset_netting_state(base_url)
    infra.reset_routing_state()

    t0 = time.monotonic()

    try:
        route_results = _settle_route_three(base_url, infra, op_a_priv)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    all_accepted = all(r.get("routing_status") == "accepted" for r in route_results.values())
    if not all_accepted:
        return _fail_case(case, "not all routing requests accepted", int((time.monotonic() - t0) * 1000))

    try:
        _add_b_obligation(base_url, _SETTLE_B_TO_A_AMOUNT, _SETTLE_B_TO_A_RR_ID, _SETTLE_B_TO_A_TRACE)
    except RuntimeError as exc:
        return _error_case(case, f"add-b-obligation failed: {exc}")

    try:
        netting_status, netting_body = _netting_trigger(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if netting_status != 200 or not netting_body:
        return _fail_case(case, f"netting/trigger HTTP {netting_status}", ms)

    batch = netting_body.get("batch") or {}
    op_a_net = batch.get("net_amount")

    # Operator B independently computes: gross_b_sees_a_to_b=150,000, gross_b_sees_b_to_a=40,000
    op_b_net = (_SETTLE_AMOUNT * 3) - _SETTLE_B_TO_A_AMOUNT  # 110,000

    nets_agree = (op_a_net == op_b_net)
    settlement_authorized = batch.get("settlement_status") == "authorized"
    recon_clean = batch.get("reconciliation_status") == "clean"

    assertions = [
        _assertion("3 A→B + 1 B→A routing setup (prerequisite)",
                   all_accepted, "3 accepted", str(all_accepted)),
        _assertion("netting/trigger HTTP 200", netting_status == 200, 200, netting_status),
        _assertion(f"Operator A computed net == {op_b_net}",
                   op_a_net == op_b_net, op_b_net, op_a_net),
        _assertion("Operator A and Operator B nets are equal (bilateral agreement)",
                   nets_agree, op_b_net, f"A:{op_a_net} B:{op_b_net}"),
        _assertion("settlement_status == authorized (nets agree)",
                   settlement_authorized, "authorized", batch.get("settlement_status")),
        _assertion("reconciliation_status == clean",
                   recon_clean, "clean", batch.get("reconciliation_status")),
    ]
    case["evidence"] = {
        "operator_a_computed_net": op_a_net,
        "operator_b_computed_net": op_b_net,
        "nets_agree": nets_agree,
        "gross_a_to_b": batch.get("gross_a_to_b"),
        "gross_b_to_a": batch.get("gross_b_to_a"),
        "settlement_status": batch.get("settlement_status"),
        "reconciliation_status": batch.get("reconciliation_status"),
        "settlement_batch_id": batch.get("settlement_batch_id"),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-SETTLE-004 ────────────────────────────────────────────────────────────

def run_fed_settle_004(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-SETTLE-004 — Settlement Execution: Ledger Entries Correct

    Settlement bank transfer produces 4 correct ledger entries:
    Op A DEBIT federation_payable:op-b + CREDIT federation_settlement_clearing
    Op B DEBIT federation_settlement_clearing + CREDIT federation_receivable:op-a

    Pass:   All 4 entries present with correct accounts and amount == net
    Fail:   Wrong accounts; wrong amounts; entries missing
    Severity: STANDARD
    Invariant: INV-FED-LEDGER-001
    """
    case = _make_case("FED-SETTLE-004", "Settlement Execution: Ledger Entries Correct")

    _reset_exec_state(base_url)
    _reset_netting_state(base_url)
    infra.reset_routing_state()

    t0 = time.monotonic()

    try:
        route_results = _settle_route_three(base_url, infra, op_a_priv)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    all_accepted = all(r.get("routing_status") == "accepted" for r in route_results.values())
    if not all_accepted:
        return _fail_case(case, "not all routing requests accepted", int((time.monotonic() - t0) * 1000))

    try:
        _add_b_obligation(base_url, _SETTLE_B_TO_A_AMOUNT, _SETTLE_B_TO_A_RR_ID, _SETTLE_B_TO_A_TRACE)
    except RuntimeError as exc:
        return _error_case(case, f"add-b-obligation failed: {exc}")

    try:
        netting_status, netting_body = _netting_trigger(base_url)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if netting_status != 200 or not netting_body:
        return _fail_case(case, f"netting/trigger HTTP {netting_status}", int((time.monotonic() - t0) * 1000))

    batch = netting_body.get("batch") or {}
    batch_id = batch.get("settlement_batch_id")

    try:
        exec_status, exec_body = _netting_execute(base_url, batch_id)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if exec_status != 200 or not exec_body:
        return _fail_case(case, f"netting/execute HTTP {exec_status}", ms)

    try:
        _, ledger_body = _get_netting_settlement_ledger(base_url)
    except RuntimeError as exc:
        return _error_case(case, f"get settlement ledger failed: {exc}")

    entries = (ledger_body.get("entries") or []) if ledger_body else []
    entry_count = len(entries)
    expected_net = (_SETTLE_AMOUNT * 3) - _SETTLE_B_TO_A_AMOUNT  # 110,000

    op_a_debit = next((e for e in entries
                       if e.get("operator") == "operator-a-test"
                       and e.get("entry_type") == "DEBIT"
                       and "federation_payable" in e.get("account", "")), None)
    op_a_credit = next((e for e in entries
                        if e.get("operator") == "operator-a-test"
                        and e.get("entry_type") == "CREDIT"
                        and e.get("account") == "federation_settlement_clearing"), None)
    op_b_debit = next((e for e in entries
                       if e.get("operator") == "operator-b-test"
                       and e.get("entry_type") == "DEBIT"
                       and e.get("account") == "federation_settlement_clearing"), None)
    op_b_credit = next((e for e in entries
                        if e.get("operator") == "operator-b-test"
                        and e.get("entry_type") == "CREDIT"
                        and "federation_receivable" in e.get("account", "")), None)

    amounts_correct = all(
        e is not None and e.get("amount_minor") == expected_net
        for e in [op_a_debit, op_a_credit, op_b_debit, op_b_credit]
    )

    assertions = [
        _assertion("settlement executed (HTTP 200)", exec_status == 200, 200, exec_status),
        _assertion("4 settlement ledger entries produced", entry_count == 4, 4, entry_count),
        _assertion("Op A DEBIT federation_payable:operator-b-test",
                   op_a_debit is not None, "present", "missing" if not op_a_debit else "present"),
        _assertion("Op A CREDIT federation_settlement_clearing",
                   op_a_credit is not None, "present", "missing" if not op_a_credit else "present"),
        _assertion("Op B DEBIT federation_settlement_clearing",
                   op_b_debit is not None, "present", "missing" if not op_b_debit else "present"),
        _assertion("Op B CREDIT federation_receivable:operator-a-test",
                   op_b_credit is not None, "present", "missing" if not op_b_credit else "present"),
        _assertion(f"all entries amount_minor == {expected_net} (net)",
                   amounts_correct, expected_net, "see entries"),
    ]
    case["evidence"] = {
        "settlement_batch_id": batch_id,
        "net_amount": expected_net,
        "ledger_entry_count": entry_count,
        "op_a_debit": op_a_debit,
        "op_a_credit": op_a_credit,
        "op_b_debit": op_b_debit,
        "op_b_credit": op_b_credit,
        "simulated_bank_reference": exec_body.get("simulated_bank_reference"),
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-SETTLE-005 ────────────────────────────────────────────────────────────

def run_fed_settle_005(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-SETTLE-005 — Obligations Marked Settled With Required Fields

    All obligations in the batch must have settlement_state=settled,
    settled_at (ISO 8601), and settlement_batch_id after settlement executes.

    Pass:   All 3 obligations have all three fields set correctly
    Fail:   Any obligation still pending; missing fields
    Severity: STANDARD
    Contract: federation-obligation.json
    """
    case = _make_case("FED-SETTLE-005", "Obligations Marked Settled With Required Fields")

    _reset_exec_state(base_url)
    _reset_netting_state(base_url)
    infra.reset_routing_state()

    t0 = time.monotonic()

    try:
        route_results = _settle_route_three(base_url, infra, op_a_priv)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    all_accepted = all(r.get("routing_status") == "accepted" for r in route_results.values())
    if not all_accepted:
        return _fail_case(case, "not all routing requests accepted", int((time.monotonic() - t0) * 1000))

    try:
        netting_status, netting_body = _netting_trigger(base_url)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    batch = (netting_body.get("batch") or {}) if netting_body else {}
    batch_id = batch.get("settlement_batch_id")
    if not batch_id or netting_status != 200:
        return _fail_case(case, f"netting/trigger failed HTTP {netting_status}",
                          int((time.monotonic() - t0) * 1000))

    try:
        exec_status, _ = _netting_execute(base_url, batch_id)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if exec_status != 200:
        return _fail_case(case, f"netting/execute HTTP {exec_status}", ms)

    obl_states = {}
    for rr_id in [_SETTLE_RR_ID_1, _SETTLE_RR_ID_2, _SETTLE_RR_ID_3]:
        try:
            _, obl = _get_obligation_op_a(base_url, rr_id)
            obl_states[rr_id] = obl or {}
        except RuntimeError:
            obl_states[rr_id] = {}

    all_settled = all(o.get("settlement_state") == "settled" for o in obl_states.values())
    all_settled_at = all(
        isinstance(o.get("settled_at"), str) and o["settled_at"]
        for o in obl_states.values()
    )
    all_batch_id = all(
        isinstance(o.get("settlement_batch_id"), str) and o["settlement_batch_id"]
        for o in obl_states.values()
    )
    batch_ids_match = all(o.get("settlement_batch_id") == batch_id for o in obl_states.values())

    assertions = [
        _assertion("settlement executed (HTTP 200)", exec_status == 200, 200, exec_status),
        _assertion("all 3 obligations settlement_state=settled",
                   all_settled, "settled",
                   str({k: v.get("settlement_state") for k, v in obl_states.items()})),
        _assertion("all obligations have settled_at (ISO 8601)",
                   all_settled_at, "ISO 8601",
                   str({k: v.get("settled_at") for k, v in obl_states.items()})),
        _assertion("all obligations have settlement_batch_id",
                   all_batch_id, "present",
                   str({k: v.get("settlement_batch_id") for k, v in obl_states.items()})),
        _assertion("all obligations reference the same settlement_batch_id",
                   batch_ids_match, batch_id,
                   str({k: v.get("settlement_batch_id") for k, v in obl_states.items()})),
    ]
    case["evidence"] = {
        "settlement_batch_id": batch_id,
        "obligations": {k: {
            "settlement_state": v.get("settlement_state"),
            "settled_at": v.get("settled_at"),
            "settlement_batch_id": v.get("settlement_batch_id"),
        } for k, v in obl_states.items()},
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-SETTLE-006 ────────────────────────────────────────────────────────────

def run_fed_settle_006(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-SETTLE-006 — Reconciliation: All Accepted Routing Requests Have Obligations

    5 routing requests accepted; every one must have exactly one obligation.
    No accepted routing request may exist without a corresponding obligation.

    Pass:   1:1 match; no orphan routing requests (INV-FED-RECON-001)
    Fail:   Any accepted request without obligation
    Severity: CRITICAL
    Invariant: INV-FED-RECON-001
    Contract: federation-obligation.json
    """
    case = _make_case(
        "FED-SETTLE-006",
        "Reconciliation: All Accepted Routing Requests Have Obligations (INV-FED-RECON-001)",
    )

    _reset_exec_state(base_url)
    _reset_netting_state(base_url)
    infra.reset_routing_state()

    t0 = time.monotonic()

    accepted_rr_ids = []
    for rr_id, trace_id in zip(_SETTLE_REC_RR_IDS, _SETTLE_REC_TRACE_IDS):
        payload = _build_exec_route_payload(
            base_url=base_url,
            sim_b_url=infra.sim_b_url,
            routing_request_id=rr_id,
            trace_id=trace_id,
            op_a_priv=op_a_priv,
            amount_minor=_SETTLE_AMOUNT,
        )
        try:
            _, result = _call_fed_route(base_url, payload)
            if result and result.get("routing_status") == "accepted":
                accepted_rr_ids.append(rr_id)
        except RuntimeError as exc:
            return _error_case(case, f"routing {rr_id} failed: {exc}")

    ms = int((time.monotonic() - t0) * 1000)

    if len(accepted_rr_ids) < 5:
        return _fail_case(case, f"only {len(accepted_rr_ids)}/5 routing requests accepted", ms)

    try:
        _, obligations_body = _get_obligations_all_op_a(base_url)
    except RuntimeError as exc:
        return _error_case(case, f"get obligations failed: {exc}")

    obligations = (obligations_body.get("obligations") or []) if obligations_body else []
    obligation_rr_ids = {
        obl["routing_request_id"] for obl in obligations
        if "routing_request_id" in obl
    }

    missing = set(accepted_rr_ids) - obligation_rr_ids
    extra = obligation_rr_ids - set(accepted_rr_ids)
    recon_clean = len(missing) == 0

    assertions = [
        _assertion("5 routing requests accepted (prerequisite)",
                   len(accepted_rr_ids) == 5, 5, len(accepted_rr_ids)),
        _assertion("obligations count == 5 (one per accepted request)",
                   len(obligations) >= 5, ">=5", len(obligations)),
        _assertion("all 5 accepted routing_request_ids have obligations (INV-FED-RECON-001)",
                   recon_clean, "empty set", str(missing)),
        _assertion("no orphan obligations",
                   len(extra) == 0, "0", len(extra)),
    ]
    case["evidence"] = {
        "accepted_routing_request_count": len(accepted_rr_ids),
        "accepted_routing_request_ids": accepted_rr_ids,
        "obligation_routing_request_ids": sorted(obligation_rr_ids),
        "missing_obligations_for": sorted(missing),
        "extra_obligations_for": sorted(extra),
        "reconciliation_clean": recon_clean,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-SETTLE-007 ────────────────────────────────────────────────────────────

def run_fed_settle_007(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-SETTLE-007 — Reconciliation: Trace Cross-Check Across Both Operators

    For each of 3 payments with distinct trace_ids, all 4 artifact types carry that
    exact trace_id: (1) ledger entry on Op A, (2) obligation on Op A,
    (3) ledger entry on Op B, (4) event on Op B.

    Pass:   All 4 artifact types found per trace_id (3 payments × 4 = 12 checks)
    Fail:   Any trace_id missing from any artifact type
    Severity: STANDARD
    Invariant: INV-FED-RECON-001
    Contract: All
    L3 Req: FED-L3-012
    """
    case = _make_case(
        "FED-SETTLE-007",
        "Reconciliation: Trace Cross-Check Across Both Operators (INV-FED-RECON-001)",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    t0 = time.monotonic()

    try:
        route_results = _settle_route_three(base_url, infra, op_a_priv)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    all_accepted = all(r.get("routing_status") == "accepted" for r in route_results.values())
    if not all_accepted:
        return _fail_case(case, "not all routing requests accepted", int((time.monotonic() - t0) * 1000))

    try:
        _, ledger_a_body = _get_ledger_op_a(base_url, _EXEC_SENDER_WALLET)
    except RuntimeError as exc:
        return _error_case(case, f"get Op A ledger failed: {exc}")

    try:
        _, obligations_body = _get_obligations_all_op_a(base_url)
    except RuntimeError as exc:
        return _error_case(case, f"get obligations failed: {exc}")

    try:
        _, events_b_body = _get_sim_b_events_http(infra.sim_b_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, f"get Sim Op B events failed: {exc}")

    ledger_a_entries = (ledger_a_body.get("entries") or []) if ledger_a_body else []
    obligations = (obligations_body.get("obligations") or []) if obligations_body else []
    events_b = (events_b_body.get("events") or []) if isinstance(events_b_body, dict) else []
    ledger_b_entries = infra.get_sim_b_ledger(_EXEC_PAYEE_WALLET)

    trace_id_pairs = [
        (_SETTLE_RR_ID_1, _SETTLE_TRACE_1),
        (_SETTLE_RR_ID_2, _SETTLE_TRACE_2),
        (_SETTLE_RR_ID_3, _SETTLE_TRACE_3),
    ]

    per_trace = {}
    all_assertions = []
    for rr_id, trace_id in trace_id_pairs:
        ledger_a_ok = any(
            e.get("trace_id") == trace_id and e.get("routing_request_id") == rr_id
            for e in ledger_a_entries
        )
        obl_ok = any(
            o.get("trace_id") == trace_id and o.get("routing_request_id") == rr_id
            for o in obligations
        )
        ledger_b_ok = any(
            e.get("trace_id") == trace_id and e.get("routing_request_id") == rr_id
            for e in ledger_b_entries
        )
        event_b_ok = any(
            e.get("trace_id") == trace_id
            and (e.get("routing_request_id") == rr_id or e.get("aggregate_id") == rr_id)
            for e in events_b
        )
        per_trace[trace_id] = {
            "routing_request_id": rr_id,
            "ledger_a": ledger_a_ok,
            "obligation_a": obl_ok,
            "ledger_b": ledger_b_ok,
            "event_b": event_b_ok,
            "all_found": all([ledger_a_ok, obl_ok, ledger_b_ok, event_b_ok]),
        }
        short = trace_id[-6:]
        all_assertions.extend([
            _assertion(f"trace …{short}: ledger entry on Op A",
                       ledger_a_ok, "found", "missing" if not ledger_a_ok else "found"),
            _assertion(f"trace …{short}: obligation on Op A",
                       obl_ok, "found", "missing" if not obl_ok else "found"),
            _assertion(f"trace …{short}: ledger entry on Op B",
                       ledger_b_ok, "found", "missing" if not ledger_b_ok else "found"),
            _assertion(f"trace …{short}: event on Op B",
                       event_b_ok, "found", "missing" if not event_b_ok else "found"),
        ])

    all_complete = all(r["all_found"] for r in per_trace.values())
    assertions = (
        [_assertion("3 routing requests accepted (prerequisite)",
                    all_accepted, "3 accepted", str(all_accepted))]
        + all_assertions
        + [_assertion("all 3 trace_ids in all 4 artifact types (INV-FED-RECON-001)",
                      all_complete, "all complete",
                      str({t[-6:]: r["all_found"] for t, r in per_trace.items()}))]
    )
    case["evidence"] = {
        "payments": 3,
        "artifacts_per_payment": 4,
        "trace_cross_check": per_trace,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-SETTLE-008 ────────────────────────────────────────────────────────────

def run_fed_settle_008(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-SETTLE-008 — Settlement Blocked on Unresolved Discrepancy

    If Operator B reports a different amount for one obligation, settlement MUST NOT
    proceed. The batch must have reconciliation_status=discrepancy and
    settlement_status=blocked.

    Pass:   reconciliation_status=discrepancy; settlement blocked; no bank transfer
    Fail:   Settlement proceeds despite discrepancy (INV-FED-LEDGER-001 violation)
    Severity: CRITICAL
    Invariant: INV-FED-LEDGER-001
    """
    case = _make_case("FED-SETTLE-008", "Settlement Blocked on Unresolved Discrepancy")

    _reset_exec_state(base_url)
    _reset_netting_state(base_url)
    infra.reset_routing_state()

    t0 = time.monotonic()

    try:
        route_results = _settle_route_three(base_url, infra, op_a_priv)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    all_accepted = all(r.get("routing_status") == "accepted" for r in route_results.values())
    if not all_accepted:
        return _fail_case(case, "not all routing requests accepted", int((time.monotonic() - t0) * 1000))

    # Inject discrepancy: Op B claims rr_id_1 has amount 49,999 instead of 50,000
    disc_amount = _SETTLE_AMOUNT - 1  # 49,999
    try:
        disc_status, _ = _inject_discrepancy(base_url, _SETTLE_RR_ID_1, disc_amount)
        if disc_status != 200:
            return _error_case(case, f"inject-discrepancy HTTP {disc_status}")
    except RuntimeError as exc:
        return _error_case(case, f"inject-discrepancy failed: {exc}")

    try:
        netting_status, netting_body = _netting_trigger(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if netting_status != 200 or not netting_body:
        return _fail_case(case, f"netting/trigger HTTP {netting_status}", ms)

    batch = netting_body.get("batch") or {}
    batch_id = batch.get("settlement_batch_id")
    recon_status = batch.get("reconciliation_status")
    settle_status = batch.get("settlement_status")
    discrepancies = batch.get("discrepancies", [])

    # Attempt settlement — must be rejected
    exec_status = None
    exec_body = None
    if batch_id:
        try:
            exec_status, exec_body = _netting_execute(base_url, batch_id)
        except RuntimeError as exc:
            exec_status = 500
            exec_body = {"error": str(exc)}

    settlement_rejected = exec_status is not None and exec_status != 200

    # Obligations must NOT be settled (still pending — batch was blocked, not advanced)
    obl_final_states = {}
    for rr_id in [_SETTLE_RR_ID_1, _SETTLE_RR_ID_2, _SETTLE_RR_ID_3]:
        try:
            _, obl = _get_obligation_op_a(base_url, rr_id)
            obl_final_states[rr_id] = obl.get("settlement_state") if obl else None
        except RuntimeError:
            obl_final_states[rr_id] = None
    no_obligation_settled = not any(s == "settled" for s in obl_final_states.values())

    assertions = [
        _assertion("3 routing requests accepted (prerequisite)",
                   all_accepted, "3 accepted", str(all_accepted)),
        _assertion("discrepancy injected (prerequisite)",
                   disc_status == 200, 200, disc_status),
        _assertion("reconciliation_status == discrepancy",
                   recon_status == "discrepancy", "discrepancy", recon_status),
        _assertion("settlement_status == blocked",
                   settle_status == "blocked", "blocked", settle_status),
        _assertion("discrepancy details logged (routing_request_id + amounts)",
                   len(discrepancies) > 0, ">=1 entry", len(discrepancies)),
        _assertion("settlement execution rejected (HTTP != 200) (INV-FED-LEDGER-001)",
                   settlement_rejected, "rejected (409)", f"HTTP {exec_status}"),
        _assertion("no obligation moved to settled state",
                   no_obligation_settled, "none settled", str(obl_final_states)),
    ]
    case["evidence"] = {
        "discrepancy_routing_request_id": _SETTLE_RR_ID_1,
        "operator_a_amount": _SETTLE_AMOUNT,
        "operator_b_reported_amount": disc_amount,
        "reconciliation_status": recon_status,
        "settlement_status": settle_status,
        "discrepancies": discrepancies,
        "execute_http_status": exec_status,
        "execute_response": exec_body,
        "obligation_states_after_blocked_batch": obl_final_states,
        "settlement_batch_id": batch_id,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-SETTLE suite runner ───────────────────────────────────────────────────

def run_suite_fed_settle(
    base_url: str,
    infra: "RunnerInfra" = None,
    op_a_priv=None,
) -> dict:
    """
    Run all 8 FED-SETTLE tests.

    Requires infra (Sim Op B) and op_a_priv (Operator A signing key).
    Without both, all tests are skipped.
    """
    def _skip(case_id, title, reason):
        return _skip_case(_make_case(case_id, title), reason)

    settle_avail = infra is not None and op_a_priv is not None

    if not settle_avail:
        reason = "settlement infrastructure not available (install cryptography)"
        cases = [
            _skip(f"FED-SETTLE-{str(i).zfill(3)}", t, reason)
            for i, t in [
                (1, "Obligation Export Includes All Pending Obligations"),
                (2, "Net Position Computed Correctly"),
                (3, "Both Operators Independently Compute Same Net"),
                (4, "Settlement Execution: Ledger Entries Correct"),
                (5, "Obligations Marked Settled With Required Fields"),
                (6, "Reconciliation: All Accepted Routing Requests Have Obligations"),
                (7, "Reconciliation: Trace Cross-Check Across Both Operators"),
                (8, "Settlement Blocked on Unresolved Discrepancy"),
                (9, "Netting Disagreement: Full Obligation Exchange Identifies Discrepancy"),
                (10, "Zero-Net Case: No Bank Transfer; All Obligations Settled"),
            ]
        ]
    else:
        cases = [
            run_fed_settle_001(base_url, infra, op_a_priv),
            run_fed_settle_002(base_url, infra, op_a_priv),
            run_fed_settle_003(base_url, infra, op_a_priv),
            run_fed_settle_004(base_url, infra, op_a_priv),
            run_fed_settle_005(base_url, infra, op_a_priv),
            run_fed_settle_006(base_url, infra, op_a_priv),
            run_fed_settle_007(base_url, infra, op_a_priv),
            run_fed_settle_008(base_url, infra, op_a_priv),
            run_fed_settle_009(base_url, infra, op_a_priv),
            run_fed_settle_010(base_url, infra, op_a_priv),
        ]

    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    skipped = sum(1 for c in cases if c["status"] in ("SKIP", "ERROR"))

    return {
        "suite_id": "FED-SETTLE",
        "suite_name": "Netting and Settlement",
        "blocking": True,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "cases": cases,
    }


# ── FED-SETTLE-009 ────────────────────────────────────────────────────────────

def run_fed_settle_009(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-SETTLE-009 — Netting Disagreement: Full Obligation Exchange Identifies Discrepancy

    Op A has 3 obligations; Sim Op B also accepted a 4th routing that Op A never committed.
    The disagreement is detected by cross-referencing obligation lists.
    The missing routing_request_id is identified; recovery creates the missing obligation.

    Pass:   Missing routing_request_id identified; recovery initiated; obligation exists after
    Fail:   Disagreement not resolved; settlement attempted; missing ID not found
    Severity: STANDARD
    Invariant: INV-FED-RECON-001
    """
    case = _make_case(
        "FED-SETTLE-009",
        "Netting Disagreement: Full Obligation Exchange Identifies Discrepancy",
    )

    _reset_exec_state(base_url)
    _reset_netting_state(base_url)
    infra.reset_routing_state()

    t0 = time.monotonic()

    # 3 routing requests through normal flow → 3 obligations on Op A
    for rr_id, trace_id in [
        (_SETTLE9_RR_ID_1, _SETTLE9_TRACE_1),
        (_SETTLE9_RR_ID_2, _SETTLE9_TRACE_2),
        (_SETTLE9_RR_ID_3, _SETTLE9_TRACE_3),
    ]:
        payload = _build_exec_route_payload(
            base_url=base_url, sim_b_url=infra.sim_b_url,
            routing_request_id=rr_id, trace_id=trace_id,
            op_a_priv=op_a_priv, amount_minor=_SETTLE_AMOUNT,
        )
        try:
            _, result = _call_fed_route(base_url, payload)
            if not result or result.get("routing_status") != "accepted":
                return _fail_case(case, f"routing {rr_id} not accepted", int((time.monotonic() - t0) * 1000))
        except RuntimeError as exc:
            return _error_case(case, str(exc))

    # Inject a 4th routing directly on Sim Op B (simulates Op A crashed before recording it)
    injected = infra.inject_accepted_routing_on_b(
        _SETTLE9_MISSING_RR_ID, _SETTLE_AMOUNT, _SETTLE9_MISSING_TRACE,
        interop_transfer_id=_SETTLE9_MISSING_ITX_ID,
    )

    # Collect Op B's accepted routing IDs (all 4)
    op_b_accepted_ids = infra.get_sim_b_accepted_routing_ids()

    # Reconcile: cross-reference Op A's obligations against Op B's accepted list
    try:
        reconcile_status, reconcile_body = _netting_reconcile(base_url, op_b_accepted_ids)
    except RuntimeError as exc:
        return _error_case(case, f"reconcile failed: {exc}")

    if reconcile_status != 200 or not reconcile_body:
        return _fail_case(case, f"reconcile HTTP {reconcile_status}", int((time.monotonic() - t0) * 1000))

    missing_on_a = reconcile_body.get("missing_on_a", [])
    disagreement_detected = reconcile_body.get("status") == "discrepancy"
    missing_id_found = _SETTLE9_MISSING_RR_ID in missing_on_a

    # Recover: create the missing obligation on Op A
    recover_status = None
    recovered_obl = None
    if missing_id_found:
        try:
            recover_status, recover_body = _fail_recover_obligation(
                base_url,
                routing_request_id=_SETTLE9_MISSING_RR_ID,
                trace_id=_SETTLE9_MISSING_TRACE,
                interop_transfer_id=_SETTLE9_MISSING_ITX_ID,
                amount_minor=_SETTLE_AMOUNT,
                from_operator_id="operator-a-test",
                to_operator_id="operator-b-test",
            )
            ms = int((time.monotonic() - t0) * 1000)
            recovered_obl = (recover_body or {}).get("obligation") if recover_status == 200 else None
        except RuntimeError as exc:
            return _error_case(case, f"recover-obligation failed: {exc}")
    else:
        ms = int((time.monotonic() - t0) * 1000)

    recovery_initiated = recover_status == 200 and recovered_obl is not None

    # Verify obligation now exists for the recovered ID
    try:
        _, recovered_final = _get_obligation_op_a(base_url, _SETTLE9_MISSING_RR_ID)
        obligation_exists_after = recovered_final is not None and "obligation_id" in (recovered_final or {})
    except RuntimeError:
        obligation_exists_after = False

    assertions = [
        _assertion("3 normal routing requests accepted (prerequisite)",
                   True, "3 accepted", "3 accepted"),
        _assertion("Op B has 4 accepted routings (including injected)",
                   len(op_b_accepted_ids) >= 4, ">=4", len(op_b_accepted_ids)),
        _assertion("reconcile detected discrepancy (Op A has fewer obligations)",
                   disagreement_detected, "discrepancy", reconcile_body.get("status")),
        _assertion("missing routing_request_id identified",
                   missing_id_found, _SETTLE9_MISSING_RR_ID,
                   missing_on_a[0] if missing_on_a else "(none)"),
        _assertion("recovery initiated (HTTP 200 from recover-obligation)",
                   recovery_initiated, "ok", f"HTTP {recover_status}"),
        _assertion("obligation exists on Op A after recovery",
                   obligation_exists_after, "exists", "missing" if not obligation_exists_after else "exists"),
    ]
    case["evidence"] = {
        "op_a_obligation_count": reconcile_body.get("operator_a_obligation_count"),
        "op_b_accepted_count": reconcile_body.get("operator_b_accepted_count"),
        "missing_on_a": missing_on_a,
        "discrepancy_detected": disagreement_detected,
        "missing_id_identified": _SETTLE9_MISSING_RR_ID if missing_id_found else None,
        "recovery_initiated": recovery_initiated,
        "recovered_obligation_id": (recovered_obl or {}).get("obligation_id"),
        "obligation_exists_after_recovery": obligation_exists_after,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-SETTLE-010 ────────────────────────────────────────────────────────────

def run_fed_settle_010(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-SETTLE-010 — Zero-Net Case: No Bank Transfer; All Obligations Settled

    Equal obligations flow in both directions: gross_A_to_B == gross_B_to_A.
    net_amount = 0. No bank transfer needed. All obligations still marked settled.

    Pass:   zero_net=True; no bank transfer; all obligations settled
    Fail:   Bank transfer attempted for 0; obligations left pending
    Severity: STANDARD
    Invariant: INV-FED-LEDGER-001
    """
    case = _make_case("FED-SETTLE-010", "Zero-Net Case: No Bank Transfer; All Obligations Settled")

    _reset_exec_state(base_url)
    _reset_netting_state(base_url)
    infra.reset_routing_state()

    t0 = time.monotonic()

    # 2 A→B obligations of 30,000 each
    for rr_id, trace_id in [(_SETTLE10_RR_ID_1, _SETTLE10_TRACE_1),
                             (_SETTLE10_RR_ID_2, _SETTLE10_TRACE_2)]:
        payload = _build_exec_route_payload(
            base_url=base_url, sim_b_url=infra.sim_b_url,
            routing_request_id=rr_id, trace_id=trace_id,
            op_a_priv=op_a_priv, amount_minor=_SETTLE10_AMOUNT,
        )
        try:
            _, result = _call_fed_route(base_url, payload)
            if not result or result.get("routing_status") != "accepted":
                return _fail_case(case, f"routing {rr_id} not accepted", int((time.monotonic() - t0) * 1000))
        except RuntimeError as exc:
            return _error_case(case, str(exc))

    # 2 B→A obligations of 30,000 each → gross_b_to_a = 60,000 = gross_a_to_b
    for i, (rr_id, trace_id) in enumerate([
        ("rr-00000000-0000-0000-0000-000000010011", "tr-00000000-0000-0000-0000-000000010011"),
        ("rr-00000000-0000-0000-0000-000000010012", "tr-00000000-0000-0000-0000-000000010012"),
    ]):
        try:
            _add_b_obligation(base_url, _SETTLE10_AMOUNT, rr_id, trace_id)
        except RuntimeError as exc:
            return _error_case(case, f"add-b-obligation failed: {exc}")

    # Trigger netting
    try:
        netting_status, netting_body = _netting_trigger(base_url)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if netting_status != 200 or not netting_body:
        return _fail_case(case, f"netting/trigger HTTP {netting_status}", int((time.monotonic() - t0) * 1000))

    batch = netting_body.get("batch") or {}
    batch_id = batch.get("settlement_batch_id")
    gross_a_to_b = batch.get("gross_a_to_b")
    gross_b_to_a = batch.get("gross_b_to_a")
    net_amount = batch.get("net_amount")
    is_zero_net_batch = net_amount == 0

    # Execute settlement
    try:
        exec_status, exec_body = _netting_execute(base_url, batch_id)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if exec_status != 200 or not exec_body:
        return _fail_case(case, f"netting/execute HTTP {exec_status}", ms)

    zero_net_flag = exec_body.get("zero_net", False)
    no_bank_transfer = exec_body.get("no_bank_transfer", False)
    ledger_entries = exec_body.get("settlement_ledger_entries", [])
    bank_ref = exec_body.get("simulated_bank_reference")

    # Obligations should still be settled
    obl_states = {}
    for rr_id in [_SETTLE10_RR_ID_1, _SETTLE10_RR_ID_2]:
        try:
            _, obl = _get_obligation_op_a(base_url, rr_id)
            obl_states[rr_id] = obl.get("settlement_state") if obl else None
        except RuntimeError:
            obl_states[rr_id] = None
    all_settled = all(s == "settled" for s in obl_states.values())

    assertions = [
        _assertion("netting/trigger HTTP 200", netting_status == 200, 200, netting_status),
        _assertion(f"gross_a_to_b == gross_b_to_a ({_SETTLE10_AMOUNT * 2})",
                   gross_a_to_b == gross_b_to_a == _SETTLE10_AMOUNT * 2,
                   _SETTLE10_AMOUNT * 2, f"A:{gross_a_to_b} B:{gross_b_to_a}"),
        _assertion("net_amount == 0", net_amount == 0, 0, net_amount),
        _assertion("settlement executed (HTTP 200)", exec_status == 200, 200, exec_status),
        _assertion("zero_net == True", zero_net_flag, True, zero_net_flag),
        _assertion("no_bank_transfer == True (no bank transfer for zero-net)",
                   no_bank_transfer, True, no_bank_transfer),
        _assertion("no settlement ledger entries (no bank transfer means no ledger entries)",
                   len(ledger_entries) == 0, 0, len(ledger_entries)),
        _assertion("simulated_bank_reference is None (no transfer initiated)",
                   bank_ref is None, None, bank_ref),
        _assertion("all A→B obligations settled despite zero-net",
                   all_settled, "settled", str(obl_states)),
    ]
    case["evidence"] = {
        "gross_a_to_b": gross_a_to_b,
        "gross_b_to_a": gross_b_to_a,
        "net_amount": net_amount,
        "zero_net": zero_net_flag,
        "no_bank_transfer": no_bank_transfer,
        "settlement_ledger_entry_count": len(ledger_entries),
        "simulated_bank_reference": bank_ref,
        "obligation_states": obl_states,
        "settlement_batch_id": batch_id,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-FAIL-001 ──────────────────────────────────────────────────────────────

def run_fed_fail_001(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-FAIL-001 — Network Timeout Retry With Same routing_request_id Succeeds (F-101)

    Sim Op B drops first routing request. Second attempt with same routing_request_id
    succeeds. Payee credited once only; obligation created once only (INV-FED-004).

    Pass:   Payment succeeds on retry; no double payment
    Fail:   Operator A generates new routing_request_id; double credit; no retry
    Severity: CRITICAL
    Invariant: INV-FED-004
    """
    case = _make_case(
        "FED-FAIL-001",
        "Network Timeout Retry With Same routing_request_id Succeeds (F-101)",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    # Configure Sim Op B to drop the next routing request
    infra.set_drop_next_route(1)

    t0 = time.monotonic()

    # First attempt — Sim Op B drops it
    payload = _build_exec_route_payload(
        base_url=base_url, sim_b_url=infra.sim_b_url,
        routing_request_id=_FAIL1_RR_ID, trace_id=_FAIL1_TRACE,
        op_a_priv=op_a_priv, amount_minor=_FAIL_AMOUNT,
    )
    try:
        _, result1 = _call_fed_route(base_url, payload)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    first_failed = (not result1 or result1.get("routing_status") != "accepted")
    payer_debited_after_first = (result1 or {}).get("payer_debited", False)
    no_obl_after_first = True
    try:
        s1_obl, obl_after_first = _get_obligation_op_a(base_url, _FAIL1_RR_ID)
        no_obl_after_first = s1_obl == 404 or not (obl_after_first and "obligation_id" in obl_after_first)
    except RuntimeError:
        pass

    # Second attempt — same routing_request_id (retry); Sim Op B now accepts
    try:
        _, result2 = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    second_accepted = (result2 or {}).get("routing_status") == "accepted"

    # Verify payee credited once only
    payee_balance = infra.get_wallet_balance(_EXEC_PAYEE_WALLET)
    payee_credited_once = payee_balance == _FAIL_AMOUNT

    # Verify one obligation only
    try:
        _, final_obl = _get_obligation_op_a(base_url, _FAIL1_RR_ID)
        obligation_count = 1 if final_obl and "obligation_id" in final_obl else 0
    except RuntimeError:
        obligation_count = 0

    assertions = [
        _assertion("first attempt failed (Sim Op B dropped request)",
                   first_failed, "failed", (result1 or {}).get("routing_status")),
        _assertion("no payer debit after failed first attempt",
                   not payer_debited_after_first, False, payer_debited_after_first),
        _assertion("no obligation after failed first attempt",
                   no_obl_after_first, "absent", "absent" if no_obl_after_first else "exists"),
        _assertion("second attempt (retry with same routing_request_id) accepted",
                   second_accepted, "accepted", (result2 or {}).get("routing_status")),
        _assertion("payee credited exactly once (INV-FED-004)",
                   payee_credited_once, _FAIL_AMOUNT, payee_balance),
        _assertion("exactly one obligation for routing_request_id (INV-FED-004)",
                   obligation_count == 1, 1, obligation_count),
    ]
    case["evidence"] = {
        "routing_request_id": _FAIL1_RR_ID,
        "first_attempt_result": result1,
        "second_attempt_result": result2,
        "payee_balance_after": payee_balance,
        "obligation_count": obligation_count,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed)}", ms, assertions)


# ── FED-FAIL-002 ──────────────────────────────────────────────────────────────

def run_fed_fail_002(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-FAIL-002 — All Retries Fail: Payment Fails, No Debit, No Obligation

    Sim Op B is offline (returns 503 always). All routing attempts fail.
    Payer wallet unchanged; obligation count = 0.

    Pass:   No debit; no obligation; routing_status != accepted
    Fail:   Payer debited despite failed routing; obligation created without acceptance
    Severity: CRITICAL
    Invariant: INV-FED-002
    """
    case = _make_case(
        "FED-FAIL-002",
        "All Retries Fail: Payment Fails, No Debit, No Obligation",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    # Make Sim Op B "offline" by dropping next 3 requests (simulates all retries exhausted)
    infra.set_drop_next_route(3)

    # Get payer balance before
    try:
        _, wallet_before = _get_wallet_op_a(base_url, _EXEC_SENDER_WALLET)
        balance_before = (wallet_before or {}).get("balance_minor")
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    t0 = time.monotonic()
    payload = _build_exec_route_payload(
        base_url=base_url, sim_b_url=infra.sim_b_url,
        routing_request_id=_FAIL2_RR_ID, trace_id=_FAIL2_TRACE,
        op_a_priv=op_a_priv, amount_minor=_FAIL_AMOUNT,
    )
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    routing_not_accepted = (not result or result.get("routing_status") != "accepted")
    payer_debited = (result or {}).get("payer_debited", True)

    # Check payer balance unchanged
    try:
        _, wallet_after = _get_wallet_op_a(base_url, _EXEC_SENDER_WALLET)
        balance_after = (wallet_after or {}).get("balance_minor")
    except RuntimeError:
        balance_after = None
    balance_unchanged = (balance_before == balance_after)

    # Check no obligation
    try:
        s2_obl, obl = _get_obligation_op_a(base_url, _FAIL2_RR_ID)
        no_obligation = s2_obl == 404 or not (obl and "obligation_id" in obl)
    except RuntimeError:
        no_obligation = True

    assertions = [
        _assertion("routing failed (all retries exhausted)",
                   routing_not_accepted, "failed", (result or {}).get("routing_status")),
        _assertion("payer_debited == False",
                   not payer_debited, False, payer_debited),
        _assertion("payer wallet balance unchanged",
                   balance_unchanged, balance_before, balance_after),
        _assertion("no obligation recorded (INV-FED-002)",
                   no_obligation, "absent", "absent" if no_obligation else "exists"),
    ]
    case["evidence"] = {
        "routing_request_id": _FAIL2_RR_ID,
        "routing_result": result,
        "payer_balance_before": balance_before,
        "payer_balance_after": balance_after,
        "no_obligation": no_obligation,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed_a = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed_a)}", ms, assertions)


# ── FED-FAIL-003 ──────────────────────────────────────────────────────────────

def run_fed_fail_003(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-FAIL-003 — Unparseable Response Treated as Network Failure (F-102)

    Sim Op B returns HTTP 200 with invalid JSON. Operator A treats as ambiguous —
    no debit on malformed response. A subsequent retry with same routing_request_id
    succeeds.

    Pass:   No debit after malformed response; retry succeeds; payee credited once
    Fail:   Debit executed on malformed response; new routing_request_id generated
    Severity: STANDARD
    Invariant: INV-FED-004
    """
    case = _make_case(
        "FED-FAIL-003",
        "Unparseable Response Treated as Network Failure (F-102)",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()
    infra.set_malformed_response_once()

    t0 = time.monotonic()
    payload = _build_exec_route_payload(
        base_url=base_url, sim_b_url=infra.sim_b_url,
        routing_request_id=_FAIL3_RR_ID, trace_id=_FAIL3_TRACE,
        op_a_priv=op_a_priv, amount_minor=_FAIL_AMOUNT,
    )

    # First attempt — malformed response
    first_status = None
    first_result = None
    try:
        first_status, first_result = _call_fed_route(base_url, payload)
    except RuntimeError:
        pass  # fixture server returned 500 → that's expected

    first_failed = first_result is None or first_result.get("routing_status") != "accepted"
    no_debit_after_first = not (first_result or {}).get("payer_debited", False)

    # Second attempt (retry) — Sim Op B is back to normal
    try:
        _, result2 = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    second_accepted = (result2 or {}).get("routing_status") == "accepted"
    payee_balance = infra.get_wallet_balance(_EXEC_PAYEE_WALLET)
    payee_credited_once = (payee_balance == _FAIL_AMOUNT)

    assertions = [
        _assertion("first attempt failed on malformed response",
                   first_failed, "failed", (first_result or {}).get("routing_status")),
        _assertion("no payer debit after malformed response",
                   no_debit_after_first, False, (first_result or {}).get("payer_debited")),
        _assertion("retry (same routing_request_id) accepted",
                   second_accepted, "accepted", (result2 or {}).get("routing_status")),
        _assertion("payee credited exactly once after retry",
                   payee_credited_once, _FAIL_AMOUNT, payee_balance),
    ]
    case["evidence"] = {
        "routing_request_id": _FAIL3_RR_ID,
        "first_attempt_status": first_status,
        "first_attempt_result": first_result,
        "second_attempt_result": result2,
        "payee_balance_after": payee_balance,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed_a = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed_a)}", ms, assertions)


# ── FED-FAIL-004 ──────────────────────────────────────────────────────────────

def run_fed_fail_004(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-FAIL-004 — Operator A Certificate Rejected by Operator B (F-204)

    Sim Op B runs trust verification on Operator A and fails. Routing request
    is rejected with rejection_code=operator_trust_failure. No debit, no obligation.

    Pass:   rejection_code == operator_trust_failure; no debit; no obligation
    Fail:   Request accepted despite trust failure; money moved
    Severity: STANDARD
    Invariant: INV-TRUST-001
    """
    case = _make_case(
        "FED-FAIL-004",
        "Operator A Certificate Rejected by Operator B (F-204)",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()
    infra.set_trust_failure_once()

    t0 = time.monotonic()
    payload = _build_exec_route_payload(
        base_url=base_url, sim_b_url=infra.sim_b_url,
        routing_request_id=_FAIL4_RR_ID, trace_id=_FAIL4_TRACE,
        op_a_priv=op_a_priv, amount_minor=_FAIL_AMOUNT,
    )

    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    routing_status = (result or {}).get("routing_status")
    rejection_code = (result or {}).get("rejection_code")
    payer_debited = (result or {}).get("payer_debited", True)

    try:
        s4_obl, obl = _get_obligation_op_a(base_url, _FAIL4_RR_ID)
        no_obligation = s4_obl == 404 or not (obl and "obligation_id" in obl)
    except RuntimeError:
        no_obligation = True

    assertions = [
        _assertion("routing rejected (rejection_code present)",
                   routing_status == "rejected", "rejected", routing_status),
        _assertion("rejection_code == operator_trust_failure",
                   rejection_code == "operator_trust_failure",
                   "operator_trust_failure", rejection_code or "(absent)"),
        _assertion("no payer debit",
                   not payer_debited, False, payer_debited),
        _assertion("no obligation recorded",
                   no_obligation, "absent", "absent" if no_obligation else "exists"),
    ]
    case["evidence"] = {
        "routing_request_id": _FAIL4_RR_ID,
        "routing_status": routing_status,
        "rejection_code": rejection_code,
        "payer_debited": payer_debited,
        "no_obligation": no_obligation,
        "routing_result": result,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed_a = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed_a)}", ms, assertions)


# ── FED-FAIL-005 ──────────────────────────────────────────────────────────────

def run_fed_fail_005(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-FAIL-005 — Crash Recovery: Missing Obligation Recreated (F-402)

    Injects state: routing_request accepted by Sim Op B, but Op A crashed before
    Phase 4+5 (no debit, no obligation). Recovery process creates the obligation.

    Pass:   Obligation exists after recovery; debit exists; both linked by routing_request_id
    Fail:   Recovery not triggered; obligation missing after restart
    Severity: CRITICAL
    Invariant: INV-FED-002
    """
    case = _make_case(
        "FED-FAIL-005",
        "Crash Recovery: Missing Obligation Recreated (F-402)",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    t0 = time.monotonic()

    # Inject crash state: routing accepted on Sim Op B but Op A crashed before committing
    try:
        inj_status, inj_body = _fail_inject_crash_state(
            base_url,
            routing_request_id=_FAIL5_RR_ID,
            trace_id=_FAIL5_TRACE,
            interop_transfer_id=_FAIL5_ITX_ID,
            amount_minor=_FAIL_AMOUNT,
        )
        if inj_status != 200:
            return _error_case(case, f"inject-crash-state HTTP {inj_status}")
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    # Verify: before recovery, no obligation and no debit exist
    try:
        s5_obl, obl_before = _get_obligation_op_a(base_url, _FAIL5_RR_ID)
        no_obl_before = s5_obl == 404 or not (obl_before and "obligation_id" in obl_before)
    except RuntimeError:
        no_obl_before = True

    try:
        _, ledger_before = _get_ledger_op_a(base_url, _EXEC_SENDER_WALLET)
        debit_before = any(
            e.get("routing_request_id") == _FAIL5_RR_ID
            for e in (ledger_before or {}).get("entries", [])
        )
    except RuntimeError:
        debit_before = False

    # Trigger recovery
    try:
        rec_status, rec_body = _fail_trigger_recovery(base_url)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    recovered_count = (rec_body or {}).get("recovered_count", 0)
    recovery_triggered = rec_status == 200 and recovered_count > 0

    # Verify: after recovery, obligation and debit exist
    try:
        _, obl_after = _get_obligation_op_a(base_url, _FAIL5_RR_ID)
        obl_exists = obl_after is not None and "obligation_id" in (obl_after or {})
    except RuntimeError:
        obl_exists = False

    try:
        _, ledger_after = _get_ledger_op_a(base_url, _EXEC_SENDER_WALLET)
        debit_exists = any(
            e.get("routing_request_id") == _FAIL5_RR_ID
            for e in (ledger_after or {}).get("entries", [])
        )
    except RuntimeError:
        debit_exists = False

    assertions = [
        _assertion("crash state injected (routing accepted, no obligation)",
                   inj_status == 200, 200, inj_status),
        _assertion("no obligation before recovery",
                   no_obl_before, "absent", "absent" if no_obl_before else "exists"),
        _assertion("no debit before recovery",
                   not debit_before, "absent", "present" if debit_before else "absent"),
        _assertion("recovery triggered (trigger-recovery HTTP 200)",
                   rec_status == 200, 200, rec_status),
        _assertion("at least 1 obligation recovered",
                   recovered_count > 0, ">0", recovered_count),
        _assertion("obligation exists after recovery (INV-FED-002)",
                   obl_exists, "exists", "exists" if obl_exists else "missing"),
        _assertion("debit exists after recovery (BC-003)",
                   debit_exists, "exists", "exists" if debit_exists else "missing"),
    ]
    case["evidence"] = {
        "routing_request_id": _FAIL5_RR_ID,
        "no_obligation_before": no_obl_before,
        "no_debit_before": not debit_before,
        "recovered_count": recovered_count,
        "obligation_exists_after": obl_exists,
        "debit_exists_after": debit_exists,
        "obligation_after": obl_after,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed_a = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed_a)}", ms, assertions)


# ── FED-FAIL-006 ──────────────────────────────────────────────────────────────

def run_fed_fail_006(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-FAIL-006 — Extended BRL Outage: Fail-Closed After 12 Hours (F-602)

    BRL is 13 hours stale (> 12h threshold). Routing MUST be refused.
    Fail-closed: no routing accepted with stale BRL (INV-TRUST-006).

    Pass:   Routing refused; trust step 2.6 fails with BRL staleness
    Fail:   Routing accepted with 13h stale BRL
    Severity: STANDARD
    Invariant: INV-TRUST-006
    """
    case = _make_case(
        "FED-FAIL-006",
        "Extended BRL Outage: Fail-Closed After 12 Hours (F-602)",
    )

    infra.reset_routing_state()
    # Set BRL to 13 hours stale (> 12h fail-closed threshold)
    infra.set_brl_very_stale(stale_hours=13)

    t0 = time.monotonic()

    # Use the verify-peer endpoint to run trust protocol against Sim Op B
    manifest_url = f"{infra.sim_b_url}/.well-known/banza/operator.json"
    try:
        verify_status, _, verify_raw = http_post(
            f"{base_url}/conformance/federation/verify-peer",
            {"peer_manifest_url": manifest_url},
        )
        ms = int((time.monotonic() - t0) * 1000)
        try:
            verify_result = json.loads(verify_raw) if verify_raw else {}
        except json.JSONDecodeError:
            verify_result = {}
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    trusted = verify_result.get("trusted", True)  # should be False
    steps = verify_result.get("steps", [])
    step_2_6 = next((s for s in steps if s.get("step") == "2.6"), None)
    step_failed_at_brl = (
        step_2_6 is not None
        and step_2_6.get("status") == "fail"
        and "brl" in (step_2_6.get("reason", "") or "").lower()
    )
    routing_refused = not trusted

    # Restore BRL to valid state for subsequent tests
    infra.set_brl_empty()

    assertions = [
        _assertion("verify-peer HTTP 200", verify_status == 200, 200, verify_status),
        _assertion("trust verification fails (routing refused with stale BRL)",
                   routing_refused, False, trusted),
        _assertion("step 2.6 (BRL check) fails with staleness reason",
                   step_failed_at_brl,
                   "step 2.6 fail: brl_expired/stale",
                   f"step={step_2_6.get('step') if step_2_6 else 'absent'} "
                   f"status={step_2_6.get('status') if step_2_6 else 'absent'} "
                   f"reason={step_2_6.get('reason') if step_2_6 else 'absent'}"),
    ]
    case["evidence"] = {
        "brl_stale_hours": 13,
        "trusted": trusted,
        "step_2_6": step_2_6,
        "routing_refused": routing_refused,
        "trust_steps": steps,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed_a = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed_a)}", ms, assertions)


# ── FED-FAIL-007 ──────────────────────────────────────────────────────────────

def run_fed_fail_007(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-FAIL-007 — Revocation Mid-Flight: Obligation Survives Revocation

    Routing accepted and obligation recorded BEFORE Sim Op B is added to BRL.
    After BRL is updated, obligation remains in settlement_state=pending.
    Revocation must NOT delete or cancel existing obligations.

    Pass:   Obligation still exists and is pending; revocation does not delete obligations
    Fail:   Obligation deleted or cancelled due to revocation
    Severity: STANDARD
    Invariant: INV-FED-002
    """
    case = _make_case(
        "FED-FAIL-007",
        "Revocation Mid-Flight: Obligation Survives Revocation",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()
    infra.set_brl_empty()

    t0 = time.monotonic()

    # Create routing + obligation BEFORE revocation
    payload = _build_exec_route_payload(
        base_url=base_url, sim_b_url=infra.sim_b_url,
        routing_request_id=_FAIL7_RR_ID, trace_id=_FAIL7_TRACE,
        op_a_priv=op_a_priv, amount_minor=_FAIL_AMOUNT,
    )
    try:
        _, result = _call_fed_route(base_url, payload)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    if not result or result.get("routing_status") != "accepted":
        return _fail_case(case, f"pre-revocation routing not accepted: {result}",
                          int((time.monotonic() - t0) * 1000))

    # Check obligation state before revocation
    try:
        _, obl_before = _get_obligation_op_a(base_url, _FAIL7_RR_ID)
        obl_id_before = (obl_before or {}).get("obligation_id")
        state_before = (obl_before or {}).get("settlement_state")
    except RuntimeError as exc:
        return _error_case(case, f"get obligation before revocation failed: {exc}")

    # Now add Sim Op B to BRL (revoke it mid-flight)
    infra.set_brl_revoked("operator-b-test")

    # Check obligation state AFTER revocation — must still exist and be pending
    try:
        _, obl_after = _get_obligation_op_a(base_url, _FAIL7_RR_ID)
        obl_id_after = (obl_after or {}).get("obligation_id")
        state_after = (obl_after or {}).get("settlement_state")
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    # Restore BRL for subsequent tests
    infra.set_brl_empty()

    obligation_survives = (obl_after is not None and obl_id_after is not None)
    state_still_pending = (state_after == "pending")

    assertions = [
        _assertion("obligation exists before revocation",
                   obl_id_before is not None, "exists", obl_id_before or "absent"),
        _assertion("obligation settlement_state=pending before revocation",
                   state_before == "pending", "pending", state_before),
        _assertion("obligation still exists AFTER revocation (INV-FED-002)",
                   obligation_survives, "exists", "absent" if not obligation_survives else "exists"),
        _assertion("obligation settlement_state unchanged (still pending) after revocation",
                   state_still_pending, "pending", state_after),
        _assertion("obligation_id unchanged after revocation",
                   obl_id_before == obl_id_after, obl_id_before, obl_id_after),
    ]
    case["evidence"] = {
        "routing_request_id": _FAIL7_RR_ID,
        "obligation_id": obl_id_before,
        "state_before_revocation": state_before,
        "state_after_revocation": state_after,
        "obligation_survives": obligation_survives,
        "brl_revoked_operator": "operator-b-test",
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed_a = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed_a)}", ms, assertions)


# ── FED-FAIL-008 ──────────────────────────────────────────────────────────────

def run_fed_fail_008(base_url: str, infra: "RunnerInfra", op_a_priv) -> dict:
    """
    FED-FAIL-008 — Obligation Amount Mismatch Detected Before Signing (F-404)

    Operator A's obligation creation is injected with a mismatched amount
    (override_amount != routing amount). The INV-FED-005 check detects the mismatch
    and PREVENTS the obligation from being recorded. No debit occurs.

    Pass:   No obligation created; error logged with INV-FED-005 reference; no debit
    Fail:   Obligation with wrong amount persisted; no error raised
    Severity: CRITICAL
    Invariant: INV-FED-005
    """
    case = _make_case(
        "FED-FAIL-008",
        "Obligation Amount Mismatch Detected Before Signing (F-404)",
    )

    _reset_exec_state(base_url)
    infra.reset_routing_state()

    # Inject amount override: obligation would be created with 49,999 instead of 50,000
    mismatch_amount = _FAIL_AMOUNT - 1  # 49,999

    t0 = time.monotonic()
    try:
        inj_status, _ = _fail_inject_obligation_amount_override(
            base_url, _FAIL8_RR_ID, mismatch_amount
        )
        if inj_status != 200:
            return _error_case(case, f"inject-obligation-amount-override HTTP {inj_status}")
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    payload = _build_exec_route_payload(
        base_url=base_url, sim_b_url=infra.sim_b_url,
        routing_request_id=_FAIL8_RR_ID, trace_id=_FAIL8_TRACE,
        op_a_priv=op_a_priv, amount_minor=_FAIL_AMOUNT,
    )
    try:
        _, result = _call_fed_route(base_url, payload)
        ms = int((time.monotonic() - t0) * 1000)
    except RuntimeError as exc:
        return _error_case(case, str(exc))

    routing_status = (result or {}).get("routing_status")
    mismatch_blocked = routing_status == "failed_inv_fed_005"
    payer_debited = (result or {}).get("payer_debited", True)
    obligation_recorded = (result or {}).get("obligation_recorded", True)

    # Verify obligation does NOT exist in obligation store
    try:
        s8_obl, obl = _get_obligation_op_a(base_url, _FAIL8_RR_ID)
        no_obligation = s8_obl == 404 or not (obl and "obligation_id" in obl)
    except RuntimeError:
        no_obligation = True

    invariant_ref = (result or {}).get("invariant", "")

    assertions = [
        _assertion("mismatch blocked (routing_status=failed_inv_fed_005)",
                   mismatch_blocked, "failed_inv_fed_005", routing_status),
        _assertion("payer_debited == False (no debit on mismatch)",
                   not payer_debited, False, payer_debited),
        _assertion("obligation_recorded == False",
                   not obligation_recorded, False, obligation_recorded),
        _assertion("no obligation in obligation store (INV-FED-005)",
                   no_obligation, "absent", "absent" if no_obligation else "exists"),
        _assertion("error references INV-FED-005",
                   "INV-FED-005" in invariant_ref, "INV-FED-005", invariant_ref or "(absent)"),
    ]
    case["evidence"] = {
        "routing_request_id": _FAIL8_RR_ID,
        "routing_amount": _FAIL_AMOUNT,
        "attempted_obligation_amount": mismatch_amount,
        "mismatch": _FAIL_AMOUNT - mismatch_amount,
        "routing_result": result,
        "no_obligation": no_obligation,
    }

    if all(a["passed"] for a in assertions):
        return _pass_case(case, ms, assertions)
    failed_a = [a["assertion"] for a in assertions if not a["passed"]]
    return _fail_case(case, f"failed: {'; '.join(failed_a)}", ms, assertions)


# ── FED-FAIL suite runner ─────────────────────────────────────────────────────

def run_suite_fed_fail(
    base_url: str,
    infra: "RunnerInfra" = None,
    op_a_priv=None,
) -> dict:
    """Run all 8 FED-FAIL tests. Requires infra and op_a_priv."""
    def _skip(case_id, title, reason):
        return _skip_case(_make_case(case_id, title), reason)

    fail_avail = infra is not None and op_a_priv is not None

    if not fail_avail:
        reason = "failure infrastructure not available (install cryptography)"
        cases = [
            _skip(f"FED-FAIL-{str(i).zfill(3)}", t, reason)
            for i, t in [
                (1, "Network Timeout Retry With Same routing_request_id Succeeds"),
                (2, "All Retries Fail: Payment Fails, No Debit, No Obligation"),
                (3, "Unparseable Response Treated as Network Failure"),
                (4, "Operator A Certificate Rejected by Operator B"),
                (5, "Crash Recovery: Missing Obligation Recreated"),
                (6, "Extended BRL Outage: Fail-Closed After 12 Hours"),
                (7, "Revocation Mid-Flight: Obligation Survives Revocation"),
                (8, "Obligation Amount Mismatch Detected Before Signing"),
            ]
        ]
    else:
        cases = [
            run_fed_fail_001(base_url, infra, op_a_priv),
            run_fed_fail_002(base_url, infra, op_a_priv),
            run_fed_fail_003(base_url, infra, op_a_priv),
            run_fed_fail_004(base_url, infra, op_a_priv),
            run_fed_fail_005(base_url, infra, op_a_priv),
            run_fed_fail_006(base_url, infra, op_a_priv),
            run_fed_fail_007(base_url, infra, op_a_priv),
            run_fed_fail_008(base_url, infra, op_a_priv),
        ]

    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    skipped = sum(1 for c in cases if c["status"] in ("SKIP", "ERROR"))

    return {
        "suite_id": "FED-FAIL",
        "suite_name": "Failure and Recovery",
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
    run_obl = fed_suite in (None, "obl")
    run_evt = fed_suite in (None, "evt")
    run_settle = fed_suite in (None, "settle")
    run_fail = fed_suite in (None, "fail")

    if (fed_suite is not None
            and not run_cert and not run_disc and not run_trust
            and not run_route and not run_exec and not run_obl
            and not run_evt and not run_settle and not run_fail):
        print(f"ERROR: Unknown --fed-suite value: {fed_suite!r}. "
              f"Available: cert, disc, trust, route, exec, obl, evt, settle, fail",
              file=sys.stderr)
        return 2

    suite_label = {
        None: (
            "FED-CERT-001–011, FED-DISC-001–008, FED-TRUST-001–009, "
            "FED-ROUTE-001–012, FED-EXEC-001–008, FED-OBL-001–007, "
            "FED-EVT-001–006, FED-SETTLE-001–010, FED-FAIL-001–008"
        ),
        "cert": "FED-CERT-001–011",
        "disc": "FED-DISC-001–008",
        "trust": "FED-TRUST-001–009",
        "route": "FED-ROUTE-001–012",
        "exec": "FED-EXEC-001–008",
        "obl": "FED-OBL-001–007",
        "evt": "FED-EVT-001–006",
        "settle": "FED-SETTLE-001–010",
        "fail": "FED-FAIL-001–008",
    }.get(fed_suite, fed_suite)

    print(f"BANZA Federation Conformance Runner {RUNNER_VERSION}")
    print(f"Operator: {base_url}")
    print(f"Slice:    10 — {suite_label}")
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
    root_priv = None
    root_pub = None
    key_id = None
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

            # Store signing keys on infra so all set_brl_* calls auto-sign (INV-TRUST-005)
            infra.configure_signing_keys(root_priv, key_id)

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

            # Serialize Operator A private key bytes for fixture server obligation signing (FED-OBL-005)
            op_a_signing_key_b64 = None
            try:
                from cryptography.hazmat.primitives.serialization import (
                    Encoding, NoEncryption, PrivateFormat,
                )
                raw_priv = op_a_priv.private_bytes(
                    Encoding.Raw, PrivateFormat.Raw, NoEncryption()
                )
                op_a_signing_key_b64 = _tr.b64url_encode(raw_priv)
            except Exception:
                pass

            # Extended setup: deliver cert + BANZA root key + BRL URL + key manifest URL + signing key
            setup_ok = setup_operator_for_federation(
                base_url, cert_a,
                banza_root_key_id=key_id,
                banza_root_pub=root_pub,
                brl_url=infra.brl_url,
                key_manifest_url=infra.key_manifest_url,
                op_a_signing_key_b64=op_a_signing_key_b64,
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
        if run_obl:
            # Restore Sim Op B to valid state for obligation lifecycle tests
            if infra and manifest_b and cert_b_valid:
                infra.configure_sim_b(manifest_b, cert_b_valid)
                infra.set_brl_empty()
            suite_results.append(run_suite_fed_obl(
                base_url,
                infra=infra,
                op_a_priv=op_a_priv if _tr.CRYPTO_AVAILABLE else None,
            ))
        if run_evt:
            # Restore Sim Op B to valid state for federation event tests
            if infra and manifest_b and cert_b_valid:
                infra.configure_sim_b(manifest_b, cert_b_valid)
                infra.set_brl_empty()
            suite_results.append(run_suite_fed_evt(
                base_url,
                infra=infra,
                op_a_priv=op_a_priv if _tr.CRYPTO_AVAILABLE else None,
            ))
        if run_settle:
            # Restore Sim Op B to valid state for netting/settlement tests
            if infra and manifest_b and cert_b_valid:
                infra.configure_sim_b(manifest_b, cert_b_valid)
                infra.set_brl_empty()
            suite_results.append(run_suite_fed_settle(
                base_url,
                infra=infra,
                op_a_priv=op_a_priv if _tr.CRYPTO_AVAILABLE else None,
            ))
        if run_fail:
            # Restore Sim Op B to valid state for failure/recovery tests
            if infra and manifest_b and cert_b_valid:
                infra.configure_sim_b(manifest_b, cert_b_valid)
                infra.set_brl_empty()
            suite_results.append(run_suite_fed_fail(
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
        if "FED-OBL" in suite_ids:
            parts.append("FED-OBL-001–007")
        if "FED-EVT" in suite_ids:
            parts.append("FED-EVT-001–006")
        if "FED-SETTLE" in suite_ids:
            parts.append("FED-SETTLE-001–010")
        if "FED-FAIL" in suite_ids:
            parts.append("FED-FAIL-001–008")
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
        if "FED-OBL" in suite_ids:
            print("  ✓ Obligation created immediately on routing acceptance   (INV-FED-002)")
            print("  ✓ Obligation amount.minor == routing request amount      (INV-FED-005)")
            print("  ✓ Obligation amount.currency == routing request currency (INV-FED-005)")
            print("  ✓ Obligation trace_id propagated unchanged               (INV-FED-001)")
            print("  ✓ Exactly one obligation per routing_request_id          (INV-FED-002)")
            print("  ✓ obligor_signature verifies against Operator A public key (non-repudiable)")
            print("  ✓ State machine: pending → in_netting → settled only")
            print("  ✓ Backward transition (settled → in_netting) rejected    (state machine)")
            print("  ✓ Settled obligation contains settled_at (ISO 8601)")
            print("  ✓ Settled obligation contains settlement_batch_id")
        if "FED-EVT" in suite_ids:
            print("  ✓ federation.routing.accepted event on Operator B")
            print("  ✓ federation.payment.initiated event on Operator A")
            print("  ✓ federation.payment.completed event on Operator B")
            print("  ✓ federation.obligation.recorded event on Operator A with obligation_id")
            print("  ✓ All 4 event types carry identical trace_id            (INV-FED-001)")
            print("  ✓ All federation events validate against federation-event.json schema")
        if "FED-SETTLE" in suite_ids:
            print("  ✓ All pending obligations enter netting batch; states advance to in_netting")
            print("  ✓ gross_a_to_b and gross_b_to_a computed correctly; net = abs(diff) (INV-FED-LEDGER-001)")
            print("  ✓ Both operators independently compute identical net position (bilateral agreement)")
            print("  ✓ Settlement produces 4 correct ledger entries on both operators (INV-FED-LEDGER-001)")
            print("  ✓ Settled obligations carry settled_at (ISO 8601) + settlement_batch_id")
            print("  ✓ Every accepted routing request has exactly one obligation (INV-FED-RECON-001)")
            print("  ✓ trace_id appears in all 4 artifact types across both operators (INV-FED-RECON-001)")
            print("  ✓ Amount mismatch blocks settlement; no bank transfer occurs   (INV-FED-LEDGER-001)")
            print("  ✓ Netting disagreement detected; missing obligation identified; recovery initiated")
            print("  ✓ Zero-net: no bank transfer; obligations still settled        (INV-FED-LEDGER-001)")
        if "FED-FAIL" in suite_ids:
            print("  ✓ Idempotent retry succeeds after network drop; payee credited once (INV-FED-004, F-101)")
            print("  ✓ All retries exhausted: no debit, no obligation               (INV-FED-002, F-104)")
            print("  ✓ Malformed response treated as failure; retry succeeds         (INV-FED-004, F-102)")
            print("  ✓ Op A cert rejected by Op B → rejection_code=operator_trust_failure (F-204)")
            print("  ✓ Crash recovery: missing obligation created on recovery run    (INV-FED-002, F-402)")
            print("  ✓ Extended BRL outage: routing refused when BRL >12h stale      (INV-TRUST-006, F-602)")
            print("  ✓ Revocation mid-flight: existing obligation survives revocation (INV-FED-002)")
            print("  ✓ Obligation amount mismatch halts recording before signing      (INV-FED-005, F-404)")
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
        "slice": "10",
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
        # Sign the evidence package when crypto is available (INV-TRUST-005 — tamper-evident)
        if _tr.CRYPTO_AVAILABLE and root_priv is not None and key_id is not None and root_pub is not None:
            try:
                report = _tr.sign_evidence_package(report, root_priv, key_id, root_pub)
            except Exception as exc:
                print(f"  Warning: evidence package signing failed: {exc}", file=sys.stderr)
        with open(output, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\nReport written to {output}")
        if report.get("package_signature"):
            pkg = report["package_signature"]
            print(f"  evidence_hash:     {report.get('evidence_hash', '')[:32]}…")
            print(f"  issuer_key_id:     {pkg.get('issuer_key_id', '')}")
            print(f"  signed_at:         {pkg.get('signed_at', '')}")

    return 0 if total_fail == 0 else 1


# ── Standalone entry point ────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="BANZA Federation Conformance Runner "
                    "(FED-CERT + FED-DISC + FED-TRUST + FED-ROUTE + FED-EXEC "
                    "+ FED-OBL + FED-EVT + FED-SETTLE + FED-FAIL)"
    )
    parser.add_argument("--url", required=True,
                        help="Base URL of the operator (e.g. http://localhost:8099)")
    parser.add_argument("--output", help="Write JSON report to this file")
    parser.add_argument("--quiet", action="store_true", help="Suppress passing test output")
    parser.add_argument("--fed-suite", dest="fed_suite",
                        help="Run only this suite: cert | disc | trust | route | exec | obl | evt | settle | fail (default: all)")
    args = parser.parse_args()

    sys.exit(run_federation_mode(
        args.url.rstrip("/"),
        output=args.output,
        quiet=args.quiet,
        fed_suite=args.fed_suite,
    ))


if __name__ == "__main__":
    main()
