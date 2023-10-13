from __future__ import annotations
from msgspec import Struct
from shared import hash


class Password(Struct):
    new: str

    def hash(self) -> bytes:
        return hash.password(self.new)


class Creatable(Password):
    repeat: str


class Patchable(Creatable):
    old: str
