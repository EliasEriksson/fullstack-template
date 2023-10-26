from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from ...models import User
from ...models import Email
from ...models import Session
from ...page import Page
from uuid import UUID
from . import queries


class Users:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user: User) -> User:
        self._session.add(user)
        return user

    async def create(
        self,
        hash: bytes,
        *,
        emails: List[Email] | None = None,
        sessions: List[Session] | None = None,
    ) -> User:
        user = User(hash=hash)
        if emails is not None:
            user.emails = emails
        if sessions is not None:
            user.sessions = sessions
        await self.add(user)
        return user

    async def fetch_by_id(self, id: UUID) -> User | None:
        return await queries.fetch_by_id(self._session, id)

    async def fetch_by_email(self, email: str) -> User | None:
        return await queries.fetch_by_email(self._session, email)

    async def list(
        self,
        size: int,
        page: int,
        *,
        emails: List[str] | None = None,
    ) -> tuple[Sequence[User], Page]:
        result = await queries.list(self._session, emails, size, page)
        count = await queries.count(self._session, emails)
        return result, Page(size, page, count)

    async def delete(self, user: User) -> User:
        await self._session.delete(user)
        return user
