# BANZA v1 Operational Transition Plan

**Document ID:** BANZA-V1-TRANSITION-TO-OPERATIONS-001  
**Date:** 2026-06-01  
**Authority:** BANZA-PROTOCOL-COMPLETION-AUDIT-001  
**Status:** ACTIVE  
**Owner:** Fidel Monteiro (Founder)

---

## Context

The BANZA Protocol Completion Audit has concluded with verdict **YES — Protocol is complete (L0–L3 scope)**. Protocol design work is formally closed.

This document defines the transition from **protocol development** to **protocol operations**. Every remaining task is catalogued, classified, and assigned to a program. Protocol work and operational work are now permanently separated.

---

## Part I — Complete Task Inventory

### Classification Key

| Class | Definition |
|-------|------------|
| `PROTOCOL` | Specification, contract, invariant, conformance vector, ADR — defines correctness |
| `OPERATIONS` | Key management, certificate issuance, endpoint operation, SDK releases |
| `INFRASTRUCTURE` | Servers, hosting, endpoints, deployments |
| `DOCUMENTATION` | Stale docs, roadmap corrections, operator-facing guides |
| `GOVERNANCE` | RFC/ADR status, decision records, process changes |
| `FUTURE` | Deferred to v1.1 or later — not required for production launch |

---

### Protocol Tasks

| ID | Task | Severity | Program | Depends on |
|----|------|----------|---------|-----------|
| PROTO-001 | Update RFC-0001/0002/0005 from `status: Draft` to `status: Implemented` with ADR-026 reference | LOW | B | — |
| PROTO-002 | Write L4 conformance vectors (card acquiring, fee model, no-money-creation at L4 scope) — estimated 12–18 tests | MEDIUM | C | — |
| PROTO-003 | Create `contracts/federation/key-manifest.json` from ADR-029 §Phase 6 specification | LOW | A | — |
| PROTO-004 | Update `BANZA_ROADMAP.md` — federation is complete today; roadmap still shows it at H1–H2 2027 | LOW | B | — |
| PROTO-005 | ADR-030 — Key Manifest Contract (formal ADR for the key-manifest.json schema, referenced by ADR-029) | LOW | FUTURE | PROTO-003 |
| PROTO-006 | ADR-031 — Multi-Signature Root Authority (upgrade path for mature federation trust) | LOW | FUTURE | — |
| PROTO-007 | ADR-032 — Protocol Version Negotiation (semantics when v1.0 and v1.1 operators federate) | LOW | FUTURE | — |
| PROTO-008 | DNS and Registry discovery modes (RFC-0005 Direct mode is live; two remaining modes undefined) | LOW | FUTURE | — |
| PROTO-009 | RFC-0006 — Offline Payment Support (genuinely Draft; AOA-native offline wallet authorization) | LOW | FUTURE | — |

---

### Operations Tasks

| ID | Task | Severity | Program | Depends on |
|----|------|----------|---------|-----------|
| OPS-001 | Root key generation ceremony (offline, HSM, ed25519, air-gapped) | **CRITICAL** | A | — |
| OPS-002 | Generate cert-issuing key `banza-cert-YYYYMM`, BRL-issuing key `banza-brl-YYYYMM`, conformance key `banza-evidence-YYYYMM` | **CRITICAL** | A | OPS-001 |
| OPS-003 | Sign initial Key Manifest with root key; publish at `banza.network/.well-known/banza/key-manifest.json` | **CRITICAL** | A | OPS-002 |
| OPS-004 | BRL endpoint live at `banza.network/federation/revocation-list.json` | **HIGH** | A | OPS-002 |
| OPS-005 | BANZA SDK v1.0 release — Key Manifest pinned, production `issuer_key_id` in verification logic | **HIGH** | A | OPS-002 |
| OPS-006 | Enforce `INV-ROOT-001` in conformance runner — reject `test-` key IDs in production mode | **MEDIUM** | A | OPS-002 |
| OPS-007 | First production operator conformance submission (receive, review, sign certificate) | **HIGH** | A | OPS-003+OPS-004+OPS-005+OPS-006 |
| OPS-008 | Define certificate renewal operations process (90-day L3+ lifecycle, monitoring, alerts) | MEDIUM | A | OPS-007 |
| OPS-009 | Define BRL update operations process (who approves suspension, what triggers emergency BRL) | MEDIUM | A | OPS-004 |

