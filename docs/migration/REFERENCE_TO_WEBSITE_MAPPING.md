---
title: REFERENCE_TO_WEBSITE_MAPPING
version: 1.0
date: 2026-05-30
status: DESIGN COMPLETE — pending execution authorization
---

# Reference to Website Mapping

**Purpose:** Map every V2 reference section to the website surface(s) it should seed. Identify coverage gaps in both directions: reference sections with no website equivalent, and website surfaces with no reference anchor.

**Principle:** The reference is the canonical source of truth. The website communicates the thesis. When a reference section is strengthened, the website surfaces that draw from it must be updated. This mapping ensures that reference changes propagate correctly.

---

## 1. Reference Section → Website Surface Map

| Reference § | Section title | Primary website surface | Secondary surfaces | Status |
|-------------|---------------|------------------------|-------------------|--------|
| §1 | O Problema: Angola Tem as Peças | Homepage "O problema" section | Comerciantes page | PARTIAL — homepage problem section exists but does not name the protocol gap as root cause |
| §2 | A Camada que Falta | Homepage — NEW protocol layer section (T0-001) | Operators page hero | ABSENT — no website surface assembles this argument |
| §3 | O que é o BANZA | Homepage hero + hero subheadline | Reference page §1 (existing) | PARTIAL — hero names BANZA as infrastructure, not as protocol layer specifically |
| §4 | Governança do Protocolo | /validacao page | Architecture page | PARTIAL — validation page exists but frames governance as a feature, not a governance model |
| §5 | Modelo de Certificação | /operators page | Reference | ABSENT — operators page shows the registry without explaining why open certification matters |
| §6 | Regras do Protocolo — Especificações Técnicas | /architecture page | Reference | PARTIAL — architecture page covers technical spec but not as "protocol rules every operator must implement" |
| §7 | Federação | /roadmap page | Architecture page | ABSENT — roadmap page has no BANZA protocol milestones; federation not visible on any page |
| §8 | O Problema do Conhecimento do Protocolo | /banzamia page (landing state) | — | ABSENT — BanzAI has no landing state; the knowledge gap problem is not framed anywhere |
| §9 | BanzAI | /banzamia page | Homepage BanzAI widget | PARTIAL — BanzAI widget exists; /banzamia page exists but opens to interface without framing |
| §10 | O Modelo de Operadores | /operators page | Homepage ecosystem section | PARTIAL — operators page shows registry; doesn't explain why the operator model matters |
| §11 | Banzami — A Implementação de Referência | Homepage hero area | Reference | ABSENT — no single surface explains what "reference implementation" means and why Banzami ≠ BANZA |
| §12 | Para Programadores | /programadores page | Homepage SDK section | PARTIAL — SDK examples exist; missing "why BANZA vs. Stripe/Flutterwave" argument |
| §13 | Para Comerciantes | /comerciantes page | Homepage QR section | PARTIAL — merchant content exists; missing structural differentiation from Multicaixa/TPA |
| §14 | Para Consumidores | Banzami app store listings | — | ABSENT — no public /consumers reference page on website |
| §15 | Arquitectura Técnica de Referência | /architecture page | — | PRESENT — architecture page exists and covers implementation details |
| §16 | Sandbox e Ambiente de Testes | /programadores sandbox section | — | PARTIAL — sandbox documented in programadores page |
| §17 | Roadmap | /roadmap page | — | PARTIAL — BanzAI roadmap exists; BANZA Protocol roadmap absent |
| §18 | Declaração de Visão | Homepage closing section | About page | PARTIAL — closing quote exists but is QR/wallet-protagonist, not protocol-protagonist |

---

## 2. Website Surface → Reference Anchor Map

For each website surface: which reference sections it should draw from, and whether it currently does.

### Homepage (`app/page.tsx`)

| Website section | Should draw from | Currently draws from | Gap |
|----------------|-----------------|---------------------|-----|
| Hero headline | §3 (BANZA identity) | §3 partial | PARTIAL |
| Hero subheadline | §3 (three-tier hierarchy) | §3 partial | PARTIAL |
| BanzAI widget | §9 (BanzAI) | §9 | PRESENT |
| ManifestoQuote | §18 (vision) | §18 partial | PARTIAL |
| Protocol Layer section | §2 (NEW) | — | ABSENT |
| "O problema" | §1 + §2 (gap argument) | §1 symptoms only | ABSENT |
| "Como funciona" | §6 (protocol specs) | Correct | PRESENT |
| "Filosofia wallet-native" | §6 (protocol invariants) | Product framing | PARTIAL |
| "Ecossistema" | §10 (operator model) | Registry listing | PARTIAL |
| "QR Commerce" | §6 (QR-native invariant) | Product feature | PARTIAL |
| "Mobile-first" | §6 (T+0 invariant) | Product promise | PARTIAL |
| "Para programadores" | §12 (developer differentiation) | SDK examples only | PARTIAL |
| "Segurança" | §6 (financial invariants) | Correct | PRESENT |
| Closing quote | §18 (protocol vision) | QR+wallet story | WEAK |
| Reference grid | All §§ | All §§ | PRESENT |

