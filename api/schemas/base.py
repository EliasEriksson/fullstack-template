from __future__ import annotations
from msgspec import Struct
from uuid import UUID
from datetime import datetime


class Base(Struct):
    id: UUID
    modified: datetime
    created: datetime
