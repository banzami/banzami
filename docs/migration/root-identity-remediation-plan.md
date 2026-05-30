---
title: Root Identity Remediation Plan — BANZA-NAMING-INVERSION-STEP-009B
version: 1.0
date: 2026-05-29
depends-on: root-identity-audit.md
status: PENDING EXECUTION
---

# Root Identity Remediation Plan

Actionable remediation for all issues found in `root-identity-audit.md`. Items are sequenced by impact and technical risk. All changes are in the Banza repo (`apps/docs`).

---

## Wave A — Immediate (display strings only, no route or component renames)

These are simple string replacements inside existing component render methods. No structural changes. Safe to apply in a single commit.

### A-1 — Fix `BanzamIAChat.tsx` — welcome screen + error text

**File:** `apps/docs/components/banzamia/BanzamIAChat.tsx`

| Line | Current | Replace with |
|------|---------|--------------|
| 280 | `<h1 ...>BanzamIA</h1>` | `<h1 ...>BanzAI</h1>` |
| 281–282 | `BanzamIA é o Sistema Operativo do Protocolo Banzami. 16 módulos.` | `BanzAI é o Sistema Operativo do Protocolo Banza. 16 módulos.` |
| 252 | `Erro ao conectar com BanzamIA. Verifique a configuração do endpoint.` | `Erro ao conectar com BanzAI. Verifique a configuração do endpoint.` |

**Audit refs:** F-01, F-02, F-03

### A-2 — Fix `HomeBanzamIAEntry.tsx` — CTA and error link text + descriptor

**File:** `apps/docs/components/banzamia/HomeBanzamIAEntry.tsx`

| Line | Current | Replace with |
|------|---------|--------------|
| 84 | `A interface inteligente oficial para entender, integrar e validar o ecossistema Banzami.` | `O Sistema Operativo do Protocolo Banza — para entender, integrar e validar o ecossistema Banzami.` |
| 129 | `Abrir BanzamIA completo →` | `Abrir BanzAI completo →` |
| 165 | `Pode abrir o BanzamIA completo` | `Pode abrir o BanzAI completo` |

**Audit refs:** F-04, F-05, M-08

### A-3 — Fix `SectionNav.tsx` — sidebar logo label

**File:** `apps/docs/components/SectionNav.tsx`

| Line | Current | Replace with |
|------|---------|--------------|
| 65 | `Banzami` (uppercase sidebar label) | `Banza` |
| 67 | `Documentação oficial` | `Documentação do Protocolo` |

**Audit refs:** M-07

**Commit for Wave A:**
```
fix(identity): BanzAI display name + protocol attribution in chat, entry widget, sidebar
```

---

## Wave B — SEO Metadata (layout.tsx)

These changes update the SEO and OpenGraph metadata to reflect the BANZA institutional site identity. High-impact for search indexing and link previews. No visual changes to rendered UI.

### B-1 — Fix `layout.tsx` — SEO title, description, OpenGraph, footer tagline

**File:** `apps/docs/app/layout.tsx`

| Field | Current | Replace with |
|-------|---------|--------------|
| `title.default` | `'Banzami — Pagamentos Instantâneos em Kwanza'` | `'Banza — Protocolo de Infraestrutura Financeira Programável'` |
| `title.template` | `'%s · Banzami'` | `'%s · Banza'` |
| `description` | `'Banzami constrói a infraestrutura que permitirá Angola pagar digitalmente...'` | `'Banza é o protocolo aberto de infraestrutura financeira programável para Angola. Banzami é o produto de pagamentos construído sobre o Banza — wallet-to-wallet, liquidação instantânea, QR-native em Kwanza.'` |
| `openGraph.title` | `'Banzami — Pagamentos Instantâneos em Kwanza'` | `'Banza — Protocolo de Infraestrutura Financeira Programável'` |
| `openGraph.description` | `'Banzami constrói a infraestrutura...'` | `'Banza é o protocolo aberto de infraestrutura financeira programável para Angola. Banzami é o produto de pagamentos construído sobre o Banza.'` |
| `openGraph.siteName` | `'Banzami'` | `'Banza'` |
| Footer tagline (layout.tsx:145) | `'Banzami — Rede Angolana de Pagamentos Instantâneos por QR Code'` | `'Banza — Protocolo Aberto de Infraestrutura Financeira para Angola'` |

**Keep unchanged:**
- `authors: [{ name: 'Organização Banzami' }]` — legal entity name, protected identifier
- Logo image and wordmark "Banzami" — domain exception

