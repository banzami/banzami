# CI Red Jobs — Failure Logs and Root Cause Analysis

**Mission:** CI-RED-JOBS-ROOT-CAUSE-REPAIR-002  
**Date:** 2026-05-30  
**Runs inspected:**
- banza run `26691197011` (Conformance, 2026-05-30T18:10:17Z)
- banzai run `26691197319` (CI, 2026-05-30T18:10:17Z)
- banzami run `26691200009` (CI, 2026-05-30T18:10:25Z)

---

## Failure 1 — banza: Reference operator conformance (Level 2)

### Failing Step

`Run conformance suite (Level 2)`

### Command Executed

```
python3 tools/banzami-conformance/run.py \
  --url http://localhost:3000 \
  --level 2 \
  --output conformance-report.json \
  --quiet
```

### Exact Error Output (from log)

```
ERROR: Cannot reach operator at http://localhost:3000: HTTP GET http://localhost:3000/health failed: <urlopen error [Errno 111] Connection refused>
Banzami Conformance Runner 1.0.0
Operator: http://localhost:3000
Level:    2

Process completed with exit code 2.
```

### Root Cause

The sandbox-operator binary binds to **port 3100** by default:

```rust
// reference/sandbox-operator/src/main.rs:50–53
let port = std::env::var("PORT")
    .ok()
    .and_then(|p| p.parse::<u16>().ok())
    .unwrap_or(3100);   // ← DEFAULT IS 3100
```

The conformance workflow starts the binary (OPERATOR_PID is set, the process runs) but then checks health and sends the runner to `http://localhost:3000` — which is never bound. Connection refused.

The workflow health-check loop does not fail when the operator doesn't answer (it silently exits the `for` loop), so the conformance runner runs against a closed port.

### Cause category

CI workflow references wrong port — not caused by ADR-025 rename, not a missing dependency. Pure configuration mismatch between operator's default port and workflow URL.

### Required Fix

Change both occurrences of `localhost:3000` in `banza/.github/workflows/conformance.yml` to `localhost:3100`:
- Line 245 (health check curl)
- Line 255 (`--url` argument to conformance runner)

---

## Failure 2 — banzai: TypeScript — build, typecheck, test

### Failing Step

`Type check`

### Command Executed

```
npm run typecheck --workspaces --if-present
```

### Exact Error Output — apps/cli (first failure)

```
> @banza-protocol/banzai-cli@0.1.0 typecheck
> tsc --noEmit

src/commands/certify.ts(20,9): error TS1343: The 'import.meta' meta-property is only allowed when
  the '--module' option is 'es2020', 'es2022', 'esnext', 'system', 'node16', 'node18', 'node20',
  or 'nodenext'.
src/commands/conformance.ts(24,22): error TS1343: The 'import.meta' meta-property is only allowed
  when the '--module' option is 'es2020', 'es2022', 'esnext', 'system', 'node16', 'node18',
  'node20', or 'nodenext'.

npm error code 2
npm error workspace @banza-protocol/banzai-cli@0.1.0
```

### Exact Error Output — apps/web (second failure)

```
> @banza-protocol/banzai-web@0.1.0 typecheck
> tsc --noEmit

components/chat/ChatInterface.tsx(92,29): error TS2345:
  Argument of type '(prev: Message[]) => (Message | { content: string; model: ModelId | undefined;
  ...})[]' is not assignable to parameter of type 'SetStateAction<Message[]>'.
  ...
  Types of property 'model' are incompatible.
    Type 'ModelId | undefined' is not assignable to type 'ModelId'.

components/chat/ChatInterface.tsx(99,29): error TS2345:
  ...
  Types of property 'citations' are incompatible.
    Type 'Citation[] | undefined' is not assignable to type 'Citation[]'.

components/chat/MessageBubble.tsx(37,12): error TS2375:
  Type '{ model: ModelId; taskType: TaskType | undefined; }' is not assignable to type 'Props'
  with 'exactOptionalPropertyTypes: true'.
  Types of property 'taskType' are incompatible.
    Type 'TaskType | undefined' is not assignable to type 'TaskType'.
```

### Root Cause — apps/cli

`apps/cli/tsconfig.json` overrides the base config with `"module": "CommonJS"`. The code in `certify.ts:20` and `conformance.ts:24` uses `import.meta` which requires ESM-compatible module output. CommonJS does not support `import.meta`.

```json
// apps/cli/tsconfig.json — WRONG
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "module": "CommonJS",         // ← does not support import.meta
    "moduleResolution": "node",   // ← paired with CommonJS
    ...
  }
}
```

