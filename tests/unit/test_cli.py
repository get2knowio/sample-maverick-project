"""Tests for greet.cli module."""

from click.testing import CliRunner

from greet import __version__
from greet.cli import main


def test_cli_runs_without_error() -> None:
    """Test that the CLI runs without error."""
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0


def test_cli_displays_version_in_output() -> None:
    """Test that the CLI displays the version in its output."""
    runner = CliRunner()
    result = runner.invoke(main)
    assert __version__ in result.output


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


def test_cli_basic_output_message() -> None:
    """Test that the CLI displays the basic skeleton message."""
    runner = CliRunner()
    result = runner.invoke(main)
    assert "Basic CLI skeleton" in result.output


def test_cli_displays_greeting_message() -> None:
    """Test that the CLI displays greeting output."""
    runner = CliRunner()
    result = runner.invoke(main)
    assert "Greet CLI" in result.output
