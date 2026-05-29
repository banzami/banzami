# Wave 2 Migration Report — SVG Diagram Label Migration

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Executed by:** BANZA-NAMING-INVERSION-STEP-004  
**Status:** Complete

---

## Summary

Wave 2 migrated all human-readable SVG text labels across the three ecosystem repositories. The naming inversion is now reflected in all SVG diagram labels: Banza appears as the protocol/infrastructure, Banzami appears as the product, and BanzAI appears as the Protocol Operating System.

| Metric | Count |
|--------|-------|
| Total SVG files scanned | 75 |
| Files modified | 65 |
| Files unchanged (no occurrences) | 10 |
| Manual fixes applied | 1 |

---

## Files Modified by Repository

| Repository | Files Modified | Insertions | Deletions |
|------------|---------------|------------|-----------|
| Banzami (kernel) | 7 | 14 | 14 |
| BanzamIA (AI OS) | 0 | 0 | 0 |
| Banza (operator) | 58 | 201 | 201 |
| **Total** | **65** | **215** | **215** |

---

## Rename Rules Applied

The following transformations were applied using the same placeholder-swap logic as Wave 1 (code-block-unaware — SVGs have no code blocks):

| Old (pre-inversion) | New (post-inversion) | Class |
|---------------------|---------------------|-------|
| BanzamIA | BanzAI | AI_OS |
| Banzami Kernel | Banza Kernel | PROTOCOL |
| Banzami Ecosystem | Banza Ecosystem | PROTOCOL |
| Banzami Protocol | Banza Protocol | PROTOCOL |
| Banzami Sandbox Operator | Banza Sandbox Operator | PROTOCOL |
| BANZAMI KERNEL | BANZA KERNEL | PROTOCOL (all-caps) |
| BANZAMIA | BANZAI | AI_OS (all-caps) |
| BANZAMIA (Portuguese forms) | BANZAI | AI_OS (all-caps Portuguese) |
| BANZAMI (protocol context) | BANZA | PROTOCOL (all-caps) |
| Banzami Sandbox | Banzami Sandbox | — (already product-correct, unchanged) |
| Banza (product/operator) | Banzami | PRODUCT |
| Banza Wallet | Banzami Wallet | PRODUCT |
| Banza Business | Banzami Business | PRODUCT |
| Banza QR · Checkout · Pay Links | Banzami QR · Checkout · Pay Links | PRODUCT |
| Banza SDK · API | Banzami SDK · API | PRODUCT |
| BanzamIA — AI-native Protocol Agent | BanzAI — Protocol Operating System | AI_OS + label |
| AI-native Protocol Agent | Protocol Operating System | AI_OS label |
| Agente de Protocolo nativo de IA | Sistema Operativo de Protocolo | AI_OS label (PT) |

---

## Protected Occurrences — Skipped

| String | Class | Reason |
|--------|-------|--------|
| `BANZAMI:` | WIRE_FORMAT | QR wire format prefix — Wave 5c |
| `BANZAMI-SBX:` | WIRE_FORMAT | Sandbox QR wire format prefix — Wave 5c |
| `/.well-known/banzami/` | WIRE_FORMAT | Operator manifest path — Wave 5c |
| `banzami.org` | DOMAIN | Registered domain — protected |
| `Banzami Lda` | ORG | Legal entity name — protected |
| `@banza` | IDENTITY_NAMESPACE | Network identity handle — permanent |
| `Banza-Signature` | API_ROUTE | Webhook header — protected |
| `>BANZAMI<` (isolated node) | ORG | brand-architecture.svg root node — org entity is still Banzami |
| `BANZAMI_IMPLEMENTATION_MATRIX` | CODE_SYMBOL | Code identifier — Wave 9 |
| `BANZAMI_REFERENCE` | CODE_SYMBOL | Code identifier — Wave 9 |

**Total protected occurrences preserved: 12 categories**

---

## Manual Fix Applied

### `protocol-graph-explorer.svg` (Banza operator — docs + apps/docs)

These labels were **already using the new naming** before Wave 2 ran (the SVG was authored post-inversion-decision):

- `Banza Protocol Spec` — already correct in new naming
- `Banza Protocol Specification v1.0.0` — already correct in new naming

The automated transform incorrectly changed them to `Banzami Protocol Spec` (treating `Banza` as product context). Reverted with a targeted `sed` fix immediately after the automated pass.

---

## Key Files Updated

### Banzami (kernel) repository

| File | Changes |
|------|---------|
| `conformance/badges/protocol-compatible.svg` | "Banzami" → "Banza" (protocol badge label) |
| `conformance/badges/federation-ready.svg` | "Banzami" → "Banza" |
| `conformance/badges/settlement-compatible.svg` | "Banzami" → "Banza" |
| `conformance/badges/trace-compatible.svg` | "Banzami" → "Banza" |
| `docs/images/architecture/event-flow.svg` | "Banzami Kernel" → "Banza Kernel" |
| `docs/images/architecture/provider-model.svg` | "Banzami Kernel" → "Banza Kernel"; "BANZAMI KERNEL CRATES" → "BANZA KERNEL CRATES" |
| `docs/images/reference/sandbox-architecture.svg` | "Banzami Sandbox Operator" → "Banza Sandbox Operator"; "BANZAMI KERNEL CRATES" → "BANZA KERNEL CRATES" |

### BanzamIA repository

No SVG files present. No changes needed.

### Banza (operator) repository

All architecture diagrams in `docs/images/architecture/` and `apps/docs/public/images/architecture/` (shared set plus extras in apps only):

