# Deep Consistency Audit Report

Version: 1.0
Date: 2026-05-30
Scope: Banza/Banzami/BanzAI brand naming — post-ADR-025 consistency pass (Waves AA–AX)

---

## 1. Executive Summary

ADR-025 established a three-tier naming architecture: **BANZA** (protocol / infrastructure / organization), **Banzami** (reference operator / payment product), and **BanzAI** (Protocol Operating System). A deep audit of the docs frontend surfaced the following categories of violation:

- **5 live 404s** caused by broken hrefs in global navigation and footer (`apps/docs/app/layout.tsx`)
- **16 broken redirect destinations** in `next.config.ts` that resolve to non-existent routes
- **4 stale TOC anchors** in `BANZAMI_REFERENCE.md`
- **1 false protocol attribution** in `BANZAMI_REFERENCE.md` (BanzAI described as operating on "protocolo Banzami" instead of "protocolo Banza")
- **1 outdated ADR citation** (ADR-016 cited without noting ADR-025 supersedes it)
- **3 module description strings** that misattribute certification as a Banzami-product artifact rather than a Banza-protocol artifact
- **3 stale test expectations** in `reference.test.ts`
- **1 routing architecture anomaly**: section 9 has two disconnected routes (`/banzai` and `/sobre-banzamia`)

All items are classified, actionable, and assigned to remediation waves. Protected identifiers (`/.well-known/banzami/`, `BANZAMI:` QR prefix, `banzami.org`, `@banzami.org`, `Banzami Lda`) are out of scope.

---

## 2. Route Audit

Routes confirmed to exist in the built output:

| Route |
|-------|
| `/arquitectura-tecnica` |
| `/banzai` |
| `/banzami-para-comerciantes` |
| `/banzami-para-programadores` |
| `/banzamia` |
| `/declaracao-de-visao` |
| `/federacao` |
| `/governanca` |
| `/modelo-de-certificacao` |
| `/o-que-e-o-banza` |
| `/operators` |
| `/para-consumidores` |
| `/por-que-angola-por-que-agora` |
| `/principios-fundamentais` |
| `/reference` |
| `/representacao-monetaria` |
| `/roadmap` |
| `/sandbox-e-ambiente-de-testes` |
| `/seguranca-e-integridade-financeira` |
| `/sobre-banzamia` |
| `/validacao` |
| `/visao-geral-do-ecossistema` |

### Navigation and Footer Link Audit

| Visible Label | File:line | Current href | Actual route | Exists? | Classification |
|---|---|---|---|---|---|
| "Banza para Programadores" (nav) | `apps/docs/app/layout.tsx:82` | `/banza-para-programadores` | `/banzami-para-programadores` | NO | BROKEN |
| "Banza para Comerciantes" (nav) | `apps/docs/app/layout.tsx:83` | `/banza-para-comerciantes` | `/banzami-para-comerciantes` | NO | BROKEN |
| "O que é o Banzami" (footer label) | `apps/docs/app/layout.tsx:151` | `/o-que-e-o-banzami` | `/o-que-e-o-banza` | NO | BROKEN + OUTDATED LABEL |
| "Banza para Programadores" (footer) | `apps/docs/app/layout.tsx:152` | `/banza-para-programadores` | `/banzami-para-programadores` | NO | BROKEN |
| "Banza para Comerciantes" (footer) | `apps/docs/app/layout.tsx:153` | `/banza-para-comerciantes` | `/banzami-para-comerciantes` | NO | BROKEN |

All five items produce live 404 responses. Line 151 has two distinct errors: the href is wrong and the displayed label ("O que é o Banzami") does not match the current section title ("O que é o Banza?").

---

## 3. next.config.ts Redirect Audit

Full table of all 20 redirects found in `next.config.ts`.

