from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import get
from litestar import post
from litestar import patch
from litestar import delete
from litestar import Response
from litestar import Request
from litestar.datastructures import ResponseHeader
from litestar.params import Parameter
from litestar.exceptions import NotFoundException
from litestar.exceptions import ClientException
from database import Database
from database import models
from uuid import UUID
from ...exceptions import ForbiddenException
from ...exceptions import PreconditionFailedException
from ...schemas import Resource
from ...schemas import PagedResource
from ...schemas.user import User
from ...schemas.user import Creatable
from ...schemas.user import Patchable
from ...schemas.token import Token
from shared import hash


class Controller(LitestarController):
    path = "/users"

    @post(
        "/",
        tags=["user"],
        summary="POST User",
    )
    async def create(
        self,
        data: Creatable,
    ) -> Response[Resource[User]]:
        async with Database() as client:
            async with client.transaction():
                created = await client.users.create(models.User.from_creatable(data))
        result = User.from_object(created)
        return Response(
            Resource(result),
            headers=[ResponseHeader(name="ETag", value=result.etag)],
        )

    @get(
        "/{id:uuid}",
        tags=["user"],
        summary="GET User",
    )
    async def fetch(
        self,
        id: UUID,
    ) -> Response[Resource[User]]:
        async with Database() as client:
            async with client.transaction():
                result = User.from_model(await client.users.fetch(id))
        if not result:
            raise NotFoundException(detail=f"No user with id: '{id}' exists.")
        return Response(
            Resource.from_object(result),
            headers=[
                ResponseHeader(
                    name="ETag",
                    value=result.etag,
                )
            ],
        )

    @get("/", tags=["user"], summary="GET Users")
    async def list(
        self,
        email: list[str] | None,
        size: Annotated[int, Parameter(gt=0)] = 10,
        page: Annotated[int, Parameter(ge=0)] = 0,
    ) -> Response[PagedResource[User]]:
        emails = [] if not email else email
        async with Database() as client:
            async with client.transaction():
                result, page = await client.users.list(emails, size, page)
        return Response(
            PagedResource(
                [User.from_object(user) for user in result],
                page,
            )
        )

    @patch(
        "/{id:uuid}",
        tags=["user"],
        summary="PATCH User",
    )
    async def patch(
        self,
        id: UUID,
        request: Request[models.User, Token, Any],
        etag: Annotated[str, Parameter(header="If-Match")],
        data: Patchable,
    ) -> Response[Resource[User]]:
        if id == request.user.id:
            raise ForbiddenException()
        if data.password and data.password.new != data.password.repeat:
            raise ClientException(f"Repeated password not equal to new password.")
        async with Database() as client:
            async with client.transaction():
                current = await client.users.fetch(id)
            if not current:
                raise NotFoundException(detail=f"No user with id: '{id}' exists.")
            if hash.etag(current.modified) != etag:
                raise PreconditionFailedException(f"This user already changed.")
            async with client.transaction():
                patched = await client.users.patch(data.patch(current))
        result = User.from_object(patched)
        return Response(
            Resource(result),
            headers=[ResponseHeader(name="ETag", value=result.etag)],
        )

    @delete(
        "/{id:uuid}",
        tags=["user"],
        summary="Delete User",
    )
    async def delete(
        self,
        id: UUID,
        request: Request[models.User, Token, Any],
    ) -> None:
        if id == request.user.id:
            raise ForbiddenException()
        async with Database() as client:
            async with client.transaction():
                current = await client.users.fetch(id)
            if not current:
                raise NotFoundException(detail=f"No user with id: '{id}' exists.")
            async with client.transaction():
                await client.users.delete(current)
        return
