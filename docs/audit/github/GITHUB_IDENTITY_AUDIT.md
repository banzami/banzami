---
title: GITHUB_IDENTITY_AUDIT
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: GITHUB-CANONICAL-IDENTITY-001
scope: github.com/banza-protocol — org + banza, banzai, banzami repos
---

# GitHub Identity Audit

**Mission:** GITHUB-CANONICAL-IDENTITY-001  
**Date:** 2026-05-30  
**Scope:** `github.com/banza-protocol` and all public/private repositories  
**Method:** Read-only. No files modified. No commits created.

---

## Identity Model Under Audit (ADR-025)

| Layer | Name | Role |
|-------|------|------|
| Protocol | **BANZA** | Open financial infrastructure protocol |
| Protocol OS | **BanzAI** | Protocol Operating System |
| Reference Operator | **Banzami** | First commercial operator built on Banza |

---

## Phase 1 — Organisation Audit

### Organisation metadata

| Field | Current Value | Assessment |
|-------|--------------|------------|
| Login | `banza-protocol` | CORRECT — communicates protocol identity |
| Display name | `Banza` | CORRECT — aligns with ADR-025 |
| Description | "Open financial infrastructure for programmable payments, operators and settlement systems." | CORRECT — no entity contamination |
| Email | `contact@banzami.org` | PROTECTED — deferred per ADR-025 |
| Blog | `https://banzami.org` | PROTECTED — domain migration deferred per ADR-025 |
| Twitter | null | NEUTRAL |
| Created | 2026-05-28 | — |
| Public repos | 3 (`banza`, `banzai`, `.github`) + 1 private (`banzami`) | CORRECT |

### Organisation profile README (`.github` repo → `profile/README.md`)

**Current title:** `# Banzami`

**Critical finding:** The org profile README displayed at `github.com/banza-protocol` is titled **"# Banzami"** and opens with:

> "Banzami is a **protocol-first, open-source financial kernel** designed for the African financial ecosystem. It defines the rules — wallets, transfers, ledger, settlement, traceability — so that any operator can build certified payment infrastructure without reinventing financial primitives."

This directly contradicts ADR-025. The organization `banza-protocol` represents the **Banza protocol**, not Banzami. Assigning protocol-layer properties ("protocol-first, open-source financial kernel", "It defines the rules") to Banzami is a **STRUCTURAL IDENTITY VIOLATION**.

**Additional profile issues:**

| Issue | Detail | Classification |
|-------|--------|----------------|
| Title is `# Banzami` | Org represents Banza, not Banzami | FALSE |
| "Banzami is a protocol-first...financial kernel" | Attributes protocol identity to Banzami | FALSE |
| "It defines the rules — wallets, transfers, ledger..." | Protocol governance attributed to Banzami | FALSE |
| Ecosystem table uses `banzami/banzami`, `banzami/banzamia` | Old GitHub org URLs | PROTECTED per ADR-025 |
| Footer links to `banzami.org` | Operator domain as protocol home | PROTECTED per ADR-025 |

**Visitor comprehension result:** A visitor who reads only the org profile README will conclude that Banzami is the protocol/infrastructure layer. This is the exact inversion ADR-025 was designed to correct.

---

## Phase 2 — Banza Repository Audit

### Repository metadata

| Field | Value | Assessment |
|-------|-------|------------|
| Name | `banza` | CORRECT |
| Description | "Open financial infrastructure kernel for programmable payments, operators and settlement systems." | CORRECT |
| Topics | africa, digital-payments, federation, financial-infrastructure, ledger, open-source, operator-network, payments, programmable-finance, protocol, rust, settlement | CORRECT — no contamination |
| Homepage | null | NEUTRAL |
| Visibility | public | CORRECT |

### README

