---
name: banza-ecosystem-adoption-roadmap
description: Master adoption roadmap sequencing the work needed to convert each audience from understanding to participation — prioritized by leverage and dependency
metadata:
  type: project
---

# BANZA — Ecosystem Adoption Roadmap

**Mission:** BANZA-ADOPTION-ARCHITECTURE-001  
**Scope:** All six audiences — Operators, Developers, Regulators, Merchants, Investors, Banks  
**Date:** 2026-05-30  
**Status:** Official

---

## Premise

The BANZA ecosystem is structurally coherent. ADR-025 is complete. Identity alignment is complete. Documentation architecture is complete. Cross-repository consistency is complete.

The next challenge is not what BANZA is. The challenge is why others should join.

The shift required:

| From | To |
|------|----|
| "What is BANZA?" | "Why should I adopt BANZA?" |
| Structural description | Rational incentive |
| Protocol definition | Network participation case |
| "Here is how it works" | "Here is what you gain by joining" |

---

## Adoption Dependency Map

Not all adoption is independent. Some audiences unlock others:

```
BNA (Regulator)
    ↓ enables
Operator adoption (certified entities can operate legally)
    ↓ enables
Developer adoption (more operators = more SDK demand)
    ↓ enables
Merchant adoption (more integrations = more places to pay)
    ↓ enables
Consumer adoption (more merchants = utility for consumers)
    ↓ creates
Network effects (more consumers = more merchant adoption)
```

**Implication:** Regulatory clarity is the highest-leverage investment in the adoption chain. A single BNA acknowledgment unblocks every operator who was waiting for regulatory cover.

**Second implication:** Banzami as the first operator and the reference implementation is simultaneously proving the protocol AND building the consumer and merchant network. These are not separable until there is a second operator.

---

## Current Adoption State

| Audience | Current State | Adoption Blocker |
|----------|--------------|-----------------|
| **Operators** | 1 certified (Banzami, L4). Conformance suite not publicly executable. | Conformance suite v1, certification economics |
| **Developers** | SDK implemented, not yet published on npm/pub.dev/Packagist. No quick-start. | Package publication, 15-min tutorial |
| **Regulators** | No documented BNA engagement. Protocol documents silent on regulatory alignment. | Regulatory alignment document, direct BNA engagement |
| **Merchants** | Product exists (Banzami Business). No public merchant pricing. No traction metrics. | Pricing transparency, consumer network size, mobile app |
| **Investors** | No public traction data. No investor-facing materials. No governance independence roadmap. | Metrics, investor narrative, team visibility |
| **Banks** | No bank-specific positioning. No EMIS technical documentation for bank-operators. | Bank-as-operator narrative, EMIS docs |

---

## Phase 1 — Protocol Minimum Viable Adoption (H2 2026)

**Goal:** Remove the blockers that prevent any external party from engaging seriously.

### P1.1 — Regulatory foundation

| Action | Owner Layer | Deliverable |
|--------|------------|-------------|
| Write regulatory alignment appendix (BANZA certification ≠ BNA license, how they relate) | BANZA protocol docs | `BANZA_CERTIFICATION.md` appendix |
| Write AOA-exclusivity commitment as formal protocol guarantee | BANZA protocol docs | `BANZA_REFERENCE.md §6` + formal statement |
| Write compliance specification mapped to BNA AML/KYC | BANZA protocol docs | `BANZA_COMPLIANCE_SPECIFICATION.md` |
| Initiate BNA engagement — informal briefing on protocol architecture | External relations | Meeting record |

**Why first:** Every other adoption path waits for regulatory clarity. This is the unblocking prerequisite.

### P1.2 — Developer minimum viability

| Action | Owner Layer | Deliverable |
|--------|------------|-------------|
| Publish `@banza/sdk` on npm | Banzami SDK | npm package live |
| Publish `banza_flutter` on pub.dev | Banzami SDK | pub.dev package live |
| Write 15-minute first-payment tutorial (sandbox QR payment, zero protocol knowledge) | Banzami docs | `docs/developer/quick-start.md` |
| Make sandbox API key issuance self-service (sign up → key issued automatically) | Banzami product | Self-service sandbox flow |

**Why in P1:** Without a published SDK, developer adoption is not possible. This is the minimum viable developer experience.

### P1.3 — Merchant minimum viability

