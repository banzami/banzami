# Conformance Repair Plan

**Mission:** CONFORMANCE-CROSS-REPO-REPAIR-001  
**Date:** 2026-05-30  
**Status:** Official

---

## Wave A — Immediate Fixes for Green CI

Applies to: banza, banzai  
Effort: < 5 minutes total  
Risk: Zero

### A-1: banza — Fix sandbox-operator binary path

**File:** `banza/.github/workflows/conformance.yml`  
**Line:** 241

```yaml
# BEFORE
./reference/sandbox-operator/target/release/sandbox-operator &

# AFTER
./reference/target/release/sandbox-operator &
```

**Why:** Cargo workspace builds binaries in the workspace root `target/` directory, not in the member crate's directory. The workspace is at `reference/`, so the binary lands at `reference/target/release/sandbox-operator`.

**Effect:** The `reference-conformance` job proceeds past the binary start step, the health check passes, the conformance runner executes, and the Level 2 certification gate is evaluated.

**Verification:** Push to main → GitHub Actions → `Conformance / Reference operator conformance (Level 2)` turns green.

---

### A-2: banzai — Fix type-check script name

**File:** `banzai/.github/workflows/ci.yml`  
**Line:** 26

```yaml
# BEFORE
run: npm run type-check --workspaces --if-present

# AFTER
run: npm run typecheck --workspaces --if-present
```

**Why:** All workspace packages define `"typecheck"` (no hyphen). The CI was calling `type-check` (hyphenated), which does not exist. The `--if-present` flag suppressed the error, causing a silent no-op. The fix makes CI actually run type checks.

**Effect:** CI now runs the real `typecheck` script in every workspace package. Any TypeScript type errors that existed silently will surface.

**Pre-fix check:** Confirm `npm run typecheck --workspaces --if-present` would pass locally before pushing. If there are latent type errors, they must be fixed alongside this change.

---

### A-3: banzai — Fix lint step

**File:** `banzai/.github/workflows/ci.yml`  
**Line:** 29

Option 1 (recommended — enforce lint now):
```yaml
# BEFORE
run: npm run lint --workspaces --if-present

# AFTER — remove the step OR replace with typecheck
# (lint scripts do not exist in any workspace package)
# Remove the lint step entirely and add it back when lint is wired
```

Option 2 (interim — keep step but document intent):
```yaml
- name: Lint (TODO — wire eslint per workspace)
  run: echo "Lint step placeholder — add eslint to workspace packages"
```

**Decision:** Remove the silent no-op lint step. Add it back in Wave C when eslint is properly wired per workspace.

---

## Wave B — Structural Fixes

Applies to: banzami  
Effort: ~30 minutes  
Risk: Low (mechanical rename, no behavior change)

### B-1: banzami — Update Go module paths to `banza-protocol` org

**Scope:** 3 `go.mod` files + 58 Go source files

**Files requiring go.mod change:**
- `banzami/services/api-gateway/go.mod:1`
- `banzami/services/admin-api/go.mod:1`
- `banzami/services/public-api/go.mod:1`

```
# BEFORE
module github.com/banzami/banzami/services/<name>

# AFTER
module github.com/banza-protocol/banzami/services/<name>
```

**All Go source files:** Replace all import strings.

```bash
# Mechanical find-and-replace across all three services
find services -name "*.go" -exec sed -i '' \
  's|github.com/banzami/banzami/services/|github.com/banza-protocol/banzami/services/|g' {} \;
```

**After:**

```bash
# Verify no stale imports remain
grep -r "github.com/banzami" services --include="*.go"
# Expected: no output

# Verify Go builds still compile
cd services/api-gateway && go build ./... && go vet ./...
cd services/admin-api && go build ./... && go vet ./...
cd services/public-api && go build ./... && go vet ./...
```

**Why it matters:**
- ADR-025 compliance: module paths should reflect the canonical org
- `go get github.com/banza-protocol/banzami/services/api-gateway` would resolve
- Future tooling that validates module paths against GitHub URLs will pass

**Risk:** Low. The rename is purely mechanical — no functional code changes. The Go compiler treats module paths as identifiers, so as long as go.mod and imports are consistent after the rename, all tests pass.

---

### B-2: banzai — Update root package.json name

**File:** `banzai/package.json`  
**Line:** 2

```json
// BEFORE
"name": "@banzami/banzamia"

// AFTER
"name": "@banza-protocol/banzai"
```

Then regenerate the lockfile:

```bash
cd ~/banzai
npm install  # regenerates package-lock.json with new name
```

