"""Rich Console wrapper and rendering functions for greeting output."""

from rich.console import Console

from greet.core import Greeting, OutputConfig
from greet.renderers.figlet import render_figlet_banner


def create_console(config: OutputConfig) -> Console:
    """Create a Rich Console instance configured according to OutputConfig.

    Args:
        config: Output configuration specifying color and other display options

    Returns:
        Configured Rich Console instance
    """
    return Console(
        force_terminal=config.use_color,
        no_color=not config.use_color,
        highlight=False,
    )


def render_greeting(greeting: Greeting, config: OutputConfig, console: Console) -> None:
    """Render a single greeting to the console.

    Args:
        greeting: The greeting to render
        config: Output configuration
        console: Rich Console instance to render to
    """
    # Render figlet banner if enabled
    if config.show_figlet:
        banner = render_figlet_banner(greeting.language.banner_name)
        console.print(banner, style="bold cyan")

    # Render the greeting text
    console.print(greeting.text, style="green")
    console.print()  # Empty line for spacing


def render_all_greetings(greetings: list[Greeting], config: OutputConfig, console: Console) -> None:
    """Render all greetings sequentially to the console.

    Args:
        greetings: List of greetings to render
        config: Output configuration
        console: Rich Console instance to render to
    """
    for greeting in greetings:
        render_greeting(greeting, config, console)
