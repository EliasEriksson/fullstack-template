from __future__ import annotations
from typing import *
from .model import Model
from dataclasses import dataclass
from math import ceil

T = TypeVar("T")


@dataclass
class Page:
    size: int
    current: int
    next: int | None
    previous: int | None
    last: int

    def __init__(self, size: int, current: int, count: int) -> None:
        self.size = size
        self.current = current
        self.last = max(0, ceil(count / size) - 1)
        self.next = (max(current + 1, 0)) if (current + 1) * size < count else None
        self.previous = min(current - 1, self.last) if current != 0 else None


class PageResourceProtocol(Protocol[T]):
    result: list[T]
    page: Page


class PagedResource(Model, PageResourceProtocol[T]):
    def __init__(self, resources: list[T], page: Page) -> None:
        super().__init__(result=resources, page=page)
