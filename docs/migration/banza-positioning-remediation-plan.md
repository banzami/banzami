---
title: BANZA Positioning Remediation Plan — BANZA-POSITIONING-AUDIT-002
version: 1.0
date: 2026-05-30
status: COMPLETE — all immediate fixes applied
---

# BANZA Positioning Remediation Plan

Reference: `docs/migration/banza-positioning-audit.md`

---

## Fixes Applied (2026-05-30)

### Fix A — Hero Canonical Positioning (MISALIGNED)

**File:** `apps/docs/components/HeroSection.tsx:57`

| | Text |
|---|---|
| Before | "Banza define como o dinheiro se move digitalmente em Angola — através de operadores certificados, regras verificáveis e infraestrutura aberta." |
| After | "Banza define como o dinheiro se move digitalmente — através de operadores certificados, regras verificáveis, infraestrutura aberta e um sistema operativo nativo capaz de explicar, validar e evoluir o protocolo." |

**Changes:**
1. Removed "em Angola" — BANZA is global open infrastructure; Angola-first is a go-to-market, not a definitional constraint
2. Added BanzAI to the foundational positioning — BanzAI is a first-class part of what BANZA is, not an optional module discovered later

**Strategic rationale:** A visitor reading the hero must understand in one sentence why BANZA is different from every other payment protocol. The native protocol OS is that differentiator. It belongs in the first sentence.

---

### Fix B — HomeBanzamIAEntry Descriptor (VALUE PROPOSITION DRIFT)

**File:** `apps/docs/components/banzamia/HomeBanzamIAEntry.tsx:85`

| | Text |
|---|---|
| Before | "O Sistema Operativo do Protocolo Banza — para entender, integrar e validar o ecossistema Banzami." |
| After | "O Sistema Operativo nativo do Protocolo Banza — para entender, integrar e evoluir o protocolo." |

**Rationale:** "o ecossistema Banzami" frames BanzAI as a tool that serves Banzami. BanzAI serves the **Banza protocol**. The widget descriptor is the first place most homepage visitors encounter BanzAI's identity — it must reinforce the protocol-OS relationship, not the product relationship.

---

### Fix C — "Como funciona" H2 (VALUE PROPOSITION DRIFT)

**File:** `apps/docs/app/page.tsx` (§4 Como funciona section)

| | Text |
|---|---|
| H2 Before | "Escanear. Confirmar. Pago instantaneamente." |
| H2 After | "Liquidação atómica. Ledger imutável. Confirmação instantânea." |
| Body added | "Sem intermediários. Sem estado partilhado externo." |

**Rationale:** "Escanear. Confirmar. Pago." describes a user UI action sequence — it's a product UX claim. It presents BANZA as a payments app. "Liquidação atómica. Ledger imutável." describes the infrastructure behavior — atomic finality and immutable record. That is what BANZA is. The body already had the correct protocol language; the headline needed to match.

---

### Fix D — QR Commerce Section (VALUE PROPOSITION DRIFT)

**File:** `apps/docs/app/page.tsx` (§7 QR Commerce section)

| | Text |
|---|---|
| H2 Before | "Um QR code. Todo o comércio angolano." |
| H2 After | "QR como primitiva nativa do protocolo." |
| Body Before | "Do táxi à escola, da cantina à plataforma de doações — o Banzami QR serve todos os casos de uso do mercado angolano." |
| Body After | "Do táxi à escola, da cantina à plataforma de doações — qualquer operador Banza pode emitir e aceitar pagamentos QR. Sem hardware dedicado. Sem intermediários." |

**Rationale:** "Um QR code. Todo o comércio angolano." positions BANZA as a QR commerce application — comparable to a merchant QR product. The canonical positioning is that QR is a protocol-native primitive that any certified operator can implement. "Qualquer operador Banza pode emitir e aceitar pagamentos QR" communicates openness and protocol-level capability, not product exclusivity.

---

### Fix E — Global Metadata Description (MISALIGNED)

**File:** `apps/docs/app/layout.tsx:21`

| | Text |
|---|---|
| Before | "Banza é o protocolo aberto de infraestrutura financeira programável para Angola. Banzami é o produto de pagamentos construído sobre o Banza — wallet-to-wallet, liquidação instantânea, QR-native em Kwanza, Banzami SDK para programadores e Banzami Business para comerciantes." |
| After | "Banza é o protocolo aberto de infraestrutura financeira programável. Operadores certificados, regras verificáveis, infraestrutura aberta. BanzAI é o sistema operativo nativo do protocolo. Banzami é o operador de referência — wallets, QR e SDKs em Kwanza." |

**Rationale:** The global description is inherited by every page via the `template` tag. All 17 section pages, the reference page, the operators page, the validation page — every page's search snippet was effectively advertising Banzami product features. The new description communicates the canonical three-tier hierarchy: BANZA (protocol) → BanzAI (OS) → Banzami (reference operator).

---

### Fix F — Global OG Description (MISALIGNED)

