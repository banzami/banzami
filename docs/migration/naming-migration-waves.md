# Naming Inversion — Migration Waves

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29

---

## Overview

Migration is structured in 9 waves ordered by risk and dependency. Each wave is a discrete, reviewable commit or PR. No wave may begin until the previous wave is merged and the working tree is clean.

Before beginning any wave: resolve all conflicts in that wave listed in `naming-conflicts.md`.

---

## Wave 1 — Documentation

**Scope:** Prose documentation only. No code, no web routes, no SVGs.  
**Repos:** Banzami, Banza (operator)  
**Estimated files:** 30–40  
**Risk:** Low  
**Rollback:** `git revert <wave-1-commit>` — no side effects

### Files in scope

| File | Action | Class |
|------|--------|-------|
| `docs/adr/ADR-001` through `ADR-020`, `ADR-022`–`ADR-024` | "Banzami Protocol/Kernel/Ecosystem" → "Banza Protocol/Kernel/Ecosystem" | PROTOCOL |
| `docs/adr/ADR-016` | Already superseded by ADR-025. Add superseded header. | PROTOCOL |
| `GOVERNANCE.md` | "Banzami organization" → "Banza Protocol Organization" (confirm class ORG first) | PROTOCOL/ORG |
| `CONTRIBUTING.md` | "Banzami protocol" → "Banza protocol" | PROTOCOL |
| `core/README.md` | Crate section headers | PROTOCOL |
| `docs/BANZAMI_REFERENCE.md` (content) | Prose references to "Banzami Protocol" | PROTOCOL |
| `docs/conformance.md` | "Banzami conformance" → "Banza conformance" | PROTOCOL |
| `docs/rfc/*.md` (prose only) | Protocol prose. Keep all normative strings (BANZAMI:, /.well-known/banzami/). | PROTOCOL |
| BanzamIA `README.md` | BanzamIA → BanzAI (AI_OS class) | AI_OS |
| Banzami `README.md` | BanzamIA → BanzAI section header; ecosystem ASCII diagram | AI_OS |

### What NOT to rename in Wave 1

- `BANZAMI_REFERENCE.md` (filename) — conflict pending resolution
- `BANZAMI:`, `BANZAMI-SBX:` in RFC normative text
- `/.well-known/banzami/operator.json` in RFC text
- `banzami.org`, `contact@banzami.org`
- Any code symbol
- Any URL or route

### Commit message

```
docs(naming): Wave 1 — protocol documentation rename Banzami → Banza, BanzamIA → BanzAI
```

---

## Wave 2 — SVG Diagrams

**Scope:** SVG text labels for architecture diagrams.  
**Repos:** Banzami, Banza  
**Estimated files:** 8–10 SVG files  
**Risk:** Low–Medium  
**Rollback:** `git revert` — visual regression requires manual verification

### Files in scope

| File | Changes | Class |
|------|---------|-------|
| `docs/images/architecture/event-flow.svg` | "Banzami Kernel" → "Banza Kernel" in title and labels | SVG_TEXT / PROTOCOL |
| `docs/images/architecture/provider-model.svg` | "BANZAMI KERNEL CRATES" → "BANZA KERNEL CRATES" | SVG_TEXT / PROTOCOL |
| `docs/images/architecture/sandbox-architecture.svg` | "Banzami Sandbox Operator" → "Banza Sandbox Operator". Keep `/.well-known/banzami/operator.json` label unchanged. | SVG_TEXT |
| `docs/images/architecture/banzamia-product-architecture.svg` | All BanzamIA labels → BanzAI | SVG_TEXT / AI_OS |
| `docs/images/architecture/banzamia-canonical-architecture.svg` | BanzamIA layer label → BanzAI | SVG_TEXT / AI_OS |
| `apps/docs/public/images/architecture/` (copies) | Mirror all SVG changes | SVG_TEXT |

### What NOT to rename in Wave 2

