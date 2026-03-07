# Greet CLI — Product Requirements Document

**Author:** Product Team
**Date:** 2026-01-15
**Status:** Draft — ready for engineering review

## Vision

We want a fun, lightweight CLI tool called `greet` that says "Hello, World!" in
a bunch of different languages.  Think of it as the modern version of
`cowsay` meets Rosetta Stone — something a developer can install in two seconds,
run once, and smile.  Ideally it should feel *delightful* when you run it in
a terminal for the first time.

## Target Users

- Developers setting up a new terminal / shell and wanting to test Unicode + color support
- Educators demonstrating internationalization concepts
- Anyone who likes fun CLI toys

## What We Want (roughly)

1. **Multilingual greetings** — at least 10 languages.  English, French, Spanish,
   German, Japanese, Mandarin Chinese, Arabic, Hindi, Swahili, Portuguese.
   The greetings should be authentic, not Google Translate garbage.

2. **Looks cool** — big ASCII art banners for each language name (figlet-style),
   colors in the terminal, maybe some emoji sprinkled in.

3. **Filterable** — user should be able to pick which languages to show.  Something
   like `greet --languages french,spanish` or `-l french`.

4. **Personalizable** — let the user replace "World" with their own name.
   `greet --name Alice` → "Hello, Alice!" / "Bonjour, Alice!" etc.

5. **Fun extras** (nice to have, not blocking launch):
   - Cowsay mode (wrap output in a speech bubble with an ASCII cow)
   - Party mode (emoji confetti, country flags, random colors)
   - Fortune mode (random proverb/saying after the greetings)
   - Typewriter animation
   - Rainbow colors
   - Box-drawing mode around each greeting

6. **Plain-text fallback** — `--no-color --no-figlet` should produce clean output
   that works in CI logs, pipes, etc.

7. **Easy to install** — standard `pip install` or `uv add`, single entry point.

## Non-Goals

- No web UI, no REST API, no daemon mode
- No translation service integration (all greetings are baked in)
- No plugin system for adding languages at runtime (just a data list)
- We're not building the next `fortune` — keep the proverb list small (~20)

## Technical Constraints

- Python 3.10+
- Click for CLI framework
- Rich for terminal rendering
- pyfiglet for ASCII art
- Should work on macOS, Linux, and Windows Terminal
- No external API calls — everything offline
- Keep it simple: one package, one entry point

## Open Questions

- Should `--random` pick one language or a random subset?  Leaning toward exactly one.
- Grid layout (`--all-at-once`) — is this worth the complexity?  Maybe defer.
- How should right-to-left languages (Arabic) render in figlet banners?

## Success Looks Like

- `pip install greet-cli && greet` works out of the box
- Running `greet` in a modern terminal produces a colorful, impressive output
- Adding a new language means adding one entry to a data structure, nothing else
- The whole thing is under 500 lines of code (excluding tests)

---

*This document is intentionally high-level.  Engineering should use this as input
to generate a detailed flight plan with concrete work units, acceptance criteria,
and file-level scope.*
