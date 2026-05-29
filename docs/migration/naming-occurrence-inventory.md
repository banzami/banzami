# Naming Occurrence Inventory

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Status:** Audit complete — no renaming has occurred

---

## Scope

Three repositories scanned:

| Repo | Path | Stack |
|------|------|-------|
| Banzami (kernel) | `/Users/fm65/Banzami` | Rust, Go, TypeScript |
| BanzamIA (AI OS) | `/Users/fm65/BanzamIA` | TypeScript, Python |
| Banza (operator) | `/Users/fm65/Banza` | TypeScript, Go, Markdown |

Excluded: `node_modules`, `.next`, `target`, `dist`, `.git`, `__pycache__`

---

## Raw Counts

| Search term | Files with matches | Repos |
|-------------|-------------------|-------|
| `banzamia` (case-insensitive) | 220 | All three |
| `banzami` only (not banzamia) | ~80 | Banzami, Banza |
| `banza` only (not banzami*) | ~140 | Banza, Banzami |
| `banzai` (new name, plans only) | 23 | Banzami, Banza |

---

## Inventory by Class

---

### CLASS: PROTOCOL

**Definition:** Occurrence refers to the open financial infrastructure protocol, kernel codebase, or specification.  
**Rename action (Wave 1/7):** `Banzami` → `Banza`

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| Banzami Protocol | Full protocol name in prose | ~40 | `README.md`, ADRs, `BANZAMI_REFERENCE.md`, GOVERNANCE | Rename to "Banza Protocol" (Wave 1 docs, Wave 3 website) |
| Banzami Kernel | The core Rust/Go runtime | ~15 | `core/README.md`, architecture SVGs, `CONTRIBUTING.md` | Rename to "Banza Kernel" (Wave 1) |
| Banzami Ecosystem | Full set of protocol participants | ~10 | `README.md`, `BANZAMI_REFERENCE.md` | Rename to "Banza Ecosystem" (Wave 1) |
| banzami-ledger | Rust crate name | 3 | `core/Cargo.toml`, workspace deps | Rename to "banza-ledger" (Wave 7 — code symbols) |
| banzami-wallets | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-wallets" (Wave 7) |
| banzami-transactions | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-transactions" (Wave 7) |
| banzami-types | Rust crate name | 5 | `core/Cargo.toml`, crate `use` statements | Rename to "banza-types" (Wave 7) |
| banzami-settlement | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-settlement" (Wave 7) |
| banzami-routing | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-routing" (Wave 7) |
| banzami-merchants | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-merchants" (Wave 7) |
| banzami-acquiring | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-acquiring" (Wave 7) |
| banzami-compliance | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-compliance" (Wave 7) |
| banzami-payouts | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-payouts" (Wave 7) |
| banzami-identity | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-identity" (Wave 7) |
| banzami-consumer-wallets | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-consumer-wallets" (Wave 7) |
| banzami-transfers | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-transfers" (Wave 7) |
| banzami-qr | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-qr" (Wave 7) |
| banzami-payment-links | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-payment-links" (Wave 7) |
| banzami-notifications | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-notifications" (Wave 7) |
| banzami-capabilities | Rust crate name | 3 | `core/Cargo.toml` | Rename to "banza-capabilities" (Wave 7) |
| banzami-conformance (tooling) | Conformance runner | 5 | `tools/banzami-conformance/` | Rename to "banza-conformance" (Wave 7) |
| Banzami as kernel org context | ADRs, GOVERNANCE, CONTRIBUTING | ~20 | `GOVERNANCE.md`, `CONTRIBUTING.md` | Rename to "Banza" (Wave 1) |
| BANZAMI_REFERENCE.md (filename) | Canonical reference document | 1 | Root of `docs/` | **OPEN DECISION** — renaming the canonical doc filename affects ADR-015 and all internal links; flag as conflict |

---

### CLASS: PRODUCT

