from litestar import Router
from litestar.middleware.base import DefineMiddleware
from api.gateway.middlewares.authentication import Authentication
from api.gateway.middlewares.authentication import JwtAuthentication
from . import auth
from . import emails

router = Router(
    path="api",
    route_handlers=[auth.router, emails.router],
    middleware=[
        DefineMiddleware(
            Authentication, JwtAuthentication(), exclude=["/auth", "/emails"]
        )
    ],
)
