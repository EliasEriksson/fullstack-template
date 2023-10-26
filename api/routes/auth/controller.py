from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import post
from litestar import get
from litestar import patch
from litestar import delete
from litestar import Response
from litestar import Request
from litestar.exceptions import ClientException
from litestar.datastructures import State
from litestar.middleware.base import DefineMiddleware
from database import Database
from database import models
from .schemas.token import Creatable
from ...schemas import Resource
from .schemas.user import Patchable
from api.routes.auth.schemas.token import Token
from .middlewares import BasicUsernamePasswordAuthentication
from .middlewares import BearerJwtAuthentication
from .middlewares import BasicUsernamePasswordVerificationAuthentication


bearer = DefineMiddleware(BearerJwtAuthentication)
basic = DefineMiddleware(BasicUsernamePasswordAuthentication)


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
    ) -> Response[None]:
        async with Database() as session:
            async with session.transaction():
                created = await data.create(session)
        for email in created.emails:
            print(f"email to {email.address}: verification: {email.verification.code}")
        return Response(status_code=204, content=None)

    @get(
        path="/{verification:uuid}",
        middleware=[DefineMiddleware(BasicUsernamePasswordVerificationAuthentication)],
    )
    async def verify(
        self,
        request: Request[models.User, models.Email, State],
    ) -> Response[Resource[str]]:
        refresh_token = request.state.pop(
            BasicUsernamePasswordVerificationAuthentication.Scope.State.refresh_token
        )
        result = Token.encode_model(request.user, request.base_url, refresh_token)
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
        request: Request[models.User, None, State],
    ) -> Response[Resource[str]]:
        refresh_token = request.state.pop(
            BasicUsernamePasswordAuthentication.Scope.State.refresh_token
        )
        result = Token.encode_model(request.user, request.base_url, refresh_token)
        return Response(
            Resource(result),
        )

    @patch(
        path="/",
        middleware=[bearer],
    )
    async def patch(
        self,
        request: Request[models.User, Token, State],
        data: Patchable,
    ) -> Response[Resource[str]]:
        async with Database() as session:
            patched = await data.patch(session, request.user)
        result = Token.encode_model(patched, request.base_url)
        return Response(
            Resource(result),
        )

    @delete(
        path="/",
        middleware=[bearer],
    )
    async def delete(
        self,
        request: Request[models.User, Token, State],
    ) -> None:
        async with Database() as session:
            async with session.transaction():
                await session.users.delete(request.user)
        return
