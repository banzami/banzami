# Canonical Identity Consolidation Report

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Executed by:** BANZA-NAMING-INVERSION-STEP-008  
**Status:** Complete

---

## Canonical Identity (Final)

| Entity | Role | Must never be called |
|--------|------|----------------------|
| **Banza** | Open financial protocol · Infrastructure kernel · Certification · Federation · Governance · Settlement · Conformance | wallet · consumer app · merchant app · checkout · mobile experience |
| **Banzami** | Reference operator · Main product · Consumer experience · Merchant experience · Wallet · Checkout · Banzami Business · QR experience | Protocol · Infrastructure · Governance · Federation · Certification authority |
| **BanzAI** | Protocol Operating System | Chatbot · AI Assistant · Knowledge Search Tool · Documentation Search · Protocol Agent · Protocol Intelligence |
| **banzami.org** | Domain only — preserved permanently | — |

---

## Fixes Applied

### BanzamIA repo (`/Users/fm65/BanzamIA`)

| Location | Field | Before | After | Risk |
|----------|-------|--------|-------|------|
| `prompts/system.md:3` | System prompt identity | `"the intelligence layer..."` | `"the Protocol Operating System..."` | CRITICAL — sent to AI model |
| `prompts/system.md:80` | Persona tagline | `"You are infrastructure intelligence."` | `"You are the Protocol Operating System."` | HIGH |
| `CONTRIBUTING.md:3` | Project description | `"AI-native orchestration and intelligence layer"` | `"the Protocol Operating System"` | MEDIUM |
| `apps/cli/src/index.ts:14` | CLI description | `"BanzamIA — Protocol intelligence for the Banzami ecosystem"` | `"BanzAI — Protocol Operating System for the Banza ecosystem"` | HIGH |
| `apps/cli/package.json:4` | Package description | `"BanzamIA CLI — Protocol intelligence for Banzami operators..."` | `"BanzAI CLI — Protocol Operating System for Banza operators..."` | MEDIUM |
| `apps/cli/src/commands/ask.ts:9` | Command description | `"Ask BanzamIA a protocol question"` | `"Ask BanzAI a protocol question"` | MEDIUM |
| `apps/cli/src/commands/ask.ts:70` | Error message | `"Is the BanzamIA API running?"` | `"Is the BanzAI API running?"` | MEDIUM |
| `apps/api/src/index.ts:91` | Startup log | `` `BanzamIA API  http://localhost:${PORT}` `` | `` `BanzAI API    http://localhost:${PORT}` `` | MEDIUM |
| `apps/api/src/providers/mock.ts:12` | Mock response header | `*[BanzamIA — ${taskType}...` | `*[BanzAI — ${taskType}...` | HIGH — user-visible |
| `apps/api/src/providers/mock.ts:271` | Mock overview heading | `## Banzami Protocol — Overview` | `## Banza Protocol — Overview` | HIGH — user-visible |
| `apps/api/src/providers/mock.ts:273` | Mock overview body | `"Banzami is a programmable financial infrastructure protocol"` | `"Banza is an open programmable financial infrastructure protocol"` | HIGH — user-visible |
| `apps/api/src/data/knowledge-corpus.ts:187` | ADR-012 content | `"BanzamIA enforces this"` | `"BanzAI enforces this"` | HIGH — AI grounding |
| `apps/api/src/data/knowledge-corpus.ts:196` | **ADR-016 snippet** | `"Banzami = org/infra. Banza = product. BanzamIA = AI layer."` | `"Banza = open financial protocol/kernel. Banzami = reference operator/product. BanzAI = Protocol Operating System. ADR-025 supersedes ADR-016."` | **CRITICAL — AI grounding data** |
| `apps/api/src/data/knowledge-corpus.ts:197` | **ADR-016 content** | Full ADR-016 pre-inversion model | Full ADR-025 canonical model | **CRITICAL — AI grounding data** |
| `apps/api/src/data/knowledge-corpus.ts:198` | ADR-016 keywords | `['ADR-016', 'brand', 'Banzami', 'Banza', 'BanzamIA', 'naming']` | `['ADR-025', 'ADR-016', 'brand', 'Banza', 'Banzami', 'BanzAI', 'naming', 'naming inversion']` | HIGH |
| `apps/api/src/data/knowledge-corpus.ts:136` | Operator snippet | `"Operators implement the Banzami protocol"` | `"Operators implement the Banza protocol"` | HIGH — AI grounding |
| `apps/api/src/data/knowledge-corpus.ts:137` | Operator content | `"entity implementing Banzami protocol"` | `"entity implementing Banza protocol"` | HIGH — AI grounding |
| `apps/api/src/data/knowledge-corpus.ts:251` | API paths title | `"Banzami Protocol API Endpoints"` | `"Banza Protocol API Endpoints"` | MEDIUM |
| `apps/api/src/data/knowledge-corpus.ts:255` | API paths content | `"Banzami protocol API paths"` | `"Banza protocol API paths"` | MEDIUM |
| `apps/web/app/layout.tsx:11` | Site title | `"BanzAI — Financial Infrastructure Intelligence"` | `"BanzAI — Protocol Operating System"` | HIGH — SEO |
| `apps/web/app/layout.tsx:15` | Site description | `"the intelligence layer"` | `"the Protocol Operating System"` | HIGH — SEO |
| `apps/web/components/chat/ChatInterface.tsx:12` | Welcome message | `"the intelligence layer"` | `"the Protocol Operating System"` | HIGH — user-visible |
| `apps/web/app/flows/page.tsx:7` | Page description | `"Banzami protocol flows"` | `"Banza protocol flows"` | MEDIUM |

