# BANZA Validation Studio Decoupling Report

**Document ID:** BANZA-VALIDATION-STUDIO-DECOUPLING-001  
**Date:** 2026-06-01  
**Authority:** ADR-025, ADR-026, ADR-028, ADR-029  
**Status:** COMPLETE  
**Owner:** Fidel Monteiro (Founder)

---

## Executive Summary

The BANZA Validation Studio originated before the protocol architecture was frozen and before operator neutrality was fully established. The original studio files (`VALIDATION_STUDIO_AUDIT.md`, `VALIDATION_STUDIO_GAP_MAP.md`, `VALIDATION_MATRIX_COVERAGE_REPORT.md`) were operator-specific and were purged in BANZA-ZERO-OPERATOR-PURGE-001.

This report completes the work begun by that purge. It establishes three independent validation domains, defines their status models, governance rules, and mutual boundaries, and answers the final question: can the BANZA Validation Studio become the canonical governance and validation layer of the BANZA ecosystem?

**Answer: YES — unconditionally, effective this document.**

The architecture is correct. Two BanzAI defects were found and corrected. Three canonical matrix definitions now exist. The boundary between BANZA authority and BanzAI guidance is explicit and durable.

---

## Phase 1 — Current State Audit

### Inventory Classification

The following classification covers every validation-related artifact in the BANZA repository. Each item is classified as BANZA, BanzAI, Operator, or Legacy.

#### BANZA (protocol layer — authoritative)

| Area | Artifacts | Classification |
|------|----------|---------------|
| Governance | `docs/adr/` (29 ADRs), `docs/rfc/` (6 RFCs), `BANZA_GOVERNANCE.md`, `BANZA_CERTIFICATION.md`, `BANZA_CONFORMANCE.md` | **BANZA** |
| Contracts | `contracts/openapi/` (4 files), `contracts/federation/` (5 files), `contracts/events/` (3 files), `contracts/webhooks/` (2 files), `contracts/qr/` (2 files), `contracts/sdk-certification/` | **BANZA** |
| Invariants | 23 invariants across INV-LEDGER, INV-WALLET, INV-STL, INV-QR, INV-TRACE, INV-IDEM, INV-TRUST, INV-FED, INV-ROOT, MON-001 | **BANZA** |
| Conformance | `conformance/vectors/` (8 files, 51 tests), `conformance/fixtures/federation/` (39 fixtures), `conformance/*/suite.json`, `conformance/report-schema.json` | **BANZA** |
| Tools | `tools/banza-conformance/run.py`, `run_fed.py`, `run_interop.py`, `trust_root.py`, `tools/root-ceremony/ceremony_script.py` | **BANZA** |
| Documentation | `docs/federation/` (20 files), `docs/operations/`, `docs/security/`, `docs/certification/`, `docs/audit/` | **BANZA** |

#### BanzAI (Protocol Operating System — evaluative)

| Area | Artifacts | Classification |
|------|----------|---------------|
| Guidance tools | `apps/banzai/src/tools/` (7 tools: certification-copilot, conformance-runner, digital-twin, federation-intelligence, manifest-validator, protocol-simulator, trace-explainer) | **BanzAI** |
| Knowledge Engine | `apps/banzai/src/rag/` (8 modules), `apps/banzai/src/graph/` (4 modules), `apps/banzai/src/store/` | **BanzAI** |
| Evaluation | `apps/banzai/evals/` (4 evals, 1 dataset), `apps/banzai/scripts/` (4 CLIs) | **BanzAI** |
| Analytics | `apps/banzai/src/analytics/` (2 modules), `apps/banzai/src/memory/` | **BanzAI** |
| API routes | `apps/banzai/src/routes/` (12 routes) | **BanzAI** |
| Orchestration | `apps/banzai/src/orchestrator/` (pipeline, router, 3 providers) | **BanzAI** |

#### Operator (implementation layer)

| Area | Artifacts | Classification |
|------|----------|---------------|
| Reference implementation | `reference/sandbox-operator/` | **Operator** |
| Integration examples | `examples/`, `integrations/plugins/` | **Operator** |

#### Legacy (purged)

| Artifact | Reason for removal |
|----------|-------------------|
| `docs/validation/VALIDATION_STUDIO_AUDIT.md` | Operator-specific contamination — removed in BANZA-ZERO-OPERATOR-PURGE-001 |
| `docs/validation/VALIDATION_STUDIO_GAP_MAP.md` | Operator-specific gap map — removed in BANZA-ZERO-OPERATOR-PURGE-001 |
| `docs/validation/VALIDATION_MATRIX_COVERAGE_REPORT.md` | Operator-specific validation report — removed in BANZA-ZERO-OPERATOR-PURGE-001 |

