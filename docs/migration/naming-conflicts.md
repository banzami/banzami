# Naming Inversion — Conflict Register

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29  
**Status:** C-001, C-002, C-004, C-009, C-010 RESOLVED. C-007, C-008 overridden by STEP-002B — migrate. C-003, C-005, C-006 unresolved.

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

✅ **RESOLVED (STEP-002B) — Option A: `@banza/sdk` remains canonical.** Banza is the protocol; the SDK is a protocol-level tool. No rename needed for the npm scope.

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

✅ **RESOLVED (STEP-002B) — Option A: `BanzaClient`, `BanzaError`, `BanzaPay` remain canonical.** C-001 resolved to keep `@banza/sdk`; these class names follow. No rename needed.

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

✅ **RESOLVED (STEP-002B) — Canonical route is `/banzai`. Legacy `/banzamia` may redirect temporarily. Implement permanent redirect in `next.config.js`.**

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

**Wave blocked:** Wave 5 (wire format migration)  
**Classification would be:** API_ROUTE

### STEP-002B Override

Previously marked "RESOLVED: KEEP AS-IS." This decision is overridden by STEP-002B.

**The naming inversion is total.** Wire protocol identifiers are migrated as part of the naming inversion. This is a breaking protocol migration and must be versioned and tested.

### Decision

✅ **RESOLVED (STEP-002B overrides STEP-002) — MIGRATE.**

- **Canonical:** `/.well-known/banza/operator.json`
- **Legacy (compatibility window):** `/.well-known/banzami/operator.json` → 301 redirect to canonical
- Operators should serve the redirect immediately; discovery clients should fetch the canonical path
- See `naming-breaking-protocol-migration.md` for full compatibility strategy

### Status

✅ RESOLVED — MIGRATE in Wave 5c.

---

## C-008 — QR Payload Prefixes: `BANZAMI-SBX:` and `BANZAMI:`

**Wave blocked:** Wave 5 (wire format migration)  
**Classification would be:** API_ROUTE

### STEP-002B Override

Previously marked "RESOLVED: KEEP AS-IS." This decision is overridden by STEP-002B.

**The naming inversion is total.** Wire protocol identifiers are migrated as part of the naming inversion. This is a breaking protocol migration and must be versioned and tested.

### Decision

✅ **RESOLVED (STEP-002B overrides STEP-002) — MIGRATE.**

- **Canonical prefixes:** `BANZA:` (production), `BANZA-SBX:` (sandbox)
- **Legacy prefixes (compatibility window):** `BANZAMI:` and `BANZAMI-SBX:` accepted by validators; not emitted by generators
- Generators must emit only canonical prefixes immediately after migration
- Validators accept legacy prefixes during compatibility window; reject after sunset
- See `naming-breaking-protocol-migration.md` for full compatibility strategy and test requirements

### Status

✅ RESOLVED — MIGRATE in Wave 5c.

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

✅ **RESOLVED (STEP-002B) — NO RENAME.** After inversion, "Banza" = protocol. `Banza-Signature` correctly means "signature from the Banza protocol." The header value is already semantically correct under the new naming. Update documentation to reflect this — the header does not change, but its name is now more accurate than before.

---

## C-010 — Identity Handle Namespace: `@banza`

**Wave blocked:** None (permanent exception — no migration action required)  
**Classification would be:** IDENTITY_NAMESPACE

### The conflict

After the naming inversion, "Banza" becomes the protocol name. The ecosystem identity handle prefix is `@banza` (e.g., `@banza:joao`, `@banza:empresa-x`). A question arises: should the handle namespace follow the product name (becoming `@banzami`) or the protocol name?

### Options

**Option A — Keep `@banza` as the canonical handle namespace (permanent)**  
Rationale: `@banza` is shorter, easier to say verbally, better for QR and social network effects. Users say "send it to my banza." The namespace belongs to the identity layer, not the brand layer. After inversion, "Banza" = protocol, which is appropriate — network identities live at the protocol level, not the product level.

**Option B — Rename handle namespace to `@banzami`**  
Rationale: The product is Banzami; consumers interact with Banzami. But this would make handles longer and harder to share. It would also treat identity as a product feature rather than a protocol primitive.

### Decision

✅ **RESOLVED (STEP-002C) — Option A: `@banza` is the permanent canonical handle namespace.**

- Network identity handles are: `@banza:name`
- The namespace is classified as `IDENTITY_NAMESPACE` — a new class added in STEP-002C
- This is a permanent exception, not a deferred one. It will not be renamed in any future wave.
- Rationale: Identity handles live at the protocol layer (`@banza` = identity on the Banza network). They must remain stable even if product or AI OS names change again. Shorter handles are better for usability.

---

## Conflict Summary

| ID | Description | Wave Blocked | Status |
|----|-------------|-------------|--------|
| C-001 | SDK package scope `@banza/*` | 6 | ✅ RESOLVED: keep `@banza/sdk` |
| C-002 | `BanzaClient` class name | 6 | ✅ RESOLVED: keep `BanzaClient` |
| C-003 | BanzamIA root package name | 4 | ☐ UNRESOLVED (defer recommended) |
| C-004 | URL route `/banzamia` | 3 | ✅ RESOLVED: canonical is `/banzai` |
| C-005 | Component directory name | 4 | ☐ UNRESOLVED (defer to Wave 9) |
| C-006 | `BANZAMI_REFERENCE.md` filename | 9 | ☐ UNRESOLVED |
| C-007 | `/.well-known/banzami/` URL | 5c | ✅ RESOLVED: MIGRATE → `/.well-known/banza/` |
| C-008 | `BANZAMI-SBX:` / `BANZAMI:` QR prefixes | 5c | ✅ RESOLVED: MIGRATE → `BANZA-SBX:` / `BANZA:` |
| C-009 | `Banza-Signature` header | — | ✅ RESOLVED: no rename (already correct after inversion) |
| C-010 | `@banza` identity handle namespace | — | ✅ RESOLVED: permanent `@banza` (STEP-002C) |

**Minimum required before Wave 3 begins:** ✅ C-004 resolved  
**Minimum required before Wave 5c begins:** ✅ C-007, C-008 resolved  
**Minimum required before Wave 6 begins:** ✅ C-001, C-002, C-009 resolved  
**Remaining unresolved:** C-003 (low stakes), C-005 (low stakes), C-006 (deferred to Wave 9)
