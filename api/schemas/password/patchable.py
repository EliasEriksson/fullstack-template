from __future__ import annotations
from . import creatable


class Patchable(creatable.Creatable):
    old: str
