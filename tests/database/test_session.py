from database import Database
from database import models
from datetime import datetime
from uuid import UUID


async def test_relationships(database: Database, soon: datetime) -> None:
    async with database as client:
        async with client.transaction():
            user = models.User()
            session = models.Session(
                expire=soon, host="example.com", agent="pytest", user=user
            )
            await client.sessions.create(session)
        id: UUID = session.id
        assert id is not None
    async with database as client:
        async with client.transaction():
            session: models.Session = await client.sessions.fetch(id)
            assert session is not None
            assert session.user is not None
            await client.users.delete_by_id(session.user.id)
        async with client.transaction():
            session = await client.sessions.fetch(id)
            assert session is None
