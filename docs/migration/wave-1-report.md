# Wave 1 Migration Report — Documentation Prose

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Executed by:** BANZA-NAMING-INVERSION-STEP-003  
**Status:** Complete

---

## Summary

Wave 1 migrated all in-scope markdown documentation across the three ecosystem repositories. The naming inversion is now reflected in all prose: Banza appears as the protocol/infrastructure, Banzami appears as the product, and BanzAI appears as the Protocol Operating System.

| Metric | Count |
|--------|-------|
| Total files processed | 269 |
| Files modified | 222 |
| Files unchanged (no occurrences) | 47 |
| Files skipped (excluded scope) | 41 |
| Manual fixes applied | 3 |

---

## Files Modified by Repository

| Repository | Files Modified | Insertions | Deletions |
|------------|---------------|------------|-----------|
| Banzami (kernel) | 104 | 735 | 733 |
| BanzamIA (AI OS) | 11 | 66 | 64 |
| Banza (operator) | 107 | 1,205 | 1,203 |
| **Total** | **222** | **2,006** | **2,000** |

---

## Rename Rules Applied

The following transformations were applied automatically using a Python transform that is code-block-aware (inline code and fenced blocks were left unchanged):

| Old (pre-inversion) | New (post-inversion) | Class |
|---------------------|---------------------|-------|
| Banzami (protocol context) | Banza | PROTOCOL |
| Banza (product context) | Banzami | PRODUCT |
| BanzamIA | BanzAI | AI_OS |
| Banzami Protocol | Banza Protocol | PROTOCOL |
| Banzami Kernel | Banza Kernel | PROTOCOL |
| Banzami Ecosystem | Banza Ecosystem | PROTOCOL |
| Banzami Infrastructure | Banza Infrastructure | PROTOCOL |
| Banzami Certification | Banza Certification | PROTOCOL |
| Banzami Federation | Banza Federation | PROTOCOL |
| Banza Wallet | Banzami Wallet | PRODUCT |
| Banza Business | Banzami Business | PRODUCT |
| Banza Checkout | Banzami Checkout | PRODUCT |
| Banza QR | Banzami QR | PRODUCT |
| Banza Pay Links | Banzami Pay Links | PRODUCT |
| Banza app | Banzami app | PRODUCT |
| BanzamIA Protocol Operating System | BanzAI Protocol Operating System | AI_OS |

---

## Protected Occurrences — Skipped

The following strings were explicitly protected by the transform and remain unchanged:

| String | Class | Reason |
|--------|-------|--------|
| `banzami.org` | DOMAIN | Registered domain — protected |
| `Banzami Lda` | ORG | Legal entity name — protected |
| `Organização Banzami` | ORG | Org name — ORG class, deferred |
| `Banzami Organisation` | ORG | Org name — ORG class, deferred |
| `Banza-Signature` | API_ROUTE | Webhook header — already correct after inversion |
| All inline code `` `...` `` | PACKAGE/CODE_SYMBOL | Code symbol renames deferred to Wave 4/7 |
| All fenced code blocks ` ``` ``` ` | PACKAGE/CODE_SYMBOL | Preserved intact |
| `Banzami::method()` (PHP) | CODE_SYMBOL | In code blocks — Wave 7 |

**Total protected occurrences preserved: ~195** (domains, emails, code blocks, ORG references)

---

## Manual Fixes Applied

Three corrections applied after the automated transform:

1. **`GOVERNANCE.md` (Banzami kernel):** Two instances of `Banza (the organization)` corrected to `Banzami (the organization)`. The phrase `Banzami (the organization)` did not match the ORG protection list (which required exact phrases). The ORG name "Banzami (the organization)" refers to the company stewarding the Banza protocol and must remain "Banzami".

2. **`README.md` (Banza operator):** `the payment product built by Banza` corrected to `the payment product built by Banzami`. Same ORG class issue — the company that built the product is named "Banzami".

3. **Transitional wording added** to three major README files:
   - `Banzami/README.md`: note that Banza was formerly called Banzami (protocol)
   - `Banza/README.md`: note that Banzami was formerly called Banza (product)
   - `BanzamIA/README.md`: note that BanzAI was formerly called BanzamIA

---

## Key Files Updated

### Banzami (kernel) repository

| File | Changes |
|------|---------|
| `README.md` | "Banzami" → "Banza" (protocol), "Banza" → "Banzami" (product), transitional note added |
| `GOVERNANCE.md` | Full protocol rename; org reference fixed manually |
| `CONTRIBUTING.md` | Protocol rename |
| `CODE_OF_CONDUCT.md` | Community name updated |
| `docs/adr/ADR-001` through `ADR-024` | All ADR prose updated (22 files) |
| `docs/rfc/RFC-0001` through `RFC-0006` | All RFC prose updated (6 files) |
| `docs/BANZAMI_REFERENCE.md` | Major reference document updated (filename deferred to Wave 9) |
| `docs/architecture/*.md` | All 7 architecture documents |
| `docs/core/*.md` | Financial domain docs |
| `docs/domains/**/*.md` | 16 domain README files |
| `sdk/**/*.md` | SDK README files and changelogs |
| `integrations/**/*.md` | Plugin README files and changelogs |
| `conformance/**/*.md` | Conformance documentation |

### BanzamIA repository

