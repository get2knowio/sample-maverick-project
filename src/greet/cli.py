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
from greet.languages import LANGUAGES
from greet.output import create_console, render_all_greetings, render_greeting


@click.command()
@click.version_option(version=__version__, prog_name="greet")
@click.help_option("-h", "--help")
@click.option(
    "--languages",
    "-l",
    type=str,
    default=None,
    help="Comma-separated list of languages to display (e.g., 'english,french,spanish')",
)
@click.option(
    "--no-figlet",
    is_flag=True,
    default=False,
    help="Disable ASCII art banners",
)
@click.option(
    "--no-color",
    is_flag=True,
    default=False,
    help="Disable terminal colors",
)
@click.option(
    "--random",
    is_flag=True,
    default=False,
    help="Display exactly one randomly selected language",
)
def main(languages: str | None, no_figlet: bool, no_color: bool, random: bool) -> None:
    """Multilingual greeting CLI tool.

    Display "Hello, World!" in multiple languages with ASCII art flourishes.
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
        name="World",
        show_figlet=not no_figlet,
        use_color=not no_color,
        random_mode=random,
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

    # Ensure exit code 0 on success
    sys.exit(0)


if __name__ == "__main__":
    main()