**Commits:** `11df1c9`, `cb3531f`  
**Pushed to:** github.com/banzami/banzamia

---

### Banzami kernel repo (`/Users/fm65/Banzami`)

| Location | Field | Before | After | Risk |
|----------|-------|--------|-------|------|
| `README.md:91` | Diagram top label | `BANZAMI` | `BANZA` | HIGH — first thing devs read |
| `README.md:112` | Diagram bottom-left label | `BANZA` | `Banzami` | HIGH — inverted |
| `README.md:113` | Diagram bottom-left subtitle | `First Operator` | `Reference Operator` | MEDIUM |
| `README.md:112` | Diagram bottom-right label | `BanzamIA` | `BanzAI` | HIGH |
| `apps/banzamia/src/orchestrator/pipeline.ts:26` | System prompt — docs | `"You are BanzamIA, the AI-native agent for the Banzami open payment protocol."` | `"You are BanzAI, the Protocol Operating System of the Banza open financial protocol."` | **CRITICAL — sent to AI** |
| `apps/banzamia/src/orchestrator/pipeline.ts:36` | System prompt — code | `"You are BanzamIA, specialising in Banzami SDK code generation."` | `"You are BanzAI, specialising in Banzami SDK code generation."` | HIGH |
| `apps/banzamia/src/orchestrator/pipeline.ts:44` | System prompt — reasoning | `"...Banzami payment network"` | `"...Banza protocol"` | HIGH |
| `apps/banzamia/src/orchestrator/pipeline.ts:52` | System prompt — validation | `"You are BanzamIA, helping with Banzami protocol validation."` | `"You are BanzAI, helping with Banza protocol validation."` | **CRITICAL** |
| `apps/banzamia/src/orchestrator/pipeline.ts:60` | System prompt — certification | `"You are BanzamIA, assisting with Banzami operator certification."` | `"You are BanzAI, assisting with Banza operator certification."` | **CRITICAL** |
| `apps/banzamia/src/orchestrator/pipeline.ts:68` | System prompt — trace | `"You are BanzamIA, analysing Banzami protocol traces."` | `"You are BanzAI, analysing Banza protocol traces."` | **CRITICAL** |
| `apps/banzamia/src/orchestrator/providers/mock.ts:10` | Mock docs response | `"Based on the Banzami protocol documentation"` | `"Based on the Banza protocol documentation"` | HIGH |
| `apps/banzamia/src/orchestrator/providers/mock.ts:11` | Mock code response | `"BanzamIA code generation"` | `"BanzAI code generation"` | MEDIUM |
| `apps/banzamia/src/orchestrator/providers/mock.ts:12` | Mock reasoning | `"Banzami payment network"` | `"Banza protocol"` | MEDIUM |
| `apps/banzamia/src/tools/trace-explainer.ts:81` | Error description | `"not in the Banzami protocol specification"` | `"not in the Banza protocol specification"` | MEDIUM |
| `conformance/operators/suite.json:2` | Suite spec | `"Banzami Operator Conformance Suite v1.0"` | `"Banza Operator Conformance Suite v1.0"` | HIGH |
| `conformance/operators/suite.json:3` | Suite description | `"...implementing the Banzami protocol..."` | `"...implementing the Banza protocol..."` | HIGH |
| `conformance/report-schema.json:35` | Schema description | `"Banzami protocol version being tested against."` | `"Banza protocol version being tested against."` | MEDIUM |
| `conformance/manifests/schema.json:32` | Schema description | `"The Banzami protocol version this operator implements"` | `"The Banza protocol version this operator implements"` | MEDIUM |
| `apps/banzamia/evals/datasets/protocol-questions.json` | Eval questions | 20 questions: `"What is the Banzami protocol?"`, BIA category "BanzamIA" | Banza protocol + BanzAI | HIGH — AI evaluation |

