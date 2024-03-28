from __future__ import annotations
from typing import *
from msgspec import Struct

T = TypeVar("T")


class PagedResource(Struct, Generic[T]):
    result: list[T]
