"""Click CLI entry point for the greet command."""

import click

from greet import __version__


@click.command()
@click.version_option(version=__version__, prog_name="greet")
@click.help_option("-h", "--help")
def main() -> None:
    """Multilingual greeting CLI tool.

    Display "Hello, World!" in multiple languages with ASCII art flourishes.
    """
    click.echo("Greet CLI v" + __version__)
    click.echo("Basic CLI skeleton - functionality to be implemented in later phases.")


if __name__ == "__main__":
    main()
