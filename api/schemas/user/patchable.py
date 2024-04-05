from __future__ import annotations
from typing import *
from msgspec import Struct
from msgspec import field
from .. import password


class UserProtocol(Protocol):
    email: str
    hash: bytes


class Patchable(Struct):
    email: str | None = field(default=None)
    password: password.Patchable | None = field(default=None)
