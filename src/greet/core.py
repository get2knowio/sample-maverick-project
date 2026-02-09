"""Core greeting generation logic and data structures."""

from dataclasses import dataclass

from greet.languages import Language


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
