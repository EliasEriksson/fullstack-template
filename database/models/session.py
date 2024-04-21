from __future__ import annotations
from typing import *
from uuid import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from .base import Base
from ..constants import Cascades
from ..constants import CASCADE
from ..constants import Lazy

if TYPE_CHECKING:
    from .user import User


class Session(Base):
    __tablename__ = "session"
    expire: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    agent: Mapped[String] = mapped_column(
        String(),
        nullable=False,
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
