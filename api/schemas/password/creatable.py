from __future__ import annotations
from .password import Password


class Creatable(Password):
    repeat: str
