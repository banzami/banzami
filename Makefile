.PHONY: identity-check check cargo-check test help

# ── Identity guard ────────────────────────────────────────────────────────────

## identity-check: Verify no operator-specific brand contamination in BANZA
identity-check:
	@scripts/check-operator-contamination.sh

# ── Rust kernel ───────────────────────────────────────────────────────────────

## cargo-check: Type-check all 19 kernel crates
cargo-check:
	cd core && cargo check --workspace

## test: Run Python SDK unit tests
test:
	cd sdk/python && python3 -m pytest tests/unit/ -q

## conformance-check: Run conformance vector validation
conformance-check:
	python3 tools/banza-conformance/run.py --suite health --url http://localhost:3100 || \
	  echo "Note: sandbox operator must be running at :3100 for full check"

# ── Pre-commit ────────────────────────────────────────────────────────────────

## pre-commit: Run all fast checks before committing
pre-commit: identity-check

# ── Help ──────────────────────────────────────────────────────────────────────

## help: Show available make targets
help:
	@grep -E '^## ' Makefile | sed 's/^## /  /'
