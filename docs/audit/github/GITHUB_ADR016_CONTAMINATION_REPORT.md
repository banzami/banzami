---
title: GITHUB_ADR016_CONTAMINATION_REPORT
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: GITHUB-CANONICAL-IDENTITY-001
---

# GitHub ADR-016 Contamination Report

**Mission:** GITHUB-CANONICAL-IDENTITY-001  
**Date:** 2026-05-30  
**Purpose:** Locate all occurrences across `github.com/banza-protocol` that attribute to Banzami properties that belong to BANZA, and classify each.

---

## Reference: ADR-016 vs ADR-025

ADR-016 (superseded) assigned:
- **Banzami** = protocol / ecosystem / open infrastructure
- **Banza** = product / reference operator / commercial experience

ADR-025 (current) inverted this:
- **Banza** = protocol / ecosystem / open infrastructure
- **Banzami** = product / reference operator / commercial experience

"ADR-016 contamination" is any string or statement that, under the ADR-025 model, falsely attributes protocol-layer properties to Banzami.

---

## Classification Legend

| Class | Meaning |
|-------|---------|
| **FALSE** | Factually incorrect under ADR-025 |
| **MISLEADING** | Not technically false but creates a false impression |
| **OUTDATED** | Was correct under ADR-016, not yet updated to ADR-025 |
| **CONTEXTUAL** | Ambiguous — depends on interpretation |
| **CORRECT** | Correctly uses the name in the right layer context |
| **PROTECTED** | Intentionally preserved per ADR-025 (emails, domains, GitHub org, crate names) |

---

## Contamination Map — All Surfaces

### Org profile README (`banza-protocol/.github` → `profile/README.md`)

| String / Statement | Classification | Notes |
|---|---|---|
| `# Banzami` (title) | **FALSE** | Org represents Banza protocol |
| "Banzami is a **protocol-first**, open-source financial kernel" | **FALSE** | Protocol identity attributed to operator |
| "It defines the rules — wallets, transfers, ledger, settlement" | **FALSE** | Rule-definition is Banza's role |
| "**Banzami** is a protocol specification" | **FALSE** | Banza is the protocol specification |
| "**Banzami** is a Rust financial core" | **FALSE** | Rust core belongs to Banza |
| "**Banzami** is a conformance suite" | **FALSE** | Conformance belongs to Banza |
| "**Banzami** is an SDK ecosystem" | **FALSE** | SDK ecosystem belongs to Banza |
| "**Banzami** is an AI orchestration layer" | **MISLEADING** | AI orchestration is BanzAI (Banza layer), not Banzami |
| "What **Banzami** is not: A payment processor" | **CONTEXTUAL** | Statement is true of Banza; stated about Banzami |
| `banzami/banzami`, `banzami/banzamia` links | **PROTECTED** | GitHub org rename deferred per ADR-025 |
| `banzami.org` footer link | **PROTECTED** | Domain deferred per ADR-025 |

**Total FALSE/MISLEADING in org profile: 9**

---

### banza repo README (`banza-protocol/banza` → `README.md`)

| String / Statement | Classification | Notes |
|---|---|---|
| `banzami.org/banzamia` (BanzAI access URL) | **OUTDATED** | Route migrated to `banzami.org/banzai` |
| `banzami.org/sobre-banzamia` (BanzAI docs URL) | **OUTDATED** | Route migrated to `banzami.org/sobre-o-banzai` |
| `BANZAMIA_MODE`, `BANZAMIA_QDRANT_URL` env vars | **OUTDATED** | Canonical is `BANZAI_*`; backward compat aliases exist |
| `banzami-types`, `banzami-ledger` crate names | **PROTECTED** | ADR-025 explicitly excludes crate renaming |
| `github.com/banzami/banzami` clone URL | **PROTECTED** | GitHub org rename deferred |
| `Related: github.com/banzami/banza` | **PROTECTED** | Same |
| `docs/BANZAMI_REFERENCE.md` still present | **OUTDATED** | Phase 3 migration renamed to BANZA_REFERENCE.md locally |

**Total FALSE/MISLEADING in banza README: 0**  
**Total OUTDATED: 3 content + 1 file**  
**Total PROTECTED: 4**

---

### banza repo GOVERNANCE.md

| String / Statement | Classification | Notes |
|---|---|---|
| "Banza is governed by **Banzami** (the organization)" | **MISLEADING** | Implies operator controls protocol |
| "The Banza protocol is stewarded by **Banzami** (the organization)" | **MISLEADING** | Same |
| "The project is maintained by [Banza](https://banzami.org)" | **CONTEXTUAL** | "Banza" links to operator domain; ambiguous maintainer |
| `security@banzami.org`, `conduct@banzami.org` | **PROTECTED** | Emails deferred per ADR-025 |
| "Banzami — one operator among many" (section) | **CORRECT** | Correctly positions Banzami as operator |
| "Banzami is not a privileged operator" | **CORRECT** | Accurate |

**Total FALSE/MISLEADING in GOVERNANCE.md: 2**

---

### banzai repo description (GitHub metadata)

