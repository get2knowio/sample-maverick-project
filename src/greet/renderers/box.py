"""Unicode box drawing for greeting decorations."""

from rich.console import Console
from rich.panel import Panel


def render_box(content: str, console: Console, use_color: bool = True) -> None:
    """Render content wrapped in a decorative Unicode box.

    Uses Rich Panel for clean Unicode box drawing with proper alignment.

    Args:
        content: The text content to wrap in a box
        console: Rich Console instance to render to
        use_color: Whether to use colors for the box border
    """
    # Create a panel with the content
    # Use cyan border in color mode, otherwise plain box
    if use_color:
        panel = Panel(
            content,
            border_style="cyan",
            expand=False,
            padding=(0, 1),
        )
    else:
        panel = Panel(
            content,
            expand=False,
            padding=(0, 1),
        )

    console.print(panel)
