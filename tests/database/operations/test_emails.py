from database import Database
from database import models
from uuid import UUID


async def test_emails(database: Database) -> None:
    async with database as session:
        async with session.transaction():
            user = models.User()
            await session.users.create(user)
            email = models.Email(address="jessie@rocket.com", user=user)
            await session.users.create(user)
        async with session.transaction():
            fetched_user = await session.users.fetch(user.id)
            fetched_email = await session.emails.fetch(email.id)
            assert user == fetched_user
            assert email == fetched_email
            assert email in user.emails


async def test_relationship(database: Database) -> None:
    async with database as session:
        async with session.transaction():
            user = models.User()
            email = models.Email(address="jessie@rocket.com", user=user)
            await session.emails.create(email)
        email_id: UUID = email.id
        assert email_id is not None
    async with database as session:
        async with session.transaction():
            email: models.Email = await session.emails.fetch(email_id)
            assert email is not None
            assert email.user is not None
            await session.users.delete_by_id(email.user.id)
        async with session.transaction():
            email = await session.emails.fetch(email_id)
            assert email is None
