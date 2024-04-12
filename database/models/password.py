from __future__ import annotations
from typing import *
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy import ForeignKey
from database.models.base import Base
from bcrypt import checkpw
from shared import hash
from ..constants import CASCADE
from ..constants import Lazy
from ..constants import Cascades

if TYPE_CHECKING:
    from . import User


class Password(Base):
    __tablename__ = "password"
    hash: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "user.id",
        )
    )
    user: Mapped[User] = relationship(
        back_populates="passwords",
        cascade=Cascades.default(),
        lazy=Lazy.default(),
    )
