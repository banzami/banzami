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
| Module route `/banzamia` (docs site) | 1 file | `app/banzamia/page.tsx` — URL path change is a breaking link. **CONFLICT.** |

**Action:** Wave 4. Use IDE rename for component symbols to catch all imports. File renames require manual import updates. Resolve `/banzamia` URL conflict first.

---

### Backend APIs

**Risk: Critical (protocol routes) / Medium (BanzamIA internal routes)**

| Sub-area | Occurrences | Notes |
|----------|-------------|-------|
| `/.well-known/banzami/operator.json` | ~8 files | **CRITICAL — PUBLIC PROTOCOL CONTRACT.** All deployed operators have published this URL. Changing it breaks operator discovery for all certified operators. Cannot rename without a protocol version (RFC). |
| `BANZAMI-SBX:` QR prefix | ~5 files | **CRITICAL — ENCODED IN ALL GENERATED QR CODES.** Every QR code ever generated with this prefix would fail validation if the validator changes the prefix it expects. Cannot rename without a QR protocol version bump. |
| `BANZAMI:` production QR prefix | ~3 files | **CRITICAL** — same as above. |
| `/webhooks/banzami` (SDK docs/examples) | ~4 files | Low risk — these are example route paths in documentation, not actual API routes. Rename in SDK docs to `/webhooks/banza` in Wave 6. |
| BanzamIA internal API routes (`/banzamia/*`) | ~12 routes | Internal to BanzamIA service. Consumers are the docs site. Coordinate rename with frontend route update. Medium risk. |
| `Banza-Signature` webhook header | ~5 files | **CONFLICT — UNRESOLVED.** This header is part of the webhook verification protocol. After inversion, "Banza" = protocol, so "Banza-Signature" becomes more correct, not less. No rename needed. But confirm. |

**Action:** Protocol routes (/.well-known, QR prefixes) must NOT be renamed in this migration. BanzamIA internal routes rename in Wave 5.

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

**Action:** Wave 6. Published packages require a breaking-change release with deprecation. Internal-only SDKs (checkout-web) can rename freely. Must resolve SDK naming conflict (see conflicts doc) before beginning.

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

**Action:** Resolve SDK conflict first. Published packages may require no rename if "@banza" scope is already correct after inversion.

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
| Website copy | Medium | 3 | Resolve /banzamia URL conflict first |
| BanzAI UI | Medium | 4 | Resolve /banzamia URL conflict first |
| APIs / env vars / Docker | Medium–Critical | 5 | Coordinate with production deploy |
| SDKs | Critical | 6 | Resolve SDK naming conflict first |
| Code symbols / Rust crates | Medium | 7 | After SDK decision |
| GitHub repos / org | Critical | 8 | Separate ADR required |
| Final cleanup | Low | 9 | After all above |
