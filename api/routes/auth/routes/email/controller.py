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
        print("7")
        async with Database() as client:
            async with client.transaction():
                print("8")
                email = await client.emails.fetch_by_code(request.auth.token)
                print("9", email)
                code = await client.codes.create(models.Code(email=email))
                print("10", code)
            print("11")
        return Response(
            schemas.resource.Otac(
                schemas.email.Email.from_object(email),
                code.token,
            )
        )
