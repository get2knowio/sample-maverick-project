# Quickstart: Greet CLI

**Feature**: 001-greet-cli
**Date**: 2026-01-16

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) (fast Python package manager)
- Terminal with Unicode support (for CJK, Arabic, Hindi scripts)

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install dependencies and create virtual environment (uv handles both)
uv sync

# Install in editable mode with dev dependencies
uv sync --dev
```

### From Package (Production)

```bash
uv tool install greet-cli
# Or with pip:
pip install greet-cli
```

## Basic Usage

```bash
# Display greetings in all 10 languages
uv run greet

# Display specific languages
uv run greet -l french,spanish

# Personalize with your name
uv run greet --name "Alice"
```

## Quick Examples

### Simple Output

```bash
# Plain text (no colors, no banners)
uv run greet --no-color --no-figlet
```

### Fun Modes

```bash
# Random greeting with cowsay
uv run greet --random --cowsay

# Party mode!
uv run greet --party

# Animated rainbow typewriter
uv run greet --typewriter --rainbow
```

### Combined Options

```bash
# French greeting for Marie in a decorative box
uv run greet -l french --name "Marie" --box

# Grid layout with fortune
uv run greet --all-at-once --fortune
```

## Development

### Run Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=greet --cov-report=term-missing

# Specific test file
uv run pytest tests/unit/test_languages.py
```

### Code Quality

```bash
# Type checking
uv run mypy --strict src/greet

# Linting
uv run ruff check src/greet

# Formatting check
uv run ruff format --check src/greet
```

### Adding Dependencies

```bash
# Runtime dependency
uv add click

# Development dependency
uv add --dev pytest
```

## Project Structure

```
src/greet/
├── cli.py           # CLI entry point
├── core.py          # Greeting generation
├── languages.py     # Language definitions
├── fortunes.py      # Proverbs data
├── output.py        # Output formatting
└── renderers/       # Visual effects
    ├── figlet.py
    ├── cowsay.py
    ├── box.py
    └── effects.py
```

## Adding a New Language

Edit `src/greet/languages.py`:

```python
Language(
    code="xx",
    name="NewLanguage",
    banner_name="NEWLANGUAGE",
    greeting_template="Hello, {name}!",
    flag_emoji="🏳️"
)
```

No other code changes required!

## Help

```bash
uv run greet --help
```