**File:** `apps/docs/app/layout.tsx:39`

| | Text |
|---|---|
| Before | "Banza é o protocolo aberto de infraestrutura financeira programável para Angola. Banzami é o produto de pagamentos construído sobre o Banza — wallet-to-wallet, liquidação instantânea, QR-native em Kwanza." |
| After | "Banza é o protocolo aberto de infraestrutura financeira programável. Operadores certificados, regras verificáveis, infraestrutura aberta. BanzAI é o sistema operativo nativo do protocolo." |

**Rationale:** OG cards (shared links on social/messaging) were describing Banzami wallet features. Corrected to protocol positioning with BanzAI as the differentiator.

---

### Fix G — Homepage Metadata Description (MISALIGNED)

**File:** `apps/docs/app/page.tsx:20`

| | Text |
|---|---|
| Before | "Banza é o protocolo aberto de infraestrutura financeira programável para Angola. Banzami é o produto de pagamentos construído sobre o Banza — pagamentos wallet-to-wallet em Kwanza, QR-native, com Banzami SDKs para programadores e Banzami Business para comerciantes." |
| After | "Banza é o protocolo aberto de infraestrutura financeira programável para Angola. Operadores certificados, regras verificáveis, infraestrutura aberta. BanzAI é o sistema operativo nativo do protocolo. Banzami é o operador de referência — wallets, QR e SDKs em Kwanza." |

---

## Verification Checklist

- [x] Build passes: `npm run build` — 0 errors
- [x] TypeScript check: `npx tsc --noEmit` — 0 errors
- [x] Hero subheadline includes BanzAI in foundational statement
- [x] Hero subheadline removed "em Angola" (infrastructure is global)
- [x] HomeBanzamIAEntry descriptor says "Protocolo Banza" not "ecossistema Banzami"
- [x] §4 "Como funciona" H2 is protocol principle, not product action
- [x] §7 "QR Commerce" H2 is protocol primitive claim, not product claim
- [x] §7 QR body says "qualquer operador Banza" not "o Banzami QR"
- [x] Global metadata description leads with protocol, includes BanzAI, positions Banzami correctly
- [x] Global OG description is protocol-first with BanzAI

---

## Visitor Mental Model After Remediation

A first-time visitor to banzami.org now reads:

1. **Badge:** "Infraestrutura Financeira Programável para Angola" — infrastructure signal
2. **H1:** "Infraestrutura financeira programável." — infrastructure identity
3. **Subheadline:** "Banza define como o dinheiro se move digitalmente — através de operadores certificados, regras verificáveis, infraestrutura aberta e um sistema operativo nativo capaz de explicar, validar e evoluir o protocolo." — full canonical positioning: protocol + BanzAI OS
4. **BanzAI widget:** "O Sistema Operativo nativo do Protocolo Banza — para entender, integrar e evoluir o protocolo." — BanzAI as protocol OS, not product assistant
5. **§4:** "Liquidação atómica. Ledger imutável. Confirmação instantânea." — infrastructure behavior
6. **§6:** "Uma rede. Múltiplos actores." — open protocol ecosystem
7. **§7:** "QR como primitiva nativa do protocolo." — protocol capability
8. **§10:** "O Banza é SDK-first." — protocol design principle

**Mental model outcome:**
- BANZA = Open Programmable Financial Infrastructure
- BanzAI = Native Protocol Operating System (strategically unique)
- Banzami = Reference Operator (encountered in product sections, not hero)

---

## Partially Aligned — Accepted (No Action)

| Surface | Reason for acceptance |
|---|---|
| ManifestoQuote: "Angola não precisa de copiar…" | Vision statement — contextual, not positioning |
| §5 "O telemóvel é a carteira." | Protocol primitive illustration — acceptable |
| §8 Use cases (táxi, cantina, etc.) | Demonstrates protocol value — correct level |
| §9 "O pagamento perfeito dura menos de 3 segundos." | Performance claim — doesn't misrepresent BANZA as product |
| HeroBanzamIAWidget quick prompt "Como integrar o Banzami?" | Valid operator question — leave |
| `validacao` governance notice "administração Banzami" | Organizational reference — accurate |

---

## Remaining Positioning Gaps (No immediate fix — strategic content gap)

| Gap | Description | Recommendation |
|---|---|---|
| No explicit "BANZA vs others" differentiator section | The strategic claim "Most protocols define rules; BANZA defines rules + OS" is implicit but never stated outright on any page | Consider adding a dedicated differentiator section to the homepage or architecture page |
| BanzAI strategic framing only on `/banzamia` and `/sobre-banzamia` | New visitors who don't click BanzAI in the navbar never see the full strategic case | Consider adding a BanzAI positioning card to the homepage above the fold |

These are content additions, not fixes — deferred to a future product content step.

---

## Commits

| Hash | Message |
|---|---|
| `[pending]` | fix(positioning): BANZA ecosystem value proposition consolidation |

---

*Applied: 2026-05-30.*
