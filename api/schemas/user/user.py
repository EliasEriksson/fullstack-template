from __future__ import annotations
from typing import *
from .. import base


class UserProtocol(base.BaseProtocol, Protocol):
    emails: list[str]


class User(base.Base):
    emails: list[str]
