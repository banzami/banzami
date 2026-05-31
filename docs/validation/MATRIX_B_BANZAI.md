# Matrix B — BanzAI Validation Matrix

**Document ID:** BANZA-VALIDATION-MATRIX-B-001  
**Date:** 2026-06-01  
**Authority:** ADR-025, ADR-028  
**Layer:** BanzAI Protocol Operating System (evaluative)  
**Status:** CANONICAL

---

## Purpose

Matrix B defines the validation scope of the BanzAI layer. BanzAI is the Protocol Operating System — it evaluates, guides, explains, and supports operators in understanding and achieving BANZA compliance. BanzAI never certifies, never issues certificates, and never holds production private keys.

This matrix tracks what BanzAI can do and where it is deployed.

---

## The Non-Negotiable BanzAI Boundary

| Action | BanzAI | BANZA |
|--------|:------:|:-----:|
| Run authoritative conformance suite | No | **Yes** |
| Issue production certificates | No | **Yes** |
| Sign Key Manifests | No | **Yes** |
| Sign BRLs | No | **Yes** |
| Certify operators | No | **Yes** |
| Hold production private keys | No | **Yes** |
| Analyze certification readiness | **Yes** | No |
| Guide operators toward compliance | **Yes** | No |
| Simulate protocol scenarios | **Yes** | No |
| Explain protocol rules | **Yes** | No |
| Assess federation compatibility | **Yes** | No |

**This boundary is an architectural invariant, not a configuration option.**  
*Authority: ADR-025, ADR-028, BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md Program B*

---

## Status Model

| Status | Definition |
|--------|-----------|
| `COMPLETE` | Implemented and operational in at least dev mode |
| `IN-PROGRESS` | Implemented; pending production deployment or live data |
| `DEFERRED` | Planned; not yet implemented |
| `DEFECT` | Implemented with incorrect behavior — must be corrected |

---

## Category 1: Knowledge Engine

The Knowledge Engine is BanzAI's protocol corpus — the indexed, searchable representation of all BANZA specification documents. All BanzAI guidance is grounded in this corpus.

| Component | Location | Status | Note |
|-----------|----------|--------|------|
| Source type taxonomy (16 types) | `apps/banzai/src/rag/types.ts` | COMPLETE | reference, accepted_rfc, accepted_adr, openapi, conformance, certification, invariant, manifest_schema, glossary, banzai_doc, architecture_doc, readme, sdk_doc, website, draft_rfc |
| Authority weighting model | `apps/banzai/src/rag/authority.ts` | COMPLETE | 1.00 (reference) → 0.50 (unknown); freshness decay with 180-day half-life |
| RAG chunker | `apps/banzai/src/rag/chunker.ts` | COMPLETE | — |
| RAG indexer | `apps/banzai/src/rag/indexer.ts` | COMPLETE | Runs against `~/banza` docs |
| RAG search | `apps/banzai/src/rag/search.ts` | COMPLETE | — |
| RAG context builder | `apps/banzai/src/rag/context.ts` | COMPLETE | — |
| RAG loader | `apps/banzai/src/rag/loader.ts` | COMPLETE | — |
| Embedding pipeline | `apps/banzai/src/rag/embedding/` | COMPLETE | Factory supports local/remote/mock providers |
| Protocol graph (semantic) | `apps/banzai/src/graph/` | COMPLETE | Indexer, retrieval, store |
| Qdrant vector store | `apps/banzai/src/store/qdrant.ts` | COMPLETE | Collection: `banzai_knowledge` |
| Knowledge indexed in production | — | IN-PROGRESS | Requires production Qdrant (INFRA-003/004) |
| Coverage CLI | `apps/banzai/scripts/coverage-cli.ts` | COMPLETE | — |
| RAG stats endpoint | `apps/banzai/src/routes/rag-stats.ts` | COMPLETE | — |

**Source authority hierarchy (for retrieval scoring):**
```
reference (1.00) > accepted_rfc (0.95) = accepted_adr (0.90) = openapi (0.90) >
conformance (0.85) = certification (0.85) = invariant (0.85) = manifest_schema (0.85) >
glossary (0.80) = banzai_doc (0.80) > architecture_doc (0.75) > readme (0.70) = sdk_doc (0.70) >
website (0.60) > draft_rfc (0.50)
```

