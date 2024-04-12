from __future__ import annotations
from typing import *
from .model import Model

T = TypeVar("T")


class ResourceProtocol(Protocol[T]):
    result: T


class Resource(Model, Generic[T]):
    result: T

    def __init__(self, resource: T) -> None:
        super().__init__(result=resource)
