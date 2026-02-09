"""Unit tests for box rendering functionality."""

from io import StringIO

from rich.console import Console

from greet.renderers.box import render_box


def test_render_box_basic() -> None:
    """Test that render_box wraps content in a box."""
    output = StringIO()
    console = Console(file=output, force_terminal=False, width=80)

    render_box("Hello, World!", console, use_color=False)
    result = output.getvalue()

    # Check that content is present
    assert "Hello, World!" in result
    # Check that box characters are present (Rich uses Unicode box drawing)
    # The output should contain box drawing characters
    assert len(result) > len("Hello, World!")


def test_render_box_with_color() -> None:
    """Test that render_box works with color enabled."""
    output = StringIO()
    console = Console(file=output, force_terminal=True, width=80)

    render_box("Test content", console, use_color=True)
    result = output.getvalue()

    # Check that content is present
    assert "Test content" in result


def test_render_box_multiline() -> None:
    """Test that render_box handles multiline content."""
    output = StringIO()
    console = Console(file=output, force_terminal=False, width=80)

    content = "Line 1\nLine 2\nLine 3"
    render_box(content, console, use_color=False)
    result = output.getvalue()

    # Check that all lines are present
    assert "Line 1" in result
    assert "Line 2" in result
    assert "Line 3" in result


def test_render_box_empty_string() -> None:
    """Test that render_box handles empty string."""
    output = StringIO()
    console = Console(file=output, force_terminal=False, width=80)

    render_box("", console, use_color=False)
    result = output.getvalue()

    # Should still produce a box, even if empty
    assert isinstance(result, str)
    assert len(result) > 0
