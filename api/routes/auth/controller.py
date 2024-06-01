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
from sqlalchemy.exc import IntegrityError
from ... import schemas
from ...middlewares.authentication import BasicAuthentication
from ...middlewares.authentication import JwtTokenAuthentication
from services.email import Email


bearer = DefineMiddleware(JwtTokenAuthentication)
basic = DefineMiddleware(BasicAuthentication)


class Controller(LitestarController):
    path = "/auth"

    @get(path="/test")
    async def test(
        self,
        agent: Annotated[str, Parameter(header="User-Agent")],
    ) -> None:
        return

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

    # @post(
    #     path="/",
    #     tags=["user"],
    #     summary="Register user.",
    # )
    # async def create(
    #     self,
    #     data: schemas.auth.Creatable,
    # ) -> None:
    #     async with Database() as client:
    #         try:
    #             async with client.transaction():
    #                 created = await client.users.create(data.create())
    #         except IntegrityError as error:
    #             raise ClientException("Email already in use.") from error
    #     mailer = Email()
    #     await asyncio.gather(
    #         *[
    #             asyncio.create_task(
    #                 mailer.send_text(f"Verification: {email.verification}")
    #             )
    #             for email in created.emails
    #         ]
    #     )

    # @patch(
    #     path="/{verification:uuid}",
    #     tags=["user"],
    #     summary="Complete registration of new user.",
    # )
    # async def patch(
    #     self,
    #     verification: UUID,
    #     data: schemas.auth.Patchable,
    # ) -> None:
    #     async with Database() as client:
    #         try:
    #             async with client.transaction():
    #                 email = await client.emails.fetch_by_verification(verification)
    #                 if not email:
    #                     raise ClientException(
    #                         f"Verification {verification} does not exist."
    #                     )
    #                 email.verified = True
    #                 data.patch(email.user)
    #         except IntegrityError as error:
    #             raise ClientException() from error

    # @get(
    #     path="/",
    #     tags=["authentication"],
    #     summary="Authenticate user",
    #     middleware=[basic],
    # )
    # async def fetch(
    #     self,
    #     request: Request[models.User, None, Any],
    # ) -> Response[schemas.Resource[str]]:
    #     result = Token.from_user(
    #         request.user, request.base_url, request.base_url
    #     ).encode()
    #     return Response(
    #         Resource(result),
    #     )

    # @patch(
    #     path="/",
    #     middleware=[bearer],
    # )
    # async def patch(
    #     self,
    #     request: Request[models.User, Token, Any],
    #     data: Patchable,
    # ) -> Response[Resource[str]]:
    #     if data.password:
    #         if data.password.password != data.password.repeat:
    #             raise ClientException("Repeated password not equal to new password.")
    #         if not request.user.verify(data.password.old):
    #             raise ClientException("Password missmatch.")
    #     async with Database() as client:
    #         async with client.transaction():
    #             patched = await client.users.patch(request.user.patch(data))
    #     result = Token.from_user(patched, request.base_url, request.base_url).encode()
    #     return Response(
    #         Resource(result),
    #     )

    # @delete(
    #     path="/",
    #     middleware=[bearer],
    # )
    # async def delete(
    #     self,
    #     request: Request[models.User, Token, Any],
    # ) -> None:
    #     async with Database() as client:
    #         async with client.transaction():
    #             await client.users.delete(request.user)
    #     return
