"""Rich Console wrapper and rendering functions for greeting output."""

from io import StringIO

from rich.console import Console

from greet.core import Greeting, OutputConfig
from greet.renderers.cowsay import wrap_in_cowsay
from greet.renderers.effects import add_confetti, random_color_style
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
    # If cowsay mode is enabled, capture output and wrap it
    if config.cowsay:
        # Create a temporary console to capture output
        output_buffer = StringIO()
        temp_console = Console(
            file=output_buffer,
            force_terminal=config.use_color,
            no_color=not config.use_color,
            highlight=False,
        )

        # Render figlet banner if enabled
        if config.show_figlet:
            banner = render_figlet_banner(greeting.language.banner_name)
            # Use random color for banner in party mode, otherwise bold cyan
            if config.party_mode and config.use_color:
                banner_style = f"bold {random_color_style()}"
            else:
                banner_style = "bold cyan"
            temp_console.print(banner, style=banner_style)

        # Prepare greeting text
        greeting_text = greeting.text

        # Add flag emoji in party mode
        if config.party_mode:
            greeting_text = f"{greeting.language.flag_emoji} {greeting_text}"

        # Add confetti in party mode
        if config.party_mode:
            greeting_text = add_confetti(greeting_text)

        # Render the greeting text with random color in party mode
        if config.party_mode and config.use_color:
            greeting_style = random_color_style()
        else:
            greeting_style = "green"

        temp_console.print(greeting_text, style=greeting_style)

        # Get the captured output
        captured_output = output_buffer.getvalue()

        # Wrap in cowsay and print to the real console
        cowsay_output = wrap_in_cowsay(captured_output.rstrip())
        console.print(cowsay_output)
    else:
        # Normal rendering without cowsay
        # Render figlet banner if enabled
        if config.show_figlet:
            banner = render_figlet_banner(greeting.language.banner_name)
            # Use random color for banner in party mode, otherwise bold cyan
            if config.party_mode and config.use_color:
                banner_style = f"bold {random_color_style()}"
            else:
                banner_style = "bold cyan"
            console.print(banner, style=banner_style)

        # Prepare greeting text
        greeting_text = greeting.text

        # Add flag emoji in party mode
        if config.party_mode:
            greeting_text = f"{greeting.language.flag_emoji} {greeting_text}"

        # Add confetti in party mode
        if config.party_mode:
            greeting_text = add_confetti(greeting_text)

        # Render the greeting text with random color in party mode
        if config.party_mode and config.use_color:
            greeting_style = random_color_style()
        else:
            greeting_style = "green"

        console.print(greeting_text, style=greeting_style)
        console.print()  # Empty line for spacing


def render_all_greetings(greetings: list[Greeting], config: OutputConfig, console: Console) -> None:
    """Render all greetings sequentially to the console.

    Args:
        greetings: List of greetings to render
        config: Output configuration
        console: Rich Console instance to render to
    """
    # If cowsay mode is enabled, capture all output and wrap it
    if config.cowsay:
        # Create a temporary console to capture output
        output_buffer = StringIO()
        temp_console = Console(
            file=output_buffer,
            force_terminal=config.use_color,
            no_color=not config.use_color,
            highlight=False,
        )

        # Render all greetings to the temporary console
        for greeting in greetings:
            render_greeting(greeting, config, temp_console)

        # Get the captured output
        captured_output = output_buffer.getvalue()

        # Wrap in cowsay and print to the real console
        cowsay_output = wrap_in_cowsay(captured_output.rstrip())
        console.print(cowsay_output)
    else:
        # Normal rendering without cowsay
        for greeting in greetings:
            render_greeting(greeting, config, console)
