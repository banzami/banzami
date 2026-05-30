# BANZA — Certification

> This document describes: **BANZA** — the open financial infrastructure protocol.
> For other layers: [BanzAI](../banzai/BANZAI_REFERENCE.md) · [Banzami](../banzami/BANZAMI_REFERENCE.md)

**Version:** 1.0  
**Date:** 2026-05-30  
**Status:** Official  
**Authority:** ADR-025

---

## Overview

BANZA Certification is the formal verification that an operator implements the BANZA protocol correctly at a given level. Certification is:

- **Earned** — by passing the conformance suite, not by self-declaration
- **Level-bound** — five levels (0–4) with increasing protocol depth
- **Version-bound** — tied to a specific protocol version
- **Time-limited** — expires after 12 months without re-verification
- **Tool-verified** — conformance tests are deterministic; AI inference is not a substitute

> A certified operator is one whose conformance suite results, financial invariants, and manifest have been verified by the BANZA certification process.

BanzAI can guide operators through the certification process — but only the conformance suite determines the result. See [BANZAI_CAPABILITIES.md](../banzai/BANZAI_CAPABILITIES.md).

---

## Universal Certification Rules

The following rules apply at **all certification levels** (0–4). Violation of any universal rule is an immediate certification blocker regardless of level.

### MON-001 — Monetary Integer Representation

| Field | Value |
|-------|-------|
| ID | `MON-001` |
| Name | Monetary Integer Representation |
| Applies to | All levels (0–4) |
| Severity | CRITICAL |

**Definition:** All monetary values MUST be represented as integer minor units. Floating-point monetary representation is prohibited across the entire protocol surface.

| Violation | Result |
|-----------|--------|
| Float values in API request/response | Certification FAIL |
| Float values in traces or structured logs | Certification FAIL |
| Float values in operator manifests | Certification FAIL |
| Float values in settlement messages | Certification FAIL |
| Float values in wallet balances | Certification FAIL |
| `gross_minor ≠ net_minor + fee_minor` | Certification FAIL |
| `balance_minor ≠ available_minor + reserved_minor` | Certification FAIL |

See [BANZA_REFERENCE.md §6](BANZA_REFERENCE.md) for the full monetary representation specification.

---

## Certification Levels

### Level 0 — Sandbox Operator

**Purpose:** Prove the operator can run the BANZA protocol in a test environment.

**Requirements:**
- Valid Operator Manifest (any certification level declared as 0)
- MON-001 — Monetary Integer Representation (universal rule)
- Sandbox environment operational
- Basic `POST /v1/sandbox/fund` and wallet query tests pass
- No live settlement rails required

**What it unlocks:** Access to sandbox API keys, test webhook delivery, BANZA developer support.

---

### Level 1 — Payment Operator

**Purpose:** Consumer wallets, static QR payments, and @handle P2P transfers.

**Required capabilities:**
- `wallet.consumer` — consumer wallet creation, funding, querying
- `wallet.merchant` — merchant wallet management
- `qr.static` — static QR generation and payment processing
- `p2p.transfer` — @handle-to-@handle consumer transfers

**Required invariants:**
- INV-LEDGER-001 — double-entry balance
- INV-LEDGER-002 — immutable entries
- INV-LEDGER-003 — no floating-point money
- INV-LEDGER-004 — atomic posting
- INV-WALLET-001 — balance consistency
- INV-STL-001 — no money creation
- INV-STL-002 — no negative balances
- INV-IDENT-001 — handle uniqueness
- INV-TRACE-001 — trace propagation

**Conformance suites:** `core-payments/` (all 5 files, 28 tests)

**What it unlocks:** Live API keys for core payment operations, payment volume up to operator-agreed limits.

---

### Level 2 — Settlement Operator

**Purpose:** Dynamic QR, payment links, and instant settlement.

**Includes:** All Level 1 requirements.

**Additional required capabilities:**
- `qr.dynamic` — dynamic QR with encoded amount
- `payment_links` — pull-payment URLs
- `settlement.t0` — T+0 (instant) settlement to merchant wallet

**Additional required invariants:**
- INV-QR-001 — QR single-use enforcement
- INV-QR-002 — dynamic QR amount immutability

**Conformance suites:** `core-payments/` + `advanced-payments/` (all 8 files, 52 tests)

**What it unlocks:** Dynamic QR, payment link issuance, instant settlement for merchants.

---

### Level 3 — Federation Operator

**Purpose:** Complete payment lifecycle including payouts and automated reconciliation.

**Includes:** All Level 1–2 requirements.

**Additional required capabilities:**
- `payout.batch` — batch payouts to bank accounts
- `reconciliation` — automated ledger reconciliation

**Conformance suites:** `core-payments/` + `advanced-payments/` + `full-protocol/` (all 10 files, 66 tests)

**What it unlocks:** Payout rails (EMIS/Multicaixa), reconciliation reports, higher transaction volume limits.

