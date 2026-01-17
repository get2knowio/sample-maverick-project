# Implementation Plan: Greet CLI - Multilingual Hello World Tool

**Branch**: `001-greet-cli` | **Date**: 2026-01-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-greet-cli/spec.md`

## Summary

Build a CLI tool called `greet` that displays stylized "Hello, World!" greetings in 10 human languages with ASCII art figlet banners. The tool supports extensive customization options including language filtering, personalization, animated output modes, and fun features like cowsay bubbles and party mode with emoji confetti. Technical approach uses Python with Click for CLI, Rich for terminal formatting, and pyfiglet for ASCII art. Package management via `uv`.

## Technical Context

**Language/Version**: Python 3.10+
**Package Manager**: uv (with uv.lock committed)
**Primary Dependencies**: Click (CLI framework), Rich (terminal formatting/colors/layout), pyfiglet (ASCII art banners)
**Storage**: N/A (no persistence required; language data stored in-memory as Python data structures)
**Testing**: pytest with pytest-cov for coverage (run via `uv run pytest`)
**Target Platform**: Cross-platform CLI (macOS, Linux, Windows with Unicode terminal support)
**Project Type**: Single project (Python package with CLI entry point)
**Performance Goals**: <2 seconds for full output in non-animated mode (per SC-001)
**Constraints**: Must support Unicode (CJK, Arabic, Hindi scripts); graceful degradation when colors unsupported
**Scale/Scope**: 10 languages at launch; extensible architecture for easy language additions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verified against Constitution v1.0.1 (2026-01-16):

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pythonic & Idiomatic | PASS | dataclasses for Language/Proverb; f-strings; comprehensions; pathlib not needed (no file ops) |
| II. Type Safety | PASS | All functions typed; Python 3.10+ union syntax (`str \| None`); `list[str]` syntax |
| III. Test-Driven Development | PASS | pytest with unit/integration/contract structure; fixtures for shared setup |
| IV. CLI Interface | PASS | Click-based; `--no-color` support; proper exit codes (0, 1, 2); stderr for errors |
| V. Data-Driven Design | PASS | Languages in `languages.py`; proverbs in `fortunes.py`; no logic changes to add data |
| VI. Simplicity First | PASS | Functions over classes where appropriate; 2 levels of package nesting; no ABCs |

**Code Quality Standards Compliance:**

| Standard | Status | Notes |
|----------|--------|-------|
| Package Management | PASS | `uv` for deps; `uv.lock` committed; `uv run` for commands |
| Formatting & Linting | PASS | `ruff format`; `ruff check`; `mypy --strict` |
| Naming Conventions | PASS | lowercase_snake modules; PascalCase classes; SCREAMING_SNAKE constants |
| Documentation | PASS | Google-style docstrings; module docstrings required |

## Project Structure

### Documentation (this feature)

```text
specs/001-greet-cli/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI interface contract)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/
├── greet/
│   ├── __init__.py      # Package init with version
│   ├── cli.py           # Click CLI entry point and option parsing
│   ├── core.py          # Core greeting generation logic
│   ├── languages.py     # Language data configuration (dataclasses)
│   ├── fortunes.py      # Proverbs/sayings data (dataclasses)
│   ├── renderers/
│   │   ├── __init__.py
│   │   ├── figlet.py    # ASCII art banner rendering
│   │   ├── cowsay.py    # Cowsay bubble wrapper
│   │   ├── box.py       # Unicode box drawing
│   │   └── effects.py   # Rainbow, typewriter animations
│   └── output.py        # Output formatting and composition

tests/
├── conftest.py          # Shared fixtures
├── unit/
│   ├── test_languages.py
│   ├── test_core.py
│   ├── test_renderers.py
│   └── test_output.py
├── integration/
│   └── test_cli.py      # End-to-end CLI tests
└── contract/
    └── test_cli_contract.py  # CLI option validation tests

pyproject.toml           # Package configuration with CLI entry point
uv.lock                  # Locked dependencies (committed)
```

**Structure Decision**: Single Python package structure with modular renderers. The `renderers/` subpackage isolates visual formatting concerns (figlet, cowsay, box, effects) from core greeting logic, supporting the extensibility requirement (FR-016). Only 2 levels of nesting per Simplicity First principle.

## Quality Gates (Pre-Merge)

Per Constitution v1.0.1, all code MUST pass before merge:

```bash
# 1. Sync dependencies
uv sync

# 2. Run tests
uv run pytest

# 3. Type checking
uv run mypy --strict src/

# 4. Linting
uv run ruff check

# 5. Formatting verification
uv run ruff format --check
```

## Complexity Tracking

No constitution violations requiring justification.
