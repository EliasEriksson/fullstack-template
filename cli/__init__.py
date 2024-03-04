from __future__ import annotations
from typing import *
import click
import sys
from . import api
from . import ui
from shared.configuration.environment import TEnvironment
from database.configuration import DatabaseConfiguration
from database.configuration import Variables
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
def test(**environment: TEnvironment):
    DatabaseConfiguration(
        cli=environment,
        defaults={
            Variables.database: "lite-star-test",
        },
    )
    ApiConfiguration(
        cli=environment,
    )
    return_code = subprocess.call(["pytest", "--asyncio-mode", "auto"])
    sys.exit(return_code)
