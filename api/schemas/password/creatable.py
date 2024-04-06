from __future__ import annotations
from . import password


class CreatableProtocol(password.PasswordProtocol):
    repeat: str


class Creatable(password.Password, CreatableProtocol): ...