| File | Key Changes |
|------|-------------|
| `banzami-ecosystem.svg` | Title: Banza Ecosystem; Kernel: BANZA KERNEL; Ref Operator: Banzami; Sandbox: Banzami Sandbox; AI OS: BANZAI — Protocol Operating System |
| `banzamia-canonical-architecture.svg` | Title: Banza — Canónica; Protocol layer: Protocolo Banza; BanzAI labels updated |
| `banzamia-cognitive-layer.svg` | "BanzAI — Protocol Operating System" (was AI-native Protocol Agent); Kernel Banza label |
| `banzamia-product-architecture.svg` | "BanzAI — Protocol Operating System"; subtitle updated |
| `banzamia-internal-architecture.svg` | "BanzAI — Task Router"; all-caps subtitle updated |
| `banzamia-force-multiplier.svg` | "× BanzAI" (×5); subtitles updated |
| `force-multiplier-model.svg` | "× BanzAI" (×6); subtitles updated |
| `banzamia-model-routing.svg` | Title and footer updated |
| `banzamia-knowledge-gap.svg` | All-caps labels: SEM BANZAI, COM BANZAI |
| `banzamia-truth-model.svg` | Footer principle attribution updated |
| `protocol-operating-system.svg` | Title and body: BanzAI Vision |
| `roadmap-architecture.svg` | Title and footer |
| `autonomous-protocol-vision.svg` | Phase 4: BanzAI label |
| `protocol-self-explanation.svg` | COM BANZAI / SEM BANZAI labels |
| `protocol-adoption-economics.svg` | COM BANZAI / SEM BANZAI labels |
| `ecosystem-intelligence-layer.svg` | All-caps subtitle updated |
| `rag-evaluation-architecture.svg` | Subtitle updated |
| `graph-enhanced-retrieval.svg` | Subtitle updated |
| `protocol-graph-architecture.svg` | Subtitle: BANZAI KNOWLEDGE GRAPH |
| `agentic-research-flow.svg` | Footer: BanzAI · Protocol Research Agent |
| `federation-intelligence.svg` | Footer updated |
| `certification-copilot.svg` | Footer updated |
| `protocol-simulator.svg` | Footer updated |
| `protocol-memory.svg` | Footer updated |
| `operator-digital-twin.svg` | Footer updated |
| `quality-dashboard-architecture.svg` | Footer updated |
| `protocol-graph-explorer.svg` | Footer updated; Banza Protocol Spec preserved (manual fix) |
| `brand-architecture.svg` (apps only) | "Banzami" product column, Banzami Wallet/Business/QR/SDK, BanzAI; root "BANZAMI" org node preserved |
| `certification-flow.svg` (apps only) | "BanzAI Manifest Validator"; "BanzAI Conformance" |
| `federation.svg` (apps only) | "Federação Banza" |
| `security-layers.svg` (apps only) | "App Banzami · Banzami Business" |

---

## Validation

| Check | Result |
|-------|--------|
| `BANZAMI:` wire format preserved | ✓ — QR lifecycle SVG unchanged |
| `BANZAMI-SBX:` preserved | ✓ — sandbox QR prefix intact |
| `banzami.org` domain preserved | ✓ — all footer citations intact |
| `@banza` identity handle preserved | ✓ — brand-architecture.svg SDK label unchanged |
| `Banza-Signature` preserved | ✓ — no occurrence in SVG files |
| ORG root "BANZAMI" preserved | ✓ — brand-architecture.svg root node intact |
| `BANZAMI_IMPLEMENTATION_MATRIX` preserved | ✓ — code identifier in ecosystem SVG governance badge |
| No `BanzamIA` remaining in SVG text | ✓ — zero occurrences in `<text>` elements |
| No `Banza Wallet / Banza Business` remaining | ✓ — all converted to Banzami product labels |
| No `Banzami Kernel` remaining | ✓ — all converted to Banza Kernel |
| No accidental double-swaps | ✓ — verified with targeted grep |
| Protocol-graph-explorer manual fix applied | ✓ — Banza Protocol Spec restored correctly |

---

## Occurrences Not Changed (Intentional)

| Category | Reason | Wave |
|----------|--------|------|
| SVG `id`, `class`, `href` attributes | Element identifiers — deferred | Wave 9 |
| SVG filename paths in `href` / `src` | Filename renames — deferred | Wave 9 |
| Wire format strings in text | Protocol constants — Wave 5c | 5c |
| Code symbol names in any SVG text | Code identifiers — Wave 7/9 | 7/9 |
| `BANZAMI_IMPLEMENTATION_MATRIX` | Code identifier | 9 |
| `BANZAMI_REFERENCE` | Code identifier | 9 |
| ORG entity root in brand-architecture.svg | ORG class — permanent | — |

---

## Remaining Waves

| Wave | Scope | Status |
|------|-------|--------|
| 1 | Documentation prose (ADRs, READMEs, reference docs) | **✓ COMPLETE** |
| 2 | SVG diagram text labels | **✓ COMPLETE** |
| 3 | Website copy (banzami.org pages, metadata) | Pending |
| 4 | BanzAI UI components, routes, lib rename | Pending |
| 5a | Env vars (`BANZAMIA_*` → `BANZAI_*`), Docker | Pending |
| 5b | BanzAI API routes (`/banzamia` → `/banzai`) | Pending |
| 5c | Wire format (QR prefixes, operator manifest path) | Pending |
| 6 | SDK documentation, Python SDK rename | Pending |
| 7 | Rust crates (`banzami-*` → `banza-*`), code symbols | Pending |
| 8 | GitHub repository renames (separate ADR required) | Pending — ADR-026 needed |
| 9 | Final cleanup (directory/filename renames) | Pending |
