import click
from database import Database
from database import DatabaseConfiguration
import asyncio
from functools import reduce
from alembic.config import Config as AlembicConfiguration
from alembic import command


cli = click.Group("database")


def database_credentials(function):
    options = (
        click.option(
            "--username", "-u", "POSTGRES_USERNAME", type=str, help="Postgres username."
        ),
        click.option(
            "--password", "-p", "POSTGRES_PASSWORD", type=str, help="Postgres password."
        ),
        click.option(
            "--database",
            "-d",
            "POSTGRES_DATABASE",
            type=str,
            help="Postgres database name.",
        ),
        click.option(
            "--host",
            "-h",
            "POSTGRES_HOST",
            type=str,
            help="Hostname for Postgres database location.",
        ),
        click.option(
            "--port",
            "-P",
            "POSTGRES_PORT",
            type=int,
            help="Port used by the Postgres database server.",
        ),
    )
    return reduce(lambda result, option: option(result), options, function)


@cli.command()
@database_credentials
def create(**options: str | int) -> None:
    configuration = DatabaseConfiguration(options)
    database = Database(configuration)
    asyncio.run(database.create())


@cli.command()
@database_credentials
def delete(**options: str | int) -> None:
    configuration = DatabaseConfiguration(options)
    database = Database(configuration)
    asyncio.run(database.delete())


@cli.command()
@database_credentials
def revision(**options: str | int) -> None:
    configuration = DatabaseConfiguration(options)
    alembic_configuration = AlembicConfiguration()
    command.revision()
    # options = {f"POSTGRES_{name.upper()}": value for name, value in options.items()}
