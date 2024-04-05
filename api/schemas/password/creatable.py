from __future__ import annotations
from . import password


class CreatableProtocol(password.Protocol):
    repeat: str


class Creatable(password.Password):
    repeat: str
