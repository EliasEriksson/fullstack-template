import os
from typing import Literal
import uvicorn
import click
from database import DatabaseConfiguration


cli = click.Group("api")


@cli.command()
@click.argument("mode", type=click.Choice(["prod", "dev"]), default="dev")
@click.option("-p", "--port", type=int, default=8080)
def start(mode: Literal["prod"] | Literal["dev"], port: int) -> None:
    configuration = DatabaseConfiguration(environment={"host": "whatever"})
    os.environ["TESTING"] = "VALUE"
    print(os.environ["TESTING"])
    if mode == "prod":
        uvicorn.run("api:app", port=port, log_level="info")
    else:
        uvicorn.run("api:app", reload=True, port=port, log_level="info")
