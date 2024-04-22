from __future__ import annotations
from typing import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy import Uuid
from sqlalchemy.sql.expression import false
from uuid import UUID
from .base import Base
from ..constants import Cascades
from ..constants import Lazy
from ..constants import CASCADE
from ..constants import gen_random_uuid

if TYPE_CHECKING:
    from .user import User


class Email(Base):
    __tablename__ = "email"
    address: Mapped[str] = mapped_column(
        String(),
        unique=True,
        nullable=False,
    )
    verified: Mapped[Boolean] = mapped_column(
        Boolean(),
        server_default=false(),
        nullable=False,
    )
    verification: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True, native_uuid=True),
        server_default=gen_random_uuid,
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete=CASCADE),
        nullable=False,
    )
    user: Mapped[User] = relationship(
        back_populates="emails",
        cascade=Cascades.default(),
        lazy=Lazy.default(),
    )
