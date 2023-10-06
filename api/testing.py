# from __future__ import annotations
from typing import *
from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi import OpenAPIController
from litestar import get
from msgspec import Struct
from dataclasses import dataclass


T = TypeVar("T")


class User(Struct):
    email: str


class NestedUser(Struct):
    result: User


class Nested(Struct, Generic[T]):
    result: T


@get("/api/user")
async def user() -> User:
    return User(email="jessie@rocket.com")


@get("/api/nested_user")
async def nested_user() -> NestedUser:
    return NestedUser(User("jessie@rocket.com"))


@get("/api/nested_generic")
async def nested_generic() -> Nested["User"]:
    return Nested(result=User(email="jessie@rocket.com"))


class DocumentationController(OpenAPIController):
    path = "/api/"


api = Litestar(
    route_handlers=[user, nested_user, nested_generic],
    openapi_config=OpenAPIConfig(
        title="Litestar template",
        version="0.0.0",
        root_schema_site="elements",
        openapi_controller=DocumentationController,
    ),
    debug=True,
)
