---
title: GITHUB_POSITIONING_GAPS
version: 1.0
date: 2026-05-30
status: COMPLETE
mission: GITHUB-CANONICAL-IDENTITY-001
---

# GitHub Positioning Gaps

**Mission:** GITHUB-CANONICAL-IDENTITY-001  
**Date:** 2026-05-30

---

## Phase 6 — Comprehension Test

Four simulated visitors, each accessing a single entry point.

---

### Visitante A — Enters only the organisation: `github.com/banza-protocol`

The visitor reads the org profile README (displayed at the org homepage).

**What the visitor learns:**

The org profile README is titled `# Banzami` and opens: *"Banzami is a protocol-first, open-source financial kernel designed for the African financial ecosystem. It defines the rules — wallets, transfers, ledger, settlement, traceability."*

| Question | What the visitor concludes | Correct? |
|----------|---------------------------|----------|
| What is BANZA? | Not mentioned. The visitor does not encounter the word "Banza" as the protocol name. | NO |
| What is BanzAI? | Listed in ecosystem table as `banzami/banzamia` — no description | NO |
| What is Banzami? | A protocol-first, open-source financial kernel. The thing that defines the rules. | NO — this is Banza's identity |
| Relationship between the three? | Banzami is the infrastructure. Others are subordinate products. | INVERTED |
| Who controls the protocol? | Banzami (the organization) | MISLEADING |
| Does the protocol belong to a company? | Yes — Banzami | MISLEADING |
| What survives if an operator disappears? | Nothing is mentioned about protocol survivability | NOT COMMUNICATED |

**Comprehension verdict:** FAIL — The org profile inverts the ADR-025 identity model entirely. A visitor forming their mental model of the ecosystem at this entry point will hold false beliefs about every layer of the hierarchy.

---

### Visitante B — Enters only the banza repository: `banza-protocol/banza`

The visitor reads the banza README.

**What the visitor learns:**

The README has a naming note, presents Banza as open-source financial infrastructure, shows a clear public/private split table, and has a section explicitly positioning Banzami as "the first commercial operator."

| Question | What the visitor concludes | Correct? |
|----------|---------------------------|----------|
| What is BANZA? | Open-source financial infrastructure kernel. Like Linux for payments. | YES |
| What is BanzAI? | Protocol Operating System. 16 modules, 8 capabilities. (Details in BanzAI section) | YES |
| What is Banzami? | First commercial operator built on Banza. Ubuntu to Linux. | YES |
| Relationship between the three? | Banza → BanzAI + Banzami as operator | YES |
| Who controls the protocol? | Governed by "Banzami (the organization)" per GOVERNANCE.md | MISLEADING |
| Does the protocol belong to a company? | GOVERNANCE.md says "governed by Banzami" | MISLEADING |
| What survives if an operator disappears? | The kernel/contracts/SDKs remain | IMPLIED but not stated |

**Comprehension verdict:** PARTIAL PASS — The README itself communicates the correct hierarchy. However, GOVERNANCE.md contradicts the README by attributing protocol governance to a commercial operator (Banzami). A visitor who reads GOVERNANCE.md will come away with a different picture.

---

### Visitante C — Enters only the banzai repository: `banza-protocol/banzai`

The visitor reads the banzai README.

**What the visitor learns:**

The README title is `# BanzAI` and the subtitle correctly says "Protocol Operating System for the Banza financial infrastructure ecosystem."

| Question | What the visitor concludes | Correct? |
|----------|---------------------------|----------|
| What is BANZA? | The financial infrastructure ecosystem that BanzAI serves | YES (inferred) |
| What is BanzAI? | Protocol OS. 16 modules, 8 capabilities, deterministic-first. | YES |
| What is Banzami? | Unclear — the repo description says "Banzami ecosystem" and `banzami.org/banzamia` appears as the access URL | CONFUSED |
| Relationship between the three? | BanzAI belongs to Banza; but description says "Banzami ecosystem" | CONFLICTED |
| Who controls the protocol? | Not addressed | NOT COMMUNICATED |
| Does the protocol belong to a company? | Not addressed | NOT COMMUNICATED |
| What survives if an operator disappears? | Not addressed | NOT COMMUNICATED |

**Comprehension verdict:** PARTIAL FAIL — The README body is mostly correct but the repository description ("Banzami ecosystem") directly contradicts the README subtitle ("Banza financial infrastructure ecosystem"). The outdated `banzami.org/banzamia` URLs in the README create confusion about where BanzAI actually lives. A visitor forms a mixed picture.

