import pytest
from database import models
from sqlalchemy import select
from configuration import Configuration
from database import Database
from shared import hash


async def test_user(database: Database) -> None:
    print("USED CONNECTION URL:", Configuration().database.url)
    async with database._session_maker() as session:
        users = await session.execute(select(models.User))
        assert len(users.scalars().all()) == 0
        await session.commit()

        async with session.begin():
            users = [
                models.User(email="jessie@rocket.com", hash=hash.password("asd123")),
                models.User(email="james@rocket.com", hash=hash.password("asd123")),
                models.User(email="giovani@rocket.com", hash=hash.password("asd123")),
            ]
            session.add_all(users)

        users = await session.execute(select(models.User))
        assert len(users.scalars().all()) == 3
        await session.commit()
