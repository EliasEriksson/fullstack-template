from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import Request
from litestar import Response
from litestar import post
from database import Database
from database import models
from ..... import schemas
from ..... import middlewares


class Controller(LitestarController):
    path = "/password"

    @post(path="/", tags=["auth"], summary="Create password.")
    async def create(self, request: Request[models.User, models.Code, Any]) -> None:
        return
