# Deep Consistency Remediation Plan

Version: 1.0
Date: 2026-05-30
Scope: Banza/Banzami/BanzAI brand naming — post-ADR-025 consistency pass (Waves AA–AX)
Reference: `docs/migration/deep-consistency-audit-report.md`

---

## 1. Overview

This plan covers targeted, surgical fixes to bring the docs frontend into alignment with ADR-025 without touching source code that is deferred to Waves 4–9. All items here are in scope for immediate execution. No changes to protected identifiers (`/.well-known/banzami/`, `BANZAMI:` QR prefix, `banzami.org`, `@banzami.org`, `Banzami Lda`) are included in any wave below.

Waves are labeled AA–AX to sit cleanly after the existing Waves 1–3 in the migration roadmap without conflicting with the deferred Wave 4–9 numbering.

**Priority order:**
1. Wave AA — urgent (live 404s in production navigation)
2. Wave AB — content quality (silent broken anchors)
3. Wave AC — content quality (false protocol attributions)
4. Wave AD — test quality (stale test expectations)
5. Wave AE — SEO health (16 broken redirects)
6. Wave AX — requires architectural decision before execution

---

## 2. Wave AA — CRITICAL: Fix Broken Nav and Footer Links

**Priority:** P0 — live 404s affecting all users who click nav or footer links
**File:** `apps/docs/app/layout.tsx`
**Items:** 5 href fixes (one also requires a label fix)

### Changes Required

| # | File:line | Change type | Current value | Replace with |
|---|---|---|---|---|
| AA-1 | `apps/docs/app/layout.tsx:82` | href | `/banza-para-programadores` | `/banzami-para-programadores` |
| AA-2 | `apps/docs/app/layout.tsx:83` | href | `/banza-para-comerciantes` | `/banzami-para-comerciantes` |
| AA-3 | `apps/docs/app/layout.tsx:151` | href | `/o-que-e-o-banzami` | `/o-que-e-o-banza` |
| AA-4 | `apps/docs/app/layout.tsx:151` | label text | "O que é o Banzami" | "O que é o Banza?" |
| AA-5 | `apps/docs/app/layout.tsx:152` | href | `/banza-para-programadores` | `/banzami-para-programadores` |
| AA-6 | `apps/docs/app/layout.tsx:153` | href | `/banza-para-comerciantes` | `/banzami-para-comerciantes` |

Note: Items AA-3 and AA-4 are on the same line. Both the `href` attribute and the visible link text must be updated together. The label fix (AA-4) is not optional — displaying "O que é o Banzami" as the label for a link pointing to `/o-que-e-o-banza` would be a content mismatch even after the href is corrected.

### Verification

After applying Wave AA:
- [ ] Navigate to docs site, confirm nav links "Banza para Programadores" and "Banza para Comerciantes" resolve without 404
- [ ] Confirm footer "O que é o Banza?" link resolves to `/o-que-e-o-banza`
- [ ] Confirm footer "Banza para Programadores" and "Banza para Comerciantes" links resolve without 404
- [ ] No regressions in surrounding nav items

---

## 3. Wave AB — Fix Reference Doc TOC Anchors

**Priority:** P1 — silent broken in-page navigation
**File:** `BANZAMI_REFERENCE.md`
**Items:** 4 anchor fixes

### Changes Required

| # | File:line | Change type | Current value | Replace with |
|---|---|---|---|---|
| AB-1 | `BANZAMI_REFERENCE.md:18` | TOC anchor | `#1-o-que-é-o-banzami` | `#1-o-que-e-o-banza` |
| AB-2 | `BANZAMI_REFERENCE.md:26` | TOC anchor | `#9-banzamia` | `#9-banzai` |
| AB-3 | `BANZAMI_REFERENCE.md:27` | TOC anchor | `#10-banza-para-programadores` | `#10-banzami-para-programadores` |
| AB-4 | `BANZAMI_REFERENCE.md:28` | TOC anchor | `#11-banza-para-comerciantes` | `#11-banzami-para-comerciantes` |

### Context

These are Markdown TOC entries of the form `[Section Title](#anchor)`. Only the anchor fragment (the part after `#`) needs to change. The link text shown in the TOC is separate from the anchor and may also need review, but the anchor is the definitive broken element.