| Action | Owner Layer | Deliverable |
|--------|------------|-------------|
| Publish merchant pricing (even if minimal: flat fee % + withdrawal fee) | Banzami product | Pricing page on banzami.com |
| Launch Banzami Business mobile app production release | Banzami product | App on Google Play Store |
| Write non-technical merchant onboarding guide | Banzami docs | `docs/merchant/get-started.md` |
| Onboard first 10 merchants publicly listed on site | Banzami commercial | Merchant directory on banzami.com |

**Why in P1:** Merchants are the network's supply side. Without them, consumers have nowhere to pay. Without pricing transparency, merchant adoption decisions cannot be made.

---

## Phase 2 — Protocol First External Operator (H1 2027)

**Goal:** Convert the first external entity to a certified operator. This is the proof that BANZA is a protocol, not just a product.

### P2.1 — Conformance suite publication

| Action | Deliverable |
|--------|-------------|
| Publish conformance suite v1 as publicly executable CLI | `banza-conformance` on GitHub, runnable locally |
| Publish conformance test vectors publicly | `banza/contracts/conformance/` |
| Document certification process end-to-end (L0 → L1 → L2) | `BANZA_CERTIFICATION.md` update |
| Publish certification economics (fees, SLAs, support model) | Pricing/certification economics page |

### P2.2 — Operator starter kit

| Action | Deliverable |
|--------|-------------|
| Publish Operator Starter Kit (scaffolded L0 implementation, TypeScript + Go) | `docs/operator/starter-kit/` |
| Publish "First certification in 30 days" guide | `docs/operator/first-certification.md` |
| Open BanzAI Certification Copilot to external operator candidates | BanzAI API public access for operators |

### P2.3 — First external certification event

| Action | Deliverable |
|--------|-------------|
| Identify first external operator candidate (telco, fintech, or bank) | Signed LOI or letter of intent to certify |
| Support first operator through L0 → L1 certification | Documented certification case |
| Publish certification result publicly | Operator registry entry |

**Success criterion:** A second entity — not Banzami — appears in the operator registry with a valid certification.

### P2.4 — Investor readiness

| Action | Deliverable |
|--------|-------------|
| Publish public metrics dashboard (transaction count, volume, merchant count, consumer count) | banzami.com/metrics |
| Publish governance independence roadmap (path to independent governance body) | `BANZA_GOVERNANCE.md` update |
| Prepare investor brief (protocol economics model, market size, team) | Investor deck / memo |

---

## Phase 3 — Network Effects Begin (H2 2027)

**Goal:** Multiple certified operators. Federation pilot. Consumer network visible to regulators and investors.

### P3.1 — Federation pilot

| Action | Deliverable |
|--------|-------------|
| RFC for federation protocol published | `banza/docs/rfc/RFC-FED-001.md` |
| Federation pilot: two operators exchange payments | Documented pilot results |
| BanzAI Federation Intelligence module deployed for pilot operators | Real federation analysis in production |

### P3.2 — Consumer network milestone

| Action | Deliverable |
|--------|-------------|
| 10,000 active consumer wallets | Publicly announced milestone |
| 100 merchants accepting Banzami QR | Merchant directory update |
| Consumer testimonials (organic) | banzami.com/stories |

### P3.3 — Regulatory formalization

| Action | Deliverable |
|--------|-------------|
| BNA formal acknowledgment of BANZA certification framework | Public statement or regulatory guidance |
| First independent compliance audit of Banzami implementation | Published audit summary |
| Observer role for BNA in RFC process formalized | Governance update |

---

## Master Gap Register

All gaps identified across the six audience reports, consolidated and prioritized:

### Critical (blocks adoption)

| Gap | Audience | Phase |
|-----|----------|-------|
| `@banza/sdk` not on npm | Developer | P1 |
| Merchant pricing not public | Merchant | P1 |
| Conformance suite not publicly executable | Operator | P2 |
| No BNA regulatory engagement documented | Regulator | P1 |
| No regulatory alignment document | Regulator | P1 |
| Sandbox API key not self-service | Developer | P1 |
| Banzami Business mobile app not production-released | Merchant | P1 |

### High (significantly impedes adoption)

