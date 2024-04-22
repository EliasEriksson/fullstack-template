from database import Database
from database import models
from datetime import datetime
from uuid import UUID


async def test_relationships(database: Database, soon: datetime) -> None:
    async with database as session:
        async with session.transaction():
            user = models.User()
            user_session = models.Session(expire=soon, agent="pytest", user=user)
            await session.sessions.create(user_session)
        session_id: UUID = user_session.id
        assert session_id is not None
    async with database as session:
        async with session.transaction():
            user_session: models.Session = await session.sessions.fetch(session_id)
            assert user_session is not None
            assert user_session.user is not None
            await session.users.delete_by_id(user_session.user.id)
        async with session.transaction():
            user_session = await session.sessions.fetch(session_id)
            assert user_session is None
