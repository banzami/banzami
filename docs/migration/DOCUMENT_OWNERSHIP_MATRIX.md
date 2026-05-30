---
name: document-ownership-matrix
description: Complete ownership classification of every root-level document across ~/banza, ~/banzai, ~/banzami — produced by ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001
metadata:
  type: project
---

# Document Ownership Matrix

**Mission:** ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001  
**Date:** 2026-05-30  
**Status:** Authoritative

---

## Classification Legend

| Class | Meaning |
|-------|---------|
| `BANZA` | Protocol-owned — rules, invariants, governance, certification, federation |
| `BANZAI` | Protocol OS-owned — cognitive layer, capabilities, model routing |
| `BANZAMI` | Reference operator-owned — wallets, merchant products, deployment |
| `SHARED` | Identical content shared across all three repos (legal, community templates) |
| `SHARED-STRUCTURE` | Same purpose across repos, content is repo-specific (CONTRIBUTING, SECURITY, GOVERNANCE) |
| `PROJECT-SPECIFIC` | Belongs to one repo by nature but is not canonical (README, CLAUDE, Makefile) |

---

## ~/banza — Protocol Repository

| File | Current Name | Class | Owner | Action |
|------|-------------|-------|-------|--------|
| `BANZA_REFERENCE.md` | BANZA_REFERENCE.md | `BANZA` | Protocol | ✓ Already canonical |
| `GOVERNANCE.md` | GOVERNANCE.md | `BANZA` | Protocol | Rename → BANZA_GOVERNANCE.md |
| `SECURITY.md` | SECURITY.md | `BANZA` | Protocol | Rename → BANZA_SECURITY.md |
| `CONTRIBUTING.md` | CONTRIBUTING.md | `SHARED-STRUCTURE` | Protocol (community) | Keep — GitHub-standard name |
| `CODE_OF_CONDUCT.md` | CODE_OF_CONDUCT.md | `SHARED` | Community | Keep — GitHub-standard name |
| `LICENSE` | LICENSE | `SHARED` | Legal | Keep — standard name |
| `README.md` | README.md | `PROJECT-SPECIFIC` | Protocol | Keep — GitHub-standard name |
| `CLAUDE.md` | CLAUDE.md | `PROJECT-SPECIFIC` | Protocol (engineering) | Keep — project instruction file |
| `docs/conformance.md` | conformance.md | `BANZA` | Protocol | Promote → BANZA_CONFORMANCE.md (root) |
| `docs/architecture/README.md` | README.md | `BANZA` | Protocol | Promote → BANZA_ARCHITECTURE.md (root) |

**Missing canonical documents (to create):**

| Document | Source Content | Owner |
|----------|---------------|-------|
| `BANZA_MANIFESTO.md` | BANZA_REFERENCE.md §1–3 + README opening | Protocol |
| `BANZA_ARCHITECTURE.md` | docs/architecture/README.md | Protocol |
| `BANZA_CERTIFICATION.md` | banzami/docs/certification.md (protocol content promoted) | Protocol |
| `BANZA_CONFORMANCE.md` | docs/conformance.md | Protocol |
| `BANZA_ROADMAP.md` | BANZA_REFERENCE.md §11 | Protocol |

---

## ~/banzai — Protocol OS Repository

| File | Current Name | Class | Owner | Action |
|------|-------------|-------|-------|--------|
| `BANZAI_REFERENCE.md` | BANZAI_REFERENCE.md | `BANZAI` | Protocol OS | ✓ Already canonical |
| `GOVERNANCE.md` | GOVERNANCE.md | `BANZAI` | Protocol OS | Rename → BANZAI_GOVERNANCE.md |
| `SECURITY.md` | SECURITY.md | `BANZAI` | Protocol OS | Rename → BANZAI_SECURITY.md |
| `CONTRIBUTING.md` | CONTRIBUTING.md | `SHARED-STRUCTURE` | Protocol OS (community) | Keep — GitHub-standard name |
| `CODE_OF_CONDUCT.md` | CODE_OF_CONDUCT.md | `SHARED` | Community | Keep — GitHub-standard name |
| `LICENSE` | LICENSE | `SHARED` | Legal | Keep — standard name |
| `README.md` | README.md | `PROJECT-SPECIFIC` | Protocol OS | Keep — GitHub-standard name |
| `CLAUDE.md` | CLAUDE.md | `PROJECT-SPECIFIC` | Protocol OS (engineering) | Keep — project instruction file |

