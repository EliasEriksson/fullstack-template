from __future__ import annotations
from msgspec import Struct
from database import models


class Password(Struct):
    new: str

    def create_hash(self) -> bytes:
        return models.User.create_hash(self.new)


class Creatable(Password):
    repeat: str


class Patchable(Creatable):
    old: str
