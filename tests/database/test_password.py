from database import Database
from database import models
from uuid import UUID


async def test_relationship(database: Database) -> None:
    async with database as client:
        async with client.transaction():
            user = models.User()
            password = models.Password(digest=models.Password.hash("asd123"), user=user)
            await client.passwords.create(password)
        password_id: UUID = password.id
        assert password_id is not None
    async with database as client:
        async with client.transaction():
            password = await client.passwords.fetch_by_id(password_id)
            assert password is not None
            assert password.user is not None
            await client.users.delete_by_id(password.user.id)
        async with client.transaction():
            password = await client.passwords.fetch_by_id(password_id)
            assert password is None


async def test_hash_and_verify() -> None:
    password = "fullstack"
    password_model = models.Password(digest=models.Password.hash(password))
    assert password_model.verify(password) is True
