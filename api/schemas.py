from __future__ import annotations
from typing import *
from msgspec import Struct
from database.page import Page
from datetime import datetime
from uuid import UUID

T = TypeVar("T")


class Base(Struct):
    id: UUID
    created: datetime
    modified: datetime


class Resource(Struct, Generic[T]):
    result: T


class PagedResource(Struct, Generic[T]):
    result: list[T]
    page: Page
