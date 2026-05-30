# Hero & Positioning Consistency Audit

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Executed by:** BANZA-NAMING-INVERSION-STEP-007  
**Status:** Audit complete — no code changes made

---

## Scope

Surfaces reviewed after Wave 3 completion:

- Homepage hero: badge, H1, subheadline, capability tags, CTA buttons (`/`)
- BanzAI teaser widget (`HeroBanzamIAWidget` on homepage)
- Homepage body sections §3–§11
- Footer tagline (global layout)
- Navigation labels (global layout)
- Reference landing page (`/reference`)
- About BanzAI page (`/sobre-banzamia`)
- BanzAI app page (`/banzamia`)
- Architecture page (`/arquitectura-tecnica` — `[section]` route)
- Operators page (`/operators`)
- Roadmap page (`/roadmap`)

---

## Positioning Rules (ADR-025)

| Entity | Role | Expected headline language |
|--------|------|---------------------------|
| Banza | Open financial protocol / infrastructure kernel | "protocolo", "infraestrutura", "rede de protocolo", "ledger" |
| Banzami | Product operator / consumer & merchant experience | "produto", "pagamentos", "app", "rede de pagamentos", "QR" |
| BanzAI | Protocol Operating System | "Sistema Operativo de Protocolo", "Protocol OS" |

**Primary rule:** On a Banzami-branded page, the above-the-fold headline must describe Banzami (product) unless the section is explicitly about the Banza protocol or BanzAI. The logo reads "Banzami" — the headline must confirm that identity, not contradict it.

---

## Findings

### F-001 — Homepage hero badge [HIGH]

| Field | Value |
|-------|-------|
| **Page** | `/` — homepage |
| **File** | `apps/docs/components/HeroSection.tsx:36` |
| **Current text** | `"Infraestrutura Financeira Programável para Angola"` |
| **Actual subject** | Banza (the protocol / infrastructure layer) |
| **Expected subject** | Banzami (the product — this is banzami.org) |
| **Risk** | HIGH |

**Why it matters:** The badge is the first rendered text element a visitor reads — it appears above the H1. It frames the visitor's initial interpretation before the logo or subheadline registers. "Infraestrutura Financeira Programável" is protocol language (it describes Banza, not Banzami). A visitor reading badge → H1 before the subheadline forms the mental model "Banzami = infrastructure" — the exact pre-inversion confusion ADR-025 was written to eliminate.

**Recommended wording:**
- `"Pagamentos Instantâneos em Kwanza · Angola"` — product-first, matches site metadata title
- `"Rede de Pagamentos QR-Native · Angola"` — slightly more evocative, still product

---

### F-002 — Homepage H1 [HIGH]

| Field | Value |
|-------|-------|
| **Page** | `/` — homepage |
| **File** | `apps/docs/components/HeroSection.tsx:42–52` |
| **Current headline** | `"Infraestrutura financeira programável."` |
| **Current subheadline** | `"Banzami é o produto de pagamentos de Angola, construído sobre o Banza — protocolo aberto de infraestrutura financeira."` *(corrected in Wave 3 P0)* |
| **Actual subject of H1** | Banza (the protocol) |
| **Expected subject** | Banzami (the product) |
| **Risk** | HIGH |

**Why it matters:** The H1 is the dominant visual element on the page — 4x larger than body text, above the fold, read before or in parallel with the logo. Its subject is "infraestrutura financeira programável" — an accurate description of Banza, not Banzami. Combined with badge F-001, a visitor receives two consecutive "infrastructure / protocol" signals before the correcting subheadline.

The P0 fix (subheadline) mitigates the confusion but does not eliminate it. Visitors who skim the badge+H1 and scroll past the subheadline, or whose attention moves to the capability tags before reading the subheadline, carry the wrong mental model forward.

**Compounding effect with F-001:** Badge says "Infraestrutura Financeira Programável" → H1 says "Infraestrutura financeira programável." → same phrase, twice, before any product language. The subheadline then corrects this but requires full attention.

**Recommended wording options:**

| Option | H1 | Notes |
|--------|----|-------|
| A — product-first | `"Pague com Banzami."` | Unambiguous; matches consumer product framing |
| B — network-first | `"A rede de pagamentos de Angola."` | Positions Banzami as a network (closer to current meaning) |
| C — hybrid | `"Pagamentos instantâneos construídos sobre infraestrutura aberta."` | Acknowledges protocol layer; product outcome is primary |
| D — badge-only fix | *(keep H1, fix badge only)* | Minimum-change option: badge anchors product identity, H1 describes the protocol layer beneath |

**Note:** Option D is valid if banzami.org is intentionally positioned as both a product site and a protocol documentation site. In that case, the H1 describes the protocol that Banzami builds on, and the subheadline explains Banzami's role. This requires a conscious design decision, not a default.

---

### F-003 — Footer tagline uses "Rede" [MEDIUM]

