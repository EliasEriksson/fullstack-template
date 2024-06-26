from __future__ import annotations

import asyncio
from typing import *
from litestar import Controller as LitestarController
from litestar.middleware import DefineMiddleware
from litestar.params import Parameter
from litestar import Request
from litestar import post
from litestar import put
from litestar import delete
from litestar.exceptions import ClientException
from api.headers import Headers
from api.database import Database
from api.database import models
from api.database.exceptions import IntegrityError
from api import schemas
from api.middlewares.authentication import Authentication
from api.middlewares.authentication import JwtAuthentication
from api.services.email import Email


authentication = DefineMiddleware(
    Authentication,
    JwtAuthentication(),
)


class Controller(LitestarController):
    path = "/password"

    @post(
        path="/",
        tags=["auth"],
        summary="Create password.",
        middleware=[DefineMiddleware(Authentication, JwtAuthentication(secure=False))],
    )
    async def create(
        self,
        request: Request[models.User, schemas.Token, Any],
        agent: Annotated[str, Parameter(header=Headers.user_agent)],
        data: schemas.password.Creatable,
    ) -> schemas.Resource[str]:
        async with Database() as client:
            async with client.transaction():
                try:
                    password = data.to_model()
                    password.user = request.user
                    await client.passwords.create(password)
                except IntegrityError as error:
                    raise ClientException("Already have a password.") from error
                session = await client.sessions.fetch_by_connection(
                    request.user, request.client.host, agent
                )
            async with client.transaction():
                session.refresh()
            result = schemas.Token.create(
                session,
                request.auth.subject,
                request.url.hostname,
                request.url.hostname,
            )
            return schemas.Resource(
                result.encode(),
            )

    @put(
        path="",
        tags=["auth"],
        middleware=[authentication],
    )
    async def set(
        self,
        request: Request[models.User, schemas.Token, Any],
        data: schemas.password.Settable,
    ) -> schemas.Resource[str]:
        async with Database() as client:
            async with client.transaction():
                passwords = await client.passwords.fetch_valid_passwords(request.user)
            if not next(
                (password for password in passwords if password.verify(data.old)), None
            ):
                raise ClientException()
            async with client.transaction():
                await client.passwords.invalidate_by_user(request.user.id)
                password = data.to_model()
                password.user_id = request.user.id
                await client.passwords.create(password)
                session = await client.sessions.fetch_by_id(request.auth.session)
            if not session:
                raise ClientException()
            return schemas.Resource(
                schemas.Token.create(
                    session,
                    request.auth.subject,
                    request.url.hostname,
                    request.url.hostname,
                ).encode()
            )

    @delete(
        path="",
        tags=["auth"],
        middleware=[authentication],
    )
    async def delete(
        self,
        request: Request[models.User, schemas.Token, Any],
    ) -> None:
        async with Database() as client:
            async with client.transaction():
                code = await client.codes.create(
                    models.Code(email_id=request.auth.subject)
                )
                email = await client.emails.fetch_by_id(request.auth.subject)
            mailer = Email()
            asyncio.ensure_future(
                mailer.send_text(
                    email.address,
                    "Password reset",
                    f"Password reset OTAC: {code.token}",
                )
            )
        return None