| Section | Finding | Classification |
|---------|---------|----------------|
| H1 title: `# Banza` | Correct | CORRECT |
| Naming note citing ADR-025 | Present, accurate | CORRECT |
| Ecosystem description | Presents Banza as open-source financial infrastructure kernel | CORRECT |
| Public/private split table | Clear operator vs protocol boundary | CORRECT |
| Ecosystem architecture diagram | Shows BANZA at top, Banzami and BanzAI as subordinate | CORRECT (structure) |
| Banzami section | "Banzami is the first commercial operator built on Banza" | CORRECT |
| Sandbox clone instruction | `git clone https://github.com/banzami/banzami` | PROTECTED per ADR-025 |
| Cargo dependency URLs | `{ git = "https://github.com/banzami/banzami" }` | PROTECTED per ADR-025 |
| BanzAI URLs in README | `banzami.org/banzamia`, `banzami.org/sobre-banzamia` | OUTDATED — migrated to `/banzai`, `/sobre-o-banzai` |
| Environment variables | `BANZAMIA_MODE`, `BANZAMIA_QDRANT_URL` etc | OUTDATED — canonical is `BANZAI_*` |
| Crate names | `banzami-types`, `banzami-ledger`, etc. | PROTECTED — ADR-025 explicitly excludes crate renaming |
| Related section | `github.com/banzami/banza` | PROTECTED per ADR-025 |

### docs/ directory

| Finding | Classification |
|---------|----------------|
| `docs/BANZAMI_REFERENCE.md` present | OUTDATED — should be `BANZA_REFERENCE.md` after Phase 3 migration |
| `docs/adr/ADR-025-ecosystem-naming-inversion.md` present | CORRECT |
| `docs/adr/ADR-016-banzami-banza-brand-architecture.md` present, status Accepted | OUTDATED — ADR-025 supersedes ADR-016; ADR-016 status should be "Superseded by ADR-025" |

### GOVERNANCE.md

| Finding | Classification |
|---------|----------------|
| "Banza is governed by **Banzami** (the organization)" | MISLEADING — implies commercial operator controls protocol |
| "The Banza protocol is stewarded by **Banzami** (the organization)" | MISLEADING |
| Maintainers: "The project is maintained by [Banza](https://banzami.org)" | CONFUSED — "Banza" links to banzami.org (operator domain) |
| Contact emails: `security@banzami.org`, `conduct@banzami.org` | PROTECTED per ADR-025 |
| Section "Banzami — one operator among many" with correct framing | CORRECT — accurately states Banzami is not privileged |

### CONTRIBUTING.md

| Finding | Classification |
|---------|----------------|
| Clone instruction: `git clone https://github.com/banzami/banzami.git` | PROTECTED per ADR-025 |
| Review requirements: `banzami-ledger`, `banzami-wallets`, `banzami-acquiring`, `banzami-transactions` | PROTECTED — crate names excluded from ADR-025 scope |

### SECURITY.md

| Finding | Classification |
|---------|----------------|
| Security review targets: `banzami-ledger/src/`, `banzami-wallets/src/` etc | PROTECTED — crate names |
| Contact: `security@banzami.org` | PROTECTED per ADR-025 |

---

## Phase 3 — BanzAI Repository Audit

### Repository metadata

| Field | Value | Assessment |
|-------|-------|------------|
| Name | `banzai` | CORRECT |
| Description | "AI-native interface and orchestration layer for the **Banzami** ecosystem." | CONTAMINATION — should reference Banza, not Banzami |
| Topics | ai, banzami, conformance, financial-infrastructure, llm, operator-certification, orchestration, protocol, rag | `banzami` topic is MISLEADING — BanzAI belongs to the Banza ecosystem |
| Homepage | null | NEUTRAL |
| Visibility | public | CORRECT |

### README

| Section | Finding | Classification |
|---------|---------|----------------|
| H1 title: `# BanzAI` | Correct | CORRECT |
| Subtitle: "Protocol Operating System for the **Banza** financial infrastructure ecosystem." | CORRECT |
| "BanzAI is not a chatbot" framing | CORRECT |
| 8 capabilities table | CORRECT |
| 16 modules structure | CORRECT |
| Ecosystem table | Uses `banzami/banzami`, `banzami/banza`, `banzami/banzamia` | PROTECTED per ADR-025 |
| Deployment URL | `banzami.org/banzamia` | OUTDATED — migrated to `banzami.org/banzai` |
| Documentation URL | `banzami.org/sobre-banzamia` | OUTDATED — migrated to `banzami.org/sobre-o-banzai` |
| Env var: `BANZAMIA_MODE=live-api-no-model` | OUTDATED — canonical is `BANZAI_MODE` |
| All `BANZAMIA_*` env vars in Quick Start | OUTDATED — canonical is `BANZAI_*` |
| CLI commands: `banzamia ask`, `banzamia certify`, `banzamia validate` | OUTDATED — CLI binary should be `banzai` |
| Architecture paths `apps/api/`, `apps/web/`, `apps/cli/` | CONTEXTUAL — may reflect actual structure |
| Financial invariants table | CORRECT |
| Certification levels table | CORRECT |

