import click
from database import Database
from database import DatabaseConfiguration
import asyncio
from functools import reduce
from alembic.config import Config as AlembicConfiguration
from alembic import command


cli = click.Group("database")


def database_credentials(command):
    options = (
        click.option(
            "--username",
            "-u",
            "POSTGRES_USERNAME",
            type=str,
            help="Postgres username.",
        ),
        click.option(
            "--password",
            "-p",
            "POSTGRES_PASSWORD",
            type=str,
            help="Postgres password.",
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
    return reduce(lambda result, option: option(result), options, command)


@cli.command()
@database_credentials
def create(**credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    database = Database(configuration)
    asyncio.run(database.create())


@cli.command()
@database_credentials
def delete(**credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    database = Database(configuration)
    asyncio.run(database.delete())


@cli.command()
@click.option("--message", "-m", type=str, help="Revision message", default=None)
@database_credentials
def revision(message: str | None, **credentials: str | int) -> None:
    DatabaseConfiguration(credentials)
    command.revision(
        AlembicConfiguration("./alembic.ini"),
        autogenerate=True,
        message=message,
    )


# merge these commands
@cli.command()
@click.argument("revision", type=str, help="Revision id.", default="head")
@database_credentials
def migrate(revision: str, **credentials: str | int) -> None:
    DatabaseConfiguration(credentials)
    command.upgrade(AlembicConfiguration("./alembic.ini"), revision)


@cli.command()
@click.argument("revision", type=str, help="alembic revision.", required=True)
@database_credentials
def downgrade(revision: str, **credentials: str | int) -> None:
    DatabaseConfiguration(credentials)
    command.downgrade(AlembicConfiguration("./alembic.ini"), revision)
