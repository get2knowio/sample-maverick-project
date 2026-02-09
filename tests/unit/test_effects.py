"""Tests for the effects module."""

import random
from io import StringIO
from unittest.mock import patch

from greet.renderers.effects import (
    add_confetti,
    rainbow_print,
    random_color_style,
    typewriter_print,
)


class TestAddConfetti:
    """Tests for the add_confetti function."""

    def test_add_confetti_adds_emojis(self) -> None:
        """Test that add_confetti adds emoji confetti around text."""
        text = "Hello, World!"
        result = add_confetti(text)

        # Check that result contains the original text
        assert text in result

        # Check that result is longer than original (has confetti added)
        assert len(result) > len(text)

        # Check that result has emojis before and after the text
        assert result.index(text) > 0  # Something before the text
        assert result.rindex(text) + len(text) < len(result)  # Something after

    def test_add_confetti_uses_confetti_emojis(self) -> None:
        """Test that add_confetti uses confetti emoji characters."""
        confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
        text = "Test"
        result = add_confetti(text)

        # Check that at least one confetti emoji is in the result
        assert any(emoji in result for emoji in confetti_emojis)

    def test_add_confetti_deterministic_with_seed(self) -> None:
        """Test that add_confetti produces consistent output with same seed."""
        text = "Hello"

        # Set seed and get result
        random.seed(42)
        result1 = add_confetti(text)

        # Reset to same seed and get result again
        random.seed(42)
        result2 = add_confetti(text)

        # Results should be identical
        assert result1 == result2

    def test_add_confetti_with_empty_string(self) -> None:
        """Test that add_confetti works with empty string."""
        result = add_confetti("")

        # Should still add confetti even with empty text
        assert len(result) > 0


class TestRandomColorStyle:
    """Tests for the random_color_style function."""

    def test_random_color_style_returns_valid_color(self) -> None:
        """Test that random_color_style returns a valid color name."""
        valid_colors = [
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

        # Call multiple times to increase confidence
        for _ in range(10):
            color = random_color_style()
            assert color in valid_colors

    def test_random_color_style_returns_string(self) -> None:
        """Test that random_color_style returns a string."""
        color = random_color_style()
        assert isinstance(color, str)

    def test_random_color_style_deterministic_with_seed(self) -> None:
        """Test that random_color_style produces consistent output with same seed."""
        # Set seed and get result
        random.seed(42)
        color1 = random_color_style()

        # Reset to same seed and get result again
        random.seed(42)
        color2 = random_color_style()

        # Results should be identical
        assert color1 == color2

    def test_random_color_style_can_vary(self) -> None:
        """Test that random_color_style can produce different colors."""
        # Get many colors and check if they vary
        colors = {random_color_style() for _ in range(50)}

        # Should have more than one unique color
        assert len(colors) > 1


class TestTypewriterPrint:
    """Tests for the typewriter_print function."""

    @patch("sys.stdout", new_callable=StringIO)
    @patch("time.sleep")
    def test_typewriter_print_outputs_text(self, mock_sleep: object, mock_stdout: StringIO) -> None:
        """Test that typewriter_print outputs the text character by character."""
        text = "Hello"
        typewriter_print(text)

        # Check that the text appears in stdout
        output = mock_stdout.getvalue()
        assert "Hello" in output

    @patch("sys.stdout", new_callable=StringIO)
    @patch("time.sleep")
    def test_typewriter_print_adds_newline(self, mock_sleep: object, mock_stdout: StringIO) -> None:
        """Test that typewriter_print adds a newline at the end."""
        text = "Test"
        typewriter_print(text)

        output = mock_stdout.getvalue()
        assert output.endswith("\n")

    @patch("sys.stdout", new_callable=StringIO)
    @patch("time.sleep")
    def test_typewriter_print_calls_sleep(self, mock_sleep: object, mock_stdout: StringIO) -> None:
        """Test that typewriter_print calls sleep for animation."""
        text = "Hi"
        typewriter_print(text, delay=0.1)

        # Should call sleep once per character
        assert mock_sleep.call_count == len(text)  # type: ignore

    @patch("sys.stdout", new_callable=StringIO)
    @patch("time.sleep")
    def test_typewriter_print_empty_string(self, mock_sleep: object, mock_stdout: StringIO) -> None:
        """Test that typewriter_print handles empty string."""
        typewriter_print("")

        output = mock_stdout.getvalue()
        assert output == "\n"

    @patch("sys.stdout", new_callable=StringIO)
    @patch("time.sleep")
    def test_typewriter_print_with_custom_delay(
        self, mock_sleep: object, mock_stdout: StringIO
    ) -> None:
        """Test that typewriter_print respects custom delay."""
        text = "X"
        custom_delay = 0.2
        typewriter_print(text, delay=custom_delay)

        # Verify sleep was called with custom delay
        mock_sleep.assert_called_with(custom_delay)  # type: ignore


class TestRainbowPrint:
    """Tests for the rainbow_print function."""

    def test_rainbow_print_returns_string(self) -> None:
        """Test that rainbow_print returns a string."""
        text = "Hello"
        result = rainbow_print(text)
        assert isinstance(result, str)

    def test_rainbow_print_contains_color_markup(self) -> None:
        """Test that rainbow_print adds color markup when colors are enabled."""
        text = "Test"
        result = rainbow_print(text, use_color=True)

        # Should contain Rich markup tags
        assert "[" in result and "]" in result

    def test_rainbow_print_respects_no_color(self) -> None:
        """Test that rainbow_print returns plain text when use_color is False."""
        text = "Hello, World!"
        result = rainbow_print(text, use_color=False)

        # Should return the original text unchanged
        assert result == text

    def test_rainbow_print_preserves_text_content(self) -> None:
        """Test that rainbow_print preserves the original text content."""
        text = "Hello"
        result = rainbow_print(text, use_color=True)

        # Remove all markup to check if original text is preserved
        # Simple check: all original characters should be in result
        for char in text:
            assert char in result

    def test_rainbow_print_cycles_colors(self) -> None:
        """Test that rainbow_print cycles through different colors."""
        text = "ABCDEFGHIJKLMNOP"  # Long enough to cycle through colors
        result = rainbow_print(text, use_color=True)

        # Should contain multiple different colors
        colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
        color_count = sum(1 for color in colors if color in result)

        # Should have at least a few different colors
        assert color_count >= 3

    def test_rainbow_print_handles_empty_string(self) -> None:
        """Test that rainbow_print handles empty string."""
        result = rainbow_print("", use_color=True)
        assert result == ""

    def test_rainbow_print_handles_whitespace(self) -> None:
        """Test that rainbow_print handles text with whitespace."""
        text = "Hello World"
        result = rainbow_print(text, use_color=True)

        # Should still contain the space
        assert " " in result

    def test_rainbow_print_with_special_characters(self) -> None:
        """Test that rainbow_print handles special characters."""
        text = "Hello, World!"
        result = rainbow_print(text, use_color=True)

        # Should preserve special characters
        assert "," in result
        assert "!" in result
