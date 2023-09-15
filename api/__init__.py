from __future__ import annotations
from litestar import Litestar, Router
from litestar.contrib.sqlalchemy.plugins import SQLAlchemySerializationPlugin
from . import endpoints
from litestar.openapi import OpenAPIConfig
from litestar import get


@get("/hello")
async def hello() -> str:
    return "hello world"


app = Litestar(
    [
        hello,
        Router(
            path="/users",
            route_handlers=[endpoints.Users],
        ),
    ],
    openapi_config=OpenAPIConfig(title="lite-star", version="0.0.0", path="/"),
    plugins=[
        SQLAlchemySerializationPlugin(),
    ],
)
