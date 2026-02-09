"""Tests for greet.languages module."""

from greet.languages import LANGUAGES, Language


def test_language_dataclass_creation() -> None:
    """Test that Language dataclass can be created with all fields."""
    lang = Language(
        code="en",
        name="English",
        banner_name="ENGLISH",
        greeting_template="Hello, {name}!",
        flag_emoji="🇬🇧",
    )
    assert lang.code == "en"
    assert lang.name == "English"
    assert lang.banner_name == "ENGLISH"
    assert lang.greeting_template == "Hello, {name}!"
    assert lang.flag_emoji == "🇬🇧"


def test_language_is_frozen() -> None:
    """Test that Language instances are immutable (frozen)."""
    lang = Language(
        code="en",
        name="English",
        banner_name="ENGLISH",
        greeting_template="Hello, {name}!",
        flag_emoji="🇬🇧",
    )
    try:
        lang.code = "fr"  # type: ignore[misc]
        assert False, "Should not be able to modify frozen dataclass"
    except AttributeError:
        pass


def test_languages_list_has_10_languages() -> None:
    """Test that LANGUAGES contains exactly 10 languages."""
    assert len(LANGUAGES) == 10


def test_languages_list_contains_expected_languages() -> None:
    """Test that LANGUAGES contains all expected language names."""
    expected_names = {
        "English",
        "French",
        "Spanish",
        "German",
        "Japanese",
        "Mandarin",
        "Arabic",
        "Hindi",
        "Swahili",
        "Portuguese",
    }
    actual_names = {lang.name for lang in LANGUAGES}
    assert actual_names == expected_names


def test_all_languages_have_unique_codes() -> None:
    """Test that all language codes are unique."""
    codes = [lang.code for lang in LANGUAGES]
    assert len(codes) == len(set(codes))


def test_all_languages_have_unique_names() -> None:
    """Test that all language names are unique."""
    names = [lang.name for lang in LANGUAGES]
    assert len(names) == len(set(names))


def test_all_greeting_templates_have_name_placeholder() -> None:
    """Test that all greeting templates contain {name} placeholder."""
    for lang in LANGUAGES:
        assert "{name}" in lang.greeting_template, f"{lang.name} missing {{name}} placeholder"


def test_all_languages_have_non_empty_fields() -> None:
    """Test that all language fields are populated."""
    for lang in LANGUAGES:
        assert lang.code, f"{lang.name} has empty code"
        assert lang.name, f"{lang.name} has empty name"
        assert lang.banner_name, f"{lang.name} has empty banner_name"
        assert lang.greeting_template, f"{lang.name} has empty greeting_template"
        assert lang.flag_emoji, f"{lang.name} has empty flag_emoji"