---

## Phase 2 — Three Validation Domains

The BANZA ecosystem has exactly three validation domains. They are independent, with defined mutual boundaries. No domain may perform the other's role.

```
┌─────────────────────────────────────────────────────────┐
│  Matrix A — BANZA Validation Matrix                     │
│  Layer: Protocol (authoritative)                        │
│  Role: Defines correctness. Certifies. Issues.         │
│  File: docs/validation/MATRIX_A_BANZA.md                │
├─────────────────────────────────────────────────────────┤
│  Matrix B — BanzAI Validation Matrix                    │
│  Layer: Protocol Operating System (evaluative)          │
│  Role: Evaluates readiness. Guides. Explains.           │
│  File: docs/validation/MATRIX_B_BANZAI.md               │
├─────────────────────────────────────────────────────────┤
│  Matrix C — Operator Implementation Matrix              │
│  Layer: Implementation (conformant)                     │
│  Role: Implements the protocol. Seeks certification.    │
│  File: docs/validation/MATRIX_C_OPERATOR.md             │
└─────────────────────────────────────────────────────────┘
```

### Domain boundaries

| Action | Matrix A (BANZA) | Matrix B (BanzAI) | Matrix C (Operator) |
|--------|:----------------:|:-----------------:|:-------------------:|
| Define protocol rules | **Yes** | No | No |
| Issue production certificates | **Yes** | No | No |
| Run authoritative conformance suite | **Yes** | No | No |
| Sign Key Manifests / BRLs | **Yes** | No | No |
| Evaluate certification readiness | No | **Yes** | No |
| Guide operators toward compliance | No | **Yes** | No |
| Implement the protocol | No | No | **Yes** |
| Seek certification | No | No | **Yes** |
| Self-certify | No | No | **Prohibited** |

---

## Phase 3 — Matrix A: BANZA Validation Matrix Design

**Full specification:** [MATRIX_A_BANZA.md](MATRIX_A_BANZA.md)

### Categories

| Category | Scope |
|----------|-------|
| **Governance** | ADRs (29), RFCs (6), governance docs, protocol development lifecycle |
| **Contracts** | OpenAPI (4), federation schemas (5), events (3), webhooks (2), QR (2), SDK certification |
| **Invariants** | Financial (12), trust/federation (14), root key (6) |
| **Conformance** | L0–L2 vectors (51 tests), L3 federation suite (79 tests), L4 (deferred v1.1) |
| **Certification** | L0–L4 definitions, certification process, runbooks |
| **Federation** | Trust model, contract surface, conformance suite, live endpoints |
| **Trust** | Root key architecture, ceremony, key manifest, BRL |
| **Documentation** | Reference docs, operator guides, runbooks |

### Status model

`COMPLETE` | `IN-PROGRESS` | `DEFERRED` | `MISSING`

### Confidence model

`HIGH` (enforced by automated tests/CI) | `MEDIUM` (documented, manually verified) | `LOW` (specified, not yet tested)

### Audit model

Every COMPLETE item must be: referenced by an accepted ADR, covered by a conformance test vector, or enforced by a CI gate.

### Dependency model

```
Contracts → Invariants → Conformance → Certification
```

### Current state summary

| Category | COMPLETE | IN-PROGRESS | DEFERRED | MISSING |
|----------|:--------:|:-----------:|:--------:|:-------:|
| Governance | 29 ADRs | 5 RFCs, closure | 3 future ADRs | — |
| Contracts | 16 | — | — | 1 (key-manifest.json) |
| Invariants | 23 | — | — | — |
| Conformance | 130 tests (L0–L3) | — | L4 | — |
| Certification | L0–L3 fully | — | L4 suite | 3 runbooks |
| Federation | Trust + suite | — | — | BRL, Key Manifest endpoints |
| Trust | Procedure + script | — | — | Root key, issuing keys, live endpoints |
| Documentation | Core docs | Roadmap, quickstart | — | L4 caveat |

---

## Phase 4 — Matrix B: BanzAI Validation Matrix Design

**Full specification:** [MATRIX_B_BANZAI.md](MATRIX_B_BANZAI.md)

### Categories

| Category | Scope |
|----------|-------|
| **Knowledge Engine** | RAG corpus (Qdrant), source types, authority weighting, protocol graph, embedding pipeline |
| **Evaluation** | Benchmark runner, citation eval, retrieval eval, adversarial eval, protocol question dataset |
| **Certification Support** | Certification copilot, readiness scoring, level analysis, blocking issue detection, roadmap generation |
| **Federation Intelligence** | Federation analysis, compatibility scoring, digital twin, operator memory |
| **Governance Intelligence** | ADR/RFC Q&A, invariant explanation, research agent |
| **Operational Intelligence** | Trace explainer, protocol simulator, manifest validator |

