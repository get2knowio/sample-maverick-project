"""Language definitions and data structures for multilingual greetings."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Language:
    """Represents a supported language for greetings.

    Attributes:
        code: ISO 639-1 language code (e.g., "en", "fr")
        name: Display name for the language (e.g., "English", "French")
        banner_name: Text to use for ASCII art banner (e.g., "ENGLISH", "FRANÇAIS")
        greeting_template: Greeting template with {name} placeholder
        flag_emoji: Country flag emoji representing the language
    """

    code: str
    name: str
    banner_name: str
    greeting_template: str
    flag_emoji: str


LANGUAGES: list[Language] = [
    Language(
        code="en",
        name="English",
        banner_name="ENGLISH",
        greeting_template="Hello, {name}!",
        flag_emoji="🇬🇧",
    ),
    Language(
        code="fr",
        name="French",
        banner_name="FRANÇAIS",
        greeting_template="Bonjour, {name} !",
        flag_emoji="🇫🇷",
    ),
    Language(
        code="es",
        name="Spanish",
        banner_name="ESPAÑOL",
        greeting_template="¡Hola, {name}!",
        flag_emoji="🇪🇸",
    ),
    Language(
        code="de",
        name="German",
        banner_name="DEUTSCH",
        greeting_template="Hallo, {name}!",
        flag_emoji="🇩🇪",
    ),
    Language(
        code="ja",
        name="Japanese",
        banner_name="JAPANESE",
        greeting_template="こんにちは、{name}！",
        flag_emoji="🇯🇵",
    ),
    Language(
        code="zh",
        name="Mandarin",
        banner_name="MANDARIN",
        greeting_template="你好，{name}！",
        flag_emoji="🇨🇳",
    ),
    Language(
        code="ar",
        name="Arabic",
        banner_name="ARABIC",
        greeting_template="مرحبا، {name}!",
        flag_emoji="🇸🇦",
    ),
    Language(
        code="hi",
        name="Hindi",
        banner_name="HINDI",
        greeting_template="नमस्ते, {name}!",
        flag_emoji="🇮🇳",
    ),
    Language(
        code="sw",
        name="Swahili",
        banner_name="KISWAHILI",
        greeting_template="Habari, {name}!",
        flag_emoji="🇰🇪",
    ),
    Language(
        code="pt",
        name="Portuguese",
        banner_name="PORTUGUÊS",
        greeting_template="Olá, {name}!",
        flag_emoji="🇧🇷",
    ),
]
