from __future__ import annotations
from msgspec import Struct
from msgspec import field
from .. import password


class Patchable(Struct):
    email: str | None = field(default=None)
    password: password.Patchable | None = field(default=None)
