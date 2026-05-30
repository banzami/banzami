---
name: final-cross-repo-consistency-audit
description: Final cross-repository consistency audit across ~/banza, ~/banzai, ~/banzami — ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001
metadata:
  type: project
---

# Final Cross-Repository Consistency Audit

**Mission:** ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001  
**Date:** 2026-05-30  
**Scope:** ~/banza · ~/banzai · ~/banzami  
**Method:** Audit only — no modifications in this phase

---

## Executive Summary

| Severity | Count | Verdict |
|----------|-------|---------|
| **P0** — Breaks ADR-025 | **0** | ✓ PASS |
| **P1** — Creates conceptual confusion | **5** | ⚠ REQUIRES FIXES |
| **P2** — Stale reference/path | **28** | ⚠ BATCH FIXABLE |
| **P3** — Cosmetic | **3** | INFO |

**The canonical reference layer (REFERENCE, ARCHITECTURE, GOVERNANCE, SECURITY, ROADMAP, CLAUDE.md files) is clean.** All P1 and P2 issues are in legacy documents: README files, CONTRIBUTING files, Cargo.toml fields, package.json metadata, and pre-ADR-025 docs subdirectories.

---

## Audit Axis 1 — Identity Consistency

**Test:** BANZA = protocol. BanzAI = Protocol OS. Banzami = reference operator.

### ~/banza CLAUDE.md

```
BANZA    = open financial infrastructure protocol  ← THIS REPO
BanzAI   = Protocol Operating System              ~/banzai
Banzami  = Reference operator implementation      ~/banzami
```
**Status: PASS ✓**

### ~/banzai CLAUDE.md

```
BANZA    = open financial infrastructure protocol   ~/banza
BanzAI   = Protocol Operating System               ← THIS REPO
Banzami  = Reference operator implementation        ~/banzami
```
**Status: PASS ✓**

### ~/banzami CLAUDE.md

```
BANZA    = open financial infrastructure protocol
BanzAI   = Protocol Operating System
Banzami  = reference operator implementation      ← THIS REPO
```
**Status: PASS ✓**

### ~/banza README.md

- Header ecosystem table: PASS ✓
- **FINDING P1-001:** "What is Banza?" section uses lowercase `Banza` throughout instead of `BANZA` (9 occurrences). Acceptable per ADR-016 legacy but creates impression the protocol's name is "Banza" not "BANZA".
- **FINDING P1-002:** Naming note line 49: `"Banza was formerly called Banzami"` — MISLEADING. The BANZA protocol was never called Banzami. The original monorepo was named `banzami/banzami` on GitHub, but the protocol brand was always `Banza/BANZA`. This creates false history.

### ~/banzai README.md

- Header ecosystem table: PASS ✓  
- **FINDING P1-003:** Claims **"8 Capabilities"** with capabilities `Prever` and `Guiar` — but `BANZAI_REFERENCE.md §5` is the canonical source and lists only **6 capabilities**: Compreender, Explicar, Validar, Simular, Certificar, Federar. The README and canonical REFERENCE document directly contradict each other on a headline metric.

### ~/banzami README.md

- Header ecosystem table: PASS ✓  
- **FINDING P1-004:** Lines 41, 69, 97, 114, 583, 629, 699, 707, 715, 835, 1259: Uses `"Banza"` as the subject when describing Banzami (the operator). Examples:
  - `"Banza is built with: fintech-grade agility, banking-grade reliability…"` — describes the operator's engineering philosophy using the protocol's name
  - `"Banza follows a modular monolith architecture"` — describes the operator's architecture using the protocol's name
  - `"Banza is building the digital payment layer for Angola"` — describes the operator's mission using the protocol's name
- **FINDING P1-005:** Line 13: `"The open-source ecosystem (SDKs, contracts, protocol specs, integrations) lives at [github.com/banzami/banzami](https://github.com/banzami/banzami)."` — DOUBLE ERROR: (a) this incorrectly assigns `BANZA`'s identity ("open-source ecosystem with SDKs, contracts, protocol specs") to `Banzami`, (b) the URL points to old org `banzami/banzami` not `banza-protocol/banzami`.

---