**Why it matters:**
- ADR-025 compliance: the package name is stale
- `package-lock.json` will contain the new name after npm install
- Any npm publish or workspace tooling referencing this name will use the canonical identifier

**Risk:** Low for a private workspace. The `"private": true` flag means this package is never published. However, the lockfile name is not functionally meaningful — the main risk is breaking any internal script that references `@banzami/banzamia` by name.

**Pre-fix check:** Search for any reference to `@banzami/banzamia` in package.json files across the workspace:

```bash
grep -r "@banzami/banzamia" ~/banzai --include="*.json" --include="*.ts"
```

If references exist in workspace dependencies, they must be updated simultaneously.

---

## Wave C — Future Hardening

Applies to: all three repos  
Effort: variable  
Risk: low

### C-1: banzai — Wire eslint per workspace

Add `"lint": "eslint src"` to each workspace `package.json` and configure shared eslint config via `tsconfig.base.json`. Then re-enable the lint step in `ci.yml`.

### C-2: banza — Add health-check failure gate

The current sandbox-operator startup loop silently succeeds even if the operator never starts:

```bash
for i in $(seq 1 20); do
  if curl -sf http://localhost:3000/health > /dev/null 2>&1; then
    echo "Operator ready"
    break
  fi
  sleep 1
done
```

If the operator fails to start, the loop exits normally and the conformance runner runs against a non-listening port. Add an explicit failure gate:

```bash
ready=false
for i in $(seq 1 20); do
  if curl -sf http://localhost:3000/health > /dev/null 2>&1; then
    echo "Operator ready after ${i}s"
    ready=true
    break
  fi
  sleep 1
done
if [ "$ready" != "true" ]; then
  echo "Operator failed to start within 20s"
  exit 1
fi
```

### C-3: banza — Pin conformance runner Python version

The workflow runs `python3` without pinning a version. Add:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
```

This prevents silent failures when the runner OS changes the default Python version.

### C-4: banzami — Add Go module path CI check

Add a CI step that asserts module paths match the canonical org:

```yaml
- name: Verify Go module paths
  run: |
    for f in services/*/go.mod; do
      if grep -q "github.com/banzami/" "$f"; then
        echo "FAIL: Stale module path in $f"
        exit 1
      fi
    done
    echo "All Go module paths are canonical"
```

### C-5: banzai — Replace turbo CI with direct npm typecheck

The banzai CI's current approach (`npm run typecheck --workspaces --if-present`) is fragile. A more robust approach:

```yaml
- name: Type check
  run: npx turbo run typecheck
```

`turbo run typecheck` uses the pipeline defined in `turbo.json` and caches results — it's both more correct and faster than `--workspaces`.

---

## Repair Execution Order

```
Wave A (green CI immediately):
  1. banza: fix line 241 of conformance.yml
  2. banzai: fix line 26 of ci.yml (type-check → typecheck)
  3. banzai: remove or replace line 29 of ci.yml (lint no-op)
  Commit + push each repo independently

Wave B (structural, same session if time allows):
  4. banzami: sed replace all Go module paths (go.mod + source)
  5. banzai: update package.json name + npm install
  Commit + push

Wave C (future sprint):
  6. banzai: wire eslint
  7. banza: add health-check failure gate
  8. banza: pin Python version
  9. banzami: add module path assertion step
  10. banzai: switch to turbo run typecheck
```

---

## Success Criteria

| Check | Repo | Expected after Wave A |
|-------|------|-----------------------|
| `Conformance / Validate conformance vectors` | banza | ✓ Green |
| `Conformance / OpenAPI compatibility check` | banza | ✓ Green |
| `Conformance / Schema compatibility check` | banza | ✓ Green |
| `Conformance / QR payload compatibility` | banza | ✓ Green |
| `Conformance / Trace contract check` | banza | ✓ Green |
| `Conformance / Manifest schema validation` | banza | ✓ Green |
| **`Conformance / Reference operator conformance (Level 2)`** | **banza** | **✓ Green (was failing)** |
| `CI / TypeScript — build, lint, type-check` | banzai | ✓ Green (actually runs typecheck now) |
| `CI / Rust — build, lint, test` | banzami | ✓ Green |
| `CI / Go api-gateway — vet, test` | banzami | ✓ Green |
| `CI / Go admin-api — vet, test` | banzami | ✓ Green |
| `CI / Go public-api — vet, test` | banzami | ✓ Green |
| `CI / TypeScript SDK — typecheck, test` | banzami | ✓ Green |

---

*Produced by: CONFORMANCE-CROSS-REPO-REPAIR-001 — 2026-05-30*