**Definition:** Occurrence refers to the consumer/merchant-facing application or its features.  
**Rename action (Wave 3/7):** `Banza` → `Banzami`

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| Banza (product name) | Consumer payment app | ~60 | `apps/consumer/`, `apps/merchant/`, marketing copy | Rename to "Banzami" (Wave 3 website, Wave 7 code) |
| Banza Business | Merchant dashboard | ~20 | `apps/merchant/`, `docs/`, `APP_STORE_REVIEW_NOTES.md` | Rename to "Banzami Business" (Wave 3) |
| Banza Wallet | Consumer wallet | ~15 | `docs/`, API schemas, consumer app copy | Rename to "Banzami Wallet" (Wave 3) |
| Banza QR | QR payment product | ~10 | `docs/`, API schemas, merchant copy | Rename to "Banzami QR" (Wave 3) |
| Banza Checkout | Checkout experience | ~8 | SDK docs, `docs/`, plugin READMEs | Rename to "Banzami Checkout" (Wave 3) |
| Banza Pay Links | Pay link product | ~8 | SDK docs, `docs/` | Rename to "Banzami Pay Links" (Wave 3) |
| Banza app | Mobile application | ~12 | App store notes, mobile README | Rename to "Banzami app" (Wave 3) |
| BanzaClient (TypeScript SDK) | SDK client class for product API | ~30 | `sdk/typescript/`, plugin `client.ts` | **CONFLICT** — see conflicts doc |
| BanzaClient (PHP SDK) | PHP client class | ~15 | `plugins/generic-php/` | **CONFLICT** — see conflicts doc |
| BanzaError | SDK error class | ~10 | `sdk/typescript/`, tests | **CONFLICT** — see conflicts doc |
| BanzaPay (Flutter) | Flutter SDK | ~8 | `apps/mobile/`, Flutter SDK | **CONFLICT** — see conflicts doc |
| "Pay with Banza" | UI copy | ~5 | Consumer app, `APP_STORE_REVIEW_NOTES.md` | Rename to "Pay with Banzami" (Wave 3) |
| Banza SDK (generic) | SDK for building on the protocol | multiple | README files, `docs/integrations/` | **CONFLICT — UNRESOLVED** |
| @banza/sdk (npm) | Published npm scope/package | 1 | `sdk/typescript/package.json` | **CONFLICT — UNRESOLVED** (Wave 6) |
| @banza/node | Published npm | 1 | `plugins/generic-node/` | **CONFLICT — UNRESOLVED** (Wave 6) |
| banza_flutter | Pub.dev package | 1 | Flutter SDK | **CONFLICT — UNRESOLVED** (Wave 6) |
| banza/sdk-php | Composer package | 1 | `plugins/generic-php/` | **CONFLICT — UNRESOLVED** (Wave 6) |
| com.banzami.consumer | Android/Flutter package ID | 1 | Mobile app config | **CONFLICT — UNRESOLVED** (Wave 8) |
| com.banzami.merchant | Android/Flutter package ID | 1 | Mobile app config | **CONFLICT — UNRESOLVED** (Wave 8) |

---

### CLASS: AI_OS

**Definition:** Occurrence refers to the BanzamIA / BanzAI Protocol Operating System.  
**Rename action (Wave 4):** `BanzamIA` → `BanzAI`

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| BanzamIA (name) | Protocol OS product name | ~44 | BanzamIA repo, Banza docs, Banzami README | Rename to "BanzAI" (Wave 4) |
| BanzamIA Protocol OS | Full-name form | ~15 | banzami.org pages, BANZAMI_REFERENCE.md | Rename to "BanzAI Protocol OS" (Wave 3/4) |
| BanzamIA API | API product name | ~8 | API docs, route comments | Rename to "BanzAI API" (Wave 4) |
| BanzamIAChat (component) | React component name | 1 | `BanzamIAChat.tsx` | Rename to "BanzAIChat" (Wave 4 code) |
| BanzamIASidebar (component) | React component | 1 | `BanzamIASidebar.tsx` | Rename to "BanzAISidebar" (Wave 4 code) |
| BanzamIAApp (component) | React component | 1 | `BanzamIAApp.tsx` | Rename to "BanzAIApp" (Wave 4 code) |
| BanzamIAIcon (component) | React component | 1 | `BanzamIAIcon.tsx` | Rename to "BanzAIIcon" (Wave 4 code) |
| BanzamIASourcesPanel (component) | React component | 1 | `BanzamIASourcesPanel.tsx` | Rename to "BanzAISourcesPanel" (Wave 4 code) |
| banzamia-client (module) | Client library identifier | 3 | `lib/banzamia-client.ts`, imports | Rename to "banza-client" or "banzai-client" (**CONFLICT**) |
| @banzami/banzamia (package) | Root npm package | 1 | BanzamIA `package.json` | Rename to "@banza/banzai" (**CONFLICT — UNRESOLVED**) |
| BANZAMIA_MODE | Env var | 4 | `.env.example`, `docker-compose.yml` (both repos) | Rename to "BANZAI_MODE" (Wave 5) |
| BANZAMIA_PORT | Env var | 4 | `.env.example`, `docker-compose.yml` | Rename to "BANZAI_PORT" (Wave 5) |
| BANZAMIA_QDRANT_URL | Env var | 4 | `.env.example`, `docker-compose.yml` | Rename to "BANZAI_QDRANT_URL" (Wave 5) |
| BANZAMIA_EMBEDDING_* | Env vars (2) | 4 | `.env.example`, `docker-compose.yml` | Rename to "BANZAI_EMBEDDING_*" (Wave 5) |
| BANZAMIA_VLLM_URL | Env var | 4 | `.env.example`, `docker-compose.yml` | Rename to "BANZAI_VLLM_URL" (Wave 5) |
| BANZAMIA_MODEL_* | Env vars (3) | 4 | `.env.example`, `docker-compose.yml` | Rename to "BANZAI_MODEL_*" (Wave 5) |
| BANZAMIA_ALLOWED_ORIGINS | Env var | 2 | BanzamIA `.env.example` | Rename to "BANZAI_ALLOWED_ORIGINS" (Wave 5) |
| /banzamia route prefix | FastAPI path prefix | ~12 | BanzamIA API routes | Rename to "/banzai" (Wave 5 — coordinate with docs site) |
| BanzamIA welcome text (UI) | Website copy | 3 | `BanzamIAChat.tsx`, banzami.org pages | Rename (Wave 3/4) |
| BanzamIA sidebar subtitle | Website copy | 1 | `BanzamIASidebar.tsx` | Rename (Wave 4) |
| BanzamIA metadata titles | SEO metadata | 4 | banzami.org pages | Rename (Wave 3) |

