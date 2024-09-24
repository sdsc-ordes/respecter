from cli import app
from typer.testing import CliRunner

runner = CliRunner()

def test_help():
    """ Checks if 'respecter --help' commands exists successfully."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