---

### Infrastructure Tasks

| ID | Task | Severity | Program | Depends on |
|----|------|----------|---------|-----------|
| INFRA-001 | `banza.network/.well-known/banza/key-manifest.json` — serve with `Cache-Control: max-age=86400` | **CRITICAL** | A | OPS-003 |
| INFRA-002 | `banza.network/federation/revocation-list.json` — serve with `Cache-Control: max-age=21600` (6h) | **HIGH** | A | OPS-004 |
| INFRA-003 | BanzAI production deployment: Qdrant vector store, embedding model, vLLM inference endpoint | HIGH | B | — |
| INFRA-004 | BanzAI protocol knowledge indexing — run `npm run index` against current `~/banza` docs | HIGH | B | INFRA-003 |
| INFRA-005 | Operator registry — public endpoint listing certified operators (operator_id, level, endpoints) | MEDIUM | A | OPS-007 |
| INFRA-006 | Certification portal — self-service conformance submission, status tracking | MEDIUM | FUTURE | OPS-007 |

---

### Documentation Tasks

| ID | Task | Severity | Program | Depends on |
|----|------|----------|---------|-----------|
| DOC-001 | `BANZA_ROADMAP.md` — remove federation from future milestones; reflect completion (same as PROTO-004) | LOW | B | — |
| DOC-002 | `FEDERATION_OPERATOR_QUICKSTART.md` — add production endpoints (real Key Manifest URL, real BRL URL) | LOW | A | OPS-003+OPS-004 |
| DOC-003 | `BANZA_CERTIFICATION.md` — mark L4 as `conformance suite: v1.1` to be honest about current state | LOW | B | — |
| DOC-004 | New: `docs/operations/CERTIFICATE_ISSUANCE_RUNBOOK.md` — step-by-step guide for issuing production certificates | MEDIUM | A | OPS-007 |
| DOC-005 | New: `docs/operations/BRL_OPERATIONS_RUNBOOK.md` — suspension/reinstatement/emergency BRL procedures | MEDIUM | A | OPS-009 |
| DOC-006 | New: `docs/operations/KEY_ROTATION_RUNBOOK.md` — issuing key rotation procedures per ADR-029 lifecycle | MEDIUM | A | OPS-002 |

---

### Governance Tasks

| ID | Task | Severity | Program | Depends on |
|----|------|----------|---------|-----------|
| GOV-001 | RFC-0001 status update: `Draft` → `Implemented` (superseded by ADR-026 §Phase 5) | LOW | B | — |
| GOV-002 | RFC-0002 status update: `Draft` → `Implemented` (superseded by ADR-026 §Phase 6) | LOW | B | — |
| GOV-003 | RFC-0005 status update: `Draft` → `Implemented` (Direct mode, superseded by ADR-026 §Phase 5) | LOW | B | — |
| GOV-004 | RFC-0003 and RFC-0004 review: confirm still Draft or advance | LOW | B | — |
| GOV-005 | Protocol Development closure declaration — formal notice that v1.0 design is frozen | LOW | B | PROTO-001 through PROTO-004 |

---

### Future Tasks (v1.1+)

| ID | Task | Target version | Program |
|----|------|---------------|---------|
| FUTURE-001 | L4 conformance vectors (card acquiring + fee model + no-money-creation at L4) | v1.1 | C |
| FUTURE-002 | ADR-030 — Key Manifest Contract (JSON Schema in `contracts/`) | v1.1 | C |
| FUTURE-003 | ADR-031 — Multi-Signature Root Authority (council upgrade path) | v1.2 | C |
| FUTURE-004 | DNS discovery mode (RFC-0005) | v1.1 | C |
| FUTURE-005 | Registry discovery mode (RFC-0005) | v1.2 | C |
| FUTURE-006 | RFC-0006 — Offline Payment Support | v1.2 | C |
| FUTURE-007 | ADR-032 — Protocol Version Negotiation | v1.1 | C |
| FUTURE-008 | Cross-border settlement (AOA ↔ other currencies) | v2.0 | C |
| FUTURE-009 | INFRA-006 — Self-service certification portal | v1.1 | C |
| FUTURE-010 | COM-003 — Public operator registry | v1.1 | C |