---

### CLASS: ORG

**Definition:** Occurrence refers to the legal organization.  
**Rename action:** Confirm with founder — legal name is Banzami; role of org name after inversion is not yet decided.

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| "Organização Banzami" | Organization label in ADRs | ~10 | ADR headers | **Confirm with founder before renaming** |
| "Banzami team" / "Banzami organization" | Informal org reference | ~5 | GOVERNANCE, CONTRIBUTING | **Confirm with founder** |
| Banzami Lda | Legal entity name | ~3 | Formal docs, legal boilerplate | **DO NOT RENAME** — legally binding |

---

### CLASS: DOMAIN

**Definition:** Domain names.  
**Rename action:** PROTECTED — do not rename.

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| banzami.org | Primary website domain | ~30 | All repos, `next.config.js`, metadata, env examples | **PROTECTED — DO NOT RENAME** |
| sandbox.banzami.org | Sandbox environment | ~10 | OpenAPI specs, environment config | **PROTECTED** |
| api.banzami.org | API domain | ~5 | OpenAPI specs, SDK docs | **PROTECTED** |
| banzami.ao | Angola TLD variant | ~2 | Marketing docs | **PROTECTED** |

---

### CLASS: EMAIL

**Definition:** Email addresses.  
**Rename action:** PROTECTED — do not rename.

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| contact@banzami.org | Primary contact | ~5 | README files, GOVERNANCE, SECURITY | **PROTECTED — DO NOT RENAME** |
| security@banzami.org | Security disclosure | ~2 | SECURITY.md | **PROTECTED** |

---

### CLASS: REPO

**Definition:** Repository names and GitHub paths.  
**Rename action:** DEFERRED — requires separate ADR.

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| github.com/banzami | GitHub organization | ~8 | READMEs, clone instructions | **PROTECTED (current decision)** |
| github.com/banzami/banzami | Kernel repo | ~5 | Clone instructions, CI badge | **DEFERRED** — separate ADR required |
| github.com/banzami/banzamia | AI OS repo | ~3 | BanzamIA README | **DEFERRED** |
| github.com/banzami/banza | Operator repo | ~3 | Banza README | **DEFERRED** |

---

### CLASS: PACKAGE

**Definition:** Published package names.  
**Rename action:** DEFERRED — requires deprecation/redirect plan.

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| @banza/sdk | npm scope/package | 1 | `sdk/typescript/package.json` | **CONFLICT — see conflicts doc** |
| @banza/node | npm package | 1 | `plugins/generic-node/package.json` | **CONFLICT** |
| banza_flutter | pub.dev package | 1 | Flutter SDK | **CONFLICT** |
| banza/sdk-php | Composer package | 1 | `plugins/generic-php/composer.json` | **CONFLICT** |
| banzami-* (21 Rust crates) | Internal Rust crates | 21 | `core/Cargo.toml` | Rename to banza-* (Wave 7) — unpublished, internal only |
| @banzami/banzamia | BanzamIA root package | 1 | BanzamIA `package.json` | **CONFLICT — UNRESOLVED** |

---

### CLASS: ENV_VAR

