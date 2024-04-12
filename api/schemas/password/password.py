from __future__ import annotations
from typing import *
from ..model import Model


class PasswordProtocol(Protocol):
    password: str


class Password(Model):
    password: str
