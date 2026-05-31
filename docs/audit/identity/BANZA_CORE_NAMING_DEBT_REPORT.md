# BANZA CORE NAMING DEBT REPORT

**Audit ID:** BANZA-BANZAMI-CONTAMINATION-AUDIT-001  
**Date:** 2026-05-31  
**Focus:** All `banzami-*` named artifacts that implement BANZA protocol primitives

This report documents the full scope of the crate/package/tool naming debt and proposes canonical BANZA names. No renames are performed here — this is a planning document.

---

## Why this is debt, not a bug

The `banzami-*` crate names predate ADR-025. At the time, the protocol and the operator shared a name. The naming inversion (ADR-025, 2026-05-29) established that BANZA is the open protocol and Banzami is one operator. The kernel crates were not renamed because:

1. Renaming Rust crates with downstream dependents is a breaking change.
2. The `~/banzami` repo depends on these crates directly.
3. The `docs/governance/CLAUDE_BASE.md` explicitly marks them as "out of scope" for the current migration wave.

This report establishes the canonical target names and the migration complexity for when the rename is eventually approved.

---

## Kernel crates (19 crates)

| Current name | Proposed canonical name | Purpose |
|---|---|---|
| `banzami-types` | `banza-types` | Shared financial primitives: `Money`, `Currency`, typed IDs |
| `banzami-ledger` | `banza-ledger` | Double-entry ledger engine — core financial truth |
| `banzami-wallets` | `banza-wallets` | Merchant wallet engine, ledger-backed balances |
| `banzami-consumer-wallets` | `banza-consumer-wallets` | Consumer wallet engine |
| `banzami-transactions` | `banza-transactions` | Transaction lifecycle FSM |
| `banzami-transfers` | `banza-transfers` | P2P wallet-to-wallet transfers |
| `banzami-qr` | `banza-qr` | QR code lifecycle and payload encoding |
| `banzami-settlement` | `banza-settlement` | Settlement batch lifecycle |
| `banzami-reconciliation` | `banza-reconciliation` | External statement reconciliation |
| `banzami-acquiring` | `banza-acquiring` | Acquiring layer provider trait |
| `banzami-routing` | `banza-routing` | Payment rail routing engine |
| `banzami-identity` | `banza-identity` | `@handle` identity and namespace |
| `banzami-merchants` | `banza-merchants` | Merchant onboarding and API key management |
| `banzami-payment-links` | `banza-payment-links` | Shareable payment links |
| `banzami-payouts` | `banza-payouts` | Outbound disbursement model |
| `banzami-risk` | `banza-risk` | Risk limit framework |
| `banzami-compliance` | `banza-compliance` | KYC/KYB status tracking |
| `banzami-notifications` | `banza-notifications` | Notification provider trait |
| `banzami-capabilities` | `banza-capabilities` | Operator capability model and manifests |

---

## Conformance tool

| Current | Proposed | Notes |
|---|---|---|
| `tools/banzami-conformance/` | `tools/banza-conformance/` | Rename directory + update all invocations |

---

## SDK packages

| SDK | Current | Proposed |
|---|---|---|
| Go module | `github.com/banzami/banzami-go` | `github.com/banza-protocols/banza-go` |
| Go package | `banzami` | `banza` |
| PHP class | `BanzamiClient` | `BanzaClient` |
| PHP exception | `BanzamiException` | `BanzaException` |
| PHP facade | `Banzami::` | `Banza::` |
| PHP composer pkg | `banzami/sdk-php` | `banza/sdk-php` |
| PHP config | `banzami.php` | `banza.php` |
| Laravel provider | `BanzamiServiceProvider` | `BanzaServiceProvider` |
| WooCommerce plugin | `banzami-payment` | `banza-payment` |
| Generic Laravel pkg | `banzami/banzami-laravel` | `banza/banza-laravel` |

---

## Protocol URL surface

| Current | Proposed | Breaking? |
|---|---|---|
| `/.well-known/banzami/operator.json` | `/.well-known/banza/operator.json` | Yes — all operators must update routes |
| `/.well-known/banzami-operator.json` (RFC-0005 alt) | `/.well-known/banza-operator.json` | Yes |
| `https://banzami.com/conformance/...` ($id URIs) | `https://banza.network/conformance/...` | Yes with deprecation |

---

## Env var naming

| Current | Proposed | Files affected |
|---|---|---|
| `BANZAMI_GATEWAY_URL` | `BANZA_GATEWAY_URL` | `integrations/plugins/generic-laravel/README.md` and PHP integration |
| `BANZAMI_WEBHOOK_SECRET` | `BANZA_WEBHOOK_SECRET` | All integration plugin examples, Python examples, TS examples |
| `BANZAMI_API_KEY` | `BANZA_API_KEY` | Integration examples throughout |

---

## Migration complexity assessment

### Tier 1 — Metadata only (no API impact, safe to apply immediately)
- `core/Cargo.toml` repository + authors fields
- `core/README.md` dependency examples
- `README.md` dependency examples
- `docs/BANZAMI_REFERENCE.md` — move out of BANZA repo

### Tier 2 — Docs only (no code impact, apply in one PR)
- All error string references to `Banzami-Signature` in `sdk/python/`
- `sdk-certification/vectors/webhook_signatures.json` header format field
- `integrations/plugins/generic-node/` header name references
- `docs/stability.md:57`
- `CLAUDE.md:114` stale matrix reference
- Env var names in docs/examples

### Tier 3 — Conformance schema `$id` URIs (requires deprecation period)
- 3 conformance schema files
- Must publish schemas at new URI and accept both during transition

### Tier 4 — Well-known operator URL (coordinated protocol migration)
- RFC update: RFC-0005
- Conformance suite test paths
- Sandbox operator route
- All operator implementations must update
- Requires minimum 90-day deprecation per BANZA_GOVERNANCE.md

### Tier 5 — Rust crate renames (major migration)
- 19 crates
- Cargo.toml across `core/`, `reference/`, and `~/banzami/`
- All `use banzami_*` imports throughout kernel source
- `core/Cargo.lock` rebuild
- `reference/Cargo.lock` rebuild
- `~/banzami` workspace dependency update
- Documentation updates across entire repo
- Estimated scope: 200+ files

### Tier 6 — SDK package renames (published breaking changes)
- Go module path (git tag + module proxy)
- PHP Composer package name
- PHP class renames (affecting all PHP/Laravel integrations)
- WooCommerce plugin slug (WordPress plugin directory)
- Requires major version bump for all affected SDKs

---

## Risk if debt is NOT resolved

1. Any third-party operator implementing the BANZA protocol will import `banzami-types` and `banzami-ledger` — embedding Banzami's brand in their codebase.
2. The conformance schema `$id` URIs resolve to Banzami's servers — if Banzami were to cease operations (the scenario described in BANZA_MANIFESTO.md), the conformance infrastructure would break.
3. The `/.well-known/banzami/operator.json` path permanently associates the protocol's operator discovery API with Banzami's brand.
4. External operators cannot credibly claim they are implementing an open protocol when the kernel packages are named after one specific operator.

---

## Recommended resolution order

1. Tier 1 (metadata) — next commit
2. Tier 2 (docs/strings) — next commit or immediate following
3. Open ADR for Tier 4 (well-known URL) — requires community review
4. Tier 3 (schema URIs) — after ADR for Tier 4
5. Tier 5 (crate renames) — after BANZA Protocol v1.0 is tagged and stabilized
6. Tier 6 (SDK package renames) — coordinated with major SDK version releases
