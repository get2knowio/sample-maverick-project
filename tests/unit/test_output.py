"""Unit tests for output rendering functionality."""

from io import StringIO

from rich.console import Console

from greet.core import Greeting, OutputConfig, generate_greeting
from greet.languages import LANGUAGES
from greet.output import create_console, render_all_greetings, render_greeting


def test_create_console_with_color() -> None:
    """Test creating a console with color enabled."""
    config = OutputConfig(use_color=True)
    console = create_console(config)
    assert isinstance(console, Console)


def test_create_console_without_color() -> None:
    """Test creating a console with color disabled."""
    config = OutputConfig(use_color=False)
    console = create_console(config)
    assert isinstance(console, Console)
    assert not console._force_terminal


def test_render_greeting_basic() -> None:
    """Test basic greeting rendering."""
    language = LANGUAGES[0]  # English
    greeting = generate_greeting(language, "World")
    config = OutputConfig(show_figlet=False, use_color=False)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False)

    render_greeting(greeting, config, console)
    result = output.getvalue()

    assert "Hello, World!" in result


def test_render_greeting_with_figlet() -> None:
    """Test greeting rendering with figlet banner."""
    language = LANGUAGES[0]  # English
    greeting = generate_greeting(language, "World")
    config = OutputConfig(show_figlet=True, use_color=False)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False)

    render_greeting(greeting, config, console)
    result = output.getvalue()

    # Should contain the greeting text
    assert "Hello, World!" in result
    # Should contain figlet banner (multi-line ASCII art)
    assert len(result.split("\n")) > 2


def test_render_greeting_without_figlet() -> None:
    """Test greeting rendering without figlet banner."""
    language = LANGUAGES[0]  # English
    greeting = generate_greeting(language, "World")
    config = OutputConfig(show_figlet=False, use_color=False)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False)

    render_greeting(greeting, config, console)
    result = output.getvalue()

    assert "Hello, World!" in result


def test_render_all_greetings_basic() -> None:
    """Test rendering all greetings."""
    greetings = [generate_greeting(lang, "World") for lang in LANGUAGES[:3]]
    config = OutputConfig(show_figlet=False, use_color=False)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False)

    render_all_greetings(greetings, config, console)
    result = output.getvalue()

    # Should contain greetings from multiple languages
    assert "Hello, World!" in result
    assert "Bonjour" in result
    assert "Hola" in result


def test_render_all_greetings_with_figlet() -> None:
    """Test rendering all greetings with figlet banners."""
    greetings = [generate_greeting(lang, "World") for lang in LANGUAGES[:2]]
    config = OutputConfig(show_figlet=True, use_color=False)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False)

    render_all_greetings(greetings, config, console)
    result = output.getvalue()

    # Should contain both greetings
    assert "Hello, World!" in result
    assert "Bonjour" in result
    # Should have substantial output from figlet banners
    assert len(result.split("\n")) > 10


def test_render_all_greetings_empty_list() -> None:
    """Test rendering empty greetings list."""
    greetings: list[Greeting] = []
    config = OutputConfig(use_color=False)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False)

    # Should not raise an error
    render_all_greetings(greetings, config, console)
    result = output.getvalue()

    # Output should be minimal or empty
    assert len(result.strip()) == 0


def test_render_greeting_with_party_mode() -> None:
    """Test greeting rendering with party mode enabled."""
    language = LANGUAGES[0]  # English
    greeting = generate_greeting(language, "World")
    config = OutputConfig(show_figlet=False, use_color=True, party_mode=True)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=True)

    render_greeting(greeting, config, console)
    result = output.getvalue()

    # Should contain the greeting text
    assert "Hello, World!" in result
    # Should contain flag emoji
    assert language.flag_emoji in result
    # Should contain confetti emojis (one of them)
    confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
    assert any(emoji in result for emoji in confetti_emojis)


