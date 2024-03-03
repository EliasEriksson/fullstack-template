from __future__ import annotations
from functools import reduce
import uvicorn
import click
from shared.configuration.environment import TEnvironment
from database.configuration import DatabaseConfiguration
from api.configuration import ApiConfiguration
from api.configuration import Variables
from .database import database_configuration

cli = click.Group("api")


def api_configuration(command):
    options = (
        click.option(
            "--jwt-private-key",
            Variables.jwt_private_key,
            type=str,
            help="Private key for signing JWTs.",
        ),
        click.option(
            "--jwt-public-key",
            Variables.jwt_public_key,
            type=str,
            help="Public key to verify JWTs.",
        ),
        click.option(
            "--password-pepper",
            Variables.password_pepper,
            type=str,
            help="Pepper used for hashing passwords.",
        ),
        click.option(
            "--mode",
            Variables.mode,
            type=click.Choice(["prod", "dev"]),
            help="THe mode in which the application is run in. Development (dev) or production (prod)",
        ),
        click.option(
            "--api-port",
            Variables.port,
            type=int,
            help="Port for the api to bind to.",
        ),
    )
    return reduce(lambda result, option: option(result), options, command)


@cli.command()
@database_configuration
@api_configuration
def start(**environment: TEnvironment) -> None:
    DatabaseConfiguration(cli=environment)
    api = ApiConfiguration(cli=environment)
    uvicorn.run("api:api", port=api.port, log_level="info")
