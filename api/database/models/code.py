from __future__ import annotations
from typing import *
import secrets
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from .base import Base
from ..constants import Lazy
from ..constants import CASCADE
from ..constants import Cascades
from uuid import UUID

if TYPE_CHECKING:
    from . import Email


class Code(Base):
    __tablename__ = "code"
    size = 64
    token: Mapped[str] = mapped_column(
        String(),
        default=lambda: secrets.token_urlsafe(Code.size),
        nullable=False,
    )
    reset_password: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
    )
    email_id: Mapped[UUID] = mapped_column(
        ForeignKey("email.id", ondelete=CASCADE),
        nullable=False,
    )
    email: Mapped[Email] = relationship(
        back_populates="code",
        lazy=Lazy.default(),
    )
