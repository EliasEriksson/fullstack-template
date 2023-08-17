from .base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from sqlalchemy import Uuid
from sqlalchemy import String
import uuid

if TYPE_CHECKING:
    from .user import User


class Post(Base):
    __tablename__ = "post"
    title: Mapped[str] = mapped_column(String(), nullable=False)
    content: Mapped[str] = mapped_column(String(), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True, native_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )
    user: Mapped["User"] = relationship(
        back_populates="posts",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, user={self.user})"
