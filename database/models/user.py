from __future__ import annotations
from typing import *
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from database.models.base import Base
from ..constants import Cascades
from ..constants import Lazy


if TYPE_CHECKING:
    from .password import Password
    from .email import Email
    from .session import Session


class Creatable(Protocol):
    email: str


class User(Base):
    __tablename__ = "user"
    emails: Mapped[list[Email]] = relationship(
        back_populates="user",
        cascade=Cascades.default(Cascades.delete_orphan),
        lazy=Lazy.default(),
    )
    passwords: Mapped[list[Password]] = relationship(
        back_populates="user",
        cascade=Cascades.default(Cascades.delete_orphan),
        lazy=Lazy.default(),
    )
    sessions: Mapped[list[Session]] = relationship(
        back_populates="user",
        cascade=Cascades.default(Cascades.delete_orphan),
        lazy=Lazy.default(),
    )
