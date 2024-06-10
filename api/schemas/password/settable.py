from __future__ import annotations
from .creatable import Creatable


class Settable(Creatable):
    old: str
