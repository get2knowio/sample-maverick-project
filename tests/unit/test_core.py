"""Tests for greet.core module."""

import pytest

from greet.core import Greeting, OutputConfig, generate_greeting
from greet.languages import Language


def test_output_config_default_values() -> None:
    """Test that OutputConfig has correct default values."""
    config = OutputConfig()
    assert config.languages is None
    assert config.name == "World"
    assert config.show_figlet is True
    assert config.use_color is True
    assert config.random_mode is False
    assert config.cowsay is False
    assert config.party_mode is False
    assert config.show_fortune is False
    assert config.grid_layout is False
    assert config.typewriter is False
    assert config.rainbow is False
    assert config.show_box is False


def test_output_config_custom_values() -> None:
    """Test that OutputConfig can be created with custom values."""
    config = OutputConfig(
        languages=["english", "french"],
        name="Alice",
        show_figlet=False,
        use_color=False,
        random_mode=True,
    )
    assert config.languages == ["english", "french"]
    assert config.name == "Alice"
    assert config.show_figlet is False
    assert config.use_color is False
    assert config.random_mode is True


def test_output_config_is_frozen() -> None:
    """Test that OutputConfig instances are immutable (frozen)."""
    config = OutputConfig()
    with pytest.raises(AttributeError):
        config.name = "NewName"  # type: ignore[misc]


def test_greeting_dataclass_creation() -> None:
    """Test that Greeting dataclass can be created with all fields."""
    lang = Language(
        code="en",
        name="English",
        banner_name="ENGLISH",
        greeting_template="Hello, {name}!",
        flag_emoji="🇬🇧",
    )
    greeting = Greeting(language=lang, text="Hello, World!", banner="BANNER")
    assert greeting.language == lang
    assert greeting.text == "Hello, World!"
    assert greeting.banner == "BANNER"


def test_greeting_default_banner() -> None:
    """Test that Greeting banner defaults to empty string."""
    lang = Language(
        code="en",
        name="English",
        banner_name="ENGLISH",
        greeting_template="Hello, {name}!",
        flag_emoji="🇬🇧",
    )
    greeting = Greeting(language=lang, text="Hello, World!")
    assert greeting.banner == ""


def test_greeting_is_frozen() -> None:
    """Test that Greeting instances are immutable (frozen)."""
    lang = Language(
        code="en",
        name="English",
        banner_name="ENGLISH",
        greeting_template="Hello, {name}!",
        flag_emoji="🇬🇧",
    )
    greeting = Greeting(language=lang, text="Hello, World!")
    with pytest.raises(AttributeError):
        greeting.text = "New text"  # type: ignore[misc]


def test_generate_greeting_basic() -> None:
    """Test basic greeting generation."""
    lang = Language(
        code="en",
        name="English",
        banner_name="ENGLISH",
        greeting_template="Hello, {name}!",
        flag_emoji="🇬🇧",
    )
    greeting = generate_greeting(lang, "World")
    assert greeting.text == "Hello, World!"
    assert greeting.language == lang
    assert greeting.banner == ""


def test_generate_greeting_custom_name() -> None:
    """Test greeting generation with custom name."""
    lang = Language(
        code="fr",
        name="French",
        banner_name="FRANÇAIS",
        greeting_template="Bonjour, {name} !",
        flag_emoji="🇫🇷",
    )
    greeting = generate_greeting(lang, "Marie")
    assert greeting.text == "Bonjour, Marie !"
    assert greeting.language == lang


def test_generate_greeting_special_characters() -> None:
    """Test greeting generation with special characters in name."""
    lang = Language(
        code="es",
        name="Spanish",
        banner_name="ESPAÑOL",
        greeting_template="¡Hola, {name}!",
        flag_emoji="🇪🇸",
    )
    greeting = generate_greeting(lang, "José")
    assert greeting.text == "¡Hola, José!"


def test_generate_greeting_long_name() -> None:
    """Test greeting generation with a long name."""
    lang = Language(
        code="de",
        name="German",
        banner_name="DEUTSCH",
        greeting_template="Hallo, {name}!",
        flag_emoji="🇩🇪",
    )
    long_name = "Dr. Maximilian von Schnitzelpusskrankengescheitmeyer"
    greeting = generate_greeting(lang, long_name)
    assert greeting.text == f"Hallo, {long_name}!"


def test_generate_greeting_unicode_characters() -> None:
    """Test greeting generation with Unicode characters."""
    lang = Language(
        code="ja",
        name="Japanese",
        banner_name="JAPANESE",
        greeting_template="こんにちは、{name}！",
        flag_emoji="🇯🇵",
    )
    greeting = generate_greeting(lang, "世界")
    assert greeting.text == "こんにちは、世界！"
