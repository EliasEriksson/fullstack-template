from typing import *

from msgspec import Struct
from database.page import Page
from uuid import UUID
from datetime import datetime

T = TypeVar("T")


class Base(Struct):
    id: UUID
    created: datetime
    modified: datetime
    etag: str


class Resource(Struct, Generic[T]):
    result: T


class PagedResource(Struct, Generic[T]):
    result: list[T]
    page: Page