**Homepage coverage:** 3 PRESENT, 7 PARTIAL, 2 ABSENT

---

### /operators (`app/operators/page.tsx`)

| Website section | Should draw from | Currently draws from | Gap |
|----------------|-----------------|---------------------|-----|
| Page hero | §10 (operator model) + §5 (open certification) | Registry stats only | ABSENT |
| Certification narrative | §5 (open certification vs. closed) | — | ABSENT |
| Operator list | §10 (registry) | Registry | PRESENT |
| Join CTA | §5 (certification process) | Generic CTA | PARTIAL |

**Operators coverage:** 1 PRESENT, 1 PARTIAL, 2 ABSENT

---

### /banzamia (`app/banzamia/page.tsx`)

| Website section | Should draw from | Currently draws from | Gap |
|----------------|-----------------|---------------------|-----|
| Landing state / framing | §8 (knowledge problem) + §9 (BanzAI) | — (no landing state) | ABSENT |
| Interface | §9 (BanzAI) | §9 | PRESENT |

**BanzAI coverage:** 1 PRESENT, 1 ABSENT

---

### /programadores (`app/programadores/page.tsx` or equivalent)

| Website section | Should draw from | Currently draws from | Gap |
|----------------|-----------------|---------------------|-----|
| Why BANZA differentiation | §12 (developer differentiation) | — | ABSENT |
| SDK integration | §12 (SDK content) | §12 | PRESENT |
| Protocol guarantees | §6 (invariants) | — | ABSENT |

**Developers coverage:** 1 PRESENT, 2 ABSENT

---

### /comerciantes (`app/comerciantes/page.tsx` or equivalent)

| Website section | Should draw from | Currently draws from | Gap |
|----------------|-----------------|---------------------|-----|
| Why QR vs. TPA structural arg | §13 (structural differentiation) | Symptom-level only | PARTIAL |
| QR workflow | §13 (merchant content) | §13 | PRESENT |
| Banzami Business | §13 | §13 | PRESENT |

**Merchants coverage:** 2 PRESENT, 1 PARTIAL

---

### /architecture (`app/architecture/page.tsx` or equivalent)

| Website section | Should draw from | Currently draws from | Gap |
|----------------|-----------------|---------------------|-----|
| Protocol framing | §3 + §6 (protocol = law) | Technology stack | PARTIAL |
| Technical details | §15 (implementation) | §15 | PRESENT |
| EcosystemMap center node | §3 (BANZA = protocol) | "API · Ledger · Core Rust" | WEAK |

**Architecture coverage:** 1 PRESENT, 1 PARTIAL, 1 WEAK

---

### /validacao (`app/validacao/page.tsx` or equivalent)

| Website section | Should draw from | Currently draws from | Gap |
|----------------|-----------------|---------------------|-----|
| Strategic transparency frame | §4 (governance = infrastructure) | — | ABSENT |
| Validation content | §4 + §6 (invariants) | Technical content | PARTIAL |

**Validation coverage:** 1 PARTIAL, 1 ABSENT

---

### /roadmap (`app/roadmap/page.tsx`)

| Website section | Should draw from | Currently draws from | Gap |
|----------------|-----------------|---------------------|-----|
| BANZA Protocol roadmap | §17 (protocol track) | — | ABSENT |
| BanzAI roadmap | §17 (BanzAI track) | §17 BanzAI items | PRESENT |
| Banzami product roadmap | §17 (Banzami track) | §17 BanzAI items only | ABSENT |

**Roadmap coverage:** 1 PRESENT, 2 ABSENT

---

## 3. Coverage Summary Matrix

