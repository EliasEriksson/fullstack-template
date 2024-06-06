from __future__ import annotations
from typing import *
from uuid import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import LargeBinary
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from bcrypt import checkpw
from shared import hash
from .base import Base
from ..constants import Lazy
from ..constants import CASCADE

if TYPE_CHECKING:
    from . import User


class Password(Base):
    __tablename__ = "password"
    digest: Mapped[bytes] = mapped_column(
        LargeBinary(),
        nullable=False,
    )
    valid: Mapped[bool] = mapped_column(
        Boolean(),
        default=True,
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete=CASCADE),
        nullable=False,
    )
    user: Mapped[User] = relationship(
        back_populates="passwords",
        lazy=Lazy.default(),
    )

    def verify(self, password: str) -> bool:
        return checkpw(password.encode(), self.digest)

    @staticmethod
    def hash(password: str) -> bytes:
        return hash.password(password)
