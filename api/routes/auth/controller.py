from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import post
from litestar import get
from litestar import Response
from litestar import Request
from litestar.middleware.base import DefineMiddleware
from database import Database
from database import models
from ..users.schemas import Creatable
from ...schemas import Resource
from .schemas import Token
from .middlewares import BasicAuthentication


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
        request: Request,
        data: Creatable,
    ) -> Response[Resource[str]]:
        print(request.url)
        async with Database() as session:
            async with session.transaction():
                created = await session.users.create(Creatable.create(data))
        result = Token.encode_model(created, "asd")
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
        result = Token.encode_model(request.user, str(request.base_url))
        return Response(Resource(result))
