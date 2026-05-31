# ADR-028 — BANZA Certification Level Architecture

**Status:** Accepted  
**Date:** 2026-05-31  
**Author:** BANZA Protocol  
**Deciders:** Fidel Monteiro (Founder)  
**Supersedes:** —  
**Superseded by:** —  
**Dependency:** ADR-026 (Federation Trust Model)  
**See also:** ADR-002, ADR-018, ADR-019, ADR-020, ADR-025, ADR-026  

---

## Context

L3 Federation Certification is now executable end-to-end. The federation conformance suite passes 79/79 tests across 9 suites. All federation contracts, trust infrastructure, BRL signature verification, and evidence package signing are operational.

Three production blockers remain:

1. **ADR-028** — certification level architecture (this document)
2. Production BANZA Root key establishment
3. Real two-operator interoperability test

This blocker exists because **two documents in the repository define L3 and L4 differently**, and no prior ADR declared one as authoritative.

### The Conflict

When the repository was first written, `BANZA_CERTIFICATION.md` defined:

- **L3** — "Complete payment lifecycle including payouts and automated reconciliation" (`payout.batch`, `reconciliation`)
- **L4** — "Full infrastructure capability including card acquiring and federation readiness" (`acquiring.emis`, `federation_ready`)

Federation was placed at L4 in that document.

When ADR-026 (Federation Trust Model) was subsequently written, it established federation at **L3**:

- ADR-026 §Phase 6: "REQUIRED_LEVEL = 3" for cross-operator routing
- INV-TRUST-004: "`supports_federation=true` requires `certification_level >= 3`"
- All FED-L3-001–014 requirements target `certification_level >= 3`
- All conformance code enforces `if level < 3: reject` at the federation routing gate

ADR-026 did not update `BANZA_CERTIFICATION.md`. The result is a semantic divergence between BANZA_CERTIFICATION.md (federation = L4) and ADR-026 + all conformance infrastructure (federation = L3).

This ADR resolves that divergence and becomes the **single authoritative source** for certification level definitions. All other documents are subordinate to this ADR.

---

## Phase 1 — Audit Findings

A complete repository audit was conducted as a prerequisite for this ADR. The following documents contain certification level references.

### Sources audited

| Document | L0 | L1 | L2 | L3 | L4 | Status |
|----------|----|----|----|----|-----|--------|
| `BANZA_CERTIFICATION.md` | Sandbox | Payment | Settlement | Payout+Recon | Infra+Fed | **DIVERGES at L3/L4** |
| `BANZA_CONFORMANCE.md` | Sandbox | Payment | Settlement+Traces | Manifest+Fed | Infra+NoMoneyCre | Consistent with ADR-026 |
| `BANZA_REFERENCE.md` | Sandbox | Payment | Settlement | Federation | Infrastructure | Consistent with ADR-026 |
| `docs/adr/ADR-026-FEDERATION-TRUST-MODEL.md` | — | — | — | Federation (REQUIRED_LEVEL=3) | — | Authoritative for federation |
| `contracts/federation/operator-certificate.json` | — | — | — | L3+ 90-day lifetime | — | Consistent with ADR-026 |
| `contracts/federation/federation-manifest.json` | — | — | — | L3+ supports_federation | — | Consistent with ADR-026 |
| `tools/banza-conformance/fixture_server.py` | — | — | — | `if level < 3: reject` | — | Consistent with ADR-026 |
| `tools/banza-conformance/run_fed.py` | — | — | — | `if cert_level >= 3` | — | Consistent with ADR-026 |
| `contracts/events/types.json` | L0 events | L1 events | — | — | — | Consistent everywhere |

### Findings

**Finding 1 — Single conflict:** `BANZA_CERTIFICATION.md` places federation at L4 (`federation_ready` capability). Every other source places federation at L3. This is the only conflict in the repository.

**Finding 2 — Consensus on all other definitions:** L0 (Sandbox), L1 (Payment), L2 (Settlement) are defined identically across all sources. No conflicts at these levels.

