from __future__ import annotations
from typing import *
from msgspec import Struct
from msgspec import field
from .. import password


class PatchableProtocol(Protocol):
    email: str | None
    password: password.PatchableProtocol | None


class Patchable(Struct, PatchableProtocol):
    email: str | None = field(default=None)
    password: password.PatchableProtocol | None = field(default=None)