## Audit Axis 2 — Ownership Consistency

**Test:** BANZA owns rules. BanzAI explains rules. Banzami implements rules.

### Canonical reference documents (BANZA_REFERENCE, BANZAI_REFERENCE, BANZAMI_REFERENCE)

All three canonical reference documents correctly state ownership:
- `BANZA_REFERENCE.md`: "BANZA defines the rules" ✓
- `BANZAI_REFERENCE.md`: "Tools determine truth. AI explains truth." ✓  
- `BANZAMI_REFERENCE.md`: "Banzami é um operador entre futuros muitos — não o dono do protocolo." ✓

**Status: PASS ✓**

### Governance documents

- `BANZA_GOVERNANCE.md`: Governs protocol decisions via ADR/RFC process ✓
- `BANZAI_GOVERNANCE.md`: Governs Protocol OS decisions, defers protocol to ~/banza ✓
- `BANZAMI_GOVERNANCE.md`: Governs operator decisions, defers protocol to ~/banza ✓

**Status: PASS ✓**

### ADDITIONAL FINDING

- `~/banza/docs/BANZAMI_REFERENCE.md` (line 10): Pre-ADR-025 combined reference still present in the banza protocol repo. Contains: `"github.com/banzami/banzami contém os SDKs, contratos e especificações de protocolo. O produto Banzami (apps, serviços, infra) é privado em github.com/banzami/banza."` — Both URLs are stale and the document is a pre-separation artifact. **P2-001**

---

## Audit Axis 3 — Cross-Reference Consistency

**Test:** All `../banza/`, `../banzai/`, `../banzami/` relative paths are valid.

### Verified paths (all resolve to existing files)

