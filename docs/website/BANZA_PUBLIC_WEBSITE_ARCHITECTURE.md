# BANZA Public Website Architecture

**Document ID:** BANZA-WEBSITE-ARCHITECTURE-001  
**Date:** 2026-06-01  
**Authority:** BANZA-WEBSITE-AND-INFRASTRUCTURE-ALIGNMENT-001  
**Domains:** `banzami.org` (temporary) → `banza.network` (production)

---

## Architectural Decision: BanzAI Is a BANZA Section

**BanzAI does not have its own public website. BanzAI does not have its own domain.**

BanzAI is a major section of the BANZA website. All public-facing communication about BanzAI lives under the BANZA website hierarchy. The `banzai.network` domain referenced in prior analysis documents does not represent a separate public site — it is a forward reference to a future subdomain or page, not an independent platform.

```
BANZA (website)
├── /protocol
├── /certification
├── /federation
├── /trust
├── /operators
├── /developers
├── /governance
├── /banzai          ← BanzAI lives here, not at a separate domain
├── /roadmap
├── /faq
└── /docs
```

This hierarchy is frozen and non-negotiable.

---

## Domain Strategy

| Phase | Domain | Status | Purpose |
|-------|--------|--------|---------|
| Current | `banzami.org` | Active | Temporary BANZA protocol website |
| Production | `banza.network` | Planned | Permanent BANZA protocol domain |

**During the temporary phase (`banzami.org`):**
- `banzami.org` and `www.banzami.org` → BANZA protocol website
- `api.banzami.org` → Operator API gateway (reference operator — unchanged)
- `admin.banzami.org` → Operator admin frontend (reference operator — unchanged)
- `business.banzami.org` → Operator merchant dashboard (reference operator — unchanged)
- `pay.banzami.org` → Operator hosted checkout (reference operator — unchanged)
- `staging.banzami.org` → Sandbox/staging API (reference operator — unchanged)
- `consumer.banzami.org` → Public API (reference operator — unchanged)

**Authority confusion avoidance:** The BANZA protocol website at `banzami.org` must not present itself as a product of any specific operator. The main domain serves protocol content. Operator subdomains serve operator products. These are distinct and must be kept separate in content and branding.

**On domain transition to `banza.network`:**
- All `/` routes and content migrate to `banza.network`
- `banzami.org` becomes redirect-only → `banza.network`
- Operator subdomains may eventually move to their own domain
- `banzai.network` referenced in prior docs: reserved for future consideration; not a current target

---

## Navigation Structure

```
/                   Homepage — What is BANZA, hero, problem, ecosystem overview
/protocol           The Protocol — Principles, architecture, how it works
/certification      Certification — L0–L4 levels, process, requirements
/federation         Federation — How the network works, 5-step flow, status
/trust              Trust — Root key, Key Manifest, BRL, certificate chain
/operators          Operators — How to become one, network effects
/banzai             BanzAI — Protocol Operating System, full capabilities
/developers         Developers — SDKs, APIs, contracts, conformance runner
/governance         Governance — RFCs, ADRs, open process
/roadmap            Roadmap — M1–M6, v1.1, v2.0
/faq                FAQ — Common questions, all audiences
/docs               Documentation — Reference, API specs, guides
```

---

## Source Mapping: BANZA_REFERENCE.md → Pages

The website reads content from `BANZA_REFERENCE.md` via a `getReference()` / `getSection()` function. The section slug must map to the website navigation.

| URL | BANZA_REFERENCE.md § | Section title | Readiness |
|-----|---------------------|---------------|:---------:|
| `/` | §1 + §2 | Introduction + Why BANZA Exists | 80% |
| `/protocol` | §3 + §4 | Core Principles + Developer Resources | 85% |
| `/certification` | §4 | Certification | 90% |
| `/federation` | §5 | Federation | 90% |
| `/trust` | §6 | Trust | 80%* |
| `/operators` | §8 | Operators | 85% |
| `/banzai` | BANZAI_REFERENCE.md | Full BanzAI reference | 75% |
| `/developers` | §9 | Developer Resources | 85% |
| `/governance` | §10 | Governance | 85% |
| `/roadmap` | §11 | Roadmap | 90% |
| `/faq` | §12 | FAQ | 90% |
| `/docs` | All sections | Full reference | 80% |

