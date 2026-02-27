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
<!-- MANUAL ADDITIONS END -->