---

## Part II — Three Execution Programs

---

### Program A — Production Launch

**Goal:** First production operator certificate issued.  
**Completion criterion:** At least one operator holds a BANZA-issued production certificate with `issuer_key_id: banza-cert-YYYYMM` (not `test-`), served at a live endpoint, verifiable by any peer using the published Key Manifest.

**Owner:** Fidel Monteiro  
**Dependency chain:** OPS-001 → OPS-002 → {OPS-003, OPS-004, OPS-005} → OPS-006 → OPS-007

#### Task List — Program A

| # | ID | Task | Class | Unblocked after |
|---|----|------|-------|----------------|
| 1 | OPS-001 | Root key generation ceremony | OPERATIONS | — |
| 2 | PROTO-003 | Create `contracts/federation/key-manifest.json` | PROTOCOL | — |
| 3 | OPS-002 | Generate cert-issuing, BRL-issuing, conformance issuing keys | OPERATIONS | OPS-001 |
| 4 | OPS-003 | Sign and publish initial Key Manifest | OPERATIONS | OPS-002 |
| 5 | INFRA-001 | Serve Key Manifest at `banza.network/.well-known/banza/key-manifest.json` | INFRASTRUCTURE | OPS-003 |
| 6 | OPS-004 | Sign and publish initial BRL (empty is valid) | OPERATIONS | OPS-002 |
| 7 | INFRA-002 | Serve BRL at `banza.network/federation/revocation-list.json` | INFRASTRUCTURE | OPS-004 |
| 8 | OPS-005 | BANZA SDK v1.0 — pin Key Manifest, add production `issuer_key_id` verification | OPERATIONS | OPS-002 |
| 9 | OPS-006 | Enforce `INV-ROOT-001` in conformance runner | OPERATIONS | OPS-002 |
| 10 | DOC-002 | Update `FEDERATION_OPERATOR_QUICKSTART.md` with production endpoints | DOCUMENTATION | INFRA-001+INFRA-002 |
| 11 | DOC-004 | `docs/operations/CERTIFICATE_ISSUANCE_RUNBOOK.md` | DOCUMENTATION | — |
| 12 | DOC-005 | `docs/operations/BRL_OPERATIONS_RUNBOOK.md` | DOCUMENTATION | — |
| 13 | DOC-006 | `docs/operations/KEY_ROTATION_RUNBOOK.md` | DOCUMENTATION | — |
| 14 | OPS-008 | Certificate renewal operations process | OPERATIONS | OPS-007 |
| 15 | OPS-009 | BRL update operations process | OPERATIONS | OPS-004 |
| 16 | OPS-007 | First production operator certification | OPERATIONS | 1–9 above |
| 17 | INFRA-005 | Operator registry endpoint | INFRASTRUCTURE | OPS-007 |

**Program A is complete when:** OPS-007 is done. One production certificate exists.

---

### Program B — Validation Studio Separation

**Goal:** BanzAI's validation and guidance capabilities are cleanly separated from BANZA's certification authority. No ambiguity about what BanzAI can do (evaluate, guide, explain) vs what BANZA does (certify, issue, revoke). Protocol documentation reflects the protocol's current state.

**Owner:** Fidel Monteiro  
**Dependency chain:** independent of Program A (runs in parallel)

**What "Validation Studio Separation" means:**

The current state has two certification-adjacent systems in the same repository:
1. `tools/banza-conformance/` — BANZA's conformance suite (the authority — produces pass/fail)
2. `apps/banzai/dist/src/tools/conformance-runner.js` — BanzAI's conformance simulation (guidance — produces readiness analysis)

These are correct by design but their boundary must be explicit and durable:

| System | Role | Can certify? | Can issue? |
|--------|------|:------------:|:-----------:|
| `tools/banza-conformance/run.py` | BANZA conformance suite | **Yes** | No |
| `tools/banza-conformance/run_fed.py` | BANZA federation conformance | **Yes** | No |
| `apps/banzai/tools/conformance-runner` | BanzAI certification copilot | No — guidance only | No |
| BanzAI `/certification/copilot` API | BanzAI readiness analysis | No — inference only | No |

