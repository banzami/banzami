---
title: BANZA Identity Purity Remediation Plan — BANZA-IDENTITY-PURITY-AUDIT-001
version: 1.0
date: 2026-05-30
status: COMPLETE — all immediate fixes applied
---

# BANZA Identity Purity Remediation Plan

Reference: `docs/migration/banza-identity-purity-audit.md`

---

## Immediate Fixes Applied (2026-05-30)

### Fix 1 — Hero Subheadline (PROTOCOL_CONTAMINATION — P0)

**File:** `apps/docs/components/HeroSection.tsx:57`

| | Text |
|---|---|
| Before | "Banzami é o produto de pagamentos de Angola, construído sobre o Banza — protocolo aberto de infraestrutura financeira." |
| After | "Banza define como o dinheiro se move digitalmente em Angola — através de operadores certificados, regras verificáveis e infraestrutura aberta." |

**Rationale:** The hero is the first text a visitor reads. Leading with "Banzami é..." defines BANZA through its product. The canonical hero framing presents BANZA as the autonomous protocol and defers Banzami to product sections.

---

### Fix 2 — Section Page OG Metadata (PROTOCOL_CONTAMINATION — 17 pages)

**File:** `apps/docs/app/[section]/page.tsx:38,40,41`

| Field | Before | After |
|---|---|---|
| description | `"Banzami — §N: {title}"` | `"Banza — §N: {title}"` |
| og:title | `"{title} · Banzami"` | `"{title} · Banza"` |
| og:description | `"Referência oficial Banzami — secção N: {title}"` | `"Referência oficial Banza — §N: {title}"` |

**Rationale:** The reference document is the Banza protocol reference, not the Banzami product reference. All 17 section pages are protocol pages — their OG cards must identify with BANZA.

---

### Fix 3 — BanzAI Roadmap Description (PROTOCOL_CONTAMINATION)

**File:** `apps/docs/app/roadmap/page.tsx:110`

| | Text |
|---|---|
| Before | "Protocol Operating System for the Banzami ecosystem." |
| After | "Protocol Operating System for the Banza protocol." |

**Rationale:** BanzAI is the Protocol Operating System for the Banza protocol. "for the Banzami ecosystem" positions BanzAI as a Banzami feature rather than a protocol-level system.

---

### Fix 4 — Sobre o BanzAI OG Title (PROTOCOL_CONTAMINATION)

**File:** `apps/docs/app/sobre-banzamia/page.tsx:12`

| | Text |
|---|---|
| Before | `'Sobre o BanzAI · Banzami'` |
| After | `'Sobre o BanzAI · Banza'` |

**Rationale:** "· Banzami" in the OG title implies BanzAI belongs to Banzami. BanzAI is the Protocol OS of BANZA, not a Banzami product.

---

### Fix 5 — Validação H1 (PROTOCOL_CONTAMINATION)

**File:** `apps/docs/app/validacao/page.tsx:35`

| | Text |
|---|---|
| Before | "Execução e Validação do Ecossistema Banzami" |
| After | "Execução e Validação do Protocolo Banza" |

**Rationale:** The validation system tracks implementation of BANZAMI_REFERENCE.md — the Banza protocol specification. The system is validating Banza protocol conformance, not Banzami product features.

---

### Fix 6 — "O Banzami é SDK-first" (OPTIONAL → improved clarity)

**File:** `apps/docs/app/page.tsx:202`

| | Text |
|---|---|
| Before | "O Banzami é SDK-first." |
| After | "O Banza é SDK-first." |

**Rationale:** SDK-first is a protocol design principle, not a product feature. The sentence continues "...ao Banzami SDK oficial" which correctly names the product artifact. The opening claim should attribute the principle to the protocol.

---

### Fix 7 — Broken CTA Links in Developer Section (BROKEN)

**File:** `apps/docs/app/page.tsx:206,209`

| | Before | After |
|---|---|---|
| Primary CTA href | `/banza-para-programadores` (404) | `/banzami-para-programadores` |
| Secondary CTA href | `/o-motor-de-crescimento-do-banza` (404 — route does not exist) | `/visao-geral-do-ecossistema` |
| Secondary CTA label | "O Motor de Crescimento do Banza" | "Visão geral do ecossistema" |

---

## Verification Checklist

- [x] Build passes: `npm run build` — 0 errors
- [x] TypeScript check: `npx tsc --noEmit` — 0 errors
- [x] Hero subheadline contains no "Banzami"
- [x] All 17 section page OG cards say "Banza" not "Banzami"
- [x] BanzAI roadmap says "Banza protocol" not "Banzami ecosystem"
- [x] Sobre BanzAI OG title says "· Banza"
- [x] Validação H1 says "Protocolo Banza"
- [x] Developer section CTA links return 200
- [x] No regression on protected identifiers (`Organização Banzami`, `/.well-known/banzami/`)

---

## Remaining — Deferred Items

### Wave 4 (code identifiers — no user-visible impact)

| Item | Location | Notes |
|---|---|---|
| `SobreBanzamiaPage` function name | `sobre-banzamia/page.tsx:18` | Code identifier |
| `prose-banzami` CSS class | `MarkdownSection.tsx:53` | Tailwind config key |
| Code comments `// Banzami for...` | `[section]/page.tsx:50,53,54,57,58` | Non-visible comments |
| `/* Center node — Banzami Core */` | `EcosystemMap.tsx:36` | Non-visible comment |

### Kept (REQUIRED_PRODUCT_REFERENCE / PROTECTED / SEO)

| Item | Reason |
|---|---|
| "Banzami SDK" in ecosystem section | Product artifact name — correct |
| "Banzami QR" in QR section | Product feature name — correct |
| "Banzami" / "Banzami SDK" / "Banzami Business" in keywords | SEO — users search these terms |
| "Banzami" in global metadata description | SEO discoverability |
| "Organização Banzami" in footers | PROTECTED — legal entity |
| `/.well-known/banzami/` | PROTECTED — wire format |
| `/banzamia` route hrefs | REQUIRED — BanzAI app route (static override) |
| `/banzami-para-*` route hrefs | REQUIRED — product section routes |
| "edição restrita à administração Banzami" | Organizational reference — contextually accurate |

---

## Commits

| Hash | Message |
|---|---|
| `[pending]` | fix(identity): BANZA identity purity — eliminate protocol contamination |

---

*Applied: 2026-05-30.*