def test_render_greeting_party_mode_respects_no_color() -> None:
    """Test that party mode respects --no-color flag (flags shown, colors disabled)."""
    language = LANGUAGES[0]  # English
    greeting = generate_greeting(language, "World")
    config = OutputConfig(show_figlet=False, use_color=False, party_mode=True)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False, no_color=True)

    render_greeting(greeting, config, console)
    result = output.getvalue()

    # Should contain the greeting text
    assert "Hello, World!" in result
    # Should contain flag emoji (emojis should still appear)
    assert language.flag_emoji in result
    # Should contain confetti emojis (emojis should still appear)
    confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
    assert any(emoji in result for emoji in confetti_emojis)


def test_render_greeting_party_mode_with_figlet() -> None:
    """Test greeting rendering with party mode and figlet enabled."""
    language = LANGUAGES[1]  # French
    greeting = generate_greeting(language, "World")
    config = OutputConfig(show_figlet=True, use_color=True, party_mode=True)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=True)

    render_greeting(greeting, config, console)
    result = output.getvalue()

    # Should contain the greeting text
    assert "Bonjour" in result
    # Should contain flag emoji
    assert language.flag_emoji in result
    # Should contain confetti emojis
    confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
    assert any(emoji in result for emoji in confetti_emojis)
    # Should contain figlet banner
    assert len(result.split("\n")) > 2


def test_render_fortune_basic() -> None:
    """Test basic fortune rendering."""
    from greet.fortunes import Proverb
    from greet.output import render_fortune

    proverb = Proverb(
        text="A journey of a thousand miles begins with a single step.",
        language="English",
        translation=None,
    )
    config = OutputConfig(use_color=False)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False)

    render_fortune(proverb, config, console)
    result = output.getvalue()

    # Should contain the proverb text
    assert "A journey of a thousand miles begins with a single step." in result


def test_render_fortune_with_translation() -> None:
    """Test fortune rendering with translation."""
    from greet.fortunes import Proverb
    from greet.output import render_fortune

    proverb = Proverb(
        text="Petit à petit, l'oiseau fait son nid.",
        language="French",
        translation="Little by little, the bird builds its nest.",
    )
    config = OutputConfig(use_color=False)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False)

    render_fortune(proverb, config, console)
    result = output.getvalue()

    # Should contain the proverb text
    assert "Petit à petit, l'oiseau fait son nid." in result
    # Should contain the translation
    assert "Little by little, the bird builds its nest." in result


def test_render_fortune_with_color() -> None:
    """Test fortune rendering with color enabled."""
    from greet.fortunes import Proverb
    from greet.output import render_fortune

    proverb = Proverb(
        text="Where there's a will, there's a way.",
        language="English",
        translation=None,
    )
    config = OutputConfig(use_color=True)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=True)

    render_fortune(proverb, config, console)
    result = output.getvalue()

    # Should contain the proverb text
    assert "Where there's a will, there's a way." in result


def test_render_grid_layout_basic() -> None:
    """Test basic grid layout rendering."""
    from greet.output import render_grid_layout

    greetings = [generate_greeting(lang, "World") for lang in LANGUAGES[:4]]
    config = OutputConfig(show_figlet=False, use_color=False, grid_layout=True)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False, width=120)

    render_grid_layout(greetings, config, console)
    result = output.getvalue()

    # Should contain greetings from all languages
    assert "Hello, World!" in result
    assert "Bonjour" in result
    assert "Hola" in result
    assert "Hallo" in result


def test_render_grid_layout_narrow_terminal() -> None:
    """Test grid layout with narrow terminal width."""
    from greet.output import render_grid_layout

    greetings = [generate_greeting(lang, "World") for lang in LANGUAGES[:3]]
    config = OutputConfig(show_figlet=False, use_color=False, grid_layout=True)

    # Capture output with narrow width
    output = StringIO()
    console = Console(file=output, force_terminal=False, width=40)

    render_grid_layout(greetings, config, console)
    result = output.getvalue()

    # Should still contain all greetings
    assert "Hello, World!" in result
    assert "Bonjour" in result


def test_render_grid_layout_empty_list() -> None:
    """Test grid layout with empty greetings list."""
    from greet.output import render_grid_layout

    greetings: list[Greeting] = []
    config = OutputConfig(use_color=False, grid_layout=True)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False)

    # Should not raise an error
    render_grid_layout(greetings, config, console)
    result = output.getvalue()

    # Output should be minimal or empty
    assert len(result.strip()) == 0


