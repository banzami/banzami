#!/usr/bin/env bash
# Banzami Conformance Runner — shell wrapper
# Usage: ./run.sh [--url URL] [--level N] [--suite SUITE] [--output FILE]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$SCRIPT_DIR/run.py" "$@"
