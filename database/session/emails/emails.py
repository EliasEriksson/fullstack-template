from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from ...models import Email
from ...models import User
from ...models import Verification
from . import queries
from database.page import Page


class Emails:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, email: Email) -> Email:
        self._session.add(email)
        return email

    async def create(
        self,
        address: str,
        *,
        user: User | None = None,
        verification: Verification | None = None,
    ) -> Email:
        email = Email(address=address)
        if user is not None:
            email.user = user
        if verification is not None:
            email.verification = verification
        await self.add(email)
        return email

    async def fetch_by_id(self, id: UUID) -> Email | None:
        return await queries.fetch(self._session, id)

    async def list(
        self, emails: List[str], size: int, page: int
    ) -> tuple[Sequence[Email], Page]:
        result = await queries.list(self._session, emails, size, page)
        count = await queries.count(self._session, emails)
        return result, Page(size, page, count)

    async def delete(self, email: Email) -> Email:
        await self._session.delete(email)
        return email
