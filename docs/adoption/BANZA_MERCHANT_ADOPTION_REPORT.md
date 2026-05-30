---
name: banza-merchant-adoption-report
description: Adoption audit for the Merchant and Investor audiences — what merchants need to adopt BANZA payments, what investors need to believe in the protocol, and what gaps exist
metadata:
  type: project
---

# BANZA — Merchant & Investor Adoption Report

**Mission:** BANZA-ADOPTION-ARCHITECTURE-001  
**Audiences:** Merchants (primary) + Investors and Banks (secondary, included here to preserve coherence with the five-audience structure)  
**Date:** 2026-05-30  
**Status:** Official

---

## Part I — Merchants

---

## Who is the Merchant Audience

Merchants span a wide range in the Angolan economy:

| Tier | Profile | Payment reality today |
|------|---------|----------------------|
| **Tier 1: Informal micro-merchant** | Cantina, market vendor, ambulant seller, domestic services | Cash only. No bank terminal. No digital option. |
| **Tier 2: Small formal business** | Restaurant, barbershop, small retailer, school | Cash dominant. Some accept Multicaixa, some accept bank transfer with WhatsApp proof. |
| **Tier 3: Medium business** | Supermarket, pharmacy, gas station, hotel | Multicaixa terminal. Limited digital experience. Long settlement cycles. |
| **Tier 4: Digital business** | Ecommerce platform, delivery app, subscription service, SaaS | Integrated with one bank. Non-standard checkout. High integration cost for payment changes. |
| **Tier 5: Enterprise / utility** | Electricity (ENDE), water (EPAL), telecoms | Large billing volumes. Slow integration cycles. High cost of payment infrastructure. |

The BANZA/Banzami commercial strategy targets Tiers 1–4 with differentiated approaches. Tier 1 is the volume base (QR), Tier 4 is the SDK integration lever.

---

## What Merchants Gain

### Tier 1–2: Zero-hardware QR acceptance

A merchant prints a static QR once. Any consumer with the Banzami Wallet scans it and pays instantly. There is no terminal, no contract with a bank, no monthly hardware fee, no EDC machine, no merchant ID approval queue.

```
Print QR → Consumer scans → Merchant sees notification → Done
```

Settlement is T+0 — the merchant wallet is credited immediately, not in a 2–5 day batch cycle.

### Tier 3–4: Operational dashboard

The Banzami Business dashboard provides:
- Real-time transaction view
- Revenue analytics (daily, weekly, monthly)
- Withdrawal management to bank account
- Dispute and refund management
- Webhook endpoint configuration
- API key management (sandbox + live)

This is infrastructure that currently requires either building in-house or paying a third-party analytics layer.

### Tier 4: SDK integration

A taxi app, delivery platform, or ecommerce site integrates `@banza/sdk` and accepts in-app Kwanza payments natively — without redirecting to a bank checkout, without asking users for card numbers, without managing a complex payment gateway relationship.

```typescript
// Accept payment in a taxi app
const payment = await banza.payments.create({
  amount_minor: 3500, // 35 Kz
  merchant_id: 'mch_taxify_angola',
  reference: `ride_${rideId}`,
  qr_type: 'dynamic',
});
```

### All tiers: No WhatsApp proof-of-payment

Every BANZA transaction has a `trace_id`. The merchant sees a confirmed payment notification in real time. The consumer sees an immediate success confirmation. Neither party sends a screenshot to the other. This is a behavioral transformation, not just a technical upgrade.

---

## What Merchants Fear

### Fear 1: "I won't know if the payment actually went through"

Cash is trusted because it's physical. Bank transfers are verified because the bank confirms. A new QR payment system introduces doubt: did the money really arrive? What if the scan appeared to work but the payment was declined?

**Current gap:** The real-time confirmation model (merchant sees wallet credit instantly) is correct architecturally, but the merchant UX for this confirmation is not fully described in public-facing materials. A merchant deciding whether to adopt does not have a clear picture of what the confirmation experience looks like from their side.

**What is needed:** A merchant-facing "How payment confirmation works" one-pager — showing the exact sequence: consumer scans → merchant app notification → bank account (on withdrawal) — with screenshots or wireframes of the real experience.

### Fear 2: "What if there's a dispute?"

A consumer pays via QR, then claims they were charged incorrectly, or the product was not delivered, or they want a refund. Under cash, the merchant handles this directly. Under a payment protocol, who arbitrates? What is the refund process? How long does it take?

**Current gap:** Banzami Business includes dispute management. The Banzami SDK includes refund API endpoints. But there is no merchant-facing documentation of the dispute lifecycle — how to initiate a refund, what the resolution timeline is, what the outcomes are.

**What is needed:** A merchant dispute and refund guide — covering: how to issue a full or partial refund, how to respond to a consumer dispute, what happens if a refund is requested after settlement.

### Fear 3: "What are the fees?"

