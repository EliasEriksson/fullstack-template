from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Uuid
from sqlalchemy import text
import uuid


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True, native_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("gen_random_uuid()"),
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
