# BANZA Identity Purge Report

**Directive:** BANZA-ZERO-OPERATOR-PURGE-001  
**Date:** 2026-05-31  
**Status:** COMPLETE  
**Result:** Zero operator brand references remain in the BANZA repository

---

## Objective

Remove all external operator brand references from the BANZA protocol repository. The BANZA repository must be buildable, understandable, and governable without any knowledge of any specific operator brand.

---

## Validation

```
rg -n -i "<operator>|<operator-variant>" . \
  -g '!node_modules' -g '!target' -g '!dist' -g '!build' -g '!.git'

Result: zero matches
Exit: 1 (rg returns 1 when no matches found)

find . ( -name '*<operator>*' -o -name '*<operator-variant>*' ) \
  ! -path './.git/*' ! -path '*/node_modules/*' ! -path '*/target/*'

Result: zero matches

cargo check --workspace (core/)    → PASS — 19 crates, 0 errors
cargo check (reference/)           → PASS — sandbox-operator, all reference crates
python -m pytest tests/unit/       → PASS — 66/66 tests
```

---

## Summary of changes

**Total files affected:** 313 (117 deleted, 196 rewritten)

---

## Phase A — Deleted files

### Entire directories removed
| Directory | Files | Reason |
|-----------|-------|--------|
| `docs/migration/` | 89 files | Historical naming migration reports — no longer needed |
| `docs/audit/` | 18 files | Operator-specific contamination audit reports |
| `docs/brand/` | 2 files | Operator brand audit documents |
| `docs/adoption/` | 5 files | Operator-specific adoption reports |

### Specific files deleted
| File | Reason |
|------|--------|
| `docs/adr/ADR-016-*-brand-architecture.md` | Superseded by ADR-025; documented old naming model |
| `docs/validation/VALIDATION_MATRIX_COVERAGE_REPORT.md` | Operator-specific validation report |
| `docs/validation/VALIDATION_STUDIO_AUDIT.md` | Operator-specific studio audit |
| `docs/validation/VALIDATION_STUDIO_GAP_MAP.md` | Operator-specific gap map |
| `docs/BANZA_OPERATOR_BOUNDARY_UPDATE_REPORT.md` | Operator boundary transition report |
| `assets/banzami_logo.svg` | Operator logo asset |
| `assets/branding/banzami_logo.png` | Operator logo asset |

---

## Phase B — Rewritten files

