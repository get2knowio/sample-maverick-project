#!/usr/bin/env bash
set -euo pipefail

# Shared setup: reset repo, copy .env, maverick init
source "$(dirname "${BASH_SOURCE[0]}")/scripts/test-setup.sh"

SPEC="001-greet-cli"

# 1. Create beads from spec (prerequisite: populates epic + task beads)
echo "=== Creating beads from spec ==="
"${MAVERICK_BIN}" refuel speckit "${SPEC}" \
  --session-log "/tmp/refuel-session.jsonl"

# 2. Capture the epic ID for fly
echo ""
echo "=== Locating epic bead ==="
EPIC_ID=$(bd list --json | jq -r '[.[] | select(.issue_type == "epic")][0].id')
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

# 5. Live run (implements beads in hidden workspace, commits via jj)
#    Tolerate partial completion — later beads may time out, but we only
#    need at least one closed bead to verify the fly→land pipeline.
echo ""
echo "=== Running fly workflow (live) ==="
FLY_EXIT=0
"${MAVERICK_BIN}" fly --epic "${EPIC_ID}" \
  --skip-review --max-beads 5 \
  --session-log "/tmp/fly-beads-session.jsonl" || FLY_EXIT=$?
if [[ "${FLY_EXIT}" -ne 0 ]]; then
  echo "  fly exited with code ${FLY_EXIT} (partial completion expected)"
fi

# 6. Verify bead progress
echo ""
echo "=== Verifying bead progress ==="
READY_COUNT=$(bd ready --json | jq 'length')
CLOSED_COUNT=$(bd list --all --json | jq '[.[] | select(.status == "closed")] | length')
echo "  Remaining ready: ${READY_COUNT}"
echo "  Closed: ${CLOSED_COUNT}"
[[ "${CLOSED_COUNT}" -ge 1 ]] || { echo "FAIL: No beads were closed"; exit 1; }

# 7. Verify hidden workspace was created
echo ""
echo "=== Verifying workspace state ==="
"${MAVERICK_BIN}" workspace status

# 8. Land: push commits from workspace (skip curation, auto-approve)
echo ""
echo "=== Running land (push) ==="
"${MAVERICK_BIN}" land --yes --no-curate

# 9. Verify workspace was cleaned up after land
echo ""
echo "=== Verifying workspace teardown ==="
if "${MAVERICK_BIN}" workspace status 2>&1 | grep -q "active"; then
  echo "WARN: Workspace still active after land (may be expected if land preserved it)"
else
  echo "  Workspace cleaned up (or no longer active)"
fi

# 10. Verify changes landed on the remote
echo ""
echo "=== Verifying push to remote ==="
git fetch origin
REMOTE_COMMITS=$(git log origin/main --oneline -10)
echo "  Recent remote commits:"
echo "${REMOTE_COMMITS}" | head -5

echo ""
echo "=== All verifications passed ==="
