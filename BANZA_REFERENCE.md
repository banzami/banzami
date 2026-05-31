# BANZA — Protocol Reference

**Version:** 1.0  
**Date:** 2026-06-01  
**Status:** Official  
**Authority:** ADR-025, ADR-026, ADR-028, ADR-029

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Why BANZA Exists](#2-why-banza-exists)
3. [Core Principles](#3-core-principles)
4. [Certification](#4-certification)
5. [Federation](#5-federation)
6. [Trust](#6-trust)
7. [BanzAI](#7-banzai)
8. [Operators](#8-operators)
9. [Developer Resources](#9-developer-resources)
10. [Governance](#10-governance)
11. [Roadmap](#11-roadmap)
12. [FAQ](#12-faq)

---

## 1. Introduction

**BANZA is the open financial infrastructure protocol for Angola** — the rules, contracts, and certification framework that any operator can implement to process payments, and that any operator can use to exchange payments with any other operator.

BANZA is not a bank. Not a product. Not an API. It is the protocol layer beneath all of those: the set of open rules that make interoperability possible without bilateral agreements.

### The Four Protocol Properties

| Property | What the protocol guarantees |
|----------|------------------------------|
| **Public rules** | The specification — RFCs, ADRs, conformance suite — is publicly available. No documentation is behind an NDA. |
| **Open certification** | Any legal entity that passes the conformance suite becomes a certified BANZA operator. No institutional approval required. No bilateral agreement. |
| **Verifiable invariants** | Financial properties are enforced by the Rust kernel and verifiable by any independent auditor. Instant settlement is not a contractual promise — it is a kernel invariant. |
| **Federation** | Certified operators can route payments between each other without bilateral agreements, because both implement the same open protocol. |

### Ecosystem Hierarchy

```
BANZA    = open financial infrastructure protocol        ← THIS DOCUMENT
BanzAI   = Protocol Operating System
Operators = certified entities that implement the protocol
```

The dependency runs in one direction only: operators depend on BANZA; BANZA never depends on any operator.

### Scope of This Document

This document defines the BANZA open financial infrastructure protocol — its rules, invariants, governance, certification, and federation model. It is the primary source for the `banza.network` website and the onboarding reference for operators, developers, and regulators.

For the BanzAI Protocol OS: see `BANZAI_REFERENCE.md`.

---

## 2. Why BANZA Exists

### The Problem

Angola has banks — twenty-three licensed financial institutions. A national interbank settlement system: EMIS. ATM networks. Homebanking apps. Multicaixa. Sixteen million people with a mobile phone.

Angola has the pieces. What Angola does not have is the layer that connects them.

To integrate payments, a company must establish a bilateral agreement with a bank. The process takes months. Documentation is private. Terms are negotiated case by case. Access is discretionary — there is no set of public rules that any entity can read and implement.

For a fintech to process payments independently, it must become a bank. For wallets on different operators to communicate with each other, no mechanism exists — each network is closed.

The symptoms are visible:

- **WhatsApp receipts.** Screenshots of bank transfers as proof of payment — because no protocol-guaranteed alternative exists.
- **Closed integrations.** A company integrates with one bank's system. That integration does not work with any other bank.
- **Small business exclusion.** A POS terminal requires an acquiring contract, hardware, and monthly fees.
- **Proprietary network dependency.** Each platform runs on its own rules. An operator can change fees, disable features, or shut down without warning.

The root cause: Angola has settlement rails — EMIS moves money between banks. EMIS does not resolve who can access the payment system, under what conditions, and according to what verifiable rules.

This layer has a name: **the protocol layer**. That is the gap BANZA fills. Not as a bank. Not as a fintech product. As a protocol.

### Two Models

**The closed model: M-Pesa**

M-Pesa belongs to Safaricom. The rules are the operator's rules. When Safaricom changes prices, all users are subject. When it exits a country, the service exits. A startup building on M-Pesa must accept whatever terms the operator decides.

M-Pesa is a remarkable product. But it is a product — not a protocol. The network belongs to the operator.

**The open model: Pix and UPI**

The Central Bank of Brazil did not create a product — it created a protocol. Nubank implements Pix. Itaú implements Pix. Google Pay implements Pix. Hundreds of entities implement Pix — each with its own product, experience, and business model — but all under the same open rules. None of them owns Pix.

In under two years, Pix became the most widely used payment method in Brazil.

India followed the same model with UPI in 2016. By 2024, UPI was processing over 15 billion transactions per month.

| | M-Pesa | Pix / UPI | BANZA |
|---|---|---|---|
| **Who defines the rules** | The operator | Governance entity | Open protocol (RFCs + ADRs) |
| **Who can participate** | Entities with operator agreement | Any certified entity | Any certified entity |
| **Can a third party become an independent operator?** | No | Yes | Yes |

### The Disappearing Operator Test

This is the definitive test.

In the closed model: if the primary operator disappears, the system disappears.

In the open model: if one operator disappears, the others continue. Pix does not belong to Nubank. If Nubank disappeared tomorrow, Pix would continue.

**BANZA follows the open model.**

The BANZA protocol rules are public. The reference operator is the first certified operator and the reference implementation — but it does not own the protocol. If every current operator disappeared tomorrow, the protocol rules, specification, and conformance suite would continue to exist. Other certified operators would continue to operate. The infrastructure would remain.

This is not an accidental property. It is a deliberate architectural decision.

---

## 3. Core Principles

### Financial correctness is non-negotiable

Every engineering decision is evaluated against: "Does this preserve financial correctness?" Operational simplicity and auditability take precedence over convenience. A payment that cannot be fully audited by an independent party is not a valid payment under BANZA.

### The protocol is the product

Operators prove the protocol works. They are not the protocol. The reference operator is the reference implementation — it demonstrates every protocol capability. But it does not own the protocol any more than Nubank owns Pix. The protocol is what scales. Operators are what demonstrate it.

### The kernel implements the protocol. Operators implement policy.

The BANZA kernel enforces financial invariants. Operators apply their own business policies within the constraints the kernel imposes. These two layers never collapse. An operator cannot override a kernel invariant; the kernel never encodes an operator's business logic.

### Traceability by default

Every financial event carries a `trace_id`. Every causal chain is reconstructible. No money moves without a ledger entry. No ledger entry is ever modified. Any auditor — independent of any operator — can reconstruct any payment from its `trace_id` alone.

### Open access

Certification is determined by the conformance suite — not by institutional access, not by bilateral agreements, not by minimum transaction volumes. Any legal entity that passes the suite becomes a certified BANZA operator.

### Protocol independence

The protocol exists independently of any operator. No single operator can shut it down, modify its rules, or restrict access to it. The specification, the conformance suite, and the certification framework remain available to all operators regardless of what any individual operator does.

---

## 4. Certification

### Why Certification Exists

Open protocols require open verification. Any entity claiming to implement BANZA must be able to prove it. The conformance suite is that proof — a set of deterministic tests that any operator must pass to receive a BANZA certificate. No conformance, no certification. No exceptions.

### Certification Levels

| Level | Name | What it certifies |
|-------|------|-------------------|
| **L0** | Sandbox Operator | Sandbox environment operational; basic wallet and transfer operations |
| **L1** | Payment Operator | Consumer wallets, static QR, P2P transfers, merchant wallets |
| **L2** | Settlement Operator | All L1 + dynamic QR, payment links, instant (T+0) settlement |
| **L3** | Federation Operator | All L2 + cross-operator routing, reconciliation, bank-rail payouts, valid BANZA certificate, BRL compliance |
| **L4** | Infrastructure Operator | All L3 + EMIS card acquiring (`acquiring.emis`) |

Each level is cumulative. L3 requires everything in L2, which requires everything in L1.

**L3 — Federation Operator — full requirements:**
- Valid BANZA-signed operator certificate at `/.well-known/banza/certificate.json`
- Certificate lifetime: 90 days maximum (INV-TRUST-002)
- Operator not present in the BANZA Revocation List (BRL)
- `supports_federation: true` declared in operator manifest (INV-TRUST-004)
- `POST /federation/route` endpoint operational
- `GET /federation/obligations` endpoint operational
- Certificate `issuer_key_id` must appear in the published BANZA Key Manifest (INV-TRUST-006)
- Federation conformance suite: 79 tests across 9 suites (FED-CERT through FED-FAIL)

**L4 note:** The L4 conformance suite (card acquiring) is defined and will be available in Protocol v1.1. L4 is defined but not yet certifiable in v1.0.

### The Open Access Principle

Certification access is defined by the protocol rules alone. There is no institutional approval process. No bilateral agreement with BANZA. No minimum transaction volume. Any legal entity that:
1. Implements the required capabilities
2. Passes the conformance suite for its target level
3. Submits the conformance results

becomes a certified BANZA operator.

### How to Get Certified

1. **Prepare your manifest.** Create a valid Operator Manifest declaring your certification level and capabilities. Use the BanzAI Manifest Validator to verify it passes structural validation.
2. **Implement the capabilities.** Build your operator against the protocol specification and SDK. See [Developer Resources](#9-developer-resources).
3. **Run the conformance suite.** Run all required tests for your target level. All tests must pass — a single failure blocks certification.
   ```bash
   python3 tools/banza-conformance/run.py --url https://your-operator.example --level 2
   ```
4. **Submit your results.** Send your conformance results and manifest to BANZA.
5. **BANZA review.** BANZA verifies conformance result authenticity, manifest consistency, and invariant status. Review completes within 5 business days.
6. **Certificate issued.** On approval: signed certificate artifact, certification badge, live API keys, registry listing.

### Operator Manifest

The operator manifest declares capabilities and certification level. It must be served at `/.well-known/banza/operator.json`.

```json
{
  "operator_id": "your-operator-id",
  "protocol_version": "1.0",
  "certification_level": 2,
  "environment": "production",
  "capabilities": {
    "supports_wallets": true,
    "supports_qr": true,
    "supports_payment_requests": true,
    "supports_traces": true,
    "supports_settlement": true
  }
}
```

### Certification Maintenance

- Certifications expire after 12 months without re-verification
- Protocol major version updates require re-certification
- Automated invariant spot-checks: monthly
- Conformance spot-checks: quarterly
- L3+ certificates expire after 90 days (must be renewed)

### BanzAI and Certification

BanzAI can guide you through the certification process: analyze your manifest, simulate conformance runs, identify gaps, and generate a certification readiness score. BanzAI does not grant certification. The conformance suite is the arbiter — deterministic tests, not AI inference. See [BanzAI](#7-banzai).

---

## 5. Federation

### Why Federation Exists

Without federation, each operator is an island.

A customer with a wallet on Operator A can pay merchants on Operator A. That is all. A merchant on Operator B is out of reach — unless Operator A and Operator B negotiate a bilateral agreement, case by case, outside the protocol.

This is not a technical limitation. It is a trust limitation. Operator A has no way to know, verifiably, that Operator B is a legitimate network participant. Without verifiable trust, there is no secure routing.

Federation solves this at the protocol level — without bilateral agreements, without intermediaries, without negotiation. Trust is proven by certificates issued by BANZA. Routing follows protocol contracts. Settlement is executed by open rules.

### Before Federation

```
Customer A               Customer B
    ↓                        ↓
Operator A               Operator B
(closed network)         (closed network)

Customer A cannot pay Merchant B.
Merchant B cannot receive from Customer A.
```

Two certified operators. Two isolated networks. No connection between them.

### With Federation

```
Customer A                              Merchant B
    ↓                                       ↑
Operator A  ←—— BANZA protocol ——→  Operator B
    ↓                                       ↑
  (debits                            (credits
  Customer A)                       Merchant B)

The payment crosses the operator boundary.
Protocol guarantees apply across the entire chain.
```

A customer on any operator can pay a merchant on any operator. Every new certified operator that joins the network makes all others more useful.

### How Federation Works

Federation occurs in five distinct moments:

**1. Trust**

Before any payment, Operator A verifies that Operator B is a legitimate BANZA network participant. This verification is cryptographic — it does not require a real-time call to BANZA.

BANZA issues a certificate to each certified operator. The certificate is signed with BANZA's key and states: "This operator was certified at level X, with these capabilities, valid until this date." Any operator can verify any certificate without contacting BANZA.

BANZA maintains a Revocation List (BRL — BANZA Revocation List), published every six hours. Before routing a payment, Operator A verifies that Operator B is not revoked or suspended.

Trust is always bidirectional: Operator B also verifies Operator A before accepting a routing request.

**2. Routing**

Operator A sends a routing request to Operator B, signed with its private key:

```
"I want to route a payment of 5,000 AOA from Customer A to Merchant B."
```

The request includes the unique transaction identifier (`trace_id`) that will be shared by all payment artifacts across both operators.

**3. Acceptance and Execution**

When Operator B accepts the request, the payment executes at that exact moment. Acceptance and execution are simultaneous — not two separate steps.

At the instant Operator B responds "accepted", Merchant B's wallet has already been credited. Merchant B receives the funds immediately.

**4. Obligation**

Operator A receives the acceptance confirmation and, atomically (in a single database operation), does two things:
- Debits Customer A's wallet
- Records an obligation: "Operator A owes 5,000 AOA to Operator B"

The obligation is signed by Operator A. It is non-repudiable. Operator A cannot later deny owing Operator B.

**5. Settlement**

Obligations accumulate over a compensation cycle (typically 24 hours). At the end of the cycle, both operators independently calculate the net position:

```
Operator A owes Operator B:  150,000 AOA  (multiple payments)
Operator B owes Operator A:   40,000 AOA  (reverse-direction payments)
────────────────────────────────────────
Net position:                 110,000 AOA  (Operator A owes Operator B)
```

A single bank transfer settles all payments in the cycle. Not one transfer per payment — one per cycle. Settlement efficiency scales with volume.

### Step-by-Step Example

**Situation:** Customer Ana has a wallet on Operator A. Merchant Bento has a wallet on Operator B. Ana wants to pay Bento 2,000 AOA.

```
1. Ana initiates the payment in Operator A's app.
   → Operator A identifies that Bento is on Operator B.

2. Operator A verifies Operator B's certificate.
   → Certificate valid. Operator B not revoked.
   → Operator B is a legitimate BANZA network member.

3. Operator A sends a routing request to Operator B (signed):
   "Request rr-abc: pay 2,000 AOA to Bento (trace: tr-xyz)"

4. Operator B verifies Operator A's certificate (bidirectional trust).
   → Identifies Bento's wallet. Wallet active.
   → Credits 2,000 AOA to Bento's wallet.
   → Responds: "Accepted. Transfer ID: itx-def"

5. Operator A receives confirmation (atomic operation):
   → Debits 2,000 AOA from Ana's wallet.
   → Records obligation: "Operator A owes 2,000 AOA to Operator B (rr-abc)"

6. Bento receives payment notification. Balance up 2,000 AOA.
   Ana receives confirmation. Balance down 2,000 AOA.

7. At end of 24-hour cycle:
   → Both operators independently calculate bilateral net position.
   → Operator A executes a single bank transfer to Operator B.
   → All cycle obligations marked as settled.
```

Throughout the entire chain, the same `trace_id` (tr-xyz) appears on every artifact: the routing request, the response, the obligation, the ledger entries on both operators, and all emitted events. Any auditor can reconstruct the complete cross-operator payment from the `trace_id` — on both operators — without the cooperation of either.

### Obligations

An obligation is the formal record that one operator owes money to another.

When Operator B accepts a routing payment, it assumes a risk: it has credited the merchant but has not yet received the funds. Operator A's obligation — cryptographically signed — is the commitment that the payment will be settled.

Obligations have a lifecycle:

```
pending → in-compensation → settled
```

An obligation cannot transition from "settled" to "pending". Immutability is a protocol property, not a database property of any individual operator.

The fundamental invariant: the amount in the obligation always equals the amount in the routing request. No fees, no discounts, no rounding are applied within the inter-operator transfer amount. Fees are separate ledger entries.

### Compensation (Netting)

Compensation is the process by which operators calculate and settle net positions at the end of each cycle.

Without netting, every payment would require an immediate bank transfer. With bilateral netting, hundreds of opposing payments collapse into a single transfer.

```
Example 24-hour cycle between Operator A and Operator B:

  Operator A → Operator B:  842 payments  →  4,210,000 AOA gross
  Operator B → Operator A:  318 payments  →  1,590,000 AOA gross
  ──────────────────────────────────────────────────────────────
  Net position:                            →  2,620,000 AOA
  Bank transfers executed:                 →  1 (not 1,160)
```

Netting is always bilateral and independent: each operator calculates the net position autonomously. Both must arrive at the same result before any transfer executes. If they diverge, settlement is suspended until the discrepancy is identified and resolved.

### Why Federation Matters

**For merchants:** A certified merchant on any one operator can receive payments from customers on any other operator. No multiple networks, no multiple agreements. One wallet, full network reach.

**For customers:** A customer can pay any merchant on any certified operator using only their own operator's app. The fragmentation where App A only works with merchants using App A is gone.

**For operators:** Each new certified operator that joins the network makes all others more valuable. An operator with 100,000 customers that joins a network with a 500,000-customer partner does not add 600,000 to the network — it multiplies the payment capability of everyone. This is Metcalfe's law: network value grows with the square of its participants.

**For regulators:** Federation is auditable by design. The `trace_id` of any cross-operator payment exists on both operators, on all artifacts: routing request, obligation, ledger entries, events. A regulator can reconstruct any federated payment in full — on both operators — without the cooperation of either operator.

**For investors and banks:** Federation transforms BANZA from a set of isolated operators into a unified payment network. The value of the network belongs to the protocol — not to any single operator. Each operator that joins increases the value of all others. This growth model is structurally different from the proprietary model where value is captured by the dominant operator.

### Federation Status

The federation specification was completed and verified in 2026. It is not a future feature.

| Item | Status |
|------|--------|
| Architecture specification (ADR-026) | COMPLETE |
| Federation contracts (5 schemas) | COMPLETE |
| Federation invariants (18: INV-TRUST-*, INV-FED-*) | COMPLETE |
| Conformance suite (79 tests, 9 suites: FED-CERT through FED-FAIL) | COMPLETE |
| Two-operator interoperability verification (14/14 scenarios) | COMPLETE |
| M1 Protocol Complete | ACHIEVED — 2026-06-01 |
| First production operator federated (M3) | Pending M2 |

Federation is ready. The remaining work is operational: completing the root key ceremony (M2), certifying the first production operator (M3).

---

## 6. Trust

### Why Trust Infrastructure Exists

Operators in the federation verify each other's certificates. This verification must be:
- **Cryptographic** — not based on a phone call or email
- **Offline** — not requiring a real-time call to BANZA on every payment
- **Unforgeable** — a certificate must be impossible to fabricate without BANZA's private key

This requires a trust hierarchy with a root of trust that every operator pins once and uses to verify all subsequent certificates.

### The Trust Hierarchy

```
BANZA Root Key (offline, ed25519, 24-month validity)
    │
    │  signs Key Manifests only
    ▼
Key Manifest (published at banza.network/.well-known/banza/key-manifest.json)
    │
    │  lists three active issuing keys
    │
    ├── Cert-Issuing Key (banza-cert-YYYYMM)    → signs operator certificates
    ├── BRL-Issuing Key  (banza-brl-YYYYMM)     → signs BANZA Revocation Lists
    └── Evidence-Issuing Key (banza-evidence-YYYYMM) → signs conformance evidence
```

**The root key signs only Key Manifests** — it never directly signs certificates, BRLs, or evidence. This limits the blast radius if an issuing key is ever compromised: only the Key Manifest (the root key's single product) is authoritative.

### The Key Manifest

The Key Manifest is a signed JSON document listing all active BANZA issuing keys. It is published at:

```
https://banza.network/.well-known/banza/key-manifest.json
```

It is signed by the root key. Any operator can verify its authenticity using the root public key, which SDKs pin at release time.

The Key Manifest contains:
- `root_key_id` — identity of the root key that signed this manifest
- `root_public_key` — root public key (ed25519, base64url)
- `expires_at` — manifest expiry (24 months from issuance)
- `manifest_signature` — ed25519 signature over the canonical JSON
- `keys` — array of active issuing keys, each with `key_id`, `domain` (certification / revocation / conformance-evidence), `public_key`, `active_since`, `expires_at`, `status`

SDKs pin the Key Manifest at release time. An expired Key Manifest causes the SDK to reject all certificates until the manifest is refreshed.

### Operator Certificates

Each certified operator is issued a certificate signed by the cert-issuing key. Operators serve their certificate at:

```
/.well-known/banza/certificate.json
```

A certificate contains:
- `operator_id` — must match the `operator_id` in the operator manifest
- `certification_level` — the certified level (0–4)
- `issuer_key_id` — the cert-issuing key that signed this certificate
- `issued_at`, `expires_at` — certificate lifetime (maximum 90 days for L3+)
- `signature` — ed25519 over the canonical JSON

Any peer operator can verify a certificate without contacting BANZA:
1. Fetch the certificate from the target operator's `/.well-known/banza/certificate.json`
2. Fetch the Key Manifest from `banza.network/.well-known/banza/key-manifest.json`
3. Verify that `issuer_key_id` appears in the Key Manifest and is active
4. Verify the certificate signature with the issuing key's public key
5. Verify the operator is not in the current BRL

### The BRL — BANZA Revocation List

The BRL is a signed list of revoked or suspended operator certificates. It is published at:

```
https://banza.network/federation/revocation-list.json
```

Updated every 6 hours. Signed by the BRL-issuing key.

Before routing any federated payment, the sending operator must verify that the receiving operator is not in the current BRL. An operator on the BRL cannot receive routed payments from any other operator, regardless of certificate validity.

### Root Key Invariants (in plain language)

| Invariant | What it means |
|-----------|---------------|
| INV-ROOT-001 | Production key IDs must not start with `test-`. Test keys are rejected in production. |
| INV-ROOT-002 | The Key Manifest must be root-signed. An unsigned manifest is invalid. |
| INV-ROOT-003 | An expired Key Manifest is invalid. SDKs must detect and reject stale manifests. |
| INV-ROOT-004 | The root key signs only Key Manifests. It never signs certificates or BRLs directly. |
| INV-ROOT-005 | The BRL must be signed by the designated BRL-issuing key. |
| INV-ROOT-006 | Issuing keys have a maximum validity of 184 days. The root key has a maximum validity of 24 months. |

### The Root Key Ceremony

The root key is generated in an **offline ceremony** on an air-gapped machine with no network connectivity, in the presence of a Ceremony Officer and an independent Witness. The private key never touches a networked machine. It is stored on two separate encrypted USB drives held by independent custodians.

This procedure ensures that no single person and no networked system ever has access to the root private key alone.

The ceremony automation script (`tools/root-ceremony/ceremony_script.py`) automates all deterministic cryptographic steps and enforces all six INV-ROOT-* invariants. It was verified with a dry run: 10/10 verifications pass.

**Production status:** The root key ceremony is scheduled. M2 Production Trust (Key Manifest + BRL live at `banza.network`) is the active milestone. See [Roadmap](#11-roadmap).

---

## 7. BanzAI

### What BanzAI Is

BanzAI is the BANZA Protocol Operating System — the cognitive layer that makes the protocol accessible to operators, developers, and auditors. It is not a chatbot. It is infrastructure.

BanzAI runs alongside the protocol to provide:
- **Certification support** — readiness analysis, manifest validation, level gap assessment
- **Federation intelligence** — operator compatibility scoring, digital twin simulation
- **Knowledge engine** — RAG-backed Q&A over all BANZA specification documents
- **Evaluation pipeline** — benchmark, citation, retrieval, and adversarial evaluation of its own answers
- **Governance intelligence** — ADR/RFC lookup, invariant explanation
- **Operational intelligence** — trace reconstruction, protocol simulation, event analysis

### The Non-Negotiable BanzAI Boundary

| Action | BanzAI | BANZA |
|--------|:------:|:-----:|
| Run the authoritative conformance suite | No | **Yes** |
| Issue production certificates | No | **Yes** |
| Sign Key Manifests or BRLs | No | **Yes** |
| Hold production private keys | No | **Yes** |
| Analyze certification readiness | **Yes** | No |
| Guide operators toward compliance | **Yes** | No |
| Simulate protocol scenarios | **Yes** | No |
| Explain protocol rules in plain language | **Yes** | No |
| Assess federation compatibility between operators | **Yes** | No |

**This boundary is an architectural invariant.** BanzAI evaluates. BANZA certifies. These roles never merge.

When BanzAI says a certification readiness score is 87%, that is guidance — not a certificate. Only the deterministic conformance suite result, followed by BANZA review, produces a certificate.

### BanzAI in the Ecosystem

```
       BANZA
       (Protocol — Authority)
         │
         │  issues certificates
         │  maintains revocation list
         │  approves certification
         │  defines the rules
         ▼
       BanzAI
       (Protocol Operating System)
         │
         │  evaluates readiness
         │  verifies trust assertions
         │  audits payment traces
         │  never decides
         ▼
      Operators
      (Participants)
         │
         │  implement the protocol
         │  process payments
         │  settle obligations
         ↕
      Operators
      (inter-operator, via protocol)
```

No operator has authority over another operator. Authority rests in the protocol — in open rules, published contracts, and verifiable invariants. BANZA is the governance entity that maintains those rules. BanzAI is the instrument of evaluation.

---

## 8. Operators

### What an Operator Is

An operator is any entity that implements the BANZA protocol to process payments. Operators:
- Declare their capabilities in an Operator Manifest
- Implement the requirements for their target certification level
- Operate within the protocol's invariant framework
- Are subject to periodic certification verification (every 12 months; every 90 days at L3+)

There is no such thing as a privileged operator. Every certified operator — including the first and the reference — is subject to exactly the same rules and the same certification process.

### What Operators Implement

The protocol defines capabilities by certification level. Each level is cumulative.

| Level | What you build |
|-------|---------------|
| L0 | Health endpoint, basic wallet operations, sandbox environment |
| L1 | Consumer wallets, merchant wallets, static QR, P2P transfers |
| L2 | Dynamic QR, payment links, T+0 settlement, webhooks, trace propagation |
| L3 | Federation routing, obligations, reconciliation, bank-rail payouts, BANZA-signed certificate |
| L4 | All L3 + EMIS card acquiring (v1.1 scope) |

At L3, the operator must also serve:
- `/.well-known/banza/operator.json` — operator manifest
- `/.well-known/banza/certificate.json` — BANZA-signed certificate
- `POST /federation/route` — accept routing requests
- `GET /federation/obligations` — expose outstanding obligations

### How to Become an Operator

The certification path has six steps. See [Certification](#4-certification) for details.

The conformance suite is open source. There is no fee to run it. Certification review completes within 5 business days. The first operators to certify will be listed in the public operator registry.

### Network Effects

Every certified operator that joins the BANZA network makes every other operator more valuable. A 100,000-customer operator that joins a network with a 500,000-customer operator does not add 600,000 — it multiplies the payment capability of everyone in the network.

This is the structural difference between an open protocol network and a proprietary platform. In a proprietary platform, value accumulates with the dominant operator. In an open protocol network, value belongs to the network — and every participant benefits from every other participant's growth.

---

## 9. Developer Resources

### SDKs

Official BANZA SDKs are available in:

| Language | Package | Status |
|----------|---------|--------|
| TypeScript | `@banza/sdk` | `sdk/typescript/` |
| Python | `banza-sdk` | `sdk/python/` |
| Go | `github.com/banza-protocol/go-sdk` | `sdk/go/` |
| PHP | `banza/php-sdk` | `sdk/php/` |
| Flutter | `banza_sdk` | (via Dart pub) |
| Checkout Web | `@banza/checkout-web` | `sdk/checkout-web/` |

All SDKs will include Key Manifest pinning and production `issuer_key_id` verification at v1.0 release (OPS-005).

### Contracts

All canonical protocol contracts live in `contracts/`:

| Area | Location | Contents |
|------|----------|----------|
| OpenAPI | `contracts/openapi/` | reference-operator.yaml, transfers.yaml, wallet-onboarding.yaml, activity.yaml |
| Federation | `contracts/federation/` | operator-certificate.json, federation-routing.json, federation-obligation.json, federation-event.json, federation-manifest.json |
| Events | `contracts/events/` | envelope.schema.json, types.json, webhook-types.json |
| Webhooks | `contracts/webhooks/` | envelope.schema.json, signature.json |
| QR | `contracts/qr/` | payload-format.json, lifecycle.json |
| SDK certification | `contracts/sdk-certification/` | Compliance vectors |

### Conformance Runner

```bash
# Run L0–L2 conformance suite
python3 tools/banza-conformance/run.py \
  --url http://localhost:3000 \
  --level 2 \
  --output report.json

# Run L3 federation conformance suite
python3 tools/banza-conformance/run_fed.py \
  --url http://localhost:3000 \
  --peer-url http://peer-operator:3001

# Run two-operator interoperability scenarios
python3 tools/banza-conformance/run_interop.py \
  --operator-a http://operator-a:3000 \
  --operator-b http://operator-b:3001
```

### Kernel Architecture (Rust)

The BANZA kernel is the core financial engine. It is composed of crates with rigorously separated responsibilities:

| Crate | Responsibility |
|-------|----------------|
| `banza-ledger` | Double-entry ledger engine — append-only, balanced, atomic |
| `banza-wallets` | Merchant wallet lifecycle |
| `banza-consumer-wallets` | Consumer wallet lifecycle |
| `banza-transactions` | Transaction state machine |
| `banza-transfers` | Wallet-to-wallet transfers |
| `banza-settlement` | T+0 settlement and payout cycles |
| `banza-reconciliation` | Automated reconciliation |
| `banza-payouts` | Outbound to bank accounts |
| `banza-qr` | Static and dynamic QR system |
| `banza-identity` | @handle identity, registration, uniqueness |
| `banza-risk` | Risk evaluation engine |
| `banza-compliance` | Regulatory compliance rules |
| `banza-routing` | Payment routing |

### Normative: Monetary Representation

> **This section is normative.** All operators, SDKs, and protocol implementations MUST conform to these rules.

**The Integer Rule**

All monetary values in the BANZA protocol MUST be represented as integers. Floating-point monetary values are prohibited across the entire protocol surface: APIs, traces and logs, operator manifests, wallet balances, ledger entries, settlement batches, SDK contracts.

```json
// PROHIBITED
{ "amount": 10.50 }

// VALID
{ "amount_minor": 1050 }
```

**The `*_minor` convention**

| Field | Meaning |
|-------|---------|
| `amount_minor` | Generic payment amount |
| `gross_minor` | Gross amount paid by consumer |
| `fee_minor` | Fee retained by operator |
| `net_minor` | Net amount delivered to recipient |
| `available_minor` | Immediately available balance |
| `reserved_minor` | Temporarily held balance |
| `balance_minor` | Total wallet balance |

**Settlement amount invariant (INV-STL-001):**
```
gross_minor = net_minor + fee_minor
```

**Wallet balance invariant (INV-WALLET-001):**
```
balance_minor = available_minor + reserved_minor
```

Wallet balances are always derived from ledger entries — never directly mutated. A wallet balance can never be negative.

**Certification rule MON-001:**

| Violation | Result |
|-----------|--------|
| Float values in API requests/responses | Certification FAIL |
| Float values in traces or logs | Certification FAIL |
| `gross_minor ≠ net_minor + fee_minor` | Certification FAIL |
| `balance_minor ≠ available_minor + reserved_minor` | Certification FAIL |

**Currency registry:**

| Currency | ISO 4217 | Minor units | Status |
|----------|----------|-------------|--------|
| Angolan Kwanza | AOA | 100 (1 AOA = 100 minor units) | Official BANZA currency |
| US Dollar | USD | 100 | Supported (test traces) |
| Euro | EUR | 100 | Supported (test traces) |

Any change to the precision policy requires an approved RFC.

### Financial Invariants

Financial invariants are non-negotiable assertions that can never be violated. They are enforced simultaneously at multiple layers.

#### Invariant Families

| Family | Scope |
|--------|-------|
| `INV-LEDGER-*` | Double-entry, immutability, no floating-point, atomicity |
| `INV-WALLET-*` | Consistent balance, no negatives |
| `INV-STL-*` | gross = net + fee, no money creation |
| `INV-IDEM-*` | Idempotency key scope, replay safety |
| `INV-TRACE-*` | Traceability completeness |
| `INV-QR-*` | QR lifecycle, uniqueness of resolution |
| `INV-IDENT-*` | Handle uniqueness |
| `INV-TRUST-*` | Certificate validity, BRL compliance, manifest verification |
| `INV-FED-*` | Federation routing, settlement, reconciliation |
| `INV-ROOT-*` | Root key architecture, key manifest, production key validation |

#### Critical Invariants

| Invariant | Description | Severity |
|-----------|-------------|----------|
| INV-LEDGER-001 | Debits = Credits on every posting | CRITICAL |
| INV-LEDGER-002 | Ledger entries are immutable | CRITICAL |
| INV-LEDGER-003 | Amounts are i64 — never float | CRITICAL |
| INV-LEDGER-004 | Partial postings never persist (atomic) | CRITICAL |
| INV-STL-001 | gross = net + fee (no money creation) | CRITICAL |
| INV-STL-002 | No negative balances | CRITICAL |
| INV-WALLET-001 | balance = available + reserved | CRITICAL |
| INV-IDENT-001 | @handle uniqueness is global | CRITICAL |
| INV-TRUST-001 | Certificate must be BANZA-signed | CRITICAL |
| INV-TRUST-002 | Certificate lifetime ≤ 90 days (L3+) | CRITICAL |
| INV-TRUST-003 | Certificate must not appear in BRL | CRITICAL |
| INV-TRUST-006 | Certificate `issuer_key_id` must appear in Key Manifest | CRITICAL |
| INV-ROOT-001 | Production key IDs must not start with `test-` | CRITICAL |
| INV-ROOT-002 | Key Manifest must be root-signed | CRITICAL |
| MON-001 | All monetary values as integer minor units | CRITICAL |

#### The Double-Entry Ledger

The ledger is:
- **Append-only** — entries are never modified or deleted
- **Balanced** — every posting has equal debits and credits
- **Integer-only** — amounts are stored as `i64` minor units, never floating-point
- **Atomic** — partial postings never persist

Canonical QR payment posting:
```
Consumer wallet (DEBIT)
    ├── Merchant wallet (CREDIT) — net amount
    └── Fee wallet    (CREDIT) — fee

gross_minor = net_minor + fee_minor  [INV-STL-001]
```

### Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Financial kernel | Rust | Memory safety, deterministic behavior, infrastructure-grade reliability |
| API orchestration | Go | Simplicity, concurrency, operational reliability |
| Database (reference) | PostgreSQL | Single source of financial truth — transactional guarantees |
| Cache / coordination | Redis | Idempotency, distributed locking, rate limiting |
| Observability | OpenTelemetry + Prometheus + Grafana | No black boxes |

---

## 10. Governance

### How BANZA Evolves

BANZA uses two complementary governance mechanisms:

**RFCs (Requests for Comments)** govern protocol decisions: financial invariants, payment flows, API contracts, operator requirements, federation protocols. An RFC is required before any implementation that changes the protocol. RFCs are proposed, discussed, accepted, and then immutable.

An RFC is required for:
- Changes to financial invariants
- Changes to payment flow protocols
- New certification levels
- New currencies in the official registry
- Federation protocol design

**ADRs (Architecture Decision Records)** record decisions after they are made: technology choices, service boundaries, SDK architecture, naming. ADRs are numbered sequentially and immutable after acceptance. ADR-025 defines the canonical BANZA/BanzAI/Operators hierarchy. ADR-026 defines the federation trust model. ADR-028 defines the certification level architecture. ADR-029 defines the production root architecture.

### No Single Operator Governs BANZA

Operator independence is an architectural invariant:
- BANZA is not owned by the reference operator
- BANZA is not governed by the reference operator
- The reference operator does not control the certification framework
- Any operator can contribute to the protocol via the ADR/RFC process, on equal footing with any other operator

The dependency graph is permanent:

```
     Operators   (any certified operator)
         ↑
       BanzAI    (Protocol Operating System)
         ↑
       BANZA     (the protocol itself)
```

BANZA and BanzAI never depend on operators. Operators depend on both.

### Protocol Development Status

Protocol design is frozen at M1 (achieved 2026-06-01). No new ADRs are required before production. No new contracts are required. Any operator can implement BANZA correctly today using only this document and the public specification.

Active work is now operational (M2–M6), not specification. See [Roadmap](#11-roadmap).

---

## 11. Roadmap

### Completed

| Milestone | Achieved | Evidence |
|-----------|:--------:|---------|
| M1 — Protocol Complete | **2026-06-01** | 79/79 federation tests, 14/14 interoperability scenarios, ADR-026/028/029 accepted |
| M5 (partial) — Validation Studio | **2026-06-01** | Three-matrix validation architecture established |

### Active

| Milestone | Status | Blocking |
|-----------|--------|---------|
| **M2 — Production Trust** | ACTIVE | Root key ceremony scheduled; Key Manifest + BRL endpoints pending. OPS-001 is the first unblocked action. |

### Planned

| Milestone | Blocked by | Description |
|-----------|-----------|-------------|
| M3 — First Operator Certified | M2 | First production certificate issued; first operator serving live certificate |
| M4 — BanzAI Operational | Nothing (parallel) | Qdrant + vLLM production deployment; knowledge indexed |
| M5 — Validation Studio Complete | GOV-001/002/003 | RFC status updates, roadmap accuracy, closure declaration |
| M6 — BANZA v1.0 Public Launch | M2 + M3 + M5 | Public announcement; external operators can begin L1–L3 certification |

### Future Versions

| Version | Scope |
|---------|-------|
| **v1.1** | L4 conformance suite (card acquiring), ADR-030 Key Manifest Contract, ADR-031 Multi-Sig Root, DNS discovery mode (RFC-0005), Protocol Version Negotiation (ADR-032) |
| **v1.2** | RFC-0006 Offline Payment Support, multi-operator registry |
| **v2.0** | Cross-border settlement (AOA ↔ other African currencies), advanced fee models |

---

## 12. FAQ

**Is BANZA a bank?**

No. BANZA is a protocol — a set of open rules. It does not hold funds, does not have a banking license, and does not process payments. Operators implement the protocol and process payments on their customers' behalf.

---

**Is BANZA only for Angola?**

BANZA was designed for Angola — its kernel handles the Kwanza, its settlement rails are EMIS and Multicaixa, and its founding context is the Angolan payment landscape. The protocol is open: any entity worldwide can implement it. But Angola is where it matters first.

---

**Can any company become a BANZA operator?**

Yes, provided they pass the conformance suite for their target certification level. There is no institutional approval, no minimum volume, no bilateral agreement. Open rules, open certification.

---

**What happens if an operator goes out of business?**

The protocol continues. Other certified operators continue to operate. The Key Manifest, the BRL, and the conformance suite remain available. The protocol is independent of any specific operator. This is the disappearing operator test — and the fundamental reason BANZA follows the open model.

---

**What is the difference between BANZA and BanzAI?**

BANZA is the protocol. It defines the rules, issues certificates, and owns the conformance suite.

BanzAI is the Protocol Operating System. It helps operators understand the rules, assess their readiness, analyze their traces, and prepare for certification. BanzAI evaluates; BANZA certifies.

---

**Does BanzAI certify operators?**

No. BanzAI produces readiness assessments, guidance, and simulation results. Only BANZA issues certificates — after an operator passes the deterministic conformance suite.

---

**How long does certification take?**

Running the conformance suite takes minutes. BANZA review completes within 5 business days. An L3 federation certificate is valid for 90 days and must be renewed.

---

**What is the BRL?**

The BANZA Revocation List — a signed, public list of revoked or suspended operator certificates, published every 6 hours at `banza.network/federation/revocation-list.json`. Before routing any federated payment, operators verify that the destination is not on the BRL.

---

**How does an operator verify another's certificate without calling BANZA in real time?**

Using the Key Manifest. The Key Manifest is published at `banza.network/.well-known/banza/key-manifest.json`. SDKs pin it at release. A certificate is valid if: (1) its `issuer_key_id` appears in the Key Manifest, (2) its signature verifies with the issuing key's public key, (3) it is not expired, and (4) the operator is not in the current BRL. No real-time BANZA server call is required.

---

**What is federation?**

Federation is the mechanism by which certified operators route payments between each other without bilateral agreements. Customer A on Operator A pays Merchant B on Operator B — crossing the operator boundary — using only the BANZA protocol. Trust is cryptographic, routing is protocol-defined, settlement is handled by bilateral netting.

---

**Does an L3 operator need a special agreement with BANZA to federate?**

No. An L3 certificate is sufficient. Federation is an automatic consequence of L3 certification — there is no additional federeation enrollment process. Any two L3+ operators can federate immediately upon certificate verification.

---

**What level should a new operator target first?**

Start at L0 or L1. L0 establishes that your sandbox environment is operational. L1 covers core wallets, static QR, and P2P transfers — the foundation of every higher level. Most operators target L2 (instant settlement) within their first implementation cycle.

---

**What is the root key ceremony?**

The root key ceremony is the offline process by which the BANZA root key is generated and stored. It is performed on an air-gapped machine, in the presence of a Ceremony Officer and an independent Witness, following a documented procedure. The private key never touches a networked machine. The ceremony establishes the root of trust for the entire BANZA certificate chain. It is a one-time event — after which issuing keys can be generated and the Key Manifest published.

---

## References

**ADRs:**
- ADR-002 — Double-entry ledger
- ADR-004 — Idempotency and rate limiting
- ADR-006 — QR payment system
- ADR-012 — SDK-first ecosystem
- ADR-013 — Wallet-native identity
- ADR-018 — Open financial kernel
- ADR-019 — Operator separation
- ADR-024 — Reference operator
- ADR-025 — Ecosystem naming (canonical, supersedes ADR-016)
- ADR-026 — Federation Trust Model
- ADR-028 — Certification Level Architecture
- ADR-029 — Production Root Architecture

**Companion documents:**
- `BANZA_CERTIFICATION.md` — Certification levels, process, maintenance (authoritative)
- `BANZA_CONFORMANCE.md` — Conformance suite overview
- `BANZA_GOVERNANCE.md` — Governance framework
- `docs/adr/` — All Architecture Decision Records
- `docs/rfc/` — All Requests for Comments
- `docs/federation/` — Federation documentation
- `docs/validation/MATRIX_A_BANZA.md` — BANZA Validation Matrix (canonical)
- `docs/governance/BANZA_V1_OPERATIONAL_TRANSITION_PLAN.md` — M1–M6 roadmap
