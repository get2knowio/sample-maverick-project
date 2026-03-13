from greet.core import GreetingEntry, OutputConfig
from greet.fortunes import Proverb
from greet.languages import Language

_EN = Language(
    name="English",
    greeting="Hello, World!",
    code="en",
    banner_label="Hello",
)


def test_output_config_defaults() -> None:
    config = OutputConfig()
    assert config.color is True
    assert config.ascii_art is True
    assert config.show_proverb is True
    assert config.language_code == "en"


def test_output_config_custom_values() -> None:
    config = OutputConfig(
        color=False, ascii_art=False, show_proverb=False, language_code="fr"
    )
    assert config.color is False
    assert config.ascii_art is False
    assert config.show_proverb is False
    assert config.language_code == "fr"


def test_greeting_entry_with_language() -> None:
    entry = GreetingEntry(language=_EN)
    assert entry.language is _EN
    assert entry.proverb is None
    assert entry.config.color is True


def test_greeting_entry_with_proverb() -> None:
    proverb = Proverb(text="A journey begins.", source="Unknown")
    entry = GreetingEntry(language=_EN, proverb=proverb)
    assert entry.proverb is proverb


def test_greeting_entry_with_custom_config() -> None:
    config = OutputConfig(color=False)
    entry = GreetingEntry(language=_EN, config=config)
    assert entry.config.color is False


def test_greeting_entry_config_default_is_independent() -> None:
    entry1 = GreetingEntry(language=_EN)
    entry2 = GreetingEntry(language=_EN)
    entry1.config.color = False
    assert entry2.config.color is True
