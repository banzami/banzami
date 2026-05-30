---
name: banza-developer-adoption-report
description: Adoption audit for the Developer audience — what a developer needs to integrate BANZA, what they gain, what they fear, and what gaps exist
metadata:
  type: project
---

# BANZA — Developer Adoption Report

**Mission:** BANZA-ADOPTION-ARCHITECTURE-001  
**Audience:** Developers — engineers integrating BANZA into applications  
**Date:** 2026-05-30  
**Status:** Official

---

## Who is the Developer Audience

The developer audience spans three distinct profiles:

| Profile | Context |
|---------|---------|
| **Merchant integration developer** | Building payment acceptance into an existing product (taxi app, ecommerce, food delivery, school system) |
| **Consumer app developer** | Building a consumer-facing wallet or payment experience on top of the BANZA protocol |
| **Operator implementation engineer** | Building a certified BANZA operator implementation from scratch |

The first two profiles are the primary adoption leverage points. Every developer who successfully integrates Banzami into their product is a protocol adoption event. SDK-first policy means every integration is also a demonstration of the protocol's developer experience.

---

## What Developers Gain

### 1. SDK-first integration path

Developers do not need to understand the full protocol to accept payments. The TypeScript SDK provides:

- Typed APIs (no manual JSON construction)
- Environment isolation (sandbox vs live in the constructor)
- Automatic idempotency key management
- Automatic retries with exponential backoff
- Webhook signature verification helpers
- QR payment helpers
- Payment intent helpers
- Standardized error hierarchy

```typescript
import { BanzaClient } from '@banza/sdk';

const banza = new BanzaClient({
  apiKey: process.env.BANZA_API_KEY,
  environment: 'sandbox',
});

const qr = await banza.qr.createStatic({
  merchantId: 'mch_xyz',
  label: 'Mesa 5',
});
```

**What currently exists:** TypeScript SDK is implemented. Flutter SDK is implemented. PHP SDK is on the H2 2026 roadmap. Go SDK and Python SDK exist in early form.

### 2. Sandbox environment

A fully isolated test environment with the same kernel as production, test wallets, and the ability to fund wallets with fictitious balances. Developers do not need production credentials to start.

**What currently exists:** Sandbox environment is operational at a protocol level. `POST /v1/sandbox/fund` is documented.

### 3. BanzAI as protocol knowledge base

Developers can ask BanzAI protocol questions in natural language. Instead of reading dozens of ADRs to understand how idempotency works in the payment flow, a developer can ask BanzAI and receive a grounded answer with ADR citations.

**What currently exists:** BanzAI `POST /ask` and `POST /chat` are operational. BanzAI is accessible at `banzami.com/banzai`.

### 4. Financial invariants enforced by the kernel

A developer integrating via the SDK does not need to implement double-entry accounting, handle partial transaction rollback, or enforce integer-only money representation. The kernel enforces all of this. The SDK exposes clean abstractions.

### 5. Observable integrations by default

Every payment generates a `trace_id`. Every step in the payment lifecycle is an event in the trace. Developers can use BanzAI's Trace Explainer module to inspect any transaction trace interactively.

---

## What Developers Fear

### Fear 1: "I have to learn a new protocol just to accept payments"

Most developers expect to integrate a payment gateway in a day. Stripe-style: create a payment intent, redirect to hosted checkout, done. The BANZA model is fundamentally different — wallet-native, handle-based, no card numbers, real-time settlement — and this difference creates a learning cost that is not yet well-scaffolded.

**Current gap:** There is no "first payment in 15 minutes" quick-start guide. The protocol documentation is thorough and correct, but a developer's first entry point should not be a 40-section reference document. The getting-started guide (`docs/getting-started.md`) exists but is not surfaced prominently as the developer's primary entry.

**What is needed:** A `GET_STARTED.md` that takes a developer from zero to a working sandbox QR payment in under 30 minutes, requiring only an API key and `npm install @banza/sdk`.

### Fear 2: "The SDK isn't published anywhere I trust"

Developers validate tools by checking npm, PyPI, pub.dev, and Packagist before committing to integration. An SDK that exists only in a GitHub repository is not yet a real SDK from a developer trust perspective.

**Current gap:** `@banza/sdk` is not yet published on npm. `banza_flutter` is not yet published on pub.dev. `banza/sdk-php` is not yet on Packagist.

**What is needed:** SDK publishing pipeline to npm, pub.dev, and Packagist — with semantic versioning, changelog, and release notes. The package name `@banza/sdk` should resolve on npm before any developer outreach is done.

### Fear 3: "What happens if a payment goes wrong in production?"

Developers building financial integrations need to understand: what are the failure modes? What does the SDK throw? How are partial failures handled? Is there a refund API? How do I handle a webhook delivery failure?

**Current gap:** Error hierarchy documentation exists at the protocol level. SDK-level error handling documentation is incomplete. There is no developer-facing "failure modes" guide covering: idempotent retries, webhook replay, partial settlement failures, QR expiry handling.

**What is needed:** A developer error-handling guide covering the canonical failure scenarios and how the SDK handles each one.

### Fear 4: "The webhook verification is complex"

Webhook security is often the most common source of integration bugs. Developers need to understand the `banza-signature` header, the HMAC computation, and the replay prevention mechanism — and they need working code examples in every SDK language.

