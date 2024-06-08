from __future__ import annotations
from typing import *
from pydantic import BaseModel

T = TypeVar("T")


class Schema(BaseModel): ...


class Result(Schema, Generic[T]):
    result: T


class Email(Schema):
    address: str


print(Result[Email](result={"address": "jessie@rocket.com"}).model_dump())
#####################################################################
