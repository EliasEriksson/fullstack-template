from litestar import Router
from litestar.middleware.base import DefineMiddleware
from api.middlewares.authentication import Authentication
from api.middlewares.authentication import JwtAuthentication
from . import users
from . import auth
from . import emails

router = Router(
    path="api",
    route_handlers=[users.router, auth.router, emails.router],
    middleware=[
        DefineMiddleware(
            Authentication, JwtAuthentication(), exclude=["/auth", "/emails"]
        )
    ],
)
