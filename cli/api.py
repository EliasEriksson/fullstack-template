from __future__ import annotations
from api.configuration.environment.types import TEnvironment
from api.configuration import Configuration
from .options import configuration_options
import uvicorn
import click

cli = click.Group("api")


@cli.command()
@configuration_options
def start(**environment: TEnvironment) -> None:
    Configuration(cli=environment)
    configuration = Configuration(cli=environment)
    print("Starting in mode:", configuration.mode)
    uvicorn.run(
        "api:api",
        port=configuration.api.port,
        log_level="info",
        reload=configuration.mode == "dev",
        proxy_headers=True,
    )