- `BANZAMI-SBX:` text in `qr-payment-lifecycle.svg` — protocol data
- `/.well-known/banzami/operator.json` label in `sandbox-architecture.svg` — protocol URL
- File names of SVGs (defer to Wave 9 or omit entirely — file renames break existing references in docs)

### Verification

Open each SVG in a browser or vector editor after editing. Confirm no text nodes are broken or mispositioned.

### Commit message

```
docs(naming): Wave 2 — SVG architecture diagrams rename Banzami → Banza, BanzamIA → BanzAI
```

---

## Wave 3 — Website Copy

**Scope:** banzami.org public pages, metadata, app store notes.  
**Repos:** Banza (apps/docs)  
**Estimated files:** 15–20 TSX/TS files  
**Risk:** Medium  
**Rollback:** `git revert` + `./deploy.sh docs-frontend`

### Prerequisite

Resolve conflict C-004 (`/banzamia` URL path) before this wave begins.

### Files in scope

| File | Action | Class |
|------|--------|-------|
| `apps/docs/app/banzamia/page.tsx` | Metadata title, description. URL path `/banzamia` — conflict resolution required. | PUBLIC_COPY |
| `apps/docs/app/roadmap/page.tsx` | BanzamIA → BanzAI in metadata and inline text | PUBLIC_COPY |
| `apps/docs/app/sobre-banzamia/page.tsx` | BanzamIA → BanzAI in metadata, OG tags, body text | PUBLIC_COPY |
| `docs/APP_STORE_REVIEW_NOTES.md` | "Banza Business" → "Banzami Business", "Banza Wallet" → "Banzami Wallet", "Pay with Banza" → "Pay with Banzami" | PUBLIC_COPY / PRODUCT |
| Other banzami.org pages | Check remaining pages for "Banza" product references | PUBLIC_COPY |

### What NOT to rename in Wave 3

- `banzami.org` domain in any form
- `contact@banzami.org`
- The URL path `/banzamia` until conflict C-004 is resolved

### Commit message

```
feat(website): Wave 3 — website copy rename: Banza product → Banzami, BanzamIA → BanzAI
```

### Deploy

```
./deploy.sh docs-frontend
```

---

## Wave 4 — BanzAI UI (formerly BanzamIA)

**Scope:** BanzamIA React components, module files, file renames.  
**Repos:** Banza (apps/docs/components/banzamia/)  
**Estimated files:** 20–25 TSX/TS files  
**Risk:** Medium  
**Rollback:** `git revert` + deploy

### Prerequisite

Wave 3 must be complete. Resolve conflict C-005 (`/banzamia` directory path) before this wave.

### Files in scope

| Action | Details |
|--------|---------|
| Rename `BanzamIAChat.tsx` → `BanzAIChat.tsx` | Update all imports in `BanzamIAApp.tsx` and page files |
| Rename `BanzamIASidebar.tsx` → `BanzAISidebar.tsx` | Update imports |
| Rename `BanzamIAApp.tsx` → `BanzAIApp.tsx` | Update page import |
| Rename `BanzamIAIcon.tsx` → `BanzAIIcon.tsx` | Update imports in all components |
| Rename `BanzamIASourcesPanel.tsx` → `BanzAISourcesPanel.tsx` | Update imports |
| Rename component symbols inside each file | `BanzamIAChat` → `BanzAIChat`, etc. |
| Rename `lib/banzamia-client.ts` → `lib/banzai-client.ts` | Update imports in all consuming files |
| Rename `@banzami/banzamia` package | → `@banza/banzai` in BanzamIA `package.json` (if conflict C-003 resolved) |
| Rename `BANZAMIA_*` env vars in UI code | Update all `process.env.BANZAMIA_*` references in frontend code |
| Update UI text strings | "BanzamIA" → "BanzAI" in welcome text, placeholder, aria labels |
| Rename `modules/banzamia/` directory | → `modules/banzai/` or `modules/` (if conflict C-005 resolved) |

### Verification

Start the docs dev server and navigate all 16 BanzAI modules. Confirm no broken imports, no broken UI text, no console errors.

