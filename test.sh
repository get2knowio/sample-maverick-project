#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAVERICK_BIN="/workspaces/maverick/.venv/bin/maverick"

# Reset repo to baseline
"${SCRIPT_DIR}/scripts/reset-repo.sh" --force

# Copy .env from maverick project
cp /workspaces/maverick/.env "${SCRIPT_DIR}/.env"

# Run the feature workflow
cd "${SCRIPT_DIR}"
"${MAVERICK_BIN}" fly feature -i branch_name=001-greet-cli
