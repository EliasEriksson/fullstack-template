from __future__ import annotations
from typing import *
from uuid import UUID
from litestar import Controller as LitestarController
from litestar.middleware import DefineMiddleware
from litestar import Request
from litestar import get
from litestar.exceptions import NotFoundException
from api.gateway.middlewares.authentication import Authentication
from api.gateway.middlewares.authentication import JwtAuthentication
from api import schemas
from api.exceptions import ForbiddenException
from api.database import Database
from api.database import models


class Controller(LitestarController):
    path = "/emails"

    @get(
        path="/{id:uuid}",
        tags=["email"],
        middleware=[DefineMiddleware(Authentication, JwtAuthentication(secure=False))],
        return_dto=schemas.email.DTO,
    )
    async def fetch(
        self,
        request: Request[models.User, schemas.Token, Any],
        id: UUID,
    ) -> schemas.Resource[models.Email]:
        if id != request.auth.email:
            raise ForbiddenException(
                f"Your user might not have a password yet. Create a password, reauthenticate and try again."
            )
        async with Database() as client:
            async with client.transaction():
                email = await client.emails.fetch_by_id(request.auth.email)
            if not email:
                raise NotFoundException()
            return schemas.Resource(email)
