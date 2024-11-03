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
from sqlalchemy.exc import IntegrityError
from api.headers import Headers
from api.database import Database
from api.database import models
from api import schemas
from api.gateway.middlewares.authentication import Authentication
from api.gateway.middlewares.authentication import JwtAuthentication
from api.gateway.middlewares.authentication import IgnoreAuthentication
from api.services.email import Email


authentication = DefineMiddleware(
    Authentication,
    JwtAuthentication(),
)


class Controller(LitestarController):
    path = "/password"

    # TODO: can be created multiple times?
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
            try:
                async with client.transaction():
                    password = data.to_model()
                    password.user = request.user
                    await client.password.create(password)
                    session = await client.sessions.fetch_by_connection(
                        request.user, request.client.host, agent
                    )
            except IntegrityError as error:
                raise ClientException("Already have a password.") from error
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
                password = await client.password.fetch_by_email(request.auth.subject)
                if not password or not password.verify(data.old):
                    raise ClientException()
            async with client.transaction():
                await client.password.delete_by_user(request.user.id)
                password = data.to_model()
                password.user_id = request.user.id
                await client.password.create(password)
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
        middleware=[DefineMiddleware(IgnoreAuthentication)],
    )
    async def delete(self, data: schemas.password.Deletable) -> None:
        async with Database() as client:
            async with client.transaction():
                email = await client.emails.fetch_by_address(data.email)
            if not email:
                return None
            async with client.transaction():
                if email.code:
                    code = email.code.regenerate(reset_password=True)
                else:
                    code = await client.codes.create(
                        models.Code(email_id=email.id, reset_password=True)
                    )

            mailer = Email()
            asyncio.ensure_future(
                mailer.send_text(
                    email.address,
                    "Password reset",
                    f"Password reset OTAC: {code.token}",
                )
            )
        return None
