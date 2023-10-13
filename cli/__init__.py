from __future__ import annotations
from typing import *
import click
import sys
from . import api
from . import ui
from database.configuration import DatabaseConfiguration
from api.configuration import ApiConfiguration
from . import database
import subprocess

cli = click.Group()
cli.add_command(api.cli)
cli.add_command(ui.cli)
cli.add_command(database.cli)


@cli.command()
@database.database_configuration
@api.api_configuration
@click.option(
    "--database",
    "-d",
    "POSTGRES_DATABASE",
    default="lite-star-test",
    type=str,
    help="Postgres database name.",
)
def test(**environment: dict[str, Any]):
    DatabaseConfiguration(environment)
    ApiConfiguration(environment, secure=False)
    return_code = subprocess.call(["pytest", "--asyncio-mode", "auto"])
    sys.exit(return_code)
