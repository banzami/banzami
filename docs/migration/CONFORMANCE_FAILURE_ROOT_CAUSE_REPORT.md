# Conformance Failure Root Cause Report

**Mission:** CONFORMANCE-CROSS-REPO-REPAIR-001  
**Date:** 2026-05-30  
**Scope:** All GitHub Actions workflows across banza, banzai, banzami  
**Status:** Official

---

## Executive Summary

Three classes of defect were identified across the three repositories. One causes a hard CI failure (red build). One causes a silent false positive (green build, tests not running). One is structural technical debt (no CI impact, identity violation).

| ID | Repo | Severity | Type | CI Impact |
|----|------|----------|------|-----------|
| RCA-001 | banza | **CRITICAL** | Binary path wrong | Hard FAIL — `reference-conformance` job |
| RCA-002 | banzai | **MEDIUM** | Script name mismatch | Silent PASS — type-check and lint never run |
| RCA-003 | banzami | **LOW** | Go module path stale | No CI failure — structural debt only |

---

## RCA-001 — banza: Binary Path Wrong in `reference-conformance` Job

### Severity: CRITICAL

### Location

`banza/.github/workflows/conformance.yml` — lines 236–241

### Exact Failing Step

```
Job: reference-conformance (Reference operator conformance Level 2)
Step: Start sandbox operator
```

### Command Executed

```bash
./reference/sandbox-operator/target/release/sandbox-operator &
```

### Error Output (expected on GitHub Actions)

```
bash: ./reference/sandbox-operator/target/release/sandbox-operator: No such file or directory
```

The health-check loop (20 × 1s) runs and exits normally because the `if curl -sf` is inside a loop with no `else exit 1`. The `OPERATOR_PID` env var is set to the PID of the failed bash process. The conformance runner then hits `http://localhost:3000` which is not listening, causing connection refused. The `Check certification level achieved` step then reads a missing `conformance-report.json` and fails.

### Root Cause

`reference/Cargo.toml` declares a **Cargo workspace** with `sandbox-operator` as a member:

```toml
[workspace]
members = [
    "sandbox-operator",
    ...
]
```

When `cargo build --release` is executed in a workspace member directory (`reference/sandbox-operator/`), Cargo places the compiled binary in the **workspace root's target directory** — not in the member's own directory.

| Expected by workflow | Actual binary location |
|----------------------|------------------------|
| `./reference/sandbox-operator/target/release/sandbox-operator` | `./reference/target/release/sandbox-operator` |

### Binary Target Name

The binary target in `reference/sandbox-operator/Cargo.toml`:

```toml
[[bin]]
name = "sandbox-operator"
path = "src/main.rs"
```

Binary name is `sandbox-operator` — confirmed correct. Only the path prefix is wrong.

### Impact

- `reference-conformance` job fails on every push to `main` and every PR
- All jobs that `needs: [validate-vectors, schema-compat, trace-contract]` are upstream of `reference-conformance` — they pass correctly; only the final conformance run fails
- The Level 2 certification gate is never actually evaluated

### Required Fix

```yaml
# conformance.yml line 241 — BEFORE
./reference/sandbox-operator/target/release/sandbox-operator &

# AFTER
./reference/target/release/sandbox-operator &
```

### Risk

Zero. The binary name is correct. Only the directory segment `sandbox-operator/` must be removed from the path.

---

## RCA-002 — banzai: Script Name Mismatch in `ci.yml`

### Severity: MEDIUM (silent false positive)

### Location

`banzai/.github/workflows/ci.yml` — lines 26–35

### What CI Reports

Green (passing). No failure.

### What Is Actually Not Running

The following steps execute `npm run <script> --workspaces --if-present`. The `--if-present` flag causes npm to silently skip any workspace package that does not have the named script. Every package skips → the step exits 0 with no output.

| CI step | Script called | Scripts in workspace packages | Result |
|---------|--------------|-------------------------------|--------|
| Type check | `type-check` | `typecheck` (all packages) | All packages skip → silent pass |
| Lint | `lint` | Not defined in any package | All packages skip → silent pass |
| Build | `build` | All packages have `build` | Actually runs |
| Test | `test` | Only `apps/api` has `test` | Runs for `apps/api` only |

### Root Cause

The workflow was written using `type-check` (hyphenated), matching the npm conventional style. The workspace packages use `typecheck` (camelCase, no hyphen), matching the Turbo pipeline convention defined in `turbo.json`:

