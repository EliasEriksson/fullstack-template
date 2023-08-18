from . import models
from .engine import engine


async def create() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(models.Base.metadata.create_all)


async def delete() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(models.Base.metadata.drop_all)