| Path | From | Status |
|------|------|--------|
| `../banza/BANZA_REFERENCE.md` | banzai/*.md | ✓ EXISTS |
| `../banza/BANZA_CERTIFICATION.md` | banzai/*.md | ✓ EXISTS |
| `../banza/BANZA_CONFORMANCE.md` | banzai/*.md | ✓ EXISTS |
| `../banza/BANZA_ROADMAP.md` | banzai/*.md | ✓ EXISTS |
| `../banzami/BANZAMI_REFERENCE.md` | banzai/*.md | ✓ EXISTS |
| `../banzami/BANZAMI_ARCHITECTURE.md` | banzai/*.md | ✓ EXISTS |
| `../banzami/BANZAMI_DEPLOYMENT.md` | banzai/*.md | ✓ EXISTS |
| `../banzami/BANZAMI_ROADMAP.md` | banzai/*.md | ✓ EXISTS |
| `../banzai/BANZAI_REFERENCE.md` | banza/*.md | ✓ EXISTS |
| `../banzai/BANZAI_CAPABILITIES.md` | banza/*.md | ✓ EXISTS |
| `../banzami/BANZAMI_REFERENCE.md` | banza/*.md | ✓ EXISTS |
| `../banzami/BANZAMI_ARCHITECTURE.md` | banza/*.md | ✓ EXISTS |
| `../banza/docs/governance/CLAUDE_BASE.md` | banzai/CLAUDE.md | ✓ EXISTS |

**Cross-repo canonical path status: PASS ✓** — No broken links in canonical documents.

---

## Audit Axis 4 — GitHub Consistency

**Test:** All URLs point to `github.com/banza-protocol/{banza,banzai,banzami}`.

### P1/P2 findings — stale `github.com/banzami/` URLs

| File | Line | Stale URL | Correct URL | Severity |
|------|------|-----------|-------------|----------|
| `banzami/README.md` | 13 | `github.com/banzami/banzami` | `github.com/banza-protocol/banzami` | P1 (part of P1-005) |
| `banza/README.md` | 273–274 | `github.com/banzami/banzami` (Cargo snippet) | `github.com/banza-protocol/banzami` | P2-002 |
| `banza/README.md` | 469 | `github.com/banzami/banza` (private) | `github.com/banza-protocol/banzami` | P2-003 |
| `banza/core/Cargo.toml` | 29 | `github.com/banzami/banzami` | `github.com/banza-protocol/banzami` | P2-004 |
| `banza/core/README.md` | 72–73 | `github.com/banzami/banzami` | `github.com/banza-protocol/banzami` | P2-005 |
| `banza/docs/getting-started.md` | 46 | `github.com/banzami/banzami` | `github.com/banza-protocol/banzami` | P2-006 |
| `banza/sdk/go/README.md` | 10, 23 | `github.com/banzami/banzami-go` | `github.com/banza-protocol/banzami-go` | P2-007 |
| `banza/sdk/python/pyproject.toml` | 42–43 | `github.com/banzami/sdk-python` | `github.com/banza-protocol/sdk-python` | P2-008 |
| `banza/docs/adr/ADR-018-open-financial-kernel.md` | 24 | `github.com/banzami/banzami` | `github.com/banza-protocol/banzami` | P2-009 |
| `banza/docs/adr/ADR-024-reference-operator.md` | 53 | `github.com/banzami/banzami.git` | `github.com/banza-protocol/banzami.git` | P2-010 |
| `banzai/CONTRIBUTING.md` | 23 | `github.com/banzami/banzami` (protocol kernel) | `github.com/banza-protocol/banza` | P2-011 |
| `banzai/CONTRIBUTING.md` | 45 | `github.com/banzami/banzamia` (fork) | `github.com/banza-protocol/banzai` | P2-012 |
| `banzami/core/Cargo.toml` | 32 | `github.com/banzami/banza` | `github.com/banza-protocol/banzami` | P2-013 |
| `banzami/sdk/go/README.md` | 10, 23 | `github.com/banzami/banzami-go` | `github.com/banza-protocol/banzami-go` | P2-014 |
| `banzami/sdk/python/pyproject.toml` | 42–43 | `github.com/banzami/sdk-python` | `github.com/banza-protocol/sdk-python` | P2-015 |
| `banzami/docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md` | 239, 252 | `github.com/banzami/banza` | `github.com/banza-protocol/banzami` | P2-016 |
| `banzami/apps/docs/data/operators.json` | 11 | `github.com/banzami/banzami` | `github.com/banza-protocol/banzami` | P2-017 |

**Additional package metadata:**
| File | Field | Stale Value | P# |
|------|-------|-------------|-----|
| `banzai/package.json` | `name` | `@banzami/banzamia` | P2-018 |

---

## Audit Axis 5 — Domain Consistency

**Test:** `banzami.org` is current deployment. `banza.network` is future protocol domain. No confusion.

### `banza.network`

Zero mentions across all three repos. No document implies this is a current domain.  
**Status: PASS ✓** (The future domain is correctly absent from current documentation.)

### `banzami.org/banzamia` stale URLs (should be `banzami.org/banzai`)

Per the ADR-025 route migration (301 redirects `/banzamia` → `/banzai` and `/sobre-banzamia` → `/sobre-o-banzai` confirmed in `banzami/CLAUDE.md §14.6`), all documentation references should use the new routes.

| File | Stale Reference | Correct Reference | Severity |
|------|----------------|-------------------|----------|
| `banza/README.md` | `banzami.org/banzamia` (×3: lines 124, 132, 196) | `banzami.org/banzai` | P2-019 |
| `banza/README.md` | `banzami.org/sobre-banzamia` (line 197) | `banzami.org/sobre-o-banzai` | P2-020 |
| `banza/apps/banzai/README.md` | `banzami.org/banzamia` → `/banzamia` path | `banzami.org/banzai` | P2-021 |
| `banzami/docs/glossary.md` | `banzami.org/banzamia` | `banzami.org/banzai` | P2-022 |
| `banzami/docs/index.md` | `banzami.org/banzamia` (×2) | `banzami.org/banzai` | P2-023 |
| `banzami/docs/banzamia/overview.md` | `banzami.org/banzamia` | `banzami.org/banzai` | P2-024 |
| `banzami/docs/banzamia/roadmap.md` | `/banzamia` route | `/banzai` | P2-025 |
| `banzami/docs/BANZA_REFERENCE.md` | `banzami.org/banzamia` (multiple) | `banzami.org/banzai` | P2-026 |

**Note:** `banzami/docs/BANZA_REFERENCE.md` is the website source of truth (read at build time). Its `banzamia` route references resolve via 301 redirect, so the site works — but the source document should use canonical routes.

---

## Audit Axis 6 — Governance Consistency

**Test:** No document says Banzami governs BANZA.

- `BANZA_GOVERNANCE.md`: "governed as an open protocol — RFC and ADR process, not any single operator" ✓
- `BANZAI_GOVERNANCE.md`: Protocol-affecting decisions deferred to ~/banza ✓
- `BANZAMI_GOVERNANCE.md`: "Protocol rule changes happen in ~/banza via ADR, not here" ✓
- `BANZAMI_REFERENCE.md`: "Banzami NÃO é o protocolo BANZA" ✓

**Status: PASS ✓**

---

## Audit Axis 7 — Certification Consistency

**Test:** Certification rules belong to BANZA. BanzAI assists. Banzami has no special authority.

- `BANZA_CERTIFICATION.md`: Defines L0–L4, process, universals ✓
- `BANZAI_CAPABILITIES.md`: "only the conformance suite determines certification" ✓
- `BANZAMI_REFERENCE.md`: "T+0 — invariante do protocolo — ver BANZA_REFERENCE.md §7" ✓

**Status: PASS ✓**

---

## Audit Axis 8 — Roadmap Consistency

**Test:** BANZA = protocol roadmap. BanzAI = OS roadmap. Banzami = operator roadmap.

| File | Content | Correct Owner | Status |
|------|---------|--------------|--------|
| `BANZA_ROADMAP.md` | Conformance Suite v1, certification, federation, open RFC | Protocol ✓ | PASS |
| `BANZAI_ROADMAP.md` | Live API, Live AI, Protocol Copilots, Audit Assistants | Protocol OS ✓ | PASS |
| `BANZAMI_ROADMAP.md` | PHP SDK, payout automation, Banzami Wallet mobile | Operator ✓ | PASS |

**Each roadmap explicitly excludes other layers' items and cross-references the others.**  
**Status: PASS ✓**

---

## Audit Axis 9 — Security Consistency

**Test:** BANZA_SECURITY = protocol invariants. BANZAI_SECURITY = AI safety. BANZAMI_SECURITY = payments/wallet.

| File | Scope | Correct |
|------|-------|---------|
| `BANZA_SECURITY.md` | Protocol kernel crates, SDK, QR contracts | ✓ |
| `BANZAI_SECURITY.md` | Prompt injection, protocol misinformation, read-only constraint | ✓ |
| `BANZAMI_SECURITY.md` | Payment flows, wallet APIs, merchant/consumer APIs | ✓ |

**Status: PASS ✓**

---

## Audit Axis 10 — Product Boundary

**Test:** BANZA docs do not describe products. Banzami docs do not redefine protocol rules.

| Check | Status |
|-------|--------|
| BANZA_ARCHITECTURE.md does not describe Banzami Wallet or Business | ✓ PASS |
| BANZA_MANIFESTO.md mentions Banzami only as reference operator | ✓ PASS |
| BANZAMI_ARCHITECTURE.md cross-references BANZA_ARCHITECTURE.md rather than duplicating rules | ✓ PASS |
| BANZAMI_PRODUCTS.md cross-references BANZA_CERTIFICATION.md rather than duplicating certification levels | ✓ PASS |
| BANZAI_CAPABILITIES.md does not describe Banzami Wallet features | ✓ PASS |
| `banzami/docs/BANZA_REFERENCE.md` (website source) mixes product and protocol content | Pre-ADR-025 artifact. Routes exist. Not a new violation. INFO |

**Status: PASS ✓** (for all canonical documents)

---

## Summary of All Findings

| ID | Severity | File | Issue |
|----|----------|------|-------|
| P1-001 | P1 | `banza/README.md:47–70` | Lowercase "Banza" used as protocol name throughout "What is Banza?" section |
| P1-002 | P1 | `banza/README.md:49` | Naming note "Banza was formerly called Banzami" — misleading/false history |
| P1-003 | P1 | `banzai/README.md:27` | "8 Capabilities" contradicts `BANZAI_REFERENCE.md` which defines 6 capabilities |
| P1-004 | P1 | `banzami/README.md:41,69,97,114+` | "Banza is built with…" — uses protocol name to describe operator engineering |
| P1-005 | P1 | `banzami/README.md:13` | "open-source ecosystem lives at github.com/banzami/banzami" — assigns BANZA identity to Banzami + wrong URL |
| P2-001 | P2 | `banza/docs/BANZAMI_REFERENCE.md` | Pre-ADR-025 combined reference with stale URLs in protocol repo |
| P2-002 | P2 | `banza/README.md:273–274` | Cargo snippet uses `github.com/banzami/banzami` |
| P2-003 | P2 | `banza/README.md:469` | `github.com/banzami/banza` listed as Banzami's private repo URL |
| P2-004 | P2 | `banza/core/Cargo.toml:29` | `repository` field: `github.com/banzami/banzami` |
| P2-005 | P2 | `banza/core/README.md:72–73` | Cargo dependency snippet uses `github.com/banzami/banzami` |
| P2-006 | P2 | `banza/docs/getting-started.md:46` | `git clone github.com/banzami/banzami` |
| P2-007 | P2 | `banza/sdk/go/README.md:10,23` | `github.com/banzami/banzami-go` |
| P2-008 | P2 | `banza/sdk/python/pyproject.toml:42–43` | `github.com/banzami/sdk-python` |
| P2-009 | P2 | `banza/docs/adr/ADR-018-open-financial-kernel.md:24` | `github.com/banzami/banzami` |
| P2-010 | P2 | `banza/docs/adr/ADR-024-reference-operator.md:53` | `github.com/banzami/banzami.git` |
| P2-011 | P2 | `banzai/CONTRIBUTING.md:23` | `github.com/banzami/banzami` for "protocol kernel changes" |
| P2-012 | P2 | `banzai/CONTRIBUTING.md:45` | `github.com/banzami/banzamia` as fork URL |
| P2-013 | P2 | `banzami/core/Cargo.toml:32` | `repository = github.com/banzami/banza` |
| P2-014 | P2 | `banzami/sdk/go/README.md:10,23` | `github.com/banzami/banzami-go` |
| P2-015 | P2 | `banzami/sdk/python/pyproject.toml:42–43` | `github.com/banzami/sdk-python` |
| P2-016 | P2 | `banzami/docs/architecture/BANZAMI_ECOSYSTEM_REFERENCE.md:239,252` | `github.com/banzami/banza` and `github.com/banzami/banzami` |
| P2-017 | P2 | `banzami/apps/docs/data/operators.json:11` | `github.com/banzami/banzami` |
| P2-018 | P2 | `banzai/package.json` | `name: @banzami/banzamia` — pre-ADR-025 package name |
| P2-019 | P2 | `banza/README.md:124,132,196` | `banzami.org/banzamia` → should be `banzami.org/banzai` |
| P2-020 | P2 | `banza/README.md:197` | `banzami.org/sobre-banzamia` → should be `banzami.org/sobre-o-banzai` |
| P2-021 | P2 | `banza/apps/banzai/README.md:22,71` | `apps/banzamia/` directory path — renamed to `apps/banzai/` |
| P2-022 | P2 | `banzami/docs/glossary.md:70` | `banzami.org/banzamia` |
| P2-023 | P2 | `banzami/docs/index.md:26,34,48` | `banzami.org/banzamia` (×3) |
| P2-024 | P2 | `banzami/docs/banzamia/overview.md:11` | `banzami.org/banzamia` |
| P2-025 | P2 | `banzami/docs/banzamia/roadmap.md:11,17` | `/banzamia` route |
| P2-026 | P2 | `banzami/docs/BANZA_REFERENCE.md` | `banzami.org/banzamia` route references (multiple) |
| P3-001 | P3 | `banza/README.md` | "Banza" (mixed case) vs "BANZA" (all-caps) inconsistency in flowing text |
| P3-002 | P3 | `banzai/apps/banzai/README.md` | `apps/banzamia/` directory shown in architecture diagram |
| P3-003 | P3 | `banzami/docs/banzamia/` | Directory name pre-dates ADR-025 rename; files inside use old paths |

---

*Produced by: ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001 — 2026-05-30*
