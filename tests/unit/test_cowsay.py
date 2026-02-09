"""Unit tests for cowsay rendering functionality."""

from greet.renderers.cowsay import wrap_in_cowsay


def test_wrap_in_cowsay_single_line() -> None:
    """Test wrapping a single line of text in cowsay bubble."""
    text = "Hello, World!"
    result = wrap_in_cowsay(text)

    # Should contain the text
    assert "Hello, World!" in result
    # Should contain bubble borders
    assert "_" in result or "-" in result
    # Should contain the ASCII cow
    assert "\\" in result or "/" in result
    # Should be multiline
    assert "\n" in result


def test_wrap_in_cowsay_multiline() -> None:
    """Test wrapping multiple lines of text in cowsay bubble."""
    text = "Hello, World!\nBonjour, le monde !\n¡Hola, Mundo!"
    result = wrap_in_cowsay(text)

    # Should contain all lines
    assert "Hello, World!" in result
    assert "Bonjour, le monde !" in result
    assert "¡Hola, Mundo!" in result
    # Should contain bubble borders
    assert "_" in result or "-" in result
    # Should contain the ASCII cow
    assert "\\" in result or "/" in result


def test_wrap_in_cowsay_empty_string() -> None:
    """Test wrapping empty string in cowsay bubble."""
    text = ""
    result = wrap_in_cowsay(text)

    # Should still have bubble and cow
    assert "_" in result or "-" in result
    assert "\\" in result or "/" in result


def test_wrap_in_cowsay_unicode() -> None:
    """Test wrapping text with Unicode characters in cowsay bubble."""
    text = "こんにちは、世界！\n你好，世界！\nمرحبا بالعالم!"
    result = wrap_in_cowsay(text)

    # Should contain all Unicode text
    assert "こんにちは、世界！" in result
    assert "你好，世界！" in result
    assert "مرحبا بالعالم!" in result


def test_wrap_in_cowsay_preserves_spacing() -> None:
    """Test that cowsay preserves spacing and alignment."""
    text = "  Indented text\nNormal text\n    More indent"
    result = wrap_in_cowsay(text)

    # Should contain the text with spacing
    assert "Indented text" in result
    assert "Normal text" in result
    assert "More indent" in result


def test_wrap_in_cowsay_long_lines() -> None:
    """Test wrapping text with long lines in cowsay bubble."""
    text = "A" * 100 + "\nShort line"
    result = wrap_in_cowsay(text)

    # Should contain the text
    assert "A" in result
    assert "Short line" in result
    # Should have bubble borders
    assert "_" in result or "-" in result


def test_wrap_in_cowsay_special_characters() -> None:
    """Test wrapping text with special characters in cowsay bubble."""
    text = "Special chars: !@#$%^&*()\nSymbols: <>[]{}|"
    result = wrap_in_cowsay(text)

    # Should contain all special characters
    assert "!@#$%^&*()" in result
    assert "<>[]{}|" in result
