from typing import *
import msgspec
from database.page import Page

T = TypeVar("T")


class Response(Generic[T], msgspec.Struct):
    result: T


class PagedResponse(Generic[T], msgspec.Struct):
    result: list[T]
    page: Page
