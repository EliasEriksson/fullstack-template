from __future__ import annotations
from typing import *
from ..model import Model
from .. import password
from pydantic import Field


class PatchableProtocol(Protocol):
    email: str | None
    password: password.PatchableProtocol | None


class Patchable(Model):
    email: str | None
    password: Annotated[password.Patchable | None, Field(default=None)]
