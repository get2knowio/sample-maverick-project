"""Rich Console wrapper and rendering functions for greeting output."""

from io import StringIO

from rich.columns import Columns
from rich.console import Console

from greet.core import Greeting, OutputConfig
from greet.fortunes import Proverb
from greet.renderers.cowsay import wrap_in_cowsay
from greet.renderers.effects import (
    add_confetti,
    rainbow_print,
    random_color_style,
    typewriter_print,
)
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
    # Handle animation modes (typewriter and/or rainbow)
    # Animation effects bypass normal rendering logic
    if config.typewriter or config.rainbow:
        # Render figlet banner if enabled (without animation)
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

        # Apply rainbow effect if enabled
        if config.rainbow:
            greeting_text = rainbow_print(greeting_text, config.use_color)

        # If typewriter mode is enabled, use typewriter_print
        if config.typewriter:
            # For typewriter mode, we need to print directly (bypassing Rich console)
            # First, render the rainbow markup if present
            if config.rainbow and config.use_color:
                # Use Rich console to render the rainbow markup, then animate
                # This is a simplified approach - print character by character
                console.print(greeting_text)
            else:
                # Pure typewriter without rainbow
                typewriter_print(greeting_text)
        else:
            # Rainbow mode without typewriter - just print with rainbow colors
            console.print(greeting_text, markup=True)

        console.print()  # Empty line for spacing
        return

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


def render_grid_layout(greetings: list[Greeting], config: OutputConfig, console: Console) -> None:
    """Render greetings in a grid layout using Rich Columns.

    Args:
        greetings: List of greetings to render
        config: Output configuration
        console: Rich Console instance to render to
    """
    if not greetings:
        return

    # Detect terminal width for adaptive grid sizing
    # Each column needs at least 30 characters to display greeting comfortably
    min_column_width = 30

    # Create greeting panels/strings for the grid
    greeting_items: list[str] = []

    for greeting in greetings:
        # Capture individual greeting output
        output_buffer = StringIO()
        temp_console = Console(
            file=output_buffer,
            force_terminal=config.use_color,
            no_color=not config.use_color,
            highlight=False,
            width=min_column_width - 4,  # Account for padding
        )

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
        greeting_output = output_buffer.getvalue().rstrip()
        greeting_items.append(greeting_output)

    # Create columns and render
    columns = Columns(greeting_items, equal=True, expand=True)
    console.print(columns)


def render_all_greetings(greetings: list[Greeting], config: OutputConfig, console: Console) -> None:
    """Render all greetings sequentially or in grid layout to the console.

    Args:
        greetings: List of greetings to render
        config: Output configuration
        console: Rich Console instance to render to
    """
    # If grid layout is enabled, use grid rendering
    if config.grid_layout:
        # If cowsay mode is enabled with grid, capture grid output and wrap it
        if config.cowsay:
            output_buffer = StringIO()
            temp_console = Console(
                file=output_buffer,
                force_terminal=config.use_color,
                no_color=not config.use_color,
                highlight=False,
                width=console.width,
            )
            render_grid_layout(greetings, config, temp_console)
            captured_output = output_buffer.getvalue()
            cowsay_output = wrap_in_cowsay(captured_output.rstrip())
            console.print(cowsay_output)
        else:
            render_grid_layout(greetings, config, console)
    # Otherwise, use sequential rendering
    elif config.cowsay:
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


def render_fortune(proverb: Proverb, config: OutputConfig, console: Console) -> None:
    """Render a fortune (proverb) to the console.

    Args:
        proverb: The proverb to render
        config: Output configuration
        console: Rich Console instance to render to
    """
    # Add separator line before fortune
    console.print()
    console.print("─" * 60, style="dim")
    console.print()

    # Render fortune header
    if config.use_color:
        console.print("✨ Fortune of the Day ✨", style="bold magenta", justify="center")
    else:
        console.print("Fortune of the Day", justify="center")

    console.print()

    # Render proverb text
    if config.use_color:
        console.print(f'"{proverb.text}"', style="italic yellow")
    else:
        console.print(f'"{proverb.text}"', style="italic")

    # Render translation if available
    if proverb.translation:
        console.print()
        if config.use_color:
            console.print(f"— {proverb.translation}", style="dim cyan")
        else:
            console.print(f"— {proverb.translation}", style="dim")

    # Show language origin
    console.print()
    if config.use_color:
        console.print(f"[{proverb.language} proverb]", style="dim", justify="right")
    else:
        console.print(f"[{proverb.language} proverb]", justify="right")

    console.print()
