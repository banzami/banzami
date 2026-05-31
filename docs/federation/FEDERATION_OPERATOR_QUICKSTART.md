# BANZA L3 Federation Certification — Operator Quickstart

**Document ID:** FEDERATION-OPERATOR-QUICKSTART-001  
**Date:** 2026-05-31  
**Status:** Canonical — operator-facing  
**Authority:** FEDERATION_CONFORMANCE_MODEL.md, ADR-026

---

## What is L3 Federation Certification?

L3 Federation Certification proves that your operator correctly implements the BANZA cross-operator payment protocol. A certified operator can:

- Accept routing requests from any other certified operator
- Route payments from your consumers to payees on any other certified operator
- Participate in bilateral netting and settlement
- Be trusted by peers via the BANZA certificate infrastructure

The certification is earned by passing 79 conformance tests across 9 suites. No self-declaration. No manual review bypass.

---

## What you must implement

Before running the conformance suite, your operator must expose these endpoints:

| Endpoint | Method | Auth | Purpose |
|---|---|---|---|
| `/.well-known/banza/certificate.json` | GET | None (public) | Serve your BANZA-issued operator certificate |
| `/.well-known/banza/operator.json` | GET | None (public) | Serve your operator manifest with federation fields |
| `/federation/route` | POST | `Banza-Federation-Signature` header | Accept routing requests from other operators |
| `/federation/obligations` | GET | `Banza-Federation-Signature` header | List recorded inter-operator obligations |
| `/federation/obligations/{id}` | GET | `Banza-Federation-Signature` header | Get a specific obligation |
| `/federation/events` | GET | `Banza-Federation-Signature` header | Serve federation event stream |

### Certificate requirements

Your operator certificate (`/.well-known/banza/certificate.json`) must:
- Have `certification_level >= 3`
- Be signed by the BANZA root key (test or production)
- Not be expired (`expires_at > now()`)
- Have `operator_id` matching your manifest
- Have `capabilities` including `"cross_operator_routing"`
- Have `issuer == "BANZA"` (exact string)

See `contracts/federation/operator-certificate.json` for the full schema.

### Manifest requirements

Your manifest (`/.well-known/banza/operator.json`) must include the federation extension fields:

```json
{
  "operator_id": "your-operator-id",
  "federation_version": "1",
  "certificate_url": "https://your-domain.example/.well-known/banza/certificate.json",
  "interop_endpoint": "https://your-domain.example",
  "supports_federation": true,
  "cross_operator_routing": true,
  "cross_operator_settlement": true,
  "federation_capabilities": {
    "routing_version": "1",
    "settlement_version": "1",
    "supported_currencies": ["AOA"],
    "netting_interval_hours": 24
  }
}
```

See `contracts/federation/federation-manifest.json` for the full schema.

### Routing endpoint requirements

`POST /federation/route` must:
1. Verify the `Banza-Federation-Signature` header (ed25519 — see ADR-026)
2. Run trust verification (9 steps) on the sender's certificate at `certificate_url`
3. Validate `to_operator_id == this operator's operator_id`
4. Resolve the `recipient_identifier`
5. Accept (credit payee atomically) or return a structured rejection with a `rejection_code`
6. Return `routing_request_id` echoed, `trace_id` echoed, `interop_transfer_id` on acceptance
7. Be idempotent: same `routing_request_id` → same response

### Obligation recording requirements

After accepting a routing request, your operator (as Operator A sending money) must:
1. Atomically debit the payer wallet AND record an obligation in the same database transaction
2. Sign the obligation with your private key (`obligor_signature`)
3. The obligation must have `trace_id` matching the routing request

See `contracts/federation/federation-obligation.json` and `FEDERATION_PROTOCOL_FLOW.md` Phase 4–5.

---

## Running the conformance suite

### Prerequisites

```bash
pip install cryptography>=41.0.0  # for ed25519 signature tests
```

### Step 1 — Start the fixture server

The fixture server acts as the "Operator A" adapter in the conformance test infrastructure:

```bash
python3 tools/banza-conformance/fixture_server.py --port 8099
```

Leave this running in Terminal 1.

### Step 2 — Run the full suite

```bash
python3 tools/banza-conformance/run.py \
  --federation \
  --url http://localhost:8099 \
  --output l3-evidence.json
```

