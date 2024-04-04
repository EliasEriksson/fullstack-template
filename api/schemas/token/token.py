from __future__ import annotations
from typing import *

from msgspec import Struct
from uuid import UUID
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


class Token(Struct):
    audience: str
    issuer: str
    subject: UUID
    issued: datetime
    expires: datetime

    def refresh(self) -> Token:
        self.issued = datetime.fromtimestamp(round(datetime.now().timestamp()))
        self.expires = self.issued + timedelta(minutes=30)
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
