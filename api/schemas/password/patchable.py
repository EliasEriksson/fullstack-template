from __future__ import annotations
from . import creatable


class PatchableProtocol(creatable.CreatableProtocol):
    old: str


class Patchable(creatable.Creatable, PatchableProtocol): ...
