from database import Database
from database import models
from ..test_database import empty_database
from shared import hash
import pytest


@pytest.fixture
async def database(empty_database: Database) -> None:
    async with empty_database as session:
        async with session.transaction():
            emails = [
                models.Email(
                    address="jessie@rocket.com", verification=models.Verification()
                ),
                models.Email(
                    address="james@rocket.com", verification=models.Verification()
                ),
                models.Email(
                    address="giovani@rocket.com", verification=models.Verification()
                ),
            ]
            for email in emails:
                await session.users.create(
                    models.User(emails=[email], hash=hash.password("asd123"))
                )
    yield empty_database


async def test_list(database: Database) -> None:
    async with database as session:
        users, page = await session.users.list([], 10, 0)
        assert len(users) == 3
        assert page.next is None
        users, page = await session.users.list([], 1, 0)
        assert len(users) == 1
        assert page.last == 2
        users, page = await session.users.list(["jessie@rocket.com"], 10, 0)
        assert len(users) == 1
        assert page.next is None
        users, page = await session.users.list(
            ["jessie@rocket.com", "james@rocket.com"], 10, 0
        )
        assert len(users) == 2
        users, page = await session.users.list(
            ["jessie@rocket.com", "james@rocket.com"], 1, 0
        )
        assert len(users) == 1
        assert page.next == 1


async def test_fetch(database: Database) -> None:
    async with database as session:
        users, page = await session.users.list([], 3, 0)
        assert len(users) == 3
        fetched = [await session.users.fetch_by_id(user.id) for user in users]
        assert any(
            (
                "jessie@rocket.com" in [email.address for email in user.emails]
                for user in fetched
            )
        )
        assert any(
            (
                "james@rocket.com" in [email.address for email in user.emails]
                for user in fetched
            )
        )
        assert any(
            (
                "giovani@rocket.com" in [email.address for email in user.emails]
                for user in fetched
            )
        )
