import click
import sys
from . import api
from . import ui
from database.configuration import DatabaseConfiguration
from . import database
import subprocess

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
    DatabaseConfiguration(credentials)
    return_code = subprocess.call(["pytest", "--asyncio-mode", "auto"])
    sys.exit(return_code)