| Source | Destination | Destination Exists? | Status |
|---|---|---|---|
| `/what-is-banzami` | `/o-que-e-o-banzami` | NO (cascading break — `/o-que-e-o-banzami` is itself 404) | BROKEN |
| `/why-banzami-exists` | `/por-que-o-banzami-existe` | NO — old section removed | BROKEN |
| `/why-now` | `/por-que-agora` | NO — old section removed | BROKEN |
| `/the-vision` | `/a-visao` | NO — old section removed | BROKEN |
| `/a-morning-in-luanda` | `/uma-manha-em-luanda` | NO — old section removed | BROKEN |
| `/how-banzami-works` | `/como-o-banzami-funciona` | NO — old section removed | BROKEN |
| `/core-features` | `/funcionalidades-principais` | NO — old section removed | BROKEN |
| `/real-angola-use-cases` | `/casos-de-uso-reais-em-angola` | NO — old section removed | BROKEN |
| `/qr-payment-ecosystem` | `/ecossistema-de-pagamentos-qr` | NO — old section removed | BROKEN |
| `/wallet-native-philosophy` | `/filosofia-wallet-native` | NO — old section removed | BROKEN |
| `/banzami-for-consumers` | `/banzami-para-consumidores` | NO — section 12 is `/para-consumidores` | BROKEN |
| `/the-banzami-flywheel` | `/o-motor-de-crescimento-banzami` | NO — old section removed | BROKEN |
| `/banzami-business-ecosystem` | `/ecossistema-de-negocio-banzami` | NO — old section removed | BROKEN |
| `/the-banzami-ecosystem` | `/o-ecossistema-banzami` | NO — old section removed | BROKEN |
| `/roadmap-future` | `/roadmap-e-futuro` | NO — section 16 is `/roadmap` | BROKEN |
| `/final-vision-statement` | `/declaracao-de-visao-final` | NO — section 17 is `/declaracao-de-visao` | BROKEN |
| `/banzami-for-merchants` | `/banzami-para-comerciantes` | YES | CORRECT |
| `/banzami-for-developers` | `/banzami-para-programadores` | YES | CORRECT |
| `/security-financial-integrity` | `/seguranca-e-integridade-financeira` | YES | CORRECT |
| `/technical-architecture` | `/arquitectura-tecnica` | YES | CORRECT |

**Summary:** 16 broken, 4 working. The `/what-is-banzami` entry is a cascading break: its destination `/o-que-e-o-banzami` is not a valid route, so neither the redirect source nor the intended destination resolves correctly. The correct destination for this source is `/o-que-e-o-banza`.

---

## 4. Navigation Content Audit

### Broken Labels

| Location | File:line | Current text | Correct text | Issue |
|---|---|---|---|---|
| Footer link label | `apps/docs/app/layout.tsx:151` | "O que é o Banzami" | "O que é o Banza?" | Section 1 title changed; label is stale |

### Notes on Nav Labels for Lines 82–83 and 152–153

The nav and footer links at lines 82, 83, 152, and 153 use the label text "Banza para Programadores" and "Banza para Comerciantes". Although the word "Banza" in these labels could be debated (the section titles use "Banzami"), the primary and urgent defect is the broken href. The label wording may be intentional shorthand; this is flagged as OUTDATED but not BROKEN for the label alone. The href is definitively BROKEN in all four cases.

---

## 5. BANZAMI_REFERENCE.md Content Audit

File: `BANZAMI_REFERENCE.md`

### 5.1 TOC Anchor Issues

| TOC line | File:line | Current anchor | Correct anchor | Classification |
|---|---|---|---|---|
| "1. O que é o Banzami?" | `BANZAMI_REFERENCE.md:18` | `#1-o-que-é-o-banzami` | `#1-o-que-e-o-banza` | OUTDATED |
| "9. BanzAI" | `BANZAMI_REFERENCE.md:26` | `#9-banzamia` | `#9-banzai` | OUTDATED |
| "10. Banza para Programadores" | `BANZAMI_REFERENCE.md:27` | `#10-banza-para-programadores` | `#10-banzami-para-programadores` | OUTDATED |
| "11. Banza para Comerciantes" | `BANZAMI_REFERENCE.md:28` | `#11-banza-para-comerciantes` | `#11-banzami-para-comerciantes` | OUTDATED |

All four anchors point to headings that have either been renamed or whose slugs no longer match. In-page TOC navigation is silently broken for these entries.

### 5.2 False Protocol Attribution

| File:line | Current text | Required correction | Classification |
|---|---|---|---|
| `BANZAMI_REFERENCE.md:1427` | "a camada de inteligência que torna o protocolo Banzami auto-gerível" | "o protocolo Banza" | FALSE |

ADR-025 defines BanzAI as the Protocol Operating System for the **Banza** protocol. Calling it the operating layer of "protocolo Banzami" confuses the product (Banzami) with the protocol (Banza). This is a false attribution, not merely an outdated label.