**Finding 3 — Two hard-coded level checks, both correct per ADR-026:**
- `fixture_server.py:211` — `if level < 3: reject` (federation routing gate, INV-TRUST-004)
- `run_fed.py:1177` — `if cert_level >= 3` (90-day lifetime rule, INV-TRUST-002)

**Finding 4 — Level model is cumulative everywhere:** All sources agree that higher levels include all lower level requirements. No source permits skipping.

**Finding 5 — `payout.batch` and `reconciliation` are correctly scoped at L3:** Automated reconciliation is a requirement of federation settlement (FED-SETTLE-006, FED-SETTLE-007). Batch payout is the mechanism by which inter-operator net positions are settled via bank rails. Both belong at L3 alongside cross-operator routing — not as alternatives to it.

---

## Phase 2 — Why Certification Levels Exist

### Purpose

Certification levels exist to express **capability boundaries** — the set of BANZA protocol operations an operator has proven it can execute correctly under conformance conditions.

They answer: *What can this operator do in the BANZA network?*

### What certification levels are NOT

| Attribute | Forbidden | Reason |
|-----------|-----------|--------|
| Company size | Not a factor | A small operator that passes L3 federation tests is L3-certified. A large operator that has not is not. |
| Commercial importance | Not a factor | The protocol has no concept of operator prestige. Trust is mathematical, not reputational. |
| Operator reputation | Not a factor | The BRL handles suspension; certification levels handle capability. |
| Time in network | Not a factor | An operator certified at L3 on day 1 is L3-certified. Tenure is irrelevant. |
| Financial volume | Not a factor | Volume limits are a commercial parameter; capability levels are protocol parameters. They may be correlated but are not equivalent. |

### Why five levels

The five levels reflect five distinct capability thresholds in the BANZA protocol, each corresponding to a qualitative increase in protocol complexity, inter-operator dependency, and financial risk:

| Level | Qualitative threshold |
|-------|-----------------------|
| L0 | Protocol reachability: can the operator speak BANZA at all? |
| L1 | Core payments: can money move within the operator? |
| L2 | Advanced payments: can the operator handle all single-operator payment types? |
| L3 | Federation: can money move across operator boundaries? |
| L4 | Infrastructure: can the operator act as a card-acquiring and high-volume network member? |

Each threshold represents a boundary that requires independent conformance evidence. A claim of L3 capability without L3 evidence is not certification — it is self-declaration, which the protocol does not recognize.

---

## Phase 3 — Evaluation of the Prior Model

### What the prior model got right

1. The five-level structure (L0–L4) is correct and is retained.
2. The names (Sandbox, Payment, Settlement, Federation, Infrastructure) are correct and are retained.
3. L0–L2 scopes are correct and are retained unchanged.
4. The cumulative rule is correct and is retained.
5. The 12-month re-certification cycle is correct and is retained.

### What the prior model got wrong

**`BANZA_CERTIFICATION.md` placed federation at L4.** This was written before ADR-026 established the federation trust architecture. At the time, federation was not a designed system — it was a future aspiration. BANZA_CERTIFICATION.md's L4 "federation_ready" was a placeholder, not a designed requirement.

ADR-026 subsequently designed federation as an L3 capability. That decision:
- Is implemented in all conformance code
- Is enforced in all contracts
- Is documented in all federation specs
- Passes 79 conformance tests

BANZA_CERTIFICATION.md was simply not updated.

### Consequence of the prior model

Without this ADR:
- An operator reading BANZA_CERTIFICATION.md believes federation requires L4 certification
- The same operator running the federation conformance suite would find it targeting L3
- The same operator reading ADR-026 would find L3 = federation
- Three contradictory answers from three authoritative-looking documents

This contradiction blocks operator onboarding and must be resolved.

---

## Phase 4 — Canonical Level Model

### Decision: ADR-026 governs

ADR-026 is the authoritative ADR for federation trust architecture. It was written specifically to define the federation level threshold. It pre-empts any prior document on this question.

**L3 = Federation Operator.** This is the canonical answer.

BANZA_CERTIFICATION.md is updated by this ADR. All other documents that already say L3 = federation are already correct.

---

### Level 0 — Sandbox Operator

