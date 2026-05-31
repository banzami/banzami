# BANZA/BANZAMI CONTAMINATION AUDIT

**Audit ID:** BANZA-BANZAMI-CONTAMINATION-AUDIT-001  
**Date:** 2026-05-31  
**Scope:** All files in `~/banza` except `.git/`, `node_modules/`, `target/`, `dist/`, `build/`, `.next/`, `docs/migration/`, `docs/audit/github/`  
**Method:** `rg -n` exhaustive search + manual classification per file  

---

## Classification legend

| Code | Meaning |
|---|---|
| **A** | CRITICAL_CONTAMINATION — Banzami treated as protocol owner, governance authority, or namespace owner |
| **B** | STRUCTURAL_DEBT — `banzami-*` naming in code that belongs to BANZA; requires migration plan |
| **C** | VALID_OPERATOR_REFERENCE — Banzami correctly cited as reference operator or commercial implementation |
| **D** | HISTORICAL_PROTECTED — Pre-ADR-025 naming in ADR records or audit archives; immutable |
| **E** | BUG — Active wrong string in a running artifact (header name, URL, constant) |

---

## SECTION 1 — CRITICAL CONTAMINATION (A)

### A-001 — Kernel Cargo.toml: repository points to Banzami org
**File:** `core/Cargo.toml:29`  
**Line:** `repository = "https://github.com/banzami/banzami"`  
**Impact:** The BANZA protocol kernel declares Banzami's GitHub repository as its canonical home. Every crate published from `core/` carries Banzami's URL in its metadata. Any external operator who reads the kernel metadata sees BANZA as Banzami's property.  
**Classification:** A — CRITICAL_CONTAMINATION  
**Fix:** Change to `https://github.com/banza-protocols/banza`  
**Requires migration plan:** No — metadata-only change, no API impact.

---

### A-002 — Kernel Cargo.toml: authors attributed to Banzami Engineering
**File:** `core/Cargo.toml:30`  
**Line:** `authors = ["Banzami Engineering <engineering@banzami.com>"]`  
**Impact:** The BANZA open protocol kernel attributes authorship to Banzami's engineering team. This directly contradicts ADR-025 and BANZA_GOVERNANCE.md ("BANZA is not owned by Banzami").  
**Classification:** A — CRITICAL_CONTAMINATION  
**Fix:** Change to `authors = ["BANZA Protocol <protocol@banza.network>"]` or remove the field (Cargo recommends omitting authors for workspace crates)  
**Requires migration plan:** No — metadata-only.

---

### A-003 — Conformance schema `$id` URIs under banzami.com domain
**Files:**  
- `conformance/manifests/schema.json:3` — `"$id": "https://banzami.com/conformance/manifests/schema.json"`  
- `conformance/capabilities/schema.json:3` — `"$id": "https://banzami.com/conformance/capabilities/schema.json"`  
- `conformance/report-schema.json:3` — `"$id": "https://banzami.com/conformance/report-schema.json"`  

**Impact:** The canonical JSON Schema identifiers for BANZA protocol conformance artifacts are hosted under Banzami's domain. Any operator implementing BANZA protocol conformance will resolve these URIs to Banzami's servers. The conformance system appears to be Banzami's property, not BANZA's. This is the most structurally serious contamination in the repo after the crate naming.  
**Classification:** A — CRITICAL_CONTAMINATION  
**Fix:** Change `$id` to `https://banza.network/conformance/...` (or a canonical BANZA domain) or to a relative path  
**Requires migration plan:** Yes — if any external tool has hardcoded these URIs, changing them is a breaking change. Needs a deprecation notice.

---

### A-004 — Well-known operator URL uses `banzami` namespace in active conformance tests
**Files:**  
- `conformance/operators/suite.json:147,155` — `"path": "/.well-known/banzami/operator.json"`  
- `conformance/vectors/operator-manifests.json:13,33,52` — same path  
- `BANZA_CONFORMANCE.md:119` — instructs all Federation Operators to serve `/.well-known/banzami/operator.json`  
- `docs/rfc/RFC-0005-operator-discovery.md:71,80` — RFC defines the path as `/.well-known/banzami-operator.json`  