| Gap | Audience | Phase |
|-----|----------|-------|
| No 15-minute developer quick-start | Developer | P1 |
| No webhook verification guide | Developer | P1 |
| No merchant onboarding guide (non-technical) | Merchant | P1 |
| No merchant dispute and refund documentation | Merchant | P1 |
| No compliance specification mapped to BNA AML/KYC | Regulator | P1 |
| No certification economics document | Operator | P2 |
| No operator starter kit | Operator | P2 |
| No public traction metrics | Investor | P2 |
| No consumer protection framework | Regulator | P2 |
| `banza_flutter` not on pub.dev | Developer | P1 |

### Medium (impedes scale, not initial adoption)

| Gap | Audience | Phase |
|-----|----------|-------|
| No governance independence roadmap | Investor/Operator | P2 |
| No bank-as-operator narrative | Bank | P2 |
| No EMIS integration technical documentation for bank-operators | Bank | P2 |
| No public operator registry | Operator | P2 |
| No OpenAPI spec in `contracts/` | Developer | P1 |
| No merchant directory (public listing) | Merchant | P1 |
| No systemic risk documentation | Regulator | P2 |
| No investor relations narrative | Investor | P2 |

---

## Adoption Success Metrics

### Phase 1 success (H2 2026)

| Metric | Target |
|--------|--------|
| `@banza/sdk` published on npm | ✓ / ✗ |
| Banzami Business mobile app on Play Store | ✓ / ✗ |
| Merchant pricing page published | ✓ / ✗ |
| Self-service sandbox key issuance live | ✓ / ✗ |
| BNA briefing conducted | ✓ / ✗ |
| Regulatory alignment document published | ✓ / ✗ |
| 10 merchants publicly listed | ✓ / ✗ |
| Developer quick-start guide published | ✓ / ✗ |

### Phase 2 success (H1 2027)

| Metric | Target |
|--------|--------|
| Conformance suite v1 publicly executable | ✓ / ✗ |
| First external operator at L1 certification | ✓ / ✗ |
| Public operator registry live | ✓ / ✗ |
| 1,000 active consumer wallets | ✓ / ✗ |
| 50+ merchants accepting Banzami QR | ✓ / ✗ |
| Public metrics dashboard live | ✓ / ✗ |

### Phase 3 success (H2 2027)

| Metric | Target |
|--------|--------|
| Two operators in federation pilot | ✓ / ✗ |
| BNA formal acknowledgment | ✓ / ✗ |
| 10,000 active consumer wallets | ✓ / ✗ |
| 100+ merchants | ✓ / ✗ |
| Independent compliance audit published | ✓ / ✗ |
| Governance independence roadmap published | ✓ / ✗ |

---

## The Adoption Narrative Arc

Each audience needs a different version of the same argument:

### For Developers
> "Accept payments in Angola in 15 minutes. `npm install @banza/sdk`. Sandbox. No bank negotiations."

### For Merchants
> "Print a QR. Accept instant Kwanza. No terminal. No contract. No WhatsApp proof."

### For Operators
> "Build a certified payment operator. Read the spec. Run the conformance suite. No bilateral agreements."

### For Regulators
> "Open protocol. Verifiable invariants. Auditability by code, not by contract. We want to build this with BNA."

### For Investors
> "The protocol layer Angola never had — and the only team building it. Infrastructure play. Protocol economics. First mover."

### For Banks
> "Your settlement rails power us. Certify as an operator and own the product layer too. Interoperability without bilateral negotiations."

The technology is built. The narrative must now be placed where each audience will find it.

---

## Reference Documents

This roadmap was produced based on the following audience-specific analyses:

- [BANZA_OPERATOR_ADOPTION_REPORT.md](BANZA_OPERATOR_ADOPTION_REPORT.md)
- [BANZA_DEVELOPER_ADOPTION_REPORT.md](BANZA_DEVELOPER_ADOPTION_REPORT.md)
- [BANZA_REGULATOR_ADOPTION_REPORT.md](BANZA_REGULATOR_ADOPTION_REPORT.md)
- [BANZA_MERCHANT_ADOPTION_REPORT.md](BANZA_MERCHANT_ADOPTION_REPORT.md)

**Canonical protocol reference:** [BANZA_REFERENCE.md](../BANZA_REFERENCE.md)

---

*Produced by: BANZA-ADOPTION-ARCHITECTURE-001 — 2026-05-30*
