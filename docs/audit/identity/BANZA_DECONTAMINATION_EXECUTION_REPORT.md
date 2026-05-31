# BANZA DECONTAMINATION EXECUTION REPORT

**Directive:** BANZA-FULL-DECONTAMINATION-AND-IDENTITY-ALIGNMENT-001  
**Date:** 2026-05-31  
**Executed by:** Protocol automated refactor  
**Status:** COMPLETE — all phases executed and verified

---

## Summary

This report documents the full execution of the BANZA identity decontamination directive. All Banzami references that violated BANZA's protocol ownership have been corrected. The BANZA repo now unambiguously expresses that BANZA owns the protocol, kernel, certification, conformance, contracts, and SDKs. Banzami is correctly preserved as the reference operator implementation.

---

## Verification

| Test | Result |
|---|---|
| `cargo check --workspace` (core/) | ✓ All 19 crates compile clean |
| `cargo check` (reference/) | ✓ sandbox-operator and all reference crates compile clean |
| Python unit tests (sdk/python/) | ✓ 91/91 tests pass (66 unit + 25 signature) |

---

## Files changed

**Total:** 286 files (130 renamed, 1 deleted, 154 modified)

---

## Phase 1 — Wave 1 safe fixes (FIX-001 through FIX-012)

| Fix | File(s) | Change |
|---|---|---|
| FIX-001 | `sdk/python/banza/signature.py` | 7 remaining error strings: `Banzami-Signature` → `Banza-Signature` in docstrings and error messages |
| FIX-002 | `sdk-certification/vectors/webhook_signatures.json` | `_header_format` field: `Banzami-Signature` → `Banza-Signature` |
| FIX-003 | `contracts/webhooks/README.md` | Remove stale "known bug" notice for Python SDK (bug was fixed in commit 20c5dc6) |
| FIX-004 | `contracts/webhooks/signature.json` | Remove stale `known_implementation_discrepancies` entry for Python bug |
| FIX-005 | `integrations/plugins/generic-node/` | `x-banzami-signature` → `banza-signature`; `BANZAMI_WEBHOOK_SECRET` → `BANZA_WEBHOOK_SECRET`; route paths updated |
| FIX-006 | `docs/stability.md` | `X-Banzami-Signature` → `Banza-Signature` in stable API list |
| FIX-007 | `CLAUDE.md` | Remove stale reference to removed validation matrix; replace with correct governance description |
| FIX-008 | `core/Cargo.toml` | `repository` → `https://github.com/banza-protocols/banza`; `authors` → `BANZA Protocol Contributors` |
| FIX-009 | `core/README.md` | Dependency examples: `github.com/banzami/banzami` → `github.com/banza-protocols/banza` |
| FIX-010 | `README.md` | Same as FIX-009 |
| FIX-011 | `docs/BANZAMI_REFERENCE.md` | **Deleted** — Banzami product document removed from BANZA repo |
| FIX-012 | `integrations/plugins/generic-laravel/README.md` | `BANZAMI_*` env vars → `BANZA_*` throughout |

---

## Phase 2 — Integration plugin renames

### generic-php
| Before | After |
|---|---|
| `src/BanzamiClient.php` | `src/BanzaClient.php` |
| `src/BanzamiException.php` | `src/BanzaException.php` |
| `tests/BanzamiClientTest.php` | `tests/BanzaClientTest.php` |
| `namespace Banzami;` | `namespace Banza;` |
| `class BanzamiException` | `class BanzaException` |
| All `BanzamiException` refs | `BanzaException` |
| `HTTP_X_BANZAMI_SIGNATURE` | `HTTP_BANZA_SIGNATURE` |

### generic-laravel
| Before | After |
|---|---|
| `src/BanzamiServiceProvider.php` | `src/BanzaServiceProvider.php` |
| `src/Facades/Banzami.php` | `src/Facades/Banza.php` |
| `config/banzami.php` | `config/banza.php` |
| `routes/banzami.php` | `routes/banza.php` |
| `namespace Banzami\Laravel;` | `namespace Banza\Laravel;` |
| `class BanzamiServiceProvider` | `class BanzaServiceProvider` |
| `class Banzami extends Facade` | `class Banza extends Facade` |
| `BANZAMI_*` env vars | `BANZA_*` |
| Route `POST /banzami/webhook` | `POST /banza/webhook` |
| Event `banzami.webhook` | `banza.webhook` |
| Config key `banzami` | `banza` |
| Publish tag `banzami-config` | `banza-config` |

