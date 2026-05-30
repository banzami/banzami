---
title: GITHUB_STRUCTURE_ALIGNMENT_REPORT
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: CANONICAL-REPOSITORY-FOUNDATION-001
---

# GitHub Structure Alignment Report

**Purpose:** Audit GitHub-specific structure (workflows, issue templates, PR templates, repo metadata) across all three repositories.

---

## 1. Repository Metadata

### Descriptions (visible on org page)

| Repo | Current description | ADR-025 aligned? | Target description |
|------|--------------------|-----------------|--------------------|
| banza | (unknown — from GitHub audit session) | ⚠ Partially | "Open financial infrastructure protocol for Angola — ledger, wallets, QR, certification" |
| banzai | (unknown — from GitHub audit session) | ✗ Previously wrong | "Protocol Operating System for the BANZA financial ecosystem — intelligence, conformance, certification" |
| banzami | (unknown — from GitHub audit session) | ⚠ Partially | "Reference operator implementation of the BANZA protocol — Angola's instant payment network" |

Note: Descriptions visible on GitHub org page are set via GitHub UI/API, not via files in the repo. The GITHUB_CANONICAL_REMEDIATION_PLAN.md (W0-002 and W0-003) covers these.

### Topics

All three repos should carry these shared ecosystem topics:
- `angola` `kwanza` `payments` `fintech` `open-source`

Repo-specific topics:
- banza: `financial-protocol` `ledger` `rust` `certification` `federation`
- banzai: `protocol-os` `rag` `llm` `conformance` `ai-infrastructure`
- banzami: `reference-operator` `qr-payments` `wallet` `merchant-payments`

---

## 2. GitHub Actions / Workflows

| Repo | Existing workflows | Missing / needed |
|------|-------------------|-----------------|
| ~/banza | `conformance.yml` — validates conformance vectors | Rust CI (build, test), link checker |
| ~/banzai | None | TypeScript CI (tsc, lint, test, build) |
| ~/banzami | `ci.yml` — Rust + Go build, test | TypeScript tests for Next.js apps |

### banzai — CI workflow plan

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    name: TypeScript — build, lint, check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build --workspaces --if-present
      - run: npm run lint --workspaces --if-present
      - run: npm run type-check --workspaces --if-present
```

---

## 3. Issue Templates

### Current State

No issue templates exist in any of the three repositories.

### Target State

#### All repositories — bug_report.yml

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: "Thanks for reporting a bug. Fill in as much detail as possible."
  - type: textarea
    id: description
    attributes:
      label: Description
      description: What happened?
    validations:
      required: true
  - type: textarea
    id: reproduction
    attributes:
      label: Steps to reproduce
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
    validations:
      required: true
  - type: dropdown
    id: severity
    attributes:
      label: Severity
      options:
        - Critical (financial invariant, data corruption)
        - High (functionality broken)
        - Medium (degraded functionality)
        - Low (cosmetic, docs)
    validations:
      required: true
```

#### All repositories — feature_request.yml

```yaml
name: Feature Request
description: Propose a new feature or capability
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem statement
      description: What problem does this solve?
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: Proposed solution
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
```

#### banza only — adr_proposal.yml

```yaml
name: ADR Proposal
description: Propose an Architecture Decision Record for the BANZA protocol
labels: ["adr", "protocol"]
body:
  - type: markdown
    attributes:
      value: "ADRs govern protocol-level decisions. See docs/adr/ for existing ADRs."
  - type: textarea
    id: context
    attributes:
      label: Context
      description: What problem are you solving?
    validations:
      required: true
  - type: textarea
    id: decision
    attributes:
      label: Proposed decision
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
    validations:
      required: true
  - type: textarea
    id: consequences
    attributes:
      label: Consequences and tradeoffs
    validations:
      required: true
```

#### All repositories — security_report.md (not yml — routes to email)

```markdown
---
name: Security Report
about: Report a security vulnerability
---

⚠️ **Do NOT use this template for security vulnerabilities.**

Please report security vulnerabilities by email to **security@banzami.org**.

See [SECURITY.md](../SECURITY.md) for the full security policy.
```

---

## 4. Pull Request Templates

### Target — .github/PULL_REQUEST_TEMPLATE.md (shared structure)

```markdown
## Summary

<!-- What does this PR do? -->

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Refactoring (no functional change)
- [ ] Documentation
- [ ] Infrastructure

## Checklist

- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Commit messages follow `type(scope): description` convention
```

With repo-specific additions appended:

**banza:**
```markdown
- [ ] ADR created or updated if this is a protocol decision
- [ ] Conformance vectors updated if API contracts changed
- [ ] Financial invariants preserved
```

**banzai:**
```markdown
- [ ] Deterministic-first principle preserved (tools determine truth, LLM explains truth)
- [ ] No path introduced where LLM inference replaces deterministic validation
- [ ] Protocol claims are sourced (RFC/ADR citations)
```

**banzami:**
```markdown
- [ ] Financial invariants preserved
- [ ] No breaking API change without ADR
- [ ] deploy.sh tested if infra changed
```

---

## 5. Labels

Standard labels to create across all repos:

| Label | Color | Purpose |
|-------|-------|---------|
| `bug` | red | Bug reports |
| `enhancement` | blue | Feature requests |
| `documentation` | light blue | Docs-only changes |
| `protocol` | dark green | Protocol-level decisions |
| `adr` | green | Architecture Decision Records |
| `security` | dark red | Security issues |
| `good first issue` | light green | Beginner-friendly |

---

## 6. Branch Protection

Recommended settings for `main` in all repos:
- Require PR before merge: yes
- Required approvals: 1
- Dismiss stale reviews: yes
- Require status checks (where CI exists): yes

These are GitHub UI settings — not file-based. Listed for completeness.

---

*Report produced: 2026-05-30.*
