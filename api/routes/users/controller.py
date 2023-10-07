from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import get
from litestar import post
from litestar import patch
from litestar import delete
from litestar import Response
from litestar.datastructures import Headers
from litestar.datastructures import ResponseHeader
from litestar.params import Parameter
from litestar.exceptions import NotFoundException
from litestar.exceptions import ClientException
from database import Database
from uuid import UUID
from ...exceptions import ForbiddenException
from ...exceptions import PreconditionFailedException
from ...schemas import Resource
from ...schemas import PagedResource
from ...guards import if_match
from .schemas import User
from .schemas import Creatable
from .schemas import Patchable
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
        async with Database() as session:
            async with session.transaction():
                created = await session.users.create(Creatable.create(data))
        result = User.from_model(created)
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
        async with Database() as session:
            async with session.transaction():
                result = User.from_model(await session.users.fetch(id))
        if not result:
            raise NotFoundException(detail=f"No user with id: '{id}' exists.")
        return Response(
            Resource(result),
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
        async with Database() as session:
            async with session.transaction():
                result, page = await session.users.list(emails, size, page)
        return Response(
            PagedResource(
                [User.from_model(user) for user in result],
                page,
            )
        )

    @patch(
        "/{id:uuid}",
        guards=[if_match],
        tags=["user"],
        summary="PATCH User",
    )
    async def patch(
        self,
        headers: Headers,
        id: UUID,
        data: Patchable,
    ) -> Response[Resource[User]]:
        if data.password.new != data.password.repeat:
            raise ClientException("Passwords are not matching.")
        etag = headers.get("If-match")
        async with Database() as session:
            async with session.transaction():
                current = await session.users.fetch(id)
            if not current:
                raise NotFoundException(detail=f"No user with id: '{id}' exists.")
            if not current.verify(data.password.old):
                raise ForbiddenException()
            if hash(current.modified) != etag:
                raise PreconditionFailedException(f"This user already changed.")
            async with session.transaction():
                patched = await session.users.patch(Patchable.patch(current, data))
        result = User.from_model(patched)
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
    ) -> None:
        async with Database() as session:
            async with session.transaction():
                current = await session.users.fetch(id)
            if not current:
                raise NotFoundException(detail=f"No user with id: '{id}' exists.")
            async with session.transaction():
                await session.users.delete(current)
