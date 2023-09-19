from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select
from .models import User
from uuid import UUID


class Users:
    _engine: AsyncEngine
    _session: async_sessionmaker[AsyncSession]

    def __init__(
        self, engine: AsyncEngine, session: async_sessionmaker[AsyncSession]
    ) -> None:
        self._engine = engine
        self._session = session

    async def create(self, *, email: str) -> User:
        user = User(email=email)
        async with self._session(bind=self._engine) as session:
            async with session.begin():
                session.add(user)
            await session.commit()
        return user

    async def fetch(self, id: UUID) -> User | None:
        query = select(User).where(id=id)
        async with self._session(bind=self._engine) as session:
            result = await session.execute(query)
        return result.scalar_one_or_none()

    async def list(self):
        query = select(User)
        async with self._session(bind=self._engine) as session:
            result = await session.execute(query)
        return result.scalars().all()

    async def patch(self):
        pass

    async def delete(self):
        pass
