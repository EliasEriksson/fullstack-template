from __future__ import annotations
from configuration.environment.types import TEnvironment
from api.database import Database
from configuration import Configuration
from .options import configuration_options
import asyncio
from alembic import command
import click


cli = click.Group("database")


@cli.command()
@configuration_options
def create(**environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    database = Database(configuration)
    asyncio.run(database.create())


@cli.command()
@configuration_options
def delete(**environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    message = (
        f"This operation will delete all tables related to this "
        f"application from the database '{configuration.database.name}'.\n"
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
@configuration_options
def revision(message: str | None, **environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    command.revision(
        configuration.database.alembic,
        autogenerate=True,
        message=message,
    )


@cli.command()
@configuration_options
def migrate(**environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    for content in configuration.database.migrations.iterdir():
        if content.is_file():
            break
    else:
        command.revision(
            configuration.database.alembic,
            "Initializing database.",
            autogenerate=True,
        )
    command.upgrade(configuration.database.alembic, "head")


@cli.command()
@click.argument("revision", type=str)
@configuration_options
def upgrade(revision: str, **environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    command.upgrade(configuration.database.alembic, revision)


@cli.command()
@click.argument("revision", type=str, required=True)
@configuration_options
def downgrade(revision: str, **environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    command.downgrade(configuration.database.alembic, revision)


@cli.command()
@configuration_options
def heads(**environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    command.heads(configuration.database.alembic)


@cli.command()
@configuration_options
def check(**environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    command.check(configuration.database.alembic)


@cli.command()
@configuration_options
def branches(**environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    command.branches(configuration.database.alembic)


@cli.command()
@configuration_options
def current(**environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    command.current(configuration.database.alembic)


@cli.command()
@configuration_options
def ensure_version(**environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    command.ensure_version(configuration.database.alembic)


@cli.command()
@click.argument("revision", type=str, required=True)
@configuration_options
def show(revision: str, **environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    command.show(configuration.database.alembic, revision)


@cli.command()
@click.argument("revision", type=str, required=True)
@configuration_options
def stamp(revision: str, **environment: TEnvironment) -> None:
    configuration = Configuration(cli=environment)
    command.stamp(configuration.database.alembic, revision)