**Impact:** Every certified BANZA operator must serve a URL path containing `banzami`. This permanently embeds Banzami's brand into the BANZA protocol's operator discovery API surface. Any future operator implementing the protocol — a bank, a telecom, a fintech with no relation to Banzami — must serve `/.well-known/banzami/operator.json`. This is structural contamination of the public protocol API.  
**Classification:** A — CRITICAL_CONTAMINATION  
**Fix:** The canonical URL should be `/.well-known/banza/operator.json`. RFC-0005 must be updated. Conformance suite test cases must be updated. The sandbox operator's route must be updated.  
**Requires migration plan:** Yes — this is a breaking change to an active API path. Requires deprecation period, RFC update, and coordination with any operator already implementing the path.

---

### A-005 — `docs/BANZAMI_REFERENCE.md` — a full Banzami product reference document inside BANZA
**File:** `docs/BANZAMI_REFERENCE.md` (191 occurrences of Banzami)  
**Impact:** This is a comprehensive Banzami product reference document (consumer app, merchant dashboard, pay.banzami.com URLs, staging infrastructure, Flutter build instructions) inside the BANZA protocol kernel repository. It describes Banzami's commercial product in detail — consumer UX flows, staging.banzami.com environments, TestFlight distribution, and commercial payment URLs. This document has no place in the BANZA protocol repo.  
**Classification:** A — CRITICAL_CONTAMINATION  
**Fix:** Move to `~/banzami/docs/`. Remove from BANZA entirely. Replace with a short pointer: "See [BANZAMI_REFERENCE.md](https://github.com/banzami/banzami/blob/main/docs/BANZAMI_REFERENCE.md)".  
**Requires migration plan:** No — file move with pointer note.

---

### A-006 — `core/README.md` dependency instructions point to `github.com/banzami/banzami`
**File:** `core/README.md:72-73`  
```toml
banzami-types  = { git = "https://github.com/banzami/banzami" }
banzami-ledger = { git = "https://github.com/banzami/banzami" }
```
**Impact:** The BANZA protocol kernel's getting-started instructions direct external operators to clone from Banzami's repo. This makes the kernel appear to be distributed as part of Banzami's codebase.  
**Classification:** A — CRITICAL_CONTAMINATION  
**Fix:** Change to `git = "https://github.com/banza-protocols/banza"`  
**Requires migration plan:** No.

---

### A-007 — `README.md` dependency examples point to `github.com/banzami/banzami`
**File:** `README.md:275-276`  
Same as A-006. The public-facing README directs all operators to Banzami's repository.  
**Classification:** A — CRITICAL_CONTAMINATION  
**Fix:** Change to `git = "https://github.com/banza-protocols/banza"`  
**Requires migration plan:** No.

---

## SECTION 2 — STRUCTURAL DEBT (B)

These are confirmed structural issues explicitly recognized in `docs/governance/CLAUDE_BASE.md` as "protected" or "out of scope for now." Classified here for completeness and remediation planning.

### B-001 — All Rust kernel crates use `banzami-*` prefix (19 crates)
**Location:** `core/crates/banzami-*/`  
**Crates:** `banzami-types`, `banzami-ledger`, `banzami-wallets`, `banzami-consumer-wallets`, `banzami-transactions`, `banzami-transfers`, `banzami-qr`, `banzami-settlement`, `banzami-reconciliation`, `banzami-acquiring`, `banzami-routing`, `banzami-identity`, `banzami-merchants`, `banzami-payment-links`, `banzami-payouts`, `banzami-risk`, `banzami-compliance`, `banzami-notifications`, `banzami-capabilities`  
**Impact:** The BANZA protocol kernel is entirely named after Banzami. Every import, every crate dependency, every reference in documentation says `banzami-*`. Protocol contributors see the kernel as Banzami's. External operators building on the kernel depend on packages named after one operator.  
**Proposed canonical names:** `banza-types`, `banza-ledger`, `banza-wallets`, etc.  
**Status per CLAUDE_BASE.md:** "Rust crate names `banzami-types`, `banzami-ledger`, etc. — explicitly out of scope"  
**Requires migration plan:** Yes — major. Affects Cargo.lock, all import paths, documentation, downstream usage by Banzami repo.

### B-002 — `tools/banzami-conformance/` — conformance runner tool
**Location:** `tools/banzami-conformance/run.py`, `run.sh`, `README.md`  
**Impact:** The BANZA protocol conformance runner is named after Banzami. Any operator running conformance tests invokes `banzami-conformance` not `banza-conformance`. The tool appears operator-specific.  
**Proposed name:** `tools/banza-conformance/`  
**Requires migration plan:** Yes — tool rename + update all invocations in CI workflows, docs, README.

