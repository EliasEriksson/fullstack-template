from __future__ import annotations
from typing import *
from ..schema import Schema

T = TypeVar("T")


class Resource(Schema, Generic[T]):
    result: T
