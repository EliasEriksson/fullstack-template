from __future__ import annotations
from typing import *
from litestar.connection import ASGIConnection
from litestar.handlers import BaseRouteHandler
from litestar.exceptions import ClientException


class RequiredHeaderException(ClientException):
    status_code = 400

    def __init__(self, header: str, **kwargs) -> None:
        super().__init__(
            detail=f"'{header}' header is required for this route.", **kwargs
        )


def if_match(
    connection: ASGIConnection[Any, Any, Any, Any], _: BaseRouteHandler
) -> None:
    if not connection.headers.get("If-Match"):
        raise RequiredHeaderException("If-Match")
