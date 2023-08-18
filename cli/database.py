import click
import database
import asyncio

cli = click.Group("database")


@cli.command()
def create():
    asyncio.run(database.create())


@cli.command()
def delete():
    asyncio.run(database.delete())
