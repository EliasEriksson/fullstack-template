from __future__ import annotations
from typing import *
from msgspec import Struct
from database.page import Page
from database import models
from datetime import datetime
from datetime import timedelta
from jose import jwt
from jose.exceptions import JWSError
from jose.exceptions import JWKError
from .configuration import ApiConfiguration
from .exceptions import TokenDecodeException
from .exceptions import TokenEncodeException
from uuid import UUID

T = TypeVar("T")


class Base(Struct):
    id: UUID
    created: datetime
    modified: datetime
    etag: str


class Resource(Struct, Generic[T]):
    result: T


class PagedResource(Struct, Generic[T]):
    result: list[T]
    page: Page


class Token(Struct):
    sub: UUID
    exp: datetime

    @classmethod
    def from_model(cls, user: models.User) -> Token:
        # "*bangs table* There must be a better way! "
        return cls(
            sub=user.id,
            exp=round((datetime.now() + timedelta(hours=8)).timestamp()),
        )

    def dict(self) -> dict[str, Any]:
        # "*bangs table* There must be a better way!"
        return {
            "sub": str(self.sub),
            "exp": self.exp,
        }

    @classmethod
    def decode(cls, token: str) -> Token:
        configuration = ApiConfiguration()
        try:
            decoded = jwt.decode(token=token, key=configuration.jwt_public_key)
            return cls(sub=decoded["sub"], exp=datetime.fromtimestamp(decoded["exp"]))
        except JWKError:
            raise TokenDecodeException()

    def encode(self) -> str:
        configuration = ApiConfiguration()
        try:
            return jwt.encode(
                self.dict(), key=configuration.jwt_private_key, algorithm="RS512"
            )
        except JWSError:
            raise TokenEncodeException()
