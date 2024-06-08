from __future__ import annotations
from typing import *
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
from jose.exceptions import JWTClaimsError
from litestar.datastructures.url import URL
from uuid import UUID
from sqlalchemy.orm import Mapped
from ..schema import Schema


class ResourceProtocol(Protocol):
    id: UUID


class PasswordProtocol(ResourceProtocol, Protocol):
    pass


class UserProtocol(ResourceProtocol, Protocol):
    passwords: list[PasswordProtocol] | Mapped[list[PasswordProtocol]]


class SessionProtocol(ResourceProtocol, Protocol):
    user: UserProtocol | Mapped[UserProtocol]


class TokenProtocol(Protocol):
    audience: str
    issuer: str
    subject: UUID
    session: UUID
    email: UUID
    secure: bool
    issued: datetime
    expires: datetime


class Token(Schema):
    audience: str
    issuer: str
    subject: UUID
    email: UUID
    session: UUID
    secure: bool
    issued: datetime
    expires: datetime

    @staticmethod
    def _now() -> datetime:
        return datetime.now().replace(microsecond=0)

    @staticmethod
    def _expires(datetime: datetime, duration: timedelta | None = None) -> datetime:
        delta = duration or timedelta(minutes=20)
        return datetime + delta

    def refresh(
        self, *, issued: datetime | None = None, duration: timedelta | None = None
    ) -> Token:
        self.issued = issued or self._now()
        self.expires = self._expires(issued, duration)
        return self

    def _to_dict(self):
        return {
            Claims.audience: self.audience,
            Claims.issuer: self.issuer,
            Claims.subject: str(self.subject),
            Claims.session: str(self.session),
            Claims.email: str(self.email),
            Claims.secure: self.secure,
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
        try:
            return cls(
                audience=token[Claims.audience],
                issuer=token[Claims.issuer],
                subject=UUID(token[Claims.subject]),
                session=UUID(token[Claims.session]),
                email=UUID(token[Claims.email]),
                secure=token[Claims.secure],
                expires=datetime.fromtimestamp(token[Claims.expires]),
                issued=datetime.fromtimestamp(token[Claims.issued]),
            )
        except KeyError as error:
            raise TokenDecodeException from error

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
        except (JWKError, ExpiredSignatureError, JWTClaimsError) as error:
            raise TokenDecodeException() from error

    @classmethod
    def create(
        cls,
        session: SessionProtocol,
        email: UUID,
        audience: str | URL,
        issuer: str | URL,
    ) -> Token:
        now = cls._now()
        return cls(
            issuer=str(issuer),
            audience=str(audience),
            subject=session.user.id,
            session=session.id,
            email=email,
            secure=len(session.user.passwords) > 0,
            issued=now,
            expires=cls._expires(now),
        )
