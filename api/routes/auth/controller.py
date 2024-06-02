from __future__ import annotations
from typing import *
import asyncio
from uuid import UUID
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
    ) -> None:
        if isinstance(request.auth, schemas.Token):
            print("authenticated with JWT")
        elif isinstance(request.auth, models.Password):
            print("authenticated with password")
        elif isinstance(request.auth, models.Code):
            print("authenticated with OTAC")
        else:
            raise AnyAuthentication.not_authorized(request.url)
        return None