| Field | Value |
|-------|-------|
| Purpose | Protocol reachability verification in a test environment |
| Scope | Single operator, sandbox only, no live settlement rails |
| Dependencies | None |
| Operator ID assigned | At L0 (stable for the operator's lifetime in the network) |

**Capabilities required:**
- Operator manifest served at `/.well-known/banza/operator.json`
- Sandbox health endpoint operational
- `POST /v1/sandbox/fund` and wallet balance query functional
- MON-001 (monetary integer representation — universal rule, all levels)

**Capabilities excluded:**
- Live payment processing
- Cross-operator routing
- Settlement rails

**Evidence required:**
- Conformance suite: health, sandbox isolation
- MON-001 compliance in all responses

**Conformance suites required:** `health`, `wallets`, `transfers` (basic)

---

### Level 1 — Payment Operator

| Field | Value |
|-------|-------|
| Purpose | Consumer and merchant payments within a single operator |
| Scope | Single operator, live environment |
| Dependencies | L0 |

**Capabilities required:**
- All L0 capabilities
- `wallet.consumer` — consumer wallet creation, funding, querying
- `wallet.merchant` — merchant wallet management
- `qr.static` — static QR generation and payment processing
- `p2p.transfer` — @handle-to-@handle consumer transfers

**Invariants required:**
- INV-LEDGER-001 — double-entry balance
- INV-LEDGER-002 — immutable entries
- INV-LEDGER-003 — no floating-point money
- INV-LEDGER-004 — atomic posting
- INV-WALLET-001 — balance consistency
- INV-STL-001 — no money creation
- INV-STL-002 — no negative balances
- INV-IDENT-001 — handle uniqueness
- INV-TRACE-001 — trace propagation

**Capabilities excluded:**
- Dynamic QR (L2+)
- Payment links (L2+)
- Cross-operator routing (L3+)
- Card acquiring (L4)

**Evidence required:**
- All L0 evidence
- Conformance suite: core-payments (28 tests)

**Conformance suites required:** All L0 + `core-payments/`

---

### Level 2 — Settlement Operator

| Field | Value |
|-------|-------|
| Purpose | Full single-operator payment lifecycle including dynamic QR, pull payments, and instant settlement |
| Scope | Single operator, live environment |
| Dependencies | L1 |

**Capabilities required:**
- All L1 capabilities
- `qr.dynamic` — dynamic QR with encoded amount
- `payment_links` — pull-payment URLs
- `settlement.t0` — T+0 (instant) settlement to merchant wallet

**Additional invariants required:**
- INV-QR-001 — QR single-use enforcement
- INV-QR-002 — dynamic QR amount immutability

**Capabilities excluded:**
- Cross-operator routing (L3+)
- Card acquiring (L4)

**Evidence required:**
- All L1 evidence
- Conformance suite: advanced-payments (52 tests)
- `trace_id` on all entities, `GET /traces` endpoint

**Conformance suites required:** All L1 + `advanced-payments/`

---

### Level 3 — Federation Operator

| Field | Value |
|-------|-------|
| Purpose | Cross-operator routing, inter-operator settlement, and automated reconciliation |
| Scope | Multi-operator; requires trust infrastructure (PKI, BRL) |
| Dependencies | L2 |
| Federation eligibility | **This level and above only** |

**Capabilities required:**
- All L2 capabilities
- `cross_operator_routing` — participation in BANZA federation routing
- `reconciliation` — automated ledger reconciliation across operator boundaries
- `payout.batch` — batch inter-operator net settlement via bank rails (EMIS/Multicaixa)

**Operator infrastructure required:**
- Valid BANZA-signed operator certificate (`certification_level >= 3`) served at `/.well-known/banza/certificate.json`
- `supports_federation: true` declared in manifest (INV-TRUST-004)
- `cross_operator_routing: true` declared in manifest
- `POST /federation/route` endpoint operational
- `GET /federation/obligations` endpoint operational
- BRL compliance: operator must not be present in the BANZA Revocation List

**Trust constraints:**
- Certificate lifetime: 90 days maximum (INV-TRUST-002)
- Certificate must be signed by BANZA root key
- Certificate `operator_id` must match manifest `operator_id`
- BRL signature must verify before revocation decisions (INV-TRUST-005)

**Invariants required:**
- All L2 invariants
- INV-TRUST-001 — certificate signature verification
- INV-TRUST-002 — certificate expiry (90-day maximum for L3+)
- INV-TRUST-003 — BRL suspension enforcement
- INV-TRUST-004 — `supports_federation=true` requires L3+ certificate
- INV-TRUST-005 — BRL signature verification (unsigned BRL = absent BRL)
- INV-TRUST-006 — BRL staleness enforcement (max 6 hours)
- INV-FED-001 — trace_id propagation across operators
- INV-FED-002 — obligation created immediately on routing acceptance
- INV-FED-003 — cross_operator_routing capability declared
- INV-FED-004 — routing idempotency
- INV-FED-005 — obligation amount identity
- INV-FED-LEDGER-001 — cross-operator ledger correctness
- INV-FED-RECON-001 — reconciliation trace completeness

**Capabilities excluded:**
- Card acquiring (L4)

**Evidence required:**
- All L2 evidence
- 79/79 FED-CERT, FED-DISC, FED-TRUST, FED-ROUTE, FED-EXEC, FED-OBL, FED-EVT, FED-SETTLE, FED-FAIL tests pass
- Evidence package cryptographically signed by test BANZA root (tamper-evident)

**Conformance suites required:** All L2 + `federation/` (79 tests across 9 suites)

**Per-operator L3 requirements (from ADR-026 §Phase 6):**

| ID | Requirement |
|----|-------------|
| FED-L3-001 | Valid certificate at `certification_level >= 3` |
| FED-L3-002 | Certificate not expired |
| FED-L3-003 | Manifest: `supports_federation: true`, `cross_operator_routing: true` |
| FED-L3-004 | `interop_endpoint` TCP-reachable |
| FED-L3-005 | `certificate.operator_id == manifest.operator_id` |
| FED-L3-006 | Operator not in BRL |
| FED-L3-007 | `POST /federation/route` endpoint operational |
| FED-L3-008 | `GET /federation/obligations` endpoint operational |

---

### Level 4 — Infrastructure Operator

| Field | Value |
|-------|-------|
| Purpose | Card acquiring and highest-tier network participation |
| Scope | Multi-operator (inherits L3 federation); card infrastructure |
| Dependencies | L3 |

**Capabilities required:**
- All L3 capabilities (including full federation)
- `acquiring.emis` — EMIS card acquiring integration

**Additional invariants required:**
- INV-STL-001 (extended) — settlement fee model: `net_minor + fee_minor = gross_minor` exactly
- No-money-creation invariant at card acquiring level

**Capabilities excluded:**
- None. L4 is the highest level.

**Evidence required:**
- All L3 evidence
- Conformance suite: infrastructure (12 files, 88 tests)
- Card acquiring integration evidence

**Conformance suites required:** All L3 + `infrastructure/`

---

## Phase 5 — Progression Rules

### Rule P-001: Levels are strictly cumulative

Certification at level N requires passing all conformance tests for levels 0 through N inclusive. There is no exception.

### Rule P-002: No level skipping

An operator cannot certify directly at L3 without first certifying at L0, L1, and L2. Each level's conformance suite includes all prior level tests.

### Rule P-003: L3 implies L2 implies L1 implies L0

A certificate with `certification_level: 3` proves the operator has passed conformance for all four levels (0, 1, 2, 3). The certificate value is the maximum certified level, not a set.

### Rule P-004: Certification is single-valued

An operator holds exactly one certification level at any time — the highest level at which it has passed all cumulative tests. An L2 operator that passes L3 federation tests becomes an L3 operator; it does not hold both L2 and L3.

### Rule P-005: L3 is the federation eligibility threshold

An operator MUST hold `certification_level >= 3` to:
- Declare `supports_federation: true` in its manifest (INV-TRUST-004)
- Receive a BANZA-signed certificate with federation-capable scope
- Participate as Operator B in any federation routing flow
- Be listed as federation-eligible in the BANZA operator registry

An L2 operator that claims federation eligibility is in protocol violation. The trust engine enforces this via Step 2.5 of the 9-step trust protocol (ADR-026).

### Rule P-006: No downgrade without re-certification

An operator that has been certified at L3 may not claim L3 status after its certificate expires without re-running the full L3 conformance suite. Certificate expiry does not grant L2 status — it grants no certified status until re-certification completes.

### Rule P-007: Certification level is immutable in the certificate

A BANZA-signed certificate states a specific `certification_level`. That value cannot be changed after issuance. If an operator upgrades from L2 to L3, a new L3 certificate is issued; the prior L2 certificate is not modified.

---

## Phase 6 — Federation Alignment

This ADR is fully aligned with ADR-026. No changes to ADR-026 are required or made.

### Points of alignment

| ADR-026 Specification | ADR-028 Confirmation |
|----------------------|---------------------|
| "REQUIRED_LEVEL = 3" for federation routing | L3 is the federation threshold (Rule P-005) |
| INV-TRUST-004: `supports_federation=true` requires L3+ | Confirmed. L3 evidence includes INV-TRUST-004 |
| 90-day maximum certificate lifetime for `certification_level >= 3` | Confirmed. L3 trust constraint |
| FED-L3-001 through FED-L3-014 requirements | Confirmed. All 14 covered by 79-test suite |
| BRL signature verification before revocation decisions | Confirmed. INV-TRUST-005, implemented in trust engine |
| Evidence package tamper-evident signing | Confirmed. ed25519 signed by test BANZA root |

### What ADR-028 does NOT change

- The 9-step trust protocol (ADR-026 §Phase 5)
- All FED-* conformance test IDs and assertions
- All FED-L3-* requirements
- All INV-TRUST-* invariants
- The `certification_level` field schema in `operator-certificate.json`
- All hard-coded level checks in conformance code
- BRL structure, signature model, or verification rules

---

## Phase 7 — BanzAI Alignment

BanzAI is the protocol operating system — the evaluation and guidance system for BANZA. It does not issue certification. It supports operators in achieving certification.

### BanzAI role at each level

| Level | BanzAI capability |
|-------|-------------------|
| L0 | Sandbox environment setup guidance; manifest validation |
| L1 | Conformance test execution against operator URL; invariant verification; failure diagnosis |
| L2 | All L1 + advanced payment conformance; trace structure verification |
| L3 | All L2 + federation conformance suite execution; trust establishment analysis; BRL status check; evidence package generation |
| L4 | All L3 + infrastructure conformance; card acquiring integration guidance |

### What BanzAI must never do

- Issue certification (BANZA issues certification; BanzAI evaluates readiness)
- Sign BANZA root certificates (the production BANZA root key is a BANZA authority artifact)
- Override conformance test results (BanzAI may explain failures; it may not override them)
- Declare an operator certified without passing the conformance suite

### Evidence generation

For L3, BanzAI generates evidence packages signed with the **test BANZA root key** (ephemeral, per-run). This is sufficient for:
- Conformance evaluation
- Certification application submission
- Pre-production readiness assessment

It is NOT sufficient for:
- Operator registry listing
- Live certificate issuance
- Federation routing eligibility in production

The production BANZA root key (blocker #2) is required before evidence packages carry production-grade certification authority. BanzAI's evaluation role is independent of this blocker — BanzAI can fully evaluate L3 readiness today.

### Dependency clarification

```
BANZA (protocol + certification authority)
    ↑
BanzAI (evaluation system)
    ↑
Operators (certification candidates)
```

BanzAI depends on BANZA protocol definitions. BANZA never depends on BanzAI's evaluation output for protocol decisions.

---

## Phase 8 — Website and Documentation Impact

### Pages requiring update

| Page / Document | Current state | Required change |
|----------------|---------------|-----------------|
| `BANZA_CERTIFICATION.md` §Level 3 | "payouts and reconciliation"; no federation | Update to federation-primary definition |
| `BANZA_CERTIFICATION.md` §Level 4 | Includes `federation_ready` capability | Remove `federation_ready` (federation is at L3) |
| Operator onboarding | May reference "L4 for federation" | Update to L3 |
| Public certification page | — | Reflect frozen model |
| BANZA Registry | — | Reflect L3 federation eligibility gate |

### Pages already correct (no change required)

| Page / Document | Status |
|----------------|--------|
| `BANZA_CONFORMANCE.md` | Correct — L3 = manifest + capability declaration |
| `BANZA_REFERENCE.md` | Correct — L3 = Federation Operator |
| `docs/adr/ADR-026-FEDERATION-TRUST-MODEL.md` | Correct — REQUIRED_LEVEL = 3 |
| `contracts/federation/operator-certificate.json` | Correct |
| `contracts/federation/federation-manifest.json` | Correct — L3+ for `supports_federation` |
| `tools/banza-conformance/` | Correct — all level checks match ADR-026 |
| `docs/federation/` | Correct — all federation docs target L3 |

### Migration notes for operators

An operator who read the old `BANZA_CERTIFICATION.md` and believed federation required L4 should be informed:

> Federation certification is at L3. If you have passed L2 conformance and can pass the federation conformance suite (79 tests), you are eligible for L3 certification. You do not need L4 to participate in BANZA federation.

This is strictly good news for operators — the bar is one level lower than they may have believed.

---

## Phase 9 — Decision

### Decision 1: L3 = Federation Operator (CONFIRMED, resolves conflict)

The canonical certification level for federation eligibility is **L3**. This has been implemented in ADR-026 and all conformance infrastructure. BANZA_CERTIFICATION.md is updated to match.

### Decision 2: Level names are frozen

| Level | Name | Frozen |
|-------|------|--------|
| 0 | Sandbox Operator | YES |
| 1 | Payment Operator | YES |
| 2 | Settlement Operator | YES |
| 3 | Federation Operator | YES |
| 4 | Infrastructure Operator | YES |

No renaming of levels is permitted without a superseding ADR.

### Decision 3: Level semantics are frozen

The purpose, capability list, invariant set, and conformance suite requirements for each level are frozen by this ADR. Changes to level semantics require a superseding ADR.

### Decision 4: The `certification_level` integer representation is stable

`certification_level` is an integer 0–4 in all protocol artifacts (certificates, manifests, events). This representation is stable. No alias, string enum, or alternative representation is introduced.

### Decision 5: Progression is strictly cumulative, no skipping

Rules P-001 through P-007 are protocol rules, not recommendations.

### Decision 6: `payout.batch` is an L3 capability

Batch inter-operator settlement via bank rails (EMIS/Multicaixa) is an L3 capability because:
- It is the mechanism for net settlement between federated operators (FED-SETTLE)
- The federation settlement conformance suite (FED-SETTLE-001–010) tests this
- It is not logically separable from reconciliation at the cross-operator boundary

### Decision 7: `federation_ready` is removed as an L4 capability

The capability `federation_ready` was a placeholder in BANZA_CERTIFICATION.md anticipating a future federation feature. That feature is now federation at L3. The placeholder is removed; L4 does not grant additional federation rights beyond L3.

### Decision 8: L4 unique value is card acquiring

The unique capability of L4 over L3 is `acquiring.emis` (EMIS card acquiring integration). L4 operators are also subject to the highest volume limits and full no-money-creation invariant enforcement at the card level.

---

## Rejected Alternatives

### Alternative A: Introduce a new L3.5 level

**Rejected.** Adding a fractional level creates ambiguity in the integer `certification_level` field. Protocol artifacts use integers. A new level between L3 and L4 would require a new level number (which would shift L4 to L5) or a non-integer representation. Neither is acceptable without significant contract changes. The conflict is resolved by alignment, not by adding levels.

### Alternative B: Keep BANZA_CERTIFICATION.md as-is and treat ADR-026 as L4-targeted

**Rejected.** ADR-026 explicitly and repeatedly states REQUIRED_LEVEL = 3. Conformance code enforces `level < 3: reject`. 79 tests target L3. Retroactively re-labeling all of this as L4 would require renaming hundreds of test IDs, all FED-L3-* requirements, all INV-TRUST-* invariants that reference L3+, and the contracts. The cost is enormous; the benefit is zero.

### Alternative C: Keep federation at L4 and add a new "federated routing" sub-level at L3

**Rejected.** This introduces a non-integer certification system and breaks the clean five-level hierarchy. The hierarchy's value lies in its simplicity.

### Alternative D: Rename levels (Foundation, Core, Settlement, Federation, Infrastructure)

**Rejected.** The numeric labels (L0–L4) are already used in contracts, test IDs, and conformance code. The named labels (Sandbox Operator through Infrastructure Operator) are used in user-facing documentation. Both systems coexist cleanly. Introducing a third naming system adds no value and creates migration work.

---

## Dependency Graph

```
L4 (Infrastructure)
    └── depends on L3

L3 (Federation)          ← federation eligibility gate
    ├── depends on L2
    ├── requires: BANZA PKI (certificates, BRL, BANZA root key)
    ├── requires: ADR-026 trust protocol implementation
    └── requires: federation conformance suite (79 tests)

L2 (Settlement)
    └── depends on L1

L1 (Payment)
    └── depends on L0

L0 (Sandbox)             ← entry point; operator_id assigned here
    └── depends on: nothing
```

---

## Certification Matrix

| Capability | L0 | L1 | L2 | L3 | L4 |
|-----------|:--:|:--:|:--:|:--:|:--:|
| Sandbox / health | ✓ | ✓ | ✓ | ✓ | ✓ |
| Wallet consumer | — | ✓ | ✓ | ✓ | ✓ |
| Wallet merchant | — | ✓ | ✓ | ✓ | ✓ |
| Static QR | — | ✓ | ✓ | ✓ | ✓ |
| P2P transfer | — | ✓ | ✓ | ✓ | ✓ |
| Dynamic QR | — | — | ✓ | ✓ | ✓ |
| Payment links | — | — | ✓ | ✓ | ✓ |
| T+0 settlement | — | — | ✓ | ✓ | ✓ |
| Cross-operator routing | — | — | — | ✓ | ✓ |
| Reconciliation | — | — | — | ✓ | ✓ |
| Payout (batch/bank) | — | — | — | ✓ | ✓ |
| Federation certificate | — | — | — | ✓ | ✓ |
| Card acquiring (EMIS) | — | — | — | — | ✓ |

---

## Governance Implications

### This ADR is the authority

For any dispute about what a certification level means, this ADR governs. All other documents are either aligned with this ADR or are out of date and must be updated.

### Future level changes require a new ADR

Any change to:
- The number of levels
- The names of levels
- The capabilities at any level
- The progression rules
- The federation eligibility threshold

…requires a new ADR that supersedes ADR-028. No unilateral documentation change can alter the frozen model.

### Operator communication requirement

When the L3/L4 alignment change is published (BANZA_CERTIFICATION.md updated per this ADR), BANZA must communicate to any operator who was told federation requires L4:

> BANZA certification has been clarified. Federation eligibility is at Level 3, not Level 4. Any operator that has completed Level 2 certification may proceed to Level 3 (Federation) without first achieving Level 4.

---

## Consequences

### Positive

1. **Single source of truth.** No ambiguity exists about what any level means.
2. **Federation threshold is lower than believed.** L2 operators can proceed to L3 directly. The prior BANZA_CERTIFICATION.md may have discouraged L2 operators from attempting federation.
3. **All conformance infrastructure is already correct.** Zero conformance code changes required.
4. **ADR-028 unblocks production blocker #1.** The certification architecture is frozen. Future work (blocker #2: production root key; blocker #3: real two-operator test) can proceed without revisiting level definitions.

### Negative

1. **BANZA_CERTIFICATION.md requires a targeted update** at L3 and L4 sections only. This is minor but necessary.
2. **Operator communication required.** Any operator who was told federation = L4 must be corrected.

### Neutral

1. The numeric level representation (`certification_level` integer 0–4) is unchanged.
2. No conformance test IDs change.
3. No invariant IDs change.
4. No contract field names change.
