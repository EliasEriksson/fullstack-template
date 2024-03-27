from __future__ import annotations
from configuration import Configuration
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from . import models
from .session import Session


class Database:
    _configuration: Configuration
    _engine: AsyncEngine
    _session_maker: async_sessionmaker[AsyncSession]
    _session: AsyncSession | None

    def __init__(self, configuration: Configuration | None = None) -> None:
        self._configuration = (
            configuration if configuration is not None else Configuration()
        )
        self._engine = create_async_engine(self._configuration.database.url, echo=False)
        self._session_maker = async_sessionmaker(self._engine, expire_on_commit=False)

    async def create(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(models.Base.metadata.create_all)

    async def delete(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(models.Base.metadata.drop_all)
            drop_alembic = text(f"DROP TABLE IF EXISTS alembic_version;")
            await connection.execute(drop_alembic)

        migrations = self._configuration.database.migrations
        if migrations.exists():
            for content in migrations.iterdir():
                if content.is_file():
                    content.unlink()

    async def __aenter__(self) -> Session:
        self._session = await self._session_maker(bind=self._engine).__aenter__()
        return Session(self._session)

    async def __aexit__(self, *args, **kwargs) -> None:
        if self._session:
            await self._session.__aexit__(*args, **kwargs)

    async def dispose(self) -> None:
        await self._engine.dispose()
