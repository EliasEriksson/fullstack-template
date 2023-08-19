import asyncio

import pytest
from . import models
from sqlalchemy import select
from . import Database
from .configuration import ConfigurationError
import os


@pytest.fixture
async def database():
    # this is ugly. load this value from test cli
    environment = {
        "POSTGRES_DATABASE": os.environ["POSTGRES_TEST_DATABASE"]
        if "POSTGRES_TEST_DATABASE" in os.environ
        else "lite-star-test",
    }
    try:
        database = Database(environment)
    except ConfigurationError:
        environment = {
            **environment,
            "POSTGRES_USERNAME": "lite-star",
            "POSTGRES_PASSWORD": "lite-star",
            "POSTGRES_HOST": "localhost",
            "POSTGRES_PORT": "5432",
        }
        database = Database(environment)
    await database.create()
    yield database
    await database.delete()


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
