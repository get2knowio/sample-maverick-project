"""Click CLI entry point for the greet command."""

import sys

import click

from greet import __version__
from greet.core import OutputConfig, generate_all_greetings
from greet.output import create_console, render_all_greetings


@click.command()
@click.version_option(version=__version__, prog_name="greet")
@click.help_option("-h", "--help")
def main() -> None:
    """Multilingual greeting CLI tool.

    Display "Hello, World!" in multiple languages with ASCII art flourishes.
    """
    # Create output configuration with default options for User Story 1
    config = OutputConfig(
        languages=None,  # Show all languages
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
