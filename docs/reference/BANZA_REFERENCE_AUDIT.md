# BANZA_REFERENCE.md — Complete Audit

**Document ID:** BANZA-REFERENCE-AUDIT-001  
**Date:** 2026-06-01  
**Authority:** BANZA-REFERENCE-CONSOLIDATION-001  
**Audited file:** `BANZA_REFERENCE.md` (v1.0, 2026-05-30, 872 lines)

---

## Summary

The current `BANZA_REFERENCE.md` is written entirely in Portuguese, predates ADR-026/028/029, contains a completely stale roadmap, and is missing four planned website sections. The narrative quality is high and worth preserving — particularly the Pix/UPI analogy, the federation explanation, and the Ana/Bento example. Everything needs translation and significant factual updates.

**Overall verdict:** REWRITE REQUIRED — content is salvageable but language, structure, and accuracy all need correction.

---

## Section-by-Section Inventory

### §1 — O Problema: Angola Tem as Peças (Lines 53–83)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese |
| Content quality | HIGH — vivid problem description (banks, EMIS, 16M phones, WhatsApp receipts) |
| Factual accuracy | GOOD |
| Pre-ADR-026/028/029? | Partly (predates trust model, but no trust content here) |
| Operator-specific contamination | NONE |
| Action | **REWRITE** — translate to English, preserve narrative |

**Issues:**
- Entirely Portuguese
- Minor: references "dezasseis milhões de pessoas" (16M) — may need updating

---

### §2 — A Camada que Falta (Lines 86–128)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese |
| Content quality | EXCELLENT — M-Pesa vs Pix/UPI model is compelling |
| Factual accuracy | GOOD |
| Operator-specific contamination | MINOR — "o operador é o primeiro operador certificado" in §2.4 |
| Action | **REWRITE** — translate to English, neutral operator reference |

**Issues:**
- Entirely Portuguese
- §2.4 "O operador" paragraph references operator survival test — good content, minor phrasing fix needed

---

### §3 — O que é o BANZA (Lines 130–199)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese |
| Content quality | HIGH — four properties, architecture diagram, what BANZA is not table |
| Factual accuracy | PARTIAL — architecture diagram still lists "the reference operator" as named entity |
| Operator-specific contamination | LOW — "the reference operator" in architecture diagram is generic label |
| Pre-ADR-026/028/029? | Partial — ADR-025 referenced, but trust/certification updates missing |
| Action | **REWRITE** — translate, update architecture diagram |

**Issues:**
- Architecture diagram (lines 136–154) has three-level structure — content is correct but uses "the reference operator" label
- "O que o BANZA não é" table says "O operador é um operador" — correct but slightly confusing phrasing
- §3 name origin paragraph (lines 196–198) mentions "the reference operator" by implication — keep the concept, remove the product reference

---

### §4 — Princípios Fundamentais (Lines 201–223)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese |
| Content quality | GOOD — five principles |
| Factual accuracy | PARTIAL |
| Pre-ADR-026/028/029? | Partly |
| Action | **REWRITE** — translate, update two principles |

**Issues:**
- "O protocolo é o produto": §4 says "O operador (o produto de consumo) é a implementação de referência do protocolo BANZA. O protocolo é o que escala." — conflates operator product with protocol. Should read: "The protocol is the product. Operators prove it works."
- "Angola primeiro" — appropriate founding context but should be framed as context, not an invariant of the protocol
- "Wallet-native", "QR-native", "Programmable", "Instant settlement" appear in §3, not §4 — redundancy

---

### §5 — Arquitectura do Ecossistema (Lines 225–269)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese |
| Content quality | GOOD — kernel crate table, tech stack table |
| Factual accuracy | PARTIAL |
| Pre-ADR-026/028/029? | Yes (no ADR-026 routing crate, no trust crate) |
| Action | **REWRITE** — translate, fix circular reference, add missing crates |

**Issues:**
- **CIRCULAR REFERENCE (DEFECT):** Line 255: `Ver [BANZA_REFERENCE.md](../banza/BANZA_REFERENCE.md)` — this is the document itself. Should reference the reference operator repo or remove entirely.
- Kernel crate table (lines 230–247) does not include new crates added for federation/trust
- "Operadores Certificados" paragraph (lines 257–260) is fine
- Tech stack table is valid — Rust, Go, PostgreSQL, Redis, OpenTelemetry

---

### §6 — Representação Monetária (Lines 271–346)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese (with English JSON examples) |
| Content quality | EXCELLENT — normative monetary rules are critical and well-defined |
| Factual accuracy | HIGH |
| Pre-ADR-026/028/029? | No impact — monetary rules are pre-ADR invariants |
| Action | **REWRITE (minor)** — translate headers, keep JSON examples |

**Issues:**
- Entirely Portuguese
- Content is correct and complete — MON-001 definition, `*_minor` convention, settlement invariant
- Currency table (AOA, USD, EUR) is correct

---

