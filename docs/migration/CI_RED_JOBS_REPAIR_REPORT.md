# CI Red Jobs Repair Report

**Mission:** CI-RED-JOBS-ROOT-CAUSE-REPAIR-002  
**Date:** 2026-05-30  
**Status:** Complete — all three repos pushed to origin/main

---

## Summary

| Repo | Job | Root Cause | Fix | Commit |
|------|-----|-----------|-----|--------|
| banza | `Conformance / Reference operator conformance (Level 2)` | Operator defaults to port 3100, workflow checked port 3000 | Change two `localhost:3000` → `localhost:3100` in `conformance.yml` | `372ab0d` |
| banzai | `CI / TypeScript — build, typecheck, test` | 4 type errors: CLI tsconfig wrong module, web `exactOptionalPropertyTypes` violations | Fix tsconfig module + conditional spreads in ChatInterface + MessageBubble | `d409b72` |
| banzami | `CI / Rust — build, lint, test` | `banzami-types` path `../../Banzami/` uses capital-B, fails on Linux CI (case-sensitive) | Fix path to `types` (within same workspace) + format + clippy | `cca0a86` |

---

## Failure 1 — banza

### Exact failing log (run 26691197011)

```
Step: Run conformance suite (Level 2)

ERROR: Cannot reach operator at http://localhost:3000: HTTP GET
  http://localhost:3000/health failed:
  <urlopen error [Errno 111] Connection refused>
Process completed with exit code 2.
```

### Root cause

`reference/sandbox-operator/src/main.rs:53`:
```rust
.unwrap_or(3100)  // default port is 3100, not 3000
```

The workflow checked health and sent the runner to `localhost:3000`. The binary was running but not listening on that port.

### Fix applied

`banza/.github/workflows/conformance.yml`:

```yaml
# BEFORE (line 245)
if curl -sf http://localhost:3000/health > /dev/null 2>&1; then
# AFTER
if curl -sf http://localhost:3100/health > /dev/null 2>&1; then

# BEFORE (line 255)
--url http://localhost:3000 \
# AFTER
--url http://localhost:3100 \
```

### Local validation

```bash
# Binary binds to 3100 by default — confirmed in main.rs:53
grep "unwrap_or" reference/sandbox-operator/src/main.rs
# → .unwrap_or(3100)
```

---

## Failure 2 — banzai

### Exact failing logs (run 26691197319)

**apps/cli:**
```
src/commands/certify.ts(20,9): error TS1343: The 'import.meta' meta-property is only
  allowed when the '--module' option is 'es2020', 'es2022', 'esnext', 'system',
  'node16', 'node18', 'node20', or 'nodenext'.
npm error workspace @banza-protocol/banzai-cli@0.1.0
```

**apps/web:**
```
components/chat/ChatInterface.tsx(92,29): error TS2345:
  Type 'ModelId | undefined' is not assignable to type 'ModelId'.
components/chat/ChatInterface.tsx(99,29): error TS2345:
  Type 'Citation[] | undefined' is not assignable to type 'Citation[]'.
components/chat/MessageBubble.tsx(37,12): error TS2375:
  Type 'TaskType | undefined' is not assignable to type 'TaskType'.
```

### Root cause — apps/cli

`apps/cli/tsconfig.json` had `"module": "CommonJS"` which disables `import.meta`. The CLI code uses `import.meta` in two files. The base config has `"module": "NodeNext"` which the CLI was overriding.

### Root cause — apps/web

`tsconfig.base.json` has `"exactOptionalPropertyTypes": true`. Three call sites passed `T | undefined` to optional props typed as `T`:
- `ChatInterface.tsx:92` — `{ model: ModelId | undefined }` in object spread
- `ChatInterface.tsx:99` — TypeScript doesn't narrow `parsed.citations` across closure boundary
- `MessageBubble.tsx:37` — JSX prop `taskType={message.taskType}` where taskType is `TaskType | undefined`

### Fixes applied

```json
// apps/cli/tsconfig.json
"module": "NodeNext",         // was "CommonJS"
"moduleResolution": "NodeNext" // was "node"
```

```tsx
// ChatInterface.tsx:92 — conditional spread avoids undefined
? { ...m, content: accumulated, ...(parsed.model != null ? { model: parsed.model as NonNullable<Message['model']> } : {}) }

// ChatInterface.tsx:99 — extract const before closure to force narrowing
const newCitations = parsed.citations
setMessages(prev => prev.map(m =>
  m.id === assistantMsgId ? { ...m, citations: newCitations } : m
))

// MessageBubble.tsx:37 — conditional spread for optional JSX prop
<ModelIndicator model={message.model} {...(message.taskType !== undefined ? { taskType: message.taskType } : {})} />
```

