from __future__ import annotations
from typing import *
from ..schema import Schema


T = TypeVar("T")


class List(Schema, Generic[T]):
    result: list[T]
    size: int
    current: int
    next: int | None
    previous: int | None
    last: int
