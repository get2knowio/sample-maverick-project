"""Visual effects for party mode and decorative elements."""

import random


def add_confetti(text: str) -> str:
    """Add emoji confetti decorations around text.

    Args:
        text: The text to decorate with confetti

    Returns:
        Text with confetti emojis added
    """
    confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
    # Add random confetti before and after
    confetti_before = "".join(random.choice(confetti_emojis) for _ in range(3))
    confetti_after = "".join(random.choice(confetti_emojis) for _ in range(3))
    return f"{confetti_before} {text} {confetti_after}"


def random_color_style() -> str:
    """Generate a random color style string for Rich formatting.

    Returns:
        A random color name suitable for Rich style strings
    """
    colors = [
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "bright_red",
        "bright_green",
        "bright_yellow",
        "bright_blue",
        "bright_magenta",
        "bright_cyan",
    ]
    return random.choice(colors)