**Audit refs:** M-01, M-02, M-03, M-04, M-05, M-06

**Commit for Wave B:**
```
fix(identity): SEO metadata + OG tags — BANZA institutional site framing per ADR-025
```

---

## Wave C — Wave 5a: Env Var References (user-visible demo note)

The demo mode note in the BanzAI sidebar references the env var `NEXT_PUBLIC_BANZAMIA_API_URL` as a visible string for the demo state. This is Wave 5a (env var rename requires coordinating all deployment configs).

**Blocked by:** env var rename across docker-compose files, Dockerfile, and server env. Requires a coordinated deployment. Do not apply in isolation.

**Scope:** `BanzamIASidebar.tsx` demo mode footer note text — change `NEXT_PUBLIC_BANZAMIA_API_URL` → `NEXT_PUBLIC_BANZAI_API_URL` only after the env var itself is renamed in all environments.

---

## Wave D — Wave 5b: Route Renames

All `/banzamia` and `/sobre-banzamia` route references. These are breaking changes — old routes must redirect to new routes to avoid broken bookmarks and external links.

**Requires before applying:**
1. Add permanent redirects (308) from `/banzamia` → `/banzai` and `/sobre-banzamia` → `/sobre-banzai` in Next.js config.
2. Update all internal `href` references in the same commit.
3. Update the backend API URL env var (Wave 5a) if the API path also changes.

**Files to update (route strings only):**
- `apps/docs/app/layout.tsx` — nav link `href="/banzamia"` → `href="/banzai"`, footer link
- `apps/docs/components/SectionNav.tsx` — `'/sobre-banzamia'` → `'/sobre-banzai'`
- `apps/docs/components/banzamia/BanzamIASidebar.tsx` — footer link route
- `apps/docs/components/banzamia/HomeBanzamIAEntry.tsx` — two `href="/banzamia"` references
- `apps/docs/components/HeroBanzamIAWidget.tsx` — `router.push('/banzamia?...')`
- `apps/docs/app/sobre-banzamia/page.tsx` — two `href="/banzamia"` references
- `apps/docs/app/` — rename directory `banzamia/` → `banzai/` and `sobre-banzamia/` → `sobre-banzai/`

**Commit for Wave D:**
```
feat(routes): rename /banzamia → /banzai and /sobre-banzamia → /sobre-banzai per ADR-025
```

---

## Wave E — Wave 4: Component Renames

Code identifier renames. No user-visible impact unless missed in Wave A/B. Requires updating every import, export, and type reference across the codebase.

| Old name | New name | File |
|----------|----------|------|
| `BanzamIAApp` | `BanzAIApp` | BanzamIAApp.tsx |
| `BanzamIAChat` | `BanzAIChat` | BanzamIAChat.tsx |
| `BanzamIASidebar` | `BanzAISidebar` | BanzamIASidebar.tsx |
| `BanzamIAIcon` | `BanzAIIcon` | BanzamIAIcon.tsx |
| `BanzamIASourcesPanel` | `BanzAISourcesPanel` | BanzamIASourcesPanel.tsx |
| `BanzamIAPage` | `BanzAIPage` | banzamia/page.tsx |
| `SobreBanzamiaPage` | `SobreBanzAIPage` | sobre-banzamia/page.tsx |

**Recommendation:** Apply together with Wave D (route renames) since the page files are being renamed anyway. Use a single large PR with automated find-replace for import strings.

---

## Execution Sequence

```
Wave A  →  Wave B  →  Wave C (env coordinated)  →  Wave D  →  Wave E
 now         now        with env deploy           with redirects  with D
```

Waves A and B are fully independent of each other — they can be applied in parallel or as a single commit. Waves C, D, E have coordination requirements.

---

## Definition of Done

The root identity audit is resolved when:

- [ ] All Tier 1 FALSE items (F-01 through F-05) are fixed in code and deployed to production
- [ ] All Tier 2 MISLEADING SEO items (M-01 through M-08) are fixed and indexed by search engines
- [ ] `/banzamia` → `/banzai` redirect in place and old route returns 308
- [ ] No user-visible string anywhere on banzami.org reads "BanzamIA" or "Protocolo Banzami"
- [ ] `docs/migration/root-identity-audit.md` updated with resolution status for each finding

---

*Plan authored: 2026-05-29. Depends on root-identity-audit.md. See BANZAMI_IMPLEMENTATION_MATRIX.json for governance tracking.*
