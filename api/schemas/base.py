from __future__ import annotations
from typing import *
from .model import Model
from uuid import UUID
from datetime import datetime


class BaseProtocol(Protocol):
    id: UUID
    modified: datetime
    created: datetime


class Base(Model, BaseProtocol):
    def __init__(self, base: BaseProtocol) -> None:
        super().__init__()
        self.id = base.id
        self.created = base.created
        self.modified = base.modified
