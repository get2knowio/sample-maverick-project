#!/usr/bin/env bash
set -euo pipefail

# Shared setup: reset repo, copy .env, maverick init
source "$(dirname "${BASH_SOURCE[0]}")/scripts/test-setup.sh"

# Run the feature workflow with session logging
"${MAVERICK_BIN}" fly run feature -i branch_name=001-greet-cli \
  --session-log "${REPO_ROOT}/session.jsonl"
