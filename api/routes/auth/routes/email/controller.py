from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import Request
from litestar import Response
from litestar import get
from ..... import schemas
from ..... import middlewares
from database import Database
from database import models
from uuid import uuid4


class Controller(LitestarController):
    path = "/email"

    @get(
        path="/",
        tags=["auth"],
        summary="OTAC email.",
        middleware=[middlewares.authentication.OtacTokenAuthentication],
    )
    async def fetch(
        self, request: Request[models.User, models.Code, Any]
    ) -> Response[schemas.resource.Otac[schemas.email.Email]]:
        async with Database() as client:
            async with client.transaction():
                email = await client.emails.fetch_by_code(request.auth.token)
                code = await client.codes.create(models.Code(id=uuid4(), email=email))
        return Response(
            schemas.resource.Otac(
                schemas.email.Email.from_object(email),
                code.token,
            )
        )
