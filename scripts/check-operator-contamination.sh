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
#   scripts/check-operator-contamination.sh --staged  # check only staged files (pre-commit hook)

set -euo pipefail

# ── Configuration ─────────────────────────────────────────────────────────────

REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# Forbidden operator brand strings (case-insensitive search, but we list all
# canonical forms so the denylist is readable)
FORBIDDEN_PATTERN="banzami|banzamia|BanzamIA|BANZAMI|BANZAMIA"

# Directories to exclude from both content and filename searches
EXCLUDE_DIRS=(
  ".git"
  "node_modules"
  "target"
  "dist"
  "build"
  ".next"
  "coverage"
)

# ── Build exclusion flags ─────────────────────────────────────────────────────

build_rg_excludes() {
  for d in "${EXCLUDE_DIRS[@]}"; do printf -- "-g '!%s/**' " "$d"; done
}

build_find_prune() {
  local prune_args=()
  for d in "${EXCLUDE_DIRS[@]}"; do
    prune_args+=(-path "./$d" -prune -o)
  done
  printf '%s ' "${prune_args[@]}"
}

# ── Mode ──────────────────────────────────────────────────────────────────────

STAGED_ONLY=false
if [[ "${1:-}" == "--staged" ]]; then
  STAGED_ONLY=true
fi

# ── Checks ────────────────────────────────────────────────────────────────────

FAIL=0

echo "──────────────────────────────────────────────────────────────────────"
echo "BANZA Operator Contamination Guard"
echo "Forbidden pattern: ${FORBIDDEN_PATTERN}"
echo "──────────────────────────────────────────────────────────────────────"
echo ""

# ── 1. File content check ─────────────────────────────────────────────────────

echo "▶ Checking file contents..."

if [[ "$STAGED_ONLY" == "true" ]]; then
  # Check only git-staged files
  STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)
  if [[ -n "$STAGED_FILES" ]]; then
    CONTENT_HITS=$(echo "$STAGED_FILES" | xargs grep -rnI -E -i "$FORBIDDEN_PATTERN" 2>/dev/null || true)
  else
    CONTENT_HITS=""
  fi
else
  # Check all tracked and untracked files, excluding configured dirs
  CONTENT_HITS=$(eval rg -n -i '"'"$FORBIDDEN_PATTERN"'"' . \
    -g '"'"'!node_modules/**'"'"' \
    -g '"'"'!target/**'"'"' \
    -g '"'"'!dist/**'"'"' \
    -g '"'"'!build/**'"'"' \
    -g '"'"'!.next/**'"'"' \
    -g '"'"'!coverage/**'"'"' \
    -g '"'"'!.git/**'"'"' \
    2>/dev/null || true)
fi

if [[ -n "$CONTENT_HITS" ]]; then
  echo "FAIL: Forbidden operator brand found in file contents:"
  echo ""
  echo "$CONTENT_HITS"
  echo ""
  FAIL=1
else
  echo "  PASS: no forbidden terms in file contents"
fi

echo ""

# ── 2. Filename / directory name check ───────────────────────────────────────

echo "▶ Checking filenames and directory names..."

PRUNE_EXPR=""
for d in "${EXCLUDE_DIRS[@]}"; do
  PRUNE_EXPR="$PRUNE_EXPR -path \"./$d\" -prune -o"
done

FILENAME_HITS=$(eval find . \
  $PRUNE_EXPR \
  "\\(" \
    -iname "'*banzami*'" \
    -o -iname "'*banzamia*'" \
  "\\)" \
  -print 2>/dev/null || true)

if [[ -n "$FILENAME_HITS" ]]; then
  echo "FAIL: Forbidden operator brand found in filenames/directories:"
  echo ""
  echo "$FILENAME_HITS"
  echo ""
  FAIL=1
else
  echo "  PASS: no forbidden terms in filenames or directory names"
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
  echo ""
  echo "Run this check again after fixing: scripts/check-operator-contamination.sh"
  exit 1
fi
