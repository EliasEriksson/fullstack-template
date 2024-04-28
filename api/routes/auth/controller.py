from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import post
from litestar import get
from litestar import patch
from litestar import delete
from litestar import Response
from litestar import Request
from litestar.params import Parameter
from litestar.middleware.base import DefineMiddleware
from litestar.exceptions import ClientException
from database import Database
from database import models
from ... import schemas
from ...middlewares.authentication import BasicAuthentication
from ...middlewares.authentication import JwtAuthentication


bearer = DefineMiddleware(JwtAuthentication)
basic = DefineMiddleware(BasicAuthentication)


class Controller(LitestarController):
    path = "/auth"

    @post(
        path="/",
        tags=["user"],
        summary="Register user.",
    )
    async def create(
        self,
        request: Request[None, None, Any],
        agent: Annotated[str, Parameter(header="User-Agent")],
        data: schemas.user.Creatable,
    ) -> Response[schemas.resource.Resource[str]]:
        async with Database() as client:
            async with client.transaction():
                created = await client.users.create(data.create(agent))
            async with client.transaction():
                session = await client.sessions.fetch_by_agent(created, agent)
        if session is None:
            raise ClientException()
        result = schemas.token.Token.from_user(created)
        # result = schemas.token.Token.from_user(
        #     created, request.base_url, request.base_url
        # ).encode()
        return Response(
            schemas.Resource(result),
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
        async with Database() as client:
            async with client.transaction():
                patched = await client.users.patch(request.user.patch(data))
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
        async with Database() as client:
            async with client.transaction():
                await client.users.delete(request.user)
        return