### B-003 — Go SDK package path: `github.com/banzami/banzami-go`
**File:** `sdk/go/go.mod:1`, `sdk/go/banzami/`  
**Impact:** The official BANZA Go SDK imports as `github.com/banzami/banzami-go/banzami`. Every Go application using the BANZA SDK will have `banzami` in their import paths.  
**Proposed:** `github.com/banza-protocols/banza-go/banza`  
**Requires migration plan:** Yes — published module path change is breaking.

### B-004 — PHP SDK class names: `BanzamiClient`, `BanzamiException`
**Files:** `sdk/php/src/BanzamiClient.php`, `sdk/php/src/Exceptions/BanzamiException.php`, `sdk/php/laravel/Facades/Banzami.php`  
**Impact:** PHP operators instantiate `new BanzamiClient(...)` and catch `BanzamiException`. These class names embed Banzami in the operator's application code.  
**Proposed:** `BanzaClient`, `BanzaException`  
**Requires migration plan:** Yes — public class name change is breaking.

### B-005 — Laravel plugin and integration plugins use banzami naming
**Files:** `integrations/plugins/generic-laravel/src/BanzamiServiceProvider.php`, `integrations/plugins/generic-laravel/composer.json` (`"name": "banzami/banzami-laravel"`), `integrations/plugins/woocommerce/banzami-payment/`, `integrations/plugins/generic-php/src/BanzamiClient.php`  
**Impact:** Integrations are namespaced under Banzami. A WooCommerce merchant installing `banzami-payment` is installing what appears to be a Banzami product, not a BANZA protocol integration.  
**Proposed:** `banza-laravel`, `banza-payment`, `BanzaClient`  
**Requires migration plan:** Yes — published package names.

### B-006 — `assets/banzami_logo.svg` — Banzami product logo in BANZA protocol repo
**File:** `assets/banzami_logo.svg`  
**Impact:** The Banzami commercial product logo lives in the open protocol repo. The protocol should have its own visual identity (`banza_logo.svg`), not Banzami's.  
**Requires migration plan:** No — file rename/replace. Low urgency, no API impact.

### B-007 — `sdk/go/go.mod`, `sdk/php/composer.json` — module declarations in BANZA codebase reference banzami GitHub org
**Noted:** Tracked as part of B-003, B-004.

---

## SECTION 3 — VALID OPERATOR REFERENCES (C)

The following occurrences are correct, precise, and comply with ADR-025. No action required.

| File | Context | Verdict |
|---|---|---|
| `BANZA_GOVERNANCE.md:9-17` | "Banzami is an independent commercial company…" — correctly explains independence | C |
| `BANZA_GOVERNANCE.md:156-166` | "Banzami — one operator among many" — correct framing | C |
| `BANZA_REFERENCE.md:15,114-124,148-152,174,178,197,209,255,421,502,569` | Banzami cited as reference operator or example | C |
| `BANZA_ARCHITECTURE.md:103,115,232,234` | "O Banzami implementa estes providers — como qualquer outro operador certificado" | C |
| `BANZA_MANIFESTO.md:75,83,110,139,156` | Manifesto uses Banzami as reference operator example correctly | C |
| `BANZA_CERTIFICATION.md:163` | "Use the Banzami reference operator as your reference" — correct | C |
| `CLAUDE.md:13,22,25,51,55,127,135` | All correct: Banzami as operator, protocol independence | C |
| `docs/governance/CLAUDE_BASE.md:24-90` | Defines naming rules correctly, explains prohibited patterns | C |
| `BANZA_GOVERNANCE.md:15` | "Banzami operates at github.com/banzami and banzami.com" — factual, correct | C |
| `README.md:5,471` | "Banzami = reference operator" — correct | C |
| `README.md:126,134,198,199` | BanzAI access at banzami.com/banzai — correct (BanzAI is deployed by Banzami) | C |
| `README.md:456,472` | security@banzami.com, banzami.com — operator contact details, deferred per ADR-025 | C |
| `BANZA_SECURITY.md:79-82` | Crate paths in security context — structural debt (B), factual in context | C |
| `conformance/README.md:34` | "The reference sandbox operator (Banzami) is certified at Level 2" — accurate | C |

---

