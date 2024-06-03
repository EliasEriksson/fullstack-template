from __future__ import annotations
from typing import *
from .. import base


class EmailProtocol(base.BaseProtocol, Protocol):
    address: str
    verified: Optional[bool]


class Email(base.Base):
    address: str
    verified: Optional[bool] = None

    # @classmethod
    # def from_protocol(cls, email: EmailProtocol) -> Email:
    #     return cls(
    #         id=email.id,
    #         address=email.address,
    #         verified=email.verified,
    #         modified=email.modified,
    #         created=email.created,
    #     )
