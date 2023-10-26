from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import func
from database.models import Email
from database.models import Verification
from uuid import UUID


async def fetch(
    session: AsyncSession,
    id: UUID,
) -> Email | None:
    query = (
        select(Email, Verification)
        .where(Email.id == id)
        .join(Verification.email_id == Email.id)
    )
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def list(
    session: AsyncSession,
    emails: List[str],
    size: int,
    page: int,
) -> Sequence[Email]:
    if not emails:
        query = select(Email, Verification)
    else:
        query = (
            select(Email, Verification)
            .where(Email.address.in_(emails))
            .join(Verification, Verification.email_id == Email.id)
        )
    query.offset(size * page).limit(size)
    result = await session.execute(query)
    return result.scalars().all()


async def count(session: AsyncSession, emails: List[str]) -> int:
    if not emails:
        query = select(func.count()).select_from(Email)
    else:
        query = select(func.count()).select_from(Email).where(Email.address.in_(emails))
    result = await session.execute(query)
    return result.scalars().one()
