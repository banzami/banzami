---
title: GITHUB_REPOSITORY_HIERARCHY_REPORT
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: GITHUB-CANONICAL-IDENTITY-001
---

# GitHub Repository Hierarchy Report

**Mission:** GITHUB-CANONICAL-IDENTITY-001  
**Date:** 2026-05-30

---

## Repository Map

```
github.com/banza-protocol
│
├── banza             [PUBLIC]   Open financial infrastructure kernel
│   ├── Rust core crates (banzami-types, banzami-ledger, …)
│   ├── Protocol contracts (OpenAPI, webhooks, QR spec)
│   ├── Official SDKs (TypeScript, Python, PHP, Go, Flutter)
│   ├── Reference sandbox operator
│   ├── ADRs, RFCs, governance docs
│   └── SDK certification test vectors
│
├── banzai            [PUBLIC]   Protocol Operating System
│   ├── API (Hono/Node — orchestrator, model routing, tools)
│   ├── Web (Next.js — 16 module UIs)
│   └── CLI (banzai CLI)
│
├── banzami           [PRIVATE]  Reference Operator
│   ├── Consumer app, merchant dashboard, QR infrastructure
│   ├── Backend services (Rust core + Go APIs)
│   ├── Production infrastructure
│   └── Operator-specific adapters (EMIS, Multicaixa)
│
└── .github           [PUBLIC]   Org profile
    └── profile/README.md        ← Org homepage content
```

---

## Structural Correctness Assessment

### Organisation structure

The three-repository structure is **correctly organised** per ADR-025:

| Repo | Maps to ADR-025 Layer | Visibility |
|------|----------------------|------------|
| `banza` | Protocol / kernel / infrastructure | Public ✓ |
| `banzai` | Protocol OS (BanzAI) | Public ✓ |
| `banzami` | Reference operator (Banzami) | Private ✓ |

The public/private split is **correct**: the protocol and Protocol OS are public; the commercial operator implementation is private.

The org login `banza-protocol` clearly signals that this is a protocol organisation, not a product company. This is well-chosen.

---

## Hierarchy Legibility — What a Visitor Sees

### First impression: org page

A visitor arriving at `github.com/banza-protocol` sees:

1. Org name: **Banza** ← correct
2. Org description: "Open financial infrastructure for programmable payments, operators and settlement systems." ← correct
3. Three repositories listed: `banza`, `banzai`, `.github` (public) + `banzami` (private, hidden from unauthenticated visitors)
4. Org profile README: **"# Banzami"** ← INVERTS the hierarchy

The first three signals communicate "Banza is the protocol." The fourth signal says "Banzami is the protocol." The org profile README destroys the correct first impression.

### Repository descriptions at a glance

| Repo | Description shown on org page | Assessment |
|------|-------------------------------|------------|
| `banza` | "Open financial infrastructure kernel for programmable payments, operators and settlement systems." | CORRECT |
| `banzai` | "AI-native interface and orchestration layer for the **Banzami** ecosystem." | MISLEADING — "Banzami ecosystem" instead of "Banza protocol ecosystem" |
| `banzami` | "First commercial operator built on the **Banzami** financial infrastructure kernel." | FALSE — built on the Banza kernel |

On the org page, all three repository descriptions are visible simultaneously. A visitor reading them in sequence gets:

> "Banza is open infrastructure. BanzAI is for the Banzami ecosystem. Banzami is the commercial operator built on Banzami infrastructure."

The hierarchy is contradictory. `banzai` points to Banzami. `banzami` points to Banzami as infrastructure. The protocol (`banza`) is the only repo that correctly points to itself.

---

## Cross-Repository Link Consistency

### Internal links in READMEs

| From repo | To repo | Link used | Correct? |
|-----------|---------|-----------|----------|
| banza README | banzami | `github.com/banzami/banza` | PROTECTED — old org, intentional |
| banza README (BanzAI section) | banzai (live URL) | `banzami.org/banzamia` | OUTDATED — should be `banzami.org/banzai` |
| banzai README | banza, banzami | `banzami/banzami`, `banzami/banza` | PROTECTED — old org, intentional |
| banzami README | banza | `github.com/banzami/banzami` | PROTECTED — old org, intentional |

The PROTECTED links all use `github.com/banzami/...` because the GitHub org rename is deferred. A visitor following any of these links will arrive at a different GitHub organization (`banzami`) rather than `banza-protocol`. This creates a perception of discontinuity, but it is an intentional state per ADR-025.

### Canonical URL inconsistencies

| Surface | URL referenced | Canonical URL | Gap |
|---------|---------------|---------------|-----|
| banza README (BanzAI) | `banzami.org/banzamia` | `banzami.org/banzai` | OUTDATED |
| banzai README (deployment) | `banzami.org/banzamia` | `banzami.org/banzai` | OUTDATED |
| banzai README (documentation) | `banzami.org/sobre-banzamia` | `banzami.org/sobre-o-banzai` | OUTDATED |

---

## Repo Naming vs ADR-025 Model

The repository names themselves are clean:

| Name | ADR-025 Role | Naming Verdict |
|------|-------------|----------------|
| `banza` | Protocol kernel | CORRECT — protocol name |
| `banzai` | Protocol OS | CORRECT — BanzAI name |
| `banzami` | Reference operator | CORRECT — operator name |

The repository names are the most durable part of the GitHub identity (short of a full org rename) and they are correctly aligned.

---

## Missing Surfaces

The following GitHub surfaces exist at the org level but are not currently present or are incomplete:

| Surface | Status | Gap |
|---------|--------|-----|
| Org profile README | Present but INVERTED content | Critical |
| Pinned repositories | Not observed | Consider pinning `banza` (protocol kernel) first |
| Org README → protocol survivability statement | ABSENT | No statement that the protocol survives any operator |
| Discussions | Not checked | Governance RFCs could live here |
| Org topics | Not observed | No org-level topics to aid discovery |

---

## Rust Crate Naming

The Rust crates are all named `banzami-*` (e.g., `banzami-ledger`, `banzami-wallets`, `banzami-types`). These names are:

- Internally consistent
- **PROTECTED per ADR-025** — crate renaming was explicitly excluded from the naming inversion scope
- Potentially confusing to external developers who encounter a crate called `banzami-ledger` inside a repository called `banza`

A new developer reading:
```toml
banzami-types  = { git = "https://github.com/banzami/banzami" }
banzami-ledger = { git = "https://github.com/banzami/banzami" }
```

...will conclude that these crates belong to the `banzami` organisation and the `banzami` repo — not to the `banza-protocol/banza` repo. This is technically correct (the git URL points to `banzami/banzami`, the old org) but the semantic confusion between the crate name prefix and the new protocol name is a long-term friction point.

A future ADR (outside current scope) should address whether crate names will eventually be migrated to `banza-*` prefix.

---

*Report complete: 2026-05-30. No files modified.*
