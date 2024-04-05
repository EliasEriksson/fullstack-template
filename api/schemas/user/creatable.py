from __future__ import annotations
from msgspec import Struct
from msgspec import field
from .. import password


class Creatable(Struct):
    email: str
    password: password.Creatable | None = field(default=None)
