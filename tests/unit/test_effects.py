"""Tests for the effects module."""

import random

from greet.renderers.effects import add_confetti, random_color_style


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
