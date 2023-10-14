from __future__ import annotations
from typing import *
from api.schemas import Base
from litestar import Request
from litestar.exceptions import ClientException
from database import models
from msgspec import Struct
from msgspec import field
from shared import hash
from ...auth.schemas import password
from api.routes.auth.schemas.token import Token


class Creatable(Struct):
    email: str
    password: password.Creatable = field(default=None)

    @staticmethod
    def create(user: Creatable) -> models.User:
        return models.User(
            email=user.email,
            hash=user.password.hash(),
        )


class User(Base):
    email: str

    @classmethod
    def from_model(cls, user: models.User) -> User:
        instance = cls(
            id=user.id,
            created=user.created,
            modified=user.modified,
            email=user.email,
            etag=hash.etag(user.modified),
        )
        return instance


class Patchable(Struct):
    email: str | None = field(default=None)
    password: password.Creatable | None = field(default=None)

    def patch(self, user: models.User) -> models.User:
        if self.email is not None:
            user.email = self.email
        if self.password and self.password.new:
            user.hash = self.password.hash()
        return user
