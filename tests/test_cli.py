from respecter.cli import app
from typer.testing import CliRunner

runner = CliRunner(mix_stderr=False)

def test_help():
    """ Checks if 'respecter --help' commands exists successfully."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0


def test_run():
    result = runner.invoke(app, ["run", "-c", "examples/custodian/config.yaml", "examples/custodian/custodian.ttl"])
    with open('examples/custodian/custodian.html', 'r') as f:
        expected = f.read()
    # TODO: compare generated html to example
    # NOTE: so far section ordering does not seem deterministic
    assert result.exit_code == 0
