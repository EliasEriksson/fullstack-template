from __future__ import annotations
from typing import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from database.models.base import Base
from uuid import UUID
from ..constants import CASCADE

if TYPE_CHECKING:
    pass


class UserEmail(Base):
    __tablename__ = "user_email"
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete=CASCADE),
        nullable=False,
    )
    email_id: Mapped[UUID] = mapped_column(
        ForeignKey("email.id", ondelete=CASCADE),
        nullable=False,
        unique=True,
    )
