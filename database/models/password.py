from __future__ import annotations
from typing import *
from uuid import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import LargeBinary
from sqlalchemy import ForeignKey
from database.models.base import Base
from bcrypt import checkpw
from shared import hash
from ..constants import Lazy
from ..constants import Cascades
from ..constants import CASCADE

if TYPE_CHECKING:
    from . import User


class Password(Base):
    __tablename__ = "password"
    digest: Mapped[bytes] = mapped_column(
        LargeBinary(),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete=CASCADE),
        nullable=False,
    )
    user: Mapped[User] = relationship(
        back_populates="passwords",
        cascade=Cascades.default(),
        lazy=Lazy.default(),
    )

    def verify(self, password: str) -> bool:
        return checkpw(password.encode(), self.digest)

    @staticmethod
    def hash(password: str) -> bytes:
        return hash.password(password)
