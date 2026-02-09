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
