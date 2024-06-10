from __future__ import annotations
from typing import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy.sql.expression import false
from uuid import UUID
from .base import Base
from ..constants import Cascades
from ..constants import Lazy
from ..constants import CASCADE

if TYPE_CHECKING:
    from .user import User
    from .code import Code


class Email(Base):
    __tablename__ = "email"
    address: Mapped[str] = mapped_column(
        String(),
        unique=True,
        nullable=False,
    )
    verified: Mapped[bool] = mapped_column(
        Boolean(),
        server_default=false(),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete=CASCADE),
        nullable=False,
    )
    user: Mapped[User] = relationship(
        back_populates="emails",
        lazy=Lazy.default(),
    )
    code: Mapped[Code | None] = relationship(
        back_populates="email",
        cascade=Cascades.default(Cascades.delete_orphan),
        lazy=Lazy.default(),
    )
