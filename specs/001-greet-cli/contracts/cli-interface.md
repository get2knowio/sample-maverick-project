# CLI Interface Contract: greet

**Feature**: 001-greet-cli
**Date**: 2026-01-16

## Command

```
greet [OPTIONS]
```

## Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--languages` | `-l` | STRING | None | Comma-separated list of languages to display |
| `--name` | | STRING | "World" | Custom name for personalized greetings |
| `--no-figlet` | | FLAG | False | Disable ASCII art banners |
| `--no-color` | | FLAG | False | Disable terminal colors (plain text) |
| `--random` | | FLAG | False | Display one randomly selected language |
| `--cowsay` | | FLAG | False | Wrap output in cowsay-style bubble |
| `--party` | | FLAG | False | Enable party mode (confetti, flags, random colors) |
| `--fortune` | | FLAG | False | Append random multilingual proverb |
| `--all-at-once` | | FLAG | False | Display greetings in grid layout |
| `--typewriter` | | FLAG | False | Animate output character by character |
| `--rainbow` | | FLAG | False | Cycle through rainbow colors |
| `--box` | | FLAG | False | Draw Unicode box around each greeting |
| `--help` | `-h` | FLAG | | Show help message and exit |
| `--version` | | FLAG | | Show version and exit |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Invalid option or argument |
| 2 | Invalid language specified |

## Output Format

### Standard Output (stdout)

All greeting content is written to stdout.

**Default format** (with figlet and colors):
```
[FIGLET BANNER: LANGUAGE_NAME]
[Colored greeting text]

[FIGLET BANNER: NEXT_LANGUAGE]
[Colored greeting text]
...
```

**Plain text format** (`--no-color --no-figlet`):
```
Hello, World!
Bonjour, le monde !
¡Hola, Mundo!
...
```

### Standard Error (stderr)

Error messages are written to stderr.

```
Error: Invalid language 'klingon'. Valid languages: english, french, spanish, german, japanese, mandarin, arabic, hindi, swahili, portuguese
```

## Option Interactions

### Combinable Options

All options can be combined freely. Specific behaviors:

| Combination | Behavior |
|------------|----------|
| `--random` + `--languages` | Random selection from filtered list only |
| `--cowsay` + `--all-at-once` | Grid wrapped in single cowsay bubble |
| `--typewriter` + `--all-at-once` | Grid animated progressively |
| `--rainbow` + `--no-color` | `--no-color` takes precedence (no colors) |
| `--box` + `--no-figlet` | Boxes shown, banners hidden |
| `--party` + `--no-color` | Flags shown, colors disabled |

### Mutually Exclusive (Soft)

None. All options are designed to work together.

## Examples

### Basic Usage

```bash
# Display all greetings with figlet banners
greet

# Display specific languages
greet -l french,spanish,japanese

# Personalized greeting
greet --name "Alice"

# Plain text output (for piping/logging)
greet --no-color --no-figlet
```

### Fun Modes

```bash
# Random single greeting with cowsay
greet --random --cowsay

# Party mode with fortune
greet --party --fortune

# Animated rainbow typewriter
greet --typewriter --rainbow
```

### Combined Options

```bash
# Personalized French greeting in a box
greet -l french --name "Marie" --box

# Grid layout with party mode
greet --all-at-once --party

# Plain random greeting
greet --random --no-figlet --no-color
```

## Language Names

Valid values for `--languages` option (case-insensitive):

- `english`
- `french`
- `spanish`
- `german`
- `japanese`
- `mandarin`
- `arabic`
- `hindi`
- `swahili`
- `portuguese`

## Version String Format

```
greet, version X.Y.Z
```
