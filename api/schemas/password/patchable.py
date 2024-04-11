from __future__ import annotations
from typing import *
from . import creatable


class PatchableProtocol(creatable.CreatableProtocol, Protocol):
    old: str


class Patchable(creatable.Creatable):
    old: str
