---
title: LOCAL_REPOSITORY_NAMING_ALIGNMENT_REPORT
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: LOCAL-REPOSITORY-NAMING-ALIGNMENT-001
---

# Local Repository Naming Alignment Report

**Mission:** LOCAL-REPOSITORY-NAMING-ALIGNMENT-001  
**Date:** 2026-05-30  
**Executed by:** Claude Code (read-only inspection + folder renames + remote updates)

---

## Summary

All three local repository folders have been renamed to match the canonical ADR-025 identity model and their git remotes updated to point to `github.com/banza-protocol`.

**Result:** SUCCESS — no source files changed, no commits created.

---

## Phase 1 — Initial State

### Repositories found

| Local folder | Remote (before) | ADR-025 role | Target name |
|---|---|---|---|
| `/Users/fm65/Banzami` | `git@github.com-banzami:banzami/banzami.git` | Protocol kernel | `banza` |
| `/Users/fm65/BanzamIA` | `https://github.com/banzami/banzamia.git` | Protocol OS | `banzai` |
| `/Users/fm65/Banza` | `git@github.com-banzami:banzami/banza.git` | Reference operator | `banzami` |

### SSH config note

The `github.com-banzami` SSH alias (using `~/.ssh/id_ed25519_banzami`) was configured for the `banzami` GitHub account. Both repos that used it (`/Users/fm65/Banzami` and `/Users/fm65/Banza`) have been switched to HTTPS for the `banza-protocol` org. The SSH alias is now unused and can be removed or kept for archive purposes.

---

## Phase 2 — Git Status Before Rename

| Folder | Git status | Notes |
|---|---|---|
| `/Users/fm65/Banza` | **CLEAN** | Ready for rename |
| `/Users/fm65/BanzamIA` | **CLEAN** | Ready for rename |
| `/Users/fm65/Banzami` | **NOT CLEAN** | See unclean state detail below |

### Unclean state — `/Users/fm65/Banzami` (now `banza`)

The folder had uncommitted changes at time of rename:

**Modified files (2):**
- `docs/adr/ADR-015-markdown-first-content-architecture.md`
- `docs/adr/ADR-016-banzami-banza-brand-architecture.md`

**Untracked files (17):**
- `docs/audit/github/` — 7 audit documents from GITHUB-CANONICAL-IDENTITY-001 session
- `docs/migration/BANZA_CORE_THESIS_REPORT.md`
- `docs/migration/BANZA_DIFFERENTIATION_EXECUTION_PLAN.md`
- `docs/migration/BANZA_DIFFERENTIATION_REPORT.md`
- `docs/migration/BANZA_MESSAGING_GAPS.md`
- `docs/migration/BANZA_MESSAGING_REWRITE_MAP.md`
- `docs/migration/BANZA_NARRATIVE_CONVERGENCE_AUDIT.md`
- `docs/migration/BANZA_STRATEGIC_POSITIONING_AUDIT.md`
- `docs/migration/CANONICAL_REWRITE_EXECUTION_REPORT.md`
- `docs/migration/deep-consistency-audit-report.md`
- `docs/migration/deep-consistency-remediation-plan.md`
- `docs/migration/hero-positioning-audit.md`
- `docs/migration/homepage-brand-alignment-report.md`
- `docs/migration/root-identity-audit.md`
- `docs/migration/root-identity-remediation-plan.md`
- `docs/migration/root-identity-safe-fixes-report.md`

**Decision:** Proceeded with rename. `mv` is a filesystem operation — it does not affect git state, history, or uncommitted changes. All files moved intact with the folder. No data loss.

---

## Phase 3 — Rename Execution

### macOS APFS case-insensitive note

macOS APFS is case-insensitive: `Banzami` == `banzami` and `Banza` == `banza`. Direct renames would cause collisions (e.g., `mv Banzami banzami` would attempt to rename a directory to itself; `mv Banza banzami` would attempt to move Banza INTO the existing Banzami directory).

**Safe sequence executed:**

