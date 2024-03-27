from __future__ import annotations
from configuration.environment.types import TEnvironment
from configuration import Configuration
from .options import configuration_options
import uvicorn
import click

cli = click.Group("api")


@cli.command()
@configuration_options
def start(**environment: TEnvironment) -> None:
    Configuration(cli=environment)
    configuration = Configuration(cli=environment)
    uvicorn.run("api:api", port=configuration.api.port, log_level="info")
