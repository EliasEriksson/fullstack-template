from __future__ import annotations
from typing import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import LargeBinary
from database.models.base import Base
from bcrypt import checkpw
from ..constants import Cascades
from ..constants import Lazy

if TYPE_CHECKING:
    from .email import Email


class User(Base):
    __tablename__ = "user"
    hash: Mapped[bytes] = mapped_column(
        LargeBinary(),
        nullable=False,
    )

    emails: Mapped[list[Email]] = relationship(
        back_populates="user",
        cascade=Cascades.default(),
        lazy=Lazy.default(),
    )

    def verify(self, password: str) -> bool:
        return checkpw(password.encode(), self.hash)
