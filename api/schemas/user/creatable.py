from __future__ import annotations
from typing import *
from ..model import Model
from .. import password
from pydantic import Field


class CreatableProtocol(Protocol):
    email: str


class Creatable(Model):
    email: str
    password: Annotated[password.Password | None, Field(None)]
