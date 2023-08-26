import click
from database import Database
from database import DatabaseConfiguration
import asyncio

cli = click.Group("database")


@cli.command()
@click.option("--username", "-u")
@click.option("--password", "-p")
@click.option("--host", "-h")
@click.option("--port", "-P")
@click.option("--database", "-d")
def create(**options: str) -> None:
    options = {f"POSTGRES_{name.upper()}": value for name, value in options.items()}
    configuration = DatabaseConfiguration(options)
    database = Database(configuration)
    asyncio.run(database.create())


@cli.command()
@click.option("--username", "-u")
@click.option("--password", "-p")
@click.option("--host", "-h")
@click.option("--port", "-P")
@click.option("--database", "-d")
def delete(**options) -> None:
    options = {f"POSTGRES_{name.upper()}": value for name, value in options.items()}
    configuration = DatabaseConfiguration(options)
    database = Database(configuration)
    asyncio.run(database.delete())
