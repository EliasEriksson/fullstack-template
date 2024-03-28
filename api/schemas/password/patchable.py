from __future__ import annotations
from .creatable import Creatable


class Patchable(Creatable):
    old: str
