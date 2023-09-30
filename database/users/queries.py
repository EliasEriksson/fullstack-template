from __future__ import annotations
from typing import *


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import update
from database.models import User
from uuid import UUID


async def fetch(session: AsyncSession, id: UUID) -> User | None:
    query = select(User).where(User.id == id)
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def list(session: AsyncSession, size: int, page: int) -> Sequence[User]:
    query = select(User).offset(size * page).limit(size)
    result = await session.execute(query)
    return result.scalars().all()


async def patch(session: AsyncSession, id: UUID, user: User) -> User:
    query = update(User).where(User.id == user.id)
    result = await session.execute(query)
    return result.scalars().one()


async def count(session: AsyncSession) -> int:
    query = select(func.count()).select_from(User)
    result = await session.execute(query)
    return result.scalars().one()
