from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from ..page import Page
from uuid import UUID
from . import queries


class Users:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        return user

    async def fetch(self, id: UUID) -> User | None:
        return await queries.fetch(self._session, id)

    async def list(
        self, emails: list[str], size: int, page: int
    ) -> tuple[Sequence[User], Page]:
        users = await queries.list(self._session, emails, size, page)
        count = await queries.count(self._session)
        return users, Page(size, page, count)

    async def patch(self, user: User):
        self._session.add(user)
        await self._session.commit()
        return user

    async def delete(self, user: User):
        await self._session.delete(user)
        await self._session.commit()
        return user
