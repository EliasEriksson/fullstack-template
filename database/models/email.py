from __future__ import annotations
from typing import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from database.models.base import Base
from uuid import UUID


if TYPE_CHECKING:
    pass


class Email(Base):
    __tablename__ = "user"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)

    # user: Mapped[]
