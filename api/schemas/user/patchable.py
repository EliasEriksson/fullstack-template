from __future__ import annotations
from typing import *
from ..model import Model
from .. import password


class PatchableProtocol(Protocol):
    email: str | None
    password: password.PatchableProtocol | None


class Patchable(Model, PatchableProtocol):
    password: password.Patchable | None
