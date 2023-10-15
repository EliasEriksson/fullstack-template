from __future__ import annotations
from typing import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import LargeBinary
from database.models.base import Base
from bcrypt import checkpw
from uuid import UUID


if TYPE_CHECKING:
    from .email import Email


class User(Base):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    hash: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)

    emails: Mapped[list[Email]] = relationship(back_populates="user")

    def verify(self, password: str) -> bool:
        return checkpw(password.encode(), self.hash)
