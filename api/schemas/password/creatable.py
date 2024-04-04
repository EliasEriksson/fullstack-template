from __future__ import annotations
from typing import Protocol
from . import password


class CreatableProtocol(password.Protocol, Protocol):
    repeat: str


class Creatable(password.Password, CreatableProtocol): ...
