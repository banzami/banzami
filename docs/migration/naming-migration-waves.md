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

- `BANZAMI_REFERENCE.md` (filename) — conflict C-006 pending resolution
- `banzami.org`, `contact@banzami.org` — protected
- Any code symbol
- Any URL or route (those go in Wave 3–5)
- Note: RFC normative text for `BANZAMI:`, `BANZAMI-SBX:`, `/.well-known/banzami/` **may** be updated in Wave 1 as prose (calling them "legacy" or "deprecated"), but the actual identifiers are migrated in Wave 5c

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

## Wave 5 — APIs, Environment Variables, Docker, Wire Format

Wave 5 is split into three sub-waves that must complete in sequence.

---

### Wave 5a — Environment Variables and Docker

**Scope:** All BANZAMIA_* env vars, Docker service names.  
**Repos:** BanzamIA, Banzami  
**Estimated files:** 8–10  
**Risk:** High — requires production coordination  
**Rollback:** Complex — requires coordinated rollback of server config

#### Prerequisite

Wave 4 must be complete. Coordinate with live server before beginning.

#### Files in scope

| File | Action |
|------|--------|
| `BanzamIA/.env.example` | Rename all BANZAMIA_* → BANZAI_* |
| `BanzamIA/docker/docker-compose.yml` | Rename service `banzamia` → `banzai`, image names, BANZAMIA_* → BANZAI_*, container names |
| `Banzami/docker/banzamia/docker-compose.yml` | Same |
| Production server `.env` files | **Coordinate with deploy — update simultaneously with code change** |
| CI/CD secrets | Rename BANZAMIA_* secrets in GitHub Actions |

#### Commit message

```
chore(infra): Wave 5a — rename BANZAMIA_* env vars and Docker services to BANZAI_*
```

---

### Wave 5b — BanzAI API Routes

**Scope:** BanzamIA Fastify router and frontend API client.  
**Estimated files:** 5–8  
**Risk:** Medium  
**Rollback:** `git revert` + deploy

#### Prerequisite

Wave 5a stable and deployed.

#### Files in scope

| File | Action |
|------|--------|
| BanzamIA Fastify router | `/banzamia/*` routes → `/banzai/*` routes |
| Frontend API client calling BanzamIA routes | Update base URL if using `/banzamia` prefix |

#### Note

`Banza-Signature` webhook header: **no rename needed** (C-009 resolved). After inversion, `Banza-Signature` correctly identifies a Banza-protocol signature. Update documentation only.

#### Commit message

```
chore(infra): Wave 5b — rename /banzamia API routes to /banzai
```

---

### Wave 5c — Wire Format Migration (Breaking Protocol)

**Scope:** QR payload prefixes, operator manifest discovery URL.  
**Estimated files:** 10–15  
**Risk:** High — affects deployed operators and generated QR codes  
**Rollback:** Revert generators and validators simultaneously; legacy codes still scan during compatibility window

#### Prerequisite

Wave 5b stable. Read `naming-breaking-protocol-migration.md` fully before beginning.

#### Actions

| Action | Details |
|--------|---------|
| QR generator | Change emitted prefix from `BANZAMI:` → `BANZA:` and `BANZAMI-SBX:` → `BANZA-SBX:` |
| QR validator | Accept both `BANZAMI:` and `BANZA:` prefixes; add deprecation warning when legacy prefix detected |
| Operator manifest discovery | Serve `/.well-known/banza/operator.json` as primary; serve `/.well-known/banzami/operator.json` as 301 redirect |
| Discovery clients (BanzamIA, conformance tools) | Fetch `/.well-known/banza/operator.json` first; fallback to legacy path during compatibility window |
| SVG labels referencing wire format strings | Update in Wave 2 if not already done; these are diagram labels — keep legacy string if the diagram is showing "what exists" |

#### Tests required

```
PASS: generator emits BANZA: (not BANZAMI:)
PASS: validator accepts BANZA:
PASS: validator accepts BANZAMI: with deprecation warning (compatibility window)
PASS: discovery client finds operator at /.well-known/banza/operator.json
PASS: discovery client follows 301 from /.well-known/banzami/ to canonical path
```

#### Commit message

```
feat(protocol): Wave 5c — wire format migration: BANZA: prefix, /.well-known/banza/ operator manifest
```

---

## Wave 6 — SDKs

**Scope:** SDK documentation updates, internal SDK rename, Python SDK rename.  
**Repos:** Banzami (sdk/), Banza (plugins/)  
**Estimated files:** 15–20  
**Risk:** Medium (C-001 resolved — no breaking class renames needed for published SDKs)  
**Rollback:** `git revert` for docs; semver patch for any published SDK updates

### Prerequisite

Wave 5c complete. C-001 and C-002 are resolved — no further prerequisite.

### Actions

| Action | Risk |
|--------|------|
| Checkout web SDK (internal): rename `BanzamiApiError` → `BanzaApiError` | Low — not published |
| Python SDK: rename `BanzamiAuthenticationError` → `BanzaAuthenticationError` | Medium — confirm consumers |
| TypeScript SDK (`@banza/sdk`): `BanzaClient`, `BanzaError`, `BanzaPay` stay — no rename needed | None |
| PHP SDK (`banza/sdk-php`): same — no class rename needed | None |
| Flutter SDK (`banza_flutter`): same — no class rename needed | None |
| All SDK docs: update `/webhooks/banzami` example → `/webhooks/banza` | Low |
| All SDK READMEs: update branding (BanzamIA → BanzAI where referenced) | Low |
| SDK docs: update env var examples (`BANZAMIA_API_URL` → `BANZA_API_URL` pattern) | Low |

### Commit message

```
docs(sdk): Wave 6 — SDK documentation and minor renames per ADR-025
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
| 1 | Documentation (prose) | 30–40 | Low | None — **ready now** |
| 2 | SVG diagrams | 8–10 | Low–Medium | None |
| 3 | Website copy | 15–20 | Medium | None (C-004 resolved: /banzai) |
| 4 | BanzAI UI components | 20–25 | Medium | Wave 3 complete |
| 5a | Env vars, Docker | 8–10 | High | Coordinate with production |
| 5b | BanzAI API routes | 5–8 | Medium | Wave 5a stable |
| 5c | Wire format (QR, manifest) | 10–15 | High | Wave 5b stable; see breaking-protocol-migration.md |
| 6 | SDKs (mostly docs) | 15–20 | Medium | Wave 5c complete (C-001 resolved: no class renames) |
| 7 | Rust crates, code symbols | 60–80 | Medium | Wave 6 complete |
| 8 | GitHub repos | N/A | Critical | Separate ADR required |
| 9 | Final cleanup | 10–15 | Low | All previous waves complete |
