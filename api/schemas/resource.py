from __future__ import annotations
from typing import *
from msgspec import Struct

T = TypeVar("T")


class Resource(Struct, Generic[T]):
    result: T
