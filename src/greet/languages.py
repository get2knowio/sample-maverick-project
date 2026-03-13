from dataclasses import dataclass


@dataclass(frozen=True)
class Language:
    name: str
    greeting: str
    code: str
    banner_label: str


LANGUAGES: list[Language] = [
    Language(
        name="English",
        greeting="Hello, World!",
        code="en",
        banner_label="Hello",
    ),
    Language(
        name="Spanish",
        greeting="¡Hola, Mundo!",
        code="es",
        banner_label="Hola",
    ),
    Language(
        name="French",
        greeting="Bonjour, le Monde!",
        code="fr",
        banner_label="Bonjour",
    ),
    Language(
        name="German",
        greeting="Hallo, Welt!",
        code="de",
        banner_label="Hallo",
    ),
    Language(
        name="Japanese",
        greeting="こんにちは、世界！",
        code="ja",
        banner_label="Konnichiwa",
    ),
    Language(
        name="Mandarin",
        greeting="你好，世界！",
        code="zh",
        banner_label="Nihao",
    ),
    Language(
        name="Arabic",
        greeting="مرحبا بالعالم!",
        code="ar",
        banner_label="Marhaba",
    ),
    Language(
        name="Portuguese",
        greeting="Olá, Mundo!",
        code="pt",
        banner_label="Ola",
    ),
    Language(
        name="Russian",
        greeting="Привет, мир!",
        code="ru",
        banner_label="Privet",
    ),
    Language(
        name="Swahili",
        greeting="Habari, Dunia!",
        code="sw",
        banner_label="Habari",
    ),
    Language(
        name="Hindi",
        greeting="नमस्ते, दुनिया!",
        code="hi",
        banner_label="Namaste",
    ),
    Language(
        name="Italian",
        greeting="Ciao, Mondo!",
        code="it",
        banner_label="Ciao",
    ),
]


def find_language(query: str) -> Language | None:
    """Find a language by code or name (case-insensitive)."""
    normalized = query.strip().lower()
    for lang in LANGUAGES:
        if lang.code.lower() == normalized or lang.name.lower() == normalized:
            return lang
    return None
