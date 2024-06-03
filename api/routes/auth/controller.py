from __future__ import annotations
from typing import *
import asyncio
from uuid import UUID
from datetime import timedelta
from litestar import Controller as LitestarController
from litestar.connection import ASGIConnection
from litestar import post
from litestar import get
from litestar import patch
from litestar import Response
from litestar import Request
from litestar.params import Parameter
from litestar.middleware.base import DefineMiddleware
from litestar.exceptions import ClientException
from litestar.exceptions import InternalServerException
from database import Database
from database import models
from sqlalchemy.exc import IntegrityError
from ... import schemas
from ...middlewares.authentication import PasswordAuthentication
from ...middlewares.authentication import JwtTokenAuthentication
from ...middlewares.authentication import AnyAuthentication
from api.headers import Headers
from services.email import Email


jwt = DefineMiddleware(JwtTokenAuthentication)
password = DefineMiddleware(PasswordAuthentication)
any = DefineMiddleware(AnyAuthentication)


class Controller(LitestarController):
    path = "/auth"

    @post(
        "/",
        tags=["auth"],
        summary="Self registration.",
    )
    async def create(
        self,
        request: Request,
        data: schemas.auth.Creatable,
    ) -> None:
        async with Database() as client:
            try:
                async with client.transaction():
                    user, email, code = data.create()
                    await client.users.create(user)
            except IntegrityError as error:
                raise ClientException("Email already in use.") from error
        mailer = Email()
        asyncio.ensure_future(
            mailer.send_text(
                email.address,
                f"{request.url.hostname} email verification.",
                f"Your OTAC: {email.code.token}",
            )
        )
        return None

    @get(
        path="/",
        tags=["auth"],
        summary="Login.",
        middleware=[any],
    )
    async def fetch(
        self,
        request: Request[
            models.User, schemas.Token | models.Password | models.Code, Any
        ],
        agent: Annotated[str, Parameter(header=Headers.user_agent)],
    ) -> Response[schemas.Resource[str]]:
        async with Database() as client:
            if isinstance(request.auth, schemas.Token):
                async with client.transaction():
                    session = await client.sessions.fetch_by_id(request.auth.session)
                if session.host == request.client.host and session.agent == agent:
                    async with client.transaction():
                        session.refresh()
                else:
                    session = await client.sessions.create(
                        models.Session(
                            host=request.client.host, agent=agent, user=request.user
                        )
                    )
                result = schemas.Token.from_session(
                    session, request.url, request.url
                ).encode()
                print("authenticated with JWT")
            elif isinstance(request.auth, models.Password):
                print("authenticated with password")
                result = ""
            elif isinstance(request.auth, models.Code):
                async with client.transaction():
                    session = await client.sessions.create(
                        models.Session(
                            host=request.client.host, agent=agent, user=request.user
                        )
                    )
                result = schemas.Token.from_session(
                    session, request.url, request.url
                ).encode()
            else:
                raise AnyAuthentication.not_authorized(request.url)
        return Response(schemas.Resource(result))