---

### Visitante D — Enters only the banzami repository: `banza-protocol/banzami`

The visitor reads the banzami README (private repo — requires access).

**What the visitor learns:**

The README subtitle is "built on Banza infrastructure" which is correct. However, the description says "built on the Banzami financial infrastructure kernel" (incorrect). Multiple README sections use "Banza" to mean "Banzami" (ADR-016 residue).

| Question | What the visitor concludes | Correct? |
|----------|---------------------------|----------|
| What is BANZA? | A financial infrastructure layer (inferred from "built on Banza infrastructure") | YES (partially) |
| What is BanzAI? | Not clearly described in this repo | NOT COMMUNICATED |
| What is Banzami? | Angola's instant payment network, QR-native, built on Banza | YES |
| Relationship between the three? | Banzami uses Banza. BanzAI unclear. | PARTIAL |
| Who controls the protocol? | Implied to be Banzami ("official Banzami SDKs") | MISLEADING |
| Does the protocol belong to a company? | Unclear — "Banza is building the digital payment layer" confuses the layers | CONFUSED |
| What survives if an operator disappears? | Not addressed | NOT COMMUNICATED |

**Comprehension verdict:** PARTIAL FAIL — The repo correctly identifies itself as an operator built on Banza, but residual ADR-016 language uses "Banza" to mean "Banzami" in multiple places. The repo description is factually incorrect.

---

## Phase 7 — Strategic Positioning Assessment

### Required positioning (per ADR-025)

| Statement | Correct on GitHub? |
|-----------|-------------------|
| BANZA is not a product. | PARTIAL — banza README is correct; org profile says otherwise |
| BANZA is not a company. | FAIL — GOVERNANCE.md says "governed by Banzami" |
| BANZA is not a wallet. | PASS — no wallet framing in banza repo |
| BANZA is not an application. | PASS — no app framing |
| BANZA is an open layer of rules, certification, interoperability, and settlement. | PASS — banza repo README communicates this |
| BanzAI is the Protocol OS that accelerates protocol adoption. | PARTIAL — banzai README is correct; repo description says "Banzami ecosystem" |
| Banzami is only one operator within the ecosystem. | PARTIAL — banza README says this explicitly; GOVERNANCE.md contradicts it |
| The protocol can survive the disappearance of any operator. | NOT COMMUNICATED — no statement of protocol survivability anywhere |

---

## Most Critical Positioning Gaps

### Gap 1 — Org profile is the wrong mental model entry point

`github.com/banza-protocol` is the canonical entry point for the protocol. The profile README must communicate the ADR-025 model immediately. Currently it does the opposite: a visitor forms the belief that "Banzami is the protocol" before encountering any repository.

**Impact:** Every subsequent page the visitor reads will be interpreted through a false mental model. Corrections in individual READMEs are insufficient if the org profile establishes the wrong frame.

### Gap 2 — GOVERNANCE.md undermines the README's correct framing

The banza README correctly positions Banzami as "one operator among many." GOVERNANCE.md then says "Banza is governed by Banzami (the organization)." This is not a minor inconsistency — governance attribution determines who controls the protocol rules. A developer, regulator, or potential operator reading GOVERNANCE.md will conclude that the protocol is controlled by its largest (and only current) commercial operator.

**Impact:** This actively undermines the "open protocol" positioning and suggests operator capture, which is the exact failure mode ADR-025 was designed to prevent.

### Gap 3 — Protocol survivability is never stated

None of the four repositories state explicitly: *"The Banza protocol continues to exist independently of any operator."* This is the most important political and technical claim the protocol must make, and it is absent from all surfaces audited.

**Impact:** A new potential operator, investor, or regulator cannot determine whether the protocol is genuinely independent or whether it ceases to exist if Banzami (the company) disappears.

### Gap 4 — BanzAI is associated with Banzami, not Banza

The banzai repo description says "Banzami ecosystem." The BanzAI README itself is correct ("Protocol OS for the Banza ecosystem"), but the repository metadata — the first thing visible on the repo page — says the opposite.

**Impact:** Developers visiting the BanzAI repo are told immediately that BanzAI belongs to the Banzami product, not the Banza protocol. This is the same identity inversion at a smaller scale.

---

*Report complete: 2026-05-30. No files modified.*
