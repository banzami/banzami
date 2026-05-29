# Naming Inversion — Conflict Register

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Status:** All conflicts UNRESOLVED — decisions required before renaming

---

## How to use this register

Each entry identifies a naming conflict that cannot be resolved by mechanical classification alone. A decision is needed before the corresponding migration wave can begin. Do NOT rename anything in the conflict's scope until a decision is recorded here.

Format per entry:

- **ID** — conflict reference
- **Wave blocked** — which wave cannot begin without this decision
- **The conflict** — what makes this ambiguous
- **Options** — possible resolutions
- **Recommendation** — if one option is clearly better
- **Decision** — to be filled in when resolved

---

## C-001 — SDK Package Scope Name: `@banza/*`

**Wave blocked:** Wave 6 (SDKs)  
**Classification would be:** PACKAGE

### The conflict

Currently, the TypeScript SDK is published under the `@banza` npm scope (e.g., `@banza/sdk`, `@banza/node`). After the naming inversion:

- **"Banza"** becomes the **protocol** name
- **"Banzami"** becomes the **product** name

The SDK enables developers to build operators and integrations on the **Banza protocol**. If the SDK is for building on the Banza protocol, then `@banza/sdk` is — after the inversion — the **more correct** name, not less correct.

### Options

**Option A — Keep `@banza/sdk` (no rename)**  
Rationale: The SDK is for the Banza protocol (formerly Banzami Protocol). After inversion, `@banza/sdk` correctly reflects "SDK for the Banza protocol." No breaking change. No deprecation needed.

**Option B — Rename to `@banzami/sdk`**  
Rationale: The SDK is primarily used by the Banzami product's developers. "Banzami" as the product operator uses the SDK. But this conflicts with the principle that SDKs expose protocol primitives, not product specifics.

**Option C — Create `@banza/sdk` as the protocol-level SDK and `@banzami/sdk` as a product-level wrapper**  
Rationale: Clean separation between protocol SDK and product SDK. But adds complexity and doubles package maintenance.

### Recommendation

**Option A** — Keep `@banza/sdk`. After the inversion, "Banza" is the protocol. The SDK is a protocol-level tool. The name becomes more accurate, not less. No rename needed.

### Decision

☐ UNRESOLVED — Fidel Monteiro to decide

---

## C-002 — SDK Client Class Name: `BanzaClient`

**Wave blocked:** Wave 6 (SDKs)  
**Classification would be:** CODE_SYMBOL + PACKAGE

### The conflict

The TypeScript and PHP SDKs expose a class named `BanzaClient`. After inversion:

- If "Banza" = protocol → `BanzaClient` means "client for the Banza protocol" → **this is correct after inversion**
- If resolution C-001 renames the SDK scope to `@banzami/sdk` → then the class should arguably be `BanzamiClient`

This conflict is downstream of C-001. If C-001 resolves to keep `@banza/sdk`, then `BanzaClient` is already correct and needs no rename.

### Options

**Option A — Keep `BanzaClient` (no rename)**  
Contingent on C-001 → Option A. "Client for the Banza protocol" is correct.

**Option B — Rename to `BanzamiClient`**  
Contingent on C-001 → Option B/C. Only makes sense if the SDK scope also becomes `@banzami`.

### Recommendation

**Option A** — contingent on C-001 Option A. Keep `BanzaClient`. It becomes more semantically accurate after inversion, not less.

### Decision

☐ UNRESOLVED — depends on C-001

---

## C-003 — BanzamIA Root Package: `@banzami/banzamia`

**Wave blocked:** Wave 4 (BanzAI UI)  
**Classification would be:** PACKAGE / AI_OS

### The conflict

The BanzamIA monorepo's root `package.json` is named `@banzami/banzamia`. After the naming inversion and the BanzamIA → BanzAI rename:

- The organization scope `@banzami` refers to the **product organization** (Banzami = product after inversion)
- But BanzAI (formerly BanzamIA) is a **protocol-level tool**, not a Banzami-product tool

Possible new names:
- `@banza/banzai` — "BanzAI, part of the Banza protocol ecosystem"
- `@banzami/banzai` — "BanzAI, published by Banzami organization"
- `banzai` — unscoped

Additionally: this is an **internal package** (not published to npm). The name only matters for the workspace and any tooling that reads it. Low stakes compared to published packages.

### Options

