# Data Model: Greet CLI

**Feature**: 001-greet-cli
**Date**: 2026-01-16

## Entities

### Language

Represents a supported language for greetings.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| code | str | Yes | ISO 639-1 code (e.g., "en", "fr") |
| name | str | Yes | Display name (e.g., "English", "French") |
| banner_name | str | Yes | Text for ASCII art banner (e.g., "ENGLISH", "FRANÇAIS") |
| greeting_template | str | Yes | Greeting with `{name}` placeholder (e.g., "Hello, {name}!") |
| flag_emoji | str | Yes | Country flag emoji (e.g., "🇬🇧", "🇫🇷") |

**Validation Rules**:
- `code` must be unique across all languages
- `name` must be unique (used for `--languages` filter matching)
- `greeting_template` must contain exactly one `{name}` placeholder
- `flag_emoji` must be a valid emoji sequence

**Identity**: Languages are identified by `code` (primary) and `name` (for user-facing filter)

### Proverb

Represents a multilingual proverb or saying for the `--fortune` feature.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | str | Yes | The proverb text |
| language | str | Yes | Language name (matches Language.name) |
| translation | str | No | English translation if not in English |

**Validation Rules**:
- `text` must be non-empty
- `language` should reference a known language (soft reference, not enforced)

### OutputConfig

Configuration object capturing all CLI options for a single execution.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| languages | list[str] | None | Filter to specific languages (None = all) |
| name | str | "World" | Name to substitute in greetings |
| show_figlet | bool | True | Show ASCII art banners |
| use_color | bool | True | Enable terminal colors |
| random_mode | bool | False | Show only one random language |
| cowsay | bool | False | Wrap output in cowsay bubble |
| party_mode | bool | False | Add confetti, flags, random colors |
| show_fortune | bool | False | Append random proverb |
| grid_layout | bool | False | Display in grid (--all-at-once) |
| typewriter | bool | False | Character-by-character animation |
| rainbow | bool | False | Rainbow color cycling |
| show_box | bool | False | Unicode box around each greeting |

**Derived from CLI options**: This object is constructed from Click option values.

### Greeting

A rendered greeting ready for display.

| Field | Type | Description |
|-------|------|-------------|
| language | Language | The source language |
| text | str | Formatted greeting with name substituted |
| banner | str | Optional figlet banner text (if enabled) |

**State**: Greeting is immutable once created.

## Relationships

```
┌─────────────┐     ┌─────────────┐
│   Language  │     │   Proverb   │
│  (10 items) │     │ (10+ items) │
└──────┬──────┘     └──────┬──────┘
       │                   │
       │ used by           │ selected by
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│  Greeting   │◄────│OutputConfig │
│  (rendered) │     │ (CLI opts)  │
└─────────────┘     └─────────────┘
```

## Data Storage

**In-Memory Only**: All data is stored as Python module-level constants.

- `languages.py`: Contains `LANGUAGES: list[Language]` with all 10 language definitions
- `fortunes.py`: Contains `PROVERBS: list[Proverb]` with 10-20 multilingual sayings

**No External Storage**: No database, files, or configuration files required at runtime.

## Extensibility Pattern

To add a new language (per FR-016):

1. Add a new `Language` entry to `LANGUAGES` list in `languages.py`
2. No logic changes required
3. The new language automatically:
   - Appears in default output
   - Becomes available for `--languages` filter
   - Works with all rendering modes

## Sample Data

### Languages (Initial 10)

```python
LANGUAGES = [
    Language(code="en", name="English", banner_name="ENGLISH",
             greeting_template="Hello, {name}!", flag_emoji="🇬🇧"),
    Language(code="fr", name="French", banner_name="FRANÇAIS",
             greeting_template="Bonjour, {name} !", flag_emoji="🇫🇷"),
    Language(code="es", name="Spanish", banner_name="ESPAÑOL",
             greeting_template="¡Hola, {name}!", flag_emoji="🇪🇸"),
    Language(code="de", name="German", banner_name="DEUTSCH",
             greeting_template="Hallo, {name}!", flag_emoji="🇩🇪"),
    Language(code="ja", name="Japanese", banner_name="JAPANESE",
             greeting_template="こんにちは、{name}！", flag_emoji="🇯🇵"),
    Language(code="zh", name="Mandarin", banner_name="MANDARIN",
             greeting_template="你好，{name}！", flag_emoji="🇨🇳"),
    Language(code="ar", name="Arabic", banner_name="ARABIC",
             greeting_template="مرحبا، {name}!", flag_emoji="🇸🇦"),
    Language(code="hi", name="Hindi", banner_name="HINDI",
             greeting_template="नमस्ते, {name}!", flag_emoji="🇮🇳"),
    Language(code="sw", name="Swahili", banner_name="KISWAHILI",
             greeting_template="Habari, {name}!", flag_emoji="🇰🇪"),
    Language(code="pt", name="Portuguese", banner_name="PORTUGUÊS",
             greeting_template="Olá, {name}!", flag_emoji="🇧🇷"),
]
```

### Proverbs (Sample)

```python
PROVERBS = [
    Proverb(text="A journey of a thousand miles begins with a single step.",
            language="English"),
    Proverb(text="Petit à petit, l'oiseau fait son nid.",
            language="French", translation="Little by little, the bird builds its nest."),
    Proverb(text="No hay mal que por bien no venga.",
            language="Spanish", translation="There is no bad from which good doesn't come."),
    # ... additional proverbs
]
```