| Reference § | Homepage | /operators | /banzamia | /programadores | /comerciantes | /architecture | /validacao | /roadmap |
|-------------|----------|-----------|-----------|----------------|--------------|--------------|-----------|---------|
| §1 Problem | PARTIAL | — | — | — | PARTIAL | — | — | — |
| §2 Protocol Layer | ABSENT | ABSENT | — | — | — | — | — | — |
| §3 What is BANZA | PARTIAL | — | — | — | — | PARTIAL | — | — |
| §4 Governance | — | — | — | — | — | — | ABSENT | — |
| §5 Certification | — | ABSENT | — | — | — | — | — | — |
| §6 Protocol Specs | PARTIAL | — | — | ABSENT | — | PARTIAL | PARTIAL | — |
| §7 Federation | — | — | — | — | — | — | — | ABSENT |
| §8 Knowledge Problem | — | — | ABSENT | — | — | — | — | — |
| §9 BanzAI | PRESENT | — | PARTIAL | — | — | — | — | — |
| §10 Operator Model | PARTIAL | ABSENT | — | — | — | — | — | — |
| §11 Ref. Impl. | ABSENT | — | — | — | — | — | — | — |
| §12 Developers | PARTIAL | — | — | PARTIAL | — | — | — | — |
| §13 Merchants | PARTIAL | — | — | — | PRESENT | — | — | — |
| §14 Consumers | — | — | — | — | — | — | — | — |
| §15 Architecture | — | — | — | — | — | PRESENT | — | — |
| §16 Sandbox | — | — | — | PARTIAL | — | — | — | — |
| §17 Roadmap | — | — | — | — | — | — | — | PARTIAL |
| §18 Vision | PARTIAL | — | — | — | — | — | — | — |

**Legend:** PRESENT ✓ / PARTIAL ◐ / ABSENT ✗ / — (not expected)

---

## 4. Priority Propagation Queue

When a reference section is updated, these website changes become required. Ordered by impact.

### Tier 0 (reference change → immediate website update required)

| Reference change | Website surface to update | Why |
|-----------------|--------------------------|-----|
| §2 written (A Camada que Falta) | Homepage — add Protocol Layer section (T0-001) | §2 is the primary content source for T0-001 |
| §2 written | /operators page hero | §2 is the "open certification vs. closed" argument |
| §1 expanded | Homepage "O problema" framing sentence (T0-002) | §1 gap argument = problem section frame |
| §5 updated | /operators page certification narrative (T0-003) | §5 is the open certification content |
| §8 written | /banzamia page landing state (T0-004) | §8 is the problem BanzAI solves — the landing framing |

### Tier 1 (reference change → website update in Phase 2)

| Reference change | Website surface to update | Why |
|-----------------|--------------------------|-----|
| §12 expanded | /programadores differentiation preface | §12 is the developer differentiation content |
| §13 expanded | /comerciantes structural differentiation | §13 is the TPA structural argument |
| §17 protocol track added | /roadmap BANZA Protocol section | §17 is the roadmap content |
| §3 reframed | EcosystemMap center node | §3 defines BANZA = protocol, not "API · Ledger · Core Rust" |
| §4 governance framing | /validacao strategic frame | §4 is the governance model |

### Tier 2 (reference change → website update in Phase 3)

| Reference change | Website surface to update | Why |
|-----------------|--------------------------|-----|
| §18 reframed | Homepage closing quote | §18 is the vision statement — protocol-first |
| §10 expanded | Homepage ecosystem section | §10 is the operator model |
| §7 reframed | /architecture federation section | §7 is federation = infrastructure proof |

---

## 5. Bidirectional Invariant

**The reference and the website must never contradict each other.** The following claims appear on the website and must be verifiable in the reference:

| Website claim | Reference section | Currently verifiable? |
|--------------|------------------|----------------------|
| "Infraestrutura Financeira Programável" (hero) | §3 | YES |
| "Certificação aberta" (operators page) | §5 | YES |
| "T+0 settlement" | §6 | YES |
| "QR é primitiva nativa do protocolo" (homepage) | §6 | YES |
| "BANZA é o protocolo que Angola não tem" | §2 | NO — §2 doesn't exist yet in V1 |
| "Como o Pix para o Brasil" | §2 | NO — §2 doesn't exist yet in V1 |
| "Qualquer operador pode certificar" (operators) | §5 | PARTIAL |
| "BanzAI é o Sistema Operativo do protocolo" | §9 | YES |

The two claims currently stated on no reference section (§2 claims) are the highest priority new content in the reference rebuild.

---

## 6. Website-First vs. Reference-First Changes

Two of the pending changes can proceed independently of the reference rebuild. They draw from sections that already exist in V1 and will continue to exist in V2:

| Change | Type | Reference dependency |
|--------|------|---------------------|
| T0-003: /operators page protocol narrative | Website-first | §5 already exists (V1 §7) |
| T0-004: /banzamia page landing state | Website-first | §9 already exists (V1 §9) |
| T0-001: Homepage protocol layer section | Reference-first | §2 must be written first |
| T0-002: Homepage problem framing sentence | Reference-first | §1 must be expanded first |

**Recommendation:** The reference rebuild and the website T0 changes can proceed in parallel if:
- T0-003 and T0-004 are executed now (draw from existing V1 sections)
- §2 (A Camada que Falta) is written first in the reference
- T0-001 and T0-002 are executed after §2 is complete

This means the reference rebuild and website changes are not strictly sequential — they can interleave at the section level.

---

*Mapping completed: 2026-05-30. No files modified.*
