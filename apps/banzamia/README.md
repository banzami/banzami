# BanzamIA

Protocol Operating System for the Banzami ecosystem.

## Overview

BanzamIA is the Protocol Operating System of Banzami — a Fastify 5 API backend that powers the BanzamIA modules on the docs site. It provides:

- **Chat** — streaming LLM responses grounded in protocol knowledge
- **Protocol Graph Explorer** — interactive navigation of typed protocol nodes and relationships
- **Agentic Protocol Research** — multi-step research across RAG + graph with contradiction detection
- **Certification Copilot** — operator readiness analysis against L0–L4 certification levels
- **Protocol Simulator** — what-if analysis: simulate capability changes before implementing
- **Federation Intelligence** — operator-to-operator compatibility analysis with blocking issue detection
- **Protocol Memory** — continuous journey history for each operator across sessions
- **Operator Digital Twin** — protocol-aware virtual representation aggregating all operator dimensions
- **Quality Dashboard** — public retrieval metrics and benchmark results

## Architecture

```
apps/banzamia/
├── src/
│   ├── agent/
│   │   └── researcher.ts       # Multi-step research agent (plan → retrieve → graph → synthesise)
│   ├── analytics/
│   │   ├── tracker.ts          # In-memory query analytics singleton
│   │   └── coverage.ts         # Knowledge base coverage analysis
│   ├── evals/
│   │   ├── retrieval-eval.ts   # Retrieval metrics (MRR, Precision@K, Recall@K)
│   │   └── adversarial-eval.ts # Protocol truth validation
│   ├── graph/
│   │   └── protocol-graph.ts   # Typed graph (10 node types, 8 edge types)
│   ├── orchestrator/           # Task routing + model providers + pipeline
│   ├── rag/                    # Embedding, chunking, indexing, search
│   ├── memory/
│   │   └── operator-memory.ts  # In-memory operator journey store (singleton Map)
│   ├── routes/
│   │   ├── ask.ts              # POST /ask
│   │   ├── certification-copilot.ts  # POST /certification/copilot
│   │   ├── chat.ts             # POST /chat (streaming)
│   │   ├── digital-twin.ts     # POST /digital-twin
│   │   ├── federation.ts       # POST /federation/analyze
│   │   ├── graph.ts            # GET /graph/*
│   │   ├── knowledge.ts        # GET /knowledge/search
│   │   ├── memory.ts           # GET|POST|DELETE /memory/:operatorId
│   │   ├── rag-stats.ts        # GET /rag/stats
│   │   ├── research.ts         # POST /research
│   │   ├── simulate.ts         # POST /simulate
│   │   └── status.ts           # GET /status
│   ├── store/
│   │   └── qdrant.ts           # Qdrant client (search, upsert, scroll)
│   └── tools/
│       ├── certification-copilot.ts  # L0–L4 readiness analysis
│       ├── conformance.ts
│       ├── digital-twin.ts     # buildDigitalTwin() — aggregates all operator dimensions
│       ├── federation-intelligence.ts  # analyzeFederation() — 0–100 compatibility score
│       ├── manifest.ts
│       ├── protocol-simulator.ts  # runSimulation() — deterministic what-if analysis
│       └── trace.ts
├── scripts/
│   ├── graph-cli.ts            # npm run graph:index
│   ├── coverage-cli.ts         # npm run rag:coverage
│   └── eval-cli.ts             # npm run rag:eval
└── tests/                      # 107 unit tests (vitest)
```

## Setup

```bash
cd apps/banzamia
cp .env.example .env       # configure QDRANT_URL, VLLM_URL if live mode
npm install
npm run dev
```

The server listens on port 4001 by default.

## Modes

| Mode | Variable | Behaviour |
|------|----------|-----------|
| `mock` | `MODE=mock` (default) | Returns deterministic mock responses — no model or Qdrant required |
| `live-ai` | `MODE=live-ai` | Full pipeline: Qdrant retrieval + vLLM model generation |

## CLI Commands

```bash
npm run index           # Ingest protocol documents into Qdrant
npm run graph:index     # Build protocol graph from markdown cross-references
npm run rag:coverage    # Analyse knowledge base coverage by source type
npm run rag:eval        # Run retrieval benchmark (MRR, Precision@K, Recall@K)
npm test                # Run test suite (107 tests)
```

## API Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /status | System status (Qdrant, model, graph) |
| POST | /ask | Single question → grounded answer |
| POST | /chat | Streaming answer (SSE) |
| GET | /knowledge/search | RAG search with ranked results |
| GET | /graph/stats | Protocol graph statistics |
| GET | /graph/node/:id | Node detail with neighbours |
| GET | /graph/search | Search nodes by query |
| GET | /graph/related/:id | BFS-related nodes |
| GET | /graph/path | Shortest path between two nodes |
| GET | /rag/stats | Combined RAG + graph + analytics snapshot |
| POST | /research | Multi-step agentic research |
| POST | /certification/copilot | Certification readiness analysis |
| POST | /simulate | What-if simulation: capability changes → readiness delta |
| POST | /federation/analyze | Operator-to-operator compatibility analysis |
| GET | /memory | List all operators with memory |
| GET | /memory/:operatorId | Full memory for one operator |
| POST | /memory/:operatorId | Create or update operator memory |
| DELETE | /memory/:operatorId | Delete operator memory |
| POST | /digital-twin | Build full operator digital twin dashboard |

## Certification Levels

| Level | Name | Key capability |
|-------|------|----------------|
| L0 | Sandbox Operator | Valid manifest + sandbox environment |
| L1 | Payment Operator | Wallets + Transfers + QR |
| L2 | Settlement Operator | Trace IDs + event correlation |
| L3 | Federation Operator | Cross-operator + federation |
| L4 | Infrastructure Operator | Payment requests + webhooks + settlement |

## Protocol Operating System Capabilities

| Capability | Module | Description |
|------------|--------|-------------|
| **Compreender** | RAG + Knowledge Base + Protocol Graph | Retrieves relevant protocol context |
| **Explicar** | Chat + Research Agent + Citations | Answers with verifiable evidence |
| **Validar** | Conformance + Manifest + Trace | Confirms protocol compliance |
| **Simular** | Protocol Simulator + What-If | Projects impact of changes before implementing |
| **Prever** | Memory + Trajectory + Analytics | Anticipates operator trajectory |
| **Guiar** | Digital Twin + Recommendations | Guides operator with personalised context |
| **Certificar** | Certification Copilot + L0–L4 Roadmap | Guides operator through each level |
| **Federar** | Federation Intelligence + Federation Graph | Analyses compatibility between operators |

## Trust Through Measurement

BanzamIA's quality metrics are public. Run `npm run rag:eval` to generate a benchmark report in `reports/`. The Quality Dashboard at `/banzamia` → **Quality Dashboard** shows live retrieval analytics.

> Tools determine truth. AI explains truth.
