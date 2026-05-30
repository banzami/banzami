---
name: document-relocation-plan
description: Exact rename, promote, and create actions for every document in ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001
metadata:
  type: project
---

# Document Relocation Plan

**Mission:** ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001  
**Date:** 2026-05-30  
**Status:** Authoritative

---

## Action Legend

| Action | Meaning |
|--------|---------|
| `RENAME` | `git mv` — git history preserved, content unchanged |
| `PROMOTE` | Copy from docs/ subdirectory to root, add canonical header |
| `CREATE` | New file; content extracted from existing sources (no content loss) |
| `KEEP` | No change — filename is GitHub-standard or project-specific |

---

## Wave 1 — Renames (git mv, history preserved)

These are the highest-priority actions. Renaming existing files first, before creating new ones.

### ~/banza

| Action | From | To | Commit |
|--------|------|----|--------|
| `RENAME` | `GOVERNANCE.md` | `BANZA_GOVERNANCE.md` | `docs(banza): rename GOVERNANCE.md → BANZA_GOVERNANCE.md` |
| `RENAME` | `SECURITY.md` | `BANZA_SECURITY.md` | `docs(banza): rename SECURITY.md → BANZA_SECURITY.md` |

### ~/banzai

| Action | From | To | Commit |
|--------|------|----|--------|
| `RENAME` | `GOVERNANCE.md` | `BANZAI_GOVERNANCE.md` | `docs(banzai): rename GOVERNANCE.md → BANZAI_GOVERNANCE.md` |
| `RENAME` | `SECURITY.md` | `BANZAI_SECURITY.md` | `docs(banzai): rename SECURITY.md → BANZAI_SECURITY.md` |

### ~/banzami

| Action | From | To | Commit |
|--------|------|----|--------|
| `RENAME` | `GOVERNANCE.md` | `BANZAMI_GOVERNANCE.md` | `docs(banzami): rename GOVERNANCE.md → BANZAMI_GOVERNANCE.md` |
| `RENAME` | `SECURITY.md` | `BANZAMI_SECURITY.md` | `docs(banzami): rename SECURITY.md → BANZAMI_SECURITY.md` |

---

## Wave 2 — BANZA Canonical Documents (create at root)

All content is extracted from existing sources. No information is lost.

### BANZA_MANIFESTO.md

**Source:** BANZA_REFERENCE.md §1–3 (problem, missing layer, what BANZA is) + README.md opening philosophy  
**Location:** `~/banza/BANZA_MANIFESTO.md`  
**Purpose:** The founding philosophy and problem statement of the BANZA protocol. Why does it exist? What problem does it solve? Why now?  
**Forbidden content:** Implementation details, product descriptions, operator-specific content  
**Commit:** `docs(banza): add BANZA_MANIFESTO.md — protocol founding philosophy`

### BANZA_ARCHITECTURE.md

**Source:** `docs/architecture/README.md` (full content — promoted, not deleted)  
**Location:** `~/banza/BANZA_ARCHITECTURE.md`  
**Purpose:** Protocol system architecture — kernel structure, payment lifecycle, service boundaries, language rationale  
**Forbidden content:** Banzami-specific deployment topology (e.g., specific domains like `api.banzami.org`), operator business logic  
**Note:** The `docs/architecture/` subdirectory is kept for detailed per-domain architecture docs  
**Commit:** `docs(banza): add BANZA_ARCHITECTURE.md — promoted from docs/architecture/`

### BANZA_CERTIFICATION.md

**Source:** `~/banzami/docs/certification.md` (protocol content promoted to protocol repo)  
**Location:** `~/banza/BANZA_CERTIFICATION.md`  
**Purpose:** Formal certification levels L0–L4, universal rules (MON-001), certification process, maintenance  
**Forbidden content:** Banzami-specific product references, operator deployment details  
**Note:** The original in banzami/docs/ is kept and updated to cross-reference this canonical version  
**Commit:** `docs(banza): add BANZA_CERTIFICATION.md — promoted protocol certification doc`

### BANZA_CONFORMANCE.md

**Source:** `docs/conformance.md` (promoted to root)  
**Location:** `~/banza/BANZA_CONFORMANCE.md`  
**Purpose:** Conformance suite specification, test vectors, financial invariants, CI integration  
**Forbidden content:** Operator-specific deployment, product descriptions  
**Note:** `docs/conformance.md` is kept (internal docs location) and updated to reference root file  
**Commit:** `docs(banza): add BANZA_CONFORMANCE.md — promoted from docs/conformance.md`

### BANZA_ROADMAP.md

**Source:** BANZA_REFERENCE.md §11 (Roadmap do Protocolo)  
**Location:** `~/banza/BANZA_ROADMAP.md`  
**Purpose:** Protocol roadmap — what the protocol will support, not what any operator will ship  
**Forbidden content:** Banzami product features, BanzAI capabilities  
**Commit:** `docs(banza): add BANZA_ROADMAP.md — protocol roadmap`

---

## Wave 3 — BANZAI Canonical Documents (create at root)

### BANZAI_ARCHITECTURE.md

**Source:** BANZAI_REFERENCE.md §4 (Arquitectura do Sistema — full section)  
**Location:** `~/banzai/BANZAI_ARCHITECTURE.md`  
**Purpose:** BanzAI system architecture — tech stack, model routing, RAG, Protocol Graph, authority classification  
**Forbidden content:** Protocol rule definitions, Banzami deployment details  
**Commit:** `docs(banzai): add BANZAI_ARCHITECTURE.md — Protocol OS architecture`

### BANZAI_CAPABILITIES.md