| File | Changes |
|------|---------|
| `README.md` | BanzamIA → BanzAI, Banzami Protocol → Banza Protocol, transitional note added |
| `CONTRIBUTING.md` | BanzamIA → BanzAI |
| `SECURITY.md` | BanzamIA → BanzAI |
| `contexts/banzami-protocol.md` | Title and all protocol references updated |
| `contexts/financial-invariants.md` | Protocol references updated |
| `prompts/*.md` | All 5 prompt files updated |
| `infra/runpod/models.md` | Infrastructure doc updated |

### Banza (operator) repository

| File | Changes |
|------|---------|
| `README.md` | Full product rename; "Banza" → "Banzami" product, transitional note added |
| `docs/BANZAMI_REFERENCE.md` | Major reference document updated (filename deferred to Wave 9) |
| `docs/adr/ADR-001` through `ADR-017` | 17 operator ADRs updated |
| `docs/banzamia/*.md` | 8 BanzamIA module documentation files |
| `docs/architecture/*.md` | Architecture documents |
| `docs/audit/*.md` | All audit reports updated |
| `docs/domains/**/*.md` | All domain README files |
| `docs/integrations/doa/*.md` | All DOA integration docs (12 files) |
| `docs/brand/*.md` | Brand guidelines updated |
| `sdk/**/*.md` | SDK README files |
| `plugins/**/*.md` | Plugin READMEs and changelogs |
| `apps/**/*.md` | App README files |

---

## Occurrences Skipped (Intentional)

The following categories of occurrences were intentionally NOT renamed in Wave 1:

| Category | Reason | Wave |
|----------|--------|------|
| All code blocks (``` ``` ```) | Code symbol renames deferred | 4/7 |
| All inline code (`` ` ` ``) | Code symbol renames deferred | 4/7 |
| Component names: `BanzamIAApp`, `BanzamIAChat`, etc. | In inline code, Wave 4 | 4 |
| Package names: `banza-sdk`, `@banza/sdk` etc. | Lowercase, not prose, Wave 6 | 6 |
| Rust crate names: `banzami-ledger` etc. | Code blocks, Wave 7 | 7 |
| PHP class calls: `Banzami::method()` | Code blocks, Wave 7 | 7 |
| Wire format strings: `BANZAMI:`, `BANZAMI-SBX:`, `/.well-known/banzami/` | In code blocks, Wave 5c | 5c |
| SVG text labels | SVG files only, Wave 2 | 2 |
| Website copy (banzami.org pages) | Wave 3 | 3 |
| Environment variable names: `BANZAMIA_*` | Wave 5a | 5a |
| API routes: `/banzamia/*` | Wave 5b | 5b |
| GitHub org: `github.com/banzami` | Separate ADR required, Wave 8 | 8 |
| Directory/filename renames | Wave 9 | 9 |

---

## Manual Review Items

The following items require human judgment before or during future waves:

| Item | File | Issue |
|------|------|-------|
| `Banzami (the organization)` pattern | Multiple ADRs | ORG class occurrences that did not match protection list — verify each instance |
| `built by Banzami` phrases | Various | Company attribution: verify "Banzami" vs "Banza" is correct in each context |
| Anchor links in TOCs | `docs/BANZAMI_REFERENCE.md` (Banza repo) | Internal anchors reference old heading names; update in Wave 9 |
| `docs/banzamia/` folder name | Banza repo | Directory name not renamed in Wave 1; deferred to Wave 9 (C-005) |
| `BANZAMI_REFERENCE.md` filename | Both repos | Filename not renamed; deferred to Wave 9 (C-006) |
| `BANZAMI_ECOSYSTEM_REFERENCE.md` | Banza repo | Filename not renamed; deferred to Wave 9 |
| `BANZA_BRAND_GUIDELINES.md` | Banza repo | Filename still uses old product name; deferred to Wave 9 |
| ORG class references | `GOVERNANCE.md`, `CONTRIBUTING.md` | "Banzami Organisation" / "Banzami Organization" phrases were protected — verify these are correct as-is |

---

## Validation

| Check | Result |
|-------|--------|
| `banzami.org` domain preserved | ✓ — 102 files still correctly reference the domain |
| `Banzami Lda` preserved | ✓ — 5 files retain legal entity name |
| `Banza-Signature` preserved | ✓ — webhook header unchanged |
| `Banza Lda` does not appear (wrong form) | ✓ — 0 occurrences |
| No code blocks modified | ✓ — PHP, Rust, shell code blocks intact |
| `BanzamIA` remaining = code blocks only | ✓ — all 61 residual are inside code/inline |
| `BANZAMI:` QR prefix preserved in code | ✓ — wire format not changed (Wave 5c) |

---

## Remaining Waves

| Wave | Scope | Status |
|------|-------|--------|
| 1 | Documentation prose (ADRs, READMEs, reference docs) | **✓ COMPLETE** |
| 2 | SVG diagram text labels | Pending |
| 3 | Website copy (banzami.org pages, metadata) | Pending |
| 4 | BanzAI UI components, routes, lib rename | Pending |
| 5a | Env vars (`BANZAMIA_*` → `BANZAI_*`), Docker | Pending |
| 5b | BanzAI API routes (`/banzamia` → `/banzai`) | Pending |
| 5c | Wire format (QR prefixes, operator manifest path) | Pending |
| 6 | SDK documentation, Python SDK rename | Pending |
| 7 | Rust crates (`banzami-*` → `banza-*`), code symbols | Pending |
| 8 | GitHub repository renames (separate ADR required) | Pending — ADR-026 needed |
| 9 | Final cleanup (directory/filename renames) | Pending |
