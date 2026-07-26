# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python CLI tool (`greet`) that displays multilingual "Hello, World!" greetings with ASCII art. Uses Click for CLI, Rich for terminal formatting, pyfiglet for ASCII banners.

## Commands

```bash
# Package management (uv required)
uv sync                              # Install dependencies from lock file
uv add <package>                     # Add runtime dependency
uv add --dev <package>               # Add dev dependency

# Development
uv run greet                         # Run CLI
uv run greet --help                  # Show help

# Quality gates (all must pass before merge)
uv run pytest                        # Run tests
uv run mypy --strict src/            # Type checking
uv run ruff check                    # Linting
uv run ruff format --check           # Formatting verification

# Single test
uv run pytest tests/unit/test_core.py::test_function_name -v
```

## Architecture

```
src/greet/
├── cli.py           # Click entry point, option parsing
├── core.py          # Greeting generation logic, OutputConfig dataclass
├── languages.py     # Language dataclass, LANGUAGES list (data-driven)
├── fortunes.py      # Proverb dataclass, PROVERBS list
├── output.py        # Rich Console wrapper, rendering functions
└── renderers/       # Visual formatting modules
    ├── figlet.py    # ASCII art banners
    ├── cowsay.py    # Speech bubble wrapper
    ├── box.py       # Unicode box drawing
    └── effects.py   # Rainbow, typewriter animations

tests/
├── unit/            # Fast, isolated tests mirroring src/ structure
├── integration/     # CLI invocation tests
└── contract/        # Interface stability tests
```

## Constitution Requirements

The project constitution (`.specify/memory/constitution.md`) is authoritative. Key rules:

**Python Style:**
- Type hints on all functions (use `str | None` syntax, not `Optional`)
- Use `list[str]` syntax (not `List[str]`)
- Prefer dataclasses for data containers
- f-strings only (no `.format()` or `%`)
- Max 3 levels of indentation

**Data-Driven Design:**
- Languages/proverbs stored as typed data structures in dedicated modules
- Adding new data must not require logic changes

**CLI Conventions:**
- Exit codes: 0=success, 1=invalid option, 2=invalid language
- Errors to stderr, content to stdout
- Support `--no-color` for pipeable output

**Simplicity:**
- Functions over classes when no state needed
- No abstract base classes unless 3+ implementations
- Delete dead code immediately

## Speckit Workflow

Feature specifications live in `specs/NNN-feature-name/`. Use slash commands:
- `/speckit.specify` - Create/update feature spec
- `/speckit.plan` - Generate implementation plan
- `/speckit.tasks` - Generate task list from plan
- `/speckit.analyze` - Cross-artifact consistency check
- `/speckit.implement` - Execute tasks

<!-- MANUAL ADDITIONS START -->

## Repository Baseline & Reset

The repo uses a **tag-based baseline** (`baseline/main`) as the source of truth for clean state. To reset back to baseline:

```bash
git fetch origin
git reset --hard baseline/main
git clean -fdx
git push origin main --force
```

After resetting, regenerate `maverick.yaml` with `maverick init --force`.

**Updating the baseline**: After committing changes you want preserved across resets, move the tag:

```bash
git tag -f baseline/main HEAD
git push origin baseline/main --force
```

<!-- MANUAL ADDITIONS END -->


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:6cd5cc61 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Agent Context Profiles

The managed Beads block is task-tracking guidance, not permission to override repository, user, or orchestrator instructions.

- **Conservative (default)**: Use `bd` for task tracking. Do not run git commits, git pushes, or Dolt remote sync unless explicitly asked. At handoff, report changed files, validation, and suggested next commands.
- **Minimal**: Keep tool instruction files as pointers to `bd prime`; use the same conservative git policy unless active instructions say otherwise.
- **Team-maintainer**: Only when the repository explicitly opts in, agents may close beads, run quality gates, commit, and push as part of session close. A current "do not commit" or "do not push" instruction still wins.

## Session Completion

This protocol applies when ending a Beads implementation workflow. It is subordinate to explicit user, repository, and orchestrator instructions.

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **Handle git/sync by active profile**:
   ```bash
   # Conservative/minimal/default: report status and proposed commands; wait for approval.
   git status

   # Team-maintainer opt-in only, unless current instructions forbid it:
   git pull --rebase
   git push
   git status
   ```
5. **Hand off** - Summarize changes, validation, issue status, and any blocked sync/commit/push step

**Critical rules:**
- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from the active profile or the current user request.
- If a required sync or push is blocked, stop and report the exact command and error.
<!-- END BEADS INTEGRATION -->