**Source:** BANZAI_REFERENCE.md §5 (As Seis Capacidades) + §6 (Os 16 Módulos)  
**Location:** `~/banzai/BANZAI_CAPABILITIES.md`  
**Purpose:** Complete reference for what BanzAI can do — six capabilities, three-layer module architecture, deterministic tool table  
**Forbidden content:** How Banzami products work, protocol governance  
**Commit:** `docs(banzai): add BANZAI_CAPABILITIES.md — six capabilities and 16 modules`

### BANZAI_ROADMAP.md

**Source:** BANZAI_REFERENCE.md §11 (Roadmap do BanzAI)  
**Location:** `~/banzai/BANZAI_ROADMAP.md`  
**Purpose:** BanzAI roadmap — Live API, Live AI, Protocol Copilots, Federation Intelligence  
**Forbidden content:** Protocol roadmap, Banzami product roadmap  
**Commit:** `docs(banzai): add BANZAI_ROADMAP.md — Protocol OS roadmap`

---

## Wave 4 — BANZAMI Canonical Documents (create at root)

### BANZAMI_ARCHITECTURE.md

**Source:** `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md` + `docs/architecture/README.md` (service topology) + BANZAMI_REFERENCE.md §5  
**Location:** `~/banzami/BANZAMI_ARCHITECTURE.md`  
**Purpose:** Technical architecture of the Banzami reference operator — service map, language boundaries, data flows, observability  
**Forbidden content:** Protocol rule definitions, BanzAI capabilities  
**Commit:** `docs(banzami): add BANZAMI_ARCHITECTURE.md — reference operator technical architecture`

### BANZAMI_PRODUCTS.md

**Source:** BANZAMI_REFERENCE.md §1 (product table), §2 (Banzami Wallet), §3 (Banzami Business), §4 (SDK for developers)  
**Location:** `~/banzami/BANZAMI_PRODUCTS.md`  
**Purpose:** Product catalogue — Banzami Wallet, Banzami Business, Banzami QR, Banzami Checkout, Banzami Pay Links  
**Forbidden content:** Protocol governance, certification requirements  
**Commit:** `docs(banzami): add BANZAMI_PRODUCTS.md — operator product catalogue`

### BANZAMI_OPERATIONS.md

**Source:** Service map knowledge + CLAUDE.md §8 (observability standards) + infra/monitoring  
**Location:** `~/banzami/BANZAMI_OPERATIONS.md`  
**Purpose:** How the reference operator runs — services, health checks, monitoring, incident response  
**Forbidden content:** Protocol rules, BanzAI deployment  
**Commit:** `docs(banzami): add BANZAMI_OPERATIONS.md — operator operational guide`

### BANZAMI_DEPLOYMENT.md

**Source:** deploy.sh structure + CLAUDE.md §19.4 (deploy script) + Dockerfile knowledge  
**Location:** `~/banzami/BANZAMI_DEPLOYMENT.md`  
**Purpose:** How to deploy the reference operator — deploy.sh usage, services, environments, staging → production flow  
**Forbidden content:** Protocol architecture, BanzAI deployment  
**Commit:** `docs(banzami): add BANZAMI_DEPLOYMENT.md — operator deployment guide`

### BANZAMI_ROADMAP.md

**Source:** BANZAMI_REFERENCE.md §8 (Roadmap do Produto)  
**Location:** `~/banzami/BANZAMI_ROADMAP.md`  
**Purpose:** Banzami product roadmap — PHP SDK, payout automation, Banzami Wallet mobile, Banzami Business v2  
**Forbidden content:** Protocol roadmap, BanzAI roadmap  
**Commit:** `docs(banzami): add BANZAMI_ROADMAP.md — operator product roadmap`

---

## Wave 5 — Internal Reference Updates

After renames, update any internal cross-references to old filenames:

| File | Old Reference | New Reference |
|------|--------------|---------------|
| `~/banza/BANZA_GOVERNANCE.md` (was GOVERNANCE.md) | `[SECURITY.md](SECURITY.md)` | `[BANZA_SECURITY.md](BANZA_SECURITY.md)` |
| `~/banza/CONTRIBUTING.md` | Any reference to `SECURITY.md` | `BANZA_SECURITY.md` |
| `~/banzami/CONTRIBUTING.md` | Any reference to `GOVERNANCE.md` | `BANZAMI_GOVERNANCE.md` |
| `~/banzami/CONTRIBUTING.md` | Any reference to `SECURITY.md` | `BANZAMI_SECURITY.md` |
| `~/banzai/CONTRIBUTING.md` | Any reference to `GOVERNANCE.md` | `BANZAI_GOVERNANCE.md` |
| `~/banzai/CONTRIBUTING.md` | Any reference to `SECURITY.md` | `BANZAI_SECURITY.md` |

---

## What Is NOT Changed

| Category | Files | Reason |
|----------|-------|--------|
| GitHub-standard community files | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` | GitHub UI recognition (PR prompts, community badge) |
| Legal standard | `LICENSE` | Apache 2.0 standard naming |
| Build/ops scripts | `Makefile`, `deploy.sh`, `dev.sh` | Operational artifacts, not documentation |
| Engineering constitution | `CLAUDE.md` | Claude Code project file, not a canonical reference |
| Repository entry | `README.md` | GitHub homepage file, must stay as README.md |
| docs/ subdirectories | All files under docs/ | Internal documentation, not root canonical docs |

---

## Execution Order

```
Wave 1: git mv ×6 (renames — do first, git history preserved)
Wave 2: Write ×5 BANZA canonical docs
Wave 3: Write ×3 BANZAI canonical docs
Wave 4: Write ×5 BANZAMI canonical docs
Wave 5: Edit ×6 internal cross-reference fixes
```

**Total operations:** 19 file operations + 6 cross-reference fixes

---

*Produced by: ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001*
