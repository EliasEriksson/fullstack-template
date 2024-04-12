from __future__ import annotations
from typing import *
from sqlalchemy.sql.expression import false
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Uuid
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from uuid import UUID
from .base import Base
from ..constants import Cascades
from ..constants import Lazy
from ..constants import CASCADE
from ..constants import gen_random_uuid

if TYPE_CHECKING:
    from .email import Email


class Verification(Base):
    __tablename__ = "verification"
    code: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True, native_uuid=True),
        nullable=False,
        server_default=gen_random_uuid,
    )
    completed: Mapped[Boolean] = mapped_column(
        Boolean(),
        nullable=False,
        server_default=false(),
    )
    email_id: Mapped[UUID] = mapped_column(
        ForeignKey("email.id", ondelete=CASCADE),
        nullable=False,
    )
    email: Mapped[Email] = relationship(
        back_populates="verification",
        cascade=Cascades.default(),
        lazy=Lazy.default(),
    )