**Definition:** Environment variable names.  
**Rename action:** Coordinate across all deployment environments (Wave 5).

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| BANZAMIA_MODE | BanzamIA runtime mode | 4 | `.env.example`, docker-compose | Rename to BANZAI_MODE |
| BANZAMIA_PORT | BanzamIA server port | 4 | `.env.example`, docker-compose | Rename to BANZAI_PORT |
| BANZAMIA_QDRANT_URL | Vector DB URL | 4 | `.env.example`, docker-compose | Rename to BANZAI_QDRANT_URL |
| BANZAMIA_EMBEDDING_MODEL | Embedding model name | 4 | `.env.example`, docker-compose | Rename to BANZAI_EMBEDDING_MODEL |
| BANZAMIA_EMBEDDING_DIM | Embedding dimensions | 4 | `.env.example`, docker-compose | Rename to BANZAI_EMBEDDING_DIM |
| BANZAMIA_VLLM_URL | vLLM inference URL | 4 | `.env.example`, docker-compose | Rename to BANZAI_VLLM_URL |
| BANZAMIA_MODEL_ROUTER | Model router endpoint | 4 | `.env.example`, docker-compose | Rename to BANZAI_MODEL_ROUTER |
| BANZAMIA_MODEL_DEFAULT | Default model | 4 | `.env.example`, docker-compose | Rename to BANZAI_MODEL_DEFAULT |
| BANZAMIA_MODEL_REASONING | Reasoning model | 4 | `.env.example`, docker-compose | Rename to BANZAI_MODEL_REASONING |
| BANZAMIA_ALLOWED_ORIGINS | CORS origins | 2 | `.env.example` | Rename to BANZAI_ALLOWED_ORIGINS |
| RUST_LOG=banzami=debug | Rust log filter | ~3 | `docker-compose.yml`, dev scripts | Rename to RUST_LOG=banza=debug (Wave 7) |

---

### CLASS: CODE_SYMBOL

**Definition:** Function names, class names, interface names in source files.  
**Rename action:** Wave 4 (AI_OS components) or Wave 7 (protocol/product code), using IDE rename refactoring.

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| BanzamIAChat | React component | 2 | `BanzamIAChat.tsx`, `BanzamIAApp.tsx` | Rename to BanzAIChat (Wave 4) |
| BanzamIASidebar | React component | 2 | `BanzamIASidebar.tsx`, `BanzamIAApp.tsx` | Rename to BanzAISidebar (Wave 4) |
| BanzamIAApp | React component | 2 | `BanzamIAApp.tsx`, page import | Rename to BanzAIApp (Wave 4) |
| BanzamIAIcon | React component | 3 | `BanzamIAIcon.tsx`, sidebar, chat | Rename to BanzAIIcon (Wave 4) |
| BanzamIASourcesPanel | React component | 2 | `BanzamIASourcesPanel.tsx` | Rename to BanzAISourcesPanel (Wave 4) |
| BanzaClient | SDK class (TS/PHP) | ~12 | `sdk/typescript/`, `plugins/generic-php/` | **CONFLICT** — see conflicts |
| BanzaError | SDK error class | ~8 | `sdk/typescript/`, tests | **CONFLICT** |
| BanzaApiError | SDK error class | ~5 | `sdk/checkout-web/` | **CONFLICT** |
| BanzamiAuthenticationError | SDK error class | ~5 | `sdk/python/`, webhook vectors | **CONFLICT** |
| BanzamiApiError | SDK error class | ~3 | `sdk/checkout-web/src/api.ts` | **CONFLICT** |
| BanzaPay | Flutter SDK class | ~5 | Flutter SDK | **CONFLICT** |
| chatStream | BanzamIA chat fn | 2 | `lib/banzamia-client.ts` | Neutral — no rename needed |
| isLiveMode | BanzamIA mode flag | 2 | `lib/banzamia-client.ts` | Neutral — no rename needed |

---

### CLASS: DATABASE

**Definition:** Database schema objects.  
**Rename action:** DEFERRED — requires migration files. No confirmed brand-named tables found in scan.

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| (none confirmed) | No brand-named tables detected | — | `db/migrations/` | No action required currently |

---

### CLASS: API_ROUTE