**Option A — Rename to `@banza/banzai`**  
Aligns with "BanzAI is a Banza protocol tool." Clean semantic alignment.

**Option B — Rename to `@banzami/banzai`**  
Aligns with "BanzAI is published by the Banzami organization." GitHub org is `banzami`; may want to keep the org scope.

**Option C — Keep `@banzami/banzamia` until repo renames are resolved (Wave 8)**  
Low risk — this is internal only. Rename when everything else is decided.

### Recommendation

**Option C** for now — defer until Wave 8, since this is internal only and the org scope question (`@banzami` vs `@banza`) depends on whether the GitHub org is renamed.

### Decision

☐ UNRESOLVED — Fidel Monteiro to decide

---

## C-004 — URL Route `/banzamia` on banzami.org

**Wave blocked:** Wave 3 (website copy) and Wave 4 (BanzAI UI)  
**Classification would be:** API_ROUTE + PUBLIC_COPY

### The conflict

The BanzamIA interface is served at `banzami.org/banzamia`. After the rename to BanzAI, the natural new URL would be `banzami.org/banzai`. However:

- **SEO impact:** Any existing links, bookmarks, or indexed pages at `/banzamia` would 404 or require a redirect.
- **Next.js routing:** Renaming the directory `app/banzamia/` to `app/banzai/` changes the URL path.
- **Redirect requirement:** A permanent redirect from `/banzamia` → `/banzai` would need to be added to `next.config.js`.

### Options

**Option A — Rename `/banzamia` → `/banzai`**  
Add permanent redirect in `next.config.js`. Users who bookmarked the old URL will be redirected automatically.

**Option B — Keep `/banzamia` URL path permanently**  
The directory name `app/banzamia/` stays. Only the page metadata/content changes to say "BanzAI." The URL remains `/banzamia` indefinitely (similar to how `banzami.org` stays even though the product is now "Banzami").

**Option C — Rename `/banzamia` → `/banzai` with redirect, then later `/banzai` → `/ai` (shorter)**  
Future clean-up option. Redirect chain: `/banzamia` → `/banzai`.

### Recommendation

**Option A** — rename to `/banzai` with a permanent redirect from `/banzamia`. The URL is new enough that SEO impact is minimal. Maintaining `/banzamia` as a permanent URL would create long-term confusion.

### Decision

☐ UNRESOLVED — Fidel Monteiro to decide

---

## C-005 — Component Directory: `components/banzamia/`

**Wave blocked:** Wave 4 (BanzAI UI)  
**Classification would be:** CODE_SYMBOL (directory)

### The conflict

The BanzamIA components live in `apps/docs/components/banzamia/`. After the rename to BanzAI, the directory should logically become `components/banzai/`. However:

- Renaming the directory requires updating every import path that references `components/banzamia/` (approximately 5–10 files).
- If the directory is not renamed, the physical path and the component names diverge (`components/banzamia/BanzAIChat.tsx` — confusing).

### Options

**Option A — Rename directory to `components/banzai/`**  
Clean. Update all imports. Minor effort.

**Option B — Keep directory as `components/banzamia/` temporarily**  
Defer directory rename to Wave 9. Allows Wave 4 to focus on component file renames and symbol renames without the additional import path changes.

### Recommendation

**Option B** for Wave 4, then clean up in **Wave 9**. Directory renames are mechanical and can happen after all the higher-stakes renaming is done.

### Decision

☐ UNRESOLVED (low stakes — can decide at start of Wave 4)

---

## C-006 — Canonical Reference Document Filename: `BANZAMI_REFERENCE.md`

**Wave blocked:** Wave 9 (final cleanup)  
**Classification would be:** PACKAGE / PUBLIC_COPY

### The conflict

The canonical reference document is `/Users/fm65/Banza/docs/BANZAMI_REFERENCE.md`. ADR-015 designates this file as the canonical source of truth and references it by name. After the inversion:

- "BANZAMI" in the filename refers to the **protocol** (now "Banza")
- The correct name would be `BANZA_REFERENCE.md`

However:
- ADR-015 references this filename explicitly
- All internal documentation links reference `BANZAMI_REFERENCE.md`
- External links (if any) would break

### Options

**Option A — Rename to `BANZA_REFERENCE.md`**  
Correct after inversion. Update ADR-015 and all internal links.

