# BANZA_REFERENCE.md — Restructure Plan

**Document ID:** BANZA-REFERENCE-RESTRUCTURE-PLAN-001  
**Date:** 2026-06-01  
**Authority:** BANZA-REFERENCE-CONSOLIDATION-001  
**Phases:** 11, 12, 14

---

## Phase 11 — Target Document Structure

The restructured `BANZA_REFERENCE.md` will have 12 sections mapping directly to the `banza.network` website structure. Each section must stand alone for its intended audience.

---

### Section 1 — Introduction

**Why it belongs:** First contact for every reader — executive, developer, operator, regulator. Must be self-contained in five sentences.

**Contents:**
- What BANZA is (one-sentence definition)
- The four protocol properties (public rules, open certification, verifiable invariants, federation)
- Ecosystem hierarchy (BANZA / BanzAI / Operators)
- What this document covers

**Source:** §3 current document (translate + compress)  
**Length target:** 300 words  
**Audience:** Universal

---

### Section 2 — Why BANZA Exists

**Why it belongs:** The problem statement and open-protocol argument must come early. Without it, readers ask "why does this need to exist?"

**Contents:**
- Angola's payment landscape (banks, EMIS, 16M mobile users, the fragmentation problem)
- What is missing: the protocol layer
- Two models: closed (M-Pesa) vs open (Pix, UPI)
- The structural comparison table (who defines rules / who can participate / third-party operator possible?)
- The disappearing operator test: protocol survives operators

**Source:** §1 + §2 current document (translate)  
**Length target:** 500 words  
**Audience:** Executives, investors, regulators, partners

---

### Section 3 — Core Principles

**Why it belongs:** Before explaining certification, federation, or trust, readers must understand the non-negotiable values driving every design decision.

