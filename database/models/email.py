from __future__ import annotations
from typing import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey
from uuid import UUID
from .base import Base
from ..constants import Cascades
from ..constants import Lazy
from ..constants import CASCADE

if TYPE_CHECKING:
    from .user import User
    from .verification import Verification


class Email(Base):
    __tablename__ = "email"
    address: Mapped[str] = mapped_column(
        String(),
        unique=True,
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete=CASCADE),
        nullable=False,
    )
    verification: Mapped[Verification] = relationship(
        back_populates="email",
        cascade=Cascades.default(Cascades.delete_orphan),
        lazy=Lazy.default(),
    )
    user: Mapped[User] = relationship(
        back_populates="emails",
        cascade=Cascades.default(),
        lazy=Lazy.default(),
    )
