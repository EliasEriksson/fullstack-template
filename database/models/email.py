from __future__ import annotations
from typing import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.sql.expression import false
from database.models.base import Base
from ..constants import Cascades
from ..constants import Lazy
from .user_email import UserEmail

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
    verified: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        server_default=false(),
    )
    verification: Mapped[Verification] = relationship(
        back_populates="email",
        uselist=False,
        cascade=Cascades.default(Cascades.delete_orphan),
        lazy=Lazy.default(),
    )
    user: Mapped[User] = relationship(
        back_populates="emails",
        secondary=UserEmail.__tablename__,
        cascade=Cascades.default(),
        lazy=Lazy.default(),
    )