### Verification

After applying Wave AB:
- [ ] Click each of the four TOC entries in `BANZAMI_REFERENCE.md` and confirm they jump to the correct heading
- [ ] No other TOC entries broken

---

## 4. Wave AC — Fix False Protocol Attributions

**Priority:** P1 — architecturally incorrect content visible to users and developers
**Files:** `BANZAMI_REFERENCE.md`, `CertificationCopilotModule.tsx`, `ConformanceModule.tsx`, `OperatorBuilderModule.tsx`
**Items:** 4 text corrections

### Changes Required

| # | File:line | Change type | Current text | Replace with |
|---|---|---|---|---|
| AC-1 | `BANZAMI_REFERENCE.md:1427` | Body copy | "o protocolo Banzami" | "o protocolo Banza" |
| AC-2 | `apps/docs/components/banzamia/modules/CertificationCopilotModule.tsx:62` | UI description string | "against Banzami certification requirements." | "against Banza protocol certification requirements." |
| AC-3 | `apps/docs/components/banzamia/modules/ConformanceModule.tsx:32` | UI description string | "Run the Banzami certification suite" | "Run the Banza certification suite" |
| AC-4 | `apps/docs/components/banzamia/modules/OperatorBuilderModule.tsx:71` | UI description string | "building and certifying a Banzami operator." | "building and certifying a Banza protocol operator." |

### Rationale

Operator certification is a Banza-protocol artifact. Any operator — including Banzami as the reference operator — certifies against the **Banza** protocol, not against Banzami's own requirements. Describing certification as "Banzami certification requirements" implies a product-level gate rather than a protocol-level standard, which is architecturally incorrect per ADR-025.

AC-1 additionally affects BanzAI's self-description: BanzAI operates the Banza protocol, not the Banzami product. The current text at line 1427 inverts this relationship.

### Supplementary Fix — ADR Citation (AC-5)

| # | File:line | Change type | Current text | Replace with |
|---|---|---|---|---|
| AC-5 | `BANZAMI_REFERENCE.md:1930` | ADR reference | "ADR-016 — Arquitectura de marca" (standalone) | Add inline note: "ADR-016 — Arquitectura de marca (superseded for brand hierarchy by ADR-025)" |

This prevents readers from acting on ADR-016 naming rules without being aware that ADR-025 is the current authority.

### Verification

After applying Wave AC:
- [ ] Search the three module files for "Banzami certification" — zero results
- [ ] Search the three module files for "Banzami certification suite" — zero results
- [ ] Confirm `BANZAMI_REFERENCE.md:1427` reads "protocolo Banza"
- [ ] Confirm `BANZAMI_REFERENCE.md:1930` references ADR-025 as superseding authority

---

## 5. Wave AD — Fix Stale Test Assertions

**Priority:** P2 — test quality; tests may pass on stale data or fail on correct data
**File:** `apps/docs/lib/__tests__/reference.test.ts`
**Items:** 3 stale expectations

**Precondition:** Wave AD must be executed after section 1's title ("O que é o Banza?") is confirmed stable in the source data. If the title has already been updated, these tests are currently failing. If the title has not yet been updated, these tests pass on stale data and will break at the moment of title update. Either way, the assertions need to track the current title.

### Changes Required

| # | File:line | Change type | Current expectation | Replace with |
|---|---|---|---|---|
| AD-1 | `apps/docs/lib/__tests__/reference.test.ts:29` | Test assertion | `toBe('o-que-e-o-banzami')` | `toBe('o-que-e-o-banza')` |
| AD-2 | `apps/docs/lib/__tests__/reference.test.ts:223` | Test assertion | `toBe('O que é o Banzami?')` | `toBe('O que é o Banza?')` |
| AD-3 | `apps/docs/lib/__tests__/reference.test.ts:280` | Test assertion | `toBe('O que é o Banzami?')` | `toBe('O que é o Banza?')` |

### Verification

After applying Wave AD:
- [ ] Run `npm test` (or equivalent) in the `apps/docs` workspace
- [ ] The three updated assertions pass
- [ ] No other test regressions introduced

---

## 6. Wave AE — Fix next.config.ts Stale Redirects

