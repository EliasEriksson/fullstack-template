from typing import *
import msgspec

T = TypeVar("T")


class Response(Generic[T], msgspec.Struct):
    result: T
