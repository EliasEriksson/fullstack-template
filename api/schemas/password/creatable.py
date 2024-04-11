from __future__ import annotations
from typing import *
from . import password


class CreatableProtocol(password.PasswordProtocol, Protocol):
    repeat: str


class Creatable(password.Password):
    repeat: str
