import pytest

from greet.languages import LANGUAGES, Language, find_language


def test_language_dataclass_fields() -> None:
    lang = Language(name="English", greeting="Hello", code="en", banner_label="Hello")
    assert lang.name == "English"
    assert lang.greeting == "Hello"
    assert lang.code == "en"
    assert lang.banner_label == "Hello"


def test_language_is_frozen() -> None:
    lang = Language(name="English", greeting="Hello", code="en", banner_label="Hello")
    with pytest.raises(Exception):
        lang.name = "Changed"  # type: ignore[misc]


def test_languages_list_has_at_least_ten() -> None:
    assert len(LANGUAGES) >= 10


def test_languages_list_contains_english() -> None:
    codes = [lang.code for lang in LANGUAGES]
    assert "en" in codes


def test_all_languages_have_non_empty_fields() -> None:
    for lang in LANGUAGES:
        assert lang.name
        assert lang.greeting
        assert lang.code
        assert lang.banner_label


def test_find_language_by_code() -> None:
    lang = find_language("en")
    assert lang is not None
    assert lang.code == "en"


def test_find_language_by_code_case_insensitive() -> None:
    lang = find_language("EN")
    assert lang is not None
    assert lang.code == "en"


def test_find_language_by_name() -> None:
    lang = find_language("English")
    assert lang is not None
    assert lang.name == "English"


def test_find_language_by_name_case_insensitive() -> None:
    lang = find_language("english")
    assert lang is not None
    assert lang.name == "English"


def test_find_language_returns_none_for_unknown() -> None:
    assert find_language("xx") is None


def test_find_language_strips_whitespace() -> None:
    lang = find_language("  en  ")
    assert lang is not None
    assert lang.code == "en"
