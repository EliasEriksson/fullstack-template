import click
from database import Database
import asyncio

cli = click.Group("database")

# probably revert this. only environment variables!
@cli.command()
@click.option("--username", "-u", default="lite-star")
@click.option("--password", "-p", default="lite-star")
@click.option("--host", "-h", default="localhost")
@click.option("--port", "-P", default="5432")
@click.option("--database", "-d", default="lite-star")
def create(**options: str) -> None:
    options = {f"POSTGRES_{name.upper()}": value for name, value in options.items()}
    database = Database(options)
    asyncio.run(database.create())


@cli.command()
@click.option("--username", "-u", default="lite-star")
@click.option("--password", "-p", default="lite-star")
@click.option("--host", "-h", default="localhost")
@click.option("--port", "-P", default="5432")
@click.option("--database", "-d", default="lite-star")
def delete(**options) -> None:
    options = {f"POSTGRES_{name.upper()}": value for name, value in options.items()}
    database = Database(options)
    asyncio.run(database.delete())
