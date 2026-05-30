---
title: CLAUDE_ALIGNMENT_REPORT
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: CLAUDE-MD-CANONICAL-ALIGNMENT-001
---

# CLAUDE Alignment Report

**Mission:** CLAUDE-MD-CANONICAL-ALIGNMENT-001  
**Date:** 2026-05-30

---

## Part 1 — Inventory

| Repository | CLAUDE.md before | Status |
|---|---|---|
| `~/banza` | ABSENT | Created fresh |
| `~/banzai` | ABSENT | Created fresh |
| `~/banzami` | PRESENT (1,400+ lines, ADR-016 language) | Rewritten |

### banzami/CLAUDE.md — Legacy analysis

The existing file was the "Banza Engineering Constitution" — a comprehensive engineering document written under the ADR-016 naming model. Key issues found:

**Identity:**
- Title: "Banza Engineering Constitution" — used "Banza" to mean the product/operator
- Section 1.1: "Banza exists to modernize payments" — correct concept, wrong entity name
- Section 1.5: "CORRECT descriptions of Banza: Angola's instant payment network" — product descriptions attributed to wrong name

**Section 2.6:** "Banza is building realtime African payment infrastructure" — should be "Banzami"
**Section 2.7:** "What Banza IS: a wallet-native payment network" — should be "Banzami"
**Section 13:** "Banza is infrastructure" — ambiguous (correct for protocol, wrong for operator)
**Section 16.1:** ADR-016 model stated: "Banza = organization / ecosystem / infrastructure / institutional entity" and "Banzami = main payment product" — INVERTED under ADR-025

---

## Part 2 — Shared Rules Extracted

**File created:** `~/banza/docs/governance/CLAUDE_BASE.md`

Rules extracted and placed in the base document:

| Rule | Source |
|---|---|
| ADR-025 canonical hierarchy (BANZA / BanzAI / Banzami) | New |
| Forbidden assumptions table | New |
| Naming rules by entity | ADR-025 |
| Protected names (ADR-025 deferred) | ADR-025 |
| SDK naming conventions | banzami CLAUDE.md §14 |
| Commit standards | banzami CLAUDE.md §12 |
| Documentation standards (ADRs, domain docs) | banzami CLAUDE.md §5 |
| Security standards | banzami CLAUDE.md §7 |
| Testing standards | banzami CLAUDE.md §8 |
| Financial correctness rules | banzami CLAUDE.md §10 |
| Protocol terminology glossary | New |
| Audit methodology (classification scheme) | GITHUB-CANONICAL-IDENTITY-001 |

---

## Part 3 — Repository-Specific Rules Defined

### banza (Protocol Kernel)

| Rule | Source |
|---|---|
| "The protocol exists independently of any operator." | New (Part 4 requirement) |
| Never introduce product logic into protocol specifications | New guardrail |
| Never make the protocol dependent on a single operator | New guardrail |
| Protocol specs ship before operator implementations | New guardrail |
| All financial invariants listed (INV-LEDGER-*, etc.) | From validation governance |
| Rust financial kernel standards (integer arithmetic, atomic writes) | New |
| ADR reference table | Extracted from banzami |
| Validation governance (approval gates) | From banzami CLAUDE.md §17 |

### banzai (Protocol OS)

| Rule | Source |
|---|---|
| "BanzAI serves the BANZA protocol ecosystem." | New (Part 4 requirement) |
| Never present BanzAI as an independent product | New guardrail |
| Tools determine truth. LLM explains truth. | From banzai CONTRIBUTING.md |
| Every protocol claim must be traceable to RFC/ADR/contract | New guardrail |
| BanzAI does not define protocol rules | New guardrail |
| Never associate BanzAI with the Banzami commercial product | New guardrail |
| Prompt engineering standards | From banzami CLAUDE.md §6 |
| Conformance and certification levels (L0–L4) | From banzai README |
| Deployment env vars (BANZAI_MODE canonical) | From migration |

### banzami (Reference Operator)

| Rule | Source |
|---|---|
| "Banzami is one implementation of BANZA." | New (Part 4 requirement) |
| Never redefine protocol rules locally | New guardrail |
| Consume protocol definitions from ~/banza | New guardrail |
| Protocol rule changes happen in ~/banza via ADR, not here | New guardrail |
| Operator-specific product naming (Banzami Wallet, Banzami Business, etc.) | ADR-025 |
| Deploy script reference (./deploy.sh + server) | Existing |
| Docs deploy architecture (dual sync: deploy.sh + Dockerfile) | Existing |
| Validation governance approval gates | banzami CLAUDE.md §17 |
| Repository layout freeze | banzami CLAUDE.md §20 |

---

## Part 4 — Legacy Terminology Removed

### Before / After table

