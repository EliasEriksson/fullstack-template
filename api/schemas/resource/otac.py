from __future__ import annotations
from typing import *
from .resource import Resource

T = TypeVar("T")


class Otac(Resource[T]):
    token: str | None

    def __init__(self, result: T, token: str | None, **kwargs) -> None:
        super().__init__(result, token=token, **kwargs)
