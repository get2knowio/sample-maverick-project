from dataclasses import dataclass, field

from greet.fortunes import Proverb
from greet.languages import Language


@dataclass
class OutputConfig:
    color: bool = True
    ascii_art: bool = True
    show_proverb: bool = True
    language_code: str = "en"


@dataclass
class GreetingEntry:
    language: Language
    proverb: Proverb | None = field(default=None)
    config: OutputConfig = field(default_factory=OutputConfig)
