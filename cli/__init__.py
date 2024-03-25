from __future__ import annotations
import click
import sys
from . import api
from . import ui
from configuration import Configuration
from configuration.environment.types import TEnvironment
from configuration.variables import Variables
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
    Configuration(
        cli={
            Variables.mode: "test",
            **{
                variable: value
                for variable, value in environment.items()
                if value is not None
            },
        },
    )
    return_code = subprocess.call(["pytest", "--asyncio-mode", "auto", "tests"])
    sys.exit(return_code)
