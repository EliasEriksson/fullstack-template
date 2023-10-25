from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Uuid
from sqlalchemy import DateTime
from sqlalchemy import func
from uuid import UUID
from ..constants import gen_random_uuid


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True, native_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=gen_random_uuid,
    )
    created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    modified: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