| Field | Value |
|-------|-------|
| **Page** | All pages (global footer) |
| **File** | `apps/docs/app/layout.tsx:145` |
| **Current text** | `"Banzami — Rede Angolana de Pagamentos Instantâneos por QR Code"` |
| **Actual subject** | Banzami |
| **Issue** | "Rede" (network) implies Banzami is the network layer |
| **Risk** | MEDIUM |

**Why it matters:** Under ADR-025, Banza is the open protocol network; Banzami is the product. "Rede Angolana de Pagamentos" positions Banzami as the network layer — the exact pre-inversion language. Visitors who skim to the footer first, or who read the footer for a quick summary of what the site is about, will see "Banzami = Rede" (network), not "Banzami = produto de pagamentos."

**Recommended wording:**
- `"Banzami — Pagamentos Instantâneos em Kwanza"` — matches layout metadata `title.default` exactly; zero ambiguity
- `"Banzami — O produto de pagamentos de Angola"` — more explicit

---

### F-004 — Homepage §8 H2: "Banza em toda Angola" [MEDIUM]

| Field | Value |
|-------|-------|
| **Page** | `/` — homepage, use-cases section |
| **File** | `apps/docs/app/page.tsx:168` |
| **Current headline** | `"Banza em toda Angola"` |
| **Current subheadline** | *(eyebrow: "Casos de uso")* — lists taxi apps, cantinas, ecommerce, doações, schools, delivery |
| **Actual subject of H2** | "Banza" (protocol namespace used for product use cases) |
| **Expected subject** | Banzami (the product enabling these consumer use cases) |
| **Risk** | MEDIUM |

**Why it matters:** The use cases listed (taxi apps, cantinas, school fees) are Banzami product use cases — consumers paying with the Banzami app, merchants accepting via Banzami QR. The section headline calls this "Banza em toda Angola," attributing Banzami's product reach to the Banza name. Post-inversion, product reach = Banzami; protocol reach = Banza.

**Recommended wording:** `"Banzami em toda Angola"`

---

### F-005 — Homepage §9 subheadline: "A experiência mobile Banza" [MEDIUM]

| Field | Value |
|-------|-------|
| **Page** | `/` — homepage, mobile-first section |
| **File** | `apps/docs/app/page.tsx:188` |
| **Current text** | `"A experiência mobile Banza é desenhada para ser instantânea, em português (pt-AO), e funcionar em qualquer rede de dados angolana."` |
| **Actual subject** | "Banza" (protocol name applied to product-layer concept) |
| **Expected subject** | Banzami (the mobile app / consumer product) |
| **Risk** | MEDIUM |

**Why it matters:** The mobile experience is the Banzami consumer app — it is a product-layer artefact. Calling it "experiência mobile Banza" uses the protocol name for something that belongs to Banzami. Note: "qualquer rede de dados angolana" at the end refers to a data network (cellular), not a brand — this is not a risk.

**Recommended wording:** `"A experiência mobile Banzami é desenhada para ser instantânea, em português (pt-AO), e funcionar em qualquer rede de dados angolana."`

---

### F-006 — Homepage §4 subheadline: "pagamento Banza" [LOW]

| Field | Value |
|-------|-------|
| **Page** | `/` — homepage, "Como funciona" section |
| **File** | `apps/docs/app/page.tsx:113` |
| **Current text** | `"Cada pagamento Banza é uma transferência directa entre carteiras, registada no ledger de forma atómica e imutável."` |
| **Actual subject** | Ambiguous — "pagamento Banza" = a payment on the Banza ledger |
| **Risk** | LOW |

**Why it matters:** "Pagamento Banza" is technically defensible — the payment primitive runs on the Banza protocol ledger. This is the most ambiguous finding: from a protocol documentation perspective, "Banza payment" accurately describes the ledger-level transaction. From a consumer product perspective, customers make "Banzami payments."

**Assessment:** If the intended audience for this section is developers or operators, keeping "Banza payment" is accurate. If the site is consumer-first, "Banzami" is correct.

**Recommended wording (if changed):** `"Cada pagamento Banzami é uma transferência directa entre carteiras, registada no ledger do Banza de forma atómica e imutável."` — preserves both brand references correctly.

---

## Clean Surfaces — No Issues Found