If your operator is running at a different URL, replace `http://localhost:8099` with your URL.

**Expected output (all pass):**
```
BANZA Federation Conformance Runner 1.1.0-slice10
Slice: 10 — FED-CERT-001–011, ..., FED-FAIL-001–008
...
[Suite] Certificate Validation    → 11 passed, 0 failed
[Suite] Discovery and Manifest    → 8 passed, 0 failed
[Suite] Trust Establishment       → 9 passed, 0 failed
[Suite] Routing Negotiation       → 12 passed, 0 failed
[Suite] Transfer Execution        → 8 passed, 0 failed
[Suite] Obligation Lifecycle      → 7 passed, 0 failed
[Suite] Federation Event Emission → 6 passed, 0 failed
[Suite] Netting and Settlement    → 10 passed, 0 failed
[Suite] Failure and Recovery      → 8 passed, 0 failed
============================================================
FED-CERT-001–011, ...: ALL PASS
```

### Step 3 — Diagnose failures

Run a single suite to isolate failures:

```bash
# Run only certificate validation
python3 tools/banza-conformance/run.py --federation --url http://localhost:8099 --fed-suite cert

# Available suite IDs: cert | disc | trust | route | exec | obl | evt | settle | fail
```

Failures print the specific assertion that failed:
```
✗ FED-CERT-002 — Certificate Signature Verifies
  ✗ signature verifies against test BANZA root (expected: true, got: false)
```

### Step 4 — Submit evidence to BANZA

Once all tests pass, submit `l3-evidence.json` to BANZA via the certification portal:

```
POST https://certification.banza.network/apply
{
  "evidence_package": "<contents of l3-evidence.json>",
  "operator_id": "your-operator-id",
  "target_level": 3
}
```

BANZA reviews the evidence and issues a production operator certificate if all requirements are met.

---

## Certification decision rules

**Certification granted** when:
- All blocking suites pass (FED-CERT through FED-OBL)
- FED-EVT: all 6 cases pass
- FED-SETTLE: cases 001–008 pass
- FED-FAIL: cases 001, 004, 005 pass
- No CRITICAL invariant violation in any suite

**Certification denied** when:
- Any failure in FED-CERT, FED-DISC, or FED-TRUST
- FED-ROUTE: any failure in cases 001–009
- FED-EXEC: any failure in cases 001–005
- FED-OBL: any failure in cases 001–005
- Any CRITICAL invariant violation

**Conditional certification** (30-day remediation window):
- FED-EVT cases 002 or 003 fail
- FED-SETTLE cases 009 or 010 fail
- FED-FAIL cases 002, 003, 006, 007, 008 fail

---

## Key invariants your implementation must enforce

| Invariant | What it means | Tested by |
|---|---|---|
| INV-TRUST-001 | Your peer's certificate signature must verify against the BANZA root key | FED-TRUST-002 (negative) |
| INV-FED-001 | trace_id must be identical in all artifacts for a cross-operator payment | FED-ROUTE-003, FED-OBL-003, FED-EVT-005 |
| INV-FED-002 | Every accepted routing request produces exactly one obligation | FED-OBL-001, FED-OBL-004 |
| INV-FED-004 | Same routing_request_id must produce the same result (idempotency) | FED-ROUTE-004 |
| INV-FED-005 | Obligation amount == routing request amount exactly | FED-OBL-002 |
| INV-FED-LEDGER-002 | All monetary values must be integer minor units (no floats) | FED-ROUTE-010 |

---

## Where to go next

| Document | Purpose |
|---|---|
| `docs/federation/FEDERATION_PROTOCOL_FLOW.md` | Complete behavioral spec for all 10 phases |
| `docs/federation/FEDERATION_INVARIANTS.md` | Formal invariant definitions with implementation notes |
| `docs/federation/FEDERATION_CONTRACT_SURFACE.md` | Full field specifications for all 5 federation contracts |
| `docs/federation/FEDERATION_FAILURE_SCENARIOS.md` | Recovery runbooks for all failure modes |
| `docs/federation/FEDERATION_CONFORMANCE_MODEL.md` | Full certification decision rules |
| `contracts/federation/` | JSON Schema definitions for all contracts |
| `docs/adr/ADR-026*.md` | Architectural Decision Record for the trust model |
