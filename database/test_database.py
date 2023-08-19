import asyncio

import pytest
from . import create
from . import delete
from . import models
from sqlalchemy import select
from . import Database


@pytest.fixture
async def database():
    environment = {
        "POSTGRES_USERNAME": "lite-star",
        "POSTGRES_PASSWORD": "lite-star",
        "POSTGRES_DATABASE": "lite-star-test",
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": "5432",
    }
    database = Database(environment)
    await create(database)
    yield database
    await delete(database)


async def test_user(database: Database) -> None:
    async with database.session() as session:
        users = await session.execute(select(models.User))
        assert len(users.scalars().all()) == 0
        await session.commit()

        async with session.begin():
            users = [
                models.User(email="jessie@rocket.com"),
                models.User(email="james@rocket.com"),
                models.User(email="giovani@rocket.com"),
            ]
            session.add_all(users)

        users = await session.execute(select(models.User))
        assert len(users.scalars().all()) == 3
        await session.commit()
