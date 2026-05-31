# BANZA_REFERENCE.md — Website Information Architecture

**Document ID:** BANZA-REFERENCE-WEBSITE-MAPPING-001  
**Date:** 2026-06-01  
**Authority:** BANZA-REFERENCE-CONSOLIDATION-001

---

## Target Website Structure

`banza.network` will be the public face of the BANZA Protocol. The following 12 sections form the site's primary information architecture. Every section of BANZA_REFERENCE.md maps to exactly one website destination.

---

## Website Section Map

### Section 1 — What is BANZA

**Website URL:** `banza.network/about`  
**Audience:** Everyone (executives, developers, regulators, general public)  
**Purpose:** First contact. Answer the question: "What is this?"

**Source material from BANZA_REFERENCE.md:**
- §3 "O que é o BANZA" — four properties (public rules, open certification, verifiable invariants, federation)
- §3 architecture diagram (three levels: BANZA / BanzAI / Operators)
- §12 vision statement

**Missing / needs creation:**
- One-paragraph executive summary (MISSING — must be written)
- Protocol metrics (79/79 tests, 14/14 scenarios, M1 complete — MISSING)
- Clear "BANZA is not a bank / not a product / not an API" table

**Page design notes:**
- Hero statement: single sentence. "BANZA is Angola's open payment protocol — the infrastructure beneath any operator."
- Three-panel illustration: BANZA protocol → BanzAI OS → Certified Operators
- "As used in: Pix (Brazil), UPI (India), BANZA (Angola)" analogy strip

---

### Section 2 — Why BANZA Exists

**Website URL:** `banza.network/why`  
**Audience:** Executives, regulators, investors, partners  
**Purpose:** Make the case for why an open protocol exists at all.

**Source material from BANZA_REFERENCE.md:**
- §1 "O Problema" — Angola's payment landscape (banks, EMIS, 16M phones)
- §2 "A Camada que Falta" — M-Pesa vs Pix/UPI model
- §2.4 "O que acontece se um operador desaparecer?" — the disappearing operator test

**Missing / needs creation:**
- English translation (entire section is Portuguese)
- Quantitative framing (market size, addressable opportunity — not yet in reference)
- Call to action for operators interested in joining

**Page design notes:**
- "Before BANZA" vs "After BANZA" visual comparison
- M-Pesa / Pix / UPI comparative table (already exists in §2 — translate)
- The disappearing operator test as a highlighted callout

---

### Section 3 — Core Principles

**Website URL:** `banza.network/principles`  
**Audience:** Technical evaluators, operators, developers  
**Purpose:** Define BANZA's non-negotiable architectural values.

**Source material from BANZA_REFERENCE.md:**
- §3 four protocol properties (wallet-native, QR-native, programmable, instant settlement)
- §4 five principles (financial correctness, protocol is the product, kernel vs operators, traceability, open access)

**Missing / needs creation:**
- English translation
- "Open access" principle needs prominence (any entity that passes conformance becomes certified — no bilateral agreement)
- "Angola-first" framing as founding context, not restriction

**Page design notes:**
- Card layout: one card per principle, icon + one-sentence definition + one-line "what this means in practice"

---

### Section 4 — Certification

**Website URL:** `banza.network/certification`  
**Audience:** Operators seeking certification, developers building on the protocol  
**Purpose:** Answer: "How do I become certified? What does each level mean?"

**Source material from BANZA_REFERENCE.md:**
- §9 certification levels (L0–L4) — NEEDS CORRECTION (DEF-004/005/006)
- §9 open access principle
- §9 certification maintenance

**Missing / needs creation:**
- Updated L3 requirements (certificate, BRL check, `supports_federation`, 90-day lifetime)
- Corrected L4 definition (card acquiring, NOT "federation_ready")
- Six-step certification process (currently only partial)
- Corrected operator manifest JSON example
- BanzAI role in certification (guidance, not authority)