*Trust section readiness at 80% — production endpoints (Key Manifest, BRL) not yet live (blocked on M2).

---

## Technical Architecture

### Website stack (existing — do not replace)

```
docs-frontend (Next.js 14 + React, TypeScript)
├── Reads: BANZA_REFERENCE.md (baked at build time via getReference())
├── Reads: BANZAI_REFERENCE.md (for /banzai section)
├── Components: PaymentFlowDiagram, EcosystemMap, SectionHero, etc.
├── Routes: /[section] (static generation from BANZA_REFERENCE.md)
├── Routes: /banzai (live BanzAI interface or static content)
└── Deployed: Docker container → nginx → banzami.org
```

The existing docs app at `/srv/banzami/src/apps/docs/` already implements:
- Content from BANZA_REFERENCE.md via `getReference()` / `getAllSectionSlugs()`
- A `/banzai` section with its own page
- A `[section]` dynamic route statically generated from BANZA_REFERENCE.md
- React components for diagrams and visual content

### Required updates (not a replacement)

1. **Metadata cleanup:** Remove "Banzami é o operador de referência" from site metadata. Replace with BANZA protocol identity.
2. **Language:** Interface text that is Portuguese must be updated to English (content sections read from BANZA_REFERENCE.md are already English after consolidation).
3. **Static generation fix:** `getAllSectionSlugs()` must be updated to match the new 12-section structure of BANZA_REFERENCE.md.
4. **BanzAI page:** `/banzai` must render content from the updated BANZAI_REFERENCE.md.
5. **SEO:** keywords and description must reflect BANZA protocol, not Banzami product.

### BanzAI section integration

The `/banzai` route at `banzami.org/banzai` must:
- Render content from `BANZAI_REFERENCE.md`
- Include the authority boundary statement: "BANZA defines. BANZA certifies. BanzAI evaluates. Operators implement."
- NOT link to a separate BanzAI website
- NOT imply BanzAI has its own public platform

The BanzAI API (`banzamia-api-1`, port 4001) is available as a backend. The `/banzai` page may optionally call it for live interactive features. This requires:
- A nginx route for the BanzAI API (currently exposed on port 4001 without nginx — add route under `banzami.org/banzai/api/`)
- Updated env var naming (see VM audit)

---

## Homepage Design (banzami.org / banza.network)

**Hero:**  
"BANZA is Angola's open payment protocol — the infrastructure beneath any operator."

**Three-panel ecosystem:**  
BANZA protocol rules → BanzAI explains, evaluates, guides → Operators implement

**Problem statement:**  
16M mobile users. Banks, EMIS, WhatsApp receipts. The missing protocol layer.

**Open protocol argument:**  
M-Pesa (closed) vs Pix/UPI/BANZA (open) — comparative table.

**Status banner:**  
"M1 Protocol Complete — 79/79 federation tests pass. 14/14 interoperability scenarios pass."

**Navigation cards to:**  
/certification · /federation · /trust · /banzai · /operators · /developers

---

## Visual Assets Required

| Asset | Status | Required for |
|-------|--------|-------------|
| Ecosystem hierarchy (BANZA → BanzAI → Operators) | PARTIAL (EcosystemMap component exists) | Homepage |
| Certification level ladder (L0 → L4) | MISSING | /certification |
| Trust chain diagram (Root → Key Manifest → Cert → Operator) | MISSING | /trust |
| Federation payment flow (Operator A → BANZA → Operator B) | PARTIAL (PaymentFlowDiagram exists) | /federation |
| BanzAI architecture (6 categories) | MISSING | /banzai |
| Validation Studio (Matrix A/B/C) | MISSING | /banzai |
| Roadmap timeline (M1–M6) | MISSING | /roadmap |
| M-Pesa vs Pix/UPI comparison | PARTIAL (data in reference) | Homepage |

---

## Content Authority

All public content on the BANZA website must be derivable from:
1. `BANZA_REFERENCE.md` — primary source for all protocol content
2. `BANZAI_REFERENCE.md` — source for /banzai section
3. Protocol ADRs — authoritative for technical claims

No content may:
- Name a specific certified operator in protocol explanations
- Imply BanzAI has its own public platform
- Present operator-specific business logic as protocol behavior
- Contradict any financial invariant (INV-LEDGER-*, INV-WALLET-*, etc.)