Merchant adoption decisions depend on fee transparency. A merchant considering Banzami vs. Multicaixa vs. cash needs to know: what percentage does Banzami take? Are there monthly fees? Are there withdrawal fees?

**Current gap:** Merchant pricing is not documented anywhere in the public protocol or operator documents. BANZAMI_PRODUCTS.md describes features but not pricing.

**What is needed:** A merchant pricing page — even if it is "get a quote" for enterprise and transparent fee tiers for smaller merchants. The absence of visible pricing creates distrust.

### Fear 4: "Nobody else uses it"

Merchant adoption depends on consumer adoption. A merchant who installs Banzami QR will only keep it if consumers are using it to pay. If the consumer base is zero, the merchant has no reason to adopt. This is the classic two-sided marketplace chicken-and-egg problem.

**Current gap:** There are no published consumer adoption metrics. There is no merchant adoption map (where can I use Banzami to pay? what merchants accept it?). The protocol documents describe architecture but not market traction.

**What is needed:**
1. A public merchant directory ("Merchants that accept Banzami") — even if it starts with 10 merchants.
2. Published transaction volume numbers (even approximate) — that show the network is real and growing.
3. A consumer-facing campaign that drives Banzami Wallet downloads before or alongside merchant onboarding.

### Fear 5: "Setup is too complex for my business"

For a Tier 1 informal merchant, "setup" means printing a piece of paper and having someone explain what to do when a customer scans it. For a Tier 4 digital business, "setup" means API integration. Neither audience should be asked to read protocol documentation.

**Current gap:** There is no merchant-specific onboarding guide. The public documentation is developer-oriented and protocol-heavy. A cantina owner and an ecommerce CTO have radically different setup paths that are not yet differentiated in any documentation.

**What is needed:** Two separate onboarding experiences:
1. **"Start accepting payments today"** — a physical-first guide for informal merchants: download the app, register, show the QR, get paid. No code, no technical concepts.
2. **"Integrate in your platform"** — the developer-focused SDK integration path (covered in the Developer report).

---

## What Information is Missing

| Missing Information | Where it Belongs | Priority |
|--------------------|-----------------|----------|
| Merchant pricing (fees, tiers, withdrawal costs) | New merchant pricing page / BANZAMI_PRODUCTS.md | CRITICAL |
| Confirmation UX description (what the merchant sees) | Merchant onboarding guide | HIGH |
| Dispute and refund guide | New `docs/merchant/disputes.md` | HIGH |
| Non-technical merchant onboarding guide | New `docs/merchant/get-started.md` | HIGH |
| Settlement timeline explanation (when does money reach bank?) | Merchant FAQ / BANZAMI_PRODUCTS.md | HIGH |
| Merchant directory (public, even small-scale) | banzami.com/merchants | MEDIUM |
| Published transaction volume (network size signal) | banzami.com / press section | MEDIUM |
| Customer support contact for merchants | BANZAMI_PRODUCTS.md | MEDIUM |

---

## What Proof is Missing (Merchant)

| Missing Proof | Priority |
|--------------|----------|
| First 10 merchants publicly listed | HIGH |
| First 100 QR payments processed (documented publicly) | HIGH |
| A merchant testimonial (video or written) | MEDIUM |
| Published volume metric (e.g., "X Kz processed in sandbox") | MEDIUM |

---

## What Tools are Missing (Merchant)

| Missing Tool | Priority |
|-------------|----------|
| **Merchant mobile app (production)** | Banzami Business mobile (Flutter) — currently the most important product gap for Tier 1–2 merchants | CRITICAL |
| **Static QR print flow** | A merchant can generate and print their QR from the app in 2 taps | HIGH |
| **Instant payment notification** | Push notification to merchant on every payment received | HIGH |
| **Payment link generator** | Create a link with one tap, share via WhatsApp | HIGH |
| **Merchant onboarding KYC flow** | Streamlined digital KYC for merchant registration | HIGH |

---

---

## Part II — Investors

---

## Who is the Investor Audience

The investor audience for BANZA/Banzami includes:

| Type | Profile |
|------|---------|
| **Angolan institutional investors** | Local banks (BAI, BFA, BPC) with fintech investment arms; sovereign wealth (Sonangol) |
| **African PE/VC** | Partech, TLcom, Helios, Novastar — funds with Angola exposure |
| **DFIs** | IFC, AfDB, Proparco — development finance interested in payment infrastructure |
| **Strategic investors** | Telecoms (Unitel), regional payment networks, tech platforms |
| **International VC** | Funds investing in African fintech infrastructure plays |

---

## What Investors Gain

### Infrastructure defensibility

BANZA is an open protocol, not a product. Products are competed away. Protocols are adopted into infrastructure and become very difficult to dislodge. If BANZA becomes the payment protocol for Angola, the defensibility is at the protocol layer, not the product layer.

The comparable case: Visa and Mastercard did not win because of better products — they won because their protocols became infrastructure. BANZA is building for that position in Angola first.