## SECTION 4 — HISTORICAL PROTECTED (D)

These appear only inside explicitly historical documents. Immutable; no action.

| File | Context |
|---|---|
| `docs/adr/ADR-016-banzami-banza-brand-architecture.md` | Superseded ADR — naming architecture before ADR-025. Immutable historical record. |
| `docs/adr/ADR-025-ecosystem-naming-inversion.md:89,163` | Explains the migration from old naming. References old names to document what changed. |
| `docs/audit/naming-inversion-plan.md` | Historical audit from naming migration phase |
| `docs/brand/audit-2026-05-15.md` | Pre-ADR-025 brand audit — historical |
| `docs/BANZA_OPERATOR_BOUNDARY_UPDATE_REPORT.md` | Historical boundary update report |

---

## SECTION 5 — BUGS (E)

Active wrong strings in running artifacts that must be fixed.

### E-001 — `sdk/python/banza/signature.py` — error messages still reference "Banzami-Signature" (PARTIAL — constant was fixed, error strings were not)
**Lines:**  
- Line 37: `"""Parse the Banzami-Signature header into (timestamp, v1)."""`  
- Line 56: `f"Banzami-Signature: invalid timestamp value {val!r}"`  
- Line 63: `"Banzami-Signature header is malformed: expected 't=<unix>,v1=<hex>'"`  
- Line 76: `"""Return True when the Banzami-Signature is valid."""`  
- Line 83: `Full value of the ``Banzami-Signature`` header.` (in `verify_signature` docstring)  
- Line 129: `"""Generate a valid ``Banzami-Signature`` header value for local testing."""`  
- Line 146: `A ``Banzami-Signature`` header value, e.g.`  

**Impact:** Error messages shown to developers reading tracebacks or documentation say the wrong header name. Any Python developer debugging a webhook will see "Banzami-Signature is malformed" not "Banza-Signature is malformed".  
**Classification:** E — BUG  
**Fix:** Replace all internal references to `Banzami-Signature` with `Banza-Signature`  
**Immediately fixable:** Yes.

### E-002 — `sdk-certification/vectors/webhook_signatures.json:5` — wrong header name in certification vectors
**Line:** `"_header_format": "Banzami-Signature: t=<unix_seconds>,v1=<hex_hmac_sha256>"`  
**Impact:** The SDK certification vectors document the wrong header name. Any SDK implementor reading the certification spec will implement the wrong header.  
**Classification:** E — BUG  
**Fix:** Change to `"Banza-Signature: t=<unix_seconds>,v1=<hex_hmac_sha256>"`  
**Immediately fixable:** Yes.

### E-003 — `contracts/webhooks/README.md:20` — stale bug notice (Python fix was already applied)
**Line:** "Known implementation discrepancy: `sdk/python/banza/signature.py` uses `Banzami-Signature`."  
**Impact:** The notice is now inaccurate — the SIGNATURE_HEADER constant was fixed in the last commit. Stale bug notice creates confusion.  
**Classification:** E — BUG (stale doc)  
**Fix:** Update to note the fix was applied in commit 20c5dc6.  
**Immediately fixable:** Yes.

### E-004 — `contracts/webhooks/signature.json:174-177` — stale known_implementation_discrepancies entry
**Impact:** Same as E-003 — the Python fix was applied but the contracts record still says it's unresolved.  
**Classification:** E — BUG (stale doc)  
**Fix:** Update or remove the discrepancy entry.  
**Immediately fixable:** Yes.

### E-005 — `integrations/plugins/generic-node/src/webhook.ts:17`, `examples/webhook-express.ts:12`, `README.md:247,280,302` — `x-banzami-signature` header
**Lines:**  
- `src/webhook.ts:17` — `req.headers['x-banzami-signature']`  
- `examples/webhook-express.ts:12` — `req.headers['x-banzami-signature']`  
- `README.md:247,280,302` — all three code examples read the wrong header  

**Impact:** Any Node.js developer using the integration plugin (not the SDK) will read the wrong header from incoming webhooks, causing silent signature verification failures.  
**Classification:** E — BUG  
**Fix:** Replace `x-banzami-signature` with `banza-signature` (lowercase; HTTP headers are case-insensitive but canonical form per contract is `Banza-Signature`)  
**Immediately fixable:** Yes.

