"""Core greeting generation logic and data structures."""

from dataclasses import dataclass

from greet.languages import LANGUAGES, Language, get_language_by_name


@dataclass(frozen=True)
class OutputConfig:
    """Configuration capturing all CLI options for a single execution.

    Attributes:
        languages: Filter to specific languages (None = all languages)
        name: Name to substitute in greeting templates
        show_figlet: Whether to show ASCII art banners
        use_color: Whether to enable terminal colors
        random_mode: Whether to show only one random language
        cowsay: Whether to wrap output in cowsay bubble
        party_mode: Whether to enable confetti, flags, and random colors
        show_fortune: Whether to append a random proverb
        grid_layout: Whether to display in grid layout
        typewriter: Whether to use typewriter animation
        rainbow: Whether to use rainbow color cycling
        show_box: Whether to draw Unicode boxes around greetings
    """

    languages: list[str] | None = None
    name: str = "World"
    show_figlet: bool = True
    use_color: bool = True
    random_mode: bool = False
    cowsay: bool = False
    party_mode: bool = False
    show_fortune: bool = False
    grid_layout: bool = False
    typewriter: bool = False
    rainbow: bool = False
    show_box: bool = False


@dataclass(frozen=True)
class Greeting:
    """A rendered greeting ready for display.

    Attributes:
        language: The source language
        text: Formatted greeting with name substituted
        banner: Optional figlet banner text (empty string if disabled)
    """

    language: Language
    text: str
    banner: str = ""


def generate_greeting(language: Language, name: str) -> Greeting:
    """Generate a greeting for a specific language with the given name.

    Args:
        language: The language to generate the greeting in
        name: The name to substitute into the greeting template

    Returns:
        A Greeting object with the formatted text
    """
    text = language.greeting_template.format(name=name)
    return Greeting(language=language, text=text, banner="")


def parse_language_filter(language_string: str) -> list[str]:
    """Parse comma-separated language names from a string.

    Args:
        language_string: Comma-separated language names (e.g., "english,french,spanish")

    Returns:
        List of language names with whitespace stripped
    """
    if not language_string:
        return []
    return [lang.strip() for lang in language_string.split(",")]


def filter_languages(language_names: list[str]) -> list[Language]:
    """Filter LANGUAGES list to only specified language names.

    Args:
        language_names: List of language names (case-insensitive)

    Returns:
        List of Language objects matching the specified names, in the order specified.
        Invalid language names are silently ignored.
    """
    result: list[Language] = []
    for name in language_names:
        lang = get_language_by_name(name)
        if lang is not None:
            result.append(lang)
    return result


def generate_all_greetings(
    languages: list[str] | None = None, name: str = "World"
) -> list[Greeting]:
    """Generate greetings for all languages or a filtered subset.

    Args:
        languages: Optional list of language names to filter by (case-insensitive).
                   If None, generates greetings for all supported languages.
        name: Name to substitute in greeting templates (default: "World")

    Returns:
        List of Greeting objects for the specified languages
    """
    # If no filter, use all languages
    if languages is None:
        selected_languages = LANGUAGES
    else:
        # Filter languages by name (case-insensitive)
        selected_languages = filter_languages(languages)

    # Generate greeting for each selected language
    return [generate_greeting(lang, name) for lang in selected_languages]
