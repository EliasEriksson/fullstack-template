from __future__ import annotations
from typing import *
from .. import base


class EmailProtocol(base.BaseProtocol, Protocol):
    address: str
    verified: Optional[bool]


class Email(base.Base):
    address: str
    verified: Optional[bool] = None