The separation is already architecturally correct. Program B makes it documented and governed.

#### Task List — Program B

| # | ID | Task | Class | Unblocked after |
|---|----|------|-------|----------------|
| 1 | GOV-001 | RFC-0001 status: `Implemented` | GOVERNANCE | — |
| 2 | GOV-002 | RFC-0002 status: `Implemented` | GOVERNANCE | — |
| 3 | GOV-003 | RFC-0005 status: `Implemented` | GOVERNANCE | — |
| 4 | GOV-004 | RFC-0003/0004 review | GOVERNANCE | — |
| 5 | PROTO-001 | RFC files updated with ADR-026 references | PROTOCOL | GOV-001/002/003 |
| 6 | PROTO-004 | `BANZA_ROADMAP.md` reflects federation as complete | PROTOCOL | — |
| 7 | DOC-001 | `BANZA_ROADMAP.md` update (same file, same task) | DOCUMENTATION | — |
| 8 | DOC-003 | `BANZA_CERTIFICATION.md` — L4 marked `conformance suite: v1.1` | DOCUMENTATION | — |
| 9 | INFRA-003 | BanzAI production deployment (Qdrant + vLLM) | INFRASTRUCTURE | — |
| 10 | INFRA-004 | BanzAI knowledge indexing from `~/banza` | INFRASTRUCTURE | INFRA-003 |
| 11 | GOV-005 | Protocol Development closure declaration | GOVERNANCE | 1–8 above |

**Program B is complete when:** GOV-005 is filed. RFC statuses are accurate. BANZA_ROADMAP.md reflects current state. BanzAI is deployed and indexed. The boundary between BanzAI guidance and BANZA certification is documented.

---

### Program C — Future L4 Infrastructure

**Goal:** BANZA Protocol v1.1 supports L4 certification. Card acquiring operators can pass a conformance suite and receive an L4 certificate.

**Owner:** TBD (v1.1 planning)  
**Dependency chain:** Program A completion recommended first (operational experience informs L4 design)

**What L4 requires that doesn't exist today:**

The L4 level ("Infrastructure Operator") adds card acquiring to the L3 federation baseline:
- `acquiring.emis` — EMIS acquiring integration
- `acquiring.multicaixa` — Multicaixa acquiring integration
- `settlement_fee_model` — advanced fee model capability
- No-money-creation invariant at infrastructure scale

None of these have conformance vectors. L4 is defined but not certifiable.

#### Task List — Program C

| # | ID | Task | Class | Depends on |
|---|----|------|-------|-----------|
| 1 | FUTURE-001 | Write L4 conformance vectors (12–18 tests) | PROTOCOL | — |
| 2 | FUTURE-002 | ADR-030 — Key Manifest Contract (`contracts/federation/key-manifest.json` formally) | PROTOCOL | PROTO-003 |
| 3 | FUTURE-003 | ADR-031 — Multi-Signature Root Authority | PROTOCOL | Program A operational experience |
| 4 | FUTURE-004 | DNS discovery mode (RFC-0005) — TXT record lookup for `_banza.<domain>` | PROTOCOL | — |
| 5 | FUTURE-007 | ADR-032 — Protocol Version Negotiation | PROTOCOL | Program A operational experience |
| 6 | FUTURE-006 | RFC-0006 — Offline Payment Support | PROTOCOL | — |
| 7 | FUTURE-009 | Certification portal (self-service) | INFRASTRUCTURE | Program A |
| 8 | FUTURE-010 | Public operator registry | INFRASTRUCTURE | Program A |
| 9 | FUTURE-008 | Cross-border settlement (AOA ↔ other) | PROTOCOL | Program A operational experience |

**Program C is complete when:** L4 conformance suite exists and at least one operator is certified at L4. BANZA Protocol v1.1 is declared.

---

## Part III — Critical Path to First Production Operator Certification

The critical path is the minimum sequence of tasks that must execute serially before a production certificate can be issued. Tasks marked `[PARALLEL]` may execute concurrently.

