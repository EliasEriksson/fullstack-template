from database import Database
from database import models
from uuid import UUID


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