### CONTRIBUTING.md

| Finding | Classification |
|---------|----------------|
| Fork instruction: `github.com/banzami/banzamia` | PROTECTED per ADR-025 |
| Kernel reference: `banzami/banzami` | PROTECTED per ADR-025 |
| Deterministic-first principle | CORRECT |

---

## Phase 4 — Banzami Repository Audit

### Repository metadata

| Field | Value | Assessment |
|-------|-------|------------|
| Name | `banzami` | CORRECT |
| Description | "First commercial operator built on the **Banzami** financial infrastructure kernel." | FALSE — Banzami is built on the **Banza** financial kernel |
| Topics | africa, banzami, digital-payments, financial-infrastructure, operator, payments, programmable-finance | `banzami` topic is CORRECT (this is the Banzami product) |
| Visibility | private | CORRECT |

### README

| Section | Finding | Classification |
|---------|---------|----------------|
| H1: `# Banzami — Private Commercial Product` | CORRECT |
| Subtitle: "Angola's instant payment network — QR-native, wallet-native, built on **Banza** infrastructure." | CORRECT |
| "This is the private commercial repository for **Banzami**" | CORRECT |
| "External integrations use official **Banzami** SDKs" | MISLEADING — official protocol SDKs are Banza SDKs; Banzami-specific internal integrations may be Banzami-specific |
| "Banza is built with: fintech-grade agility..." | OUTDATED — uses "Banza" to mean Banzami (ADR-016 residue) |
| "Banza follows a modular monolith architecture..." | OUTDATED — same |
| "Banza is building the digital payment layer for Angola..." | OUTDATED — same; mission belongs to Banzami, not Banza |
| "Banza is an API-first infrastructure layer" | OUTDATED — uses Banza where Banzami is meant |
| Product Vision: "Banza is building..." | OUTDATED |
| Server IP in Production section | SECURITY CONCERN — not an identity issue, but operator infra should not be in public docs |
| ADR-013, ADR-012 references | CORRECT — cross-references are accurate |

---

## Summary Table — All Findings

| # | Location | Finding | Severity | Classification |
|---|----------|---------|----------|----------------|
| 1 | Org profile README | Title `# Banzami`, describes Banzami as protocol kernel | CRITICAL | FALSE |
| 2 | banzai description | "Banzami ecosystem" | HIGH | MISLEADING |
| 3 | banzami description | "Banzami financial infrastructure kernel" | HIGH | FALSE |
| 4 | banza GOVERNANCE.md | "Banza is governed by Banzami" | HIGH | MISLEADING |
| 5 | banza GOVERNANCE.md | "stewarded by Banzami" | HIGH | MISLEADING |
| 6 | banza README | `banzami.org/banzamia` BanzAI URLs | MEDIUM | OUTDATED |
| 7 | banzai README | `banzami.org/banzamia` deployment URL | MEDIUM | OUTDATED |
| 8 | banzai README | `BANZAMIA_MODE`, `BANZAMIA_*` env vars | MEDIUM | OUTDATED |
| 9 | banzai README | CLI `banzamia ask/certify/validate` | MEDIUM | OUTDATED |
| 10 | banza docs/ | `BANZAMI_REFERENCE.md` still present | MEDIUM | OUTDATED |
| 11 | banzami README | "Banza is built with..." (means Banzami) | MEDIUM | OUTDATED |
| 12 | banzami README | "official Banzami SDKs" | LOW | MISLEADING |
| 13 | Org email/blog | `contact@banzami.org`, `banzami.org` | — | PROTECTED per ADR-025 |
| 14 | All repo URLs | `github.com/banzami/...` | — | PROTECTED per ADR-025 |
| 15 | Crate names | `banzami-types`, `banzami-ledger`, etc. | — | PROTECTED per ADR-025 |
| 16 | banza ADR-016 | Status still "Accepted" | LOW | OUTDATED — should be "Superseded" |

---

*Audit complete: 2026-05-30. No files modified.*