```
START
  │
  ▼
OPS-001 ── Root key generation ceremony (HSM, offline)
  │
  ▼
OPS-002 ── Generate cert-issuing + BRL-issuing + conformance keys
  │                                │
  ├──────────────────────┬──────────────────────┐
  ▼                      ▼                      ▼
OPS-003              OPS-004               OPS-005 [PARALLEL]
Sign+publish         Sign+publish           SDK v1.0
Key Manifest         Initial BRL            release
  │                      │
  ▼                      │
INFRA-001             INFRA-002 [PARALLEL]
Serve key-manifest    Serve BRL
at banza.network      at banza.network
  │                      │
  └──────────┬───────────┘
             │
             ▼
           OPS-006
           INV-ROOT-001 enforcement in runner
           (reject test- keys in production mode)
             │
             ▼
           OPS-007
           First operator submits conformance results
           BANZA verifies: cert signature, expiry, BRL, invariants
           BANZA signs certificate with banza-cert-YYYYMM key
             │
             ▼
           MILESTONE M3 — First Operator Certified

Non-critical path [PARALLEL to above]:
  PROTO-003 ── key-manifest.json contract file
  DOC-004/005/006 ── operations runbooks
  Program B ── RFC statuses, roadmap, BanzAI deployment
```

**Minimum elapsed time estimate:**

The critical path has 4 serial stages after the key ceremony:
1. Key ceremony → issuing keys (one offline signing session)
2. Issuing keys → Key Manifest + BRL published (one signing + deploy)
3. Infrastructure live → conformance runner updated (code change + deploy)
4. Runner ready → first operator certified (operator preparation time TBD)

Stages 1–3 are entirely within BANZA's control. Stage 4 depends on the first operator's readiness. A first-party certification (the reference operator) can compress stage 4 to hours.

---

## Part IV — Milestone Sequence

---

### M1 — Protocol Complete

**Status: ACHIEVED — 2026-06-01**

| Evidence | Source |
|----------|--------|
| 79/79 federation conformance tests pass | `tools/banza-conformance/run_fed.py` |
| 14/14 real two-operator interoperability scenarios pass | `tools/banza-conformance/run_interop.py` |
| ADR-026 accepted — Federation Trust Model | `docs/adr/ADR-026` |
| ADR-028 accepted — Certification Level Architecture | `docs/adr/ADR-028` |
| ADR-029 accepted — Production Root Architecture | `docs/adr/ADR-029` |
| Completion audit: YES (L0–L3 scope) | `docs/audit/BANZA_PROTOCOL_COMPLETION_AUDIT.md` |
| `make identity-check` PASS | CI gate |

**What M1 means:** The protocol design is frozen. No new ADRs are required before production. No new contracts are required. No new invariants are required. Any operator can implement BANZA correctly today using only public specification documents.

---

### M2 — Production Trust Established

**Status: OPEN**  
**Program:** A  
**Unblocked by:** Nothing — OPS-001 is the first unblocked action in the entire backlog  
**Completion criterion:** Key Manifest is live at `banza.network/.well-known/banza/key-manifest.json`, BRL is live at `banza.network/federation/revocation-list.json`, SDK v1.0 is released

**Deliverables:**
- Root key exists (offline, secured)
- Three issuing keys exist: `banza-cert-YYYYMM`, `banza-brl-YYYYMM`, `banza-evidence-YYYYMM`
- Key Manifest signed and published
- BRL signed and published
- BANZA SDK v1.0 released with Key Manifest pinned
- `INV-ROOT-001` enforced in conformance runner

---

### M3 — First Operator Certified

**Status: OPEN**  
**Program:** A  
**Blocked by:** M2  
**Completion criterion:** One production certificate exists with `issuer_key_id: banza-cert-YYYYMM`, the operator is serving it at `/.well-known/banza/certificate.json`, and a peer can verify it against the published Key Manifest

**Deliverables:**
- Certificate issued (signed by `banza-cert-YYYYMM` key)
- Certificate served publicly
- Peer verification confirmed (manually, or via conformance suite in production mode)
- Certification record created (operator_id, level, issued_at, expires_at)

---

### M4 — BanzAI Operational

**Status: OPEN**  
**Program:** B  
**Unblocked by:** Nothing — independent of Program A  
**Completion criterion:** BanzAI is deployed in production with Qdrant indexed, vLLM serving, and all 8 Protocol OS capabilities functional

