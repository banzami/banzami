---
title: SHARED_VS_PROJECT_SPECIFIC_MATRIX
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: CANONICAL-REPOSITORY-FOUNDATION-001
---

# Shared vs. Project-Specific Matrix

**Purpose:** Classify every root-level file by whether its content is shared across all repos, project-specific, or a shared structure with project-specific content.

---

## Classification Legend

| Class | Meaning |
|-------|---------|
| `SHARED` | Identical content in all three repos. Maintained in one place, copied to others. |
| `SHARED-STRUCTURE` | Same document structure and sections, but content is repo-specific. |
| `PROJECT-SPECIFIC` | Unique to each repository. No shared content. |

---

## Classification Table

### LICENSE
**Class: SHARED**

Apache License 2.0 — identical across all three repositories. If the license ever changes, all three change simultaneously.

| Repo | Current state | Action |
|------|--------------|--------|
| ~/banza | ✓ Apache 2.0 | No change |
| ~/banzai | ✓ Apache 2.0 | No change |
| ~/banzami | ✗ Missing | Create — copy from ~/banza/LICENSE |

---

### CODE_OF_CONDUCT.md
**Class: SHARED**

Contributor Covenant v2.1 — applies equally to all three project communities. The only project-specific element is the enforcement contact email (`conduct@banzami.org` or `security@banzami.org`).

| Repo | Current state | Action |
|------|--------------|--------|
| ~/banza | ✓ Contributor Covenant | No change |
| ~/banzai | ✗ Missing | Create — identical to ~/banza/CODE_OF_CONDUCT.md |
| ~/banzami | ✗ Missing | Create — identical to ~/banza/CODE_OF_CONDUCT.md |

---

### SECURITY.md
**Class: SHARED-STRUCTURE**

Same structure: reporting instructions, response SLA, scope definition, financial invariant priority. Content differs by scope.

**Shared structure:**
```
## Reporting a vulnerability
## Response SLA (48h acknowledgement, shared policy)
## Scope (THIS REPO ONLY)
## Out of scope
## Financial invariant vulnerabilities (BANZA kernel only)
```

| Repo | Scope |
|------|-------|
| ~/banza | Protocol kernel, SDKs, contracts, integrations |
| ~/banzai | API server, web interface, CLI, RAG/prompts, prompt injection |
| ~/banzami | Payment flows, wallets, merchant APIs, consumer APIs |

| Repo | Current state | Action |
|------|--------------|--------|
| ~/banza | ✓ (ADR-016 scope note) | Minor update: fix "Banzami commercial product" reference |
| ~/banzai | ✓ mostly correct | No change needed |
| ~/banzami | ✗ Missing | Create with operator-specific scope |

---

### CONTRIBUTING.md
**Class: SHARED-STRUCTURE**

Same sections across all repos, different contribution areas.

**Shared sections:**
- How to contribute (open issue first, fork, branch, PR)
- Branch naming convention
- Commit convention (type(scope): description)
- Code review process
- Testing requirements
- Documentation requirements

**Project-specific sections:**
- What you can contribute to (repo-specific areas)
- What is out of scope here (cross-reference to other repos)
- Contribution principles (repo-specific engineering rules)

| Repo | Current state | Action |
|------|--------------|--------|
| ~/banza | ✓ (wrong GitHub URLs) | Fix URLs |
| ~/banzai | ✓ good content | No change |
| ~/banzami | ✗ Missing | Create with operator contribution areas |

---

### GOVERNANCE.md
**Class: SHARED-STRUCTURE**

Same governance concepts applied differently per repo.

**Shared structure:**
```
## Overview
## Decision types (major vs. minor)
## Decision process (for major decisions)
## ADR / RFC process (where applicable)
## Maintainers
## Contact
```

**Project-specific content:**

| Repo | Governance domain |
|------|-----------------|
| ~/banza | Protocol governance: RFCs for protocol changes, ADRs for implementation. Open certification framework. |
| ~/banzai | OS governance: prompt changes, capability additions, model routing changes, knowledge base governance. |
| ~/banzami | Operator governance: deployment decisions, product roadmap, API versioning, merchant policies. |