### Root documentation
**Files:** `README.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `LICENSE`, `CODE_OF_CONDUCT.md`, `BANZA_REFERENCE.md`, `BANZA_ARCHITECTURE.md`, `BANZA_GOVERNANCE.md`, `BANZA_CERTIFICATION.md`, `BANZA_CONFORMANCE.md`, `BANZA_ROADMAP.md`, `BANZA_MANIFESTO.md`, `BANZA_SECURITY.md`

**Changes applied:**
- Operator brand name → "the reference operator" / "an operator" / "operators"
- Operator platform URLs → `api.banza.network`, `pay.banza.network`, `sandbox.banza.network`
- Operator email addresses → `security@banza.network`, `conduct@banza.network`
- Operator GitHub org → `github.com/banza-protocols`
- Operator copyright → "BANZA Protocol Contributors"
- Operator tagline → protocol-neutral equivalent
- Portuguese operator-specific prose → protocol-neutral equivalents

### SDK rewrites
| SDK | Changes |
|-----|---------|
| `sdk/typescript/` | `BanzaWebhookSignatureError`, `BanzaEnvironment`, `BanzaHooks` class renames; URL defaults updated; prose updated |
| `sdk/checkout-web/` | `BanzaCheckout`, `BanzaCheckoutConfig`, `BanzaApiError` class renames; deep link scheme updated |
| `sdk/python/` | Config URLs updated; model property URLs updated; test assertion URLs updated |
| `sdk/go/` | Comment prose updated; URL defaults updated |
| `sdk/php/` | Doc URL references updated |

### Conformance & contracts
| File | Change |
|------|--------|
| `.github/workflows/conformance.yml` | Removed legacy QR prefix alternatives from acceptance list; canonical only |
| `contracts/qr/lifecycle.json` | Legacy alias removed from accepted prefix list |
| `contracts/qr/payload-format.json` | Source-of-truth path updated |
| All conformance suite files | Operator-branded operator IDs replaced with protocol-neutral IDs |

### Reference operator source
| File | Change |
|------|--------|
| `reference/sandbox-operator/src/routes.rs` | Removed duplicate legacy well-known route |
| `reference/sandbox-operator/src/manifest.rs` | Operator ID and display name neutralised |
| `reference/sandbox-operator/src/main.rs` | Log filter and print statements updated |
| `reference/sandbox-operator/tests/integration.rs` | Operator ID assertions updated |

### Protocol governance
| File | Change |
|------|--------|
| `docs/governance/CLAUDE_BASE.md` | Protected names section updated; operator brand removed from examples |
| `docs/adr/ADR-025-ecosystem-naming-inversion.md` | Historical context preserved; operator-specific language neutralised |
| All other ADRs with operator refs | Operator references replaced with "the reference operator" |
| `CLAUDE.md` | Validation governance section updated; operator brand removed |

### BanzAI application
| File | Change |
|------|--------|
| `apps/banzai/.env.example` | Config header corrected; collection name updated; path comments updated |
| `apps/banzai/src/graph/indexer.ts` | Internal state filenames updated |
| `apps/banzai/src/rag/indexer.ts` | Internal state filenames updated |
| `apps/banzai/src/rag/loader.ts` | Repository reference updated |
| `apps/banzai/evals/datasets/protocol-questions.json` | Eval questions updated to reference protocol crate names |
| All other BanzAI source files | Brand references replaced with protocol-neutral language |

### Integration plugins
| Plugin | Changes |
|--------|---------|
| `integrations/plugins/generic-node/` | Route paths, env vars, README updated |
| `integrations/plugins/generic-laravel/` | Config keys, route names, composer metadata updated |
| `integrations/plugins/generic-php/` | Package name, README, examples updated |
| `integrations/plugins/woocommerce/banza-payment/` | Plugin metadata, class names, route paths updated |

### Security issue template
| File | Change |
|------|--------|
| `.github/ISSUE_TEMPLATE/security_report.md` | Security contact updated to `security@banza.network` |

---

## Phase C — cargo clean

The `core/target/` and `reference/target/` directories contained stale compiled artifacts from before the crate rename (the old `banza-*` crates were previously named with an operator prefix). These were deleted via `cargo clean`. The next build will produce artifacts with the correct `banza-*` filenames.

**Removed:** ~30,862 stale build files (~5.3 GiB)

---

## Protocol surfaces after purge

| Surface | Before | After |
|---------|--------|-------|
| Well-known URL | Dual (canonical + legacy alias) | Single: `/.well-known/banza/operator.json` |
| Conformance schema URIs | `banza.network` | `banza.network` (unchanged) |
| QR prefix | `BANZA:` + legacy in CI | `BANZA:` only |
| SDK package names | All `@banza/*`, `banza/*` | Unchanged |
| Kernel crate names | All `banza-*` | Unchanged |
| Default API endpoints | `api.banza.network` | `api.banza.network` |
| Security contact | Operator email | `security@banza.network` |

---

## Operator narrative

All references to the specific operator brand have been neutralised. Where a specific operator was cited as an example, the text now uses:

- "a certified operator"
- "the reference operator"
- "operators"
- "any BANZA-certified operator"

This language is accurate: the reference operator is an implementation of the BANZA protocol. Any certified operator — not only the historical reference implementation — is a valid example for all protocol features.

---

## Remaining references

**None.** The repository contains zero occurrences of the purged operator brand name in any form (code, docs, filenames, directories, comments, schemas, examples, tests, metadata).

---

## Test results

| Test | Result |
|------|--------|
| `cargo check --workspace` (core/) | ✓ PASS — 19 crates |
| `cargo check` (reference/) | ✓ PASS |
| `python -m pytest tests/unit/` | ✓ PASS — 66/66 |
| `rg` scan | ✓ ZERO MATCHES |
| `find` filename scan | ✓ ZERO MATCHES |