| Surface | Legacy string | Replacement | Classification |
|---|---|---|---|
| banzami CLAUDE.md title | "Banza Engineering Constitution" | "Banzami — Reference Operator Engineering Constitution" | OUTDATED |
| banzami §1.1 | "Banza exists to..." | "Banzami exists to..." | OUTDATED |
| banzami §1.3 | "Banza enables: taxi apps, cantinas..." | "Banzami demonstrates: taxi apps, cantinas..." | OUTDATED |
| banzami §1.5 | "CORRECT descriptions of Banza: Angola's instant payment network" | Added: "Banzami is one operator — BANZA is the protocol" | OUTDATED |
| banzami §1.6 | "Banza provides the UX layer, wallet layer..." | "Banzami provides the UX layer, wallet layer... on top of BANZA protocol" | OUTDATED |
| banzami §2.6 | "Banza is building realtime African payment infrastructure" | "Banzami is building realtime Angolan payment infrastructure...on top of the open BANZA protocol" | OUTDATED |
| banzami §2.7 | "What Banza IS: a wallet-native payment network" | "What Banzami IS: a wallet-native payment network" | OUTDATED |
| banzami §13 | "Banza is infrastructure" | "Banzami is a national-scale payment operator" | OUTDATED |
| banzami §14 | "Banza is an SDK-first platform" | "Banzami is an SDK-first operator. ALL applications must use official BANZA protocol SDKs" | OUTDATED |
| banzami §16.1 | "Banza = organization / ecosystem / infrastructure" | Replaced with ADR-025 three-layer model | FALSE (ADR-016 residue) |
| banzami §16.2 | "Use 'Banzami' for product-level context" | Retained — correct under ADR-025 | CORRECT |
| banzami §16.3 | "Use 'Banza' for organizational context" | Replaced: "Use 'BANZA' or 'Banza' for protocol context" | OUTDATED |
| banzami §16.4 | `Banzami (organization) └── Banza (main product)` | `BANZA (protocol) ├── BanzAI └── Banzami (operator)` | FALSE (ADR-016) |

**Instances of "BANZAMIA" found:** 0 (already cleaned by BANZA-STRUCTURAL-NAMING-MIGRATION-001)

---

## Part 5 — Final CLAUDE Structure

### ~/banza/CLAUDE.md (new)

```
Header: "I am working on the open financial infrastructure protocol."
Identity: ADR-025 three layers
Ecosystem guardrail: "The protocol exists independently of any operator."
Responsibilities: core/, contracts/, sdk/, conformance/, sdk-certification/, reference/
Guardrails: no product logic in specs, no single-operator dependency, no invariant weakening
Tech stack: Rust/Go/PostgreSQL/Redis
Rust standards: integer arithmetic, atomic writes, idempotency
ADR reference table
Validation governance
Deployment note (via ~/banzami deploy.sh)
What this repo is NOT
```

### ~/banzai/CLAUDE.md (new)

```
Header: "I am working on the Protocol Operating System."
Identity: ADR-025 three layers
Ecosystem guardrail: "BanzAI serves the BANZA protocol ecosystem."
Responsibilities: apps/api, apps/web, apps/cli, contexts/, prompts/, core/
Guardrails: not independent product, tools-determine-truth, traceable claims, no protocol rule authoring
Tech stack: Hono/Node.js/Qdrant/Anthropic Claude
Prompt engineering standards
Conformance levels (L0–L4)
Deployment (via ~/banzami deploy.sh banzai-api)
What BanzAI is NOT
```

### ~/banzami/CLAUDE.md (rewritten)

```
Header: "I am working on the reference operator implementation of BANZA."
Identity: ADR-025 three layers
Reference operator guardrail: "Banzami is one implementation of BANZA."
Mission: §1 (operator language throughout)
Core engineering: §2 (corrected to say "Banzami", not "Banza")
Tech stack: §3 (unchanged)
Repository structure: §4 (~/banzami)
Documentation standards: §5
Security: §6
Engineering quality: §7
Observability: §8
Financial architecture: §9
API standards: §10
Git standards: §11
Operational philosophy: §12 (corrected: "Banzami is a national-scale payment operator")
SDK-first: §13 (corrected: "BANZA protocol SDKs")
Documentation source of truth: §14 (BANZA_REFERENCE.md)
Brand architecture: §15 (ADR-025 model replaces ADR-016)
Validation governance: §16
Governance primitive freeze: §17
Final principle: §18
Repository layout freeze: §19
```

---

## Part 6 — Success Criteria Verification

| Test | Result |
|---|---|
| New session in ~/banza understands "I am working on the protocol" | ✓ Header line 1 states this explicitly |
| New session in ~/banzai understands "I am working on the Protocol OS" | ✓ Header line 1 states this explicitly |
| New session in ~/banzami understands "I am working on the reference operator" | ✓ Header line 1 states this explicitly |
| No CLAUDE.md contradicts ADR-025 | ✓ All three verified |
| "The protocol exists independently of any operator" stated in banza | ✓ Stated in guardrail and header |
| "BanzAI serves the BANZA protocol ecosystem" stated in banzai | ✓ Stated in guardrail and header |
| "Banzami is one implementation of BANZA" stated in banzami | ✓ Stated in guardrail and header |
| Legacy ADR-016 model removed from banzami | ✓ §16.1 and §16.4 replaced |
| "BANZAMIA" occurrences | 0 found — already cleaned by previous migration |

---

## Files Created / Modified

| File | Action |
|---|---|
| `~/banza/docs/governance/CLAUDE_BASE.md` | Created — shared ecosystem rules |
| `~/banza/CLAUDE.md` | Created — protocol kernel identity |
| `~/banzai/CLAUDE.md` | Created — Protocol OS identity |
| `~/banzami/CLAUDE.md` | Rewritten — reference operator identity |
| `~/banza/docs/migration/CLAUDE_ALIGNMENT_REPORT.md` | Created — this report |

---

*Alignment complete: 2026-05-30.*