**Contents:**
- Financial correctness is non-negotiable
- The protocol is the product (operators prove it works; they don't own it)
- Kernel implements the protocol; operators implement policy
- Traceability by default (every payment has a `trace_id`)
- Open access (conformance suite = certification, no institutional access required)
- Protocol independence (protocol survives any single operator)

**Source:** §3 + §4 current document (translate + update)  
**Length target:** 300 words  
**Audience:** Technical evaluators, operators, developers

---

### Section 4 — Certification

**Why it belongs:** Certification is the gateway to the network. Every operator must understand this before doing anything else.

**Contents:**
- Why certification exists (open rules require open verification)
- Certification levels L0–L4 (corrected per ADR-028)
- Open access principle
- The six-step certification process
- Certification maintenance (12-month expiry, automated spot-checks)
- BanzAI's role: guidance, not certification

**Source:** §9 current document (translate + correct DEF-004/005/006 + add ADR-028 requirements)  
**Length target:** 500 words  
**Audience:** Operators, developers

**Critical corrections required:**
- L3 must include: BANZA-signed certificate at `/.well-known/banza/certificate.json`, 90-day lifetime, BRL check, `supports_federation: true`, `POST /federation/route` endpoint
- L4 must be corrected: remove `federation_ready` (already L3), L4 = card acquiring only
- Operator manifest JSON must use correct field names (`protocol_version`, not `version`)

---

### Section 5 — Federation

**Why it belongs:** Federation is BANZA's most differentiated capability. It is the mechanism that makes a multi-operator network possible. It requires its own complete section.

**Contents:**
- Why federation exists (without it, each operator is an island)
- Before/after diagrams
- How federation works: five steps (trust, routing, acceptance+execution, obligation, settlement)
- Step-by-step example (Ana → Operator A → BANZA protocol → Operator B → Bento)
- Obligation lifecycle (`pending → in-compensation → settled`)
- Compensation/netting (1 bank transfer per cycle, not 1 per payment)
- Why federation matters (4 perspectives: merchants, clients, operators, regulators)
- Current status: specification complete, 79/79 conformance tests pass, 14/14 interoperability scenarios pass

**Source:** §10 current document (translate + fix DEF-007/008)  
**Length target:** 800 words  
**Audience:** Operators, developers, executives, regulators

**Critical correction required:**
- Remove "✓ Executa o conformance suite (79 testes de federação)" from BanzAI role — BanzAI runs guidance simulation; `tools/banza-conformance/run_fed.py` is the authoritative runner
- Replace stale implementation table with accurate current status

---

### Section 6 — Trust

**Why it belongs:** Federation trust requires understanding the cryptographic infrastructure underneath. This section is a prerequisite for L3+ operators. It must be explained in plain language — not requiring cryptography knowledge.

**Contents:**
- Why trust infrastructure exists (operators need to verify each other without calling BANZA in real time)
- The trust hierarchy: Root Key → Key Manifest → Issuing Keys → Operator Certificates
- The Root Key: offline, ed25519, 24-month validity, used only to sign Key Manifests
- The Key Manifest: what it is, where it lives (`banza.network/.well-known/banza/key-manifest.json`), how SDKs pin it
- Three issuing keys: cert-issuing (signs certificates), brl-issuing (signs BRL), evidence-issuing (signs conformance evidence)
- Operator certificates: what they contain, where operators serve them (`/.well-known/banza/certificate.json`), 90-day lifetime
- The BRL (BANZA Revocation List): what it is, where it lives (`banza.network/federation/revocation-list.json`), updated every 6 hours
- Certificate verification: no BANZA server call needed in real time
- Root key ceremony: what it is, why it matters, that it is scheduled
- Production status: ceremony scheduled, M2 Production Trust is the active milestone

**Source:** ADR-029, `docs/security/`, `docs/operations/ROOT_CEREMONY_*`  
**Length target:** 500 words  
**Audience:** Technical operators (L3+), security auditors, regulators  
**ENTIRELY NEW — not present in current document**

---

### Section 7 — BanzAI

**Why it belongs:** BanzAI appears throughout the document but has no dedicated section. The boundary between BANZA (authority) and BanzAI (evaluation) must be explicitly stated once, clearly.

**Contents:**
- What BanzAI is: the Protocol Operating System
- Six capability categories (Knowledge Engine, Evaluation, Certification Support, Federation Intelligence, Governance Intelligence, Operational Intelligence)
- What BanzAI does not do (certify, issue, sign, hold production keys)
- BanzAI in the ecosystem (evaluates against BANZA rules; BANZA applies them)
- The authority model diagram (BANZA → BanzAI → Operators)

**Source:** §9 + §10 current document (translate + expand) + `MATRIX_B_BANZAI.md`  
**Length target:** 400 words  
**Audience:** Operators using BanzAI, developers, executives

---

### Section 8 — Operators

**Why it belongs:** A future operator needs a single section that answers all their entry questions without reading certification docs and quickstart guides separately.

**Contents:**
- What an operator is (any entity that implements the protocol to process payments)
- What operators must implement (by level, brief summary)
- How to become an operator (six steps: manifest → implement → run suite → submit → review → certified)
- What happens after certification (API keys, registry listing, federation eligibility at L3)
- Network effects (each operator increases the value of all others)
- Operator independence (no operator governs another; authority rests in the protocol)

**Source:** §5 current document + `BANZA_CERTIFICATION.md` + `FEDERATION_OPERATOR_QUICKSTART.md`  
**Length target:** 400 words  
**Audience:** Organizations considering becoming BANZA operators

---

### Section 9 — Developer Resources

**Why it belongs:** Developers need a single place to find contracts, SDKs, conformance runner, and normative specs. This section serves as the technical gateway.

**Contents:**
- SDK table (TypeScript, Python, Go, PHP, Flutter, Checkout Web — package name, version, status)
- Contracts surface (OpenAPI 4 files, federation 5 schemas, webhooks 2, QR 2, SDK certification)
- Conformance runner usage (bash command: `python3 tools/banza-conformance/run.py --level N`)
- Kernel architecture (crate table — 13 crates with responsibilities)
- Normative: monetary representation (full §6 content translated)
- Financial invariants reference (full §7 content translated + INV-TRUST-* and INV-ROOT-* families added)
- Tech stack (Rust, Go, PostgreSQL, Redis, OpenTelemetry)

**Source:** §5, §6, §7 current document (translate) + `sdk/`, `contracts/`, `tools/`  
**Length target:** 600 words  
**Audience:** Developers

---

### Section 10 — Governance

**Why it belongs:** Governance is the proof that BANZA is genuinely open. It must explain how decisions are made and who can participate.

**Contents:**
- RFC process (when required, what it governs, how to submit)
- ADR process (what ADRs record, immutability)
- No single operator governs BANZA (operator independence principle)
- BANZA → BanzAI → Operators dependency graph (permanent, non-negotiable direction)
- Protocol development status (Protocol frozen at M1; operations now active)

**Source:** §8 current document (translate + remove DEF-002/003)  
**Length target:** 300 words  
**Audience:** Contributors, operators, regulators

---

### Section 11 — Roadmap

**Why it belongs:** Shows investors, operators, and the community where the protocol is and where it is going.

**Contents:**
- M1 Protocol Complete — ACHIEVED 2026-06-01 (79/79 tests, 14/14 scenarios, ADR-026/028/029 accepted)
- M2 Production Trust — ACTIVE (root key ceremony scheduled; Key Manifest + BRL endpoints pending)
- M3 First Operator Certified — Blocked by M2
- M4 BanzAI Operational — Independent, parallel
- M5 Validation Studio Separation — Partially complete (three matrices established)
- M6 BANZA v1.0 Public Launch — Blocked by M2 + M3 + M5
- v1.1 Future: L4 conformance suite, ADR-030/031/032, DNS discovery
- v2.0 Future: Cross-border (AOA ↔ other currencies), multi-signature root

**Source:** `docs/governance/BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md` (§11 current document REMOVED)  
**Length target:** 300 words  
**Audience:** Investors, operators, community

---

### Section 12 — FAQ

**Why it belongs:** Common questions must be answered in plain language to reduce barrier to entry for all audiences.

**Contents (14 FAQs):**
1. Is BANZA a bank? → No.
2. Is BANZA only for Angola? → Designed for Angola; protocol is open.
3. Can any company become an operator? → Yes, if they pass the conformance suite.
4. What happens if an operator goes out of business? → The protocol continues; other operators continue.
5. What is the difference between BANZA and BanzAI? → Protocol vs Protocol OS.
6. Does BanzAI certify operators? → No. BANZA certifies. BanzAI guides.
7. How long does certification take? → Review within 5 business days.
8. What is the BRL? → BANZA Revocation List — public list of revoked certificates.
9. How does an operator verify another's certificate without calling BANZA? → Key Manifest + certificate chain.
10. What is federation? → Two-sentence answer.
11. Is certification free? → The conformance suite is open source.
12. What level should a new operator target first? → L0 or L1.
13. Does an L3 operator need a special agreement with BANZA to federate? → No — certification is sufficient.
14. What is the root key ceremony? → One paragraph.

**Source:** Created from existing content across all sections  
**Length target:** 400 words  
**Audience:** Universal  
**ENTIRELY NEW — not present in current document**

---

## Phase 12 — Website Readiness Scores

### Before Restructure

| Dimension | Score (0–10) | Justification |
|-----------|:------------:|---------------|
| Executive Readiness | 3 | Entire doc in Portuguese; stale roadmap; missing trust section |
| Developer Readiness | 4 | Technical content exists but Portuguese; missing trust, SDK, contracts |
| Operator Readiness | 3 | Certification table exists but wrong; Portuguese; no practical steps |
| Regulatory Readiness | 4 | Auditability explained; Portuguese; missing trust architecture |
| Website Readiness | 2 | Portuguese throughout; 5 sections missing; stale roadmap; 10 defects |
| **Overall** | **3.2** | |

### After Restructure

| Dimension | Score (0–10) | Justification |
|-----------|:------------:|---------------|
| Executive Readiness | 9 | English; clear narrative; vision, problem, solution all present; trust explained |
| Developer Readiness | 8 | Contracts, SDKs, conformance runner, invariants, kernel all covered |
| Operator Readiness | 8 | Correct L3/L4 requirements; full certification path; practical steps |
| Regulatory Readiness | 9 | Trust architecture, auditability, invariants, BRL all explained |
| Website Readiness | 8 | 12 sections map to 12 website pages; visual asset candidates identified |
| **Overall** | **8.4** | |

**Gap to 10/10:** Developer Readiness -2 (full contract schema docs and live API examples remain in `contracts/` — reference doc points there). Operator Readiness -2 (production endpoints not yet live, quickstart incomplete until M2). Website Readiness -2 (visuals not yet designed; FAQ not battle-tested).

---

## Phase 14 — Final Verdict

### Can BANZA_REFERENCE.md become the canonical source for the future banza.network website?

**YES — after the restructure defined in this plan is executed.**

The document cannot serve as website source in its current form. After the restructure, it is the canonical source.

### Remaining work before website production

All items below are required for `banza.network` go-live. None blocks the restructure itself.

| Priority | Item | Unblocked? |
|----------|------|-----------|
| **CRITICAL** | Execute root key ceremony → M2 Production Trust (Key Manifest + BRL live) | OPS-001 scheduled |
| **CRITICAL** | SDK v1.0 release with Key Manifest pinned | After M2 |
| **HIGH** | Trust section must include live endpoint URLs (post-M2) | After M2 |
| **HIGH** | Operator quickstart must include live endpoints | After M2 |
| **HIGH** | Roadmap section must link to live M2/M3 status | After M2 |
| **MEDIUM** | FAQ #9 "verify without BANZA" needs live Key Manifest URL | After M2 |
| **MEDIUM** | Visual asset production (14 diagrams) | Immediately |
| **MEDIUM** | GOV-001/002/003 RFC status updates | Today |
| **MEDIUM** | DOC-003 BANZA_CERTIFICATION.md L4 caveat | Today |
| **LOW** | Operator registry URL | After M3 |
| **LOW** | Certification portal URL | After M6 (FUTURE-009) |
| **LOW** | Portuguese translation of restructured document | Post-launch |

### What the restructure resolves immediately

- All 10 defects from the audit (DEF-001 through DEF-010)
- Complete English translation
- All five missing sections (Trust, BanzAI standalone, Operators, Developer Resources, FAQ)
- Correct L3/L4 certification requirements
- Correct BanzAI role (no false conformance suite claim)
- Accurate roadmap (M1–M6 + v1.1/v2.0)
- Removed legacy validation domains and wrong matrix reference
- Updated ADR references (ADR-026, ADR-028, ADR-029)

### Restructure execution

The restructured `BANZA_REFERENCE.md` is created as part of task BANZA-REFERENCE-CONSOLIDATION-001. This plan document (`BANZA_REFERENCE_RESTRUCTURE_PLAN.md`) serves as the specification that the restructured document must satisfy.
