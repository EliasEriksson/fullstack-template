import click
import database

cli = click.Group("database")


@cli.command()
def create():
    database.models.Base.metadata.create_all(database.engine)


@cli.command()
def delete():
    database.models.Base.metadata.drop_all(database.engine)
