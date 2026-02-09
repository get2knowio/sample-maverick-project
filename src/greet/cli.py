"""Click CLI entry point for the greet command."""

import sys

import click

from greet import __version__
from greet.core import OutputConfig, filter_languages, generate_all_greetings, parse_language_filter
from greet.languages import LANGUAGES
from greet.output import create_console, render_all_greetings


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
def main(languages: str | None) -> None:
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

    # Create output configuration with default options for User Story 1
    config = OutputConfig(
        languages=language_list,
        name="World",
        show_figlet=True,
        use_color=True,
    )

    # Generate greetings for all languages
    greetings = generate_all_greetings(
        languages=config.languages,
        name=config.name,
    )

    # Create console and render all greetings
    console = create_console(config)
    render_all_greetings(greetings, config, console)

    # Ensure exit code 0 on success
    sys.exit(0)


if __name__ == "__main__":
    main()
