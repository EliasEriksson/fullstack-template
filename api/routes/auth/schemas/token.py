from __future__ import annotations
from typing import *
from uuid import UUID
from msgspec import Struct
from msgspec import field
from datetime import datetime
from datetime import timedelta
from database import models
from api.configuration import ApiConfiguration
from jose import jwt
from jose.exceptions import JWSError
from jose.exceptions import JWKError
from jose.exceptions import ExpiredSignatureError
from api.routes.auth.exceptions import TokenDecodeException
from api.routes.auth.exceptions import TokenEncodeException
from dataclasses import dataclass
from litestar.datastructures.url import URL
from . import password


@dataclass
class Claims:
    subject = "sub"
    expires = "exp"
    issued = "iss"
    audience = "aud"


@dataclass
class Algorithms:
    RS512 = "RS512"


class Creatable(Struct):
    emails: list[str]
    password: password.Creatable

    @staticmethod
    def create(user: Creatable) -> models.User:
        return models.User(
            emails=[models.Email(address=email) for email in user.emails],
            hash=user.password.hash(),
        )


class Token(Struct):
    audience: str
    subject: UUID
    expires: datetime
    issued: datetime

    @staticmethod
    def _issued() -> datetime:
        return datetime.fromtimestamp(round(datetime.now().timestamp()))

    @staticmethod
    def _expires(datetime) -> datetime:
        return datetime + timedelta(minutes=20)

    def _to_jose_dict(self) -> dict[str, Any]:
        return {
            Claims.audience: self.audience,
            Claims.subject: str(self.subject),
            Claims.expires: round(self.expires.timestamp()),
            Claims.issued: round(self.issued.timestamp()),
        }

    def encode(self) -> str:
        configuration = ApiConfiguration()
        try:
            return jwt.encode(
                self._to_jose_dict(),
                key=configuration.jwt_private_key,
                algorithm=Algorithms.RS512,
            )
        except JWSError:
            raise TokenEncodeException()

    def refresh(self) -> Token:
        self.issued = self._issued()
        self.expires = self._expires(self.issued)
        return self

    @classmethod
    def _from_jose_dict(cls, token: dict[str, Any]) -> Token:
        return cls(
            audience=token[Claims.audience],
            subject=UUID(token[Claims.subject]),
            expires=datetime.fromtimestamp(token[Claims.expires]),
            issued=datetime.fromtimestamp(token[Claims.issued]),
        )

    @classmethod
    def decode(cls, token: str, audience: str | URL) -> Token:
        configuration = ApiConfiguration()
        try:
            return cls._from_jose_dict(
                jwt.decode(
                    token,
                    key=configuration.jwt_public_key,
                    algorithms=[Algorithms.RS512],
                    audience=str(audience),
                )
            )
        except (JWKError, ExpiredSignatureError):
            raise TokenDecodeException()

    @classmethod
    def encode_model(cls, user: models.User, audience: str | URL) -> str:
        now = cls._issued()
        return cls.encode(
            cls(
                subject=user.id,
                expires=now + timedelta(minutes=20),
                issued=cls._expires(now),
                audience=str(audience),
            )
        )


class Patchable(Struct):
    emails: list[str] | None = field(default=None)
    password: password.Patchable | None = field(default=None)

    def patch(self, user: models.User) -> models.User:
        # try to move this logic deeper, so it can be shared
        if self.emails is not None:
            existing = {email.address for email in user.emails}
            new = (models.Email(address=email) for email in self.emails if email not in existing)
            keep = (email for email in user.emails if email.address in self.emails)
            user.emails = [*keep, *new]
        if self.password is not None:
            user.hash = self.password.hash()
        user.modified = datetime.now()
        return user
