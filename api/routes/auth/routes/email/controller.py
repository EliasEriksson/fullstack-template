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
    ) -> Response[schemas.Resource[schemas.email.Email]]:
        return Response(
            schemas.Resource(schemas.email.Email.from_protocol(request.auth.email))
        )
