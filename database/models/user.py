from __future__ import annotations
from typing import *
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import LargeBinary
from database.models.base import Base
from bcrypt import checkpw
from datetime import datetime
from sqlalchemy.orm import Mapped
from shared import hash


class Password(Protocol):
    password: str


class Patch(Protocol):
    email: str | None
    password: Password | None


class Creatable(Protocol):
    email: str
    password: Password | None


class User(Base):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    hash: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)

    def verify(self, password: str) -> bool:
        return checkpw(password.encode(), self.hash)

    def patch(self, patch: Patch) -> User:
        if patch.email is not None:
            self.email = patch.email
        if patch.password is not None:
            self.hash = self.hash_password(patch.password.password)
        self.modified = datetime.now()
        return self

    @classmethod
    def from_creatable(cls, creatable: Creatable) -> User:
        return cls(
            email=creatable.email,
            hash=cls.hash_password(creatable.password.password),
        )

    @staticmethod
    def hash_password(password: str) -> bytes:
        return hash.password(password)