**Definition:** Public API route paths.  
**Rename action:** DEFERRED for breaking changes; coordinate with SDK versioning.

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| /.well-known/banzami/operator.json | Operator manifest discovery URL | ~8 | Go router, OpenAPI spec, reference operator | **CRITICAL — DO NOT RENAME** without protocol version bump. This is a public protocol contract. |
| BANZAMI-SBX: (QR prefix) | Sandbox QR payload prefix | ~5 | `qr-payment-lifecycle.svg`, OpenAPI, QR code generators | **CRITICAL — DO NOT RENAME** — encoded in all generated QR codes |
| BANZAMI: (QR prefix) | Production QR payload prefix | ~3 | OpenAPI, QR generators | **CRITICAL — DO NOT RENAME** |
| /webhooks/banzami (example) | Webhook receiver example route | ~4 | SDK docs, plugin READMEs | Rename to /webhooks/banza (Wave 6 — SDK docs only) |
| /banzamia/* (BanzamIA API) | AI OS API path prefix | ~12 | BanzamIA Fastify router | Rename to /banzai/* (Wave 5) |

---

### CLASS: PUBLIC_COPY

**Definition:** User-visible text in website, app UI, or documentation.  
**Rename action:** Wave 3 (website) / Wave 4 (BanzamIA UI).

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| "BanzamIA é o Sistema Operativo" | Welcome text | 1 | `BanzamIAChat.tsx` | → "BanzAI é o Sistema Operativo" (Wave 4) |
| "Protocol Operating System" subtitle | Sidebar label | 1 | `BanzamIASidebar.tsx` | No rename needed — neutral term |
| Page title "BanzamIA — Protocol OS" | SEO metadata | 4 | `app/banzamia/page.tsx`, etc. | → "BanzAI — Protocol OS" (Wave 3) |
| "Sobre o BanzamIA" | Navigation link | 1 | Sidebar footer | → "Sobre o BanzAI" (Wave 4) |
| App store copy "Banza Business" | Apple/Google copy | ~40 | `APP_STORE_REVIEW_NOTES.md` | → "Banzami Business" (Wave 3) |
| App store copy "Banza Wallet" | Apple/Google copy | ~15 | `APP_STORE_REVIEW_NOTES.md` | → "Banzami Wallet" (Wave 3) |
| "Pay with Banza" | CTA text | ~5 | Consumer app UI strings | → "Pay with Banzami" (Wave 3) |
| Roadmap page description | banzami.org/roadmap | 1 | `roadmap/page.tsx` | Update for BanzAI branding (Wave 3) |

---

### CLASS: SVG_TEXT

**Definition:** Text inside SVG architecture diagrams.  
**Rename action:** Wave 2.

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| "Banzami Kernel" label | Architecture SVG | 3 | `event-flow.svg`, `provider-model.svg` | → "Banza Kernel" (Wave 2) |
| "BANZAMI KERNEL CRATES" | Provider model SVG | 1 | `provider-model.svg` | → "BANZA KERNEL CRATES" (Wave 2) |
| "Banzami Sandbox Operator" | Sandbox architecture SVG | 1 | `sandbox-architecture.svg` | → "Banza Sandbox Operator" (Wave 2) |
| "/.well-known/banzami/operator.json" | SVG label | 1 | `sandbox-architecture.svg` | **CRITICAL** — keep as-is; reflects actual protocol endpoint |
| "BANZAMI-SBX:" | QR diagram label | 1 | `qr-payment-lifecycle.svg` | **CRITICAL** — keep as-is; reflects actual QR prefix |
| "Event Flow — Banzami Kernel" | SVG title | 1 | `event-flow.svg` | → "Event Flow — Banza Kernel" (Wave 2) |
| BanzamIA module labels | Product architecture SVG | ~20 | `banzamia-product-architecture.svg` | → BanzAI labels (Wave 2) |
| BanzamIA canonical architecture | Canonical SVG | ~15 | `banzamia-canonical-architecture.svg` | → BanzAI (Wave 2) |

---

### CLASS: TEST_FIXTURE

**Definition:** Occurrences in test files, fixtures, and test helpers.  
**Rename action:** Wave 7 (together with code symbols they test).

| Occurrence | Meaning | File count | Example locations | Action |
|------------|---------|------------|-------------------|--------|
| BanzamiWebhookSignatureError | Test class reference | 1 | `sdk-certification/typescript/webhook_vectors.test.ts` | Rename with CLASS: CODE_SYMBOL rename |
| BanzaClient (in tests) | Test instantiation | ~5 | `integrations/plugins/generic-node/tests/client.test.ts` | Rename when SDK symbol renamed |
| BanzaError (in tests) | Test assertion | ~5 | `sdk/typescript/src/client.test.ts` | Rename when SDK symbol renamed |
| BanzaApiError (in tests) | Test assertion | ~3 | Checkout SDK tests | Rename when SDK symbol renamed |
| "banzami" in query fixtures | Test question strings | 3 | BanzamIA `tests/` | Keep or update per test purpose |