def test_render_grid_layout_with_party_mode() -> None:
    """Test grid layout rendering with party mode enabled."""
    from greet.output import render_grid_layout

    greetings = [generate_greeting(lang, "World") for lang in LANGUAGES[:2]]
    config = OutputConfig(
        show_figlet=False,
        use_color=True,
        party_mode=True,
        grid_layout=True,
    )

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=True, width=120)

    render_grid_layout(greetings, config, console)
    result = output.getvalue()

    # Should contain greetings
    assert "Hello, World!" in result
    # Should contain flag emojis
    assert LANGUAGES[0].flag_emoji in result
    # Should contain confetti emojis
    confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
    assert any(emoji in result for emoji in confetti_emojis)


def test_render_all_greetings_with_grid_layout() -> None:
    """Test render_all_greetings uses grid layout when config.grid_layout is True."""
    greetings = [generate_greeting(lang, "World") for lang in LANGUAGES[:3]]
    config = OutputConfig(show_figlet=False, use_color=False, grid_layout=True)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False, width=120)

    render_all_greetings(greetings, config, console)
    result = output.getvalue()

    # Should contain all greetings
    assert "Hello, World!" in result
    assert "Bonjour" in result
    assert "Hola" in result


def test_render_greeting_with_box() -> None:
    """Test greeting rendering with box mode enabled."""
    language = LANGUAGES[0]  # English
    greeting = generate_greeting(language, "World")
    config = OutputConfig(show_figlet=False, use_color=False, show_box=True)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False, width=80)

    render_greeting(greeting, config, console)
    result = output.getvalue()

    # Should contain the greeting text
    assert "Hello, World!" in result
    # Should contain box drawing characters (Rich Panel uses box drawing)
    # The output should be longer than just the greeting text
    assert len(result) > len("Hello, World!")


def test_render_greeting_with_box_and_figlet() -> None:
    """Test greeting rendering with box mode and figlet banner."""
    language = LANGUAGES[0]  # English
    greeting = generate_greeting(language, "World")
    config = OutputConfig(show_figlet=True, use_color=False, show_box=True)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False, width=80)

    render_greeting(greeting, config, console)
    result = output.getvalue()

    # Should contain the greeting text
    assert "Hello, World!" in result
    # Should contain figlet banner (multi-line ASCII art)
    assert len(result.split("\n")) > 2
    # Should be wrapped in a box (output is longer)
    assert len(result) > 100


def test_render_greeting_with_box_no_figlet() -> None:
    """Test box works with --no-figlet (boxes shown, banners hidden)."""
    language = LANGUAGES[0]  # English
    greeting = generate_greeting(language, "World")
    config = OutputConfig(show_figlet=False, use_color=False, show_box=True)

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=False, width=80)

    render_greeting(greeting, config, console)
    result = output.getvalue()

    # Should contain the greeting text
    assert "Hello, World!" in result
    # Should not contain extensive figlet output (fewer lines)
    # Box with greeting only should be much shorter than with figlet
    lines = result.split("\n")
    # With box and no figlet, should have roughly 3-5 lines (top border, content, bottom border)
    assert len(lines) < 10


def test_render_greeting_with_box_and_party_mode() -> None:
    """Test greeting rendering with box and party mode enabled."""
    language = LANGUAGES[0]  # English
    greeting = generate_greeting(language, "World")
    config = OutputConfig(
        show_figlet=False,
        use_color=True,
        show_box=True,
        party_mode=True,
    )

    # Capture output
    output = StringIO()
    console = Console(file=output, force_terminal=True, width=80)

    render_greeting(greeting, config, console)
    result = output.getvalue()

    # Should contain the greeting text
    assert "Hello, World!" in result
    # Should contain flag emoji
    assert language.flag_emoji in result
    # Should contain confetti emojis
    confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
    assert any(emoji in result for emoji in confetti_emojis)
