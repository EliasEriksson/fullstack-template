import click
from database import Database
from database import DatabaseConfiguration
import asyncio
from functools import reduce
from alembic import command


cli = click.Group("database")


def database_credentials(command):
    options = (
        click.option(
            "--postgres-username",
            "-u",
            "POSTGRES_USERNAME",
            type=str,
            help="Postgres username.",
        ),
        click.option(
            "--postgres-password",
            "-p",
            "POSTGRES_PASSWORD",
            type=str,
            help="Postgres password.",
        ),
        click.option(
            "--postgres-database",
            "-d",
            "POSTGRES_DATABASE",
            type=str,
            help="Postgres database name.",
        ),
        click.option(
            "--postgres-host",
            "-h",
            "POSTGRES_HOST",
            type=str,
            help="Hostname for Postgres database location.",
        ),
        click.option(
            "--postgres-port",
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
    message = (
        f"This operation will delete all tables related to this "
        f"application from the database '{configuration.database}'.\n"
        f"OBS! This operation is irreversible.\n"
        f"Are you sure you want to continue? (y/n): "
    )
    if input(message).lower() == "y":
        print("Proceeding...")
        database = Database(configuration)
        asyncio.run(database.delete())
        print("Database deleted.")
    else:
        print("Aborted.")


@cli.command()
@click.option("--message", "-m", type=str, help="Revision message", default=None)
@database_credentials
def revision(message: str | None, **credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    command.revision(
        configuration.alembic,
        autogenerate=True,
        message=message,
    )


@cli.command()
@database_credentials
def migrate(**credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    for content in configuration.migrations.iterdir():
        if content.is_file():
            break
    else:
        command.revision(
            configuration.alembic,
            "Initializing database.",
            autogenerate=True,
        )
    command.upgrade(configuration.alembic, "head")


@cli.command()
@click.argument("revision", type=str)
@database_credentials
def upgrade(revision: str, **credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    command.upgrade(configuration.alembic, revision)


@cli.command()
@click.argument("revision", type=str, required=True)
@database_credentials
def downgrade(revision: str, **credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    command.downgrade(configuration.alembic, revision)


@cli.command()
@database_credentials
def heads(**credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    command.heads(configuration.alembic)


@cli.command()
@database_credentials
def check(**credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    command.check(configuration.alembic)


@cli.command()
@database_credentials
def branches(**credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    command.branches(configuration.alembic)


@cli.command()
@database_credentials
def current(**credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    command.current(configuration.alembic)


@cli.command()
@database_credentials
def ensure_version(**credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    command.ensure_version(configuration.alembic)


@cli.command()
@click.argument("revision", type=str, required=True)
@database_credentials
def show(revision: str, **credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    command.show(configuration.alembic, revision)


@cli.command()
@click.argument("revision", type=str, required=True)
@database_credentials
def stamp(revision: str, **credentials: str | int) -> None:
    configuration = DatabaseConfiguration(credentials)
    command.stamp(configuration.alembic, revision)
