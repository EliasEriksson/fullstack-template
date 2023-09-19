from __future__ import annotations
from litestar import Litestar, Router
from litestar.contrib.sqlalchemy.plugins import SQLAlchemySerializationPlugin
from . import routes
from litestar.openapi import OpenAPIConfig

app = Litestar(
    route_handlers=[
        Router(path="/users", route_handlers=[routes.users.Controller]),
    ],
    openapi_config=OpenAPIConfig(
        title="lite-star",
        version="0.0.0",
        path="/",
    ),
    plugins=[
        SQLAlchemySerializationPlugin(),
    ],
    debug=True,
)
