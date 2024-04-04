from __future__ import annotations
from typing import *
from msgspec import Struct
from uuid import UUID
from datetime import datetime


class BaseProtocol(Protocol):
    id: UUID
    modified: datetime
    created: datetime


class Base(Struct, BaseProtocol): ...
