# VALIDATION_STUDIO_AUDIT.md

**Audit ID:** VALIDATION-STUDIO-COVERAGE-AUDIT-001  
**Date:** 2026-05-31  
**Working directory audited:** `~/banzami/apps/validation-studio/`  
**Data source audited:** `~/banzami/docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json`

---

## Critical finding before all else

**The Validation Studio does NOT live in `~/banza`.**

The prompt states "The BANZA repository already contains a Validation Studio." This is incorrect. The studio lives in:

```
~/banzami/apps/validation-studio/   ← BANZAMI repository (reference operator)
```

Not in:

```
~/banza/apps/validation-studio/     ← this directory does not exist
```

This is an institutional separation fact, not a bug. Everything below is an audit of `~/banzami/apps/validation-studio/` and its data source `~/banzami/docs/validation/`.

---

## Files inspected

### Studio application (`~/banzami/apps/validation-studio/`)

| File | Purpose |
|---|---|
| `package.json` | Next.js 15, React 19, Tailwind 4, Vitest |
| `app/studio/validation/page.tsx` | Route — loads matrix + git context, renders Studio |
| `app/page.tsx` | Root redirect to studio |
| `app/layout.tsx` | App shell |
| `components/Studio.tsx` | Main UI — filter bar, item list, item editor, diff + commit modals |
| `components/ItemList.tsx` | Sortable list with status badges, confidence score, governance issue count |
| `components/ItemEditor.tsx` | Full item editor — all fields editable, live governance enforcement |
| `components/DiffModal.tsx` | Pre-save diff review with governance check |
| `components/CommitModal.tsx` | Git commit interface with fingerprint display |
| `lib/types.ts` | Complete TypeScript type definitions |
| `lib/matrix.ts` | Read/write matrix file, compute change summary |
| `lib/governance.ts` | Governance rule enforcement (per-item + full matrix) |
| `lib/fingerprint.ts` | SHA-256 fingerprint computed from item state + git diff + proposed patch |
| `lib/git.ts` | Git branch, status, diff, commit integration |
| `actions/matrix.ts` | Server actions: loadMatrix, saveMatrix, previewSave |
| `actions/git.ts` | Server actions: getGitContext, getMatrixDiff |
| `lib/__tests__/fingerprint.test.ts` | Fingerprint unit tests |
| `lib/__tests__/governance.test.ts` | Governance rule unit tests |

### Validation data (`~/banzami/docs/validation/`)

| File | Content |
|---|---|
| `BANZAMI_IMPLEMENTATION_MATRIX.json` | 5,553 lines — 79 items, 24 categories |
| `VALIDATION_DOMAINS.md` | 11 domain definitions with standards and category mappings |
| `INVARIANT_TAXONOMY.md` | Financial invariant definitions |
| `README.md` | Governance protocol documentation |

### Makefile target

```makefile
studio: studio-install
    cd apps/validation-studio && npm run dev
```

Port: 3099. URL: `http://localhost:3099/studio/validation`.

---

## Current data model — complete schema

```typescript
interface ValidationMatrix {
  meta: {
    version: string           // "1.0"
    lastUpdated: string       // "2026-05-22"
    referenceVersion: string  // "1.0"
    referenceFile: string     // "docs/BANZA_REFERENCE.md"
    description: string
  }
  categories: ValidationCategory[]  // 24 categories
  items: ValidationItem[]            // 79 items
}

interface ValidationItem {
  id: string                          // "LED-001", "WAL-003", "SDK-001"
  title: string
  categoryId: string                  // "cat-ledger", "cat-sdk", etc.
  validationDomain: ValidationDomain  // "DOM-FIN", "DOM-DEV", etc.
  referenceSection: string            // "§6.2" or "§13.7 (ADR-025)"
  description: string
  requirement: string
  status: ValidationStatus            // VALIDATED | IMPLEMENTED | IN_PROGRESS | PLANNED | FUTURE | BLOCKED | NEEDS_REVIEW | REVALIDATION_REQUIRED
  priority: ValidationPriority        // CRITICAL | HIGH | MEDIUM | LOW
  ownerArea: string
  technicalArea: string
  validationMethods: ValidationMethod[] // unit_tests | integration_tests | e2e_tests | manual_ux | financial_invariant | reconciliation | security_audit | sandbox | production_review
  acceptanceCriteria: string[]
  testCoverage: boolean
  evidence: ValidationEvidence[]      // { type: 'route'|'component'|'config'|'adr'|'test'|'pr', label: string, ref: string }
  notes?: string
  dependencies: string[]              // informational — all known dependencies
  requires: string[]                  // enforcement — must be VALIDATED before this can be VALIDATED
  affects: string[]                   // items that should be revalidated if this item changes
  revalidateWhenChanged: string[]     // file glob patterns — trigger revalidation on match
  blockingIssues: string[]
  invariants: ValidationInvariant[]   // { id, name, rule, status: PASS|FAIL|UNKNOWN|NOT_RUN, lastChecked? }
  confidence: ConfidenceScore         // { score: 0-100, level: LOW|MEDIUM|HIGH|VERY_HIGH, basis: string[] }
  freezeReason?: string
  lastValidatedAt?: string
  validatedAgainstCommit?: string     // git commit hash at time of last VALIDATED transition
  history: ValidationHistory[]        // append-only audit trail with fingerprint per entry
  lastUpdated: string
}
```

