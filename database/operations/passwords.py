from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import CRUD
from ..models import Password


class Passwords(CRUD):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Password)