**Option B — Keep `BANZAMI_REFERENCE.md` permanently**  
The filename becomes a historical artifact (like `banzami.org` staying as the domain). Avoids link rot.

**Option C — Rename to `PROTOCOL_REFERENCE.md`**  
Neutral name that doesn't depend on the brand name. Future-proof if the brand changes again.

### Recommendation

**Option C** — `PROTOCOL_REFERENCE.md` is the most durable choice. The document describes the protocol; its name shouldn't need to change if the brand changes again. Update ADR-015 accordingly.

### Decision

☐ UNRESOLVED — Fidel Monteiro to decide

---

## C-007 — Protocol API Discovery URL: `/.well-known/banzami/operator.json`

**Wave blocked:** Permanently BLOCKED from rename without a new RFC  
**Classification would be:** API_ROUTE

### The conflict

The operator manifest discovery URL is `/.well-known/banzami/operator.json`. This is a normative protocol URL defined in RFC-0005 (or equivalent). After the inversion:

- The new protocol name is "Banza"
- The "correct" URL after inversion would be `/.well-known/banza/operator.json`

However:
- Every certified and deployed operator has already implemented `/.well-known/banzami/operator.json`
- Changing this URL is a **breaking change to the protocol wire format**
- All operators would need to simultaneously update their implementations
- The change requires a new RFC and a protocol version bump

### Decision

**This conflict CANNOT be resolved in this migration without a protocol version.**

`/.well-known/banzami/operator.json` remains as-is. A future RFC can introduce `/.well-known/banza/operator.json` in a new protocol version with a compatibility period.

### Status

✅ RESOLVED — KEEP AS-IS. No migration action.

---

## C-008 — QR Payload Prefixes: `BANZAMI-SBX:` and `BANZAMI:`

**Wave blocked:** Permanently BLOCKED from rename without a new RFC  
**Classification would be:** API_ROUTE

### The conflict

QR payment codes use the prefixes `BANZAMI-SBX:` (sandbox) and `BANZAMI:` (production). These are:

- Normative protocol strings
- Encoded in every QR code ever generated
- Validated by all scanners

Renaming to `BANZA-SBX:` and `BANZA:` would invalidate all existing QR codes.

### Decision

**RESOLVED — KEEP AS-IS.** A future RFC introducing QR protocol v2 can define new prefixes with a compatibility period where both are accepted.

### Status

✅ RESOLVED — KEEP AS-IS. No migration action.

---

## C-009 — `Banza-Signature` Webhook Header

**Wave blocked:** Wave 6 (SDKs)  
**Classification would be:** API_ROUTE / CODE_SYMBOL

### The conflict

Webhook payloads are signed and verified using a header called `Banza-Signature`. After inversion:

- "Banza" = protocol → `Banza-Signature` becomes the correct name for a "protocol-level signature"
- However, this was named when "Banza" = product

Does this header need renaming? After inversion, `Banza-Signature` actually becomes more semantically correct (it's a signature from the Banza protocol, not from the Banzami product).

### Decision

☐ LIKELY NO RENAME NEEDED — but confirm that `Banza-Signature` (Banza = protocol) is the intended meaning. If yes, update documentation to reflect the corrected semantics without changing the actual header value.

### Status

☐ UNRESOLVED — confirm with Fidel Monteiro

---

## Conflict Summary

| ID | Description | Wave Blocked | Status |
|----|-------------|-------------|--------|
| C-001 | SDK package scope `@banza/*` | 6 | UNRESOLVED |
| C-002 | `BanzaClient` class name | 6 | UNRESOLVED (depends on C-001) |
| C-003 | BanzamIA root package name | 4 | UNRESOLVED (defer recommended) |
| C-004 | URL route `/banzamia` | 3 | UNRESOLVED |
| C-005 | Component directory name | 4 | UNRESOLVED (defer recommended) |
| C-006 | `BANZAMI_REFERENCE.md` filename | 9 | UNRESOLVED |
| C-007 | `/.well-known/banzami/` URL | — | RESOLVED: KEEP AS-IS |
| C-008 | `BANZAMI-SBX:` / `BANZAMI:` QR prefixes | — | RESOLVED: KEEP AS-IS |
| C-009 | `Banza-Signature` header | 6 | UNRESOLVED (likely no rename) |

**Minimum required before Wave 3 begins:** Resolve C-004  
**Minimum required before Wave 6 begins:** Resolve C-001, C-002, C-009
