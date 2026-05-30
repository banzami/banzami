# Conformance Dependency Graph

**Mission:** CONFORMANCE-CROSS-REPO-REPAIR-001  
**Date:** 2026-05-30  
**Status:** Official

---

## Cross-Repository Dependency Map

This graph maps every dependency edge between the three repositories as it pertains to conformance, CI, and build systems.

```
banza (protocol)
│
│  Provides TO banzami:
│  ├── core/crates/banzami-* (Rust path deps — referenced by reference/Cargo.toml)
│  │     banzami-types, banzami-ledger, banzami-wallets, banzami-transactions
│  │     banzami-acquiring, banzami-routing, banzami-settlement
│  │     banzami-notifications, banzami-identity, banzami-qr
│  │     banzami-payment-links, banzami-risk, banzami-transfers
│  │     banzami-capabilities
│  ├── conformance/vectors/*.json (test vectors)
│  ├── conformance/*/suite.json (suite definitions)
│  ├── tools/banzami-conformance/run.py (conformance runner)
│  └── reference/sandbox-operator (reference operator binary)
│
│  Provides TO banzai:
│  └── (none — banzai consumes banza docs at runtime, not at build time)
│
│  Consumes FROM banzami:
│  └── (none — banza is upstream)
│
│  Consumes FROM banzai:
│  └── (none — banza is upstream)

banzai (Protocol OS)
│
│  Provides TO banza:
│  └── (none — banzai is a consumer, not a provider)
│
│  Provides TO banzami:
│  └── BanzAI API (runtime, not build-time — no CI dependency)
│
│  Consumes FROM banza (runtime, not CI):
│  ├── BANZA_REFERENCE.md (loaded into RAG/knowledge base at runtime)
│  ├── conformance/vectors/*.json (indexed at runtime for protocol knowledge)
│  └── docs/adr/*.md (indexed at runtime)
│
│  Consumes FROM banzami (runtime, not CI):
│  └── BANZAMI_REFERENCE.md (loaded into RAG/knowledge base at runtime)

banzami (reference operator)
│
│  Provides TO banza:
│  └── (none — banzami is a consumer; it is the subject of banza's conformance suite)
│
│  Provides TO banzai:
│  └── (none)
│
│  Consumes FROM banza (build-time, path deps):
│  ├── ../../banza/core/crates/banzami-* (all 13 kernel crates)
│  └── (via reference/Cargo.toml workspace.dependencies)
│
│  Note: The CI in banzami does NOT check out banza or banzai.
│        The kernel crate path deps assume the repos are sibling directories
│        (~/banza and ~/banzami side by side) — which is true locally but
│        FALSE in GitHub Actions.
```

---

## CI Dependency Matrix

| Workflow | Repo | Depends on other repo at CI time? | How |
|----------|------|------------------------------------|-----|
| `conformance.yml` | banza | No | Self-contained |
| `ci.yml` | banzai | No | Self-contained |
| `ci.yml` | banzami | **Yes — banza kernel crates** | Path deps in `reference/Cargo.toml` |

---

## The Kernel Crate Path Dependency Problem

This is the most significant structural dependency and a potential source of future CI failures.

`banza/reference/Cargo.toml` declares:

```toml
[workspace.dependencies]
banzami-types     = { path = "../core/crates/banzami-types" }
banzami-ledger    = { path = "../core/crates/banzami-ledger" }
...
```

The path `../core/crates/banzami-types` resolves relative to the `reference/` directory — meaning it assumes `../../banza/core/crates/banzami-types` exists as a sibling repo directory. On a developer's machine where `~/banza` and `~/banzami` are side by side, this works. In GitHub Actions, the `banza` workflow only checks out the `banza` repo — so `../core/crates/banzami-types` resolves to `banza/core/crates/banzami-types` which IS the same repo.

Wait — the `reference/Cargo.toml` is in the `banza` repo, and the path `../core/crates/banzami-types` resolves relative to `banza/reference/`, which is `banza/core/crates/banzami-types`. This IS within the banza repo.

