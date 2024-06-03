from __future__ import annotations
from typing import *
from uuid import UUID
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from database.operations.crud import CRUD
from .. import models


class Codes(CRUD[models.Code]):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, models.Code)

    async def fetch_by_token(self, token: str) -> models.Code | None:
        query = select(models.Code).where(
            cast(ColumnElement, models.Code.token == token)
        )
        result = await self._session.execute(query)
        return result.scalars().one_or_none()

    async def delete_by_user_id(self, user: UUID) -> int:
        query = delete(models.Code).where(
            cast(
                ColumnElement,
                models.Code.email_id
                == select(models.Email.id)
                .join(models.User)
                .where(cast(ColumnElement, models.User.id == user))
                .scalar_subquery(),
            )
        )
        result = await self._session.execute(query)
        return cast(int, result.rowcount)
