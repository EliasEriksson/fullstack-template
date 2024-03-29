from __future__ import annotations
from .creatable import Creatable
from ..base import Base


class User(Base, Creatable):
    pass
