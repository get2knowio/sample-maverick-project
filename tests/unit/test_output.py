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