**Deliverables:**
- Qdrant collection `banzai_knowledge` indexed with current `~/banza` documents
- Protocol graph built and queryable
- `/certification/copilot` returns L0–L3 readiness analysis against live conformance data
- `/federation/analyze` returns operator compatibility analysis
- RAG benchmark report available at `/rag/stats`
- `MODE=live-ai` operational (not mock)

---

### M5 — Validation Studio Separation Complete

**Status: OPEN**  
**Program:** B  
**Blocked by:** RFC status updates, BANZA_ROADMAP.md update, BANZA_CERTIFICATION.md L4 caveat  
**Completion criterion:** GOV-005 (Protocol Development closure declaration) is filed. BanzAI's role as evaluator (not certifier) is explicitly documented everywhere.

**Deliverables:**
- RFC-0001/0002/0005 show `status: Implemented`
- BANZA_ROADMAP.md reflects federation as complete today
- BANZA_CERTIFICATION.md marks L4 conformance suite as v1.1
- GOV-005 closure declaration filed
- `docs/audit/BANZA_PROTOCOL_COMPLETION_AUDIT.md` is the closure evidence

**What this milestone means:** Every engineer, operator, or auditor who reads the BANZA repository sees an accurate picture. The protocol section is locked. The operations section is active. The future section is labelled. BanzAI guides; BANZA certifies; the line is explicit and documented.

---

### M6 — BANZA v1.0 Public Launch

**Status: OPEN**  
**Programs:** A + B  
**Blocked by:** M2, M3, M5  
**Completion criterion:** BANZA Protocol v1.0 is publicly announced. External operators can begin L1–L3 certification. BanzAI is available to guide them.

**Deliverables:**
- At least M3 (one certified operator) — demonstrates the system works end-to-end
- BanzAI operational (M4) — new operators have guided onboarding
- Protocol documentation accurate (M5) — no stale future-tense content about things that are already done
- Public announcement: "BANZA Protocol v1.0 is available. L1–L3 certification is open."
- Conformance suite available at `github.com/banza-protocol/banza` (public)
- SDK packages published (`@banza/sdk`, `github.com/banza-protocol/go-sdk`, etc.)

---

## Part V — State Summary

### Protocol development: CLOSED

The protocol design is frozen. The following categories of work are complete:

- All financial invariants (INV-LEDGER, INV-WALLET, INV-SETTLE, INV-IDEM, INV-RECON, INV-QR)
- All trust invariants (INV-TRUST-001 through INV-TRUST-007)
- All federation invariants (INV-FED-001 through INV-FED-007, extensions, INV-ROOT-001 through INV-ROOT-006)
- All certification levels defined (L0–L3 certifiable; L4 defined and deferred to v1.1)
- All federation contracts (operator-certificate, routing, obligation, event, manifest)
- Federation trust model (ADR-026)
- Certification architecture (ADR-028)
- Root key architecture (ADR-029)
- Conformance suite L0–L2 (51 vectors)
- Federation conformance suite (79 tests)
- Real two-operator interoperability (14/14)

### Operational execution: ACTIVE

The critical path (OPS-001 through OPS-007) is unblocked. The first action is the root key ceremony. Everything downstream is deterministic.

### Future work: DEFERRED

L4, DNS discovery, offline payments, cross-border, multi-sig root, version negotiation — all deferred to v1.1 or later. None is a v1.0 requirement. All are documented in Program C.

---

## Appendix — Task Register Summary

| Program | Protocol | Operations | Infrastructure | Documentation | Governance | Future |
|---------|:--------:|:----------:|:--------------:|:-------------:|:----------:|:------:|
| A — Production Launch | 1 | 9 | 4 | 4 | — | — |
| B — Validation Studio | 2 | — | 2 | 2 | 5 | — |
| C — Future L4 | — | — | 2 | — | — | 9 |
| **Total** | **3** | **9** | **8** | **6** | **5** | **9** |

Program A: 18 tasks. Blocked only by the root key ceremony.  
Program B: 11 tasks. All unblocked today.  
Program C: 11 tasks. Deferred. No urgency.

**Total active work: 29 tasks across Programs A and B.**
