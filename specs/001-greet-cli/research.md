# Research: Greet CLI Implementation

**Feature**: 001-greet-cli
**Date**: 2026-01-16

## Technology Decisions

### CLI Framework: Click

**Decision**: Use Click as the CLI framework
**Rationale**:
- Industry standard for Python CLIs with excellent documentation
- Native support for option groups, boolean flags (`--no-color`), and value options (`--name NAME`)
- Built-in help generation and error handling
- Composable command structure if future expansion needed
**Alternatives Considered**:
- argparse: Standard library but verbose; lacks Click's decorator elegance
- Typer: Built on Click with type hints, but adds dependency layer without clear benefit for this scope
- Fire: Auto-generates CLI from functions, but less control over option naming conventions

### Terminal Formatting: Rich

**Decision**: Use Rich library for terminal output
**Rationale**:
- Comprehensive support for ANSI colors, styles, and Unicode box drawing
- Built-in `Console` class with `no_color` mode for `--no-color` support
- Native grid/table layouts for `--all-at-once` mode
- Handles terminal width detection automatically
- Active maintenance and excellent documentation
**Alternatives Considered**:
- Colorama: Colors only; no layout support
- Blessed/Curses: Lower-level, more complex for this use case
- Termcolor: Minimal; lacks Rich's layout capabilities

### ASCII Art Banners: pyfiglet

**Decision**: Use pyfiglet for figlet-style ASCII art
**Rationale**:
- Direct port of classic figlet with extensive font library
- Simple API: `pyfiglet.figlet_format("TEXT", font="standard")`
- Supports font selection if future customization desired
**Alternatives Considered**:
- art: Alternative ASCII art library, but pyfiglet has broader font compatibility
- Manual ASCII: Not scalable for 10+ language names

### Package Management: uv

**Decision**: Use uv for package and environment management
**Rationale**:
- Extremely fast (10-100x faster than pip)
- Deterministic builds with `uv.lock` lockfile
- Handles virtual environment creation automatically
- Modern Python packaging with PEP 517/518 support
- Single tool replaces pip, pip-tools, virtualenv, and pyenv
**Alternatives Considered**:
- pip + venv: Standard but slower; no lockfile by default
- Poetry: Full-featured but slower; heavier dependency
- PDM: Similar features to uv but less performant

### Testing: pytest

**Decision**: Use pytest with pytest-cov (run via `uv run pytest`)
**Rationale**:
- De facto standard for Python testing
- Fixtures support clean test isolation
- Click has `CliRunner` for testing CLI commands
- pytest-cov integrates coverage reporting
**Alternatives Considered**:
- unittest: Standard library but more verbose; less ecosystem support

## Best Practices Research

### Click CLI Patterns

**Option Naming**:
- Boolean flags use `--flag/--no-flag` pattern or `is_flag=True`
- Value options use `--option VALUE` pattern
- Short options with `-x` single character

**Example pattern for greet**:
```python
@click.command()
@click.option('--languages', '-l', default=None, help='Comma-separated language filter')
@click.option('--no-figlet', is_flag=True, help='Disable ASCII art banners')
@click.option('--no-color', is_flag=True, help='Disable terminal colors')
@click.option('--random', is_flag=True, help='Show one random language')
@click.option('--cowsay', is_flag=True, help='Wrap in cowsay bubble')
@click.option('--party', is_flag=True, help='Enable party mode')
@click.option('--fortune', is_flag=True, help='Append random proverb')
@click.option('--name', default='World', help='Custom name for greeting')
@click.option('--all-at-once', is_flag=True, help='Grid layout display')
@click.option('--typewriter', is_flag=True, help='Typing animation')
@click.option('--rainbow', is_flag=True, help='Rainbow color cycling')
@click.option('--box', is_flag=True, help='Unicode box around greetings')
def greet(...):
    pass
```

### Rich Output Patterns

**Console with no_color**:
```python
from rich.console import Console
console = Console(no_color=no_color_flag, force_terminal=True)
```

**Grid layout** (for `--all-at-once`):
```python
from rich.table import Table
from rich.columns import Columns
```

**Box drawing** (for `--box`):
```python
from rich.panel import Panel
```

### Language Data Structure

**Decision**: Use dataclass or TypedDict for language definitions
**Structure**:
```python
@dataclass
class Language:
    code: str           # e.g., "en", "fr"
    name: str           # e.g., "English", "French"
    banner_name: str    # e.g., "ENGLISH", "FRANÇAIS"
    greeting: str       # e.g., "Hello, {name}!"
    flag_emoji: str     # e.g., "🇺🇸", "🇫🇷"
```

**Greeting Template**: Use `{name}` placeholder for string formatting

### Authentic Greetings Research

| Language | Greeting | Banner | Flag |
|----------|----------|--------|------|
| English | Hello, {name}! | ENGLISH | 🇬🇧 |
| French | Bonjour, {name} ! | FRANÇAIS | 🇫🇷 |
| Spanish | ¡Hola, {name}! | ESPAÑOL | 🇪🇸 |
| German | Hallo, {name}! | DEUTSCH | 🇩🇪 |
| Japanese | こんにちは、{name}！ | 日本語 | 🇯🇵 |
| Mandarin | 你好，{name}！ | 中文 | 🇨🇳 |
| Arabic | !مرحبا، {name} | العربية | 🇸🇦 |
| Hindi | नमस्ते, {name}! | हिन्दी | 🇮🇳 |
| Swahili | Habari, {name}! | KISWAHILI | 🇰🇪 |
| Portuguese | Olá, {name}! | PORTUGUÊS | 🇧🇷 |

**Note**: Japanese banner uses Japanese characters (日本語) as figlet may not render well; fallback to "JAPANESE" if needed. Same consideration for Mandarin, Arabic, Hindi.

### Cowsay Implementation

**Decision**: Implement simple cowsay-style bubble internally
**Rationale**: Avoids external dependency; bubble + animal is straightforward
**Pattern**:
```
 _______________
< Hello, World! >
 ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

### Typewriter Animation

**Pattern**: Use `time.sleep()` with small delay between characters
```python
import time
for char in text:
    console.print(char, end='')
    time.sleep(0.03)  # 30ms delay
```

### Rainbow Effect

**Pattern**: Cycle through Rich color styles per character
```python
colors = ['red', 'orange1', 'yellow', 'green', 'blue', 'purple']
for i, char in enumerate(text):
    console.print(char, style=colors[i % len(colors)], end='')
```

## Dependency Versions

| Package | Minimum Version | Notes |
|---------|-----------------|-------|
| Python | 3.10 | Required for modern type hints |
| click | 8.0 | Stable, widely used |
| rich | 13.0 | Latest major with full feature set |
| pyfiglet | 0.8 | Stable release |
| pytest | 7.0 | Modern fixtures support (dev dependency) |
| pytest-cov | 4.0 | Coverage integration (dev dependency) |
| mypy | 1.0 | Type checking (dev dependency) |
| ruff | 0.1 | Linting and formatting (dev dependency) |

## Project Setup Commands

```bash
# Initialize project
uv init greet-cli
cd greet-cli

# Add runtime dependencies
uv add click rich pyfiglet

# Add dev dependencies
uv add --dev pytest pytest-cov mypy ruff

# Sync all dependencies
uv sync

# Run tests
uv run pytest

# Type check
uv run mypy --strict src/

# Lint and format
uv run ruff check
uv run ruff format
```

## Open Questions Resolved

All technical questions resolved through research. No NEEDS CLARIFICATION remaining.
