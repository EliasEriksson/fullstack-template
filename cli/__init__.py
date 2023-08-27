import click
import sys
import pytest
from . import api
from . import ui
from . import database

cli = click.Group()
cli.add_command(api.cli)
cli.add_command(ui.cli)
cli.add_command(database.cli)


@cli.command()
@database.database_credentials
@click.option(
    "--database",
    "-d",
    "POSTGRES_DATABASE",
    default="lite-star-test",
    type=str,
    help="Postgres database name.",
)
def test(**credentials: str):
    database.DatabaseConfiguration(credentials)
    return_code = pytest.main(["--asyncio-mode", "auto"])
    sys.exit(return_code)
