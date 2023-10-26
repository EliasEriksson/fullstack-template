from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy import select
from ...models import User
from ...models import Email
from ...models import Verification
from ...models import Session
from uuid import UUID


async def fetch_by_id(
    session: AsyncSession,
    id: UUID,
) -> User | None:
    query = (
        select(User, Email, Verification, Session)
        .where(User.id == id)
        .outerjoin(Email, Email.user_id == User.id)
        .join(Verification, Verification.email_id == Email.id)
        .outerjoin(Session, Session.user_id == User.id)
    )
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def fetch_by_email(session: AsyncSession, email: str) -> User | None:
    query = (
        select(User, Email, Verification, Session)
        .where(Email.address == email)
        .outerjoin(Email, Email.user_id == User.id)
        .join(Verification, Verification.email_id == Email.id)
        .outerjoin(Session, Session.user_id == User.id)
    )
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def list(
    session: AsyncSession,
    emails: List[str] | None = None,
    size: int = 1,
    page: int = 0,
) -> Sequence[User]:
    query = select(User, Email, Verification)
    if emails is not None:
        query = query.where(Email.address.in_(emails))
    query = (
        query.outerjoin(Email, Email.user_id == User.id)
        .join(Verification, Verification.email_id == Email.id)
        .outerjoin(Session, Session.user_id == User.id)
        .offset(size * page)
        .limit(size)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def count(
    session: AsyncSession,
    emails: List[str] | None = None,
) -> int:
    query = select(func.count()).select_from(User)
    if emails is not None:
        query = query.where(Email.address.in_(emails)).outerjoin(
            Email, Email.user_id == User.id
        )
    result = await session.execute(query)
    return result.scalars().one()
