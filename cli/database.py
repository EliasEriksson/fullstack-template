import click

cli = click.Group("database")


@cli.command()
def create():
    pass


@cli.command()
def delete():
    pass
