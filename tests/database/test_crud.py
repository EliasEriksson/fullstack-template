from database import Database
from database import models


async def test_crud(database: Database) -> None:
    async with database as client:
        async with client.transaction():
            users, page = await client.users.list(10, 0)
            assert len(users) == 0
            for user in (models.User() for _ in range(3)):
                await client.users.create(user)
        async with client.transaction():
            users, page = await client.users.list(1, 1)
            assert len(users) == 1
            assert page.previous == 0
            assert page.current == 1
            assert page.next == 2
            assert page.last == 2
            assert page.size == 1
            for user in users:
                await client.users.delete(user)
        async with client.transaction():
            users, page = await client.users.list(2, 0)
            assert len(users) == 2
            assert page.previous is None
            assert page.current == 0
            assert page.next is None
            assert page.last == 0
            assert page.size == 2
            for user in users:
                assert await client.users.delete_by_id(user.id) == 1
        async with client.transaction():
            users, page = await client.users.list(10, 0)
            assert len(users) == 0
            assert page.previous is None
            assert page.current == 0
            assert page.next is None
            assert page.last == 0
            assert page.size == 10