```json
{
  "tasks": {
    "typecheck": { ... },
    "lint": {}
  }
}
```

`turbo.json` defines a `lint` task, but no workspace `package.json` has a `lint` script entry — meaning `turbo run lint` would be a no-op, and the npm script `lint` doesn't exist in any workspace.

### Impact

- The banzai CI always shows green even when TypeScript type errors are introduced
- No lint is ever enforced in CI
- The false signal is dangerous: a broken type in `apps/api` or `core/rag` would not block a PR

### Required Fix

```yaml
# ci.yml line 26 — BEFORE
run: npm run type-check --workspaces --if-present

# AFTER
run: npm run typecheck --workspaces --if-present
```

For lint: either add `"lint": "..."` scripts to each workspace package, or remove the lint step from the CI until lint is wired. The correct choice is to add lint (e.g., `eslint`) to each workspace and then enable it. As an interim fix, the lint step can call `typecheck` as well, or be commented out with a TODO.

### Risk

Low for the fix itself (renaming the npm script call). The change turns a silent pass into a real gate — meaning any existing type errors that were silently ignored will now surface. This is the correct outcome.

---

## RCA-003 — banzami: Go Module Paths Not Updated to `banza-protocol` Org

### Severity: LOW (structural debt, no CI failure)

### Location

- `banzami/services/api-gateway/go.mod:1`
- `banzami/services/admin-api/go.mod:1`
- `banzami/services/public-api/go.mod:1`

### Current State

All three Go service `go.mod` files declare the old GitHub org in their module path:

```
module github.com/banzami/banzami/services/api-gateway
module github.com/banzami/banzami/services/admin-api
module github.com/banzami/banzami/services/public-api
```

All 58 Go source files that import internal packages use matching paths, so the imports are internally consistent. `go vet ./...` and `go test ./...` pass.

### Why It Is Not a CI Failure

Go module paths are namespace identifiers, not live fetch targets for local builds. The CI runs `go vet ./...` and `go test ./...` within each service directory, where the module path in `go.mod` and the import statements in source files are consistent with each other. Go does not attempt to fetch `github.com/banzami/banzami` during local compilation.

### Why It Is Still a Defect

1. Any developer who attempts `go get github.com/banzami/banzami/services/api-gateway` will get a 404 (the org has moved)
2. The module path is an ADR-025 identity violation — it names the old GitHub org
3. Cross-service imports (if any service ever imports another service's package) would require the correct canonical path
4. Future tooling that performs module path validation would flag this

### Required Fix

All three `go.mod` files: change `github.com/banzami/banzami/services/X` → `github.com/banza-protocol/banzami/services/X`.

All 58 Go source files that contain `"github.com/banzami/banzami/services/...` import strings: update to match.

This is a mechanical find-and-replace with no semantic change — the code behavior is unchanged.

---

## Scope of Investigation — Confirmed Clean

The following were audited and found correct:

| Item | Result |
|------|--------|
| Conformance vector JSON syntax | Valid — all files parse |
| Vector ID uniqueness | Unique — no duplicates |
| Suite → vector reference integrity | All referenced IDs defined |
| Report schema structure | Correct `$schema`, `title`, `type`, `required`, `properties` |
| Manifest schema required fields | All present (`operator_id`, `environment`, `simulated`, `production_allowed`, `capabilities`) |
| QR payload prefixes | Vectors use `BANZAMI-SBX:` and `BANZAMI:` — workflow checks match |
| `tools/banzami-conformance/run.py` | No stale GitHub URLs or identity violations (the `.well-known/banzami/` paths are intentional protocol paths) |
| `tools/check-openapi-compatibility.sh` | No stale references |
| `banza/conformance/manifests/schema.json` | Capabilities schema has all required fields |
| banzami Rust CI | Runs correctly — migrations, clippy, tests |
| banzami TypeScript SDK CI | `npm ci` + `typecheck` + `test` all correct |
| banzami Go CI | `go vet` + `go test` pass (module paths internally consistent) |
| banzai `npm ci` | Runs correctly — `package-lock.json` present and valid |
| banzai `build` step | Actually runs across workspaces — correct |
| banzai `test` step | Runs for `apps/api` — correct |
| Cross-repo reusable workflows | None present — no cross-repo workflow dependencies |
| Secrets | Deploy secrets are environment-gated — expected to be absent on forks |

---

*Produced by: CONFORMANCE-CROSS-REPO-REPAIR-001 — 2026-05-30*
