---
name: final-remaining-risks
description: Remaining risks after ECOSYSTEM-CANONICAL-DOCUMENT-ARCHITECTURE-001 — classified, prioritised, and with proposed remediation — ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001
metadata:
  type: project
---

# Final Remaining Risks

**Mission:** ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001  
**Date:** 2026-05-30

---

## No P0 Issues

No active ADR-025 violations were found. The canonical reference layer — all `BANZA_*.md`, `BANZAI_*.md`, `BANZAMI_*.md` documents, all `CLAUDE.md` files — is fully compliant with ADR-025.

The remaining risks are concentrated in:
1. Legacy README files (written before or during ADR-025 migration, not fully updated)
2. Pre-ADR-025 docs subdirectories
3. Package metadata inherited from the old `banzami/banzamia` repository

---

## Risk Register

### RISK-001 — banzami/README.md Identity Confusion (P1)

**Severity:** High — README is the highest-traffic document  
**Risk:** A developer opening `~/banzami` reads "Banza is built with fintech-grade agility..." and concludes that "Banza" is the engineering entity that built the platform. This contradicts ADR-025 which reserves "BANZA" for the open protocol.  
**Root cause:** The README was written with "Banza" as the operator name before ADR-025 established that "Banza/BANZA" exclusively means the protocol.  
**Affected lines:** 41, 69, 97, 114, 583, 629, 699, 707, 715, 835, 1259 (and more)  
**Remediation:** Replace all `"Banza "` with `"Banzami "` where describing operator engineering philosophy, architecture, and product. Pattern: `s/^Banza /Banzami /g` — requires careful scoped replacement.  
**Effort:** Medium (requires scoped search-replace to avoid changing `Banzami`, `BanzAI`, `BANZA`)  
**Priority:** 1 — Fix before any public launch or external contributor onboarding

---

### RISK-002 — banzami/README.md Line 13 BANZA Identity Assigned to Banzami (P1)

**Severity:** High — directly misrepresents who owns the open-source ecosystem  
**Risk:** "The open-source ecosystem (SDKs, contracts, protocol specs, integrations) lives at [github.com/banzami/banzami]" — assigns BANZA's identity (open protocol, SDKs, contracts) to Banzami and points to a broken URL.  
**Root cause:** Pre-ADR-025 artifact from when the monorepo `banzami/banzami` held everything.  
**Remediation:** Replace line 13 with: `"The open protocol and SDK ecosystem is maintained at [github.com/banza-protocol/banza](https://github.com/banza-protocol/banza). The Banzami operator implementation is this repository."` (or remove the line entirely — the ecosystem table at the top covers this correctly.)  
**Effort:** Low (single line)  
**Priority:** 1 — Fix immediately

---

### RISK-003 — banzai/README.md Capability Count Contradiction (P1)

**Severity:** High — public claim contradicts canonical REFERENCE document  
**Risk:** README claims "8 Capabilities" with `Prever` and `Guiar` capabilities that do not appear in `BANZAI_REFERENCE.md §5`, which defines exactly 6 capabilities. Any contributor or operator will see this contradiction immediately.  
**Root cause:** The README was written at a different point in BanzAI's design than the REFERENCE document. The REFERENCE document is more authoritative.  
**Decision needed:** Is the canonical count 6 or 8? If `Prever` and `Guiar` are real capabilities that BanzAI has, `BANZAI_REFERENCE.md` must be updated first (per content flow rules). If they are experimental or deprecated, remove from README.  
**Remediation (if 6 is canonical):** Replace README section "8 Capabilities" with the 6 listed in BANZAI_REFERENCE.md  
**Remediation (if 8 is canonical):** Add `Prever` and `Guiar` to BANZAI_REFERENCE.md §5 first, then README reflects it  
**Effort:** Low (once decision is made)  
**Priority:** 1 — Contradiction must be resolved before it reaches external contributors

---

### RISK-004 — banza/README.md Naming Note Misleads (P1)

**Severity:** Medium — misleads about the protocol's history  
**Risk:** `"Banza was formerly called Banzami"` implies the BANZA protocol used to be named "Banzami". This is false. The protocol was always "Banza". What was renamed was:
- The combined GitHub monorepo (`banzami/banzami` → split into `banza-protocol/{banza,banzai,banzami}`)
- The Protocol OS (BanzamIA → BanzAI)  

**Remediation:** Replace the naming note with accurate history:
```markdown
> **Naming note:** The ecosystem was formerly housed in a monorepo called `banzami/banzami`.
> ADR-025 (2026-05-29) separated it into three repositories:
> `banza-protocol/banza` (protocol), `banza-protocol/banzai` (Protocol OS),
> `banza-protocol/banzami` (reference operator). See `docs/migration/` for the full record.
```
**Effort:** Low  
**Priority:** 2

---

### RISK-005 — banzai/CONTRIBUTING.md Fork URL Wrong (P2)

**Severity:** Medium — breaks the contribution flow for external contributors  
**Risk:** A contributor following `CONTRIBUTING.md` step 1 is directed to fork `github.com/banzami/banzamia` — a repository that does not exist under that org/name.  
**Remediation:** Replace with `https://github.com/banza-protocol/banzai`  
**Effort:** Low  
**Priority:** 2

---

### RISK-006 — banzai/package.json Name Pre-ADR-025 (P2)

