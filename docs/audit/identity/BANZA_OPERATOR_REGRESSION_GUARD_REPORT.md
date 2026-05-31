# BANZA Operator Contamination Regression Guard

**Directive:** BANZA-BANZAI-OPERATOR-REGRESSION-GUARD-001  
**Date:** 2026-05-31  
**Status:** ACTIVE — enforced on every push and pull request

---

## Purpose

Prevent specific commercial operator brand names from re-entering the BANZA protocol repository after the identity purge (BANZA-ZERO-OPERATOR-PURGE-001).

BANZA is an open protocol. Any operator may build on it. No operator's name or brand belongs in protocol specifications, kernel code, SDKs, contracts, or documentation.

---

## Denylist

The following terms are forbidden anywhere in the repository:

| Term | Variants covered |
|------|-----------------|
| `banzami` | case-insensitive: `banzami`, `BANZAMI`, `Banzami` |
| `banzamia` | case-insensitive: `banzamia`, `BANZAMIA`, `BanzamIA` |

---

## Scope

The guard checks:
- All file contents (source code, docs, configs, prompts, eval datasets, CI workflows)
- All filenames
- All directory names

Exclusions (build artifacts and dependency caches):
- `.git/`
- `node_modules/`
- `target/`
- `dist/`
- `build/`
- `.next/`
- `coverage/`

---

## Files added

| File | Purpose |
|------|---------|
| `scripts/check-operator-contamination.sh` | Local check script — exits 1 on violation |
| `Makefile` | `make identity-check` target |
| `.github/workflows/identity-guard.yml` | CI job — runs on every push and pull request |

---

## Usage

### Local check (run before committing)
```bash
make identity-check
```

### Staged-only check (for pre-commit hook)
```bash
scripts/check-operator-contamination.sh --staged
```

### Optional pre-commit hook setup
```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/usr/bin/env bash
scripts/check-operator-contamination.sh --staged
EOF
chmod +x .git/hooks/pre-commit
```

### CI
The `identity-guard` workflow runs automatically on every push and pull request. It runs independently of (and in parallel with) the `Conformance` workflow.

---

## Replacement vocabulary

When writing about protocol features, use protocol-neutral terms:

| Instead of *(operator brand)* | Use |
|-------------------------------|-----|
| *(operator brand)* | certified operator |
| *(operator brand)* | reference operator |
| *(operator brand)* | operator implementation |
| *(operator brand)* | federation member |
| *(operator brand)* app | BANZA-compatible app |
| *(operator brand)* dashboard | operator dashboard |

---

## Validation results

| Check | Command | Result |
|-------|---------|--------|
| Identity check | `make identity-check` | ✓ PASS |
| cargo check | `cd core && cargo check --workspace` | ✓ PASS — 19 crates |
| Python tests | `cd sdk/python && python3 -m pytest tests/unit/ -q` | ✓ PASS — 66/66 |

---

## Related

- `BANZA_GOVERNANCE.md` — Operator Neutrality enforcement section
- `CLAUDE.md` — Operator Neutrality Rule section
- `docs/audit/identity/BANZA_IDENTITY_PURGE_REPORT.md` — The purge that this guard protects