| Repo | Current state | Action |
|------|--------------|--------|
| ~/banza | ✓ exists — P0 content issue ("governed by Banzami") | Fix critical content |
| ~/banzai | ✗ Missing | Create |
| ~/banzami | ✗ Missing | Create |

---

### README.md
**Class: PROJECT-SPECIFIC**

Each README is entirely specific to its repository. No shared content.

**Shared header elements (not content):**
- Ecosystem position statement (3-line hierarchy)
- Link to other repositories
- `docs/` and `.github/` references

| Repo | Primary message | Current state | Action |
|------|----------------|--------------|--------|
| ~/banza | "The open BANZA protocol" | ✓ exists — URL issues, missing hierarchy | Fix URLs + framing |
| ~/banzai | "The Protocol Operating System" | ✓ exists — multiple rename issues | Fix naming |
| ~/banzami | "The reference operator" | ✓ exists — framing gaps | Update framing |

---

### CLAUDE.md
**Class: PROJECT-SPECIFIC**

Each CLAUDE.md is entirely specific to its repository. References shared CLAUDE_BASE.md.

| Repo | Current state |
|------|--------------|
| ~/banza | ✓ aligned |
| ~/banzai | ✓ aligned |
| ~/banzami | ✓ aligned |

No action needed.

---

### *_REFERENCE.md (BANZA_REFERENCE, BANZAI_REFERENCE, BANZAMI_REFERENCE)
**Class: PROJECT-SPECIFIC**

Each canonical reference document is entirely specific to its owner.

| Repo | File | Current state |
|------|------|--------------|
| ~/banza | BANZA_REFERENCE.md | ✓ created last session |
| ~/banzai | BANZAI_REFERENCE.md | ✓ created last session |
| ~/banzami | BANZAMI_REFERENCE.md | ✓ created last session |

No action needed.

---

### .github/ISSUE_TEMPLATE/
**Class: SHARED-STRUCTURE**

Same template structure, repo-specific labels and content.

**Common templates for all repos:**
- `bug_report.yml` — structured bug report
- `feature_request.yml` — structured feature request
- `security_report.md` — security vulnerability disclosure (links to email)

**Repo-specific template:**
- `adr_proposal.yml` — for banza only (protocol ADR proposals)

---

### .github/PULL_REQUEST_TEMPLATE.md
**Class: SHARED-STRUCTURE**

Same checklist structure, repo-specific items.

**Shared checklist items:**
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Commit messages follow convention

**Repo-specific items:**
- ~/banza: [ ] ADR created if protocol change, [ ] Conformance vectors updated
- ~/banzai: [ ] Deterministic-first principle preserved, [ ] No LLM paths for certification decisions
- ~/banzami: [ ] Financial invariants preserved, [ ] No breaking API changes without ADR

---

### .github/workflows/
**Class: PROJECT-SPECIFIC**

Each repo has its own CI/CD workflow.

| Repo | Current workflows | Missing |
|------|-----------------|---------|
| ~/banza | conformance.yml | lint, unit tests |
| ~/banzai | (none) | ci.yml (TypeScript build, lint, test) |
| ~/banzami | ci.yml (Rust + Go) | TypeScript tests |

---

## Priority Summary

### Immediate (P0/P1 — blocking ecosystem trust)

1. Fix `~/banza/GOVERNANCE.md` — "governed by Banzami" P0
2. Fix `~/banzai/README.md` — multiple naming regressions
3. Fix `~/banza/README.md` — old GitHub URLs
4. Create `~/banzami/LICENSE`
5. Create `~/banzami/CONTRIBUTING.md`
6. Create `~/banzami/SECURITY.md`
7. Create `~/banzami/GOVERNANCE.md`
8. Create `~/banzai/CODE_OF_CONDUCT.md`
9. Create `~/banzai/GOVERNANCE.md`

### Secondary (ecosystem consistency)

10. Create .github/ISSUE_TEMPLATE/ for all three repos
11. Create .github/PULL_REQUEST_TEMPLATE.md for all three repos
12. Fix ~/banza/CONTRIBUTING.md URLs

---

*Matrix produced: 2026-05-30. No files modified.*