### Commit message

```
feat(banzai-ui): Wave 4 — BanzamIA components renamed to BanzAI
```

### Deploy

```
./deploy.sh docs-frontend
```

---

## Wave 5 — APIs, Environment Variables, Docker

**Scope:** BanzamIA internal API routes, all BANZAMIA_* env vars, Docker service names.  
**Repos:** BanzamIA, Banzami  
**Estimated files:** 10–15  
**Risk:** High — requires production coordination  
**Rollback:** Complex — requires coordinated rollback of server config

### Prerequisite

Wave 4 must be complete. Coordinate with live server before beginning this wave.

### Files in scope

| File | Action |
|------|--------|
| `BanzamIA/.env.example` | Rename all BANZAMIA_* → BANZAI_* |
| `BanzamIA/docker/docker-compose.yml` | Rename service `banzamia` → `banzai`, image names, BANZAMIA_* → BANZAI_*, container names |
| `Banzami/docker/banzamia/docker-compose.yml` | Same |
| `Banzami/docker/banzamia/` directory | → `docker/banzai/` (Wave 9 cleanup or here) |
| BanzamIA Fastify router | `/banzamia/*` routes → `/banzai/*` routes |
| Frontend API client that calls BanzamIA routes | Update base URL if using `/banzamia` prefix |
| Production server `.env` files | **Coordinate with deploy — update server config simultaneously with code change** |
| CI/CD secrets | Rename BANZAMIA_* secrets in GitHub Actions |

### Special consideration

`Banza-Signature` webhook header — after inversion, "Banza" is the protocol name, so `Banza-Signature` becomes the more accurate name. This is not a rename in the traditional sense — it may already be correct after the inversion. Confirm and document.

### Commit message

```
chore(infra): Wave 5 — BanzamIA env vars, docker, API routes renamed to BanzAI
```

---

## Wave 6 — SDKs

**Scope:** SDK class names, published package renames, SDK documentation.  
**Repos:** Banzami (sdk/), Banza (plugins/)  
**Estimated files:** 30–40  
**Risk:** Critical — published packages  
**Rollback:** Publish previous version; deprecate new; notify consumers

### Prerequisite

Resolve conflicts C-001 (SDK name), C-002 (BanzaClient class name) before beginning.

### Actions (after conflict resolution)

| Action | Risk |
|--------|------|
| Checkout web SDK (internal): rename `BanzamiApiError` | Low — not published |
| Published TypeScript SDK: if renaming `BanzaClient` → `BanzamiClient`, ship v2.0.0 with deprecation of v1 | Critical |
| Published PHP SDK: same | Critical |
| Published Flutter SDK: same | Critical |
| Python SDK: rename `BanzamiAuthenticationError` per conflict resolution | Medium |
| Update SDK docs: webhook example route `/webhooks/banzami` → `/webhooks/banza` | Low |
| Update SDK README branding | Medium |

### Note

If conflict C-001 resolves that `@banza/sdk` is already correct after inversion (SDK for the Banza protocol), then no class renames are needed — only documentation updates. This would reduce Wave 6 from Critical to Low.

### Commit message

```
feat(sdk): Wave 6 — SDK rename per ADR-025 (breaking: see CHANGELOG)
```

---

## Wave 7 — Code Symbols / Rust Crates

**Scope:** All 21 Rust crate names, internal code symbols not yet renamed, test fixtures.  
**Repos:** Banzami (core/)  
**Estimated files:** 60–80 (all crates and their dependency references)  
**Risk:** Medium — internal only, no external consumers  
**Rollback:** `git revert` + `cargo build`

### Actions

| Action | Details |
|--------|---------|
| Rename all 21 `banzami-*` crates to `banza-*` | Edit workspace `Cargo.toml` + every crate's `Cargo.toml` `[package]` name + every `[dependencies]` block in all crates |
| Update `RUST_LOG=banzami=debug` | → `RUST_LOG=banza=debug` in docker-compose, dev scripts |
| Update `tools/banzami-conformance` | → `tools/banza-conformance` (directory rename + Cargo name) |
| Rename `BanzamiWebhookSignatureError` in tests | After SDK decision |
| Update remaining code symbol tests | `BanzaClient` etc. — after Wave 6 |

