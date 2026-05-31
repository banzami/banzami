#!/usr/bin/env bash
# check-operator-contamination.sh
#
# Operator Neutrality Guard for the BANZA protocol repository.
#
# BANZA is an operator-neutral open protocol. This guard enforces two levels:
#
#   LEVEL 1 — Explicit denylist
#     Blocks known historical operator brand names (exact string match).
#
#   LEVEL 2 — Governance claim detection
#     Flags patterns that imply a specific operator has protocol authority,
#     governance control, or certification ownership.
#
# Usage:
#   scripts/check-operator-contamination.sh           # full check
#   scripts/check-operator-contamination.sh --staged  # staged files only (pre-commit)

set -euo pipefail

REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# ── Level 1: Forbidden operator brand (built at runtime — avoids self-match) ──

_P="banza"; _S="mi"
L1_PATTERN="${_P}${_S}|${_P}${_S}a"
L1_GLOB_1="*${_P}${_S}*"
L1_GLOB_2="*${_P}${_S}a*"
unset _P _S

# ── Level 2: Operator governance/authority claims ─────────────────────────────
# Patterns that suggest a specific operator governs, owns, or defines BANZA.
# These are heuristic — review flagged lines manually.

L2_PATTERNS=(
  "governs BANZA"
  "governs the protocol"
  "defines BANZA"
  "defines the protocol"
  "owns BANZA"
  "owns the protocol"
  "controls BANZA"
  "controls the protocol"
  "operator.*certif.*BANZA"
  "BANZA.*owned by"
  "protocol.*governed by.*operator"
)

# ── Guard artefacts excluded from Level 1 (they document the pattern) ─────────

SELF_EXCLUDE=(
  "-g" "!scripts/check-operator-contamination.sh"
  "-g" "!.github/workflows/identity-guard.yml"
  "-g" "!docs/audit/identity/**"
  "-g" "!docs/governance/OPERATOR_NEUTRALITY_TERMINOLOGY.md"
)

# ── Mode ──────────────────────────────────────────────────────────────────────

STAGED_ONLY=false
[[ "${1:-}" == "--staged" ]] && STAGED_ONLY=true

FAIL=0

echo "══════════════════════════════════════════════════════════════════════"
echo "BANZA Operator Neutrality Guard"
echo "══════════════════════════════════════════════════════════════════════"
echo ""

# ── LEVEL 1: Denylist check ───────────────────────────────────────────────────

echo "▶ Level 1 — Explicit denylist (file contents)..."

if [[ "$STAGED_ONLY" == "true" ]]; then
  STAGED=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)
  if [[ -n "$STAGED" ]]; then
    L1_CONTENT=$(echo "$STAGED" | xargs grep -rnI -E -i "$L1_PATTERN" 2>/dev/null || true)
  else
    L1_CONTENT=""
  fi
else
  L1_CONTENT=$(rg -n -i "$L1_PATTERN" . \
    -g '!node_modules/**' -g '!target/**' -g '!dist/**' \
    -g '!build/**' -g '!.next/**' -g '!coverage/**' -g '!.git/**' \
    "${SELF_EXCLUDE[@]}" \
    2>/dev/null || true)
fi

if [[ -n "$L1_CONTENT" ]]; then
  echo "  FAIL: Forbidden operator brand in file contents:"
  echo ""
  echo "$L1_CONTENT"
  echo ""
  FAIL=1
else
  echo "  PASS"
fi

echo ""
echo "▶ Level 1 — Explicit denylist (filenames)..."

L1_NAMES=$(find . \
  -path "./.git" -prune -o -path "./node_modules" -prune -o \
  -path "./target" -prune -o -path "./dist" -prune -o \
  -path "./build" -prune -o -path "./.next" -prune -o \
  -path "./coverage" -prune -o \
  \( -iname "$L1_GLOB_1" -o -iname "$L1_GLOB_2" \) -print 2>/dev/null || true)

if [[ -n "$L1_NAMES" ]]; then
  echo "  FAIL: Forbidden operator brand in filenames:"
  echo ""
  echo "$L1_NAMES"
  echo ""
  FAIL=1
else
  echo "  PASS"
fi

echo ""

# ── LEVEL 2: Governance claim detection ──────────────────────────────────────

echo "▶ Level 2 — Governance claim detection..."

L2_HITS=""
for pattern in "${L2_PATTERNS[@]}"; do
  hits=$(rg -n -i "$pattern" . \
    -g '!node_modules/**' -g '!target/**' -g '!dist/**' \
    -g '!build/**' -g '!.next/**' -g '!coverage/**' -g '!.git/**' \
    -g '!docs/audit/identity/**' \
    -g '!docs/governance/OPERATOR_NEUTRALITY_TERMINOLOGY.md' \
    2>/dev/null || true)
  if [[ -n "$hits" ]]; then
    L2_HITS="${L2_HITS}${hits}"$'\n'
  fi
done

if [[ -n "$L2_HITS" ]]; then
  echo "  WARNING: Potential operator governance claim detected."
  echo "  Review these lines — if a specific operator is being given protocol"
  echo "  authority, this is a violation. Generic uses are acceptable."
  echo ""
  echo "$L2_HITS"
  echo ""
  # Level 2 warns but does not fail — requires human review
  echo "  (Level 2 is advisory — no automatic failure)"
else
  echo "  PASS: no governance claim patterns found"
fi

echo ""

# ── Result ────────────────────────────────────────────────────────────────────

echo "══════════════════════════════════════════════════════════════════════"
if [[ "$FAIL" -eq 0 ]]; then
  echo "PASS: BANZA operator neutrality verified"
  echo ""
  echo "BANZA remains protocol-pure and operator-neutral."
  exit 0
else
  echo "FAIL: operator-specific contamination detected (see Level 1 above)"
  echo ""
  echo "Fix: replace operator-brand names with protocol-neutral terms."
  echo "See: docs/governance/OPERATOR_NEUTRALITY_TERMINOLOGY.md"
  exit 1
fi
