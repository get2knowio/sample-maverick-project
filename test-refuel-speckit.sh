#!/usr/bin/env bash
set -euo pipefail

# Shared setup: reset repo, copy .env, maverick init
source "$(dirname "${BASH_SOURCE[0]}")/scripts/test-setup.sh"

SPEC="001-greet-cli"

# 1. List workflow steps (smoke test for workflow discovery + YAML parsing)
echo "=== Listing refuel-speckit workflow steps ==="
"${MAVERICK_BIN}" refuel speckit "${SPEC}" --list-steps

# 2. Dry-run (shows execution plan, no bd/git mutations)
echo ""
echo "=== Running refuel-speckit workflow (dry-run) ==="
"${MAVERICK_BIN}" refuel speckit "${SPEC}" --dry-run

# 3. Live run (preflight validates bd, creates real beads, commits & merges)
echo ""
echo "=== Running refuel-speckit workflow (live) ==="
"${MAVERICK_BIN}" refuel speckit "${SPEC}" \
  --session-log "/tmp/refuel-session.jsonl"

# 4. Verify bead creation
echo ""
echo "=== Verifying bead creation ==="
BEADS_JSON=$(bd list --json)
EPIC_COUNT=$(echo "${BEADS_JSON}" | jq '[.[] | select(.issue_type == "epic")] | length')
TASK_COUNT=$(echo "${BEADS_JSON}" | jq '[.[] | select(.issue_type == "task")] | length')
echo "  Epics: ${EPIC_COUNT}"
echo "  Tasks: ${TASK_COUNT}"
[[ "${EPIC_COUNT}" -ge 1 ]] || { echo "FAIL: No epic bead created"; exit 1; }
[[ "${TASK_COUNT}" -ge 1 ]] || { echo "FAIL: No task beads created"; exit 1; }

# 5. Verify ready/blocked status
echo ""
echo "=== Structural dependency verification ==="
READY_COUNT=$(bd ready --json | jq 'length')
BLOCKED_COUNT=$(bd blocked --json | jq 'length')
echo "  Ready (unblocked): ${READY_COUNT}"
echo "  Blocked: ${BLOCKED_COUNT}"
[[ "${READY_COUNT}" -ge 1 ]]   || { echo "FAIL: No ready beads"; exit 1; }
[[ "${BLOCKED_COUNT}" -ge 1 ]] || { echo "FAIL: No blocked beads"; exit 1; }

echo ""
echo "=== All verifications passed ==="
