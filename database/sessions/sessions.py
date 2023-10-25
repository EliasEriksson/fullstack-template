from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Session
from datetime import datetime
from . import queries


class Sessions:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, session: Session) -> Session:
        self._session.add(session)
        return session

    async def fetch(self, host: str, agent: str) -> Session | None:
        return await queries.fetch_by_client(self._session, host, agent)

    async def patch(self, session: Session) -> Session:
        session.modified = datetime.now()
        self._session.add(session)
        return session

    async def delete(self, session: Session) -> Session:
        await self._session.delete(session)
        return session
