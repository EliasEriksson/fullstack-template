from __future__ import annotations
from typing import *
from api.schemas.model import Model

T = TypeVar("T")


class ResourceProtocol(Protocol[T]):
    result: T


class Resource(Model, Generic[T]):
    result: T

    def __init__(self, resource: T, **kwargs) -> None:
        super().__init__(result=resource, **kwargs)

    def model_dump(self, **kwargs) -> dict[str, Any]:
        return super().model_dump(**kwargs, exclude_none=True)
