from __future__ import annotations
from typing import *
from ...schemas import Base
from litestar import Request
from litestar.exceptions import ClientException
from database import models
from msgspec import Struct
from msgspec import field
from shared import hash
from api.routes.auth.schemas.token import Token


class Password(Struct):
    new: str
    repeat: str

    def hash(self) -> bytes:
        return hash.password(self.new)


class PatchablePassword(Password):
    old: str | None = field(default=None)


class Creatable(Struct):
    email: str
    password: Password

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
    password: PatchablePassword | None = field(default=None)

    def validate(self, request: Request[models.User, Token, Any]) -> None:
        if self.password:
            if self.password.new != self.password.repeat:
                raise ClientException("Passwords are not matching.")
            elif request.auth.subject == request.user.id:
                if not self.password.old:
                    raise ClientException("Missing old password.")
                elif not request.user.verify(self.password.old):
                    raise ClientException("Password missmatch.")

    def patch(self, user: models.User) -> models.User:
        if self.email is not None:
            user.email = self.email
        if self.password and self.password.new:
            user.hash = self.password.hash()
        return user
