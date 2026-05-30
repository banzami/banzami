---
title: GITHUB_PROTOCOL_GOVERNANCE_REVIEW
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: GITHUB-CANONICAL-IDENTITY-001
---

# GitHub Protocol Governance Review

**Mission:** GITHUB-CANONICAL-IDENTITY-001  
**Date:** 2026-05-30  
**Focus:** Protocol governance surfaces — who governs, who owns, who certifies

---

## Governance Surfaces Reviewed

1. `banza-protocol/banza` → `GOVERNANCE.md`
2. `banza-protocol/banza` → `docs/adr/ADR-025-ecosystem-naming-inversion.md`
3. `banza-protocol/banza` → `docs/adr/ADR-016-banzami-banza-brand-architecture.md`
4. `banza-protocol/banza` → `CONTRIBUTING.md`
5. `banza-protocol/banza` → `SECURITY.md`
6. `banza-protocol/.github` → org profile README

---

## GOVERNANCE.md Analysis

### Language that undermines protocol independence

**Finding 1:** *"Banza is governed by **Banzami** (the organization) and maintained as an open-source ecosystem project."*

This is the opening sentence of the Governance section. It attributes control of the open protocol to a commercial operator. In the ADR-025 model, Banzami is one operator among many — not the protocol's governing entity. The protocol must be able to survive the disappearance of any operator, including Banzami.

**Risk:** Any operator, regulator, or investor reading this line will conclude that Banzami (the commercial product) controls the Banza protocol rules, certification standards, and SDK compatibility. This makes the "open protocol" positioning indefensible.

**Finding 2:** *"The Banza protocol is stewarded by **Banzami** (the organization). Protocol evolution decisions are made with the following priorities..."*

Same issue. "Stewarded by Banzami" implies that if Banzami ceases operations, the protocol has no steward — i.e., the protocol dies with the operator.

**Finding 3:** *Maintainers section: "The project is maintained by [Banza](https://banzami.org)."*

This uses "Banza" as the display name but links to `banzami.org`. A visitor clicks the link expecting to reach the protocol's home page and arrives at the operator's commercial website. This is ambiguous and confuses the maintainer identity.

### Language that correctly states the boundary

**Finding 4 (positive):** The section *"Banzami — one operator among many"* reads:

> "Banzami is the first commercial operator built on Banza. It is not: A privileged operator with special kernel access / The hidden center of the ecosystem / The reference for how all operators must work."

This is correct and important. However, it directly contradicts Findings 1 and 2 within the same document. A document cannot simultaneously say "Banza is governed by Banzami" and "Banzami is not the hidden center of the ecosystem."

### Governance contact emails

All contacts reference `@banzami.org` addresses:
- `security@banzami.org`
- `conduct@banzami.org`

These are **PROTECTED per ADR-025** and intentionally unchanged during the migration period. However, they reinforce the perception that the protocol is an arm of the Banzami company.

---

## ADR-025 Document Review

The ADR-025 document itself (`docs/adr/ADR-025-ecosystem-naming-inversion.md`) is **well-formed and accurate**:

- Correctly defines the three layers
- Documents the protected names and their reasons
- Explains the migration principle ("Break nothing blindly")
- Non-Goals section explicitly prevents premature renaming
- Compatibility period wording is appropriate

**One gap:** The document's author field reads `Organização Banzami` and deciders field reads `Fidel Monteiro (Founder)`. This is accurate but highlights that a single commercial entity (Banzami) authored the ADR that established the naming model for an "open protocol." A more resilient governance model would distinguish between:
- The entity that authored the ADR (Banzami)
- The entity that governs the protocol going forward

This is not a problem now, but becomes relevant when the first external operator seeks certification.

---

## ADR-016 Status

ADR-016 (`ADR-016-banzami-banza-brand-architecture.md`) has `**Status:** Accepted` but is **superseded by ADR-025**.

An ADR that has been superseded but shows "Accepted" is a governance landmine: a contributor reading ADR-016 first will apply ADR-016 rules without knowing ADR-025 overrides them.

**Required fix:** ADR-016 status line should read: `**Status:** Superseded by ADR-025 (2026-05-29)`

---

## Certification Governance

The banzai repo (Protocol OS) handles operator certification (L0–L4). The GOVERNANCE.md of the banza repo does not address:

- Who certifies operators if BanzAI (the certification tool) and Banzami (the operator) are the same entity?
- What prevents Banzami from certifying itself at L4 without independent verification?
- How do competing operators get certified fairly if the certification tool is controlled by the first operator?

These are not current problems (there is currently only one operator), but they become critical at the moment the protocol claims to be a multi-operator, open infrastructure. The governance model must address this before any second operator attempts certification.

---

## Contributing Governance

`CONTRIBUTING.md` correctly scopes out-of-scope areas:

> "The Banzami commercial product (apps, backend services, production infrastructure)"  
> "Banzami design system and branded UI components"

This correctly distinguishes what belongs to the protocol vs. the operator. This is a strong positive signal.

However, the clone instruction `git clone https://github.com/banzami/banzami.git` (PROTECTED, not yet renamed) will remain confusing until the GitHub org migration is executed. A new contributor must follow a URL to the old `banzami` org to contribute to a repository called `banza` in the `banza-protocol` org.

---

## Security Policy

`SECURITY.md` is clean. Scope is well-defined:

> "Out of scope: The Banzami commercial product (separate private repository)"

This correctly distinguishes protocol security from operator security.

The financial invariant vulnerability list (`banzami-ledger/src/`, `banzami-wallets/src/`) uses crate names that are PROTECTED per ADR-025 — correct.

---

## Summary: Governance Risks

| Risk | Surface | Severity |
|------|---------|----------|
| Protocol attributed to commercial operator | GOVERNANCE.md | HIGH |
| No mechanism for operator-independent governance | GOVERNANCE.md (absent) | HIGH |
| ADR-016 active but superseded | ADR-016 status | MEDIUM |
| Certification independence gap (self-certifying operator) | Not documented anywhere | MEDIUM |
| Maintainer identity links to operator domain | GOVERNANCE.md maintainers | LOW |
| Contribution path requires old GitHub org URL | CONTRIBUTING.md | LOW (PROTECTED) |

---

*Report complete: 2026-05-30. No files modified.*
