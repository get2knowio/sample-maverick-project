import pytest

from greet.fortunes import PROVERBS, Proverb


def test_proverb_dataclass_fields() -> None:
    p = Proverb(text="Do good.", source="Unknown")
    assert p.text == "Do good."
    assert p.source == "Unknown"


def test_proverb_is_frozen() -> None:
    p = Proverb(text="Do good.", source="Unknown")
    with pytest.raises(Exception):
        p.text = "Changed"  # type: ignore[misc]


def test_proverbs_list_has_at_least_twenty() -> None:
    assert len(PROVERBS) >= 20


def test_all_proverbs_have_non_empty_fields() -> None:
    for proverb in PROVERBS:
        assert proverb.text
        assert proverb.source
