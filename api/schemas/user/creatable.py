from __future__ import annotations
from typing import *
from ..model import Model
from .. import password


class CreatableProtocol(Protocol):
    email: str
    password: password.CreatableProtocol | None


class Creatable(Model, CreatableProtocol):
    password: password.Creatable | None
