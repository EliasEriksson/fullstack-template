from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from ...models import Email
from ...models import Verification


class Verifications:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, verification: Verification) -> Verification:
        self._session.add(verification)
        return verification

    async def create(self, *, email: Email | None = None) -> Verification:
        verification = Verification()
        if email is not None:
            verification.email = email
        await self.add(verification)
        return verification