### Fingerprint algorithm

The studio computes fingerprints by hashing:
```
SHA-256({
  itemId, itemStatus, itemEvidence, itemAcceptanceCriteria,
  itemInvariants, itemRequires,
  gitDiff,                    ← incorporates actual code state
  proposedStatus, proposedEvidence, proposedInvariants
})[:16]
```

This is significantly more robust than a static hash — it ties the fingerprint to actual code changes visible in the git diff.

---

## Current matrix state (79 items)

### By status
| Status | Count |
|---|---|
| VALIDATED | 16 |
| IMPLEMENTED | 5 |
| IN_PROGRESS | 2 |
| BLOCKED | 4 |
| PLANNED | 48 |
| FUTURE | 4 |

### By domain
| Domain | Count | Description |
|---|---|---|
| DOM-FIN | 15 | Financial integrity (ledger, wallets, settlement, P2P) |
| DOM-DEV | 12 | Developer platform (SDKs, API, webhooks, sandbox) |
| DOM-CONSUMER | 11 | Consumer experience (QR, payment links, pay requests) |
| DOM-DOCS | 9 | Documentation & governance |
| DOM-INFRA | 8 | Infrastructure |
| DOM-MERCHANT | 7 | Merchant experience |
| DOM-SEC | 6 | Security |
| DOM-IDENTITY | 6 | Wallet & identity |
| DOM-OBS | 3 | Observability |
| DOM-COMPLIANCE | 2 | Compliance |

### By priority
| Priority | Count |
|---|---|
| CRITICAL | 47 |
| HIGH | 22 |
| MEDIUM | 8 |
| LOW | 2 |

---

## Governance machinery — what exists

The studio has mature governance enforcement:

1. **Governance rules** (`lib/governance.ts`): checks for empty title/requirement/referenceSection, VALIDATED-without-evidence, VALIDATED-with-low-confidence, BLOCKED-without-reason, financial items without invariants, items with unresolved dependency locks (`requires` not VALIDATED).

2. **Confidence scoring** (`lib/types.ts: computeConfidence`): automatic 0-100 score from evidence (20pts), unit_tests (15pts), integration_tests (20pts), E2E/manual_ux (15pts), production/sandbox (10pts), invariants PASS (20pts). Threshold 80 required for VALIDATED.

3. **Fingerprint** (`lib/fingerprint.ts`): SHA-256 of item state + git diff + proposed patch. Detects code drift between proposal and application.

4. **Audit history** (`lib/matrix.ts: appendHistory`): every status transition appended immutably with timestamp, from/to status, approvedBy, fingerprint, commit hash, and reason.

5. **Diff preview** (`components/DiffModal.tsx`): shows field-level changes before any write.

6. **Git integration** (`lib/git.ts`): reads branch, status, diff; commits from inside the studio.

---

## Phase A contract integration status

Phase A produced:
- `~/banza/contracts/events/` (envelope.schema.json, types.json, webhook-types.json)
- `~/banza/contracts/webhooks/` (signature.json, envelope.schema.json)
- `~/banza/contracts/qr/` (payload-format.json, lifecycle.json)

**Zero of these files are referenced in the existing matrix.**

Current contract references in evidence (4 items, all old contracts):
| Item | Contract reference |
|---|---|
| WAL-001 | `contracts/openapi/wallet-onboarding.yaml` |
| WAL-003 | `contracts/openapi/activity.yaml` |
| P2P-003 | `contracts/openapi/transfers.yaml` |
| ARCH-REPO-001 | `contracts/README.md` |

**Items where Phase A contracts should be added as evidence:**
- `WH-001`, `WH-002`, `WH-003` → `contracts/webhooks/signature.json`, `contracts/events/webhook-types.json`
- `QR-001`, `QR-002`, `QR-003`, `QR-004`, `QR-005` → `contracts/qr/payload-format.json`, `contracts/qr/lifecycle.json`
- `SDK-001`–`SDK-004` → `contracts/events/types.json`, `contracts/webhooks/envelope.schema.json`
- `LED-001`–`LED-004` → `contracts/events/envelope.schema.json`

---

## ADR-025 compliance

**Studio source code:** Compliant. No violations found.

**Matrix data:**
- `meta.description` uses "Banza ecosystem" — ✅ compliant (refers to the ecosystem, not protocol-as-product)
- `meta.referenceFile: "docs/BANZA_REFERENCE.md"` — ✅ correct (BANZA, not Banzami)
- No uses of "Banzami ecosystem", "Banzami protocol", "BanzamIA", "banzami.org"

**One borderline case:** the matrix is named `BANZAMI_IMPLEMENTATION_MATRIX.json` — the `BANZAMI_` prefix refers to Banzami as the reference operator implementing BANZA. This is appropriate for the Banzami repo. It would not be appropriate if the same filename were used for a BANZA protocol-level matrix.

---

## Summary

The Validation Studio is a mature, production-quality governance tool. It is not a prototype. It has real governance enforcement, fingerprint-based approval, full audit trails, and git integration. It is significantly more capable than the Phase B matrix I created in `~/banza/docs/validation/`.

Its scope, however, is Banzami product features — not BANZA protocol conformance certification.
