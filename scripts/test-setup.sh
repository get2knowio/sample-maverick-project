#!/usr/bin/env bash
#
# Shared setup for test scripts.
# Sources environment, resets repo to baseline, and initializes maverick.
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

# Reset repo to baseline
"${REPO_ROOT}/scripts/reset-repo.sh" --force

# Copy .env from maverick project
cp /workspaces/maverick/.env "${REPO_ROOT}/.env"

# Clean stale stealth-mode exclusions (bd now runs in normal mode)
sed -i '/\.beads\//d' "${REPO_ROOT}/.git/info/exclude" 2>/dev/null || true

# Initialize maverick project config and beads workspace
cd "${REPO_ROOT}"
"${MAVERICK_BIN}" init --no-detect --type python --force
