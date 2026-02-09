"""Click CLI entry point for the greet command."""

import sys

import click

from greet import __version__
from greet.core import (
    OutputConfig,
    filter_languages,
    generate_all_greetings,
    generate_greeting,
    parse_language_filter,
    select_random_language,
)
from greet.fortunes import select_random_proverb
from greet.languages import LANGUAGES
from greet.output import create_console, render_all_greetings, render_fortune, render_greeting


@click.command()
@click.version_option(version=__version__, prog_name="greet")
@click.help_option("-h", "--help")
@click.option(
    "--languages",
    "-l",
    type=str,
    default=None,
    help=(
        "Comma-separated list of languages to display (e.g., 'english,french,spanish'). "
        "Valid languages: english, french, spanish, german, japanese, mandarin, arabic, "
        "hindi, swahili, portuguese. Omit to display all languages."
    ),
)
@click.option(
    "--no-figlet",
    is_flag=True,
    default=False,
    help=(
        "Disable ASCII art banners for language names. Use this for plain text output "
        "or when terminal doesn't support large ASCII art."
    ),
)
@click.option(
    "--no-color",
    is_flag=True,
    default=False,
    help=(
        "Disable terminal colors and produce plain text output. Useful for logging, "
        "piping to files, or terminals without color support. Overrides --rainbow and "
        "--party color features."
    ),
)
@click.option(
    "--random",
    is_flag=True,
    default=False,
    help=(
        "Display exactly one randomly selected language instead of all languages. "
        "Can be combined with --languages to select randomly from a filtered subset."
    ),
)
@click.option(
    "--name",
    type=str,
    default="World",
    help=(
        "Custom name to substitute in greetings instead of 'World' "
        "(e.g., --name 'Alice' produces 'Hello, Alice!'). "
        "Name is properly localized for each language."
    ),
)
@click.option(
    "--cowsay",
    is_flag=True,
    default=False,
    help=(
        "Wrap the entire output in a cowsay-style speech bubble with an ASCII animal. "
        "Adds whimsical flair to any greeting combination."
    ),
)
@click.option(
    "--party",
    is_flag=True,
    default=False,
    help=(
        "Enable party mode: adds emoji confetti, country flag emojis for each language, "
        "and randomized colors for extra celebration. Colors disabled if --no-color is used."
    ),
)
@click.option(
    "--fortune",
    is_flag=True,
    default=False,
    help=(
        "Append a random multilingual proverb or saying after the greetings. "
        "Adds cultural wisdom from around the world."
    ),
)
@click.option(
    "--all-at-once",
    is_flag=True,
    default=False,
    help=(
        "Display all greetings in a compact grid layout instead of sequential display. "
        "Grid adapts to terminal width automatically."
    ),
)
@click.option(
    "--typewriter",
    is_flag=True,
    default=False,
    help=(
        "Enable typewriter animation with character-by-character display. "
        "Creates a typing effect for dynamic visual appeal."
    ),
)
@click.option(
    "--rainbow",
    is_flag=True,
    default=False,
    help=(
        "Enable rainbow color cycling where each character cycles through rainbow colors. "
        "Disabled if --no-color is used."
    ),
)
@click.option(
    "--box",
    is_flag=True,
    default=False,
    help=(
        "Draw a decorative Unicode box border around each greeting. "
        "Works with or without --no-figlet for framed output."
    ),
)
def main(
    languages: str | None,
    no_figlet: bool,
    no_color: bool,
    random: bool,
    name: str,
    cowsay: bool,
    party: bool,
    fortune: bool,
    all_at_once: bool,
    typewriter: bool,
    rainbow: bool,
    box: bool,
) -> None:
    """Multilingual greeting CLI tool - Display "Hello, World!" in 10 languages with ASCII art.

    By default, displays greetings in all 10 supported languages (English, French,
    Spanish, German, Japanese, Mandarin, Arabic, Hindi, Swahili, Portuguese) with
    colorful ASCII art banners.

    \b
    Examples:
      greet                              # All languages with ASCII art
      greet -l french,spanish            # Only French and Spanish
      greet --name "Alice"               # Personalized greetings
      greet --random --cowsay            # Random greeting in speech bubble
      greet --party --fortune            # Celebration mode with proverb
      greet --no-color --no-figlet       # Plain text (for piping/logging)
      greet --all-at-once --box          # Grid layout with borders
      greet --typewriter --rainbow       # Animated rainbow effect

    \b
    Exit Codes:
      0 - Success
      1 - Invalid option or argument
      2 - Invalid language name specified
    """
    # Parse and validate language filter if provided
    language_list: list[str] | None = None
    if languages is not None:
        language_list = parse_language_filter(languages)

        # Validate that all requested languages are valid
        if language_list:
            # Filter to get valid languages
            valid_languages = filter_languages(language_list)

            # Check for invalid language names
            valid_names = {lang.name.lower() for lang in valid_languages}
            invalid_languages = [name for name in language_list if name.lower() not in valid_names]

            if invalid_languages:
                # Display error message with invalid languages and valid options
                available = ", ".join(sorted([lang.name for lang in LANGUAGES]))
                invalid_str = ", ".join(invalid_languages)
                click.echo(
                    f"Error: Invalid language name(s): {invalid_str}\nValid options: {available}",
                    err=True,
                )
                sys.exit(2)

    # Create output configuration with CLI options
    config = OutputConfig(
        languages=language_list,
        name=name,
        show_figlet=not no_figlet,
        use_color=not no_color,
        random_mode=random,
        cowsay=cowsay,
        party_mode=party,
        show_fortune=fortune,
        grid_layout=all_at_once,
        typewriter=typewriter,
        rainbow=rainbow,
        show_box=box,
    )

    # Create console
    console = create_console(config)

    # Handle random mode - select and display a single random language
    if random:
        # Select a random language from the filtered set (or all if no filter)
        random_language = select_random_language(config.languages)
        # Generate greeting for the selected language
        greeting = generate_greeting(random_language, config.name)
        # Render single greeting
        render_greeting(greeting, config, console)
    else:
        # Generate greetings for all languages
        greetings = generate_all_greetings(
            languages=config.languages,
            name=config.name,
        )
        # Render all greetings
        render_all_greetings(greetings, config, console)

    # Render fortune if enabled
    if fortune:
        proverb = select_random_proverb()
        render_fortune(proverb, config, console)

    # Ensure exit code 0 on success
    sys.exit(0)


if __name__ == "__main__":
    main()