---

## Category 2: Evaluation

BanzAI's evaluation pipeline measures the quality of its own knowledge retrieval and guidance. These are meta-evaluations — they evaluate BanzAI, not operators.

| Component | Location | Status | Note |
|-----------|----------|--------|------|
| Benchmark runner | `apps/banzai/evals/benchmark-runner.ts` | COMPLETE | — |
| Citation eval | `apps/banzai/evals/citation-eval.ts` | COMPLETE | Verifies RAG answers cite real docs |
| Retrieval eval | `apps/banzai/evals/retrieval-eval.ts` | COMPLETE | Measures recall of protocol content |
| Adversarial eval | `apps/banzai/evals/adversarial-eval.ts` | COMPLETE | Tests against misleading queries |
| Protocol question dataset | `apps/banzai/evals/datasets/protocol-questions.json` | COMPLETE | BANZA-specific question bank |
| Eval CLI | `apps/banzai/scripts/eval-cli.ts` | COMPLETE | — |
| Coverage analytics | `apps/banzai/src/analytics/coverage.ts` | COMPLETE | — |
| Evaluation tracker | `apps/banzai/src/analytics/tracker.ts` | COMPLETE | — |
| Eval tests | `apps/banzai/tests/eval.test.ts` | COMPLETE | — |
| Production eval pipeline running | — | IN-PROGRESS | Requires INFRA-003/004 |

---

## Category 3: Certification Support

BanzAI provides readiness analysis and guidance toward certification. It does not certify.

| Component | Location | Status | Note |
|-----------|----------|--------|------|
| Certification copilot | `apps/banzai/src/tools/certification-copilot.ts` | COMPLETE | Returns readiness analysis, never a certificate |
| Readiness scoring (0–100) | Inside copilot | COMPLETE | Score = met requirements / total requirements |
| Level status analysis (L0–L4) | Inside copilot | COMPLETE | Achieved / partial / blocked per level |
| Blocking issue detection | Inside copilot | COMPLETE | Manifest safety violations flagged |
| Roadmap generation | Inside copilot | COMPLETE | L0→L1→L2→L3→L4 upgrade paths |
| Certification copilot API route | `apps/banzai/src/routes/certification-copilot.ts` | COMPLETE | — |
| Protocol simulator | `apps/banzai/src/tools/protocol-simulator.ts` | COMPLETE | Simulates impact of proposed changes |
| Manifest validator | `apps/banzai/src/tools/manifest-validator.ts` | COMPLETE | Structural + semantic validation of operator/QR/payment-link manifests |
| Simulation API route | `apps/banzai/src/routes/simulate.ts` | COMPLETE | — |

**What the copilot explicitly does NOT do:**
- Issue a certificate
- Commit to a certification result
- Replace the BANZA conformance suite as the final arbiter

---

## Category 4: Federation Intelligence

BanzAI analyzes federation compatibility between operators. It does not approve or deny federation.

| Component | Location | Status | Note |
|-----------|----------|--------|------|
| Federation analysis | `apps/banzai/src/tools/federation-intelligence.ts` | COMPLETE | Compatibility score, blocking issues, missing capabilities |
| Digital twin | `apps/banzai/src/tools/digital-twin.ts` | COMPLETE | Operator profile: certification + federation + memory + invariants + RFCs |
| Operator memory | `apps/banzai/src/memory/operator-memory.ts` | COMPLETE | In-process store — not persistent across restarts |
| Operator memory API route | `apps/banzai/src/routes/memory.ts` | COMPLETE | — |
| Federation analysis API route | `apps/banzai/src/routes/federation.ts` | COMPLETE | — |
| Digital twin API route | `apps/banzai/src/routes/digital-twin.ts` | COMPLETE | — |
| Persistent operator memory (database) | — | DEFERRED | Current implementation uses in-process Map |

