from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from litestar import Litestar, get
from litestar.contrib.sqlalchemy.plugins import SQLAlchemySerializationPlugin
import database
from database import DatabaseConfiguration
from contextlib import asynccontextmanager


@get("/")
async def hello_world() -> str:
    database = DatabaseConfiguration()
    print("env", os.environ["TESTING"])
    # print(database.url)
    return "Hello, world!"


app = Litestar(
    [hello_world],
    plugins=[
        SQLAlchemySerializationPlugin(),
    ],
)
