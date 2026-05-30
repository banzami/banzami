---
title: ROOT_FILE_ALIGNMENT_MATRIX
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: CANONICAL-REPOSITORY-FOUNDATION-001
---

# Root File Alignment Matrix

**Purpose:** Inventory and classify every root-level governance file across all three repositories.

**Legend:**
- `✓` — exists, content aligned with ADR-025
- `⚠` — exists, content issues found
- `✗` — missing (required)
- `—` — not applicable to this repo

---

## Root Files Matrix

| File | ~/banza | ~/banzai | ~/banzami | Classification |
|------|---------|---------|---------|----------------|
| `README.md` | `⚠` ADR-016 URLs | `⚠` old naming throughout | `⚠` private product framing | PROJECT-SPECIFIC — needs update |
| `CLAUDE.md` | `✓` | `✓` | `✓` | PROJECT-SPECIFIC — aligned |
| `CONTRIBUTING.md` | `⚠` old URLs | `✓` mostly good | `✗` MISSING | SHARED STRUCTURE — project-specific content |
| `CODE_OF_CONDUCT.md` | `✓` | `✗` MISSING | `✗` MISSING | SHARED — identical content |
| `SECURITY.md` | `⚠` ADR-016 scope note | `✓` | `✗` MISSING | SHARED STRUCTURE — project-specific scope |
| `LICENSE` | `✓` Apache 2.0 | `✓` Apache 2.0 | `✗` MISSING | SHARED — identical content |
| `GOVERNANCE.md` | `⚠` P0 CRITICAL | `✗` MISSING | `✗` MISSING | SHARED STRUCTURE — project-specific content |
| `*_REFERENCE.md` | `✓` BANZA_REFERENCE | `✓` BANZAI_REFERENCE | `✓` BANZAMI_REFERENCE | PROJECT-SPECIFIC |
| `.github/workflows/` | `✓` conformance.yml | `✗` MISSING | `✓` ci.yml | PROJECT-SPECIFIC |
| `.github/ISSUE_TEMPLATE/` | `✗` MISSING | `✗` MISSING | `✗` MISSING | SHARED STRUCTURE |
| `.github/PULL_REQUEST_TEMPLATE.md` | `✗` MISSING | `✗` MISSING | `✗` MISSING | SHARED STRUCTURE |
| `CHANGELOG.md` | `✗` MISSING | `✗` MISSING | `✗` MISSING | PROJECT-SPECIFIC — deferred |
| `ROADMAP.md` | `✗` MISSING | `✗` MISSING | `✗` MISSING | PROJECT-SPECIFIC — covered by *_REFERENCE |
| `Makefile` | `—` | `—` | `✓` | PROJECT-SPECIFIC |
| `deploy.sh` | `—` | `—` | `✓` | PROJECT-SPECIFIC |

---

## Critical Issues

### P0 — banza/GOVERNANCE.md

**Line:** "Banza is governed by Banzami (the organization)"

**Classification:** FALSE (ADR-025 terminology inversion)

**Impact:** Any visitor reading the governance file forms the inverted mental model: Banzami owns the protocol. This is the most critical finding in the entire audit.

**Required fix:** Remove "governed by Banzami (the organization)". Replace with: "BANZA is governed by an open protocol governance process — RFCs, ADRs, and a certification framework that is independent of any single operator."

---

### P1 — banzai/README.md

Multiple ADR-016/pre-rename issues:

| Line/Section | Issue | Fix |
|---|---|---|
| Ecosystem table | `github.com/banzami/banzami` | `github.com/banza-protocol/banza` |
| Ecosystem table | `github.com/banzami/banza` | `github.com/banza-protocol/banzami` |
| Ecosystem table | `github.com/banzami/banzamia` | `github.com/banza-protocol/banzai` |
| Ecosystem table | "First certified commercial operator" for banza | Should be: "Open financial infrastructure protocol" |
| Ecosystem table | "Open financial protocol kernel (Rust)" for banzami | Inverted — should describe Banzami |
| Deployment section | `BANZAMIA_MODE=live-api-no-model` | `BANZAI_MODE=live-api-no-model` |
| CLI section | `banzamia ask "..."` | `banzai ask "..."` |
| Architecture section | `banzamia/` directory | `banzai/` directory |
| Hosted instance URL | `banzami.org/banzamia` | `banzami.org/banzai` |

---

### P1 — banza/README.md

| Issue | Fix |
|---|---|
| `git clone https://github.com/banzami/banzami` | `git clone https://github.com/banza-protocol/banzami` |
| `cd banzami/reference` | should reference banzami repo correctly |
| Opening description lacks ADR-025 three-tier framing | Add ecosystem hierarchy |

---

### P1 — banza/CONTRIBUTING.md

| Issue | Fix |
|---|---|
| `git clone https://github.com/banzami/banzami.git` | `git clone https://github.com/banza-protocol/banza.git` |
| `cd banzami` | `cd banza` |

---

### P2 — banzami/README.md

| Issue | Fix |
|---|---|
| "Private Commercial Product" in title | "Reference Operator Implementation" |
| "built by Banzami" | consistent with ADR-025 framing |
| Missing: "Banzami is one operator — BANZA is the protocol" framing | Add opening ecosystem position |

---

## .github/ Status

| Asset | banza | banzai | banzami |
|---|---|---|---|
| Bug report template | `✗` | `✗` | `✗` |
| Feature request template | `✗` | `✗` | `✗` |
| ADR proposal template | `✗` | `✗` | `—` |
| Security report template | `✗` | `✗` | `✗` |
| PR template | `✗` | `✗` | `✗` |
| ci.yml / conformance.yml | `✓` conformance | `✗` | `✓` ci |

---

## Missing Files Count

| Repo | Missing required files |
|------|----------------------|
| ~/banza | CHANGELOG.md (deferred), .github templates |
| ~/banzai | CODE_OF_CONDUCT.md, GOVERNANCE.md, .github/ directory + templates |
| ~/banzami | CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, LICENSE, GOVERNANCE.md, .github templates |

---

*Matrix produced: 2026-05-30. No files modified.*