**Commit:** `993f9ab`  
**Pushed to:** github.com/banzami/banzami

---

### Banza docs repo (`/Users/fm65/Banza`)

| Location | Field | Before | After | Risk |
|----------|-------|--------|-------|------|
| `docs/glossary.md:70` | BanzAI definition | `"The AI-native Protocol Agent...An 8-module interface..."` | `"The Protocol Operating System...16 specialized modules..."` | HIGH — canonical docs |
| `docs/index.md:155` | Ecosystem tree | `"BanzamIA (AI layer)"` | `"BanzAI (Protocol Operating System)"` | HIGH |
| `docs/index.md:174` | Terminology table | `"BanzAI | The AI-native Protocol Agent"` | `"BanzAI | Protocol Operating System"` | HIGH |
| `docs/banzamia/overview.md:13` | BanzAI identity | `"an **AI-native Protocol Agent**"` | `"the **Protocol Operating System**"` | HIGH |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md:105` | ASCII diagram label | `BANZAMIA` | `BANZAI` | HIGH |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md:106` | ASCII diagram subtitle | `(AI-native Protocol Agent)` | `(Protocol Operating System)` | HIGH |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md:117` | Applications row | `Banza (consumer mobile) · Banza Business (merchant) · Banza Checkout` | `Banzami (consumer mobile) · Banzami Business (merchant) · Banzami Checkout` | HIGH |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md:124` | Brand table header | `"Per ADR-016:"` | `"Per ADR-025 (supersedes ADR-016):"` | HIGH |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md:128` | Brand table — Banza row | `"Organisation, protocol, ecosystem, infrastructure, governance"` | `"Open financial protocol — kernel, ledger, certification, federation, governance"` | HIGH |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md:129` | Brand table — Banzami row | `"Consumer payment product (primary reference implementation)"` | `"Reference operator and main product — consumer app, wallet, QR, checkout, Banzami Business"` | HIGH |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md:130` | Brand table — BanzAI row | `"AI-native Protocol Agent"` | `"Protocol Operating System — 16 modules, 8 capabilities"` | HIGH |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md:132` | Tagline | `` `Banzami constrói a infraestrutura. Banza move o dinheiro.` `` | `` `Banza constrói a infraestrutura. Banzami move o dinheiro.` `` | **CRITICAL — inverted pre-ADR-025 tagline** |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md:525` | Section 11.2 diagram | `BanzamIA` | `BanzAI` | MEDIUM |
| `apps/docs/components/banzamia/BanzamIAChat.tsx:381` | Chat placeholder | `"protocolo Banzami"` | `"protocolo Banza"` | MEDIUM — user-visible |
| `apps/docs/components/banzamia/modules/KnowledgeModule.tsx:56` | Module description | `"Banzami protocol docs"` | `"Banza protocol docs"` | MEDIUM — user-visible |
| `apps/docs/data/operators.json` | Operator descriptions (4) | `"Banzami protocol"` | `"Banza protocol"` | HIGH — public registry |
| `apps/docs/lib/banzamia-client.ts:940` | Glossary summary | `"Banzami protocol terms"` | `"Banza protocol terms"` | MEDIUM |

**Commit:** `29ca3ff`  
**Pushed to:** github.com/banzami/banza  
**Deployed:** `./deploy.sh docs-frontend` — production updated

---

## Deferred Items (Require Architectural Decisions)

These items contain the legacy naming but require code/infrastructure changes beyond safe copy fixes. They are tracked for Waves 4–9.

### Wave 4 — Code identifiers (component names)

| Item | Location | Current | Target |
|------|----------|---------|--------|
| React component | `apps/docs/components/banzamia/BanzamIAApp.tsx` | `BanzamIAApp` | `BanzAIApp` |
| React component | `apps/docs/components/banzamia/BanzamIAChat.tsx` | `BanzamIAChat` | `BanzAIChat` |
| React component | `apps/docs/components/banzamia/BanzamIAIcon.tsx` | `BanzamIAIcon` | `BanzAIIcon` |
| React component | `apps/docs/components/banzamia/BanzamIASidebar.tsx` | `BanzamIASidebar` | `BanzAISidebar` |
| React component | `apps/docs/components/banzamia/BanzamIASourcesPanel.tsx` | `BanzamIASourcesPanel` | `BanzAISourcesPanel` |
| Page component | `apps/docs/app/banzamia/page.tsx` | `BanzamIAPage()` | `BanzAIPage()` |
| Tailwind comment | `apps/docs/tailwind.config.ts:13` | `"BanzamIA light institutional theme"` | `"BanzAI light institutional theme"` |

### Wave 5a — Environment variables

| Variable | Used in | Target |
|----------|---------|--------|
| `BANZAMIA_MODE` | BanzamIA API, docker-compose, Banzami README | `BANZAI_MODE` |
| `BANZAMIA_PORT` | docker-compose | `BANZAI_PORT` |
| `BANZAMIA_QDRANT_URL` | BanzamIA API, docker-compose | `BANZAI_QDRANT_URL` |
| `BANZAMIA_EMBEDDING_*` | docker-compose | `BANZAI_EMBEDDING_*` |
| `BANZAMIA_VLLM_URL` | BanzamIA API, docker-compose | `BANZAI_VLLM_URL` |
| `BANZAMIA_MODEL_*` | BanzamIA API, docker-compose | `BANZAI_MODEL_*` |
| `BANZAMIA_ALLOWED_ORIGINS` | BanzamIA API | `BANZAI_ALLOWED_ORIGINS` |
| `BANZAMIA_CONFORMANCE_RUNNER_PATH` | BanzamIA conformance tool | `BANZAI_CONFORMANCE_RUNNER_PATH` |
| `BANZAMIA_REFERENCE_OPERATOR_URL` | BanzamIA trace explainer | `BANZAI_REFERENCE_OPERATOR_URL` |
| `BANZAMIA_QWEN_URL` | BanzamIA vLLM provider | `BANZAI_QWEN_URL` |
| `BANZAMIA_API_URL` | BanzamIA web app, CLI | `BANZAI_API_URL` |
| `NEXT_PUBLIC_BANZAMIA_API_URL` | Banza docs frontend | `NEXT_PUBLIC_BANZAI_API_URL` |

### Wave 5b — API route paths

| Path | File | Target |
|------|------|--------|
| `/banzamia/*` | BanzamIA Fastify router | `/banzai/*` |
| `/sobre-banzamia` | Banza docs `[section]` route | `/sobre-banzai` |

### Wave 5c — Wire format (protected, requires ADR)

| Identifier | Status |
|------------|--------|
| `BANZAMI:` QR prefix | Protected — requires separate ADR |
| `BANZAMI-SBX:` QR prefix | Protected — requires separate ADR |
| `/.well-known/banzami/` | Protected — requires separate ADR |

### Wave 9 — File and directory renames

| Current | Target |
|---------|--------|
| `apps/banzamia/` (Banzami repo) | `apps/banzai/` |
| `docker/banzamia/` | `docker/banzai/` |
| `apps/docs/lib/banzamia-client.ts` | `apps/docs/lib/banzai-client.ts` |
| `apps/docs/app/banzamia/` (route dir) | `apps/docs/app/banzai/` |

### Package names (requires npm scope coordination)

| Package | Current | Target |
|---------|---------|--------|
| BanzamIA CLI | `@banzami/banzamia-cli` | `@banzami/banzai-cli` |
| BanzamIA root | `@banzami/banzamia` | `@banzami/banzai` |

---

## Validation Results

| Check | Result |
|-------|--------|
| `BanzamIA` in BanzAI UI human-visible text | ✓ Zero (web layout, chat, flows page) |
| `BanzamIA` in BanzAI system prompts | ✓ Zero |
| `BanzamIA` in knowledge corpus content (user-facing) | ✓ Zero |
| `BanzamIA` in conformance suite descriptions | ✓ Zero |
| `BanzamIA` in eval question text | ✓ Zero |
| `Banzamia Protocol` / `Banzami protocol` in UI copy | ✓ Zero (all Banza protocol) |
| `AI-native Protocol Agent` in live docs | ✓ Zero |
| `intelligence layer` as product definition | ✓ Zero |
| `Banzami constrói a infraestrutura` (pre-inversion tagline) | ✓ Fixed to `Banza constrói a infraestrutura` |
| ADR-016 brand model in knowledge corpus | ✓ Replaced with ADR-025 model |
| Domain `banzami.org` preserved | ✓ Unchanged |
| `@banza` identity namespace preserved | ✓ Unchanged |
| `Banzami Lda` / `Organização Banzami` preserved | ✓ Unchanged |
| `BANZAMI:` wire format preserved | ✓ Unchanged |
| `/.well-known/banzami/` preserved | ✓ Unchanged |
| Docs site deployed | ✓ `./deploy.sh docs-frontend` complete |
| BanzamIA repo committed + pushed | ✓ `cb3531f` |
| Banzami kernel committed + pushed | ✓ `993f9ab` |
| Banza docs committed + pushed | ✓ `29ca3ff` |

---

## Remaining Occurrence Analysis

### BanzamIA strings still present (code identifiers — deferred)

| Count | Pattern | Reason |
|-------|---------|--------|
| 5 | `BanzamIA*.tsx` component names | Wave 4 code rename |
| 14+ | `BANZAMIA_*` env var names | Wave 5a rename |
| 2 | `/banzamia` route paths | Wave 5b rename |
| 1 | `@banzami/banzamia-cli` package name | Wave 9 |
| 2 | `docker/banzamia/` directory | Wave 9 |

### "Intelligence layer" strings still present

| Location | Context | Status |
|----------|---------|--------|
| `docs/banzamia/architecture.md` | Technical architecture doc (dev-facing) | Flagged — update in next pass |
| Audit files (`/docs/audit/`) | Historical audit records | Intentional — historical |
| Wave 3 migration plan | Migration documentation | Intentional — historical |

---

## Notes

- **ADR-016 knowledge corpus entry** was the most critical fix: the BanzAI AI system was being grounded with factually wrong brand data (Banzami=infra, Banza=product, BanzamIA=AI). It has been replaced with the ADR-025 canonical model. This affects every AI-generated response about brand architecture.
- **AI system prompts** (6 prompts in `pipeline.ts`) were sending `BanzamIA` and `Banzami protocol` to the language model. All updated to `BanzAI` and `Banza protocol`.
- **The pre-inversion tagline** `Banzami constrói a infraestrutura. Banza move o dinheiro.` appeared in `BANZAMI_ECOSYSTEM_REFERENCE.md` with brands swapped. Fixed to `Banza constrói a infraestrutura. Banzami move o dinheiro.`
- **BanzAI title** in the web app was `"Financial Infrastructure Intelligence"` — does not describe a Protocol Operating System. Updated to `"Protocol Operating System"`.
- **`docs/banzamia/architecture.md`** contains component names (`BanzamIAApp`, `BanzamIASidebar`, etc.) as code references — these are Wave 4 code identifier changes, deferred intentionally. The architecture doc itself will be updated when components are renamed.
