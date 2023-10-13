from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import post
from litestar import get
from litestar import patch
from litestar import Response
from litestar import Request
from litestar.middleware.base import DefineMiddleware
from litestar.exceptions import ClientException
from database import Database
from database import models
from .schemas.token import Creatable
from .schemas.token import Patchable
from ...schemas import Resource
from api.routes.auth.schemas.token import Token
from .middlewares import BasicAuthentication
from .middlewares import BearerAuthentication


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
                created = await session.users.create(Creatable.create(data))
        result = Token.encode_model(created, request.base_url)
        return Response(
            Resource(result),
        )

    @get(
        path="/",
        tags=["authentication"],
        summary="Authenticate user",
        middleware=[DefineMiddleware(BasicAuthentication)],
    )
    async def fetch(
        self,
        request: Request[models.User, None, Any],
    ) -> Response[Resource[str]]:
        result = Token.encode_model(request.user, request.base_url)
        return Response(
            Resource(result),
        )

    @patch(
        path="/",
        middleware=[DefineMiddleware(BearerAuthentication)],
    )
    async def patch(
        self,
        request: Request[models.User, Token, Any],
        data: Patchable,
    ) -> Response[Resource[str]]:
        if data.password and not request.user.verify(data.password.old):
            raise ClientException("Password missmatch.")
        async with Database() as session:
            async with session.transaction():
                patched = await session.users.patch(data.patch(request.user))
        result = Token.encode_model(patched, request.base_url)
        return Response(
            Resource(result),
        )
