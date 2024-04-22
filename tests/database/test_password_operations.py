from database import Database
from database import models
from uuid import UUID


async def test_relationship(database: Database) -> None:
    async with database as session:
        async with session.transaction():
            user = models.User()
            password = models.Password(digest=models.Password.hash("asd123"), user=user)
            await session.passwords.create(password)
        password_id: UUID = password.id
        assert password_id is not None
    async with database as session:
        async with session.transaction():
            password: models.Password = await session.passwords.fetch(password_id)
            assert password is not None
            assert password.user is not None
            await session.users.delete_by_id(password.user.id)
        async with session.transaction():
            password = await session.passwords.fetch(password_id)
            assert password is None
