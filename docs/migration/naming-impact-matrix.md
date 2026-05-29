# Naming Inversion — Impact Matrix

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29

---

## Risk Legend

| Level | Definition |
|-------|-----------|
| **Low** | Self-contained change. Findable with grep. No external consumers. Rollback: revert commit. |
| **Medium** | Multi-file change with internal dependencies. Potential for missed occurrences. Rollback: revert commit + CI validation. |
| **High** | Affects external consumers, deployed systems, or cross-repo coordination. Rollback complex. |
| **Critical** | Breaking change for external parties, published packages, or protocol contracts. Requires deprecation period and version coordination. |

---

## Matrix

### Documentation

**Risk: Low**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| ADRs in `docs/adr/` | ~30 files, ~200 occurrences | Internal docs. Grep-findable. ADR-016 superseded by ADR-025. |
| BANZAMI_REFERENCE.md | 1 file, ~80 occurrences | Single file; changes visible immediately on docs site. Filename itself is a conflict (see conflicts doc). |
| RFCs in `docs/rfc/` | ~8 files, ~40 occurrences | Internal protocol specs. Protocol-level terms (BANZAMI: QR prefix, /.well-known/banzami/) must not be renamed even in documentation. |
| GOVERNANCE.md, CONTRIBUTING.md | 2 files, ~30 occurrences | Foundational docs. Low risk but high visibility. |
| README files (all repos) | 3 files, ~60 occurrences | First thing developers see. Medium-visibility, low technical risk. |
| Migration docs (this wave's own docs) | ~6 files | These docs use all name forms intentionally — do not rename within migration docs themselves. |

**Action:** Wave 1. Classify each occurrence before editing. Do not rename QR prefixes or protocol discovery URLs even when they appear in documentation prose.

---

### SVG Diagrams

**Risk: Low–Medium**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| Architecture SVGs (kernel repo) | 4 SVG files, ~40 text labels | Text nodes must be edited carefully; SVGs use exact positioning. Verify visually after. |
| Product architecture SVG | 1 file, ~20 labels | `banzamia-product-architecture.svg` — labels, module names, tagline. |
| Canonical architecture SVG | 1 file, ~15 labels | `banzamia-canonical-architecture.svg` — labels in 5-layer stack. |
| QR lifecycle SVG | 1 file | Contains `BANZAMI-SBX:` as protocol data label — **do not rename this text**. |
| Sandbox architecture SVG | 1 file | Contains `/.well-known/banzami/operator.json` as a label — **do not rename this text**. |

**Action:** Wave 2. Edit SVG text nodes manually. Keep all protocol contract strings unchanged even in diagrams.

---

### Website Copy (banzami.org)

**Risk: Medium**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| Page metadata (title, description, OG) | ~8 pages | SEO impact if changed; crawlers may temporarily show old names. |
| Navigation text | ~5 occurrences | Sidebar, header, footer links referencing BanzamIA → BanzAI. |
| Body copy (banzamia.org pages) | ~40 occurrences | Product descriptions, capability tables, welcome text. |
| App store notes | ~60 occurrences | Banza Business → Banzami Business; Banza Wallet → Banzami Wallet; submitted to Apple/Google. |
| Roadmap page | ~10 occurrences | Module labels, roadmap descriptions. |
| BanzamIA route (`/banzamia`) | 1 route | URL slug on banzami.org — changing this is a breaking change for bookmarks/links. **CONFLICT — see conflicts doc.** |

**Action:** Wave 3. Coordinate SEO. The `/banzamia` URL path conflict must be resolved before this wave begins.

---

### BanzAI UI (BanzamIA components)

**Risk: Medium**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| React component names | 5 components | `BanzamIAChat`, `BanzamIASidebar`, `BanzamIAApp`, `BanzamIAIcon`, `BanzamIASourcesPanel` — internal to docs app, no external consumers. |
| Component file names | 5 files | `BanzamIAChat.tsx` etc. File renames require import updates in all importing files. |
| UI text strings | ~15 occurrences | Welcome text, placeholder text, aria labels, footer text. |
| Import paths | ~10 occurrences | `import { BanzamIAChat }` in `BanzamIAApp.tsx` and pages. Must update all. |
| Module route `/banzamia` (docs site) | 1 file | `app/banzamia/page.tsx` — canonical route is `/banzai`. Add permanent redirect from `/banzamia`. C-004 resolved. |

**Action:** Wave 4. Use IDE rename for component symbols to catch all imports. File renames require manual import updates. C-004 is resolved: canonical route is `/banzai`, redirect `/banzamia` → `/banzai` via `next.config.js`.

---

### Backend APIs

**Risk: Critical (protocol routes) / Medium (BanzamIA internal routes)**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| `/.well-known/banzami/operator.json` | ~8 files | **Breaking protocol migration.** Canonical: `/.well-known/banza/operator.json`. Legacy path serves 301 redirect. See `naming-breaking-protocol-migration.md`. Wave 5c. |
| `BANZAMI-SBX:` QR prefix | ~5 files | **Breaking protocol migration.** Canonical: `BANZA-SBX:`. Generators emit new prefix; validators accept both during compatibility window. Wave 5c. |
| `BANZAMI:` production QR prefix | ~3 files | **Breaking protocol migration.** Canonical: `BANZA:`. Same strategy. Wave 5c. |
| `/webhooks/banzami` (SDK docs/examples) | ~4 files | Documentation only. Rename to `/webhooks/banza` in Wave 6. |
| BanzamIA internal API routes (`/banzamia/*`) | ~12 routes | Internal. Canonical: `/banzai/*`. Coordinate with frontend route rename. Wave 5b. |
| `Banza-Signature` webhook header | ~5 files | **No rename needed (C-009 resolved).** After inversion, "Banza" = protocol, so `Banza-Signature` is already correct. Update documentation only. |

**Action:** Wire protocol identifiers (/.well-known, QR prefixes) are migrated as part of the naming inversion — this is a breaking protocol migration, versioned and tested. See `naming-breaking-protocol-migration.md`. BanzamIA internal routes rename in Wave 5b. Wire format changes in Wave 5c.

---

### SDKs

**Risk: Critical**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| TypeScript SDK (published `@banza/sdk`) | ~30 class/function refs | `BanzaClient`, `BanzaError`, `BanzaApiError` — published npm package. Changing class names is a breaking API change for all downstream users. Requires semver major bump and deprecation plan. |
| PHP SDK (`banza/sdk-php`) | ~15 refs | Same as TS SDK. Composer package. |
| Flutter SDK (`banza_flutter`) | ~8 refs | `BanzaPay` class. pub.dev package. |
| Python SDK (`banza` package) | ~5 refs | `BanzamiAuthenticationError` — this is a PRODUCT-named error in a PROTOCOL-named SDK. Pre-existing inconsistency; classify before renaming. |
| Node plugin (`@banza/node`) | ~10 refs | Internal usage primarily; npm package. |
| Checkout web SDK (internal) | ~5 refs | `BanzamiApiError` — internal SDK, not published. Can rename without deprecation. |

**Action:** Wave 6. C-001 resolved: `@banza/sdk`, `BanzaClient`, `BanzaError`, `BanzaPay` are already correct after inversion — no class renames needed. Wave 6 is primarily documentation updates and the `BanzamiAuthenticationError` rename in the Python SDK. Risk drops from Critical to Medium.

---

### Rust Crates

**Risk: Medium (internal) / High (if crates become public)**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| 21 workspace crates (`banzami-*`) | ~63 total files | All crates are currently internal (not published to crates.io). Free to rename without deprecation — but renaming 21 crates is a large coordinated change. All inter-crate dependencies must be updated simultaneously. |
| Rust integration tests | ~3 test files | Must update crate name in `Cargo.toml` deps of test crates. |

**Action:** Wave 7. Rename all 21 crates in a single coordinated commit (update workspace `Cargo.toml` + all `[dependencies]` blocks). Run `cargo build` to verify. Since crates are not published, no deprecation needed.

---

### NPM Packages

**Risk: Critical**

| Package | Current | Proposed | Notes |
|---------|---------|---------|-------|
| `@banza/sdk` | Published | **CONFLICT** | If "Banza" becomes the protocol name, this name becomes more correct (SDK for the Banza protocol). May not need renaming. See conflicts. |
| `@banza/node` | Published | **CONFLICT** | Same as above. |
| `@banzami/banzamia` | Internal root package | `@banza/banzai`? | Internal only — no external consumers. Rename in Wave 4. |
| `banzamia-client` (internal module) | Internal | `banzai-client`? | Internal only — rename in Wave 4. |

**Action (C-001 resolved):** `@banza/sdk` and `@banza/node` scopes are already correct after inversion — no rename needed. `@banzami/banzamia` → `@banza/banzai` (internal, rename in Wave 4; C-003 unresolved, defer to Wave 8).

---

### GitHub Repositories

**Risk: Critical**

| Repo | Current | Proposed | Notes |
|------|---------|---------|-------|
| `github.com/banzami/banzami` | Kernel | `github.com/banzami/banza`? | Rename breaks all existing clone URLs, CI badge links, fork references. Requires GitHub repo rename + redirect. |
| `github.com/banzami/banzamia` | AI OS | `github.com/banzami/banzai`? | Same. |
| `github.com/banzami/banza` | Operator | `github.com/banzami/banzami`? | If kernel becomes `banza`, there's a namespace collision — current `banza` repo must rename first. Ordering matters. |
| GitHub organization `banzami` | Org | `banza`? | Changing org name changes ALL repo URLs under the org simultaneously. Extreme coordination required. |

**Action:** Wave 8. Requires dedicated planning. GitHub org rename is highest-risk single action in this migration — deferred to a separate ADR.

---

### CI/CD

**Risk: High**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| Workflow file names | ~3 files | `.github/workflows/` — file names may reference repo names |
| Workflow env vars | ~5 refs | BANZAMIA_* vars in CI secrets and workflow steps |
| Docker image names | ~4 refs | `docker/banzamia/docker-compose.yml` — service names, image tags |
| Deploy scripts | 1 (`deploy.sh`) | References service names; currently `docs-frontend` is BanzamIA-agnostic |

**Action:** Wave 5 (env vars) / Wave 8 (repo-level CI changes). Update CI secrets in coordination with env var rename.

---

### Docker / Containers

**Risk: Medium**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| `docker/banzamia/docker-compose.yml` | 1 file, ~18 refs | Service name `banzamia`, image `banzamia-api`, 12 BANZAMIA_* env vars |
| `docker/banzamia/Dockerfile` | 1 file | Image definition for BanzamIA service |
| BanzamIA standalone `docker-compose.yml` | 1 file, ~11 refs | Same pattern as above |
| Container service names | ~4 | `banzamia`, `banzamia-api`, `banzamia-web` — internal Docker network names only |

**Action:** Wave 5. Rename Docker service names and env vars simultaneously. Coordinate with live deployment.

---

### Environment Variables

**Risk: High**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| BANZAMIA_* vars (11 distinct vars) | 4 files, ~38 total | Must update simultaneously: `.env.example`, `docker-compose.yml` (both repos), all server `.env` files on production. Missing one env var causes silent runtime failure. |
| RUST_LOG filter (`banzami=debug`) | ~3 files | Low-stakes — log filtering only. Rename when crates rename. |

**Action:** Wave 5. Requires coordinated deployment update. Cannot rename docs without renaming server config simultaneously.

---

### Database Schemas

**Risk: Low**

| Sub-area | Notes |
|----------|-------|
| No brand-named tables detected | Migration files in `db/migrations/` did not reveal brand names in table or column identifiers. |

**Action:** No action required.

---

### Test Fixtures

**Risk: Low–Medium**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| SDK test files | ~9 files | Reference class names (BanzaClient, BanzaError, BanzamiWebhookSignatureError). Must update alongside code symbols. |
| BanzamIA query fixtures | ~3 files | Test question strings containing "banzami". Low risk — these are content, not identifiers. |

**Action:** Wave 7 (alongside code symbols). Run test suite after each symbol rename.

---

### SVG Diagrams (additional detail)

See SVG Diagrams section above. No additional notes.

---

### Certification Docs

**Risk: Low**

| Sub-area | Notes |
|----------|-------|
| Conformance docs (`docs/conformance.md`) | References Banzami certification levels and protocol. Rename Banzami → Banza in prose. L0–L4 level names unchanged. |
| `tools/banzami-conformance/` | Tool name rename → `banza-conformance` (Wave 7). |

---

### RFCs

**Risk: Low (prose) / Critical (protocol strings)**

| Sub-area | Notes |
|----------|-------|
| RFC prose text | ~8 RFC files with ~40 occurrences. Protocol references (Banzami Protocol → Banza Protocol) can be renamed in Wave 1. |
| RFC protocol strings (`BANZAMI:`, `BANZAMI-SBX:`, `/.well-known/banzami/`) | These are normative protocol identifiers in RFC text. **Must not be renamed** — they define the protocol wire format. A new RFC would be required to change them. |

---

### ADRs

**Risk: Low**

All ADRs except ADR-016 and ADR-025 use "Banzami" to mean the protocol. Update in Wave 1 documentation rename. ADR-016 is already superseded by ADR-025.

---

## Summary

| Category | Risk | Wave | Blocker? |
|----------|------|------|---------|
| Documentation | Low | 1 | No |
| SVG diagrams | Low–Medium | 2 | No |
| Website copy | Medium | 3 | No (C-004 resolved: /banzai canonical) |
| BanzAI UI | Medium | 4 | No (C-004 resolved) |
| APIs / env vars / Docker (5a+5b) | High | 5a–5b | Coordinate with production deploy |
| Wire format (5c) | High | 5c | After 5a–5b stable; see breaking-protocol-migration.md |
| SDKs | Medium | 6 | No (C-001 resolved: mostly docs updates) |
| Code symbols / Rust crates | Medium | 7 | After Wave 6 docs complete |
| GitHub repos / org | Critical | 8 | Separate ADR required |
| Final cleanup | Low | 9 | After all above |