**This path dependency is correct and self-contained within banza.** The `reference/` workspace uses `banza/core/crates/`, not `banzami/core/crates/`. The banza repo contains its own kernel crates as the protocol reference.

Separately, `banzami/core/` (the Banzami operator's Rust core) is a separate codebase that uses banzami-specific crate implementations. The `banzami` CI compiles from `banzami/core/` with no dependency on `banza/core/`.

**Conclusion**: There are no cross-repo build dependencies in CI. Each repo is fully self-contained for CI purposes.

---

## Dependency Edge Status

| Edge | Type | Status | Broken? |
|------|------|--------|---------|
| `banza/reference/` → `banza/core/crates/banzami-*` | Path dep (build) | Within same repo | ✓ Valid |
| `banzai` → `banza/BANZA_REFERENCE.md` | Runtime RAG load | Not in CI | N/A |
| `banzai` → `banzami/BANZAMI_REFERENCE.md` | Runtime RAG load | Not in CI | N/A |
| `banzami/core/` | Self-contained Rust workspace | No cross-repo deps in CI | ✓ Valid |
| `banzami/services/api-gateway/go.mod` declares `github.com/banzami/banzami` | Module namespace | Stale (old org) | ⚠ Structural |
| `banzami/services/admin-api/go.mod` declares `github.com/banzami/banzami` | Module namespace | Stale (old org) | ⚠ Structural |
| `banzami/services/public-api/go.mod` declares `github.com/banzami/banzami` | Module namespace | Stale (old org) | ⚠ Structural |
| `banzai` root `package.json` name `@banzami/banzamia` | npm package name | Stale (private) | ⚠ Structural |
| `banzai` lockfile name `@banzami/banzamia` | Derived from package.json | Stale (harmless) | ⚠ Structural |

---

## Workflow-Level Dependency Graph

```
banza/conformance.yml
├── validate-vectors          (no deps)
├── openapi-compat            (no deps)
├── schema-compat             (no deps)
├── qr-compat                 (no deps)
├── trace-contract            (no deps)
├── manifest-validation       (no deps)
└── reference-conformance
    ├── needs: validate-vectors    ✓
    ├── needs: schema-compat       ✓
    ├── needs: trace-contract      ✓
    ├── Build: reference/sandbox-operator (Rust binary)  ← BROKEN PATH
    ├── Start: binary at wrong path                       ← FAILS HERE
    └── Run: tools/banzami-conformance/run.py

banzai/ci.yml
└── build
    ├── npm ci                 ✓ (package-lock.json present)
    ├── type-check             ⚠ SILENT NOOP (wrong script name)
    ├── lint                   ⚠ SILENT NOOP (no lint scripts in workspaces)
    ├── build                  ✓ (all workspaces have build script)
    └── test                   ~ (only apps/api has test script)

banzami/ci.yml
├── rust                       ✓ (self-contained, no cross-repo deps)
├── go-gateway                 ✓ (module path stale but internally consistent)
├── go-admin                   ✓ (module path stale but internally consistent)
├── go-public                  ✓ (module path stale but internally consistent)
├── typescript                 ✓ (sdk/typescript, self-contained)
└── deploy                     ~ (requires secrets, only runs on push to main)
```

Legend: `✓` = working | `⚠` = broken/wrong but not causing red CI | `~` = conditional/partial | `←` = root cause

---

## The Breaking Edge

Only one dependency edge is broken in a way that causes CI failures:

```
banza/conformance.yml
  └─ reference-conformance
       └─ "Start sandbox operator"
            └─ ./reference/sandbox-operator/target/release/sandbox-operator
                                   ↑
                           WRONG DIRECTORY
                           Binary is actually at:
                           ./reference/target/release/sandbox-operator
```

This is the single root cause of the failing `Conformance / Reference operator conformance (Level 2)` job.

---

*Produced by: CONFORMANCE-CROSS-REPO-REPAIR-001 — 2026-05-30*
