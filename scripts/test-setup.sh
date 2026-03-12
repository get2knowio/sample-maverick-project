#!/usr/bin/env bash
#
# Shared setup for test scripts.
# Resets repo to baseline and initializes maverick.
#
# Usage: source scripts/test-setup.sh
#   After sourcing, SCRIPT_DIR, REPO_ROOT, and MAVERICK_BIN are available.
#
set -euo pipefail

# Resolve paths relative to the caller's location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}"
MAVERICK_BIN="/workspaces/maverick/.venv/bin/maverick"

# Disable pagers to avoid blocking in non-interactive environments
export GH_PAGER=
export GIT_PAGER=

# Stop any running dolt server before reset — git clean -fdx in reset-repo.sh
# deletes .beads/dolt/ (the data dir) leaving the server with a dangling ref.
# Killing it first lets bd init (via maverick init) start a fresh instance.
pkill -f 'dolt sql-server' 2>/dev/null && sleep 1 || true

# Reset repo to baseline
"${REPO_ROOT}/scripts/reset-repo.sh" --force

# Clean stale stealth-mode exclusions (bd now runs in normal mode)
sed -i '/\.beads\//d' "${REPO_ROOT}/.git/info/exclude" 2>/dev/null || true

# Clean any stale maverick workspace from previous runs
cd "${REPO_ROOT}"
"${MAVERICK_BIN}" workspace clean --yes 2>/dev/null || true

# Initialize maverick project config and beads workspace
"${MAVERICK_BIN}" init --no-detect --type python --force

# Restore the curated test config (init --force overwrites maverick.yaml with a bare one)
cp "${REPO_ROOT}/maverick.test.yaml" "${REPO_ROOT}/maverick.yaml"
