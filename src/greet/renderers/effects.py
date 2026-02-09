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

    # Split text into grapheme clusters to avoid breaking multi-codepoint emojis
    # This handles flag emojis (regional indicator pairs) and other complex emojis
    import re

    # Pattern matches:
    # - Flag emojis: two consecutive regional indicator symbols (U+1F1E6 to U+1F1FF)
    # - Emojis with variation selectors (e.g., ️)
    # - Zero-width joiner sequences (families, etc.)
    # - Single characters as fallback
    flag_pattern = re.compile(
        r"(?:[\U0001F1E6-\U0001F1FF]{2}|"  # Regional indicator pairs (flags)
        r"[\U0001F300-\U0001F9FF][\uFE00-\uFE0F\u200D\U0001F3FB-\U0001F3FF]*|"
        r".)",  # Single character fallback
        re.UNICODE | re.DOTALL,
    )
    graphemes = flag_pattern.findall(text)

    result_parts: list[str] = []
    for i, grapheme in enumerate(graphemes):
        color = rainbow_colors[i % len(rainbow_colors)]
        if grapheme.strip():  # Only colorize non-whitespace characters
            result_parts.append(f"[{color}]{grapheme}[/{color}]")
        else:
            result_parts.append(grapheme)

    return "".join(result_parts)
