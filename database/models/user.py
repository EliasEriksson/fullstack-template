from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy import Uuid
import uuid

if TYPE_CHECKING:
    from .post import Post


class User(Base):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", cascade="all, delete", passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, email={self.email})"
