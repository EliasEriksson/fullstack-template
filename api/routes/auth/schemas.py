from __future__ import annotations
from typing import *
from uuid import UUID
from msgspec import Struct
from datetime import datetime
from datetime import timedelta
from database import models
from ...configuration import ApiConfiguration
from jose import jwt
from jose.exceptions import JWSError
from jose.exceptions import JWKError
from .exceptions import TokenDecodeException
from .exceptions import TokenEncodeException
from dataclasses import dataclass


@dataclass
class Claims:
    subject = "sub"
    expires = "exp"
    issued = "iss"
    audience = "aud"


@dataclass
class Algorithms:
    RS512 = "RS512"


class Token(Struct):
    audience: str
    subject: UUID
    expires: datetime
    issued: datetime

    def _to_jose_dict(self) -> dict[str, Any]:
        return {
            Claims.audience: self.audience,
            Claims.subject: str(self.subject),
            Claims.expires: round(self.expires.timestamp()),
            Claims.issued: round(self.issued.timestamp()),
        }

    @classmethod
    def _from_jose_dict(cls, token: dict[str, Any]) -> Token:
        return cls(
            audience=token[Claims.audience],
            subject=UUID(token[Claims.subject]),
            expires=datetime.fromtimestamp(token[Claims.expires]),
            issued=datetime.fromtimestamp(token[Claims.issued]),
        )

    @classmethod
    def decode(cls, token: str, audience: str) -> Token:
        configuration = ApiConfiguration()
        try:
            return cls._from_jose_dict(
                jwt.decode(
                    token,
                    key=configuration.jwt_public_key,
                    algorithms=[Algorithms.RS512],
                    audience=audience,
                )
            )
        except JWKError:
            raise TokenDecodeException()

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

    @classmethod
    def encode_model(cls, user: models.User, audience: str) -> str:
        now = datetime.fromtimestamp(round(datetime.now().timestamp()))
        return cls.encode(
            cls(
                subject=user.id,
                expires=now + timedelta(minutes=20),
                issued=now,
                audience=audience,
            )
        )
