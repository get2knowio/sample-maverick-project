"""Tests for greet.core module."""

import pytest

from greet.core import Greeting, OutputConfig, generate_all_greetings, generate_greeting
from greet.languages import LANGUAGES, Language


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


def test_generate_all_greetings_default_name() -> None:
    """Test generating all greetings with default name."""
    greetings = generate_all_greetings()
    # Should return greeting for each language in LANGUAGES
    assert len(greetings) == len(LANGUAGES)
    # Each greeting should have "World" as the name
    assert all("World" in g.text or "Mundo" in g.text or "世界" in g.text for g in greetings)
    # Should contain all language objects
    lang_codes = {g.language.code for g in greetings}
    expected_codes = {lang.code for lang in LANGUAGES}
    assert lang_codes == expected_codes


def test_generate_all_greetings_custom_name() -> None:
    """Test generating all greetings with custom name."""
    greetings = generate_all_greetings(name="Alice")
    assert len(greetings) == len(LANGUAGES)
    # Should contain Alice in the greetings
    assert any("Alice" in g.text for g in greetings)


def test_generate_all_greetings_language_filter_single() -> None:
    """Test generating greetings filtered to single language."""
    greetings = generate_all_greetings(languages=["english"])
    assert len(greetings) == 1
    assert greetings[0].language.code == "en"
    assert greetings[0].text == "Hello, World!"


def test_generate_all_greetings_language_filter_multiple() -> None:
    """Test generating greetings filtered to multiple languages."""
    greetings = generate_all_greetings(languages=["french", "spanish"])
    assert len(greetings) == 2
    codes = {g.language.code for g in greetings}
    assert codes == {"fr", "es"}


def test_generate_all_greetings_case_insensitive_filter() -> None:
    """Test that language filter is case insensitive."""
    greetings1 = generate_all_greetings(languages=["ENGLISH"])
    greetings2 = generate_all_greetings(languages=["English"])
    greetings3 = generate_all_greetings(languages=["english"])
    assert len(greetings1) == len(greetings2) == len(greetings3) == 1
    assert greetings1[0].language.code == greetings2[0].language.code == greetings3[0].language.code


def test_generate_all_greetings_invalid_language() -> None:
    """Test that invalid language names are ignored."""
    greetings = generate_all_greetings(languages=["english", "klingon", "french"])
    # Should only include valid languages (english and french)
    assert len(greetings) == 2
    codes = {g.language.code for g in greetings}
    assert codes == {"en", "fr"}


def test_generate_all_greetings_all_invalid_languages() -> None:
    """Test that all invalid languages returns empty list."""
    greetings = generate_all_greetings(languages=["klingon", "vulcan"])
    assert len(greetings) == 0


def test_generate_all_greetings_empty_language_list() -> None:
    """Test that empty language list returns empty greetings."""
    greetings = generate_all_greetings(languages=[])
    assert len(greetings) == 0


def test_generate_all_greetings_none_filter() -> None:
    """Test that None filter returns all languages."""
    greetings = generate_all_greetings(languages=None)
    assert len(greetings) == len(LANGUAGES)
