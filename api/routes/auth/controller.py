from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import post
from litestar import get
from litestar import patch
from litestar import delete
from litestar import Response
from litestar import Request
from litestar.middleware.base import DefineMiddleware
from litestar.exceptions import ClientException
from database import Database
from database import models
from ...schemas.user import Creatable
from ...schemas.user import Patchable
from ...schemas import Resource
from ...schemas.token import Token
from .middlewares import BasicAuthentication
from .middlewares import BearerAuthentication


bearer = DefineMiddleware(BearerAuthentication)
basic = DefineMiddleware(BasicAuthentication)


class Controller(LitestarController):
    path = "/auth"

    @post(
        path="/",
        tags=["user"],
        summary="Register user",
    )
    async def create(
        self,
        request: Request[None, None, Any],
        data: Creatable,
    ) -> Response[Resource[str]]:
        async with Database() as session:
            async with session.transaction():
                created = await session.users.create(models.User.from_creatable(data))
        result = Token.from_user(created, request.base_url, request.base_url).encode()
        return Response(
            Resource(result),
        )

    @get(
        path="/",
        tags=["authentication"],
        summary="Authenticate user",
        middleware=[basic],
    )
    async def fetch(
        self,
        request: Request[models.User, None, Any],
    ) -> Response[Resource[str]]:
        result = Token.from_user(
            request.user, request.base_url, request.base_url
        ).encode()
        return Response(
            Resource(result),
        )

    @patch(
        path="/",
        middleware=[bearer],
    )
    async def patch(
        self,
        request: Request[models.User, Token, Any],
        data: Patchable,
    ) -> Response[Resource[str]]:
        if data.password:
            if data.password.password != data.password.repeat:
                raise ClientException("Repeated password not equal to new password.")
            if not request.user.verify(data.password.old):
                raise ClientException("Password missmatch.")
        async with Database() as session:
            async with session.transaction():
                patched = await session.users.patch(request.user.patch(data))
        result = Token.from_user(patched, request.base_url, request.base_url).encode()
        return Response(
            Resource(result),
        )

    @delete(
        path="/",
        middleware=[bearer],
    )
    async def delete(
        self,
        request: Request[models.User, Token, Any],
    ) -> None:
        async with Database() as session:
            async with session.transaction():
                await session.users.delete(request.user)
        return
