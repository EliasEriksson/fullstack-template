from __future__ import annotations
from typing import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import LargeBinary
from database.models.base import Base
from bcrypt import checkpw
from datetime import datetime


class Patch(Protocol):
    email: str | None
    hash: str | None


class User(Base):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    hash: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)

    def verify(self, password: str) -> bool:
        return checkpw(password.encode(), self.hash)

    def patch(self, patch: Patch) -> User:
        if patch.email is not None:
            self.email = patch.email
        if patch.hash is not None:
            self.hash = patch.hash
        self.modified = datetime.now()
        return self
