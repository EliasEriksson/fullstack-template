from __future__ import annotations
from typing import *
from msgspec import Struct
from shared import hash


class PasswordProtocol(Protocol):
    password: str


class Password(Struct):
    password: str

    def hash(self) -> bytes:
        return hash.password(self.password)
