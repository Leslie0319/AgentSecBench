from typer.testing import CliRunner

from agentsecbench.cli import app

runner = CliRunner()


def test_run_subcommand_is_exposed() -> None:
    result = runner.invoke(app, ["run", "--help"])
    assert result.exit_code == 0
    assert "Run one benchmark experiment" in result.stdout
