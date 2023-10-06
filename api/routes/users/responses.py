from __future__ import annotations
from ...responses import Base
from database import models
from msgspec import Struct
from xxhash import xxh128


class Creatable(Struct):
    email: str

    @staticmethod
    def create(user: Creatable) -> models.User:
        return models.User(email=user.email)


class User(Base):
    email: str

    @classmethod
    def from_model(cls, user: models.User) -> User:
        instance = cls(
            id=user.id,
            created=user.created,
            modified=user.modified,
            email=user.email,
            etag=xxh128(user.modified.isoformat()).digest().hex(),
        )
        return instance


class Patchable(Struct):
    email: str | None

    @staticmethod
    def patch(user: models.User, patch: Patchable) -> models.User:
        if patch.email is not None:
            user.email = patch.email
        return user
