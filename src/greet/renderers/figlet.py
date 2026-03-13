import pyfiglet


def render_banner(label: str) -> str:
    """Render label as ASCII art banner via pyfiglet.

    Falls back to a plain header for non-ASCII (non-Latin) labels.
    """
    if label.isascii():
        return str(pyfiglet.figlet_format(label))
    return f"=== {label} ==="