### First-mover in an underpenetrated market

Angola has 16 million mobile phone users, a large informal economy, and no existing payment protocol layer. The digital payment penetration is low. Whoever builds the protocol layer — and builds it right — captures the infrastructure rent of an entire country's digital payment transition.

### Protocol economics: operator fees at scale

As more operators certify, BANZA's economic model includes:
- Certification fees
- Protocol usage fees (per-transaction royalty or license model — not yet defined)
- BanzAI API access fees (operator subscriptions for protocol intelligence)
- Developer ecosystem fees

This is not a single operator's revenue model. It is a protocol layer's revenue model — potentially more durable and scalable.

### Open protocol = regulatory alignment

National regulators (BNA) are more likely to endorse an open protocol than a single company's product. BANZA's open architecture is a structural advantage in regulatory negotiations, not a weakness.

---

## What Investors Fear

### Fear 1: Regulatory risk

Is BANZA operating within Angolan law? If BNA decides to shut down or heavily restrict non-bank payment operators, what happens to the protocol?

**Current gap:** No published regulatory engagement history. No BNA endorsement or acknowledgment. No published legal opinion on the regulatory status of BANZA operators.

### Fear 2: Adoption velocity

Is the network growing? How many merchants? How many consumers? What is the transaction volume? Without public metrics, investors are evaluating a protocol with no traction data.

**Current gap:** No public dashboard. No investor relations section. No traction documentation.

### Fear 3: Team execution

Can the team execute the certification framework, attract operators, and build the consumer network — all simultaneously, in the Angolan market, with local infrastructure constraints?

**Current gap:** No public team page. No track record of protocol-layer infrastructure at this scale in Angola.

### Fear 4: Protocol governance is not independent

If Banzami controls both the protocol governance and the reference operator, an investor evaluating the "open protocol" thesis must evaluate the commitment to genuine openness.

**Current gap:** No independent governance body. No published commitment to spinning out protocol governance.

---

## What Investors Need That is Missing

| Missing | Priority |
|---------|----------|
| Public traction metrics (consumers, merchants, volume) | CRITICAL |
| Regulatory status memo / BNA engagement evidence | CRITICAL |
| Economic model for protocol layer (certification + API fees) | HIGH |
| Roadmap to governance independence | HIGH |
| Team and track record page | HIGH |
| DFI / strategic investor pipeline visibility | MEDIUM |

---

## Part III — Banks

---

## Who is the Bank Audience

Angola's 23 licensed banks include BFA, BAI, BPC, Banco Económico, BCI, and others. Banks are simultaneously:

- **Potential infrastructure partners** (EMIS rails, settlement accounts for operators)
- **Potential operator candidates** (a bank that builds a BANZA-certified wallet layer for its customers)
- **Potential competitive threats** (if a bank views BANZA as disintermediation)

The BANZA narrative must address all three positions simultaneously.

---

## What Banks Gain

### Settlement infrastructure relationship

BANZA operators settle via EMIS and bank settlement accounts. Banks are a required component of the payment flow — not bypassed by it. Every BANZA consumer wallet has a funding path through a bank. Every merchant payout route ends at a bank.

### New digital distribution channel

A bank that certifies as a BANZA operator gains the ability to offer QR-native wallet services to its customers with protocol-grade reliability — without building the entire infrastructure from scratch. The Banzami reference implementation is available. The conformance suite certifies the implementation. The bank's engineering team builds the product layer.

### Interoperability without bilateral agreements

Currently, bank A cannot directly interoperate with bank B's mobile wallet. BANZA federation provides a protocol-level answer: two certified operators can route payments without negotiating a bilateral commercial agreement.

---

## What Banks Fear

### Disintermediation

If consumers use BANZA wallets instead of bank accounts for everyday payments, banks lose transaction fee revenue and lose data about consumer payment behavior. This is a legitimate structural concern.

**Answer:** BANZA wallets are funded through banks. Settlement goes through banks. The protocol increases payment volume — which increases the total transaction base, including bank-intermediated flows. BANZA is a volume amplifier for the banking system, not a bypass.

### Loss of data and relationship

Banks value the relationship with depositors. A BANZA wallet operator owns the consumer relationship at the product layer, not the bank.

**Answer for banks as operators:** Banks can certify as BANZA operators. A bank that operates a certified BANZA wallet owns the consumer relationship AND is the wallet operator. The protocol enables banks to compete at the product layer, not just the rails layer.

---

## What Banks Need That is Missing

| Missing | Priority |
|---------|----------|
| "Banks as BANZA operators" positioning document | HIGH |
| EMIS integration technical documentation | HIGH |
| Clear description of how wallet funding and settlement works with existing bank accounts | HIGH |
| Commercial model for bank-as-operator | MEDIUM |
| Data sharing and privacy model (what operators can and cannot do with consumer data) | MEDIUM |

---

*Part of BANZA-ADOPTION-ARCHITECTURE-001 — 2026-05-30*