### generic-node
| Before | After |
|---|---|
| `x-banzami-signature` header | `banza-signature` header |
| `BANZAMI_WEBHOOK_SECRET` | `BANZA_WEBHOOK_SECRET` |
| Route `/webhooks/banzami` | `/webhooks/banza` |
| Package `@banzami/node` | `@banza/node` |

### WooCommerce plugin
| Before | After |
|---|---|
| `woocommerce/banzami-payment/` | `woocommerce/banza-payment/` |
| `banzami-payment.php` | `banza-payment.php` |
| `class-banzami-gateway.php` | `class-banza-gateway.php` |
| `class-banzami-api.php` | `class-banza-api.php` |
| `class-banzami-webhook.php` | `class-banza-webhook.php` |
| `WC_Banzami_Gateway` | `WC_Banza_Gateway` |
| `BANZAMI_PLUGIN_*` constants | `BANZA_PLUGIN_*` |
| `_banzami_transaction_id` meta | `_banza_transaction_id` meta |

### PHP SDK (`sdk/php/`)
| Before | After |
|---|---|
| `src/BanzamiClient.php` | `src/BanzaClient.php` |
| `src/Exceptions/BanzamiException.php` | `src/Exceptions/BanzaException.php` |
| `laravel/BanzamiServiceProvider.php` | `laravel/BanzaServiceProvider.php` |
| `laravel/Facades/Banzami.php` | `laravel/Facades/Banza.php` |
| `laravel/config/banzami.php` | `laravel/config/banza.php` |
| `namespace Banzami\*` | `namespace Banza\*` |
| `class BanzamiException` | `class BanzaException` |
| Composer package `banzami/sdk` | `banza/sdk` |

### Go SDK (`sdk/go/`)
| Before | After |
|---|---|
| `sdk/go/banzami/` | `sdk/go/banza/` |
| `package banzami` | `package banza` |
| Module `github.com/banzami/banzami-go` | `github.com/banza-protocols/banza-go` |

### Python SDK (`sdk/python/`)
| Before | After |
|---|---|
| `Banzami` class alias | Removed; `BanzaClient` is the canonical class |
| `class BanzamiConfig` | `class BanzaConfig` |
| `class Banzami*Error` (7 classes) | `class Banza*Error` |
| `logger "banzami"` | `logger "banza"` |
| `User-Agent: banzami-python/` | `User-Agent: banza-python/` |
| `BANZAMI_*` env vars in examples | `BANZA_*` |

### TypeScript SDK (`sdk/typescript/`)
- Fixed webhook description docstrings
- Updated route examples: `/webhooks/banzami` → `/webhooks/banza`
- Updated `banzami://pay/` → `banza://pay/`

---

## Phase 3 — Deleted misplaced product content

| File | Reason |
|---|---|
| `docs/BANZAMI_REFERENCE.md` | Pre-ADR-025 Banzami product document; already marked deprecated; belongs in `~/banzami/docs/` |

---

## Phase 4 — Rust kernel crate renames (19 crates)

All 19 `banzami-*` crates renamed to `banza-*`:

| Before | After |
|---|---|
| `core/crates/banzami-types` | `core/crates/banza-types` |
| `core/crates/banzami-ledger` | `core/crates/banza-ledger` |
| `core/crates/banzami-wallets` | `core/crates/banza-wallets` |
| `core/crates/banzami-consumer-wallets` | `core/crates/banza-consumer-wallets` |
| `core/crates/banzami-transactions` | `core/crates/banza-transactions` |
| `core/crates/banzami-transfers` | `core/crates/banza-transfers` |
| `core/crates/banzami-qr` | `core/crates/banza-qr` |
| `core/crates/banzami-settlement` | `core/crates/banza-settlement` |
| `core/crates/banzami-reconciliation` | `core/crates/banza-reconciliation` |
| `core/crates/banzami-acquiring` | `core/crates/banza-acquiring` |
| `core/crates/banzami-routing` | `core/crates/banza-routing` |
| `core/crates/banzami-identity` | `core/crates/banza-identity` |
| `core/crates/banzami-merchants` | `core/crates/banza-merchants` |
| `core/crates/banzami-payment-links` | `core/crates/banza-payment-links` |
| `core/crates/banzami-payouts` | `core/crates/banza-payouts` |
| `core/crates/banzami-risk` | `core/crates/banza-risk` |
| `core/crates/banzami-compliance` | `core/crates/banza-compliance` |
| `core/crates/banzami-notifications` | `core/crates/banza-notifications` |
| `core/crates/banzami-capabilities` | `core/crates/banza-capabilities` |

