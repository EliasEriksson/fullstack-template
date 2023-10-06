from __future__ import annotations
from typing import *
from litestar.connection import ASGIConnection
from litestar.handlers import BaseRouteHandler
from litestar.exceptions import ClientException


class RequiredHeaderException(ClientException):
    status_code = 400


def if_match(
    connection: ASGIConnection[Any, Any, Any, Any], _: BaseRouteHandler
) -> None:
    if not connection.headers.get("If-Match"):
        raise RequiredHeaderException(f"'If-Match' header is required for this route.")
