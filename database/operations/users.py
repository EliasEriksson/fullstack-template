from __future__ import annotations
from typing import *
from sqlalchemy import select
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from database.operations.crud import CRUD
from .. import models


class Users(CRUD[models.User]):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, models.User)

    async def fetch_by_email(self, email: str) -> models.User | None:
        query = (
            select(models.User)
            .join(models.User.emails)
            .where(cast(ColumnElement, models.Email.address == email))
        )
        result = await self._session.execute(query)
        return result.scalars().one_or_none()
