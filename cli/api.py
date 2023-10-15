from __future__ import annotations
from typing import *
from typing import Literal
from functools import reduce
import uvicorn
import click
from database.configuration import DatabaseConfiguration
from api.configuration import ApiConfiguration
from .database import database_configuration

cli = click.Group("api")


def api_configuration(command):
    options = (
        click.option(
            "--jwt-private-key",
            "JWT_PRIVATE_KEY",
            type=str,
            help="Private key for signing JWTs.",
        ),
        click.option(
            "--jwt-public-key",
            "JWT_PUBLIC_KEY",
            type=str,
            help="Public key to verify JWTs.",
        ),
        click.option(
            "--password-pepper",
            "PASSWORD_PEPPER",
            type=str,
            help="Pepper used for hashing passwords.",
        ),
    )
    return reduce(lambda result, option: option(result), options, command)


@cli.command()
@database_configuration
@api_configuration
@click.argument("mode", type=click.Choice(["prod", "dev"]), default="dev")
@click.option("--port", type=int, default=8080)
def start(
    mode: Literal["prod"] | Literal["dev"], port: int, **environment: dict[str, Any]
) -> None:
    DatabaseConfiguration(environment=environment)
    if mode == "prod":
        ApiConfiguration(environment=environment, secure=True)
        uvicorn.run("api:api", port=port, log_level="info")
    else:
        ApiConfiguration(environment=environment, secure=False)
        uvicorn.run("api:api", reload=True, port=port, log_level="info")
