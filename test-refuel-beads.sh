#!/usr/bin/env bash
set -euo pipefail

# Shared setup: reset repo, copy .env, maverick init
source "$(dirname "${BASH_SOURCE[0]}")/scripts/test-setup.sh"

SPEC_DIR="${REPO_ROOT}/specs/001-greet-cli"

# 1. List workflow steps (smoke test for workflow discovery + YAML parsing)
echo "=== Listing refuel-speckit workflow steps ==="
"${MAVERICK_BIN}" refuel speckit "${SPEC_DIR}" --list-steps

# 2. Run the refuel-speckit workflow in dry-run mode
#    (creates synthetic bead IDs, wires dependencies, no bd CLI needed)
echo ""
echo "=== Running refuel-speckit workflow (dry-run) ==="
"${MAVERICK_BIN}" refuel speckit "${SPEC_DIR}" --dry-run \
  --session-log "${REPO_ROOT}/refuel-session.jsonl"

echo ""
echo "=== refuel-speckit dry-run completed successfully ==="
