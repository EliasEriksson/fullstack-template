from __future__ import annotations
from typing import *
from . import creatable


class PatchableProtocol(creatable.Protocol, Protocol):
    old: str


class Patchable(creatable.Creatable, PatchableProtocol): ...
