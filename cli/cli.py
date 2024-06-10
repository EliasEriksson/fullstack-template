from __future__ import annotations
from configuration import Configuration
from configuration.environment.types import TEnvironment
from configuration.variables import Variables
from .options import configuration_options
from . import ui
from . import database
from . import api
import subprocess
import sys
import click

cli = click.Group()
cli.add_command(api.cli)
cli.add_command(ui.cli)
cli.add_command(database.cli)


@cli.command()
@configuration_options
def test(**environment: TEnvironment):
    configuration = Configuration(
        cli={
            **{
                variable: value
                for variable, value in environment.items()
                if value is not None
            },
            Variables.mode: "test",
        },
    )
    print("Starting in mode:", configuration.mode)
    return_code = subprocess.call(["pytest", "--asyncio-mode", "auto", "tests"])
    sys.exit(return_code)