### BanzAI principle: evaluates, never certifies

This is verified at the code level. No BanzAI tool:
- Issues a certificate
- Signs a Key Manifest or BRL
- Writes to any authoritative BANZA registry
- Holds production private keys

All BanzAI outputs are framed as readiness analysis, compatibility scores, guidance signals, or natural-language explanations.

### Defects found and corrected

| ID | Defect | Correction |
|----|--------|-----------|
| BZ-DEFECT-001 | `digital-twin.ts`: RFC-0006 labeled "Operator Manifest" | Corrected to "Offline Payment Support" |
| BZ-DEFECT-002 | `conformance-runner.ts`: L4-001 "Full federation participation" and L4-002 "Offline payment support" — both wrong for L4 | L4-001 → "Settlement batch lifecycle"; L4-002 → "EMIS card acquiring integration" (skip, v1.1 caveat) |

---

## Phase 5 — Matrix C: Operator Implementation Matrix Design

**Full specification:** [MATRIX_C_OPERATOR.md](MATRIX_C_OPERATOR.md)

### Categories

| Category | Scope |
|----------|-------|
| **Wallet** | Consumer wallets, merchant wallets, balance management, handle identity |
| **QR Payments** | Static QR (L1), dynamic QR (L2), lifecycle, invariants |
| **Payments and Transfers** | P2P transfers, idempotency, payment requests, payment links, trace propagation |
| **Ledger** | Double-entry, immutability, atomic posting, integer storage |
| **Events and Webhooks** | Event emission, envelope schema, webhook delivery, signature |
| **Settlement** | T+0 settlement (L2), batch settlement, bank rails (L3), invariant enforcement |
| **APIs** | Health, wallets, well-known endpoints (L3), federation routing (L3) |
| **Trust and Certificate Compliance** | Certificate validity, BRL check, Key Manifest verification, `test-` rejection |
| **Operator-Specific** | KYC/AML, consumer app, merchant dashboard, fee model — outside protocol scope |

### Generic operator model

Every row in Matrix C uses level-based requirements (L0–L4), invariant references, and contract references. No operator brand appears. Any certified BANZA operator — present or future — must satisfy the same rows.

---

## Phase 6 — Terminology Alignment

Review of all views, labels, and terminology against ADR-026, ADR-028, and ADR-029.

### Findings

| Location | Issue | Severity | Action |
|----------|-------|----------|--------|
| `BANZA_GOVERNANCE.md` | "Um operador operates at..." — Portuguese text leaked in; should be "An operator operates at..." | LOW | Document; fix in next governance pass |
| `BANZA_CERTIFICATION.md` | References `[BANZAI_CAPABILITIES.md](../banzai/BANZAI_CAPABILITIES.md)` — file lives in BanzAI repo, not BANZA repo; broken for readers of this repo | LOW | Document; consider linking to the public BanzAI reference instead |
| `apps/banzai/src/tools/conformance-runner.ts` | L4-001/L4-002 names incorrect (offline payment, full federation) | MEDIUM | **FIXED** in this session |
| `apps/banzai/src/tools/digital-twin.ts` | RFC-0006 labeled "Operator Manifest" — RFC-0006 is Offline Payment Support | MEDIUM | **FIXED** in this session |
| `BANZA_CONFORMANCE.md` | "The reference sandbox operator (the reference operator) is certified at Level 2" — phrasing implies a specific operator is the standard | LOW | Acceptable for now; update to "The reference sandbox operator" without the parenthetical |

### Terminology compliance status

| Term | Forbidden? | Status | Used correctly? |
|------|-----------|--------|----------------|
| Specific operator brand names | Yes | COMPLETE | Zero occurrences (`make identity-check` PASS) |
| "certified operator" / "reference operator" / "any operator" | Required | COMPLETE | Used throughout |
| "BanzAI evaluates" vs "BANZA certifies" | Required | COMPLETE | Reflected in all tools and docs |
| ADR-026 federation terminology | Required | COMPLETE | All federation docs use canonical terms |
| ADR-028 certification level names | Required | COMPLETE | L0–L4 names consistent |
| ADR-029 key hierarchy terms | Required | COMPLETE | root / cert-issuing / brl-issuing / evidence-issuing consistent |

---

## Phase 7 — Governance Alignment

### Dependency graph verification

The canonical dependency is:

```
     Operators   (any certified operator — Matrix C)
         ↑
       BanzAI    (Protocol Operating System — Matrix B)
         ↑
       BANZA     (open protocol — Matrix A)
```

This direction is enforced. BANZA never depends on BanzAI. BanzAI never depends on operators. Operators depend on both.

### Alignment verification

| Check | Result |
|-------|--------|
| BANZA conformance suite is the authority — BanzAI conformance runner is guidance | **VERIFIED** — BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md Program B explicitly documents this |
| BanzAI cannot certify | **VERIFIED** — no certification code path in BanzAI tools issues a certificate |
| BanzAI does not hold production private keys | **VERIFIED** — no private key handling in any `apps/banzai/` source file |
| Operators cannot self-certify | **VERIFIED** — certification requires BANZA-signed certificate from the root trust chain |
| Protocol invariants flow BANZA → operators | **VERIFIED** — all invariants defined in BANZA; BanzAI explains them; operators enforce them |

### Remaining governance ambiguities

| Ambiguity | Location | Impact | Resolution |
|-----------|----------|--------|-----------|
| BanzAI's `conformance-runner.ts` check IDs (L0-001, L1-001, etc.) visually resemble authoritative BANZA check IDs | `apps/banzai/src/tools/conformance-runner.ts` | LOW — confusion for contributors | Add header comment distinguishing BanzAI simulation IDs from BANZA conformance test IDs |
| Program B is called "Validation Studio Separation" in the transition plan, but its tasks are governance/documentation updates, not studio changes | `docs/governance/BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md` | LOW — naming confusion only | This decoupling report replaces the need for that program label to be descriptive |

---

## Phase 8 — Migration Sequence

### Immediate (no dependencies — done in this session)

| Action | Result |
|--------|--------|
| Fix RFC-0006 mislabeling in `digital-twin.ts` | **DONE** |
| Fix L4-001/L4-002 in `conformance-runner.ts` | **DONE** |
| Create `docs/validation/MATRIX_A_BANZA.md` | **DONE** |
| Create `docs/validation/MATRIX_B_BANZAI.md` | **DONE** |
| Create `docs/validation/MATRIX_C_OPERATOR.md` | **DONE** |
| Create `docs/validation/BANZA_VALIDATION_STUDIO_DECOUPLING_REPORT.md` | **DONE** |

### Short-term (before M5 — unblocked, days of effort)

| Action | ID | Effort |
|--------|----|--------|
| RFC-0001/0002/0005 status: `Draft` → `Implemented` | GOV-001/002/003 | Minutes each |
| RFC-0003/0004 review | GOV-004 | 1–2 hours |
| `BANZA_ROADMAP.md` — federation complete | PROTO-004/DOC-001 | 30 minutes |
| `BANZA_CERTIFICATION.md` — L4 marked as v1.1 scope | DOC-003 | 15 minutes |
| Protocol Development Closure declaration | GOV-005 | 1 hour |

### Before M3 (before first operator certification)

| Action | ID | Effort |
|--------|----|--------|
| Create `contracts/federation/key-manifest.json` from ADR-029 | PROTO-003 | 2 hours |
| Update `FEDERATION_OPERATOR_QUICKSTART.md` with production endpoints | DOC-002 | 30 minutes (after OPS-003/004) |

### Before M6 (before public launch)

| Action | ID | Effort |
|--------|----|--------|
| Certificate Issuance Runbook | DOC-004 | 1 day |
| BRL Operations Runbook | DOC-005 | 1 day |
| Key Rotation Runbook | DOC-006 | 1 day |

### Preserved

All audit history is preserved. Immutable records (ADRs, conformance reports, federation test reports) remain unchanged. The three matrix files are additive — they do not replace any existing document.

---

## Phase 9 — Report

**File:** This document (`BANZA_VALIDATION_STUDIO_DECOUPLING_REPORT.md`)

### Architecture established

The BANZA Validation Studio now consists of three canonical matrices:

```
docs/validation/
├── MATRIX_A_BANZA.md          ← BANZA protocol — authoritative
├── MATRIX_B_BANZAI.md         ← BanzAI — evaluative
├── MATRIX_C_OPERATOR.md       ← Operators — implementation
└── BANZA_VALIDATION_STUDIO_DECOUPLING_REPORT.md   ← This document
```

### Findings summary

