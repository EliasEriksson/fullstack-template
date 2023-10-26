from __future__ import annotations
from typing import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import LargeBinary
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import UniqueConstraint
from uuid import UUID
from secrets import token_urlsafe
from datetime import datetime
from datetime import timedelta
from bcrypt import checkpw
from shared import hash
from .base import Base
from ..constants import Cascades
from ..constants import CASCADE
from ..constants import Lazy


if TYPE_CHECKING:
    from .user import User


class Session(Base):
    __tablename__ = "session"
    __table_args__ = (UniqueConstraint("user_id", "agent", "host"),)
    hash: Mapped[bytes] = mapped_column(
        LargeBinary(),
        nullable=False,
    )
    host: Mapped[String] = mapped_column(
        String(),
        nullable=False,
    )
    agent: Mapped[String] = mapped_column(
        String(),
        nullable=False,
    )
    expires: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now() + timedelta(days=30),
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete=CASCADE),
        nullable=False,
    )
    user: Mapped[User] = relationship(
        back_populates="sessions",
        cascade=Cascades.default(),
        lazy=Lazy.default(),
    )

    def verify(self, user: UUID, token: str) -> bool:
        return self.user_id == user and checkpw(token.encode(), self.hash)

    def regenerate(self) -> str:
        refresh_token = self.generate_token()
        self.hash = cast(Mapped[bytes], self.create_hash(refresh_token))
        self.expires = cast(Mapped[DateTime], datetime.now() + timedelta(days=30))
        return refresh_token

    @staticmethod
    def generate_token() -> str:
        return token_urlsafe(64)

    @staticmethod
    def create_hash(token: str) -> bytes:
        return hash.password(token)
