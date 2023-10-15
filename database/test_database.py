import pytest
from database import models
from sqlalchemy import select
from database import Database
from shared import hash


@pytest.fixture
async def database():
    database = Database()
    await database.create()
    yield database
    await database.delete()


async def test_user(database: Database) -> None:
    async with Database() as session:
        async with session.transaction():
            users, page = await session.users.list([], 10, 0)
            print(users)
            assert len(users) == 0

            emails = [
                "jessie@rocket.com",
                "james@rocket.com",
                "giovani@rocket.com",
            ]
            for email in emails:
                await session.users.create(
                    models.User(email=email, hash=hash.password("asd123")),
                )
            # await session.commit()
        # await session.commit()
        # users, page = await session.users.list([], 10, 1)
        # assert len(users) == 3
