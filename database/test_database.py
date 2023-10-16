import pytest
from database import models
from database import Database
from shared import hash
from .configuration import DatabaseConfiguration
from sqlalchemy import literal_column
from sqlalchemy import select


@pytest.fixture
async def empty_database():
    database = Database()
    await database.create()
    yield database
    await database.delete()


@pytest.fixture
async def database(empty_database: Database) -> None:
    async with Database() as session:
        async with session.transaction():
            emails = [
                models.Email(address="jessie@rocket.com"),
                models.Email(address="james@rocket.com"),
                models.Email(address="giovani@rocket.com"),
            ]
            for email in emails:
                await session.users.create(
                    models.User(emails=[email], hash=hash.password("asd123"))
                )
    yield empty_database


async def test_database(empty_database: Database) -> None:
    configuration = DatabaseConfiguration()
    async with empty_database as session:
        query = select(literal_column("current_user"))
        result = await session.execute(query)
        user = result.scalars().one_or_none()
        assert user == configuration.username
