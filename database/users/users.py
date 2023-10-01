from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from database.models import User
from ..page import Page
from uuid import UUID
from . import queries


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
        async with self._session(bind=self._engine) as session:
            return await queries.fetch(session, id)

    async def list(self, size: int, page: int) -> tuple[Sequence[User], Page]:
        async with self._session(bind=self._engine) as session:
            async with session.begin():
                users = await queries.list(session, size, page)
                count = await queries.count(session)
        return users, Page(size, page, count)

    async def patch(self, user: User):
        async with self._session(bind=self._engine) as session:
            async with session.begin():
                session.add(user)
            await session.commit()
        return user

    async def delete(self):
        pass
