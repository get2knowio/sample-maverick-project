#!/usr/bin/env bash
set -euo pipefail

# Shared setup: reset repo, copy .env, maverick init
source "$(dirname "${BASH_SOURCE[0]}")/scripts/test-setup.sh"

SPEC="001-greet-cli"

# 1. Create beads from spec (prerequisite: populates epic + task beads)
echo "=== Creating beads from spec ==="
"${MAVERICK_BIN}" refuel speckit "${SPEC}" \
  --session-log "${REPO_ROOT}/refuel-session.jsonl"

# 2. Capture the epic ID for fly
echo ""
echo "=== Locating epic bead ==="
EPIC_ID=$(bd list --json | jq -r '[.[] | select(.type == "epic")][0].id')
if [[ -z "${EPIC_ID}" || "${EPIC_ID}" == "null" ]]; then
  echo "FAIL: No epic bead found after refuel speckit"
  exit 1
fi
echo "  Epic ID: ${EPIC_ID}"

# 3. List workflow steps (smoke test for workflow discovery + YAML parsing)
echo ""
echo "=== Listing fly workflow steps ==="
"${MAVERICK_BIN}" fly --epic "${EPIC_ID}" --list-steps

# 4. Dry-run (shows execution plan, validates inputs without mutations)
echo ""
echo "=== Running fly workflow (dry-run) ==="
"${MAVERICK_BIN}" fly --epic "${EPIC_ID}" --dry-run

# 5. Live run (implements beads, commits, closes)
echo ""
echo "=== Running fly workflow (live) ==="
"${MAVERICK_BIN}" fly --epic "${EPIC_ID}" \
  --skip-review --max-beads 5 \
  --session-log "${REPO_ROOT}/fly-beads-session.jsonl"

# 6. Verify bead progress
echo ""
echo "=== Verifying bead progress ==="
READY_COUNT=$(bd ready --json | jq 'length')
CLOSED_COUNT=$(bd list --json | jq '[.[] | select(.status == "closed")] | length')
echo "  Remaining ready: ${READY_COUNT}"
echo "  Closed: ${CLOSED_COUNT}"
[[ "${CLOSED_COUNT}" -ge 1 ]] || { echo "FAIL: No beads were closed"; exit 1; }

echo ""
echo "=== All verifications passed ==="
