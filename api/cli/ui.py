import click

cli = click.Group("ui")


@cli.command()
def install():
    pass


@cli.command()
def start():
    pass


@cli.command()
def build():
    pass


@cli.command()
def npm():
    pass
