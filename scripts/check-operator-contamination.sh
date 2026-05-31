#!/usr/bin/env bash
# check-operator-contamination.sh
#
# Regression guard: ensures no specific commercial operator brand has been
# introduced into the BANZA protocol repository.
#
# BANZA is an open protocol. It must remain independent of any operator.
# Operator-specific content belongs in operator repositories, not here.
#
# Usage:
#   scripts/check-operator-contamination.sh           # check everything
#   scripts/check-operator-contamination.sh --staged  # check only staged files

set -euo pipefail

REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# Build the forbidden pattern at runtime by joining parts so this script does
# not contain the banned strings as literals (which would trigger itself).
_P="banza"; _S="mi"
FORBIDDEN_PATTERN="${_P}${_S}|${_P}${_S}a"
FORBIDDEN_GLOB_1="*${_P}${_S}*"
FORBIDDEN_GLOB_2="*${_P}${_S}a*"
unset _P _S

# Guard artefacts are excluded — they necessarily reference the pattern
# in documentation or code form.
SELF_EXCLUDE=(
  "-g" "!scripts/check-operator-contamination.sh"
  "-g" "!.github/workflows/identity-guard.yml"
  "-g" "!docs/audit/identity/*REGRESSION_GUARD*"
)

# ── Mode ──────────────────────────────────────────────────────────────────────

STAGED_ONLY=false
[[ "${1:-}" == "--staged" ]] && STAGED_ONLY=true

FAIL=0

echo "──────────────────────────────────────────────────────────────────────"
echo "BANZA Operator Contamination Guard"
echo "──────────────────────────────────────────────────────────────────────"
echo ""

# ── 1. File content check ─────────────────────────────────────────────────────

echo "▶ Checking file contents..."

if [[ "$STAGED_ONLY" == "true" ]]; then
  STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)
  if [[ -n "$STAGED_FILES" ]]; then
    CONTENT_HITS=$(echo "$STAGED_FILES" | xargs grep -rnI -E -i "$FORBIDDEN_PATTERN" 2>/dev/null || true)
  else
    CONTENT_HITS=""
  fi
else
  CONTENT_HITS=$(rg -n -i "$FORBIDDEN_PATTERN" . \
    -g '!node_modules/**' \
    -g '!target/**' \
    -g '!dist/**' \
    -g '!build/**' \
    -g '!.next/**' \
    -g '!coverage/**' \
    -g '!.git/**' \
    "${SELF_EXCLUDE[@]}" \
    2>/dev/null || true)
fi

if [[ -n "$CONTENT_HITS" ]]; then
  echo "FAIL: Forbidden operator brand found in file contents:"
  echo ""
  echo "$CONTENT_HITS"
  echo ""
  FAIL=1
else
  echo "  PASS: no forbidden operator brand in file contents"
fi

echo ""

# ── 2. Filename / directory name check ───────────────────────────────────────

echo "▶ Checking filenames and directory names..."

FILENAME_HITS=$(find . \
  -path "./.git" -prune -o \
  -path "./node_modules" -prune -o \
  -path "./target" -prune -o \
  -path "./dist" -prune -o \
  -path "./build" -prune -o \
  -path "./.next" -prune -o \
  -path "./coverage" -prune -o \
  \( -iname "$FORBIDDEN_GLOB_1" -o -iname "$FORBIDDEN_GLOB_2" \) \
  -print 2>/dev/null || true)

if [[ -n "$FILENAME_HITS" ]]; then
  echo "FAIL: Forbidden operator brand found in filenames/directories:"
  echo ""
  echo "$FILENAME_HITS"
  echo ""
  FAIL=1
else
  echo "  PASS: no forbidden operator brand in filenames or directory names"
fi

echo ""

# ── Result ────────────────────────────────────────────────────────────────────

echo "──────────────────────────────────────────────────────────────────────"
if [[ "$FAIL" -eq 0 ]]; then
  echo "PASS: no operator-specific contamination found"
  echo ""
  echo "BANZA remains protocol-pure."
  exit 0
else
  echo "FAIL: operator-specific contamination detected — see above"
  echo ""
  echo "Fix: replace operator-brand names with protocol-neutral terms:"
  echo "  'certified operator', 'reference operator', 'operator implementation'"
  exit 1
fi
