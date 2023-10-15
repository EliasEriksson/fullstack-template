from __future__ import annotations
from typing import *
import click
from database import Database
from database import DatabaseConfiguration
import asyncio
from functools import reduce
from alembic import command


cli = click.Group("database")


def database_configuration(command):
    options = (
        click.option(
            "--postgres-username",
            "POSTGRES_USERNAME",
            type=str,
            help="Postgres username.",
        ),
        click.option(
            "--postgres-password",
            "POSTGRES_PASSWORD",
            type=str,
            help="Postgres password.",
        ),
        click.option(
            "--postgres-database",
            "POSTGRES_DATABASE",
            type=str,
            help="Postgres database name.",
        ),
        click.option(
            "--postgres-host",
            "POSTGRES_HOST",
            type=str,
            help="Hostname for Postgres database location.",
        ),
        click.option(
            "--postgres-port",
            "POSTGRES_PORT",
            type=int,
            help="Port used by the Postgres database server.",
        ),
    )
    return reduce(lambda result, option: option(result), options, command)


@cli.command()
@database_configuration
def create(**environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
    database = Database(configuration)
    asyncio.run(database.create())


@cli.command()
@database_configuration
def delete(**environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
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
@database_configuration
def revision(message: str | None, **environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
    command.revision(
        configuration.alembic,
        autogenerate=True,
        message=message,
    )


@cli.command()
@database_configuration
def migrate(**environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
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
@database_configuration
def upgrade(revision: str, **environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
    command.upgrade(configuration.alembic, revision)


@cli.command()
@click.argument("revision", type=str, required=True)
@database_configuration
def downgrade(revision: str, **environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
    command.downgrade(configuration.alembic, revision)


@cli.command()
@database_configuration
def heads(**environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
    command.heads(configuration.alembic)


@cli.command()
@database_configuration
def check(**environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
    command.check(configuration.alembic)


@cli.command()
@database_configuration
def branches(**environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
    command.branches(configuration.alembic)


@cli.command()
@database_configuration
def current(**environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
    command.current(configuration.alembic)


@cli.command()
@database_configuration
def ensure_version(**environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
    command.ensure_version(configuration.alembic)


@cli.command()
@click.argument("revision", type=str, required=True)
@database_configuration
def show(revision: str, **environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
    command.show(configuration.alembic, revision)


@cli.command()
@click.argument("revision", type=str, required=True)
@database_configuration
def stamp(revision: str, **environment: dict[str, Any]) -> None:
    configuration = DatabaseConfiguration(environment)
    command.stamp(configuration.alembic, revision)
