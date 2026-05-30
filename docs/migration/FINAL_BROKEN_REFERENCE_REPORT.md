---
name: final-broken-reference-report
description: All broken or stale cross-references across ~/banza, ~/banzai, ~/banzami — ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001
metadata:
  type: project
---

# Final Broken Reference Report

**Mission:** ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001  
**Date:** 2026-05-30

---

## Section 1 — Cross-Repo Canonical References

All cross-repo relative paths in canonical documents (`BANZA_*.md`, `BANZAI_*.md`, `BANZAMI_*.md`) were verified against the filesystem.

| Reference | From | Target exists | Status |
|-----------|------|--------------|--------|
| `../banza/BANZA_REFERENCE.md` | banzai/*.md | ✓ | VALID |
| `../banza/BANZA_CERTIFICATION.md` | banzai/*.md | ✓ | VALID |
| `../banza/BANZA_CONFORMANCE.md` | banzai/*.md | ✓ | VALID |
| `../banza/BANZA_ROADMAP.md` | banzai/*.md | ✓ | VALID |
| `../banzami/BANZAMI_REFERENCE.md` | banzai/*.md | ✓ | VALID |
| `../banzami/BANZAMI_ARCHITECTURE.md` | banzai/*.md | ✓ | VALID |
| `../banzami/BANZAMI_DEPLOYMENT.md` | banzai/*.md | ✓ | VALID |
| `../banzami/BANZAMI_ROADMAP.md` | banzai/*.md | ✓ | VALID |
| `../banzai/BANZAI_REFERENCE.md` | banza/*.md | ✓ | VALID |
| `../banzai/BANZAI_CAPABILITIES.md` | banza/*.md | ✓ | VALID |
| `../banzami/BANZAMI_REFERENCE.md` | banza/*.md | ✓ | VALID |
| `../banzami/BANZAMI_ARCHITECTURE.md` | banza/*.md | ✓ | VALID |
| `../banza/docs/governance/CLAUDE_BASE.md` | banzai/CLAUDE.md | ✓ | VALID |
| `docs/governance/CLAUDE_BASE.md` | banza/CLAUDE.md | ✓ | VALID |

**Result: 0 broken canonical cross-references.**

---

## Section 2 — Broken GitHub URLs

All of these are stale — they point to the old `github.com/banzami/` organization which was split into `github.com/banza-protocol/{banza,banzai,banzami}`.

### ~/banza repository

| File | Line(s) | Stale URL | Correct URL |
|------|---------|-----------|-------------|
| `README.md` | 273–274 | `https://github.com/banzami/banzami` | `https://github.com/banza-protocol/banzami` |
| `README.md` | 469 | `github.com/banzami/banza` | `github.com/banza-protocol/banzami` |
| `core/Cargo.toml` | 29 | `https://github.com/banzami/banzami` | `https://github.com/banza-protocol/banzami` |
| `core/README.md` | 72–73 | `https://github.com/banzami/banzami` | `https://github.com/banza-protocol/banzami` |
| `docs/getting-started.md` | 46 | `https://github.com/banzami/banzami` | `https://github.com/banza-protocol/banzami` |
| `docs/adr/ADR-018-open-financial-kernel.md` | 24 | `github.com/banzami/banzami` | `github.com/banza-protocol/banza` |
| `docs/adr/ADR-024-reference-operator.md` | 53 | `https://github.com/banzami/banzami.git` | `https://github.com/banza-protocol/banzami.git` |
| `sdk/go/README.md` | 10, 23 | `github.com/banzami/banzami-go` | `github.com/banza-protocol/banzami-go` |
| `sdk/python/pyproject.toml` | 42–43 | `https://github.com/banzami/sdk-python` | `https://github.com/banza-protocol/sdk-python` |

**Note on ADR-018:** ADR-018 references `github.com/banzami/banzami` as where the open kernel is published. The correct URL now is `github.com/banza-protocol/banza` (protocol kernel) — the open kernel moved to the banza repo.

### ~/banzai repository

| File | Line(s) | Stale URL | Correct URL |
|------|---------|-----------|-------------|
| `CONTRIBUTING.md` | 23 | `https://github.com/banzami/banzami` | `https://github.com/banza-protocol/banza` |
| `CONTRIBUTING.md` | 45 | `https://github.com/banzami/banzamia` | `https://github.com/banza-protocol/banzai` |

### ~/banzami repository

| File | Line(s) | Stale URL | Correct URL |
|------|---------|-----------|-------------|
| `README.md` | 13 | `https://github.com/banzami/banzami` | `https://github.com/banza-protocol/banzami` |
| `core/Cargo.toml` | 32 | `https://github.com/banzami/banza` | `https://github.com/banza-protocol/banzami` |
| `sdk/go/README.md` | 10, 23 | `github.com/banzami/banzami-go` | `github.com/banza-protocol/banzami-go` |
| `sdk/python/pyproject.toml` | 42–43 | `https://github.com/banzami/sdk-python` | `https://github.com/banza-protocol/sdk-python` |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md` | 239 | `github.com/banzami/banza` | `github.com/banza-protocol/banzami` |
| `docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md` | 252 | `github.com/banzami/banzami` | `github.com/banza-protocol/banzami` |
| `apps/docs/data/operators.json` | 11 | `https://github.com/banzami/banzami` | `https://github.com/banza-protocol/banzami` |
| `sdk/flutter/README.md` | 21 | `https://github.com/banzami/flutter-sdk.git` | `https://github.com/banza-protocol/flutter-sdk.git` |

---

## Section 3 — Stale Route References (`/banzamia` → `/banzai`)

These references use the pre-ADR-025 URL path. The 301 redirects are in place (`/banzamia` → `/banzai`), so these do not cause broken links at runtime — but source documents should use canonical routes.

### ~/banza repository

| File | Line(s) | Stale | Correct |
|------|---------|-------|---------|
| `README.md` | 124 | `banzami.org/banzamia` | `banzami.org/banzai` |
| `README.md` | 132 | `banzami.org/banzamia` | `banzami.org/banzai` |
| `README.md` | 196 | `banzami.org/banzamia` | `banzami.org/banzai` |
| `README.md` | 197 | `banzami.org/sobre-banzamia` | `banzami.org/sobre-o-banzai` |
| `apps/banzai/README.md` | 22, 71 | `apps/banzamia/` directory path | `apps/banzai/` |
| `apps/banzai/README.md` | 146 | `/banzamia` route | `/banzai` |

### ~/banzami repository

| File | Line(s) | Stale | Correct |
|------|---------|-------|---------|
| `docs/glossary.md` | 70 | `banzami.org/banzamia` | `banzami.org/banzai` |
| `docs/index.md` | 26, 34, 48 | `banzami.org/banzamia` | `banzami.org/banzai` |
| `docs/banzamia/overview.md` | 11, 103 | `banzami.org/banzamia`, `/banzamia?` | `banzami.org/banzai`, `/banzai?` |
| `docs/banzamia/roadmap.md` | 11, 17 | `/banzamia` route | `/banzai` |
| `docs/banzamia/architecture.md` | 14, 198 | `banzami.org/banzamia`, `banzamia-api` | `banzami.org/banzai`, `banzai-api` |
| `docs/BANZA_REFERENCE.md` | multiple | `banzami.org/banzamia` | `banzami.org/banzai` |
| `docs/certification.md` | 153 | `banzamia/operator-builder.md` link | `banzai/operator-builder.md` (if dir renamed) |

**Note on `docs/banzamia/` directory:** The entire `docs/banzamia/` subdirectory in the banzami repo was not renamed to `docs/banzai/` during ADR-025 migration. The directory name is stale. Files inside it reference `/banzamia` routes and `banzamia-` prefixed internal names. This is a P2/P3 batch cleanup.

---

## Section 4 — Package Metadata

| File | Field | Stale Value | Correct Value |
|------|-------|-------------|---------------|
| `banzai/package.json` | `name` | `@banzami/banzamia` | `@banza-protocol/banzai` |

---

## Section 5 — What Is NOT a Broken Reference

The following are intentionally preserved and should NOT be changed:

| Item | Reason |
|------|--------|
| `banzami-types`, `banzami-ledger`, etc. (Rust crate names) | ADR-025 protected names — deferred rename |
| `security@banzami.org`, `contact@banzami.org` | Protected email addresses — deferred |
| `banzami.org` domain | Protected domain — deferred, still active deployment |
| `/banzamia` → `/banzai` 301 redirects | Kept for backwards compat; redirects are functional |
| Historical references in `docs/migration/*.md` | Audit/migration documents intentionally record old names |
| `docs/banzamia/` content in banzami repo | Pre-rename docs that describe the banzamia-era architecture — historical value preserved |

---

*Produced by: ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001 — 2026-05-30*
