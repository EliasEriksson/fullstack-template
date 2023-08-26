import click
from database import Database
from database import DatabaseConfiguration
import asyncio
from functools import reduce

cli = click.Group("database")


def database_credentials(function):
    options = (
        click.option("--username", "-u", type=str, help="Postgres username."),
        click.option("--password", "-p", type=str, help="Postgres password."),
        click.option("--database", "-d", type=str, help="Postgres database name."),
        click.option(
            "--host", "-h", type=str, help="Hostname for Postgres database location."
        ),
        click.option(
            "--port", "-P", type=int, help="Port used by the Postgres database server."
        ),
    )
    return reduce(lambda result, option: option(result), options, function)


@cli.command()
@database_credentials
def create(**options: str) -> None:
    options = {f"POSTGRES_{name.upper()}": value for name, value in options.items()}
    configuration = DatabaseConfiguration(options)
    database = Database(configuration)
    asyncio.run(database.create())


@cli.command()
@database_credentials
def delete(**options: str) -> None:
    options = {f"POSTGRES_{name.upper()}": value for name, value in options.items()}
    configuration = DatabaseConfiguration(options)
    database = Database(configuration)
    asyncio.run(database.delete())
