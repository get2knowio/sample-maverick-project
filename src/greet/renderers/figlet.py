"""Figlet ASCII art banner rendering."""

import pyfiglet


def render_figlet_banner(text: str) -> str:
    """Render text as a figlet ASCII art banner.

    Args:
        text: The text to render as ASCII art

    Returns:
        Multi-line string containing the ASCII art banner
    """
    return str(pyfiglet.figlet_format(text))
