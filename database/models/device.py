from __future__ import annotations
from typing import *
from uuid import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Uuid
from .base import Base
from ..constants import Cascades
from ..constants import CASCADE
from ..constants import Lazy


if TYPE_CHECKING:
    from .user import User


class Device(Base):
    """
    Generated and sent as a cookie?
    device must exist to allow a session refresh
    """

    __tablename__ = "session"
    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True, native_uuid=True),
        primary_key=True,
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
