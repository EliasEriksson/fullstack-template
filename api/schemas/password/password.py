from __future__ import annotations
from msgspec import Struct
from shared import hash


class Password(Struct):
    password: str

    @property
    def hash(self) -> bytes:
        return hash.password(self.password)
