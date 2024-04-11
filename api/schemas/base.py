from __future__ import annotations
from typing import *
from .model import Model
from uuid import UUID
from datetime import datetime


class BaseProtocol(Protocol):
    id: UUID
    modified: datetime
    created: datetime


class Base(Model):
    id: UUID
    modified: datetime
    created: datetime
