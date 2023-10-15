from __future__ import annotations
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import LargeBinary
from database.models.base import Base
from bcrypt import checkpw


class User(Base):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    hash: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)

    def verify(self, password: str) -> bool:
        return checkpw(password.encode(), self.hash)
