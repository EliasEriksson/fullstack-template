from __future__ import annotations

from litestar import Controller as LitestarController
from litestar import get
from database import Database
from database import models
from . import dtos
import uuid
from .responses import Response


class Controller(LitestarController):
    @get("/", dto=dtos.User, tags=["user"], summary="GET User")
    async def fetch(self) -> Response[models.User]:
        database = Database()
        user = await database.users.create(email=f"james_{uuid.uuid4()}@rocket.com")
        return Response(result=user)
