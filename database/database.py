from . import DatabaseConfiguration
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from . import models
from .users import Users


class Database:
    _configuration: DatabaseConfiguration
    _engine: AsyncEngine
    _session: async_sessionmaker[AsyncSession]
    users: Users

    def __init__(self, configuration: DatabaseConfiguration | None = None) -> None:
        self._configuration = (
            configuration if configuration is not None else DatabaseConfiguration()
        )
        self._engine = create_async_engine(self._configuration.url, echo=True)
        self._session = async_sessionmaker(self._engine, expire_on_commit=False)
        self.users = Users(self._engine, self._session)

    async def create(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(models.Base.metadata.create_all)

    async def delete(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(models.Base.metadata.drop_all)
            drop_alembic = text(f"DROP TABLE IF EXISTS alembic_version;")
            await connection.execute(drop_alembic)

        migrations = self._configuration.migrations
        if migrations.exists():
            for content in migrations.iterdir():
                if content.is_file():
                    content.unlink()

    async def dispose(self) -> None:
        await self._engine.dispose()
