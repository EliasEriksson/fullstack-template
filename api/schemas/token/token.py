from __future__ import annotations
from typing import *
from msgspec import Struct
from datetime import datetime
from datetime import timedelta
from configuration import Configuration
from .claims import Claims
from .algorithms import Algorithms
from .exceptions import TokenEncodeException
from .exceptions import TokenDecodeException
from jose import jwt
from jose.exceptions import JWSError
from jose.exceptions import JWKError
from jose.exceptions import ExpiredSignatureError
from litestar.datastructures.url import URL
from uuid import UUID


class User(Protocol):
    id: UUID


class Token(Struct):
    audience: str
    issuer: str
    subject: UUID
    issued: datetime
    expires: datetime

    @staticmethod
    def _now() -> datetime:
        return datetime.now().replace(microsecond=0)

    @staticmethod
    def _expires(datetime: datetime) -> datetime:
        return datetime + timedelta(minutes=20)

    def refresh(self) -> Token:
        self.issued = self._now()
        self.expires = self._expires(self.issued)
        return self

    def _to_dict(self):
        return {
            Claims.audience: self.audience,
            Claims.issuer: self.issuer,
            Claims.subject: str(self.subject),
            Claims.expires: round(self.expires.timestamp()),
            Claims.issued: round(self.issued.timestamp()),
        }

    def encode(self) -> str:
        try:
            return jwt.encode(
                self._to_dict(),
                key=Configuration().api.jwt_private_key,
                algorithm=Algorithms.RS512,
            )
        except JWSError as error:
            raise TokenEncodeException() from error

    @classmethod
    def _from_dict(cls, token: dict[str, Any]) -> Token:
        return cls(
            audience=token[Claims.audience],
            issuer=token[Claims.issuer],
            subject=UUID(token[Claims.subject]),
            expires=datetime.fromtimestamp(token[Claims.expires]),
            issued=datetime.fromtimestamp(token[Claims.issued]),
        )

    @classmethod
    def decode(cls, token: str, audience: str | URL) -> Token:
        try:
            return cls._from_dict(
                jwt.decode(
                    token,
                    key=Configuration().api.jwt_public_key,
                    audience=str(audience),
                )
            )
        except (JWKError, ExpiredSignatureError) as error:
            raise TokenDecodeException() from error

    @classmethod
    def from_user(cls, user: User, audience: str | URL, issuer: str | URL) -> Token:
        now = cls._now()
        return cls(
            issuer=str(issuer),
            audience=str(audience),
            subject=user.id,
            issued=now,
            expires=cls._expires(now),
        )
