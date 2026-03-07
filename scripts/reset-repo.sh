#!/usr/bin/env bash
#
# Reset the sample-maverick-project repository to its baseline state.
# Use this after running tests that may have mutated the repo.
#
# Usage: ./scripts/reset-repo.sh [--force]
#   --force: Skip confirmation prompt
#
# Baseline is defined by the tag: baseline/main
# This tag is pushed to origin and used as the source of truth.
#
set -euo pipefail

MAIN_TAG="baseline/main"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if --force flag is provided
FORCE=false
if [[ "${1:-}" == "--force" ]]; then
    FORCE=true
fi

# Confirmation prompt
if [[ "$FORCE" != "true" ]]; then
    echo "This will:"
    echo "  - Delete ALL local branches except 'main'"
    echo "  - Hard reset 'main' to the baseline commit"
    echo "  - Force push to origin (resetting remote state)"
    echo "  - Remove all untracked files and directories"
    echo ""
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Aborted."
        exit 0
    fi
fi

log_info "Starting repository reset..."

# 1. Abort any in-progress operations
git merge --abort 2>/dev/null || true
git rebase --abort 2>/dev/null || true
git cherry-pick --abort 2>/dev/null || true

# 2. Fetch origin to ensure we have latest refs
log_info "Fetching origin..."
git fetch origin --prune

# 3. Checkout main first (safe branch to work from)
log_info "Checking out main..."
git checkout main --force

# 4. Delete all local branches except main
log_info "Deleting extra local branches..."
for branch in $(git branch | grep -v "^\*" | grep -v "main"); do
    branch_name=$(echo "$branch" | xargs)
    if [[ -n "$branch_name" ]]; then
        log_warn "Deleting branch: $branch_name"
        git branch -D "$branch_name" 2>/dev/null || true
    fi
done

# 5. Fetch baseline tag
log_info "Fetching baseline tag..."
git fetch origin "refs/tags/$MAIN_TAG:refs/tags/$MAIN_TAG" --force 2>/dev/null || true

# Verify tag exists
if ! git rev-parse "$MAIN_TAG" >/dev/null 2>&1; then
    log_error "Tag $MAIN_TAG not found. Cannot reset."
    exit 1
fi

# 6. Hard reset main to baseline tag
log_info "Resetting main to $MAIN_TAG..."
git reset --hard "$MAIN_TAG"

# 7. Delete remote branches that shouldn't exist (except main)
log_info "Cleaning up remote branches..."
for remote_branch in $(git branch -r | grep "origin/" | grep -v "origin/main" | grep -v "origin/HEAD"); do
    branch_name=$(echo "$remote_branch" | sed 's|origin/||' | xargs)
    if [[ -n "$branch_name" ]]; then
        log_warn "Deleting remote branch: $branch_name"
        git push origin --delete "$branch_name" 2>/dev/null || true
    fi
done

# 8. Force push main to ensure remote matches baseline
log_info "Force pushing main to origin..."
git push origin main --force

# 9. Ensure baseline tag is on origin
log_info "Pushing baseline tag to origin..."
git push origin "$MAIN_TAG" --force

# 10. Clean untracked files and directories
log_info "Cleaning untracked files..."
git clean -fdx

# 11. Re-initialize bd if .dolt is missing after clean
if [[ ! -d ".dolt" ]] && command -v bd >/dev/null 2>&1; then
    log_info "Re-initializing bd..."
    bd init 2>/dev/null || true
fi

log_info "Repository reset complete!"
echo ""
echo "Current state:"
git log --oneline -5
echo ""
git status
