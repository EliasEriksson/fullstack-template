import click


cli = click.Group("api")


@cli.command()
@click.option("-p", "--port", default=8080)
def start(port) -> None:
    click.echo(f"api start {port}")
