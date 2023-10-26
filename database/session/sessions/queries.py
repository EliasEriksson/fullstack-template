from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy import select
from database.models import Session
from database.models import User
from database.models import Email
from database.models import Verification
from uuid import UUID


async def fetch_by_client(
    session: AsyncSession,
    host: str,
    agent: str,
) -> Session | None:
    query = select(Session).where(Session.host == host).where(Session.agent == agent)
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def fetch_by_hash(hash: bytes) -> Session | None:
    query = select(Session).where
