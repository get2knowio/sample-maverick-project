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
