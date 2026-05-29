# Naming Inversion Migration Map

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Status:** Planning — no renaming has occurred yet

---

## How to use this map

Each row maps one legacy name to its new canonical name. The "Migration Notes" column indicates constraints, open decisions, and the migration class (see `naming-classification-rules.md`).

Before renaming any occurrence, classify it using `naming-classification-rules.md`. If an occurrence does not fit a row in this map, add it before renaming.

---

## Core Ecosystem Names

| Legacy Name | Legacy Meaning | New Name | New Meaning | Migration Notes |
|-------------|----------------|----------|-------------|-----------------|
| Banzami Protocol | Open financial protocol specification | Banza Protocol | Same | Class: PROTOCOL |
| Banzami Kernel | Rust core crates and Go services | Banza Kernel | Same | Class: PROTOCOL. Repository rename deferred. |
| Banzami Ecosystem | The full set of repos, operators, SDKs | Banza Ecosystem | Same | Class: PROTOCOL |
| Banzami Organization | The legal entity and team | Banza Protocol Organization | Open infrastructure org | Class: ORG. Use transitional form during migration. |
| Banzami (as protocol/infra) | When Banzami is used to mean the protocol | Banza | Protocol and ecosystem | Class: PROTOCOL. Classify occurrence context first. |

## Product Names

| Legacy Name | Legacy Meaning | New Name | New Meaning | Migration Notes |
|-------------|----------------|----------|-------------|-----------------|
| Banza (product) | Consumer/merchant payment experience | Banzami | Main product and reference operator | Class: PRODUCT. Classify occurrence context first. |
| Banza Wallet | Consumer wallet | Banzami Wallet | Same | Class: PRODUCT |
| Banza Business | Merchant dashboard | Banzami Business | Same | Class: PRODUCT |
| Banza QR | QR payment product | Banzami QR | Same | Class: PRODUCT |
| Banza Checkout | Checkout experience | Banzami Checkout | Same | Class: PRODUCT |
| Banza Pay Links | Pay link product | Banzami Pay Links | Same | Class: PRODUCT |
| Banza app | Mobile application | Banzami app | Same | Class: PRODUCT |

## SDK Names

| Legacy Name | Legacy Meaning | New Name | New Meaning | Migration Notes |
|-------------|----------------|----------|-------------|-----------------|
| Banza SDK | TypeScript/Flutter/PHP SDKs for building on the protocol | **OPEN DECISION — see note** | — | Class: PACKAGE. See note below. |
| Banzami SDK | (not currently used this way) | — | — | — |

> **SDK name open decision:** The SDK allows developers to build operators and integrations on the Banza protocol. If "Banza" is the protocol name, "Banza SDK" is the natural fit ("SDK to build on Banza"). However, ADR-012 established an SDK-first ecosystem and the SDKs are currently shipped as `banza-*`. A separate decision is needed before renaming any SDK packages. Until decided, keep `banza-sdk`, `banza-typescript-sdk`, `banza-flutter-sdk`, `banza-php-sdk` as-is.

## AI Protocol OS

| Legacy Name | Legacy Meaning | New Name | New Meaning | Migration Notes |
|-------------|----------------|----------|-------------|-----------------|
| BanzamIA | Protocol Operating System | BanzAI | Protocol Operating System for Banza | Class: AI_OS |
| BanzamIA API | AI OS API endpoints | BanzAI API | Same | Class: API_ROUTE. Wait for AI_OS rename. |
| BanzamIA Protocol OS | Full-name form of the product | BanzAI Protocol OS | Same | Class: AI_OS + PUBLIC_COPY |
| BanzamIA Chat | Chat module | BanzAI Chat | Same | Class: AI_OS + CODE_SYMBOL |
| BanzamIA Sidebar | Sidebar component | BanzAI Sidebar | Same | Class: AI_OS + CODE_SYMBOL |
| BanzamIA App | Application shell | BanzAI App | Same | Class: AI_OS + CODE_SYMBOL |
| banzamia-client | Client library identifier | banzai-client | Same | Class: PACKAGE. Rename with AI_OS wave. |

## Wire Format Identifiers — MIGRATE (STEP-002B)

Previously classified as protected. Overridden by STEP-002B: the naming inversion is total.

| Legacy Name | Legacy Meaning | New Name | New Meaning | Migration Notes |
|-------------|----------------|----------|-------------|-----------------|
| `BANZAMI:` (QR prefix) | Production QR payload prefix | `BANZA:` | Same | Class: API_ROUTE. Generators emit new; validators accept both. Wave 5c. |
| `BANZAMI-SBX:` (QR prefix) | Sandbox QR payload prefix | `BANZA-SBX:` | Same | Class: API_ROUTE. Same strategy. Wave 5c. |
| `/.well-known/banzami/operator.json` | Operator manifest discovery URL | `/.well-known/banza/operator.json` | Same | Class: API_ROUTE. Legacy path: 301 redirect. Wave 5c. |
| `banzami-operator` (type ID) | Operator type identifier | `banza-operator` | Same | Class: PROTOCOL. Rename in Wave 5c or Wave 7. |
| `banzami-conformance` (tool) | Conformance runner | `banza-conformance` | Same | Class: PROTOCOL + CODE_SYMBOL. Wave 7. |

See `naming-breaking-protocol-migration.md` for compatibility strategy and test requirements.

## Protected Names — DO NOT RENAME

| Name | Class | Reason |
|------|-------|--------|
| `banzami.org` | DOMAIN | Registered domain. DNS migration is a separate decision. **PROTECTED** |
| `contact@banzami.org` | EMAIL | Public contact address on all communications. **PROTECTED** |
| `security@banzami.org` | EMAIL | Security disclosure address. **PROTECTED** |
| `github.com/banzami` | REPO | GitHub organization. Renaming breaks all clone URLs. Deferred — separate ADR. |
| `@banzami` social handles | SOCIAL | Social media handles. Deferred to brand team. |
| `Banzami Lda` | ORG | Legal entity name in formal documents. **PROTECTED** |

## Certification Levels

No renaming required. Certification level names (L0–L4: Sandbox, Payment, Settlement, Federation, Infrastructure) are not brand names and are not affected.

## Financial Invariants

No renaming required. Invariant IDs (INV-LEDGER-001, INV-STL-001, etc.) and RFC numbers (RFC-0001–RFC-0008) are protocol identifiers and are not brand names.

---

## Migration Waves (Proposed Order)

Renaming should proceed in waves to minimize broken states:

See `naming-migration-waves.md` for the full wave breakdown. Summary:

| Wave | Scope |
|------|-------|
| 1 | Documentation prose (ADRs, READMEs, reference docs) |
| 2 | SVG diagram text labels |
| 3 | Website copy (banzami.org pages, metadata) |
| 4 | BanzAI UI components, routes, lib rename |
| 5a | Env vars (BANZAMIA_* → BANZAI_*), Docker |
| 5b | BanzAI API routes (/banzamia → /banzai) |
| 5c | Wire format (QR prefixes, operator manifest path) |
| 6 | SDK documentation, Python SDK rename |
| 7 | Rust crates (banzami-* → banza-*), code symbols |
| 8 | GitHub repository renames (separate ADR required) |
| 9 | Final cleanup (directory/filename renames) |

Each wave is a separate commit. No wave begins until the previous is merged and the working tree is clean.