### §7 — Invariantes Financeiros (Lines 348–400)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese (with English invariant IDs) |
| Content quality | GOOD — critical invariants defined |
| Factual accuracy | PARTIAL |
| Pre-ADR-026/028/029? | YES — missing INV-TRUST-*, INV-ROOT-* families |
| Action | **REWRITE + EXPAND** — translate, add ADR-026/029 invariant families |

**Issues:**
- Invariant family table (lines 354–361) is missing: `INV-TRUST-*`, `INV-FED-*`, `INV-ROOT-*`, `INV-RECON-*`
- Critical invariants table (lines 363–374) is missing trust/federation invariants
- BanzAI "Trace Explainer" reference (line 398) — move to BanzAI section, not here
- Content is otherwise accurate

---

### §8 — Governança do Protocolo (Lines 402–439)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese |
| Content quality | PARTIAL |
| Factual accuracy | PARTIAL |
| Pre-ADR-026/028/029? | Yes |
| Action | **REWRITE + REMOVE two subsections** |

**Issues:**
1. **WRONG REFERENCE (DEFECT):** "Validation Matrix" subsection (lines 423–426) says "`docs/validation/BANZA_IMPLEMENTATION_MATRIX.json` é a fonte de verdade para o progresso de implementação do operador de referência." This file lives in the reference operator repo, not this repo. The BANZA validation architecture now lives in `docs/validation/MATRIX_A_BANZA.md` and companions. **REMOVE this subsection.**
2. **LEGACY CONTENT (DEFECT):** "Domínios de Validação" table (lines 428–438) — DOM-FIN, DOM-IDENTITY, DOM-CONSUMER, DOM-MERCHANT, DOM-DEVELOPER, DOM-INFRA, DOM-SECURITY, DOM-COMPLIANCE — are operator-product domains from before operator separation. Not protocol governance domains. **REMOVE.**
3. RFC/ADR explanations are accurate
4. ADR-025 reference is correct

---

### §9 — Modelo de Certificação (Lines 441–493)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese |
| Content quality | PARTIAL |
| Factual accuracy | PARTIAL (notable errors) |
| Pre-ADR-026/028/029? | YES — predates ADR-028 certification architecture |
| Action | **REWRITE** — significant errors must be corrected |

**Issues:**
1. **WRONG L3 REQUIREMENTS:** L3 shows "L2 + payout.batch, reconciliation" — missing certificate requirement, BRL check, `supports_federation: true` manifest requirement, 90-day certificate lifetime, `POST /federation/route` endpoint. These are required per ADR-028.
2. **WRONG L4 DEFINITION:** Shows "L3 + acquiring.emis, federation_ready" — `federation_ready` is NOT a new L4 capability; it's already satisfied at L3. L4 is card acquiring only.
3. **WRONG MANIFEST FORMAT:** `"version": "1.0.0"` (should be `"protocol_version": "1.0"`), `"invariants_asserted"` is not a real manifest field, environment value `"LIVE"` should be `"production"`.
4. **MISSING:** Certificate issuance (from BanzAI section §10 note), BRL compliance as a certification requirement

---

### §10 — Federação (Lines 495–808)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese |
| Content quality | EXCELLENT — the strongest section in the document |
| Factual accuracy | PARTIAL (one content error, one massively stale table) |
| Pre-ADR-026/028/029? | YES — written before conformance was complete |
| Action | **REWRITE** — translate, fix BanzAI error, replace stale table |

**Issues:**
1. **BANZAI ERROR (DEFECT):** Lines 699: "✓ Executa o conformance suite (79 testes de federação)" — BanzAI does NOT run the authoritative conformance suite. The authoritative runner is `tools/banza-conformance/run_fed.py`. BanzAI's `conformance-runner.ts` is a guidance simulation. **Must be corrected.**
2. **MASSIVELY STALE STATUS TABLE (Lines 793–804):** Shows federation implementation as 2027–2028 future work. Current state is:
   - Runner: COMPLETE (79/79 tests pass)
   - Kernel federation: COMPLETE (FED-SETTLE suite, reconciliation, obligations)
   - Pilots: 14/14 interoperability scenarios pass — M1 achieved 2026-06-01
   - "Federação aberta: 2028" — federation spec is frozen TODAY
   This entire table must be replaced with accurate current state.
3. The narrative content (before/after, Ana/Bento example, obligations, netting) is EXCELLENT — preserve in full translation.

---

### §11 — Roadmap do Protocolo (Lines 810–837)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese |
| Content quality | POOR — entirely stale |
| Factual accuracy | NONE — every item is wrong |
| Pre-ADR-026/028/029? | YES |
| Action | **REMOVE + REPLACE** |

**Stale items (every single one):**
- "Conformance Suite v1: H2 2026" → COMPLETE (shipped 2026)
- "Certificação Nível 1–2: H2 2026" → L0–L2 conformance suite complete
- "Certificação Nível 3–4: H1 2027" → L3 federation spec: COMPLETE, 79/79 tests pass
- "Operadores de terceiros: H1 2027" → pending M3 but spec + suite complete
- "RFC de federação: H1 2027" → ADR-026 ACCEPTED 2026
- "Portal de certificação: H1 2027" → DEFERRED (FUTURE-009, v1.1)
- "Piloto de federação: H2 2027" → 14/14 interoperability scenarios pass NOW
- "Federação aberta: 2028" → federation spec COMPLETE, pending root key ceremony
- "Carris cross-border: H2 2027+" → DEFERRED (FUTURE-008, v2.0)

