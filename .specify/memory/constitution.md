<!--
Sync Impact Report
==================
Version change: 1.0.0 → 1.0.1
Modified sections:
  - Code Quality Standards: Added uv as package manager
  - Development Workflow > Quality Gates: Added uv sync command
Added sections: None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ (no changes needed)
  - .specify/templates/spec-template.md ✅ (no changes needed)
  - .specify/templates/tasks-template.md ✅ (no changes needed)
  - specs/001-greet-cli/quickstart.md ⚠ (should update install commands to use uv)
Follow-up TODOs: Update quickstart.md to use uv commands
-->

# Greet CLI Project Constitution

## Core Principles

### I. Pythonic & Idiomatic Code

All code MUST follow Python idioms and conventions as defined by PEP 8 and the Python community.

**Non-negotiable rules:**
- Use descriptive variable names that read like English (`languages_to_display` not `lang_lst`)
- Prefer list/dict/set comprehensions over manual loops when they improve readability
- Use context managers (`with`) for resource management
- Leverage Python's standard library before adding dependencies
- Use f-strings for string formatting (not `.format()` or `%`)
- Follow "flat is better than nested" - max 3 levels of indentation
- Use `pathlib.Path` over `os.path` for file operations
- Prefer `dataclasses` or `NamedTuple` for data containers

**Rationale:** Pythonic code is readable, maintainable, and works with the language rather than against it.

### II. Type Safety

All code MUST use type hints as defined by PEP 484 and modern Python typing features.

**Non-negotiable rules:**
- All function signatures MUST include type annotations (parameters and return types)
- All module-level constants MUST be typed
- Use `typing` module features: `Optional`, `Union`, `TypeAlias` where appropriate
- Use `|` union syntax for Python 3.10+ (e.g., `str | None` not `Optional[str]`)
- Generic collections use built-in syntax (`list[str]` not `List[str]`)
- Complex types SHOULD be extracted to `TypeAlias` for readability

**Rationale:** Type hints enable IDE support, catch bugs early, and serve as documentation.

### III. Test-Driven Development

Tests MUST be written before implementation when explicitly requested. Test coverage is a quality gate.

**Non-negotiable rules:**
- When tests are requested: Write tests first → Verify they fail → Implement → Verify they pass
- Use pytest as the testing framework
- Test files mirror source structure (`src/greet/core.py` → `tests/unit/test_core.py`)
- Unit tests MUST be fast (<100ms each) and isolated (no external dependencies)
- Integration tests cover user-facing behavior (CLI invocations)
- Contract tests verify interface stability
- Use fixtures for shared test setup; avoid test inheritance

**Rationale:** Tests provide confidence for refactoring and document expected behavior.

### IV. CLI Interface

All user interaction MUST flow through a well-defined command-line interface following Unix conventions.

**Non-negotiable rules:**
- Use Click for CLI implementation (decorator-based, composable)
- Follow text I/O protocol: `stdin/args` → `stdout`, errors → `stderr`
- Support `--no-color` flag for plain text output (pipeable, loggable)
- Exit codes: `0` = success, non-zero = error (documented per command)
- Provide `--help` for all commands with clear descriptions
- Error messages MUST be actionable ("Invalid language 'xyz'. Valid: english, french...")
- Support standard signals (SIGINT for graceful termination)

**Rationale:** CLI tools that follow conventions integrate well with Unix pipelines and automation.

### V. Data-Driven Design

Configuration and data MUST be separated from logic to enable extensibility without code changes.

**Non-negotiable rules:**
- Data definitions (languages, proverbs) stored in dedicated modules as typed data structures
- Adding new data (e.g., a new language) MUST NOT require logic changes
- Use dataclasses or TypedDict for structured data
- Avoid magic strings in logic; reference data by attribute
- Configuration follows: constants → environment → defaults (no config files unless justified)

**Rationale:** Data-driven design enables non-developers to extend functionality and reduces code duplication.

### VI. Simplicity First

Start with the simplest solution that works. Complexity MUST be justified.

**Non-negotiable rules:**
- YAGNI: Do not implement features "for the future"
- Prefer functions over classes when state is not needed
- Avoid inheritance; use composition or plain functions
- No abstract base classes unless 3+ concrete implementations exist
- Max 3 levels of package nesting
- Max 1 level of function call depth for main logic paths
- If a function exceeds 30 lines, consider splitting
- Delete dead code immediately; do not comment it out

**Rationale:** Simple code is easier to understand, test, and maintain. Complexity is a cost.

## Code Quality Standards

### Package Management

- **Package manager**: Use `uv` for all dependency and environment management
- **Lock file**: `uv.lock` MUST be committed to version control
- **Virtual environments**: Use `uv venv` to create isolated environments
- **Adding dependencies**: `uv add <package>` (runtime) or `uv add --dev <package>` (dev)
- **Syncing**: `uv sync` to install all dependencies from lock file
- **Running commands**: `uv run <command>` to execute in project environment

**Rationale:** `uv` is fast, deterministic, and provides modern Python packaging with lockfile support.

### Formatting & Linting

- **Formatter**: Use `ruff format` (drop-in black replacement, faster)
- **Import sorting**: Handled by `ruff` (isort-compatible)
- **Linter**: Use `ruff check` for fast, comprehensive linting
- **Type checker**: Use `mypy` in strict mode for type verification

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | lowercase_snake | `languages.py`, `cowsay.py` |
| Classes | PascalCase | `Language`, `OutputConfig` |
| Functions | lowercase_snake | `render_greeting()`, `wrap_in_box()` |
| Constants | SCREAMING_SNAKE | `DEFAULT_NAME`, `SUPPORTED_LANGUAGES` |
| Type aliases | PascalCase | `LanguageCode`, `GreetingTemplate` |

### Documentation

- All public modules MUST have a docstring describing purpose
- All public functions MUST have a docstring (Google style preferred)
- Inline comments explain "why", not "what"
- README.md covers installation and basic usage
- Complex algorithms get a brief explanation comment

## Development Workflow

### Branch Strategy

- Feature branches follow pattern: `NNN-short-name` (e.g., `001-greet-cli`)
- Main branch is protected; all changes via PR
- Commits are atomic and descriptive

### Quality Gates

Before merge, code MUST pass:
1. Dependencies synced (`uv sync`)
2. All tests (`uv run pytest`)
3. Type checking (`uv run mypy --strict src/`)
4. Linting (`uv run ruff check`)
5. Formatting verification (`uv run ruff format --check`)

### Review Checklist

- [ ] Does the code follow Pythonic idioms?
- [ ] Are all functions typed?
- [ ] Are tests present and passing (if requested)?
- [ ] Is the solution as simple as possible?
- [ ] Is configuration separated from logic?
- [ ] Does CLI output follow conventions?

## Governance

This constitution supersedes all other development practices for this project.

**Amendment Process:**
1. Propose change with rationale in a PR
2. Document impact on existing code
3. Update version following semver (MAJOR.MINOR.PATCH)
4. Migrate affected code before merge

**Compliance:**
- All PRs MUST verify compliance with principles
- Violations MUST be documented in plan.md Complexity Tracking table with justification
- Constitution is the source of truth; CLAUDE.md and other guides derive from it

**Version**: 1.0.1 | **Ratified**: 2026-01-16 | **Last Amended**: 2026-01-16
