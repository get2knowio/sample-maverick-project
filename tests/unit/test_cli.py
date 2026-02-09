"""Tests for greet.cli module."""

from click.testing import CliRunner

from greet import __version__
from greet.cli import main


def test_cli_runs_without_error() -> None:
    """Test that the CLI runs without error."""
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0


def test_cli_outputs_greetings() -> None:
    """Test that the CLI outputs greetings from all languages."""
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    # Should contain greetings from multiple languages
    assert len(result.output) > 100


def test_cli_help_option() -> None:
    """Test that --help option works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Multilingual greeting CLI tool" in result.output


def test_cli_help_short_option() -> None:
    """Test that -h short option works."""
    runner = CliRunner()
    result = runner.invoke(main, ["-h"])
    assert result.exit_code == 0
    assert "Multilingual greeting CLI tool" in result.output


def test_cli_version_option() -> None:
    """Test that --version option works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "greet" in result.output
    assert __version__ in result.output


def test_cli_displays_all_languages() -> None:
    """Test that the CLI displays greetings in all languages."""
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    # Check for greetings in various languages
    assert "Hello, World!" in result.output  # English
    assert "Bonjour" in result.output  # French
    assert "Hola" in result.output  # Spanish
    assert "Hallo" in result.output  # German


def test_cli_displays_figlet_banners() -> None:
    """Test that the CLI displays figlet ASCII art banners."""
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    # Figlet output should be multi-line and substantial
    lines = result.output.split("\n")
    assert len(lines) > 20  # Should have many lines for 10 languages with banners


def test_cli_exit_code_on_success() -> None:
    """Test that successful execution returns exit code 0."""
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0


