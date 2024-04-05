from __future__ import annotations
from . import password


class Creatable(password.Password):
    repeat: str
