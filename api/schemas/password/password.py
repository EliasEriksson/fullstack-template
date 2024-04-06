from __future__ import annotations
from typing import *
from shared import hash

# from pydantic import BaseModel
from ..model import Model


class PasswordProtocol(Protocol):
    password: str


class Password(Model, PasswordProtocol):
    password: str
