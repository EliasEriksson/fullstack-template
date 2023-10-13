from __future__ import annotations
from typing import *
from litestar import Controller as LitestarController
from litestar import Request
from litestar import Response
from litestar import get
from api.routes.auth.schemas.token import Token
from .....schemas import Resource
from database import models


class Controller(LitestarController):
    path = "/refresh"

    @get("/")
    async def fetch(
        self,
        request: Request[models.User, Token, Any],
    ) -> Response[Resource[str]]:
        result = Token.encode_model(request.user, request.base_url)
        return Response(Resource(result))
