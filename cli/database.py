from __future__ import annotations
import click
from shared.configuration.environment import TEnvironment
from database import Database
from database import DatabaseConfiguration
from database import Variables
import asyncio
from functools import reduce
from alembic import command


cli = click.Group("database")


def database_configuration(command):
    options = (
        click.option(
            "--postgres-username",
            Variables.username,
            type=str,
            help="Postgres username.",
        ),
        click.option(
            "--postgres-password",
            Variables.password,
            type=str,
            help="Postgres password.",
        ),
        click.option(
            "--postgres-database",
            Variables.database,
            type=str,
            help="Postgres database name.",
        ),
        click.option(
            "--postgres-host",
            Variables.host,
            type=str,
            help="Hostname for Postgres database location.",
        ),
        click.option(
            "--postgres-port",
            Variables.port,
            type=int,
            help="Port used by the Postgres database server.",
        ),
        click.option(
            "--postgres-test-database",
            Variables.test_database,
            type=str,
            help="Postgres database name to run tests against.",
        ),
    )
    return reduce(lambda result, option: option(result), options, command)


@cli.command()
@database_configuration
def create(**environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # database = Database(configuration)
    # asyncio.run(database.create())


@cli.command()
@database_configuration
def delete(**environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # message = (
    #     f"This operation will delete all tables related to this "
    #     f"application from the database '{configuration.database}'.\n"
    #     f"OBS! This operation is irreversible.\n"
    #     f"Are you sure you want to continue? (y/n): "
    # )
    # if input(message).lower() == "y":
    #     print("Proceeding...")
    #     database = Database(configuration)
    #     asyncio.run(database.delete())
    #     print("Database deleted.")
    # else:
    #     print("Aborted.")


@cli.command()
@click.option("--message", "-m", type=str, help="Revision message", default=None)
@database_configuration
def revision(message: str | None, **environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # command.revision(
    #     configuration.alembic,
    #     autogenerate=True,
    #     message=message,
    # )


@cli.command()
@database_configuration
def migrate(**environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # for content in configuration.migrations.iterdir():
    #     if content.is_file():
    #         break
    # else:
    #     command.revision(
    #         configuration.alembic,
    #         "Initializing database.",
    #         autogenerate=True,
    #     )
    # command.upgrade(configuration.alembic, "head")


@cli.command()
@click.argument("revision", type=str)
@database_configuration
def upgrade(revision: str, **environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # command.upgrade(configuration.alembic, revision)


@cli.command()
@click.argument("revision", type=str, required=True)
@database_configuration
def downgrade(revision: str, **environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # command.downgrade(configuration.alembic, revision)


@cli.command()
@database_configuration
def heads(**environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # command.heads(configuration.alembic)


@cli.command()
@database_configuration
def check(**environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # command.check(configuration.alembic)


@cli.command()
@database_configuration
def branches(**environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # command.branches(configuration.alembic)


@cli.command()
@database_configuration
def current(**environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # command.current(configuration.alembic)


@cli.command()
@database_configuration
def ensure_version(**environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # command.ensure_version(configuration.alembic)


@cli.command()
@click.argument("revision", type=str, required=True)
@database_configuration
def show(revision: str, **environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # command.show(configuration.alembic, revision)


@cli.command()
@click.argument("revision", type=str, required=True)
@database_configuration
def stamp(revision: str, **environment: TEnvironment) -> None:
    pass
    # configuration = DatabaseConfiguration(cli=environment)
    # command.stamp(configuration.alembic, revision)