**Priority:** P2 — SEO and inbound link health; broken redirect destinations send crawlers and users to 404
**File:** `apps/docs/next.config.ts`
**Items:** Remove 14 broken redirects; fix 1 cascading redirect; retain 4 working redirects

### Action: Remove These 14 Broken Redirects

The destinations no longer exist. Keeping them in the redirect table causes search engines to follow a chain that terminates in a 404 rather than receiving a clean 410 Gone or simply not being indexed.

| Source to remove | Broken destination |
|---|---|
| `/why-banzami-exists` | `/por-que-o-banzami-existe` |
| `/why-now` | `/por-que-agora` |
| `/the-vision` | `/a-visao` |
| `/a-morning-in-luanda` | `/uma-manha-em-luanda` |
| `/how-banzami-works` | `/como-o-banzami-funciona` |
| `/core-features` | `/funcionalidades-principais` |
| `/real-angola-use-cases` | `/casos-de-uso-reais-em-angola` |
| `/qr-payment-ecosystem` | `/ecossistema-de-pagamentos-qr` |
| `/wallet-native-philosophy` | `/filosofia-wallet-native` |
| `/the-banzami-flywheel` | `/o-motor-de-crescimento-banzami` |
| `/banzami-business-ecosystem` | `/ecossistema-de-negocio-banzami` |
| `/the-banzami-ecosystem` | `/o-ecossistema-banzami` |
| `/roadmap-future` | `/roadmap-e-futuro` |
| `/final-vision-statement` | `/declaracao-de-visao-final` |

### Action: Fix 2 Broken Redirects with Correct Destinations

| # | Source | Current (broken) destination | Correct destination |
|---|---|---|---|
| AE-1 | `/what-is-banzami` | `/o-que-e-o-banzami` (cascading 404) | `/o-que-e-o-banza` |
| AE-2 | `/banzami-for-consumers` | `/banzami-para-consumidores` (404) | `/para-consumidores` |

### Action: Retain These 4 Working Redirects

| Source | Destination |
|---|---|
| `/banzami-for-merchants` | `/banzami-para-comerciantes` |
| `/banzami-for-developers` | `/banzami-para-programadores` |
| `/security-financial-integrity` | `/seguranca-e-integridade-financeira` |
| `/technical-architecture` | `/arquitectura-tecnica` |

### Verification

After applying Wave AE:
- [ ] `next.config.ts` redirects array contains exactly 6 entries (4 retained + 2 fixed)
- [ ] `curl -I https://banzami.org/what-is-banzami` follows to `/o-que-e-o-banza` with 200
- [ ] `curl -I https://banzami.org/banzami-for-consumers` follows to `/para-consumidores` with 200
- [ ] All 14 removed sources return 404 (no redirect loop)
- [ ] 4 retained redirects still resolve correctly

---

## 7. Wave AX — Resolve /banzai vs /sobre-banzamia Routing Anomaly

**Priority:** P3 — requires architectural decision; no code changes until decision is documented
**Files:** `apps/docs/components/banzamia/SectionNav.tsx`, `apps/docs/components/banzamia/SectionCard.tsx`, possibly `apps/docs/next.config.ts`

### Current State

- `/banzai` — exists, renders section 9 content, receives zero nav links (floating orphan)
- `/sobre-banzamia` — exists, receives all section 9 nav links, overridden in `SectionNav.tsx` and `SectionCard.tsx`

### Decision Required

One of two options must be chosen before any code is written:

**Option A — Make `/sobre-banzamia` canonical:**
- Add redirect: `/banzai` → `/sobre-banzamia` (permanent)
- Remove nav override logic in `SectionNav.tsx` and `SectionCard.tsx` (they already point to `/sobre-banzamia`, so the override becomes the canonical behavior)
- Document `/sobre-banzamia` as the official section 9 route

**Option B — Make `/banzai` canonical (slug-derived, matches section heading):**
- Add redirect: `/sobre-banzamia` → `/banzai` (permanent)
- Remove nav overrides in `SectionNav.tsx` and `SectionCard.tsx` so they point to `/banzai`
- Document `/banzai` as the official section 9 route

