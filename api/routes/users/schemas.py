from __future__ import annotations
from ...schemas import Base
from database import models
from msgspec import Struct
from bcrypt import hashpw
from bcrypt import gensalt
from shared import hash


class Password(Struct):
    new: str
    repeat: str

    def hash(self) -> bytes:
        return hash.password(self.new)


class PatchablePassword(Password):
    old: str


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
    email: str | None
    password: PatchablePassword | None

    @staticmethod
    def patch(user: models.User, patch: Patchable) -> models.User:
        if patch.email is not None:
            user.email = patch.email
        if patch.password:
            user.hash = patch.password.hash()
        return user
