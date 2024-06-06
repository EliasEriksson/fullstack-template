from __future__ import annotations
from typing import *
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from sqlalchemy.sql.expression import ColumnElement
from database.operations.crud import CRUD
from ..exceptions import IntegrityError
from .. import models


class Passwords(CRUD[models.Password]):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, models.Password)

    async def create(self, model: models.Password) -> models.Password:
        query = select(models.Password).where(
            cast(ColumnElement, models.Password.valid == True)
        )
        result = await self._session.execute(query)
        passwords = result.scalars().all()
        if len(passwords) > 1:
            print("invalidate old passwords")
        elif len(passwords):
            raise IntegrityError("User already have password.")
        return await super().create(model)

    async def invalidate_by_email(self, email: str) -> int:
        query = (
            update(models.Password)
            .values(valid=False)
            .where(
                cast(
                    ColumnElement,
                    models.Password.user_id
                    == select(models.User.id)
                    .join(models.User.emails)
                    .where(cast(ColumnElement, models.Email.address == email))
                    .scalar_subquery(),
                )
            )
        )
        result = await self._session.execute(query)
        return cast(int, result.rowcount)
