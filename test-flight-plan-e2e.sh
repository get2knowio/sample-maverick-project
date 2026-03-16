#!/usr/bin/env bash
set -euo pipefail

# Shared setup: reset repo, maverick init
source "$(dirname "${BASH_SOURCE[0]}")/scripts/test-setup.sh"

PRD="docs/greet-cli-prd.md"
PLAN_NAME="greet-cli"
PLAN_DIR=".maverick/plans/${PLAN_NAME}"
FLIGHT_PLAN="${PLAN_DIR}/flight-plan.md"

# ── Phase 1: Generate flight plan from PRD ──────────────────
echo "=== Phase 1: Generating flight plan from PRD ==="
"${MAVERICK_BIN}" plan generate "${PLAN_NAME}" \
  --from-prd "${PRD}" \
  --session-log /tmp/generate-flight-plan-session.jsonl
[[ -f "${FLIGHT_PLAN}" ]] || { echo "FAIL: Flight plan not created"; exit 1; }
echo "  Flight plan created at ${FLIGHT_PLAN}"

# ── Phase 2: Validate generated flight plan ─────────────────
echo ""
echo "=== Phase 2: Validating generated flight plan ==="
"${MAVERICK_BIN}" plan validate "${PLAN_NAME}"

# ── Phase 3: Refuel — decompose into work units + beads ─────
echo ""
echo "=== Phase 3: Refuel ==="
"${MAVERICK_BIN}" refuel "${PLAN_NAME}" \
  --session-log /tmp/refuel-flight-plan-session.jsonl

WU_COUNT=$(find "${PLAN_DIR}" -name "[0-9][0-9][0-9]-*.md" 2>/dev/null | wc -l)
echo "  Work unit files: ${WU_COUNT}"
[[ "${WU_COUNT}" -ge 1 ]] || { echo "FAIL: No work unit files"; exit 1; }

BEADS_JSON=$(bd list --flat --json)
EPIC_COUNT=$(echo "${BEADS_JSON}" | jq '[.[] | select(.issue_type == "epic")] | length')
TASK_COUNT=$(echo "${BEADS_JSON}" | jq '[.[] | select(.issue_type == "task")] | length')
echo "  Epics: ${EPIC_COUNT}, Tasks: ${TASK_COUNT}"
[[ "${EPIC_COUNT}" -ge 1 ]] || { echo "FAIL: No epic"; exit 1; }
[[ "${TASK_COUNT}" -ge 1 ]] || { echo "FAIL: No tasks"; exit 1; }

EPIC_ID=$(echo "${BEADS_JSON}" | jq -r '[.[] | select(.issue_type == "epic")][0].id')
echo "  Epic ID: ${EPIC_ID}"

echo ""
echo "=== Brief: Beads created ==="
"${MAVERICK_BIN}" brief --epic "${EPIC_ID}"

# ── Phase 4: Fly — implement a subset of beads ─────────────
echo ""
echo "=== Phase 4: Fly (max 3 beads, skip review) ==="
FLY_EXIT=0
"${MAVERICK_BIN}" fly --epic "${EPIC_ID}" \
  --max-beads 3 \
  --auto-commit \
  --session-log /tmp/fly-flight-plan-session.jsonl || FLY_EXIT=$?
if [[ "${FLY_EXIT}" -ne 0 ]]; then
  echo "  fly exited ${FLY_EXIT} (partial completion tolerated)"
fi

CLOSED_COUNT=$(bd list --all --flat --json | jq '[.[] | select(.status == "closed")] | length')
echo "  Closed beads: ${CLOSED_COUNT}"
[[ "${CLOSED_COUNT}" -ge 1 ]] || { echo "FAIL: No beads closed"; exit 1; }

"${MAVERICK_BIN}" workspace status

# ── Phase 4b: Verify runway data was recorded ────────────────
echo ""
echo "=== Phase 4b: Verify runway recording ==="
PROJECT_NAME=$(basename "${REPO_ROOT}")
WORKSPACE_RUNWAY="${HOME}/.maverick/workspaces/${PROJECT_NAME}/.maverick/runway"
if [[ -d "${WORKSPACE_RUNWAY}" ]]; then
  echo "  Runway directory exists at ${WORKSPACE_RUNWAY}"
  OUTCOME_LINES=$(wc -l < "${WORKSPACE_RUNWAY}/episodic/bead-outcomes.jsonl" 2>/dev/null || echo 0)
  echo "  Bead outcome records: ${OUTCOME_LINES}"
  [[ "${OUTCOME_LINES}" -ge 1 ]] || echo "  WARN: No bead outcomes recorded (best-effort, non-fatal)"
else
  echo "  WARN: Runway not found in workspace (best-effort, non-fatal)"
fi

# ── Phase 5: Land — push changes ────────────────────────────
echo ""
echo "=== Phase 5: Land ==="
"${MAVERICK_BIN}" land --yes 

git fetch origin
git log origin/main --oneline -5

# ── Phase 5b: Verify runway consolidation ran ────────────────
echo ""
echo "=== Phase 5b: Verify runway consolidation ==="
USER_RUNWAY="${REPO_ROOT}/.maverick/runway"
if [[ -d "${USER_RUNWAY}/semantic" ]]; then
  INSIGHTS="${USER_RUNWAY}/semantic/consolidated-insights.md"
  if [[ -f "${INSIGHTS}" ]]; then
    INSIGHTS_SIZE=$(wc -c < "${INSIGHTS}")
    echo "  consolidated-insights.md exists (${INSIGHTS_SIZE} bytes)"
    [[ "${INSIGHTS_SIZE}" -gt 0 ]] || echo "  WARN: Insights file is empty"
  else
    echo "  WARN: consolidated-insights.md not found (consolidation may have been skipped)"
  fi
else
  echo "  WARN: No semantic directory in user runway (consolidation may not have synced)"
fi

echo ""
echo "=== All flight-plan e2e verifications passed ==="