| String / Statement | Classification | Notes |
|---|---|---|
| "orchestration layer for the **Banzami** ecosystem" | **MISLEADING** | BanzAI belongs to Banza ecosystem, not Banzami ecosystem |

**Total FALSE/MISLEADING in banzai description: 1**

---

### banzai repo README (`banza-protocol/banzai` → `README.md`)

| String / Statement | Classification | Notes |
|---|---|---|
| Subtitle: "Protocol Operating System for the **Banza** financial infrastructure ecosystem" | **CORRECT** | Correct attribution |
| Ecosystem table: `banzami/banzami`, `banzami/banzamia` | **PROTECTED** | Old org, ADR-025 deferred |
| `banzami.org/banzamia` deployment URL | **OUTDATED** | Migrated to `banzami.org/banzai` |
| `banzami.org/sobre-banzamia` docs URL | **OUTDATED** | Migrated to `banzami.org/sobre-o-banzai` |
| `BANZAMIA_MODE=live-api-no-model` (Quick Start) | **OUTDATED** | Canonical is `BANZAI_MODE` |
| All `BANZAMIA_*` env vars in Quick Start | **OUTDATED** | Canonical is `BANZAI_*` |
| CLI: `banzamia ask`, `banzamia certify` etc | **OUTDATED** | CLI should be `banzai` post-migration |

**Total FALSE/MISLEADING in banzai README: 0**  
**Total OUTDATED: 5**  
**Total PROTECTED: 2**

---

### banzami repo description (GitHub metadata)

| String / Statement | Classification | Notes |
|---|---|---|
| "built on the **Banzami** financial infrastructure kernel" | **FALSE** | No such thing as "Banzami financial infrastructure kernel"; built on the Banza kernel |

**Total FALSE in banzami description: 1**

---

### banzami repo README (`banza-protocol/banzami` → `README.md`)

| String / Statement | Classification | Notes |
|---|---|---|
| "built on **Banza** infrastructure" (subtitle) | **CORRECT** | Correct |
| "External integrations use official **Banzami** SDKs" | **MISLEADING** | Protocol SDKs are Banza SDKs; Banzami uses/wraps them |
| "**Banza** is built with: fintech-grade agility..." | **OUTDATED** | ADR-016 residue: "Banza" used to mean "Banzami" |
| "**Banza** follows a modular monolith architecture" | **OUTDATED** | ADR-016 residue |
| "**Banza** is building the digital payment layer for Angola" | **OUTDATED** | ADR-016 residue: mission belongs to Banzami |
| "**Banza** is an API-first infrastructure layer" | **OUTDATED** | ADR-016 residue |
| "Product Vision: **Banza** is building..." | **OUTDATED** | ADR-016 residue |

**Total FALSE in banzami README: 0**  
**Total MISLEADING: 1**  
**Total OUTDATED: 5**

---

## Contamination Summary Table

The target strings from the audit specification:

| Target String | Found | Location | Classification |
|---|---|---|---|
| "Banzami protocol" | No direct match | — | — |
| "Banzami infrastructure" | No direct match | — | — |
| "Banzami ecosystem" | YES | banzai repo description | MISLEADING |
| "Banzami network" | No direct match | — | — |
| "Banzami platform" | No direct match | — | — |
| "Banzami operating system" | No direct match | — | — |
| "Banzami certification" | No direct match | — | — |
| "Banzami settlement" | No direct match | — | — |
| "Banzami ledger" | No direct match | — | — |
| "Banzami federation" | No direct match | — | — |
| Banzami = protocol kernel | YES | Org profile README | FALSE |
| Banzami = financial kernel | YES | banzami repo description | FALSE |
| Banzami governs Banza | YES | GOVERNANCE.md | MISLEADING |
| Banzami stewards Banza | YES | GOVERNANCE.md | MISLEADING |

---

## Contamination Severity Score by Surface

| Surface | FALSE | MISLEADING | OUTDATED | PROTECTED |
|---------|-------|------------|----------|-----------|
| Org profile README | 7 | 2 | 0 | 2 |
| banza README | 0 | 0 | 4 | 4 |
| banza GOVERNANCE.md | 0 | 2 | 0 | 2 |
| banzai description | 0 | 1 | 0 | 0 |
| banzai README | 0 | 0 | 5 | 2 |
| banzami description | 1 | 0 | 0 | 0 |
| banzami README | 0 | 1 | 5 | 0 |
| **Totals** | **8** | **6** | **14** | **10** |

---

## Key Finding

The highest concentration of **FALSE** statements (7 out of 8 total) is in the **org profile README** — the single most visible surface of the entire `github.com/banza-protocol` presence. This surface is also the easiest to fix: it requires only a text rewrite with no code changes, no migration risks, and no ADR-025 protected elements.

The **OUTDATED** items (14 total) are largely a consequence of local migration work not yet pushed to the GitHub remote. Once the BANZA-STRUCTURAL-NAMING-MIGRATION-001 commits are pushed to the corresponding GitHub repositories, most OUTDATED items resolve automatically.

---

*Report complete: 2026-05-30. No files modified.*