Replacement roadmap should accurately reflect M1–M6 milestones and v1.1/v2.0 future work.

---

### §12 — Declaração de Visão (Lines 840–854)

| Attribute | Value |
|-----------|-------|
| Language | Portuguese |
| Content quality | HIGH — clear, principled vision statement |
| Factual accuracy | HIGH |
| Operator-specific contamination | NONE |
| Action | **KEEP + translate to English** |

**Issues:**
- Portuguese only
- "dos operadores actuais" — minor wording, fine

---

### References Section (Lines 856–872)

**Issues:**
- Missing ADR-026, ADR-028, ADR-029 — the three most recent and critical ADRs
- Self-referential link to `../banza/BANZA_REFERENCE.md` (DEFECT — this IS that file)

---

## Defects Register

| ID | Location | Defect | Severity |
|----|----------|--------|----------|
| DEF-001 | §5 line 255 | Circular self-reference: links to `../banza/BANZA_REFERENCE.md` which is this document | HIGH |
| DEF-002 | §8 lines 423–426 | References `docs/validation/BANZA_IMPLEMENTATION_MATRIX.json` which lives in reference operator repo, not here | HIGH |
| DEF-003 | §8 lines 428–438 | "Domínios de Validação" (DOM-FIN through DOM-COMPLIANCE) are legacy operator-product domains, not protocol governance | MEDIUM |
| DEF-004 | §9 L3 row | L3 certification requirements incomplete — missing certificate, BRL check, `supports_federation`, 90-day lifetime | HIGH |
| DEF-005 | §9 L4 row | L4 shows "federation_ready" as new L4 capability — it is already L3; L4 is card acquiring only | HIGH |
| DEF-006 | §9 manifest | Operator manifest JSON uses wrong field names (`version` vs `protocol_version`) and non-existent field (`invariants_asserted`) | MEDIUM |
| DEF-007 | §10 line 699 | BanzAI "Executa o conformance suite (79 testes de federação)" — incorrect; BanzAI runs guidance simulation only; authoritative suite is `run_fed.py` | HIGH |
| DEF-008 | §10 lines 793–804 | Federation implementation status table shows 2027–2028 future work; federation is COMPLETE 2026 | CRITICAL |
| DEF-009 | §11 all | Roadmap is entirely stale — every item was achieved or superseded | CRITICAL |
| DEF-010 | References | Missing ADR-026, ADR-028, ADR-029 | HIGH |

---

## Content Classification Summary

| Section | Action | Priority |
|---------|--------|----------|
| §1 Problem statement | REWRITE (translate) | HIGH |
| §2 M-Pesa vs Pix/UPI model | REWRITE (translate) | HIGH |
| §3 What is BANZA | REWRITE (translate + update) | HIGH |
| §4 Core principles | REWRITE (translate + update) | HIGH |
| §5 Ecosystem architecture | REWRITE (translate + fix DEF-001) | HIGH |
| §6 Monetary representation | REWRITE (translate, content correct) | MEDIUM |
| §7 Financial invariants | REWRITE + EXPAND (translate, add INV-TRUST/ROOT) | HIGH |
| §8 Governance | REWRITE (translate, remove DEF-002/DEF-003) | HIGH |
| §9 Certification | REWRITE (fix DEF-004/005/006) | CRITICAL |
| §10 Federation | REWRITE (translate, fix DEF-007/DEF-008) | CRITICAL |
| §11 Roadmap | REMOVE + REPLACE | CRITICAL |
| §12 Vision | KEEP + translate | LOW |
| References | UPDATE (add ADR-026/028/029) | HIGH |

## Missing Sections (Not Present, Required for Website)

| Section | Status | Source material |
|---------|--------|----------------|
| **Trust** (root key, Key Manifest, BRL, certificate chain) | MISSING | ADR-029, ceremony procedure docs |
| **BanzAI** (standalone section) | MISSING | BANZAI_REFERENCE.md, apps/banzai/ |
| **Operators** (how to become an operator, operator quickstart) | MISSING | BANZA_CERTIFICATION.md, FEDERATION_OPERATOR_QUICKSTART.md |
| **Developer Resources** (SDKs, contracts, conformance runner) | MISSING | sdk/, contracts/, tools/ |
| **FAQ** | MISSING | Infer from existing content |

---

## Language Assessment

The entire document is in Portuguese. For banza.network targeting international operators, developers, regulators, and partners, the document must be rewritten in English. The Portuguese narrative voice is excellent — the substance should be preserved in translation.

Portuguese-language content may be appropriate as a secondary audience document (Angola-facing) but the primary authoritative reference must be English.
