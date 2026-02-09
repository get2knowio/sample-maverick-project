"""Shared test fixtures for greet CLI tests."""

import pytest

from greet.core import OutputConfig
from greet.languages import Language


@pytest.fixture
def sample_language() -> Language:
    """Provide a sample Language for testing."""
    return Language(
        code="en",
        name="English",
        banner_name="ENGLISH",
        greeting_template="Hello, {name}!",
        flag_emoji="🇬🇧",
    )


@pytest.fixture
def default_output_config() -> OutputConfig:
    """Provide default OutputConfig for testing."""
    return OutputConfig(
        languages=None,
        name="World",
        show_figlet=True,
        use_color=True,
        random_mode=False,
        cowsay=False,
        party_mode=False,
        show_fortune=False,
        grid_layout=False,
        typewriter=False,
        rainbow=False,
        show_box=False,
    )
