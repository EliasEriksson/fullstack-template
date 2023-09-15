import pytest
from database import models
from sqlalchemy import select
from database import Database


@pytest.fixture
async def database():
    database = Database()
    await database.create()
    yield database
    await database.delete()


async def test_user(database: Database) -> None:
    async with database._session() as session:
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
