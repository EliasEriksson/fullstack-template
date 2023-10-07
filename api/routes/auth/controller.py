from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import post
from litestar import get
from litestar import Response
from litestar import Request
from litestar.middleware.base import DefineMiddleware
from litestar.datastructures import ResponseHeader
from database import Database
from database import models
from api.routes.users.schemas import Creatable
from api.routes.users.schemas import User
from api.schemas import Resource
from ...schemas import Token
from ...middleware import BasicAuthentication


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
        data: Creatable,
    ) -> Response[Resource[str]]:
        async with Database() as session:
            async with session.transaction():
                created = await session.users.create(Creatable.create(data))
        result = Token.from_model(created).encode()
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
    ) -> Response[Resource[Token]]:
        result = Token.from_model(request.user).encode()
        return Response(Resource(result))