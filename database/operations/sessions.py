from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.operations.crud import CRUD
from .. import models


class Sessions(CRUD[models.Session]):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, models.Session)

    async def fetch_by_agent(
        self, user: models.User, agent: str
    ) -> models.Session | None:
        query = select(models.Session).where(models.Session.agent == agent)
        result = await self._session.execute(query)
        return result.scalars().one_or_none()