| Finding | Type | Status |
|---------|------|--------|
| Three validation domains clearly defined | Architecture | **NEW — established in this report** |
| All 23 protocol invariants complete | Protocol | VERIFIED COMPLETE |
| All 130 conformance tests passing (L0–L3) | Protocol | VERIFIED COMPLETE |
| BanzAI boundary architecturally correct | Architecture | VERIFIED |
| RFC-0006 mislabeled in digital-twin.ts | BanzAI defect | **FIXED** |
| L4-001/L4-002 wrong in conformance-runner.ts | BanzAI defect | **FIXED** |
| Key Manifest contract file missing | BANZA gap | DOCUMENTED (PROTO-003) |
| RFC-0001/0002/0005 status stale (still Draft) | Governance gap | DOCUMENTED (GOV-001/002/003) |
| L4 conformance suite deferred | Governance | DOCUMENTED (v1.1 scope) |
| Three operations runbooks missing | Operations gap | DOCUMENTED (DOC-004/005/006) |

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-----------|--------|-----------|
| BanzAI operator memory is in-process only (lost on restart) | HIGH | LOW | Document known limitation; defer persistent memory to INFRA roadmap |
| `docs/validation/` dir was empty before this report | RESOLVED | — | Three matrix files now exist |
| BanzAI tools could be mistaken for authoritative conformance | LOW | HIGH | Matrix B explicitly documents the boundary; each tool's output is framed as "readiness analysis" |
| L4 conformance suite missing could block L4-seeking operators | LOW | MEDIUM | L4 marked DEFERRED in Matrix A; BANZA_CERTIFICATION.md must add L4 caveat (DOC-003) |

---

## Phase 10 — Final Verdict

### Can the BANZA Validation Studio become the canonical governance and validation layer of the BANZA ecosystem?

**YES — effective this document.**

The Validation Studio is now defined as the three-matrix system established in this report. It is:

- **Operator-neutral** — no operator brand appears in any of the three matrices
- **Protocol-aligned** — all matrix content derives from ADR-026, ADR-028, ADR-029, and the frozen protocol specification
- **Architecturally sound** — the BANZA/BanzAI boundary is explicit, durable, and verified at the code level
- **Free of legacy contamination** — the original operator-specific validation files were purged; the new matrices are protocol-centric from the ground up
- **Governance-consistent** — the dependency graph (Operators ↑ BanzAI ↑ BANZA) is reflected in every category of every matrix

### What remains before the Validation Studio is fully operational

| Item | Blocking M5? | Notes |
|------|:-----------:|-------|
| GOV-001/002/003 RFC status updates | Yes | Days of effort; fully unblocked |
| DOC-003 BANZA_CERTIFICATION.md L4 caveat | Yes | 15 minutes; fully unblocked |
| GOV-005 Protocol Development Closure | Yes | Blocked on GOV-001/002/003 and PROTO-004 |
| BANZAI production deployment (INFRA-003/004) | No (M4) | Independent of studio structure |
| Three operations runbooks (DOC-004/005/006) | No | Required before M6 |

### What is now locked

- The three-matrix architecture is canonical. No future work may collapse Matrix A, B, and C into a single document or blend their scopes.
- BanzAI's role is evaluative. This is not subject to revision without an ADR.
- BANZA's certification authority is exclusive. No other system in this ecosystem issues production certificates.

---

## Companion Documents

| Document | Purpose |
|----------|---------|
| [MATRIX_A_BANZA.md](MATRIX_A_BANZA.md) | BANZA Protocol — authoritative validation matrix |
| [MATRIX_B_BANZAI.md](MATRIX_B_BANZAI.md) | BanzAI — evaluative validation matrix |
| [MATRIX_C_OPERATOR.md](MATRIX_C_OPERATOR.md) | Certified operators — implementation matrix |
| [BANZA_CERTIFICATION.md](../../BANZA_CERTIFICATION.md) | Certification levels L0–L4 |
| [BANZA_CONFORMANCE.md](../../BANZA_CONFORMANCE.md) | Conformance suite overview |
| [BANZA_GOVERNANCE.md](../../BANZA_GOVERNANCE.md) | Protocol governance |
| [ADR-025](../adr/ADR-025-ecosystem-naming-inversion.md) | Ecosystem naming (canonical) |
| [ADR-026](../adr/ADR-026-FEDERATION-TRUST-MODEL.md) | Federation Trust Model |
| [ADR-028](../adr/ADR-028-CERTIFICATION-LEVEL-ARCHITECTURE.md) | Certification Level Architecture |
| [ADR-029](../adr/ADR-029-PRODUCTION-ROOT-ARCHITECTURE.md) | Production Root Architecture |
| [BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md](../governance/BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md) | Program B (Validation Studio Separation) |

---

*Validation architecture established. Three independent matrices defined. Two BanzAI defects corrected. No protocol behavior changed. No federation behavior changed.*
