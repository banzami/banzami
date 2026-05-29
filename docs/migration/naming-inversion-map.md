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

## Protected Names — DO NOT RENAME

| Name | Class | Reason |
|------|-------|--------|
| `banzami.org` | DOMAIN | Registered domain. DNS migration is a separate decision. |
| `contact@banzami.org` | EMAIL | Public contact address on all communications. |
| `github.com/banzami` | REPO | GitHub organization. Renaming breaks all clone URLs. Deferred. |
| `@banzami` handles | SOCIAL | Social media handles. Deferred to brand team. |

## Certification Levels

No renaming required. Certification level names (L0–L4: Sandbox, Payment, Settlement, Federation, Infrastructure) are not brand names and are not affected.

## Financial Invariants

No renaming required. Invariant IDs (INV-LEDGER-001, INV-STL-001, etc.) and RFC numbers (RFC-0001–RFC-0008) are protocol identifiers and are not brand names.

---

## Migration Waves (Proposed Order)

Renaming should proceed in waves to minimize broken states:

| Wave | Scope | Trigger |
|------|-------|---------|
| 1 | Documentation only (ADRs, READMEs, BANZAMI_REFERENCE.md) | After ADR-025 accepted |
| 2 | Website copy (banzami.org pages, metadata, SVG text) | After Wave 1 complete |
| 3 | AI OS rename (BanzamIA → BanzAI components, routes, identifiers) | After Wave 2 complete |
| 4 | Repository renames | Separate decision and ADR required |
| 5 | Package/crate renames | Separate decision and ADR required; involves published packages |
| 6 | Domain/email migration | Separate decision and ADR required; DNS transition plan needed |

Each wave requires a separate commit or PR with a scoped audit of changed occurrences.
