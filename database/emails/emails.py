from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime
from ..models import Email
from . import queries
from ..page import Page


class Emails:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, email: Email) -> Email:
        self._session.add(email)
        return email

    async def fetch(self, id: UUID) -> Email | None:
        return await queries.fetch(self._session, id)

    async def list(
        self, emails: List[str], size: int, page: int
    ) -> tuple[Sequence[Email], Page]:
        result = await queries.list(self._session, emails, size, page)
        count = await queries.count(self._session, emails)
        return result, Page(size, page, count)

    async def patch(self, email: Email) -> Email:
        email.modified = datetime.now()
        self._session.add(email)
        return email

    async def delete(self, email: Email) -> Email:
        await self._session.delete(email)
        return email
