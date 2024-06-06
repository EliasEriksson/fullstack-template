from __future__ import annotations
from typing import *
from uuid import UUID
from litestar import Controller as LitestarController
from litestar.middleware import DefineMiddleware
from litestar import Request
from litestar import Response
from litestar import get
from litestar.exceptions import NotFoundException
from api.middlewares.authentication import Authentication
from api.middlewares.authentication import JwtAuthentication
from api import schemas
from api.exceptions import ForbiddenException
from database import Database
from database import models


class Controller(LitestarController):
    path = "/emails"

    @get(
        path="/{id:uuid}",
        tags=["email"],
        middleware=[DefineMiddleware(Authentication, JwtAuthentication(secure=False))],
    )
    async def fetch(
        self,
        request: Request[models.User, schemas.Token, Any],
        id: UUID,
    ) -> Response[schemas.Resource[schemas.Email]]:
        if id != request.auth.email:
            raise ForbiddenException(
                f"Your user might not have a password yet. Create a password, reauthenticate and try again."
            )
        async with Database() as client:
            async with client.transaction():
                email = await client.emails.fetch_by_id(request.auth.email)
            if not email:
                raise NotFoundException()
            return Response(
                schemas.Resource(
                    schemas.Email.from_object(email),
                )
            )