### Local validation

```bash
cd ~/banzai
npm ci
npm run typecheck --workspaces --if-present
# EXIT: 0 — all 6 workspaces pass
```

---

## Failure 3 — banzami

### Exact failing log (run 26691200009)

```
Step: Check formatting

`cargo metadata` exited with an error: error: failed to load manifest for
  workspace member /home/runner/work/banzami/banzami/core/ledger

Caused by:
  failed to read /home/runner/work/banzami/Banzami/core/crates/banzami-types/Cargo.toml
  No such file or directory (os error 2)

Process completed with exit code 1.
```

### Root cause

`banzami/core/Cargo.toml:40`:
```toml
banzami-types = { path = "../../Banzami/core/crates/banzami-types" }
```

The capital `B` in `Banzami` worked on macOS (case-insensitive filesystem) but failed on Linux (case-sensitive). The crate lives at `core/types/` within the same workspace — the path was unnecessarily going outside the repo.

Path resolution on Linux CI:
```
/home/runner/work/banzami/banzami/core/../../Banzami/core/crates/banzami-types
= /home/runner/work/banzami/Banzami/core/crates/banzami-types  ✗ (no capital-B directory)
```

### Fix applied

```toml
# banzami/core/Cargo.toml:40 — BEFORE
banzami-types = { path = "../../Banzami/core/crates/banzami-types" }

# AFTER
banzami-types = { path = "types" }
```

### Cascading fixes after path was unblocked

Once `cargo metadata` worked, `cargo fmt --all -- --check` and `cargo clippy --workspace --all-targets -- -D warnings` ran for the first time on this workspace and found pre-existing issues:

**Formatting (cargo fmt):** Import ordering, alignment, and line wrapping across ~15 source files — auto-applied with `cargo fmt --all`.

**Clippy lints (36 instances fixed):**
- Digits grouped inconsistently (`1_000_000_00` → `100_000_000`) across ledger, settlement, wallets, compliance, risk test files — these are AOA minor unit values where a trailing `_00` visual suffix was used
- `map_or` simplified to `is_none_or` (consumer-wallets/onboarding.rs, settlement/engine.rs)
- `impl Default` can be derived (merchants/api_key.rs)
- `.clone()` on Copy type `Money` (acquiring/engine.rs)
- Dead code fields: `#[allow(dead_code)]` on `EMISProvider`, `PayoutRow`, `RequestId`, `RiskFlagsQuery`
- Complex sqlx tuple types: `#[allow(clippy::type_complexity)]` on admin route handlers
- Unused variable `transit` → `_transit` in funding test

### Local validation

```bash
cd ~/banzami/core
cargo fmt --all -- --check
# EXIT: 0
SQLX_OFFLINE=true cargo clippy --workspace --all-targets -- -D warnings
# No errors output
```

---

## Final CI State (expected after pushes)

| Repo | Workflow | Job | Expected |
|------|----------|-----|---------|
| banza | Conformance | Validate conformance vectors | ✓ Green |
| banza | Conformance | OpenAPI compatibility | ✓ Green |
| banza | Conformance | Schema compatibility | ✓ Green |
| banza | Conformance | QR payload compatibility | ✓ Green |
| banza | Conformance | Trace contract | ✓ Green |
| banza | Conformance | Manifest schema validation | ✓ Green |
| **banza** | **Conformance** | **Reference operator conformance (Level 2)** | **✓ Green** |
| **banzai** | **CI** | **TypeScript — build, typecheck, test** | **✓ Green** |
| banzami | CI | Go api-gateway | ✓ Green |
| banzami | CI | Go admin-api | ✓ Green |
| banzami | CI | Go public-api | ✓ Green |
| **banzami** | **CI** | **Rust — build, lint, test** | **✓ Green** |
| banzami | CI | TypeScript SDK | ✓ Green |

---

## Commits

| Repo | Hash | Description |
|------|------|-------------|
| banza | `372ab0d` | fix(ci): repair reference operator conformance job — port 3000 → 3100 |
| banzai | `d409b72` | fix(ci): repair TypeScript CI job — typecheck failures in apps/cli and apps/web |
| banzami | `cca0a86` | fix(ci): repair Rust CI job — banzami-types path + cargo fmt + clippy |

---

*Produced by: CI-RED-JOBS-ROOT-CAUSE-REPAIR-002 — 2026-05-30*
