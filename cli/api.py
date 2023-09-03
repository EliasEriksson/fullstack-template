from typing import Literal
import uvicorn
import click


cli = click.Group("api")


@cli.command()
@click.argument("mode", type=click.Choice(["prod", "dev"]), default="dev")
@click.option("-p", "--port", type=int, default=8080)
def start(mode: Literal["prod"] | Literal["dev"], port: int) -> None:
    if mode == "prod":
        uvicorn.run("api:app", port=port, log_level="info")
    else:
        uvicorn.run("api:app", reload=True, port=port, log_level="info")
