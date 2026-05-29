# BanzamIA

Protocol Intelligence Platform for the Banzami ecosystem.

## Overview

BanzamIA is the cognitive interface of the Banzami protocol — a Fastify 5 API backend that powers the BanzamIA modules on the docs site. It provides:

- **Chat** — streaming LLM responses grounded in protocol knowledge
- **Protocol Graph Explorer** — interactive navigation of typed protocol nodes and relationships
- **Agentic Protocol Research** — multi-step research across RAG + graph with contradiction detection
- **Certification Copilot** — operator readiness analysis against L0–L4 certification levels
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
│   ├── routes/
│   │   ├── ask.ts              # POST /ask
│   │   ├── certification-copilot.ts  # POST /certification/copilot
│   │   ├── chat.ts             # POST /chat (streaming)
│   │   ├── graph.ts            # GET /graph/*
│   │   ├── knowledge.ts        # GET /knowledge/search
│   │   ├── rag-stats.ts        # GET /rag/stats
│   │   ├── research.ts         # POST /research
│   │   └── status.ts           # GET /status
│   ├── store/
│   │   └── qdrant.ts           # Qdrant client (search, upsert, scroll)
│   └── tools/
│       ├── certification-copilot.ts  # L0–L4 readiness analysis
│       ├── conformance.ts
│       ├── manifest.ts
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

## Certification Levels

| Level | Name | Key capability |
|-------|------|----------------|
| L0 | Reference-compatible | Valid manifest + sandbox environment |
| L1 | Protocol-compatible | Wallets + Transfers + QR |
| L2 | Trace-compatible | Trace IDs + event correlation |
| L3 | Federation-ready | Cross-operator + federation |
| L4 | Settlement-compatible | Payment requests + webhooks + settlement |

## Trust Through Measurement

BanzamIA's quality metrics are public. Run `npm run rag:eval` to generate a benchmark report in `reports/`. The Quality Dashboard at `/banzamia` → **Quality Dashboard** shows live retrieval analytics.

> Tools determine truth. AI explains truth.
