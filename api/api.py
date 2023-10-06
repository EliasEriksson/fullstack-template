from __future__ import annotations
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemySerializationPlugin
from . import routes
from litestar.openapi import OpenAPIConfig
from litestar.openapi import OpenAPIController
from litestar.static_files.config import StaticFilesConfig
from pathlib import Path


class DocumentationController(OpenAPIController):
    path = "/api/"
    favicon_url = "/static/favicon.png"


api = Litestar(
    route_handlers=[routes.router],
    static_files_config=[
        StaticFilesConfig(
            directories=[Path("api/static")],
            path="static",
        )
    ],
    openapi_config=OpenAPIConfig(
        title="Litestar template",
        version="0.0.0",
        root_schema_site="elements",
        openapi_controller=DocumentationController,
    ),
    debug=True,
)
