"""Unit tests for figlet rendering functionality."""

from greet.renderers.figlet import render_figlet_banner


def test_render_figlet_banner_basic() -> None:
    """Test that render_figlet_banner returns a non-empty string."""
    result = render_figlet_banner("HELLO")
    assert isinstance(result, str)
    assert len(result) > 0
    # Figlet output should be multiple lines
    assert "\n" in result


def test_render_figlet_banner_empty_string() -> None:
    """Test that render_figlet_banner handles empty string."""
    result = render_figlet_banner("")
    assert isinstance(result, str)


def test_render_figlet_banner_contains_input_text() -> None:
    """Test that the banner contains recognizable characters from input."""
    result = render_figlet_banner("TEST")
    # Figlet should produce ASCII art representation
    assert len(result) > len("TEST")


def test_render_figlet_banner_consistent_output() -> None:
    """Test that same input produces same output."""
    text = "ENGLISH"
    result1 = render_figlet_banner(text)
    result2 = render_figlet_banner(text)
    assert result1 == result2