### Verification

```bash
cargo build --workspace
cargo test --workspace
```

### Commit message

```
refactor(core): Wave 7 — rename banzami-* Rust crates to banza-*
```

---

## Wave 8 — Repository Renames

**Scope:** GitHub repository names, GitHub organization name.  
**Risk:** Critical — breaks all clone URLs, forks, CI badge links, any published link to the repo  
**Rollback:** GitHub org/repo rename back — GitHub provides redirects, but redirects are not permanent

### Prerequisite

Dedicated ADR required before this wave. The following sequencing issue must be resolved:

Current state:
- `github.com/banzami/banzami` (kernel)
- `github.com/banzami/banzamia` (AI OS)
- `github.com/banzami/banza` (operator)

After inversion, proposed state:
- `github.com/banzami/banza` (kernel — currently the operator repo name)
- `github.com/banzami/banzai` (AI OS)
- `github.com/banzami/banzami` (operator — currently the kernel repo name)

**Conflict:** The kernel wants to become `banza` but that name is currently occupied by the operator repo. The operator repo wants to become `banzami` but that name is currently occupied by the kernel repo. This is a swap, not a rename. GitHub does not support atomic swaps — temporary names are required.

Proposed sequence:
1. Rename operator `banza` → `banzami-operator-temp`
2. Rename kernel `banzami` → `banza`
3. Rename AI OS `banzamia` → `banzai`
4. Rename operator `banzami-operator-temp` → `banzami`

### GitHub organization rename (optional, deferred)

Renaming `github.com/banzami` → `github.com/banza` changes ALL repo URLs simultaneously. GitHub provides redirects but they are not permanent. This is a separate decision.

### Commit message

```
chore(repo): Wave 8 — repository renames per ADR-025 (separate ADR-026 required)
```

---

## Wave 9 — Final Cleanup

**Scope:** Remaining stragglers, directory renames, filename renames.  
**Risk:** Low  
**Rollback:** `git revert`

### Actions

| Action | Details |
|--------|---------|
| Rename `docs/images/architecture/banzamia-*.svg` files | → `banzai-*.svg` — update all markdown references |
| Rename `apps/docs/public/images/architecture/banzamia-*.svg` | Mirror above |
| Rename `apps/docs/app/banzamia/` directory | → `apps/docs/app/banzai/` (if conflict C-004 resolved) |
| Rename `apps/docs/components/banzamia/` directory | → `components/banzai/` |
| Rename `apps/banzamia/` in Banzami repo (if it exists) | → `apps/banzai/` |
| Rename `docker/banzamia/` directory in Banzami repo | → `docker/banzai/` |
| BANZAMI_REFERENCE.md filename | If conflict C-006 resolved |
| Final cross-repo consistency check | Grep all three repos for remaining unclassified occurrences |

### Commit message

```
chore(naming): Wave 9 — final cleanup, directory and filename renames
```

---

## Wave Summary

| Wave | Scope | Est. Files | Risk | Blocker |
|------|-------|------------|------|---------|
| 1 | Documentation (prose) | 30–40 | Low | None |
| 2 | SVG diagrams | 8–10 | Low–Medium | None |
| 3 | Website copy | 15–20 | Medium | Resolve C-004 (URL path) |
| 4 | BanzAI UI components | 20–25 | Medium | Wave 3 complete; resolve C-005 |
| 5 | APIs, env vars, Docker | 10–15 | High | Coordinate with production |
| 6 | SDKs | 30–40 | Critical | Resolve C-001, C-002 |
| 7 | Rust crates, code symbols | 60–80 | Medium | Wave 6 decisions final |
| 8 | GitHub repos | N/A | Critical | Separate ADR; resolve sequencing |
| 9 | Final cleanup | 10–15 | Low | All previous waves complete |
