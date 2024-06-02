from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import Request
from litestar import Response
from litestar import post
from ..... import schemas
from ..... import middlewares


class Controller(LitestarController):
    path = "/password"
