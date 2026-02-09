"""Visual effects for party mode and decorative elements."""

import random
import sys
import time


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


def typewriter_print(text: str, delay: float = 0.05) -> None:
    """Print text with character-by-character typewriter animation.

    Args:
        text: The text to print with animation
        delay: Delay in seconds between each character (default: 0.05)
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def rainbow_print(text: str, use_color: bool = True) -> str:
    """Apply rainbow color cycling to each character in text.

    Args:
        text: The text to colorize
        use_color: Whether to apply colors (respects --no-color flag)

    Returns:
        Text with rainbow color markup for Rich Console (or plain text if use_color is False)
    """
    if not use_color:
        return text

    rainbow_colors = [
        "red",
        "bright_red",
        "yellow",
        "bright_yellow",
        "green",
        "bright_green",
        "cyan",
        "bright_cyan",
        "blue",
        "bright_blue",
        "magenta",
        "bright_magenta",
    ]

    result_parts: list[str] = []
    for i, char in enumerate(text):
        color = rainbow_colors[i % len(rainbow_colors)]
        if char.strip():  # Only colorize non-whitespace characters
            result_parts.append(f"[{color}]{char}[/{color}]")
        else:
            result_parts.append(char)

    return "".join(result_parts)
