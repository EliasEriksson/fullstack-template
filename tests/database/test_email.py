from database import Database
from database import models
from uuid import UUID


async def test_relationship(database: Database) -> None:
    async with database as client:
        async with client.transaction():
            user = models.User()
            email = models.Email(address="jessie@rocket.com", user=user)
            await client.emails.create(email)
        id: UUID = email.id
        assert id is not None
    async with database as client:
        async with client.transaction():
            email: models.Email = await client.emails.fetch_by_id(id)
            assert email is not None
            assert email.user is not None
            await client.users.delete_by_id(email.user.id)
        async with client.transaction():
            email = await client.emails.fetch_by_id(id)
            assert email is None