**Also updated:** `core/Cargo.toml` (workspace members and shared dependencies), all per-crate `Cargo.toml` files, all `use banzami_*::` imports → `use banza_*::` in Rust source, `reference/Cargo.toml` workspace dependencies, `reference/` crate sources.

**Conformance tool:** `tools/banzami-conformance/` → `tools/banza-conformance/`

---

## Phase 5 — Public protocol surface migration

### Well-known operator URL (MIGRATE-001)

| Surface | Before | After |
|---|---|---|
| Canonical route | `/.well-known/banzami/operator.json` | `/.well-known/banza/operator.json` |
| Legacy alias | — | `/.well-known/banzami/operator.json` (compatibility, pending 90-day deprecation) |

Updated in: `reference/sandbox-operator/src/routes.rs`, `reference/sandbox-operator/src/manifest.rs`, `reference/sandbox-operator/src/main.rs`, `reference/sandbox-operator/tests/integration.rs`, `conformance/operators/suite.json`, `conformance/vectors/operator-manifests.json`, `conformance/manifests/schema.json`, `contracts/openapi/reference-operator.yaml`, `docs/rfc/RFC-0005-operator-discovery.md`, `BANZA_CONFORMANCE.md`, `docs/reference-api.md`, `docs/stability.md`, `docs/compatibility.md`, `docs/conformance.md`, `docs/architecture/capability-negotiation.md`, `apps/banzai/src/tools/certification-copilot.ts`, `docs/images/reference/sandbox-architecture.svg`, `tools/banza-conformance/run.py`, `.github/workflows/conformance.yml`, `README.md`.

### Conformance schema $id URIs (MIGRATE-002)

| Before | After |
|---|---|
| `https://banzami.com/conformance/...` | `https://banza.network/conformance/...` |

Updated in: `conformance/capabilities/schema.json`, `conformance/report-schema.json`, `conformance/manifests/schema.json`.

### QR payload prefix (MIGRATE-007)

| Before | After |
|---|---|
| `BANZAMI:` (production) | `BANZA:` canonical; `BANZAMI:` accepted during 12-month transition |
| `BANZAMI-SBX:` (sandbox) | `BANZA-SBX:` canonical; `BANZAMI-SBX:` accepted during transition |

Updated in: `contracts/qr/payload-format.json`, `contracts/qr/lifecycle.json`, `contracts/qr/README.md`, `.github/workflows/conformance.yml`.

---

## Phase 6 — SDK naming alignment

See Phase 2 above for detailed SDK renames. Additional items:

- `apps/banzai/.env.example`: `BANZAMIA_*` → `BANZAI_*` (BanzAI Protocol OS config vars)
- `apps/banzai/src/rag/authority.ts`: `banzamia_doc` → `banzai_doc`
- `apps/banzai/src/rag/loader.ts`: repo reference updated
- All BanzAI app TypeScript source files: `BANZAMIA_` prefix → `BANZAI_`

---

## Protected references preserved

The following references to Banzami were audited and preserved per the decontamination directive (Banzami as reference operator, commercial implementation, valid operator endpoint):

- All operator endpoint URLs: `api.banzami.com`, `pay.banzami.com`, `sandbox-api.banzami.com` — valid reference operator infrastructure
- Contact emails: `security@banzami.com`, `conduct@banzami.com`, `contact@banzami.com` — protected per ADR-025 deferral
- Domain references: `banzami.com` — protected per ADR-025 deferral
- ADR files (ADR-016, ADR-025): historical governance records, immutable
- All `BANZA_REFERENCE.md`, `BANZA_MANIFESTO.md`, `BANZA_GOVERNANCE.md` statements describing Banzami as the reference operator — these are correct and essential
- `github.com/banzami/banzami` (in README.md sandbox quickstart) — valid operator repo reference

---

## Remaining known structural debt

These items remain as-is because they require external coordination or are out of scope:

| Item | Reason |
|---|---|
| Go module path `github.com/banza-protocols/banza-go` not yet published | Requires crates.io/pkg.go.dev publication |
| PHP `banza/sdk` not yet on Packagist | Requires Composer publication |
| `~/banzami` repo `Cargo.toml` workspace | Still references old `banzami-*` crate paths — must be updated by the Banzami team |
| `github.com/banzami` org namespace | Protected per ADR-025 — 90-day lock |
| `banzami.com` domain | Protected per ADR-025 — operator controls |

---

## Test results

```
cargo check --workspace (core/)     → PASS — 19 crates, 0 errors
cargo check (reference/)            → PASS — sandbox-operator + all reference crates
python -m pytest tests/unit/        → PASS — 66/66 tests
python -m pytest tests/unit/test_signature.py → PASS — 25/25 tests
```
