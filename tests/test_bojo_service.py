import pytest
from typer.testing import CliRunner
from bojo import __app_name__, __version__, cli

runner = CliRunner()

@pytest.mark.cli
def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout