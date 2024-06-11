from api.configuration.variables import Variables
from api.configuration.api.variables import Variables as ApiVariables
from api.configuration.database.variables import Variables as DatabaseVariables
from functools import reduce
import click


def configuration_api_options(command):
    options = (
        click.option(
            "--jwt-private-key",
            ApiVariables.jwt_private_key,
            type=str,
            help="Private key for signing JWTs.",
        ),
        click.option(
            "--jwt-public-key",
            ApiVariables.jwt_public_key,
            type=str,
            help="Public key to verify JWTs.",
        ),
        click.option(
            "--password-pepper",
            ApiVariables.password_pepper,
            type=str,
            help="Pepper used for hashing passwords.",
        ),
        click.option(
            "--api-port",
            ApiVariables.port,
            type=int,
            help="Port for the api to bind to.",
        ),
    )
    return reduce(lambda result, option: option(result), options, command)


def configuration_database_options(command):
    options = (
        click.option(
            "--postgres-username",
            DatabaseVariables.username,
            type=str,
            help="Postgres username.",
        ),
        click.option(
            "--postgres-password",
            DatabaseVariables.password,
            type=str,
            help="Postgres password.",
        ),
        click.option(
            "--postgres-database",
            DatabaseVariables.name,
            type=str,
            help="Postgres database name.",
        ),
        click.option(
            "--postgres-host",
            DatabaseVariables.host,
            type=str,
            help="Hostname for Postgres database location.",
        ),
        click.option(
            "--postgres-port",
            DatabaseVariables.port,
            type=int,
            help="Port used by the Postgres database server.",
        ),
        click.option(
            "--postgres-test-database",
            DatabaseVariables.test,
            type=str,
            help="Postgres database name to run tests against.",
        ),
    )
    return reduce(lambda result, option: option(result), options, command)


@configuration_api_options
@configuration_database_options
def configuration_options(command):
    options = {
        click.option(
            "--mode",
            Variables.mode,
            type=click.Choice(["prod", "dev", "test"]),
            help="The mode in which the application is run in. Development (dev) or production (prod)",
        ),
    }
    return reduce(lambda result, option: option(result), options, command)
