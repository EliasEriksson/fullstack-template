# from __future__ import annotations
# from typing import *
# from litestar import Controller as LitestarController
# from litestar import Request
# from litestar import Response
# from litestar import get
# from api.schemas.token import Token
# from .....schemas import Resource
# from database import models
#
#
# class Controller(LitestarController):
#     path = "/refresh"
#
#     @get("/")
#     async def fetch(
#         self,
#         request: Request[models.User, Token, Any],
#     ) -> Response[Resource[str]]:
#         result = Token.from_user(
#             request.user, request.base_url, request.base_url
#         ).encode()
#         return Response(Resource(result))