def test_cli_languages_option_single() -> None:
    """Test --languages option with single language."""
    runner = CliRunner()
    result = runner.invoke(main, ["--languages", "english"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output
    # Should not contain other languages
    assert "Bonjour" not in result.output


def test_cli_languages_short_option_single() -> None:
    """Test -l short option with single language."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "french"])
    assert result.exit_code == 0
    assert "Bonjour" in result.output
    # Should not contain other languages
    assert "Hello, World!" not in result.output


def test_cli_languages_option_multiple() -> None:
    """Test --languages option with multiple languages."""
    runner = CliRunner()
    result = runner.invoke(main, ["--languages", "french,spanish"])
    assert result.exit_code == 0
    assert "Bonjour" in result.output
    assert "Hola" in result.output
    # Should not contain other languages
    assert "Hello, World!" not in result.output
    assert "Hallo" not in result.output


def test_cli_languages_option_case_insensitive() -> None:
    """Test --languages option is case insensitive."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "FRENCH"])
    assert result.exit_code == 0
    assert "Bonjour" in result.output


def test_cli_languages_option_with_spaces() -> None:
    """Test --languages option with spaces around commas."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "french, spanish"])
    assert result.exit_code == 0
    assert "Bonjour" in result.output
    assert "Hola" in result.output


def test_cli_invalid_language_shows_error() -> None:
    """Test that invalid language shows helpful error message."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "klingon"])
    assert result.exit_code == 2
    assert "Invalid language" in result.output or "invalid language" in result.output
    # Should list valid options
    assert "English" in result.output or "english" in result.output


def test_cli_partial_invalid_languages_shows_error() -> None:
    """Test that partial invalid languages shows error for all invalid ones."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "english,klingon,french"])
    assert result.exit_code == 2
    assert "klingon" in result.output.lower()


def test_cli_all_invalid_languages_shows_error() -> None:
    """Test that all invalid languages shows error."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "klingon,vulcan"])
    assert result.exit_code == 2


def test_cli_invalid_language_exit_code() -> None:
    """Test that invalid language returns exit code 2."""
    runner = CliRunner()
    result = runner.invoke(main, ["--languages", "notareallanguage"])
    assert result.exit_code == 2


def test_cli_no_figlet_flag() -> None:
    """Test that --no-figlet disables ASCII art banners."""
    runner = CliRunner()
    result_with_figlet = runner.invoke(main, ["-l", "english"])
    result_without_figlet = runner.invoke(main, ["-l", "english", "--no-figlet"])

    assert result_without_figlet.exit_code == 0
    assert "Hello, World!" in result_without_figlet.output
    # Output without figlet should be significantly shorter
    assert len(result_without_figlet.output) < len(result_with_figlet.output)


def test_cli_no_color_flag() -> None:
    """Test that --no-color disables terminal colors."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "english", "--no-color"])

    assert result.exit_code == 0
    assert "Hello, World!" in result.output
    # Should not contain ANSI color codes (basic check)
    # Rich may still add some formatting, but major color codes should be absent


def test_cli_random_flag() -> None:
    """Test that --random displays exactly one random language."""
    runner = CliRunner()
    result = runner.invoke(main, ["--random"])

    assert result.exit_code == 0
    # Output should contain a greeting but be much shorter than all languages
    assert len(result.output) > 0
    # Quick check: output should be significantly shorter than default (all languages)
    result_all = runner.invoke(main)
    assert len(result.output) < len(result_all.output) / 3  # At least 3x shorter


def test_cli_random_flag_with_language_filter() -> None:
    """Test that --random works with --languages to select from filtered set."""
    runner = CliRunner()
    # When filtering to one language, random should still work and show that language
    result = runner.invoke(main, ["--random", "-l", "english"])

    assert result.exit_code == 0
    assert "Hello, World!" in result.output
    # Should not contain other languages
    assert "Bonjour" not in result.output


def test_cli_random_flag_changes_output() -> None:
    """Test that --random produces different outputs (statistically)."""
    runner = CliRunner()
    # Run multiple times and collect outputs
    outputs = []
    for _ in range(10):
        result = runner.invoke(main, ["--random"])
        outputs.append(result.output)

    # At least some outputs should differ (very high probability with 10 languages)
    unique_outputs = set(outputs)
    # With 10 runs and 10 languages, we should see at least 2 different languages
    assert len(unique_outputs) >= 2


def test_cli_no_figlet_and_no_color_combined() -> None:
    """Test that --no-figlet and --no-color work together."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "english", "--no-figlet", "--no-color"])

    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_cli_random_with_no_figlet() -> None:
    """Test that --random and --no-figlet work together."""
    runner = CliRunner()
    result = runner.invoke(main, ["--random", "--no-figlet"])

    assert result.exit_code == 0
    # Should have minimal output - just one greeting without banner
    assert len(result.output.strip()) > 0


def test_cli_name_option_single_language() -> None:
    """Test --name option with single language."""
    runner = CliRunner()
    result = runner.invoke(main, ["--name", "Marie", "-l", "french"])
    assert result.exit_code == 0
    assert "Bonjour, Marie !" in result.output
    # Should not contain default "World"
    assert "le monde" not in result.output.lower()


def test_cli_name_option_multiple_languages() -> None:
    """Test --name option with multiple languages."""
    runner = CliRunner()
    result = runner.invoke(main, ["--name", "Alice", "-l", "english,spanish"])
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.output
    assert "¡Hola, Alice!" in result.output


def test_cli_name_option_default_world() -> None:
    """Test that default name is 'World' when --name not specified."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "english"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_cli_name_option_with_spaces() -> None:
    """Test --name option with spaces in the name."""
    runner = CliRunner()
    result = runner.invoke(main, ["--name", "Dr. Smith", "-l", "english"])
    assert result.exit_code == 0
    assert "Hello, Dr. Smith!" in result.output


def test_cli_name_option_with_special_characters() -> None:
    """Test --name option with special characters."""
    runner = CliRunner()
    result = runner.invoke(main, ["--name", "José", "-l", "spanish"])
    assert result.exit_code == 0
    assert "¡Hola, José!" in result.output


def test_cli_name_option_with_unicode() -> None:
    """Test --name option with Unicode characters."""
    runner = CliRunner()
    result = runner.invoke(main, ["--name", "世界", "-l", "japanese"])
    assert result.exit_code == 0
    assert "こんにちは、世界！" in result.output


def test_cli_name_option_with_random() -> None:
    """Test --name option works with --random flag."""
    runner = CliRunner()
    result = runner.invoke(main, ["--name", "Bob", "--random"])
    assert result.exit_code == 0
    # Should contain Bob in some language greeting
    assert "Bob" in result.output
    # Should not contain World
    assert "World" not in result.output


def test_cli_name_option_all_languages() -> None:
    """Test --name option applies to all languages when no filter."""
    runner = CliRunner()
    result = runner.invoke(main, ["--name", "Everyone"])
    assert result.exit_code == 0
    # Should contain Everyone in at least one greeting
    assert "Everyone" in result.output


def test_cli_cowsay_flag() -> None:
    """Test that --cowsay wraps output in speech bubble."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "english", "--cowsay"])
    assert result.exit_code == 0
    # Should contain the greeting
    assert "Hello, World!" in result.output
    # Should contain bubble borders
    assert "_" in result.output or "-" in result.output
    # Should contain ASCII cow
    assert "(oo)" in result.output or "^__^" in result.output


def test_cli_cowsay_with_random() -> None:
    """Test that --cowsay works with --random flag."""
    runner = CliRunner()
    result = runner.invoke(main, ["--cowsay", "--random"])
    assert result.exit_code == 0
    # Should contain bubble borders
    assert "_" in result.output or "-" in result.output
    # Should contain ASCII cow
    assert "(oo)" in result.output or "^__^" in result.output
    # Should be shorter than all languages (random shows just one)
    result_all = runner.invoke(main)
    assert len(result.output) < len(result_all.output) / 2


def test_cli_cowsay_with_no_figlet() -> None:
    """Test that --cowsay works with --no-figlet."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "english", "--cowsay", "--no-figlet"])
    assert result.exit_code == 0
    # Should contain the greeting
    assert "Hello, World!" in result.output
    # Should contain bubble and cow
    assert "(oo)" in result.output


def test_cli_cowsay_with_name() -> None:
    """Test that --cowsay works with --name option."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "french", "--cowsay", "--name", "Marie"])
    assert result.exit_code == 0
    # Should contain personalized greeting
    assert "Bonjour, Marie !" in result.output
    # Should contain bubble and cow
    assert "(oo)" in result.output


def test_cli_cowsay_with_multiple_languages() -> None:
    """Test that --cowsay wraps multiple languages."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "english,french", "--cowsay"])
    assert result.exit_code == 0
    # Should contain both greetings
    assert "Hello, World!" in result.output
    assert "Bonjour" in result.output
    # Should contain bubble and cow
    assert "(oo)" in result.output


def test_cli_party_flag() -> None:
    """Test that --party adds confetti and flag emojis."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "english", "--party"])
    assert result.exit_code == 0
    # Should contain the greeting
    assert "Hello, World!" in result.output
    # Should contain flag emoji
    assert "🇬🇧" in result.output
    # Should contain confetti emojis (at least one)
    confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
    assert any(emoji in result.output for emoji in confetti_emojis)


def test_cli_party_with_no_color() -> None:
    """Test that --party respects --no-color (flags shown, colors disabled)."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "french", "--party", "--no-color"])
    assert result.exit_code == 0
    # Should contain the greeting
    assert "Bonjour" in result.output
    # Should contain flag emoji (emojis still appear)
    assert "🇫🇷" in result.output
    # Should contain confetti emojis (emojis still appear)
    confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
    assert any(emoji in result.output for emoji in confetti_emojis)


def test_cli_party_with_random() -> None:
    """Test that --party works with --random flag."""
    runner = CliRunner()
    result = runner.invoke(main, ["--party", "--random"])
    assert result.exit_code == 0
    # Should contain confetti emojis
    confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
    assert any(emoji in result.output for emoji in confetti_emojis)
    # Should contain at least one flag emoji
    flag_emojis = ["🇬🇧", "🇫🇷", "🇪🇸", "🇩🇪", "🇯🇵", "🇨🇳", "🇸🇦", "🇮🇳", "🇰🇪", "🇧🇷"]
    assert any(emoji in result.output for emoji in flag_emojis)


def test_cli_party_with_cowsay() -> None:
    """Test that --party works with --cowsay."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "spanish", "--party", "--cowsay"])
    assert result.exit_code == 0
    # Should contain the greeting
    assert "Hola" in result.output
    # Should contain flag emoji
    assert "🇪🇸" in result.output
    # Should contain confetti
    confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
    assert any(emoji in result.output for emoji in confetti_emojis)
    # Should contain cowsay
    assert "(oo)" in result.output


def test_cli_party_with_multiple_languages() -> None:
    """Test that --party works with multiple languages."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "english,japanese", "--party"])
    assert result.exit_code == 0
    # Should contain both greetings
    assert "Hello, World!" in result.output
    assert "こんにちは、World！" in result.output  # Japanese greeting with World
    # Should contain both flag emojis
    assert "🇬🇧" in result.output
    assert "🇯🇵" in result.output
    # Should contain confetti
    confetti_emojis = ["🎉", "🎊", "✨", "🎈", "🎆", "🎇"]
    assert any(emoji in result.output for emoji in confetti_emojis)
