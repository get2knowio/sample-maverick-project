RAINBOW_COLORS: list[str] = ["red", "yellow", "green", "cyan", "blue", "magenta"]


def apply_rainbow(text: str) -> str:
    """Apply rainbow colors to text using Rich markup tags.

    Cycles through at least 3 distinct colors, one per character.
    """
    if not text:
        return text
    parts: list[str] = []
    for i, char in enumerate(text):
        color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
        parts.append(f"[{color}]{char}[/{color}]")
    return "".join(parts)
