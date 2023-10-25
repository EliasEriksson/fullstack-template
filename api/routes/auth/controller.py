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
from .schemas.token import Creatable
from .schemas.token import Patchable
from ...schemas import Resource
from api.routes.auth.schemas.token import Token
from .middlewares import BasicUsernamePasswordAuthentication
from .middlewares import BearerAuthentication
from .middlewares import BasicUsernamePasswordUnverifiedAuthentication


bearer = DefineMiddleware(BearerAuthentication)
basic_verified = DefineMiddleware(BasicUsernamePasswordAuthentication)
basic_unverified = DefineMiddleware(BasicUsernamePasswordUnverifiedAuthentication)


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
                created = await session.users.create(Creatable.create(data))
        for email in created.emails:
            print(f"email to {email.address}: verification: {email.verification.code}")
        return Response(status_code=204, content=None)

    @get(
        path="/",
        tags=["authentication"],
        summary="Authenticate user",
        middleware=[basic_verified],
    )
    async def fetch(
        self,
        request: Request[models.User, None, Any],
    ) -> Response[Resource[str]]:
        result = Token.encode_model(request.user, request.base_url)
        return Response(
            Resource(result),
        )

    @get(
        path="/{verification:uuid}",
        middleware=[basic_unverified],
    )
    async def verify(
        self,
        request: Request[models.User, models.Email, Any],
        agent: Annotated[str, Parameter(header="User-Agent")],
    ) -> Response[Resource[Token]]:
        async with Database() as session:
            async with session.transaction():
                refresh_token = models.Session.generate_token()
                user_session = models.Session(
                    user=request.user,
                    hash=models.Session.create_hash(refresh_token),
                    host=request.client.host,
                    agent=agent,
                )
                request.auth.verification.completed = True
                await session.sessions.create(user_session)
                await session.emails.create(request.auth)
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
        request: Request[models.User, Token, Any],
        data: Patchable,
    ) -> Response[Resource[str]]:
        if data.password:
            if data.password.new != data.password.repeat:
                raise ClientException("Repeated password not equal to new password.")
            if not request.user.verify(data.password.old):
                raise ClientException("Password missmatch.")
        async with Database() as session:
            async with session.transaction():
                patched = await session.users.patch(data.patch(request.user))
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
        request: Request[models.User, Token, Any],
    ) -> None:
        async with Database() as session:
            async with session.transaction():
                await session.users.delete(request.user)
        return
