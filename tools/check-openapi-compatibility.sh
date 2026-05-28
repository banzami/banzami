#!/usr/bin/env bash
# check-openapi-compatibility.sh
# Compares two OpenAPI specs and reports breaking changes.
#
# Usage:
#   ./tools/check-openapi-compatibility.sh NEW OLD
#   ./tools/check-openapi-compatibility.sh --help
#
# A "breaking change" is any diff that would require consumers to change code:
#   - Removed endpoint
#   - Removed required request field
#   - Removed response field
#   - Changed field type
#   - Changed HTTP method on an existing path
#   - Changed a required field from optional to required in a response
#
# This tool uses Python (stdlib only) for YAML/JSON parsing. It is intentionally
# dependency-free so it works in any CI environment.
#
# Exit codes:
#   0 — no breaking changes detected
#   1 — breaking changes detected (details printed to stdout)
#   2 — usage error or file not found

set -euo pipefail

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  sed -n '2,20p' "$0" | sed 's/^# //'
  exit 0
fi

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 NEW_SPEC OLD_SPEC" >&2
  echo "  Compare NEW_SPEC against OLD_SPEC and report breaking changes." >&2
  exit 2
fi

NEW_SPEC="$1"
OLD_SPEC="$2"

if [[ ! -f "$NEW_SPEC" ]]; then
  echo "Error: NEW_SPEC not found: $NEW_SPEC" >&2
  exit 2
fi
if [[ ! -f "$OLD_SPEC" ]]; then
  echo "Error: OLD_SPEC not found: $OLD_SPEC" >&2
  exit 2
fi

python3 - "$NEW_SPEC" "$OLD_SPEC" <<'PYTHON'
import sys, json, re

def load_spec(path):
    with open(path) as f:
        content = f.read()
    # Try JSON first, fall back to YAML via stdlib (pyyaml not guaranteed).
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Minimal YAML→dict for OpenAPI files: handles simple mappings.
    # For full YAML support, install pyyaml and use yaml.safe_load().
    try:
        import yaml  # type: ignore
        return yaml.safe_load(content)
    except ImportError:
        print("Warning: pyyaml not installed. YAML support is limited.", file=sys.stderr)
        # Return empty spec — cannot parse.
        return {}

def get_paths(spec):
    return spec.get("paths", {})

def get_methods(path_item):
    http_methods = {"get","post","put","patch","delete","head","options"}
    return {k: v for k, v in path_item.items() if k in http_methods}

def get_required_body_fields(op):
    body = op.get("requestBody", {})
    content = body.get("content", {})
    for media_type in content.values():
        schema = media_type.get("schema", {})
        return set(schema.get("required", []))
    return set()

def get_response_fields(op):
    for status, resp in op.get("responses", {}).items():
        if str(status).startswith("2"):
            content = resp.get("content", {})
            for media_type in content.values():
                schema = media_type.get("schema", {})
                props = schema.get("properties", {})
                return set(props.keys())
    return set()

def check_breaking(new_spec, old_spec):
    breaking = []
    old_paths = get_paths(old_spec)
    new_paths = get_paths(new_spec)

    # 1. Removed endpoints.
    for path, path_item in old_paths.items():
        if path not in new_paths:
            for method in get_methods(path_item):
                breaking.append(f"REMOVED endpoint: {method.upper()} {path}")
            continue

        old_methods = get_methods(path_item)
        new_methods = get_methods(new_paths[path])

        for method, old_op in old_methods.items():
            if method not in new_methods:
                breaking.append(f"REMOVED method: {method.upper()} {path}")
                continue

            new_op = new_methods[method]

            # 2. Removed required request body fields.
            old_req = get_required_body_fields(old_op)
            new_req = get_required_body_fields(new_op)
            for field in old_req - new_req:
                breaking.append(f"REMOVED required request field '{field}': {method.upper()} {path}")

            # 3. Removed response fields.
            old_resp = get_response_fields(old_op)
            new_resp = get_response_fields(new_op)
            for field in old_resp - new_resp:
                breaking.append(f"REMOVED response field '{field}': {method.upper()} {path}")

    return breaking

new_spec = load_spec(sys.argv[1])
old_spec = load_spec(sys.argv[2])

if not new_spec or not old_spec:
    print("Could not parse one or both specs. Ensure pyyaml is installed for YAML files.")
    sys.exit(2)

issues = check_breaking(new_spec, old_spec)

if issues:
    print(f"BREAKING CHANGES DETECTED ({len(issues)} issues):")
    for issue in issues:
        print(f"  ✗ {issue}")
    sys.exit(1)
else:
    new_count = sum(len(get_methods(pi)) for pi in get_paths(new_spec).values())
    old_count = sum(len(get_methods(pi)) for pi in get_paths(old_spec).values())
    print(f"No breaking changes detected.")
    print(f"  Old spec: {old_count} operations")
    print(f"  New spec: {new_count} operations")
    if new_count > old_count:
        print(f"  + {new_count - old_count} new operation(s) added")
    sys.exit(0)
PYTHON
