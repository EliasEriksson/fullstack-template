from __future__ import annotations
from collections.abc import AsyncGenerator
from litestar import Litestar, get
from litestar.contrib.sqlalchemy.plugins import SQLAlchemySerializationPlugin
import database
from database import DatabaseConfiguration
from contextlib import asynccontextmanager


# async def database_connection(app: Litestar) -> AsyncGenerator[None, None]:
#
#     try:


@get("/")
async def hello_world() -> str:
    database = DatabaseConfiguration()
    print(database.url)
    return "Hello, world!"


app = Litestar(
    [hello_world],
    plugins=[
        SQLAlchemySerializationPlugin(),
    ],
)
