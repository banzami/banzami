---
title: GITHUB_ADR025_ALIGNMENT_REPORT
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: GITHUB-CANONICAL-IDENTITY-001
---

# GitHub ADR-025 Alignment Report

**Mission:** GITHUB-CANONICAL-IDENTITY-001  
**Date:** 2026-05-30

---

## ADR-025 Decision Summary (Reference)

ADR-025 (Ecosystem Naming Inversion, 2026-05-29) established:

| Role | Name |
|------|------|
| Protocol / ecosystem / open infrastructure | **Banza** |
| Main product / reference operator / commercial payment experience | **Banzami** |
| Protocol Operating System | **BanzAI** |

### Protected names (explicitly deferred by ADR-025)

The following are **intentionally unchanged** during the migration period:

| Protected Element | Reason |
|---|---|
| `@banza` | Identity namespace — permanent, not a brand element |
| `banzami.org` | Domain has SEO equity — deferred to separate ADR |
| `contact@banzami.org` | Public email on all communications |
| `security@banzami.org` | Security disclosure address |
| `github.com/banzami` (org) | Breaking all clone URLs — deferred |
| All crate names (`banzami-types`, etc.) | Explicitly excluded from ADR-025 scope |
| Code symbols, env vars, database tables | Explicitly excluded from ADR-025 scope |

---

## Alignment Assessment — Surface by Surface

### 1. Organisation (`github.com/banza-protocol`)

| ADR-025 Requirement | Status | Evidence |
|---|---|---|
| Org represents the Banza protocol | PARTIAL | Login is `banza-protocol`, display name is "Banza" ✓; but profile README says "Banzami" |
| Protocol identity not attributed to Banzami | FAIL | Profile README: "Banzami is a protocol-first, open-source financial kernel" |
| Protocol not described as a product/operator | PASS | Description and display name are neutral |

**Alignment score: 1/3 PASS**

---

### 2. Banza repository (`banza-protocol/banza`)

| ADR-025 Requirement | Status | Evidence |
|---|---|---|
| Presented as protocol, not product | PASS | Description, topics, README H1 all correct |
| Banzami presented as operator, not protocol | PASS | README has explicit "Banzami is the first commercial operator" section |
| BanzAI URLs use canonical routes | FAIL | README shows `banzami.org/banzamia` — migrated locally but not pushed to GitHub |
| Reference document named BANZA_REFERENCE.md | FAIL | GitHub shows `docs/BANZAMI_REFERENCE.md` |
| Governance does not attribute protocol to Banzami | FAIL | GOVERNANCE.md: "Banza is governed by Banzami (the organization)" |
| ADR-016 marked as superseded | FAIL | ADR-016 status is still "Accepted" in the file |
| Protected names preserved | PASS | Emails, domains, GitHub org URLs all preserved |
| Crate names unchanged | PASS | ADR-025 explicitly excluded crate renaming |

**Alignment score: 3/8 PASS**

---

### 3. BanzAI repository (`banza-protocol/banzai`)

| ADR-025 Requirement | Status | Evidence |
|---|---|---|
| Presented as Protocol OS, not product or protocol | PASS | README subtitle "Protocol Operating System for the Banza financial infrastructure ecosystem" |
| Associated with Banza, not Banzami | FAIL | Repo description: "orchestration layer for the **Banzami** ecosystem" |
| Canonical route references updated | FAIL | README shows `banzami.org/banzamia` — migrated locally but not on GitHub |
| Canonical env var `BANZAI_MODE` used | FAIL | README shows `BANZAMIA_MODE` throughout Quick Start |
| CLI uses `banzai` binary | FAIL | CLI section uses `banzamia ask`, `banzamia certify` |
| Protected names preserved | PASS | GitHub org URLs preserved |

**Alignment score: 2/6 PASS**

---

### 4. Banzami repository (`banza-protocol/banzami`)

| ADR-025 Requirement | Status | Evidence |
|---|---|---|
| Presented as operator/product, not protocol | PASS | README H1 "Private Commercial Product", subtitle "built on Banza infrastructure" |
| Banza identified as the protocol layer | PARTIAL | README correctly references Banza kernel in subtitle; but multiple sections use "Banza" to mean Banzami |
| Does not claim protocol ownership | PASS | README explicitly says "The open-source ecosystem lives at github.com/banzami/banzami" |
| Description attributes to correct kernel | FAIL | Description: "built on the Banzami financial infrastructure kernel" — should be "Banza" |

**Alignment score: 2/4 PASS**

---

## Overall ADR-025 Compliance Score

| Surface | PASS | TOTAL | Score |
|---------|------|-------|-------|
| Organisation | 1 | 3 | 33% |
| banza repo | 3 | 8 | 38% |
| banzai repo | 2 | 6 | 33% |
| banzami repo | 2 | 4 | 50% |
| **Total** | **8** | **21** | **38%** |

**Overall: 38% ADR-025 compliance.**

The GitHub surface has not yet undergone the structural migration that was applied to the local repositories. The org profile README is the most critical failure — it inverts the entire ADR-025 identity model at the entry point of the ecosystem's public presence.

---

## Violations by Severity

### CRITICAL (identity inversion — directly contradicts ADR-025 core decision)

1. **Org profile README titled `# Banzami`** — The banza-protocol org profile represents the Banza protocol. Titling it "Banzami" and describing "Banzami as protocol-first financial kernel" is a direct ADR-025 inversion at the most prominent entry point.

### HIGH (structural misattribution)

2. **GOVERNANCE.md: "Banza is governed by Banzami"** — Protocol governance documents must not attribute protocol stewardship to a commercial operator. This creates a false impression of operator capture.

3. **GOVERNANCE.md: "stewarded by Banzami (the organization)"** — Same issue.

4. **banzai description: "Banzami ecosystem"** — BanzAI is the Protocol OS of the **Banza** ecosystem. Associating it with "Banzami ecosystem" misattributes it to the operator.

5. **banzami description: "Banzami financial infrastructure kernel"** — There is no "Banzami financial infrastructure kernel". The kernel belongs to Banza. This directly contradicts ADR-025.

### MEDIUM (outdated — migration applied locally, not yet pushed to GitHub)

6. `banzami.org/banzamia` URL in banza README — should be `banzami.org/banzai`
7. `banzami.org/banzamia` URL in banzai README — same
8. `BANZAMIA_MODE` env vars in banzai README — canonical is `BANZAI_MODE`
9. CLI `banzamia` binary in banzai README — canonical is `banzai`
10. `docs/BANZAMI_REFERENCE.md` in banza repo — canonical is `BANZA_REFERENCE.md`
11. "Banza is built with..." (means Banzami) in banzami README — ADR-016 residue

### LOW (minor clarification needed)

12. ADR-016 status still "Accepted" — should be "Superseded by ADR-025"
13. "official Banzami SDKs" in banzami README — protocol SDKs are Banza SDKs

### PROTECTED (intentional, per ADR-025)

14. `contact@banzami.org`, `security@banzami.org` emails
15. `banzami.org` domain links
16. `github.com/banzami/...` URLs throughout all READMEs
17. Crate names `banzami-types`, `banzami-ledger`, etc.

---

*Report complete: 2026-05-30. No files modified.*
