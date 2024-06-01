from __future__ import annotations
from typing import *
from sqlalchemy import select
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from database.operations.crud import CRUD
from .. import models


class Emails(CRUD[models.Email]):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, models.Email)

    async def fetch_by_code(self, code: str) -> models.Email | None:
        query = select(models.Email).where(
            cast(ColumnElement, models.Email.code.token == code)
        )
        result = await self._session.execute(query)
        return result.scalars().one_or_none()

    # async def fetch_by_verification(self, verification: UUID) -> models.Email | None:
    #     query = (
    #         select(models.email)
    #         .where(cast(ColumnElement, models.Email.verification == verification))
    #         .where(cast(ColumnElement, models.Email.verified == False))
    #     )
    #     result = await self._session.execute(query)
    #     return result.scalars().one_or_none()
