from __future__ import annotations
from . import creatable


class Settable(creatable.Creatable):
    old: str
