"""Tests for greet.fortunes module."""

from greet.fortunes import PROVERBS, Proverb


def test_proverb_dataclass_creation() -> None:
    """Test that Proverb dataclass can be created with all fields."""
    proverb = Proverb(
        text="A journey of a thousand miles begins with a single step.",
        language="English",
        translation=None,
    )
    assert proverb.text == "A journey of a thousand miles begins with a single step."
    assert proverb.language == "English"
    assert proverb.translation is None


def test_proverb_with_translation() -> None:
    """Test that Proverb can be created with a translation."""
    proverb = Proverb(
        text="Petit à petit, l'oiseau fait son nid.",
        language="French",
        translation="Little by little, the bird builds its nest.",
    )
    assert proverb.text == "Petit à petit, l'oiseau fait son nid."
    assert proverb.language == "French"
    assert proverb.translation == "Little by little, the bird builds its nest."


def test_proverb_is_frozen() -> None:
    """Test that Proverb instances are immutable (frozen)."""
    proverb = Proverb(text="Test", language="English")
    try:
        proverb.text = "Changed"  # type: ignore[misc]
        assert False, "Should not be able to modify frozen dataclass"
    except AttributeError:
        pass


def test_proverbs_list_has_minimum_count() -> None:
    """Test that PROVERBS contains at least 10 proverbs."""
    assert len(PROVERBS) >= 10, "Should have at least 10 proverbs"


def test_proverbs_list_has_expected_count() -> None:
    """Test that PROVERBS contains 20 proverbs (2 per language)."""
    assert len(PROVERBS) == 20


def test_all_proverbs_have_non_empty_text() -> None:
    """Test that all proverbs have non-empty text."""
    for proverb in PROVERBS:
        assert proverb.text, f"Proverb in {proverb.language} has empty text"


def test_all_proverbs_have_non_empty_language() -> None:
    """Test that all proverbs have non-empty language field."""
    for proverb in PROVERBS:
        assert proverb.language, f"Proverb '{proverb.text[:30]}...' has empty language"


def test_proverbs_cover_all_languages() -> None:
    """Test that proverbs include all 10 supported languages."""
    expected_languages = {
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
    actual_languages = {proverb.language for proverb in PROVERBS}
    assert actual_languages == expected_languages


def test_non_english_proverbs_have_translation() -> None:
    """Test that non-English proverbs have translations."""
    for proverb in PROVERBS:
        if proverb.language != "English":
            assert proverb.translation is not None, (
                f"{proverb.language} proverb missing translation: {proverb.text}"
            )


def test_english_proverbs_have_no_translation() -> None:
    """Test that English proverbs have no translation (None)."""
    for proverb in PROVERBS:
        if proverb.language == "English":
            assert proverb.translation is None, (
                f"English proverb should not have translation: {proverb.text}"
            )


def test_proverbs_contain_multilingual_characters() -> None:
    """Test that proverbs contain appropriate multilingual characters."""
    # Japanese proverbs should contain Japanese characters
    japanese_proverbs = [p for p in PROVERBS if p.language == "Japanese"]
    assert any(
        any(
            "\u3040" <= char <= "\u309f"
            or "\u30a0" <= char <= "\u30ff"
            or "\u4e00" <= char <= "\u9fff"
            for char in p.text
        )
        for p in japanese_proverbs
    ), "Japanese proverbs should contain Japanese characters"

    # Arabic proverbs should contain Arabic characters
    arabic_proverbs = [p for p in PROVERBS if p.language == "Arabic"]
    assert any(any("\u0600" <= char <= "\u06ff" for char in p.text) for p in arabic_proverbs), (
        "Arabic proverbs should contain Arabic characters"
    )

    # Hindi proverbs should contain Devanagari characters
    hindi_proverbs = [p for p in PROVERBS if p.language == "Hindi"]
    assert any(any("\u0900" <= char <= "\u097f" for char in p.text) for p in hindi_proverbs), (
        "Hindi proverbs should contain Devanagari characters"
    )

    # Mandarin proverbs should contain Chinese characters
    mandarin_proverbs = [p for p in PROVERBS if p.language == "Mandarin"]
    assert any(any("\u4e00" <= char <= "\u9fff" for char in p.text) for p in mandarin_proverbs), (
        "Mandarin proverbs should contain Chinese characters"
    )


def test_each_language_has_two_proverbs() -> None:
    """Test that each language has exactly 2 proverbs."""
    language_counts: dict[str, int] = {}
    for proverb in PROVERBS:
        language_counts[proverb.language] = language_counts.get(proverb.language, 0) + 1

    for language, count in language_counts.items():
        assert count == 2, f"{language} should have exactly 2 proverbs, but has {count}"


def test_select_random_proverb_returns_proverb() -> None:
    """Test that select_random_proverb returns a Proverb object."""
    from greet.fortunes import select_random_proverb

    proverb = select_random_proverb()
    assert isinstance(proverb, Proverb)
    assert proverb in PROVERBS


def test_select_random_proverb_returns_different_proverbs() -> None:
    """Test that select_random_proverb returns different proverbs (statistically)."""
    from greet.fortunes import select_random_proverb

    # Run multiple times and collect proverbs
    proverbs = []
    for _ in range(20):
        proverb = select_random_proverb()
        proverbs.append(proverb.text)

    # With 20 proverbs in the list and 20 draws, we should see at least 2 different ones
    unique_proverbs = set(proverbs)
    assert len(unique_proverbs) >= 2, "Random selection should produce variety"