**Missing canonical documents (to create):**

| Document | Source Content | Owner |
|----------|---------------|-------|
| `BANZAI_ARCHITECTURE.md` | BANZAI_REFERENCE.md §4 | Protocol OS |
| `BANZAI_CAPABILITIES.md` | BANZAI_REFERENCE.md §5–6 | Protocol OS |
| `BANZAI_ROADMAP.md` | BANZAI_REFERENCE.md §11 | Protocol OS |

---

## ~/banzami — Reference Operator Repository

| File | Current Name | Class | Owner | Action |
|------|-------------|-------|-------|--------|
| `BANZAMI_REFERENCE.md` | BANZAMI_REFERENCE.md | `BANZAMI` | Reference Operator | ✓ Already canonical |
| `GOVERNANCE.md` | GOVERNANCE.md | `BANZAMI` | Reference Operator | Rename → BANZAMI_GOVERNANCE.md |
| `SECURITY.md` | SECURITY.md | `BANZAMI` | Reference Operator | Rename → BANZAMI_SECURITY.md |
| `CONTRIBUTING.md` | CONTRIBUTING.md | `SHARED-STRUCTURE` | Operator (community) | Keep — GitHub-standard name |
| `CODE_OF_CONDUCT.md` | CODE_OF_CONDUCT.md | `SHARED` | Community | Keep — GitHub-standard name |
| `LICENSE` | LICENSE | `SHARED` | Legal | Keep — standard name |
| `README.md` | README.md | `PROJECT-SPECIFIC` | Operator | Keep — GitHub-standard name |
| `CLAUDE.md` | CLAUDE.md | `PROJECT-SPECIFIC` | Operator (engineering) | Keep — project instruction file |
| `Makefile` | Makefile | `PROJECT-SPECIFIC` | Operator (build) | Keep — build artifact |
| `deploy.sh` | deploy.sh | `PROJECT-SPECIFIC` | Operator (ops) | Keep — operational artifact |
| `dev.sh` | dev.sh | `PROJECT-SPECIFIC` | Operator (dev) | Keep — development artifact |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md` | BANZAMI_ECOSYSTEM_REFERENCE.md | `BANZAMI` | Operator | Promote → BANZAMI_ARCHITECTURE.md (root) |

**Missing canonical documents (to create):**

| Document | Source Content | Owner |
|----------|---------------|-------|
| `BANZAMI_ARCHITECTURE.md` | docs/architecture/ content | Operator |
| `BANZAMI_PRODUCTS.md` | BANZAMI_REFERENCE.md §1–4 (product sections) | Operator |
| `BANZAMI_OPERATIONS.md` | Operational knowledge (services, infrastructure, monitoring) | Operator |
| `BANZAMI_DEPLOYMENT.md` | deploy.sh, Dockerfile, deployment knowledge | Operator |
| `BANZAMI_ROADMAP.md` | BANZAMI_REFERENCE.md §8 | Operator |

---

## GitHub-Standard Files — Retention Decision

The following files use GitHub-recognized names that trigger special UI behavior. They are retained with their GitHub-standard names:

| File | GitHub Behavior | Decision |
|------|----------------|----------|
| `SECURITY.md` | "Security" tab in repo | **RENAMED** to `BANZA/BANZAI/BANZAMI_SECURITY.md` — ecosystem identity takes precedence |
| `CONTRIBUTING.md` | Shown when opening PRs | **KEPT** — community-facing, GitHub-standard |
| `CODE_OF_CONDUCT.md` | Community standards badge | **KEPT** — legal/community-standard |
| `LICENSE` | License badge in UI | **KEPT** — legal requirement |

Note: GitHub does not recognize `BANZA_SECURITY.md` for the Security tab. The canonical naming is an explicit trade-off: ecosystem clarity over GitHub feature integration. This aligns with the ADR-025 priority that the repository tree itself must communicate architecture.

---

## Summary Counts

| Repo | Files Renamed | Files Created | Files Kept |
|------|--------------|--------------|------------|
| ~/banza | 2 | 5 | 6 |
| ~/banzai | 2 | 3 | 6 |
| ~/banzami | 2 | 5 | 8 |
| **Total** | **6** | **13** | **20** |

---

*Produced by: ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001*
