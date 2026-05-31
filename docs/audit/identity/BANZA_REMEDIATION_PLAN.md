# BANZA REMEDIATION PLAN

**Audit ID:** BANZA-BANZAMI-CONTAMINATION-AUDIT-001  
**Date:** 2026-05-31  
**Status:** APPROVED FOR REVIEW — no changes applied yet

---

## SAFE IMMEDIATE FIXES

These require no migration plan, no API changes, and no coordination. They can be applied in the next commit.

### FIX-001 — Python SDK remaining error message strings
**File:** `sdk/python/banza/signature.py`  
**What:** Error message strings still say "Banzami-Signature" in 7 places. The constant was already fixed (commit 20c5dc6); the internal docstrings and error messages were not.  
**Change:** Replace all remaining `Banzami-Signature` in error strings, docstrings, and `_parse_header` with `Banza-Signature`  
**Risk:** None — these are error strings and docstrings, not protocol surface  
**Affects public API:** No

### FIX-002 — SDK certification vector header format field
**File:** `sdk-certification/vectors/webhook_signatures.json:5`  
**What:** `"_header_format": "Banzami-Signature: t=..."` → `"Banza-Signature: t=..."`  
**Risk:** None — this is a comment/metadata field, not a test vector input  
**Affects public API:** No

### FIX-003 — `contracts/webhooks/README.md` — remove stale bug notice
**File:** `contracts/webhooks/README.md:20`  
**What:** The Python header bug was fixed in commit 20c5dc6. The notice is now stale.  
**Change:** Update to note the fix was applied  
**Risk:** None  
**Affects public API:** No

### FIX-004 — `contracts/webhooks/signature.json` — remove stale discrepancy entry
**File:** `contracts/webhooks/signature.json:174-177`  
**What:** Remove or update the `known_implementation_discrepancies` entry for the Python bug  
**Risk:** None  
**Affects public API:** No

### FIX-005 — Node integration plugin: `x-banzami-signature` → `banza-signature`
**Files:**  
- `integrations/plugins/generic-node/src/webhook.ts:17`  
- `integrations/plugins/generic-node/examples/webhook-express.ts:12`  
- `integrations/plugins/generic-node/README.md:247,280,302`  
**Change:** Replace `x-banzami-signature` with `banza-signature` (canonical lowercase HTTP header lookup)  
**Risk:** Low — example code; anyone using the wrong header is already broken  
**Affects public API:** Yes — this is example integration code that operators copy. But the current value is a bug, not a stable API.

### FIX-006 — `docs/stability.md:57` — wrong header in stable API list
**File:** `docs/stability.md:57`  
**What:** `X-Banzami-Signature` → `Banza-Signature`  
**Risk:** None  
**Affects public API:** No

### FIX-007 — `CLAUDE.md:114` — stale validation matrix reference
**File:** `CLAUDE.md:114`  
**What:** Remove or update the reference to `docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json`. This file was removed from the BANZA repo in commit 20c5dc6.  
**Risk:** None — affects AI operating instructions only  
**Affects public API:** No

### FIX-008 — `core/Cargo.toml:29-30` — wrong repository URL and authors
**File:** `core/Cargo.toml`  
**What:**  
- Line 29: `repository = "https://github.com/banzami/banzami"` → `"https://github.com/banza-protocols/banza"`  
- Line 30: `authors = ["Banzami Engineering <engineering@banzami.com>"]` → remove or replace  
**Risk:** None — Cargo metadata only. No code change.  
**Affects public API:** No

### FIX-009 — `core/README.md:72-73` — dependency examples point to wrong repo
**File:** `core/README.md`  
**What:** `git = "https://github.com/banzami/banzami"` → `git = "https://github.com/banza-protocols/banza"`  
**Risk:** None — documentation  
**Affects public API:** No

### FIX-010 — `README.md:275-276` — same as FIX-009 for root README
**File:** `README.md`  
**Risk:** None — documentation  
**Affects public API:** No

### FIX-011 — `docs/BANZAMI_REFERENCE.md` — move out of BANZA repo
**File:** `docs/BANZAMI_REFERENCE.md`  
**What:** Remove this Banzami product reference document from the BANZA repo. Replace with a one-line pointer to the Banzami repo.  
**Risk:** Low — if any external link points to this file in the BANZA repo, it will 404. A redirect note mitigates this.  
**Affects public API:** No

### FIX-012 — Integration plugins env var naming in documentation
**Files:** `integrations/plugins/generic-laravel/README.md` (BANZAMI_GATEWAY_URL, BANZAMI_WEBHOOK_SECRET)  
**What:** Change env var names in documentation to `BANZA_GATEWAY_URL`, `BANZA_WEBHOOK_SECRET`  
**Risk:** Low for new installations; existing installations using the old env var names will not break because the env var is just a name in their shell config  
**Affects public API:** No — env var names are not versioned

---

## MIGRATION REQUIRED

These changes require coordination, planning, and potentially ADRs before applying.