**Boundary note:** BanzAI's federation analysis produces a "compatibility score" and "federation_ready" flag. These are guidance signals. The actual federation authorization remains with the BANZA trust infrastructure (Key Manifest + BRL + certificate chain).

---

## Category 5: Governance Intelligence

BanzAI enables natural-language query of BANZA governance documents: ADRs, RFCs, invariant definitions, certification criteria.

| Component | Location | Status | Note |
|-----------|----------|--------|------|
| Knowledge API route | `apps/banzai/src/routes/knowledge.ts` | COMPLETE | — |
| Research API route | `apps/banzai/src/routes/research.ts` | COMPLETE | — |
| Ask API route | `apps/banzai/src/routes/ask.ts` | COMPLETE | RAG-backed Q&A |
| Chat API route | `apps/banzai/src/routes/chat.ts` | COMPLETE | — |
| Researcher agent | `apps/banzai/src/agent/researcher.ts` | COMPLETE | — |
| Graph API route | `apps/banzai/src/routes/graph.ts` | COMPLETE | — |
| Governance docs indexed in Qdrant | — | IN-PROGRESS | Requires INFRA-004 |

---

## Category 6: Operational Intelligence

BanzAI provides protocol-level diagnostics: trace explanation, event analysis, and status monitoring.

| Component | Location | Status | Note |
|-----------|----------|--------|------|
| Trace explainer | `apps/banzai/src/tools/trace-explainer.ts` | COMPLETE | Event timeline, causal chain analysis, anomaly detection |
| Status API route | `apps/banzai/src/routes/status.ts` | COMPLETE | — |
| LLM orchestration pipeline | `apps/banzai/src/orchestrator/pipeline.ts` | COMPLETE | — |
| LLM router | `apps/banzai/src/orchestrator/router.ts` | COMPLETE | — |
| LLM providers (vLLM, mock) | `apps/banzai/src/orchestrator/providers/` | COMPLETE | — |
| Production vLLM deployment | — | IN-PROGRESS | INFRA-003 |

---

## Category 7: BanzAI Defects Found in This Audit

These defects were identified during BANZA-VALIDATION-STUDIO-DECOUPLING-001 and corrected.

| ID | File | Defect | Correction | Status |
|----|------|--------|-----------|--------|
| BZ-DEFECT-001 | `apps/banzai/src/tools/digital-twin.ts` | RFC-0006 labeled "Operator Manifest" — RFC-0006 is "Offline Payment Support" (FUTURE-006) | Title corrected to "Offline Payment Support"; relevance changed from 'manifest' to 'offline' | **FIXED** |
| BZ-DEFECT-002 | `apps/banzai/src/tools/conformance-runner.ts` | L4-001 "Full federation participation" and L4-002 "Offline payment support" — both incorrect; L4 is Infrastructure Operator (card acquiring), conformance suite is v1.1 scope | L4-001 → "Settlement batch lifecycle"; L4-002 → "EMIS card acquiring integration" with `skip` result and v1.1 caveat | **FIXED** |

---

## Deployment Status

| Environment | Status | Note |
|-------------|--------|------|
| Development (mock mode) | COMPLETE | All tools operational with mock LLM provider |
| Production (Qdrant + vLLM) | IN-PROGRESS | INFRA-003 and INFRA-004 required |
| Knowledge indexed | IN-PROGRESS | INFRA-004: run `npm run index` against current `~/banza` |

**Milestone:** M4 — BanzAI Operational (Program B)

---

## Summary

| Category | COMPLETE | IN-PROGRESS | DEFERRED | DEFECT |
|----------|:--------:|:-----------:|:--------:|:------:|
| Knowledge Engine | 13 | 2 | — | — |
| Evaluation | 8 | 1 | — | — |
| Certification Support | 9 | — | — | — |
| Federation Intelligence | 6 | — | 1 | — |
| Governance Intelligence | 5 | 1 | — | — |
| Operational Intelligence | 5 | 1 | — | — |
| Defects | — | — | — | 2 (both fixed) |

**BanzAI boundary: VERIFIED CORRECT** — BanzAI evaluates. BANZA certifies.