**Companion file:** `BANZA_CERTIFICATION.md` (authoritative)

**Page design notes:**
- Level cards: L0 through L4, each with capabilities checklist
- Certification timeline graphic (submit → review → certified in 5 business days)
- "Certification is earned, not bought" callout

---

### Section 5 — Federation

**Website URL:** `banza.network/federation`  
**Audience:** Operators (L3+), developers, executives, regulators  
**Purpose:** Explain how the payment network works when multiple operators exist.

**Source material from BANZA_REFERENCE.md:**
- §10 entire federation section — EXCELLENT CONTENT (translate + fix DEF-007/008)
- Before/after diagrams
- Ana/Bento example
- Obligations lifecycle
- Netting/compensation example
- Network effects (Metcalfe's law paragraph)

**Missing / needs creation:**
- English translation throughout
- Replace stale implementation table with: "Federation specification complete. 79/79 conformance tests pass. 14/14 interoperability scenarios pass. M1 Protocol Complete achieved 2026-06-01."
- Fix BanzAI role description (DEF-007)

**Page design notes:**
- Animated flow: Client A → Operator A → BANZA protocol → Operator B → Merchant B
- Before/after network diagram (two isolated islands → connected network)
- Numbers: 79 tests, 14 scenarios, 5 steps

---

### Section 6 — Trust

**Website URL:** `banza.network/trust`  
**Audience:** Technical operators (L3+), security auditors, regulators  
**Purpose:** Explain the cryptographic trust infrastructure behind federation.

**Source material from BANZA_REFERENCE.md:**
- §10 trust chain diagram (lines 744–764) — GOOD, translate and expand
- §10 BRL explanation (lines 557–561) — GOOD, translate

**Missing — entire section must be created from:**
- ADR-029 — Production Root Architecture
- `docs/security/ROOT_KEY_CEREMONY_PROCEDURE.md` (plain-language summary)
- `docs/operations/ROOT_CEREMONY_EXECUTION_PLAN.md`
- INV-ROOT-001 through INV-ROOT-006 (in plain language)

**Content required:**
- The trust hierarchy: root key → Key Manifest → issuing keys → certificates
- Key Manifest: what it is, where it lives (`banza.network/.well-known/banza/key-manifest.json`)
- BRL: what it is, how it works (`banza.network/federation/revocation-list.json`)
- Certificate chain verification (no BANZA server needed in real time)
- Root key ceremony (brief explanation — "generated offline, air-gapped machine, independent witness")
- Production status: "Root key ceremony scheduled. M2 Production Trust is the active milestone."

**Page design notes:**
- Trust chain diagram: Root Key → Key Manifest → Cert-Issuing Key → Operator Certificate → Verified by peer
- "No real-time server call required" as a featured property

---

### Section 7 — BanzAI

**Website URL:** `banza.network/banzai`  
**Audience:** Operators using BanzAI, developers building with BanzAI  
**Purpose:** Explain what BanzAI is, what it does, and what it never does.

**Source material from BANZA_REFERENCE.md:**
- §10 "O Papel do BanzAI na Federação" — good content, translate and expand
- §10 "Modelo de Autoridade" diagram — excellent, translate
- §9 BanzAI and certification paragraph — good, translate

**Missing — expand from:**
- BanzAI's 6 capability categories (from `MATRIX_B_BANZAI.md`)
- `apps/banzai/` tool descriptions

**Non-negotiable content:**
- "BanzAI does not certify. BANZA certifies." — must be prominent
- "BanzAI does not hold production private keys."
- "BanzAI evaluates readiness; the conformance suite determines certification."

**Page design notes:**
- Two-column layout: "BanzAI does" vs "BanzAI does not"
- Authority model diagram (BANZA → BanzAI → Operators)

---

### Section 8 — Operators

**Website URL:** `banza.network/operators`  
**Audience:** Companies considering becoming BANZA operators  
**Purpose:** Answer: "What does it mean to be a certified operator? How do I join?"

**Source material from BANZA_REFERENCE.md:**
- §5 "Operadores" paragraph (lines 249–260)
- §9 "Princípio de acesso aberto" (any entity that passes conformance)
- §10 network effects paragraph (Metcalfe's law)

**Missing — create from:**
- `docs/federation/FEDERATION_OPERATOR_QUICKSTART.md`
- `BANZA_CERTIFICATION.md` (certification process)
- Operator manifest schema

**Content required:**
- "What is a BANZA operator?" (one paragraph)
- "What does an operator need to implement?" (by level)
- Network effect: each operator that joins makes all others more valuable
- "How to become an operator" (6 steps from BANZA_CERTIFICATION.md)
- Operator manifest structure

**Page design notes:**
- Network diagram showing how joining operator A adds value to operators B, C, D
- CTA: "Start your certification journey" → links to conformance suite

---

### Section 9 — Developer Resources

**Website URL:** `banza.network/developers`  
**Audience:** Developers building on BANZA or implementing an operator  
**Purpose:** Technical hub — contracts, SDKs, conformance runner, financial spec.

**Source material from BANZA_REFERENCE.md:**
- §5 kernel crate table (lines 230–247)
- §5 tech stack table (lines 261–268)
- §6 monetary representation (entire section — translate, keep normative)
- §7 financial invariants (entire section — translate, expand)

**Missing — create from:**
- `sdk/` (TypeScript, Python, Go, PHP, Flutter, Checkout Web)
- `contracts/` (OpenAPI, federation, webhooks, QR)
- `tools/banza-conformance/` (how to run the suite)
- `conformance/vectors/` (test vectors reference)

**Content required:**
- SDK table (language, package name, version)
- Contracts surface (OpenAPI, webhooks, QR spec, federation schemas)
- Conformance runner usage (bash command)
- Kernel architecture (crate table)
- Normative monetary representation (from §6)
- Full invariant taxonomy (from §7 + add INV-TRUST-*/INV-ROOT-*)

**Page design notes:**
- SDK language tab selector (TypeScript / Python / Go / PHP / Flutter)
- "Copy" button for conformance runner command
- Invariant table with expandable rows

---

### Section 10 — Governance

**Website URL:** `banza.network/governance`  
**Audience:** Contributors, operators, regulators  
**Purpose:** Explain how BANZA evolves, who governs it, and how decisions are made.

**Source material from BANZA_REFERENCE.md:**
- §8 RFC/ADR governance (lines 404–422) — translate, remove legacy content
- §3 "A distinção fundamental" (protocol ≠ operator)
- §3 "O que acontece se um operador desaparecer?"

**Missing — create from:**
- `BANZA_GOVERNANCE.md` (governance doc)
- `docs/rfc/README.md` (RFC process)
- ADR process

**Content required:**
- RFC process (when required, how to submit)
- ADR process (what it records, what it governs)
- "No single operator governs BANZA"
- BANZA → BanzAI → Operators dependency graph
- Protocol Development Closure status (M5)

**Page design notes:**
- Governance flow: Community RFC → Review → Accepted ADR → Conformance test → Certification
- "Open governance" compared to "operator-controlled" model

---

### Section 11 — Roadmap

**Website URL:** `banza.network/roadmap`  
**Audience:** Investors, operators planning implementation, community  
**Purpose:** Show where BANZA is and where it is going.

**Source material from BANZA_REFERENCE.md:**
- §11 — REMOVE ENTIRELY (completely stale, all items achieved)

**Missing — replace with:**
- M1 Protocol Complete (ACHIEVED 2026-06-01)
- M2 Production Trust (ACTIVE — root key ceremony scheduled)
- M3 First Operator Certified (planned post-M2)
- M4 BanzAI Operational
- M5 Validation Studio Complete
- M6 BANZA v1.0 Public Launch
- v1.1 (L4, DNS discovery, ADR-030/031)
- v2.0 (cross-border, multi-sig root)

Source: `docs/governance/BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md`

**Page design notes:**
- Horizontal timeline: M1 (done) → M2 (active) → M3 → M4/M5 (parallel) → M6 → v1.1 → v2.0
- Completed milestones shown differently from active/future

---

### Section 12 — FAQ

**Website URL:** `banza.network/faq`  
**Audience:** Everyone  
**Purpose:** Short answers to the most common questions.

**Source material from BANZA_REFERENCE.md:**
- §3 "O que o BANZA não é" table
- §2 "O que acontece se um operador desaparecer?"
- §9 "Princípio de acesso aberto"

**Missing — create entirely:**
- "Is BANZA a bank?" → No.
- "Is BANZA only for Angola?" → BANZA was designed for Angola. The protocol is open.
- "Can any company become an operator?" → Yes, if they pass the conformance suite.
- "What happens if an operator goes out of business?" → Federation continues; protocol is independent.
- "What is the difference between BANZA and BanzAI?" → BANZA is the protocol. BanzAI is the Protocol OS.
- "Does BanzAI certify operators?" → No. BANZA certifies. BanzAI guides.
- "How long does certification take?" → Review within 5 business days.
- "What is the BRL?" → BANZA Revocation List — public list of revoked operator certificates.
- "How do I verify an operator's certificate without calling BANZA?" → Key Manifest + certificate chain.

**Page design notes:**
- Accordion FAQ layout
- Searchable

---

## Coverage Matrix

| Website Section | BANZA_REFERENCE.md source | Completeness | Action |
|-----------------|--------------------------|:------------:|--------|
| What is BANZA | §3, §12 | 60% | Translate + complete |
| Why BANZA Exists | §1, §2 | 70% | Translate |
| Core Principles | §3, §4 | 80% | Translate + update |
| Certification | §9 | 40% | Translate + major corrections |
| Federation | §10 | 70% | Translate + fix 2 defects |
| Trust | §10 (partial) | 20% | Translate + major new section |
| BanzAI | §9, §10 | 40% | Translate + expand |
| Operators | §5, §9 | 30% | Translate + create |
| Developer Resources | §5, §6, §7 | 50% | Translate + SDK/contracts |
| Governance | §8 | 60% | Translate + remove legacy |
| Roadmap | §11 | 0% | Remove + replace entirely |
| FAQ | none | 0% | Create from scratch |

---

## Readiness Scores (Current vs After Restructure)

| Audience | Current (10-point scale) | After Restructure |
|----------|:------------------------:|:-----------------:|
| **Executive** | 3 (Portuguese, stale roadmap) | 9 |
| **Developer** | 4 (Portuguese, missing trust/SDK) | 8 |
| **Operator** | 3 (Portuguese, wrong L3/L4 reqs) | 8 |
| **Regulatory** | 4 (Portuguese, missing trust arch) | 9 |
| **Website** | 2 (Portuguese, stale, missing 5 sections) | 8 |

---

## Visual Asset Candidates for banza.network

The following visuals should be designed for the website based on content in the reference document:

| Asset | Source | Priority |
|-------|--------|----------|
| Three-tier architecture diagram (BANZA / BanzAI / Operators) | §3 | CRITICAL |
| Before/after federation network diagram | §10 | CRITICAL |
| Authority model hierarchy (BANZA → BanzAI → Operators) | §10 | CRITICAL |
| Trust chain diagram (Root → Key Manifest → Issuing → Certificate) | ADR-029 | HIGH |
| Certification level progression (L0 → L1 → L2 → L3 → L4) | §9 | HIGH |
| M-Pesa vs Pix/UPI vs BANZA comparison table | §2 | HIGH |
| Federation payment flow (Ana → Operator A → BANZA → Operator B → Bento) | §10 | HIGH |
| Netting/compensation example | §10 | MEDIUM |
| Roadmap timeline | §11 replacement | HIGH |
| Obligation lifecycle state machine | §10 | MEDIUM |
