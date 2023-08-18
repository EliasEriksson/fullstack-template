import pytest
from . import create
from . import delete
from .session import Session
from . import models
from sqlalchemy import select


@pytest.fixture
async def setup():
    await create()
    yield None
    await delete()


async def test_user(setup: None) -> None:
    async with Session() as session:
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
