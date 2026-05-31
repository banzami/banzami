# BANZA Operator Neutrality Report

**Directive:** OPERATOR-NEUTRALITY-GUARD-002  
**Date:** 2026-05-31  
**Status:** COMPLETE

---

## Principle Implemented

**Operator neutrality is an architectural invariant of BANZA.**

The dependency graph is immutable:

```
Operators  →  BanzAI  →  BANZA
```

BANZA defines protocol rules. Operators implement them. BANZA never depends on, references, or privileges any specific operator.

---

## Files Modified

### Governance documentation

| File | Change |
|------|--------|
| `CLAUDE.md` | Expanded "Operator Neutrality Rule" into full "Operator Neutrality Principle" with dependency graph, what BANZA must never contain, what BANZA defines, terminology table |
| `BANZA_GOVERNANCE.md` | Added full "Operator Neutrality Principle" section with dependency graph, architectural definition, violations table, enforcement mechanism |
| `README.md` | Added "Operator Neutrality Principle" section with dependency graph before Governance section; rewrote "What is the reference operator?" → "What is a certified operator?"; neutralised ecosystem header; updated architecture diagram |

### New files

| File | Purpose |
|------|---------|
| `docs/governance/OPERATOR_NEUTRALITY_TERMINOLOGY.md` | Terminology guide: approved terms, forbidden terms, example rewrites, federation vocabulary, governance claim examples |

### Guard upgrade

| File | Change |
|------|--------|
| `scripts/check-operator-contamination.sh` | Upgraded to two-level guard: Level 1 (explicit denylist) + Level 2 (governance claim detection). Added terminology guide to exclusions. |
| `.github/workflows/identity-guard.yml` | Added terminology guide to exclusions. |

---

## Examples Rewritten

| Before | After |
|--------|-------|
| `> the reference operator = reference operator...` | `> Certified operators = independent commercial entities...` |
| `## What is the reference operator?` | `## What is a certified operator?` |
| Product-specific description (consumer app, merchant dashboard, EMIS) | Protocol-neutral description (any operator builds these) |
| Architecture diagram with specific operator label | Diagram with "Certified Operator (any operator)" |
| `- the reference operator — reference operator implementation` | `- Certified operators — independent implementations of BANZA` |

---

## Guard Upgrade — Level 2

The guard now runs two levels:

**Level 1 (blocking):** Exact denylist — no known operator brand names. Fails CI.

**Level 2 (advisory):** Governance claim patterns — flags content that implies an operator has protocol authority. Requires human review. Patterns checked:
- `governs BANZA` / `governs the protocol`
- `defines BANZA` / `defines the protocol`
- `owns BANZA` / `owns the protocol`
- `controls BANZA` / `controls the protocol`
- `operator.*certif.*BANZA`
- `BANZA.*owned by`
- `protocol.*governed by.*operator`

Level 2 is advisory — it warns but does not automatically fail. This is intentional: these patterns can appear in valid governance documentation (e.g., "No operator governs BANZA").

---

## Validation Results

| Check | Result |
|-------|--------|
| `make identity-check` (Level 1) | ✓ PASS |
| `make identity-check` (Level 2) | ✓ PASS — no governance claim patterns |
| `cargo check --workspace` | ✓ PASS — 19 crates |
| `python -m pytest tests/unit/` | ✓ PASS — 66/66 |

---

## Remaining Risks

| Risk | Mitigation |
|------|------------|
| New operator brand introduced via PR | Level 1 guard blocks it in CI |
| Governance claim introduced via PR | Level 2 warns; human review required |
| Operator-specific logic in a crate | Not detectable by string search; requires code review |
| Future operator with a name similar to protocol terms | Level 1 denylist must be updated if a new operator name is to be blocked |

The highest remaining risk is operator-specific *logic* (not names) being introduced in Rust crates. This requires code review, not automated string matching.