### 5.3 Outdated ADR Citation

| File:line | Current text | Issue | Classification |
|---|---|---|---|
| `BANZAMI_REFERENCE.md:1930` | "ADR-016 — Arquitectura de marca" | Cited without noting that ADR-025 supersedes it for brand hierarchy decisions | OUTDATED |

The citation is not wrong in isolation but creates a misleading authority chain for readers who act on ADR-016 without knowing ADR-025 overrides the naming portions.

---

## 6. BanzAI Module Content Audit

Three component description strings misattribute Banza-protocol artifacts (certification, conformance suite) to Banzami the product.

| File:line | Current text | Required correction | Classification |
|---|---|---|---|
| `apps/docs/components/banzamia/modules/CertificationCopilotModule.tsx:62` | "Analyse your operator manifest and capabilities against Banzami certification requirements." | "against Banza protocol certification requirements." | FALSE |
| `apps/docs/components/banzamia/modules/ConformanceModule.tsx:32` | "Run the Banzami certification suite against any operator endpoint." | "Run the Banza certification suite against any operator endpoint." | FALSE |
| `apps/docs/components/banzamia/modules/OperatorBuilderModule.tsx:71` | "Step-by-step guide to building and certifying a Banzami operator." | "building and certifying a Banza protocol operator." | FALSE |

Operator certification is defined at the protocol layer (Banza). Attributing it to "Banzami" implies the requirements are product-specific rather than protocol-wide, which is architecturally incorrect per ADR-025.

### Confirmed Correct References in Modules (No Action)

These were reviewed and confirmed correct per ADR-025:

| File:line | Text | Reason correct |
|---|---|---|
| `apps/docs/components/banzamia/modules/TraceModule.tsx:54` | "any Banzami payment flow" | Banzami IS the payment product |
| `apps/docs/components/banzamia/modules/SDKModule.tsx:178` | "All Banzami integrations must use official SDKs" | Banzami SDK is the product SDK |
| `apps/docs/components/banzamia/modules/SDKModule.tsx:125` | "Generate Banzami SDK integration examples" | Banzami SDK is the product SDK |
| `apps/docs/components/banzamia/modules/OperatorBuilderModule.tsx:231` | `/.well-known/banzami/operator.json` | PROTECTED wire format |
| `apps/docs/components/banzamia/modules/ManifestModule.tsx:86` | `/.well-known/banzami/operator.json` | PROTECTED wire format |
| `apps/docs/components/banzamia/modules/RFCExplorerModule.tsx:11` | RFC-006 defines `/.well-known/banzami/` | PROTECTED |
| `apps/docs/components/banzamia/modules/RFCExplorerModule.tsx:20` | ADR-016 entry references ADR-025 | Already updated — CORRECT |
| `apps/docs/pages/operators/page.tsx:93` | `/.well-known/banzami/operator.json` | PROTECTED wire format |
| `apps/docs/components/banzamia/EcosystemMap.tsx:36` | comment "Center node — Banzami Core" | Code comment only, not user-visible |
| `apps/docs/components/banzamia/HomeBanzamIAEntry.tsx:13` | `'O que é o Banzami?'` | Valid user question about the product |

---

## 7. Test Suite Audit

File: `apps/docs/lib/__tests__/reference.test.ts`

| File:line | Current expectation | Correct expectation | Classification |
|---|---|---|---|
| `reference.test.ts:29` | `expect(toSlug('O que é o Banzami?')).toBe('o-que-e-o-banzami')` | `toBe('o-que-e-o-banza')` — section 1 title is now "O que é o Banza?" | OUTDATED |
| `reference.test.ts:223` | `expect(s?.title).toBe('O que é o Banzami?')` | `toBe('O que é o Banza?')` | OUTDATED |
| `reference.test.ts:280` | `expect(s?.title).toBe('O que é o Banzami?')` | `toBe('O que é o Banza?')` | OUTDATED |

These tests will pass if the underlying section title is still the old string, or fail if the title has already been updated. Either way they are stale anchors that must be updated to match the current section 1 heading. Remediation is deferred to Wave AD (after the source section title is confirmed stable).

---

## 8. Routing Architecture Anomaly

### Section 9 — BanzAI: Two Disconnected Routes

