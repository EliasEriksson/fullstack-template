import click
import database

cli = click.Group("database")


@cli.command()
def create():
    database.create()


@cli.command()
def delete():
    database.delete()