**Current gap:** Webhook signature verification is implemented in the TypeScript SDK. PHP, Python, and Go examples are minimal or absent. No developer-focused guide exists covering "replay protection" with concrete code.

**What is needed:** Webhook security guide with working code examples in TypeScript, PHP, Python, Go, and Flutter — including deliberate bad examples to illustrate what not to do.

### Fear 5: "I don't understand how wallets work"

BANZA is wallet-native. For a developer used to card-centric or bank-transfer-centric models, the concepts of "consumer wallet", "merchant wallet", "funding", "@handle identity", and "reserved balance" are unfamiliar. Without a clear mental model, integration attempts become guesswork.

**Current gap:** The conceptual model of wallets (available, reserved, total balance; how funding works; how settlement from consumer to merchant flows) is documented in the reference documents but not in a developer-oriented quick-reference form.

**What is needed:** A "Wallet Concepts" developer guide — a 2-page explainer with diagrams covering: how balances work, what a funding flow looks like, how a QR payment moves money between wallets, and what the developer sees vs. what the consumer sees.

---

## What Information is Missing

| Missing Information | Where it Belongs | Priority |
|--------------------|-----------------|----------|
| First-payment quick-start (sandbox, 15 min) | `docs/getting-started.md` (revamp) | CRITICAL |
| SDK publishing status (npm/pub.dev/Packagist links) | README + BANZAMI_PRODUCTS.md | HIGH |
| Error handling guide (failure modes, SDK errors, retries) | New `docs/developer/error-handling.md` | HIGH |
| Webhook verification guide (all languages) | New `docs/developer/webhooks.md` | HIGH |
| Wallet concepts explainer (for developers) | New `docs/developer/wallet-concepts.md` | HIGH |
| API reference (auto-generated from OpenAPI spec) | `contracts/` + docs site | HIGH |
| Rate limits, quotas, and burst handling | New `docs/developer/limits.md` | MEDIUM |
| Sandbox test credentials and test scenarios | New `docs/sandbox/scenarios.md` | MEDIUM |
| SDK changelog and versioning policy | Each SDK repo | MEDIUM |
| Support channels for developers | `BANZAMI_PRODUCTS.md` | MEDIUM |

---

## What Proof is Missing

| Missing Proof | Description | Priority |
|--------------|-------------|----------|
| **Published npm package** | `npm install @banza/sdk` must work before any developer outreach | CRITICAL |
| **Working integration example** | A GitHub repo (separate from the SDK) showing a complete taxi app or ecommerce integration using only `@banza/sdk` | HIGH |
| **DOA migration to TypeScript SDK** | The first-party reference app using the SDK proves it works end-to-end | HIGH |
| **Developer testimonial (1st integration)** | One developer outside of Banzami who has successfully integrated the sandbox | MEDIUM |

---

## What Tools are Missing

| Missing Tool | Description | Priority |
|-------------|-------------|----------|
| **`@banza/sdk` on npm** | Publicly installable TypeScript SDK | CRITICAL |
| **Sandbox API key instant issuance** | A developer can get a sandbox key without manual approval — just sign up and get credentials | HIGH |
| **OpenAPI spec in `contracts/`** | Machine-readable API spec enabling auto-generated client code in any language | HIGH |
| **SDK playground (Swagger UI or similar)** | Interactive API explorer in the developer console | MEDIUM |
| **`banza-conformance` CLI** | Lets an operator-developer verify their implementation before formal certification | MEDIUM |
| **Trace inspector UI** | In the dashboard, a developer can paste a `trace_id` and see every event in the payment flow | MEDIUM |
| **PHP SDK on Packagist** | `composer require banza/sdk-php` must work for Laravel and WordPress integrations | MEDIUM |

---

## The Developer Adoption Funnel

Understanding the gap requires mapping where developers drop off:

```
Discovers BANZA
    ↓
Reads README / documentation           ← WHERE: Is there a "15-minute" hook?
    ↓
Finds and installs the SDK             ← BLOCKER: npm package not yet published
    ↓
Gets sandbox API key                   ← FRICTION: Is this self-service or manual?
    ↓
Makes first API call (sandbox)         ← WHERE: Is there a working example?
    ↓
Integrates into product (sandbox)      ← FRICTION: No error handling guide
    ↓
Goes to production                     ← FRICTION: No production onboarding docs
    ↓
Stays integrated                       ← FRICTION: No changelog / SDK updates
```

Every `←` annotation is a drop-off risk. The higher on the funnel the drop-off, the higher the adoption cost.

---

## Priority Actions

1. **Publish `@banza/sdk` on npm** — this is the single most visible adoption signal. A package on npm is real; a GitHub repo is not.
2. **Build a 15-minute first-payment tutorial** — from `npm install` to a confirmed sandbox QR payment, with zero protocol knowledge required.
3. **Make sandbox key issuance self-service** — a developer who has to wait for manual approval will not wait.
4. **Publish OpenAPI spec** — enables auto-generated SDKs in languages not yet officially supported.
5. **Write the three missing developer guides** (error handling, webhooks, wallet concepts).

---

*Part of BANZA-ADOPTION-ARCHITECTURE-001 — 2026-05-30*
