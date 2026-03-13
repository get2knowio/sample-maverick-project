from greet.renderers.figlet import render_banner


def test_ascii_label_returns_figlet_art() -> None:
    result = render_banner("Hello")
    assert isinstance(result, str)
    assert len(result) > len("Hello")
    # pyfiglet output contains the letters spread across multiple lines
    assert "\n" in result


def test_ascii_label_contains_content() -> None:
    result = render_banner("Hi")
    assert result.strip()  # non-empty after stripping


def test_non_ascii_label_falls_back_to_plain_header() -> None:
    label = "こんにちは"
    result = render_banner(label)
    assert label in result
    assert result.startswith("===")
    assert result.endswith("===")


def test_non_latin_arabic_falls_back() -> None:
    label = "مرحبا"
    result = render_banner(label)
    assert label in result
    assert "===" in result


def test_empty_string_returns_figlet_output() -> None:
    result = render_banner("")
    assert isinstance(result, str)


def test_plain_ascii_word() -> None:
    result = render_banner("Hola")
    # Should not use the fallback format
    assert not result.startswith("===")