**Severity:** Low-Medium — affects npm workspace identity if package is published  
**Risk:** `"name": "@banzami/banzamia"` — pre-ADR-025 package name. If this package were ever published to npm, it would appear under the old org/name.  
**Remediation:** Update to `"name": "@banza-protocol/banzai"` or `"name": "@banzai/core"`  
**Caution:** Verify this name is not referenced in scripts or other package.json files before changing. Run `grep -r "@banzami/banzamia" . --include="*.json" --include="*.ts"` first.  
**Effort:** Low (with pre-change verification)  
**Priority:** 3

---

### RISK-007 — 17+ Stale `github.com/banzami/` URLs in SDK, ADR, and core files (P2)

**Severity:** Low — links go to a GitHub org that no longer holds the active repos  
**Risk:** Developers clicking these links land on stale or missing repositories. SDK dependency snippets show wrong git URLs.  
**Note:** The old `banzami` GitHub org may still exist; if repos were transferred (not deleted), some links may redirect. But this cannot be relied upon.  
**Remediation:** Batch replace across all affected files (see FINAL_BROKEN_REFERENCE_REPORT.md Section 2 for full list).  
**Effort:** Medium (17+ files across 3 repos, requires careful scoped search-replace)  
**Priority:** 3 — After P1 fixes are resolved

---

### RISK-008 — 8+ Stale `banzami.org/banzamia` Route References (P2)

**Severity:** Low — 301 redirects are live, so runtime behavior is correct  
**Risk:** Source documents are misleading; future developers maintaining these docs might remove the redirect without realizing the docs still reference old routes.  
**Remediation:** Batch replace `banzami.org/banzamia` → `banzami.org/banzai` and `banzami.org/sobre-banzamia` → `banzami.org/sobre-o-banzai` across all affected files.  
**Effort:** Medium (8+ files, primarily in banzami/docs/)  
**Priority:** 3

---

### RISK-009 — `docs/banzamia/` Directory Name in banzami Repo (P3)

**Severity:** Low — internal docs directory; not visible to external contributors  
**Risk:** The directory `banzami/docs/banzamia/` still uses the pre-rename name. Files inside reference internal paths with `banzamia` prefix.  
**Remediation options:**
- Option A: Rename `docs/banzamia/` → `docs/banzai/` and update all internal references
- Option B: Leave as historical archive; add a note that the directory content predates ADR-025  
**Recommendation:** Option B is safer — renaming a docs directory risks breaking any existing bookmarks or links from the deployed website.  
**Effort:** High (if renaming) / Low (if adding note)  
**Priority:** 4 — Cosmetic; not a correctness issue

---

### RISK-010 — banza/docs/BANZAMI_REFERENCE.md (Pre-ADR-025 Combined Reference in Protocol Repo) (P2)

**Severity:** Low-Medium — confusing to find a "BANZAMI_REFERENCE.md" inside the banza protocol repo  
**Risk:** This is the old pre-ADR-025 combined reference document. It contains stale URLs, ADR-016 framing, and claims that "this document is the canonical ecosystem reference" — which is now wrong (the canonical references are the three separate BANZA_/BANZAI_/BANZAMI_REFERENCE.md files).  
**Remediation:** Add a deprecation header to `banza/docs/BANZAMI_REFERENCE.md` noting it is a pre-ADR-025 historical document and pointing to the three canonical references.  
**Effort:** Low  
**Priority:** 3

---

## Risk Disposition Matrix

| Risk | Severity | Effort | Priority | Disposition |
|------|----------|--------|----------|-------------|
| RISK-001 banzami/README.md "Banza" → "Banzami" | HIGH | Medium | 1 | FIX NOW |
| RISK-002 banzami/README.md line 13 | HIGH | Low | 1 | FIX NOW |
| RISK-003 banzai/README.md capability count | HIGH | Low | 1 | DECIDE + FIX |
| RISK-004 banza/README.md naming note | MEDIUM | Low | 2 | FIX SOON |
| RISK-005 banzai/CONTRIBUTING.md fork URL | MEDIUM | Low | 2 | FIX SOON |
| RISK-006 banzai/package.json name | LOW | Low | 3 | BATCH |
| RISK-007 17+ stale github.com/banzami/ URLs | LOW | Medium | 3 | BATCH |
| RISK-008 8+ stale banzami.org/banzamia routes | LOW | Medium | 3 | BATCH |
| RISK-009 docs/banzamia/ directory name | LOW | High | 4 | DEFER |
| RISK-010 banza/docs/BANZAMI_REFERENCE.md | LOW | Low | 3 | ADD DEPRECATION HEADER |

---

## Proposed Batch Fix Waves

### Wave A — Critical P1 Fixes (do first, affects external perception)

1. `banzami/README.md` — scoped replace "Banza " → "Banzami " in engineering philosophy, architecture, product sections
2. `banzami/README.md:13` — replace line with accurate description
3. `banzai/README.md:27` — resolve capability count contradiction (requires human decision on 6 vs 8)
4. `banza/README.md:49` — replace misleading naming note

### Wave B — CONTRIBUTING + High-Visibility P2

5. `banzai/CONTRIBUTING.md` — fix fork URL and protocol kernel URL
6. `banza/README.md:124,132,196,197,469` — fix stale URLs in README body

### Wave C — Batch URL Replacement

7. All `github.com/banzami/` → `github.com/banza-protocol/` across all repos (17+ files)
8. All `banzami.org/banzamia` → `banzami.org/banzai` (8+ files)

### Wave D — Metadata and Historical Docs

9. `banzai/package.json` — update name field
10. `banza/docs/BANZAMI_REFERENCE.md` — add deprecation header
11. `banzami/docs/banzamia/` — add note or rename (decision needed)

---

*Produced by: ECOSYSTEM-FINAL-CROSS-REPO-CONSISTENCY-AUDIT-001 — 2026-05-30*
