from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy import select
from database.operations.crud import CRUD
from .. import models


class Sessions(CRUD[models.Session]):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, models.Session)

    async def fetch_by_connection(
        self, user: models.User, host: str, agent: str
    ) -> models.Session | None:
        query = (
            select(models.Session)
            .join(models.Session.user)
            .where(cast(ColumnElement, models.User.id == user.id))
            .where(cast(ColumnElement, models.Session.host == host))
            .where(cast(ColumnElement, models.Session.agent == agent))
        )
        result = await self._session.execute(query)
        return result.scalars().one_or_none()
