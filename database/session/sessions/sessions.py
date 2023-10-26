from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from ...models import Session
from ...models import User
from . import queries


class Sessions:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, session: Session) -> Session:
        self._session.add(session)
        return session

    async def create(
        self, host: str, agent: str, *, user: User | None = None
    ) -> Tuple[Session, str]:
        refresh_token = Session.generate_token()
        session = Session(
            hash=Session.create_hash(refresh_token), host=host, agent=agent
        )
        if user is not None:
            session.user = user
        await self.add(session)
        return session, refresh_token

    async def fetch(self, host: str, agent: str) -> Session | None:
        return await queries.fetch_by_client(self._session, host, agent)

    async def delete(self, session: Session) -> Session:
        await self._session.delete(session)
        return session
