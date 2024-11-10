from __future__ import annotations
from typing import *
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete
from sqlalchemy.sql.expression import ColumnElement
from api.database.operations.crud import CRUD
from .. import models


class Password(CRUD[models.Password]):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, models.Password)

    async def fetch_by_email(self, email: UUID) -> models.Password | None:
        query = (
            select(models.Password)
            .join(models.User)
            .join(models.Email)
            .where(cast(ColumnElement, models.Email.id == email))
        )
        result = await self._session.execute(query)
        return result.scalars().one_or_none()

    async def delete_by_user(self, user: UUID) -> int:
        query = delete(models.Password).where(
            cast(ColumnElement, models.User.id == user)
        )
        result = await self._session.execute(query)
        return cast(int, result.rowcount)

    async def delete_by_email(self, email: UUID) -> int:
        query = delete(models.Password).where(
            models.Password.user_id
            == select(models.User.id)
            .join(models.Email)
            .where(cast(ColumnElement, models.Email.id == email))
            .scalar_subquery()
        )
        result = await self._session.execute(query)
        return cast(int, result.rowcount)
