from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from typing import *
from . import models
from .configuration import Configuration
import os


class Database(Configuration):
    engine: AsyncEngine
    session: async_sessionmaker[AsyncSession]

    def __init__(self, environment: Optional[dict[str, str]] = None) -> None:
        super().__init__(environment)
        username = self.string("POSTGRES_USERNAME")
        password = self.string("POSTGRES_PASSWORD")
        database = self.string("POSTGRES_DATABASE")
        host = self.string("POSTGRES_HOST")
        port = self.integer("POSTGRES_PORT")
        self.engine = create_async_engine(
            f"postgresql+psycopg://{username}:{password}@{host}:{port}/{database}",
            echo=True,
        )
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(models.Base.metadata.create_all)

    async def delete(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(models.Base.metadata.drop_all)
