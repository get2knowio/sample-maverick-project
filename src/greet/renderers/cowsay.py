"""Cowsay-style speech bubble wrapper for output."""


def wrap_in_cowsay(text: str) -> str:
    """Wrap text in a cowsay-style speech bubble with ASCII cow.

    Args:
        text: Text to wrap in the speech bubble (can be multiline)

    Returns:
        Formatted string with text in speech bubble and ASCII cow below
    """
    # Split text into lines
    lines = text.split("\n") if text else [""]

    # Calculate the maximum line width
    max_width = max((len(line) for line in lines), default=0)

    # Build the speech bubble
    bubble_parts: list[str] = []

    # Top border
    bubble_parts.append(" " + "_" * (max_width + 2))

    # Content lines with borders
    if len(lines) == 1:
        # Single line - use < and > borders
        bubble_parts.append(f"< {lines[0].ljust(max_width)} >")
    else:
        # Multiple lines - use different borders for first, middle, and last lines
        for i, line in enumerate(lines):
            padded_line = line.ljust(max_width)
            if i == 0:
                # First line
                bubble_parts.append(f"/ {padded_line} \\")
            elif i == len(lines) - 1:
                # Last line
                bubble_parts.append(f"\\ {padded_line} /")
            else:
                # Middle lines
                bubble_parts.append(f"| {padded_line} |")

    # Bottom border
    bubble_parts.append(" " + "-" * (max_width + 2))

    # Add the ASCII cow
    cow = [
        "        \\   ^__^",
        "         \\  (oo)\\_______",
        "            (__)\\       )\\/\\",
        "                ||----w |",
        "                ||     ||",
    ]

    # Combine bubble and cow
    result = "\n".join(bubble_parts) + "\n" + "\n".join(cow)

    return result
