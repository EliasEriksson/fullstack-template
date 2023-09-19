from __future__ import annotations
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from .base import Base


class User(Base):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)

    def __init__(self, *, email: str) -> None:
        super().__init__(email=email)