1. `mv /Users/fm65/Banzami /tmp/banza_migration_temp` — moved to neutral temp location
2. `mv /Users/fm65/Banza /Users/fm65/banzami` — `banzami` path now free, rename safe
3. `mv /tmp/banza_migration_temp /Users/fm65/banza` — `banza` path now free (Banza gone), rename safe
4. `mv /Users/fm65/BanzamIA /Users/fm65/banzai` — no conflict

**All git `.git/HEAD` files verified intact after each step.**

---

## Phase 4 — Remote Updates

### Git history verification (before updating remotes)

Confirmed that `banza-protocol` repositories have **identical git histories** to the local repos (same commit SHAs). The `banza-protocol` org uses the same underlying repositories.

### Remote URL updates

| Repo | Old remote | New remote |
|---|---|---|
| `banza` | `git@github.com-banzami:banzami/banzami.git` | `https://github.com/banza-protocol/banza.git` |
| `banzai` | `https://github.com/banzami/banzamia.git` | `https://github.com/banza-protocol/banzai.git` |
| `banzami` | `git@github.com-banzami:banzami/banza.git` | `https://github.com/banza-protocol/banzami.git` |

Protocol changed from SSH (with custom alias) to HTTPS for `banza` and `banzami`, consistent with `gh` CLI authentication (HTTPS). `banzai` was already HTTPS.

---

## Phase 5 — Verification

### Final state

| Local folder | Remote | Branch | Tracking | Git status |
|---|---|---|---|---|
| `/Users/fm65/banza` | `https://github.com/banza-protocol/banza.git` | `main` | `origin/main` ✓ | Uncommitted changes (docs only) |
| `/Users/fm65/banzai` | `https://github.com/banza-protocol/banzai.git` | `main` | `origin/main` ✓ | CLEAN |
| `/Users/fm65/banzami` | `https://github.com/banza-protocol/banzami.git` | `main` | `origin/main` ✓ | CLEAN |

**Upstream tracking for `banzai/main` was not configured** before this mission (the branch showed no tracking). Set via `git branch --set-upstream-to=origin/main main` during Phase 5.

### Fetch result

`git fetch origin` executed successfully on all three repos with no errors. All branches are up to date with their remote counterparts.

---

## Phase 6 — Editor Workspace

No `.code-workspace` files found for the Banza repositories (`find` returned no results). The VS Code workspace for these repositories is configured via recent workspaces or manual folder opens.

**Action required (manual):**
1. In VS Code/Cursor, open each folder with its new name:
   - Remove (if still open): `BANZAMI` (now invalid path)
   - Remove (if still open): `BanzamIA` (now invalid path)
   - Remove (if still open): `BANZA` (now invalid path)
   - Add: `/Users/fm65/banza`
   - Add: `/Users/fm65/banzai`
   - Add: `/Users/fm65/banzami`

The Explorer will then show the correct canonical names.

---

## Final Structure

```
~/
├── banza/       ← Protocol kernel (was Banzami → banzami/banzami.git → banza-protocol/banza.git)
├── banzai/      ← Protocol OS (was BanzamIA → banzami/banzamia.git → banza-protocol/banzai.git)
└── banzami/     ← Reference operator (was Banza → banzami/banza.git → banza-protocol/banzami.git)
```

A developer opening the local workspace now sees:

```
banza     → BANZA protocol kernel
banzai    → BanzAI Protocol Operating System
banzami   → Banzami reference operator
```

No local folder name contradicts ADR-025. ✓  
No source files changed. ✓  
No commits created. ✓

---

## Pending Actions (not in scope of this mission)

1. **Commit untracked/modified files in `banza/`** — The 17 untracked files and 2 modified ADRs in `/Users/fm65/banza` should be committed. These include the GITHUB-CANONICAL-IDENTITY-001 audit documents and earlier narrative documentation.

2. **SSH config cleanup** — The `github.com-banzami` SSH alias in `~/.ssh/config` is now unused. It can be removed or documented as archived.

3. **Update SSH config comment** — The comment "Alias só para o repo /Users/fm65/Banzami" is stale. The alias is unused and the folder no longer exists at that path.

4. **Open VS Code folders manually** — Re-open `banza`, `banzai`, `banzami` in the editor to update workspace memory.

---

*Migration complete: 2026-05-30. No source files changed. No commits created.*
