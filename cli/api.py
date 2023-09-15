from typing import Literal
from functools import reduce
import uvicorn
import click
from database.configuration import DatabaseConfiguration

cli = click.Group("api")


def database_credentials(command):
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
@database_credentials
@click.argument("mode", type=click.Choice(["prod", "dev"]), default="dev")
@click.option("-p", "--port", type=int, default=8080)
def start(
    mode: Literal["prod"] | Literal["dev"], port: int, **credentials: dict[str, any]
) -> None:
    DatabaseConfiguration(environment=credentials)
    if mode == "prod":
        uvicorn.run("api:app", port=port, log_level="info")
    else:
        uvicorn.run("api:app", reload=True, port=port, log_level="info")
