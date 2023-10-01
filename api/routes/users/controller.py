from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import get
from litestar import post
from litestar import patch
from litestar.params import Parameter
from litestar.dto import DTOData
from litestar.exceptions import NotFoundException
from database import Database
from database import models
from . import dtos
from uuid import UUID
from uuid import uuid4
from api.responses import Response
from api.responses import PagedResponse
from pathlib import Path


class Controller(LitestarController):
    path = str(Path(__file__).parent.name)

    @post("/", dto=dtos.User, tags=["user"], summary="POST User")
    async def create(self) -> Response[models.User]:
        database = Database()
        result = await database.users.create(email=f"james_{uuid4()}@rocket.com")
        return Response(result)

    @get("/{id:uuid}", dto=dtos.User, tags=["user"], summary="GET User")
    async def fetch(self, id: UUID) -> Response[models.User]:
        database = Database()
        result = await database.users.fetch(id)
        if not result:
            raise NotFoundException(detail=f"No user with id: '{id}' exists.")
        return Response(result)

    @get("/", dto=dtos.User, tags=["user"], summary="GET Users")
    async def list(
        self,
        size: Annotated[int, Parameter(gt=0)] = 10,
        page: Annotated[int, Parameter(ge=0)] = 0,
    ) -> PagedResponse[models.User]:
        database = Database()
        result, page = await database.users.list(size, page)
        return PagedResponse(result, page)

    @patch(
        "/{id:uuid}",
        dto=dtos.PatchUser,
        return_dto=dtos.User,
        tags=["user"],
        summary="PATCH User",
    )
    async def patch(
        self, id: UUID, data: DTOData[models.User]
    ) -> Response[models.User]:
        database = Database()
        user = models.User(id=id)
        if not user:
            raise NotFoundException(detail=f"No user with id: '{id}' exists.")
        data.update_instance(user)
        result = await database.users.patch(user)
        return Response(result)