Section 9 of the reference document is titled "BanzAI". Its slug, as derived from the section heading, is `/banzai`. This route exists in the build and renders section 9 content.

However, `SectionNav.tsx` and `SectionCard.tsx` override all section 9 links to point to `/sobre-banzamia` instead of `/banzai`. The route `/sobre-banzamia` also exists in the build.

The result:

| Route | Exists? | Receives nav links? | Content |
|---|---|---|---|
| `/banzai` | YES | NO — floating, reachable only via direct URL | Section 9 content |
| `/sobre-banzamia` | YES | YES — all nav and card links | Section 9 content (or variant) |

**Impact:** `/banzai` is a live orphan route. Users who land on it via a bookmark, external link, or search engine result are on a page that has no navigation context. `/sobre-banzamia` is the only navigable path, but its relationship to the canonical section 9 slug is undocumented and architecturally ambiguous.

**Decision required before remediation:** Either `/banzai` should redirect to `/sobre-banzamia` (making `/sobre-banzamia` canonical), or `/sobre-banzamia` should redirect to `/banzai` (making the slug-derived route canonical) and nav overrides should be removed. This is assigned to Wave AX and requires an architectural decision.

---

## 9. Classification Summary

| Classification | Count | Description |
|---|---|---|
| BROKEN | 21 | Live 404s or cascading redirect failures (5 nav/footer links + 16 redirect destinations) |
| FALSE | 4 | Architecturally incorrect attributions (1 in BANZAMI_REFERENCE.md + 3 in modules) |
| OUTDATED | 9 | Stale labels, anchors, or citations (4 TOC anchors + 1 footer label + 1 ADR cite + 3 test assertions) |
| CORRECT | 10 | Reviewed and confirmed correct per ADR-025 |
| PROTECTED | 5 | Protected identifiers — must not change |
| CONTEXTUAL | 3 | Correct in context as Banzami-product references |
| ANOMALY | 1 | Routing architecture issue requiring a decision (Wave AX) |

**Total items audited:** 53

---

## 10. Deferred Items Table

These items are out of scope for Waves AA–AX. They are assigned to later waves per the migration roadmap.

| Item | Location | Wave | Reason deferred |
|---|---|---|---|
| Component identifier `BanzamIAApp` | Multiple files | Wave 4 | Requires coordinated component rename across all consumers |
| Component identifier `BanzamIAChat` | Multiple files | Wave 4 | Same as above |
| Component identifier `BanzamIASidebar` | Multiple files | Wave 4 | Same as above |
| Component identifier `BanzamIAIcon` | Multiple files | Wave 4 | Same as above |
| Component identifier `BanzamIASourcesPanel` | Multiple files | Wave 4 | Same as above |
| Env var `BANZAMIA_*_URL` refs | `apps/docs/components/banzamia/modules/StatusModule.tsx` | Wave 5a | Env var rename requires infra coordination |
| Route `/banzamia` | `apps/docs/app/banzamia/` | Wave 5b | Part of larger BanzAI app routing decision |
| Route `/sobre-banzamia` | `apps/docs/app/sobre-banzamia/` | Wave 5b | Part of Wave AX architectural decision (must resolve AX first) |
| Wire format `/.well-known/banzami/` | Multiple files | Wave 5c | PROTECTED — must never change |
| Wire format `BANZAMI:` QR prefix | Multiple files | Wave 5c | PROTECTED — must never change |
| Wire format `BANZAMI-SBX:` | Multiple files | Wave 5c | PROTECTED — must never change |
| Directory path `apps/banzamia` (string ref) | `apps/docs/components/banzamia/modules/QualityModule.tsx` | Wave 9 | Filesystem path change; large blast radius |
| Module source file `contexts/banzami-protocol.md` | `apps/docs/components/banzamia/modules/KnowledgeModule.tsx` | Wave 9 | File rename required |
| Image filename `banzamia-*.svg` | `/images/architecture/` | Wave 9 | Asset rename; requires CDN/cache coordination |
| Image filename `banzami-logo.png` | `/images/banza/` | Wave 9 | Asset rename; requires CDN/cache coordination |
| Test file `reference.test.ts` (stale assertions) | `apps/docs/lib/__tests__/reference.test.ts` | Deferred to after Wave AB | Fix when section 1 title is confirmed stable; Wave AD tracks this |
