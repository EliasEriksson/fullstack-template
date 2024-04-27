from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from database.operations.crud import CRUD
from .. import models


class Emails(CRUD[models.Email]):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, models.Email)
