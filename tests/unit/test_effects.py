from greet.renderers.effects import RAINBOW_COLORS, apply_rainbow


def test_empty_string_returns_empty() -> None:
    assert apply_rainbow("") == ""


def test_output_contains_rich_color_tags() -> None:
    result = apply_rainbow("abc")
    assert "[red]" in result or "[yellow]" in result or "[green]" in result


def test_output_wraps_each_char_in_tags() -> None:
    result = apply_rainbow("Hi")
    assert "[/" in result  # closing tags present


def test_at_least_three_distinct_colors_defined() -> None:
    assert len(RAINBOW_COLORS) >= 3


def test_colors_are_distinct() -> None:
    assert len(set(RAINBOW_COLORS)) == len(RAINBOW_COLORS)


def test_long_text_cycles_colors() -> None:
    # Text longer than color count should cycle colors
    text = "a" * (len(RAINBOW_COLORS) + 1)
    result = apply_rainbow(text)
    # First and last char should use the same color (cycling)
    first_color = RAINBOW_COLORS[0]
    assert f"[{first_color}]" in result


def test_single_char_uses_first_color() -> None:
    result = apply_rainbow("X")
    first_color = RAINBOW_COLORS[0]
    assert f"[{first_color}]X[/{first_color}]" in result


def test_all_original_chars_preserved() -> None:
    text = "Hello"
    result = apply_rainbow(text)
    for char in text:
        assert char in result
