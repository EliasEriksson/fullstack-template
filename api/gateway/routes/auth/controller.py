from __future__ import annotations
from typing import *
import asyncio
from litestar import Controller as LitestarController
from litestar import post
from litestar import get
from litestar import Request
from litestar.params import Parameter
from litestar.middleware.base import DefineMiddleware
from litestar.exceptions import ClientException
from litestar.exceptions import NotAuthorizedException
from api.database import Database
from api.database import models
from sqlalchemy.exc import IntegrityError
from api import schemas
from api.gateway.middlewares.authentication import Authentication
from api.gateway.middlewares.authentication import PasswordAuthentication
from api.gateway.middlewares.authentication import OtacAuthentication
from api.gateway.middlewares.authentication import JwtAuthentication
from api.headers import Headers
from api.services.email import Email

authentication = DefineMiddleware(
    Authentication,
    JwtAuthentication(secure=False),
    PasswordAuthentication(),
    OtacAuthentication(),
)


class Controller(LitestarController):
    path = "/auth"

    @get(
        "/test",
        middleware=[authentication],
    )
    async def test(self) -> None:
        return None

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
            except IntegrityError:
                async with client.transaction():
                    email = await client.emails.fetch_by_address(data.email)
                    if email.code:
                        await client.codes.update(
                            email.code.regenerate(reset_password=False)
                        )
                    else:
                        await client.codes.create(
                            models.Code(email=email, reset_password=False)
                        )
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
        middleware=[authentication],
    )
    async def fetch(
        self,
        request: Request[
            models.User, schemas.Token | models.Password | models.Code, Any
        ],
        agent: Annotated[str, Parameter(header=Headers.user_agent)],
    ) -> schemas.Resource[str]:
        async with Database() as client:
            if isinstance(request.auth, schemas.Token):
                async with client.transaction():
                    session = await client.sessions.fetch_by_id(request.auth.session)
                    email = request.auth.subject
                if not session:
                    raise ClientException()
            elif isinstance(request.auth, (models.Email, models.Code)):
                # TODO the password is not properly deleted if PW reset OTAC is used.
                async with client.transaction():
                    session = await client.sessions.create(
                        models.Session(
                            host=request.client.host, agent=agent, user=request.user
                        ),
                        refresh=True,
                    )
                email = (
                    request.auth.id
                    if isinstance(request.auth, models.Email)
                    else request.auth.email.id
                )
            else:
                # TODO: add www-authenticate header.
                raise NotAuthorizedException()
            result = schemas.Token.create(
                session, email, request.url.hostname, request.url.hostname
            )
            return schemas.Resource(
                result.encode(),
            )
