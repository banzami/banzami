# VALIDATION_STUDIO_GAP_MAP.md

**Audit ID:** VALIDATION-STUDIO-COVERAGE-AUDIT-001  
**Date:** 2026-05-31

---

## Verdict

**B — Existing Validation Studio is useful but needs structural upgrade to become the canonical validation matrix.**

---

## The two-matrix problem

The audit discovered that two separate matrices now exist:

| Matrix | Location | Items | Schema | Status |
|---|---|---|---|---|
| Banzami product matrix | `~/banzami/docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` | 79 items | Sophisticated (history, confidence, invariants, fingerprints) | Active, Studio-connected, partially populated |
| BANZA protocol matrix | `~/banza/docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` | 56 items | Simpler (no history, no confidence, no invariants) | Created in Phase B, uncommitted, no UI |

These are not the same thing. They track different concerns. The duplicate filename (`BANZAMI_IMPLEMENTATION_MATRIX.json`) is misleading and will cause confusion. They must be reconciled before either is committed.

---

## Gap 1 — Location and institutional separation

**Current:** Validation Studio and its matrix live in `~/banzami` (the reference operator repo).  
**Issue:** If the studio is meant to be the canonical governance tool for the BANZA protocol, it should live in `~/banza`. If it governs Banzami product features, it correctly lives in `~/banzami`.  
**Fact:** The current matrix tracks Banzami product features (79 items: docs, wallet, QR, identity, merchant app). This correctly belongs in `~/banzami`.

**Proposed resolution:**
- `~/banzami/docs/validation/` → **Banzami Product Validation Matrix** (what exists today — 79 items, product features)
- `~/banza/docs/validation/` → **BANZA Protocol Conformance Matrix** (what needs to be built — protocol features, certification levels, conformance vectors)
- These are different matrices. Neither replaces the other.

---

## Gap 2 — Phase B matrix schema conflict

**Current:** `~/banza/docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` (Phase B, uncommitted) has a simpler schema than the Banzami studio model.

**Issue:** The Phase B schema lacks: `history[]`, `confidence`, `invariants[]`, `acceptanceCriteria[]`, `requires[]`, fingerprint linked to git diff. These are non-negotiable for governance integrity.

**Proposed resolution:** Discard the Phase B matrix file. If a BANZA protocol matrix is built, adopt the Banzami studio schema as the base and extend it with the protocol-specific fields.

**Phase B matrix file to be removed from `~/banza`:** `docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json`  
**Replace with:** A new protocol-scoped matrix using the proper schema from `~/banzami/lib/types.ts`.

---

## Gap 3 — Phase A contract integration (Banzami matrix)

**Current:** Zero Phase A contract files referenced in the Banzami product matrix.

**Items requiring evidence updates in `~/banzami/docs/validation/`:**

| Item ID | Title | Missing evidence |
|---|---|---|
| WH-001 | Sistema de webhooks — entrega de eventos | `contracts/webhooks/envelope.schema.json`, `contracts/events/webhook-types.json` |
| WH-002 | Verificação de assinatura HMAC-SHA256 | `contracts/webhooks/signature.json` |
| WH-003 | Retry automático com backoff exponencial | `contracts/webhooks/signature.json` |
| QR-001 | QR Estático | `contracts/qr/payload-format.json`, `contracts/qr/lifecycle.json` |
| QR-002 | QR Dinâmico | `contracts/qr/payload-format.json`, `contracts/qr/lifecycle.json` |
| QR-003 | Scan e resolução de QR | `contracts/qr/payload-format.json` |
| SDK-001 | TypeScript SDK | `contracts/events/types.json`, `contracts/webhooks/signature.json` |
| SDK-002 | PHP SDK | `contracts/webhooks/signature.json` |
| SDK-003 | Flutter SDK | `contracts/webhooks/signature.json`, `contracts/qr/payload-format.json` |
| SDK-004 | Go SDK | `contracts/webhooks/signature.json` |
| LED-001 | Ledger de dupla entrada | `contracts/events/envelope.schema.json` |
| LED-002 | Imutabilidade | `contracts/events/envelope.schema.json` |
| LED-003 | Operações atómicas | `contracts/events/envelope.schema.json` |

These are additive evidence entries — they do not require governance approval (only status changes do).

---