### E-006 — `docs/stability.md:57` — `X-Banzami-Signature` listed as stable API contract
**Line:** `- \`X-Banzami-Signature\` header format`  
**Impact:** The stability document lists a wrong header name as a stable API surface. This tells external developers they can depend on `X-Banzami-Signature` forever.  
**Classification:** E — BUG  
**Fix:** Change to `Banza-Signature`  
**Immediately fixable:** Yes.

### E-007 — `integrations/plugins/generic-laravel/README.md:35,44` — `BANZAMI_GATEWAY_URL` env var
**Lines:**  
- `BANZAMI_GATEWAY_URL=https://api.banzami.com`  
- `| BANZAMI_GATEWAY_URL | Banza API base URL`  

**Impact:** The canonical env var prefix per `docs/governance/CLAUDE_BASE.md` is `BANZA_*`. `BANZAMI_GATEWAY_URL` and `BANZAMI_WEBHOOK_SECRET` (appearing throughout integration plugins) conflict with the protocol standard.  
**Classification:** E — BUG  
**Fix:** Rename env vars to `BANZA_GATEWAY_URL`, `BANZA_WEBHOOK_SECRET`, etc.  
**Immediately fixable:** Yes for docs; breaking for existing installations.

### E-008 — `CLAUDE.md:114` — references `docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` which no longer exists in BANZA
**Impact:** CLAUDE.md's governance section instructs that status changes to this file require approval — but the file was removed from BANZA in commit 20c5dc6. The reference is stale.  
**Classification:** E — BUG (stale)  
**Fix:** Update CLAUDE.md to remove the stale validation matrix governance section, or point to the correct location (`~/banzami/docs/validation/`).  
**Immediately fixable:** Yes.

---

## SECTION 6 — SUMMARY TABLE

| ID | Classification | File | Severity | Immediately Fixable | Migration Required |
|---|---|---|---|---|---|
| A-001 | CRITICAL | `core/Cargo.toml:29` | HIGH | Yes | No |
| A-002 | CRITICAL | `core/Cargo.toml:30` | HIGH | Yes | No |
| A-003 | CRITICAL | `conformance/{manifests,capabilities,report}-schema.json:3` | HIGH | Yes (with deprecation) | Yes |
| A-004 | CRITICAL | `conformance/operators/suite.json:147,155`, manifests vectors, RFC-0005 | HIGH | No — breaking API path | Yes |
| A-005 | CRITICAL | `docs/BANZAMI_REFERENCE.md` | MEDIUM | Yes — move file | No |
| A-006 | CRITICAL | `core/README.md:72-73` | HIGH | Yes | No |
| A-007 | CRITICAL | `README.md:275-276` | HIGH | Yes | No |
| B-001 | STRUCTURAL DEBT | `core/crates/banzami-*/` (19 crates) | HIGH | No | Yes — major |
| B-002 | STRUCTURAL DEBT | `tools/banzami-conformance/` | MEDIUM | No | Yes |
| B-003 | STRUCTURAL DEBT | `sdk/go/go.mod`, `sdk/go/banzami/` | MEDIUM | No | Yes — breaking |
| B-004 | STRUCTURAL DEBT | `sdk/php/src/BanzamiClient.php` etc. | MEDIUM | No | Yes — breaking |
| B-005 | STRUCTURAL DEBT | `integrations/plugins/*/banzami-*` | LOW | No | Yes |
| B-006 | STRUCTURAL DEBT | `assets/banzami_logo.svg` | LOW | Yes | No |
| E-001 | BUG | `sdk/python/banza/signature.py` (error strings) | HIGH | Yes | No |
| E-002 | BUG | `sdk-certification/vectors/webhook_signatures.json:5` | HIGH | Yes | No |
| E-003 | BUG | `contracts/webhooks/README.md:20` (stale) | LOW | Yes | No |
| E-004 | BUG | `contracts/webhooks/signature.json:174-177` (stale) | LOW | Yes | No |
| E-005 | BUG | `integrations/plugins/generic-node/` (`x-banzami-signature`) | HIGH | Yes | No |
| E-006 | BUG | `docs/stability.md:57` | MEDIUM | Yes | No |
| E-007 | BUG | `integrations/plugins/generic-laravel/` (BANZAMI_* env vars) | MEDIUM | Yes (docs) | Yes (installations) |
| E-008 | BUG | `CLAUDE.md:114` (stale matrix reference) | LOW | Yes | No |
