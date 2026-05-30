#!/usr/bin/env bash
# Detects forbidden terminology across Banzami ecosystem repos.
# Run from: apps/banzamia/
# Usage: bash scripts/audit-terminology.sh [repo-root-or-path]

set -euo pipefail

SEARCH_ROOTS="${1:-../../}"
FAILED=0

check() {
  local term="$1"
  local description="$2"
  local results
  results=$(grep -rn "$term" $SEARCH_ROOTS \
    --include="*.md" --include="*.ts" --include="*.tsx" \
    2>/dev/null | grep -v node_modules | grep -v ".git" | grep -v ".dart_tool" | grep -v "ios/Pods" | grep -v ".pytest_cache" | grep -v ".venv" | grep -v "docs/audit/" || true)
  if [ -n "$results" ]; then
    echo "❌ FORBIDDEN TERM: $description"
    echo "$results" | head -5
    echo ""
    FAILED=1
  fi
}

echo "🔍 BanzamIA Terminology Audit"
echo "=============================="
echo ""

check "Protocol Intelligence" '"Protocol Intelligence" as canonical BanzamIA title'
check "banzami-core[^-]" '"banzami-core" as package name (container names like banzami-core-api are OK)'
check "fm65/BanzamIA" '"fm65/BanzamIA" old repo path'
check "Future Third-Party Operators" '"Future Third-Party Operators" (use "Certified Operators")'
check "Reference-compatible" '"Reference-compatible" (use "Sandbox Operator")'
check "Protocol-compatible" '"Protocol-compatible" (use "Payment Operator")'
check "Trace-compatible" '"Trace-compatible" (use "Settlement Operator")'
check "Federation-ready" '"Federation-ready" (use "Federation Operator")'
check "Settlement-compatible" '"Settlement-compatible" (use "Infrastructure Operator")'
check "Core Payments" '"Core Payments" as certification level name (use "Payment Operator")'
check "Advanced Payments" '"Advanced Payments" as certification level name (use "Settlement Operator")'
check "Full Protocol" '"Full Protocol" as certification level name (use "Federation Operator")'
check "Sandbox Certified" '"Sandbox Certified" as certification level name (use "Sandbox Operator")'
check "Infrastructure Op[^e]" '"Infrastructure Op" abbreviation (use "Infrastructure Operator")'

if [ $FAILED -eq 0 ]; then
  echo "✅ All terminology checks passed."
else
  echo "💥 Audit failed — forbidden terms detected above."
  exit 1
fi