## Gap 4 — Missing protocol-specific fields

To make the existing studio schema serve as the BANZA protocol conformance matrix, these fields need to be added to `ValidationItem` in `lib/types.ts`:

```typescript
// Addition to ValidationItem (all optional for backwards compatibility)
certificationLevel?: 0 | 1 | 2 | 3 | 4
contractArtifacts?: string[]          // contracts/* files specifying this feature
conformanceVectors?: string[]         // conformance vector IDs (e.g. ["QR-001","QR-002"])
conformanceSuiteCases?: string[]      // wired suite case IDs
sdkCoverage?: Partial<Record<
  'typescript' | 'python' | 'php' | 'go' | 'flutter',
  'implemented' | 'partial' | 'missing' | 'not_applicable'
>>
kernelCrate?: string                  // Rust crate implementing this
referenceImplFile?: string            // sandbox-operator path
referenceImplFunction?: string
```

These are additive — existing items continue to work without them.

---

## Gap 5 — Python SDK header name bug

Discovered during audit. Unrelated to matrix schema but actionable:

**File:** `~/banza/sdk/python/banza/signature.py:27`  
**Current:** `SIGNATURE_HEADER = "Banzami-Signature"`  
**Correct:** `SIGNATURE_HEADER = "Banza-Signature"`  
**Impact:** Python webhook integrations will fail to locate the header in incoming requests.

---

## Recommended implementation sequence

### Immediate (before any commit)

1. **Remove Phase B matrix** from `~/banza/docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` — it conflicts with the existing, more sophisticated Banzami matrix.

2. **Retain the three Phase B audit reports** in `~/banza/docs/validation/` — they are accurate analysis documents regardless of which matrix schema is adopted.

3. **Fix Python SDK header name** — one-line change, no governance required.

### Short-term (next session)

4. **Add Phase A contract evidence to Banzami matrix** — edit `~/banzami/docs/validation/BANZAMI_IMPLEMENTATION_MATRIX.json` through the Validation Studio to add evidence entries for WH-*, QR-*, SDK-*, LED-* items pointing to the new contracts/. No status changes = no governance approval needed.

5. **Add protocol-specific fields to studio schema** — extend `lib/types.ts` with `certificationLevel`, `contractArtifacts`, `conformanceVectors`, `sdkCoverage`, `kernelCrate`. Backwards compatible — all optional.

6. **Decide matrix architecture** — either:
   - **Option A:** Single matrix in `~/banzami` tracks both Banzami product AND BANZA protocol conformance. Items get `certificationLevel` and `conformanceVectors` fields. Clean but mixes operator product with protocol governance.
   - **Option B:** Two separate matrices. `~/banzami/docs/validation/` = product matrix. `~/banza/docs/validation/` = protocol conformance matrix. Studio can be pointed at either. Cleanest institutional separation.

### Medium-term

7. **Wire conformance suite cases** — once certificationLevel is tracked, 55 vectors in `conformance/vectors/` can be wired into the suite files and linked from matrix items.

8. **Add SDK per-language status** — SDK-001 through SDK-004 currently have no language breakdown. Adding `sdkCoverage` allows tracking TypeScript at 93%, Python at 89%, PHP at 68%, Go at 43%, Flutter at 0%.

---

## What does NOT need to be done

- Do not rebuild the Validation Studio from scratch. It is already mature.
- Do not replace the `~/banzami` matrix with the Phase B matrix — the Phase B schema is inferior.
- Do not move the Validation Studio to `~/banza` — it belongs in `~/banzami` for product validation.
- Do not create a competing governance system in `~/banza` — use the existing studio schema as the base.

---

## Summary table

| Gap | Risk | Blocking | Fix |
|---|---|---|---|
| Phase B matrix schema conflict | HIGH | Yes — two competing schemas | Remove Phase B matrix file |
| Studio in wrong repo (per prompt) | CLARIFICATION | No — it's correctly in ~/banzami | Update shared understanding |
| Phase A contracts unlinked | MEDIUM | No | Add evidence entries via studio |
| Missing protocol fields | HIGH | Yes for certification | Extend schema (additive) |
| Python SDK header bug | HIGH | Yes for production | One-line fix |
| Conformance suite not wired | HIGH | Yes for L1 cert | Wire vectors to suite.json |