---

### Level 4 — Infrastructure Operator

**Purpose:** Full infrastructure capability including card acquiring and federation readiness.

**Includes:** All Level 1–3 requirements.

**Additional required capabilities:**
- `acquiring.emis` — EMIS card acquiring integration
- `federation_ready` — inter-operator routing capability

**Conformance suites:** All suites including `infrastructure/` (all 12 files, 88 tests)

**What it unlocks:** Card acquiring, participation in BANZA federation (when available), highest transaction volume limits, operator network access.

---

## Certification Process

### Step 1: Prepare your manifest

Create a valid manifest for your target level. Run the Manifest Validator to verify it passes structural and semantic validation. See [BANZAI_CAPABILITIES.md](../banzai/BANZAI_CAPABILITIES.md) for the BanzAI Operator Builder and Manifest Validator tools.

### Step 2: Implement the capabilities

Build your operator implementation against the BANZA Kernel API or by implementing the equivalent protocol behaviour. Use the [Banzami reference operator](../banzami/BANZAMI_ARCHITECTURE.md) as your reference.

### Step 3: Run the conformance suite

Run the conformance suite for your target level against your sandbox environment:

```bash
banzami-conformance run \
  --level 1 \
  --api-key bz_test_... \
  --base-url https://sandbox-api.youroperator.ao \
  --output conformance-results.json
```

All tests must pass. A single failure blocks certification for that level.

### Step 4: Submit for certification

Submit your conformance results to BANZA:

```
POST /certification/apply
{
  "manifest": { ...operator manifest... },
  "conformance_results": "conformance-results.json",
  "target_level": 1,
  "contact": { "technical": "...", "operations": "..." }
}
```

### Step 5: BANZA review

BANZA reviews:
- Conformance result file authenticity (signed by conformance runner)
- Manifest consistency with conformance results
- Financial invariant status for all declared capabilities
- Sandbox environment availability

Review typically completes within 5 business days.

### Step 6: Certification issued

On approval, BANZA issues:
- A signed certification artifact (JSON + signature)
- A certification badge for your operator profile
- Live API key access for certified capabilities
- Entry in the public operator registry

---

## Certification Maintenance

### Re-certification triggers

| Trigger | Action required |
|---------|----------------|
| Protocol major version update | Re-run full conformance suite for your level |
| New capability added to manifest | Re-run conformance for the new capability |
| 12 months elapsed | Re-run full conformance suite |
| Invariant failure detected in monitoring | Immediate re-certification required |

### Automated monitoring

Certified operators are subject to:
- Monthly automated invariant verification (spot checks via sandbox)
- Quarterly conformance spot-checks (subset of full suite)
- Real-time invariant monitoring via OTel attributes

### Certification suspension

A certification is suspended (not revoked) when:
- A critical invariant failure is detected in monitoring
- The operator does not respond to re-certification requests within 30 days

Suspended operators cannot process live payments until re-certification is complete.

---

## Operator Registry

The public operator registry lists all certified operators with:
- Operator ID and name
- Certification level
- Certified capabilities
- Certification date and expiry
- Sandbox endpoint (if available)

---

## Certification Badges

Certified operators receive a badge for each level:

| Badge | Level | Label |
|-------|-------|-------|
| L0 | 0 | BANZA Sandbox Operator |
| L1 | 1 | BANZA Payment Operator |
| L2 | 2 | BANZA Settlement Operator |
| L3 | 3 | BANZA Federation Operator |
| L4 | 4 | BANZA Infrastructure Operator |

---

## FAQ

**Can I certify at Level 2 without passing Level 1?**

No. Each level is cumulative. Level 2 requires all Level 1 tests to pass, plus the additional Level 2 tests.

**Can an operator be certified at multiple levels simultaneously?**

No. Certification is for a single level. Level 3 includes all Level 1 and 2 requirements.

**What happens if a conformance test fails?**

Your certification application is rejected for the target level. Fix the failure, re-run the suite, and resubmit.

**Can AI replace the conformance suite?**

No. BanzAI can explain test failures and suggest fixes, but only the conformance suite determines certification. AI inference is not a substitute. This is the deterministic-first principle — see [BANZAI_REFERENCE.md §7](../banzai/BANZAI_REFERENCE.md).

**How long does review take?**

5 business days for standard review. Expedited review (24 hours) available for Infrastructure Operator applications.

---

**Referências:**

- [BANZA_CONFORMANCE.md](BANZA_CONFORMANCE.md) — Conformance suite specification
- [BANZA_REFERENCE.md §7](BANZA_REFERENCE.md) — Financial invariants (authoritative)
- [BANZA_REFERENCE.md §9](BANZA_REFERENCE.md) — Certification model overview
- [BANZAI_CAPABILITIES.md](../banzai/BANZAI_CAPABILITIES.md) — BanzAI Certification Copilot
- `docs/validation/INVARIANT_TAXONOMY.md` — Invariant registry