The base `tsconfig.base.json` has `"module": "NodeNext"` which does support `import.meta`. The CLI tsconfig explicitly downgrades this.

### Root Cause — apps/web

`tsconfig.base.json` enables `"exactOptionalPropertyTypes": true`. This causes three errors:

**Error 1 & 2 — ChatInterface.tsx lines 92/99:**

With `exactOptionalPropertyTypes: true`, an object literal `{ model: value }` where `value: ModelId | undefined` does not satisfy `model?: ModelId` (which means "if model is present, it is ModelId — undefined is only allowed by omitting the key entirely").

Line 92: `{ ...m, content: accumulated, model: (parsed.model as Message['model']) ?? m.model }` — the RHS type is `ModelId | undefined`.

Line 99: `{ ...m, citations: parsed.citations }` — TypeScript does not narrow `parsed.citations` to `Citation[]` across the closure boundary into `setMessages(prev => ...)` even though we are inside `if (parsed.citations)`.

**Error 3 — MessageBubble.tsx line 37:**

`<ModelIndicator model={message.model} taskType={message.taskType} />` — `message.taskType` has type `TaskType | undefined`, but `ModelIndicator.Props.taskType` is `taskType?: TaskType`. With `exactOptionalPropertyTypes`, passing `undefined` explicitly to an optional prop is a type error; it must be omitted entirely.

### Cause category

Not caused by ADR-025 rename. These are pre-existing latent type errors surfaced because `typecheck` now actually runs (it was silently skipped before the script name fix in CONFORMANCE-CROSS-REPO-REPAIR-001).

---

## Failure 3 — banzami: Rust — build, lint, test

### Failing Step

`Check formatting`

### Command Executed

```
cargo fmt --all -- --check
```

### Exact Error Output (from log)

```
`cargo metadata` exited with an error: error: failed to load manifest for workspace member
  `/home/runner/work/banzami/banzami/core/ledger`
referenced by workspace at `/home/runner/work/banzami/banzami/core/Cargo.toml`

Caused by:
  failed to load manifest for dependency `banzami-types`

Caused by:
  failed to read `/home/runner/work/banzami/Banzami/core/crates/banzami-types/Cargo.toml`

Caused by:
  No such file or directory (os error 2)

Process completed with exit code 1.
```

### Root Cause

`banzami/core/Cargo.toml` line 40:

```toml
banzami-types = { path = "../../Banzami/core/crates/banzami-types" }
```

This path is resolved by Cargo relative to the workspace root (`banzami/core/`):

```
/home/runner/work/banzami/banzami/core/../../Banzami/core/crates/banzami-types
= /home/runner/work/banzami/Banzami/core/crates/banzami-types
```

On Linux (GitHub Actions runner), the filesystem is **case-sensitive**. The repository was cloned to `/home/runner/work/banzami/banzami/` (lowercase). There is no `/home/runner/work/banzami/Banzami/` (capital B) directory.

On macOS (developer machine), the filesystem is **case-insensitive** by default: `~/Banzami/` resolves to `~/banzami/`, so the path worked locally.

The `banzami-types` crate already exists within the same repo at `banzami/core/crates/banzami-types/`. The path dependency simply needs to reference it correctly.

```
Correct path from banzami/core/: crates/banzami-types
Wrong path (capital B, case works on macOS only): ../../Banzami/core/crates/banzami-types
```

### Cause category

Case-sensitivity bug — works on macOS (case-insensitive), fails on Linux CI (case-sensitive). Not caused by ADR-025 rename directly, but the path `Banzami` reflects the old capitalized repo name. The crate already exists at the correct location within the repo.

---

## Summary Table

| Failure | Repo | File | Log Line | Root Cause | Category |
|---------|------|------|----------|-----------|---------|
| Port mismatch | banza | `conformance.yml:245,255` | `Connection refused` on port 3000 | Operator defaults to 3100 | Config mismatch |
| CLI module setting | banzai | `apps/cli/tsconfig.json:6` | `TS1343: import.meta not allowed` | `"module": "CommonJS"` blocks import.meta | Latent type error |
| Web exactOptional | banzai | `ChatInterface.tsx:92,99` + `MessageBubble.tsx:37` | `TS2345`, `TS2375` with exactOptionalPropertyTypes | Optional props assigned with `| undefined` | Latent type error |
| Cargo path case | banzami | `core/Cargo.toml:40` | `No such file: /Banzami/core/crates/banzami-types` | `../../Banzami/` capital-B path fails on Linux | Case-sensitivity bug |

---

*Produced by: CI-RED-JOBS-ROOT-CAUSE-REPAIR-002 — 2026-05-30*
