from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import CRUD
from ..models import User


class Users(CRUD):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)
