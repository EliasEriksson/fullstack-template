from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import get
from litestar import post
from litestar import patch
from litestar.params import Parameter
from litestar.dto import DTOData
from litestar.exceptions import NotFoundException
from litestar.exceptions import ClientException, HTTPException
from database import Database
from database import models
from . import dtos
from uuid import UUID
from api.responses import Response
from api.responses import PagedResponse
from pathlib import Path


class PreconditionFailedException(ClientException):
    status_code = 412


class Controller(LitestarController):
    path = str(Path(__file__).parent.name)

    @post(
        "/",
        dto=dtos.CreateUser,
        return_dto=dtos.User,
        tags=["user"],
        summary="POST User",
    )
    async def create(self, data: DTOData[models.User]) -> Response[models.User]:
        async with Database() as session:
            async with session.transaction():
                result = await session.users.create(data.update_instance)
        return Response(result)

    @get("/{id:uuid}", dto=dtos.User, tags=["user"], summary="GET User")
    async def fetch(self, id: UUID) -> Response[models.User]:
        async with Database() as session:
            async with session.transaction():
                result = await session.users.fetch(id)
        if not result:
            raise NotFoundException(detail=f"No user with id: '{id}' exists.")
        return Response(result)

    @get("/", dto=dtos.User, tags=["user"], summary="GET Users")
    async def list(
        self,
        size: Annotated[int, Parameter(gt=0)] = 10,
        page: Annotated[int, Parameter(ge=0)] = 0,
    ) -> PagedResponse[models.User]:
        async with Database() as session:
            async with session.transaction():
                result, page = await session.users.list(size, page)
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
        async with Database() as session:
            user = await session.users.fetch(id)
            if not user:
                raise NotFoundException(detail=f"No user with id: '{id}' exists.")
            data.update_instance(user)
            result = await session.users.patch(user)
        return Response(result)
