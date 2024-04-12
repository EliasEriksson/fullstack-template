from __future__ import annotations
from typing import *
from .. import base


class UserProtocol(base.BaseProtocol, Protocol):
    email: str


class User(base.Base):
    email: str
