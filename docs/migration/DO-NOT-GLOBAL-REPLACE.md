# DO NOT PERFORM A GLOBAL SEARCH-AND-REPLACE

**ADR:** ADR-025 — Ecosystem Naming Inversion  
**Version:** 1.0  
**Date:** 2026-05-29

---

## Why global replacement is forbidden

The strings "Banzami", "Banza", and "BanzamIA" appear in this codebase with **different semantic meanings** depending on context. A global search-and-replace cannot distinguish between meanings and will produce incorrect, broken, or legally dangerous results.

---

## Dangerous examples

### Example 1 — Protected domain name

`banzami.org` must remain unchanged.

A global replace of "Banzami" → "Banza" would produce `banza.org`, which is a different domain we may not own and would break every link on the internet pointing to the current website.

### Example 2 — Product vs. protocol

"The Banza app connects to the Banzami Protocol."

After inversion this becomes: "The Banzami app connects to the Banza Protocol."

A global replace of "Banza" → "Banzami" produces: "The Banzami app connects to the BanzamiProtocol." (double-replace).

A global replace of "Banzami" → "Banza" produces: "The Banza app connects to the Banza Protocol." (wrong — product is not renamed to Banza).

Neither a Banzami-first nor a Banza-first global replace produces the correct result.

### Example 3 — Legal entity in formal documents

Formal contracts and legal filings use "Banzami Lda" (the registered name). A global replace of "Banzami" → "Banza" in these documents would alter legally binding text.

### Example 4 — Package names with consumers

`banza-sdk` and `banzamia-client` are referenced by external developers. Renaming these in source without a deprecation/redirect plan breaks existing integrations silently.

### Example 5 — API routes

`/api/banzamia/chat` is a public endpoint. A global replace in route definitions changes the URL path, breaking every existing API consumer without warning.

---

## The correct process

1. **Find** every occurrence of "Banzami", "Banza", "BanzamIA" (case-sensitive and case-insensitive).
2. **Classify** each occurrence using `naming-classification-rules.md`.
3. **Check** the migration map in `naming-inversion-map.md` for the target name and any open decisions.
4. **Rename** only the classified occurrence, not all occurrences matching the same string.
5. **Commit** each wave separately so regressions are isolated and reviewable.

---

## Occurrences that MUST NOT be renamed without a separate decision

| Occurrence | Reason |
|------------|--------|
| `banzami.org` in any form | Registered domain — **PROTECTED** |
| `contact@banzami.org`, `security@banzami.org` | Email addresses — **PROTECTED** |
| `github.com/banzami` | GitHub organization — rename breaks all clone URLs; requires separate ADR |
| `@banzami` social handles | Requires platform coordination; separate decision |
| Published npm/crate/pub package names | Breaks consumer installations; requires deprecation plan |
| Database table/column names | Requires migration files and coordinated deploy |
| Legal entity name in formal documents | Legally binding text — `Banzami Lda` stays |

## Wire protocol identifiers — MIGRATE (not permanently protected)

The following were previously listed as permanently protected. **This was overridden by STEP-002B.** They must be migrated with a compatibility window:

| Occurrence | Canonical target | Compatibility |
|------------|-----------------|---------------|
| `/.well-known/banzami/operator.json` | `/.well-known/banza/operator.json` | Legacy path: 301 redirect |
| `BANZAMI:` QR prefix | `BANZA:` | Legacy prefix: accepted during window, not emitted |
| `BANZAMI-SBX:` QR prefix | `BANZA-SBX:` | Same |

See `naming-breaking-protocol-migration.md` for the full strategy.

---

## Tooling guidance

When searching for occurrences to classify:

```bash
# Find all occurrences (case-insensitive) across source files
grep -rn --include="*.ts" --include="*.tsx" --include="*.rs" \
  --include="*.go" --include="*.md" --include="*.svg" \
  -i "banzami\|banzamia\|banzai" .

# Exclude node_modules and build artifacts
grep -rn --exclude-dir=node_modules --exclude-dir=.next \
  --exclude-dir=target --exclude-dir=dist \
  --include="*.ts" --include="*.tsx" --include="*.md" \
  -i "banzami\|banzamia" .
```

Do not use the output of these commands to drive a batch replace. Use them to build your classification list first.
