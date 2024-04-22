from __future__ import annotations
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Base as BaseModel
from .page import Page
from uuid import UUID
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import delete


T = TypeVar("T", bound=BaseModel)


class CRUD(Generic[T]):
    _session: AsyncSession
    _model: Type[T]

    def __init__(self, session: AsyncSession, model: Type[T]) -> None:
        self._session = session
        self._model = model

    async def create(self, model: T) -> T:
        self._session.add(model)
        return model

    async def fetch(self, id: UUID) -> T | None:
        query = select(self._model).where(self._model.id == id)
        result = await self._session.execute(query)
        return result.scalars().one_or_none()

    async def list(self, size: int, page: int) -> tuple[Sequence[T], Page]:
        query = select(self._model).offset(size * page).limit(size)
        result = await self._session.execute(query)
        count = await self.count()
        return result.scalars().all(), Page(size, page, count)

    async def update(self, model: T) -> T:
        return await self.create(model)

    async def delete_by_id(self, id: UUID) -> bool:
        query = delete(self._model).where(self._model.id == id)
        result = await self._session.execute(query)
        return cast(int, result.rowcount) > 0

    async def delete(self, model: T) -> T:
        await self._session.delete(model)
        return model

    async def count(self) -> int:
        query = select(func.count()).select_from(self._model)
        result = await self._session.execute(query)
        return result.scalars().one()
