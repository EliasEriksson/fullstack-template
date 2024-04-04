from __future__ import annotations
from typing import *
from msgspec import Struct
from msgspec import field
from .. import password


class CreatableProtocol(Protocol):
    email: str
    password: password.CreatableProtocol | None


class Creatable(Struct, CreatableProtocol):
    password = field(default=None)
