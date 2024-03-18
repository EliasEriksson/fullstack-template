from __future__ import annotations

import os
from typing import *
import click
import sys
from . import api
from . import ui
from configuration import Configuration
from configuration.environment.types import TEnvironment
from configuration.variables import Variables

# from shared.configuration.environment import TEnvironment
# from shared.configuration import Configuration
# from shared.configuration.configuration import Variables

# from database.configuration_old import DatabaseConfiguration
# from database.configuration_old import Variables
# from api.configuration import ApiConfiguration
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
    return_code = subprocess.call(["pytest", "--asyncio-mode", "auto"])
    sys.exit(return_code)