| Surface | Page | Headline / Text | Verdict |
|---------|------|-----------------|---------|
| Navigation labels | All pages | Referência, Programadores, Comerciantes, Arquitectura, Segurança, Operadores, Validação, BanzAI | ✓ Neutral topical labels; no brand confusion |
| BanzAI widget header | Homepage | "Pergunte ao BanzAI" · chip "BanzAI" | ✓ Correctly positioned |
| BanzAI widget subtitle | Homepage | "O Sistema Operativo de Protocolo do ecossistema Banzami." | ✓ Both brands correctly placed |
| Capability tags | Homepage hero | Operadores certificados · Federação · Liquidação · Rastreabilidade · Conformidade · BanzAI | ✓ Protocol capabilities for Banza; BanzAI correctly distinguished |
| Site metadata title | All | `"Banzami — Pagamentos Instantâneos em Kwanza"` | ✓ Correct product framing |
| Logo + wordmark | All (header) | "Banzami" | ✓ Correct |
| Reference landing | `/reference` | H1: "Banzami — Referência Oficial" | ✓ Correctly positioned |
| Reference description | `/reference` | "ecossistema Banzami" + "rede Banza" | ✓ Both brand references correct |
| About BanzAI | `/sobre-banzamia` | "O BanzAI é o Sistema Operativo do Protocolo Banza — 16 módulos…" | ✓ Correctly positioned |
| BanzAI app | `/banzamia` | title: "BanzAI — Protocol Operating System" | ✓ Correctly positioned |
| Operators page | `/operators` | H1: "Registo de Operadores Banza" · badge: "Protocolo v1.0" | ✓ Correct — Banza protocol operators |
| Operators description | `/operators` | "operadores que implementam o protocolo Banza" | ✓ Correct |
| Roadmap | `/roadmap` | H1: "BanzAI Roadmap" · breadcrumb: Banzami / BanzAI | ✓ Correctly positioned; breadcrumb hierarchy is accurate |
| Architecture page | `/arquitectura-tecnica` | Content from BANZAMI_REFERENCE.md (Wave 1 scope) | ✓ Prose updated in Wave 1; metadata template uses "Banzami — §N: Title" correctly |

---

## Visitor Mental Model Test

**Scenario: first-time visitor lands on banzami.org**

Sequential reading order (above the fold):

| Step | Element | Text | Brand signal |
|------|---------|------|-------------|
| 1 | Logo | Banzami | Banzami ✓ |
| 2 | Badge | "Infraestrutura Financeira Programável para Angola" | Banza ✗ (F-001) |
| 3 | H1 | "Infraestrutura financeira programável." | Banza ✗ (F-002) |
| 4 | Subheadline | "Banzami é o produto de pagamentos de Angola, construído sobre o Banza…" | Banzami ✓ corrects confusion |
| 5 | Capability tags | Operadores certificados, Federação, Liquidação, Rastreabilidade, Conformidade, BanzAI | Protocol-layer ← accurate but reinforces infrastructure framing |
| 6 | BanzAI widget | "Pergunte ao BanzAI — Sistema Operativo de Protocolo do ecossistema Banzami" | BanzAI ✓ |

**Risk:** A visitor who reads steps 1–3 and does not slow down for step 4 carries "Banzami = infrastructure" as their primary mental model. The badge and H1 deliver this message twice before the subheadline corrects it. Any visitor who scrolls past the subheadline — a common mobile pattern — is vulnerable to this false framing.

**Minimum fix to break the pattern:** Fix the badge (F-001) to product language. The badge is smaller than the H1 and read first. Changing it from "Infraestrutura Financeira Programável para Angola" to "Pagamentos Instantâneos em Kwanza" anchors the visitor in product territory before they read the H1, giving the H1 protocol language a different reading context: "infrastructure" is what Banzami is built on, not what Banzami is.

---

## Priority Matrix

| # | Finding | File | Risk | Fix effort | Recommended priority |
|---|---------|------|------|-----------|---------------------|
| F-001 | Hero badge — protocol language | `HeroSection.tsx:36` | HIGH | XS — 1 string | P1 |
| F-002 | Hero H1 — protocol framing | `HeroSection.tsx:42` | HIGH | S — requires design decision | P2 (design review first) |
| F-003 | Footer "Rede Angolana" | `layout.tsx:145` | MEDIUM | XS — 1 string | P2 |
| F-004 | §8 H2 "Banza em toda Angola" | `page.tsx:168` | MEDIUM | XS — 1 string | P2 |
| F-005 | §9 "experiência mobile Banza" | `page.tsx:188` | MEDIUM | XS — 1 string | P2 |
| F-006 | §4 "pagamento Banza" | `page.tsx:113` | LOW | XS — 1 string | P3 (intentional reading possible) |

---

## Notes

- **F-002 design intent:** The H1 "Infraestrutura financeira programável." may be intentional — banzami.org serves operators, developers, and consumers, not only consumers. If the site's primary audience is protocol implementers, the H1 accurately describes what they care about. The subheadline then positions Banzami as the reference product built on it. This is a legitimate dual-audience positioning strategy. The decision to change or keep the H1 belongs to product, not migration.

- **Architecture page:** Content derives from BANZAMI_REFERENCE.md, updated in Wave 1. The section page metadata uses the template `Banzami — §N: [title]` (correct). No positioning issues found at the rendering layer.

- **Code identifiers excluded:** Component names (`BanzamIAWidget`, `BanzamIASidebar`), route paths (`/banzamia`), env vars — deferred to Waves 4–9. These are not human-readable positioning text.

- **Wave 3 P0 effectiveness:** The subheadline fix (P0: F-001 false statement corrected) is working as intended. It accurately describes the relationship between Banzami and Banza. The remaining findings are positioning refinements that go beyond factual correction.
