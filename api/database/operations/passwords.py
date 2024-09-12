from __future__ import annotations
from typing import *
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.sql.expression import true
from api.database.operations.crud import CRUD
from ..exceptions import IntegrityError
from .. import models


class Passwords(CRUD[models.Password]):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, models.Password)

    async def list_valid_passwords(
        self, user: models.User
    ) -> Sequence[models.Password]:
        query = (
            select(models.Password)
            .where(cast(ColumnElement, models.Password.user == user))
            .where(cast(ColumnElement, models.Password.valid == true()))
        )
        result = await self._session.execute(query)
        return result.scalars().all()

    async def create(self, model: models.Password) -> models.Password:
        query = select(models.Password).where(
            cast(ColumnElement, models.Password.valid)
        )
        result = await self._session.execute(query)
        passwords = result.scalars().all()
        if len(passwords) > 1:
            print("invalidate old passwords")
        elif len(passwords):
            raise IntegrityError("User already have password.")
        return await super().create(model)

    async def invalidate_by_user(self, user: UUID) -> int:
        query = (
            update(models.Password)
            .values(valid=False)
            .where(cast(ColumnElement, models.Password.user_id == user))
        )
        result = await self._session.execute(query)
        return cast(int, result.rowcount)

    async def invalidate_by_email_id(self, email: UUID) -> int:
        # TODO: repair this function!
        query = (
            update(models.Password)
            .values({models.Password.valid: False})
            .where(
                models.Password.user_id
                == select(models.Email.user_id)
                .where(cast(ColumnElement, models.Email.id == email))
                .scalar_subquery()
            )
        )
        result = await self._session.execute(query)
        return cast(int, result.rowcount)