### MIGRATE-001 — Well-known operator URL: `/.well-known/banzami/operator.json` → `/.well-known/banza/operator.json`
**Scope:**  
- `docs/rfc/RFC-0005-operator-discovery.md` (RFC update required)
- `conformance/operators/suite.json` (test path update)
- `conformance/vectors/operator-manifests.json` (vector path update)
- `BANZA_CONFORMANCE.md` (docs)
- `reference/sandbox-operator/src/routes.rs` (route rename)
- All certified operators must update their implementations  

**ADR required:** Yes — the well-known URL is a protocol-level API surface  
**Deprecation period:** Minimum 90 days per BANZA_GOVERNANCE.md  
**Approach:** Serve both `/.well-known/banzami/operator.json` and `/.well-known/banza/operator.json` during transition period  
**Estimated effort:** Medium — ~20 files

### MIGRATE-002 — Conformance schema `$id` URIs: `banzami.com` → `banza.network`
**Scope:**  
- `conformance/manifests/schema.json`
- `conformance/capabilities/schema.json`
- `conformance/report-schema.json`  

**ADR required:** Yes — published JSON Schema IDs are external references  
**Approach:** Publish schemas at new URI, keep old URI pointing to new location via redirect  
**Estimated effort:** Low — 3 files

### MIGRATE-003 — Rust kernel crate renames (19 crates): `banzami-*` → `banza-*`
**Scope:** 19 crates in `core/crates/`, all their source files, `core/Cargo.toml`, `core/Cargo.lock`, `reference/Cargo.toml`, `reference/Cargo.lock`, `~/banzami/` workspace (external dependency update)  

**ADR required:** Yes — this is a major structural change to the protocol kernel  
**Semver:** Major version bump for all crates  
**Coordination required:** Must be coordinated with Banzami team (they depend on these crates)  
**Breaking for:** Any external operator who has added these crates as git dependencies  
**Deprecation period:** Minimum 90 days — re-export under old names during transition  
**Estimated effort:** High — 200+ files, coordinated multi-repo migration  
**Prerequisite:** MIGRATE-001 and MIGRATE-002 should be completed first

### MIGRATE-004 — Go SDK: module path `github.com/banzami/banzami-go` → `github.com/banza-protocols/banza-go`
**Scope:** `sdk/go/go.mod`, all `sdk/go/banzami/*.go` package names, `sdk/go/go.sum`  
**ADR required:** Yes  
**Semver:** Major version (v2)  
**Breaking for:** All Go applications that import `github.com/banzami/banzami-go`  
**Approach:** Publish v2 module at new path; maintain v1 read-only for 12 months  
**Estimated effort:** Medium

### MIGRATE-005 — PHP SDK: class renames `BanzamiClient` → `BanzaClient`, `BanzamiException` → `BanzaException`
**Scope:** `sdk/php/src/`, `sdk/php/laravel/`, all tests, all documentation  
**ADR required:** Yes  
**Semver:** Major version  
**Breaking for:** All PHP/Laravel applications using the SDK  
**Estimated effort:** Medium

### MIGRATE-006 — Integration plugins: package, class, and plugin renames
**Scope:** `integrations/plugins/generic-laravel/`, `integrations/plugins/woocommerce/banzami-payment/`, `integrations/plugins/generic-php/`  
**ADR required:** No — integrations are lower-stability artifacts  
**Breaking for:** Existing WordPress/WooCommerce installations  
**Estimated effort:** Medium — coordinate with plugin directory listings

### MIGRATE-007 — QR payload prefix: `BANZAMI:` → `BANZA:`, `BANZAMI-SBX:` → `BANZA-SBX:`
**Scope:** `contracts/qr/payload-format.json`, `contracts/qr/lifecycle.json`, `contracts/qr/README.md`, `conformance/`, `BANZA_CONFORMANCE.md`, `.github/workflows/conformance.yml`, `reference/sandbox-operator/src/state.rs`  
**ADR required:** Yes — QR payload format is a protocol-level spec  
**Breaking for:** All QR codes currently deployed with `BANZAMI:` prefix  
**Approach:** Accept both prefixes during 12-month transition; require new prefixes for new QR codes after transition  
**Estimated effort:** High — runtime changes, not just docs

---

## Priority sequence

```
Wave 1 — Immediate (next commit, no coordination needed)
  FIX-001 through FIX-012

Wave 2 — ADR proposals (open for review, no code changes yet)
  Open ADR for MIGRATE-001 (well-known URL)
  Open ADR for MIGRATE-002 (schema $id)
  Open ADR for MIGRATE-007 (QR prefix)

Wave 3 — Kernel (after Wave 2 ADRs accepted)
  MIGRATE-001 (implement dual-serve, schedule deprecation)
  MIGRATE-002 (publish at new URI)
  MIGRATE-003 (crate renames — coordinated with ~/banzami)

Wave 4 — SDK and integrations (after Wave 3 stabilized)
  MIGRATE-004 (Go SDK v2)
  MIGRATE-005 (PHP SDK major)
  MIGRATE-006 (integration plugins)
```

---

## Governance for each wave

| Wave | ADR required | Min review period | Coordination |
|---|---|---|---|
| Wave 1 | No | None | None |
| Wave 2 | Yes — one ADR per item | 7 days each | None |
| Wave 3 | After ADRs accepted | Per ADR | ~/banzami team |
| Wave 4 | Yes | 7 days each | SDK consumers |