**Recommendation:** Option B is architecturally cleaner because `/banzai` is the slug naturally derived from the section title "BanzAI", consistent with how all other sections are routed. `/sobre-banzamia` appears to be a holdover from a previous naming scheme (when the section was called "BanzamIA"). However, this decision carries SEO implications if `/sobre-banzamia` has already been indexed, and must be confirmed by the product owner before execution.

### Execution Steps (post-decision)

| # | File | Action |
|---|---|---|
| AX-1 | `apps/docs/next.config.ts` | Add redirect for the non-canonical route to the canonical one |
| AX-2 | `apps/docs/components/banzamia/SectionNav.tsx` | Remove section 9 override; use canonical route |
| AX-3 | `apps/docs/components/banzamia/SectionCard.tsx` | Remove section 9 override; use canonical route |

### Verification (post-execution)

- [ ] `/banzai` and `/sobre-banzamia` do not both render content — one redirects to the other
- [ ] All section 9 nav links point to the canonical route
- [ ] No orphan routes remain for section 9

---

## 8. Deferred (Waves 4–9)

These items were identified during the audit but are out of scope for Waves AA–AX. They must not be changed until their respective waves are explicitly initiated.

| Item | Location | Wave | Precondition |
|---|---|---|---|
| Component identifiers: `BanzamIAApp`, `BanzamIAChat`, `BanzamIASidebar`, `BanzamIAIcon`, `BanzamIASourcesPanel` | Multiple component files | Wave 4 | Requires coordinated rename across all consumers |
| Env var `BANZAMIA_*_URL` | `apps/docs/components/banzamia/modules/StatusModule.tsx` | Wave 5a | Env var rename requires infra and deployment coordination |
| Route `/banzamia` | `apps/docs/app/banzamia/` | Wave 5b | Part of BanzAI app routing; must not move until Wave AX is resolved |
| Route `/sobre-banzamia` | `apps/docs/app/sobre-banzamia/` | Wave 5b | Blocked on Wave AX architectural decision |
| Wire format `/.well-known/banzami/` | Multiple files | Wave 5c | PROTECTED — must never change per ADR-025 |
| Wire format `BANZAMI:` QR prefix | Multiple files | Wave 5c | PROTECTED — must never change per ADR-025 |
| Wire format `BANZAMI-SBX:` | Multiple files | Wave 5c | PROTECTED — must never change per ADR-025 |
| Directory string `apps/banzamia` | `apps/docs/components/banzamia/modules/QualityModule.tsx` | Wave 9 | Filesystem rename; large blast radius |
| Module source `contexts/banzami-protocol.md` | `apps/docs/components/banzamia/modules/KnowledgeModule.tsx` | Wave 9 | File rename required |
| Image filenames `banzamia-*.svg` | `/images/architecture/` | Wave 9 | Asset rename; CDN/cache coordination required |
| Image filename `banzami-logo.png` | `/images/banza/` | Wave 9 | Asset rename; CDN/cache coordination required |

---

## 9. Definition of Done

A wave is considered complete when all of the following are true:

- [ ] All file:line changes in the wave have been applied
- [ ] All verification checklist items in the wave pass
- [ ] `npm run build` (or equivalent) in `apps/docs` completes without errors
- [ ] No new 404s introduced (confirm with a link-check pass on changed pages)
- [ ] Changes committed and pushed to `origin/main` per the always-deploy policy
- [ ] A wave execution report is added to `docs/migration/` following the pattern of `wave-1-report.md`, `wave-2-svg-report.md`, `wave-3-execution-report.md`

---

## 10. Priority Order

| Order | Wave | Urgency | Reason |
|---|---|---|---|
| 1 | Wave AA | URGENT — P0 | Live 404s in production navigation visible to every user |
| 2 | Wave AB | P1 — content quality | Silent broken in-page anchors; no 404 but navigation fails |
| 3 | Wave AC | P1 — content quality | False protocol attributions mislead developers building operators |
| 4 | Wave AD | P2 — test quality | Stale assertions silently pass or block correct future changes |
| 5 | Wave AE | P2 — SEO health | 16 broken redirect destinations; search crawlers hit dead ends |
| 6 | Wave AX | P3 — architecture | Requires product owner decision before any code changes |
