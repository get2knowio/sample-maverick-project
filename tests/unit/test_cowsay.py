from greet.renderers.cowsay import render_cowsay


def test_output_contains_text() -> None:
    result = render_cowsay("Hello, World!")
    assert "Hello, World!" in result


def test_output_contains_cow_art() -> None:
    result = render_cowsay("Hi")
    assert "(oo)" in result
    assert "^__^" in result


def test_output_contains_speech_bubble() -> None:
    result = render_cowsay("test")
    assert "< test >" in result


def test_border_width_matches_text() -> None:
    text = "abc"
    result = render_cowsay(text)
    # border is dashes of length len(text) + 2
    assert "-" * (len(text) + 2) in result


def test_multiline_structure() -> None:
    result = render_cowsay("Hi")
    lines = result.splitlines()
    assert len(lines) >= 5  # bubble (3 lines) + cow (several lines)


def test_single_char_text() -> None:
    result = render_cowsay("X")
    assert "X" in result
    assert "(oo)" in result
