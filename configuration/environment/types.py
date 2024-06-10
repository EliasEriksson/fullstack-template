from __future__ import annotations
from typing import *

TValue = str | int | float | None
TEnvironment = dict[str, TValue]


class TVariables(Protocol):
    def __iter__(self) -> Iterable[str]: ...

    def __getitem__(self, item: str) -> TValue: ...
