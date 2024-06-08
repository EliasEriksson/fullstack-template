from database import Database
from api.database import models


async def test_fetch_by_email(database: Database) -> None:
    address = "jessie@rocket.com"
    async with database as session:
        async with session.transaction():
            user = models.User()
            email = models.Email(address=address, user=user)
            await session.emails.create(email)
        id = user.id
    async with database as session:
        async with session.transaction():
            user = await session.users.fetch_by_email(address)

    assert user is not None
    assert user.id == id
