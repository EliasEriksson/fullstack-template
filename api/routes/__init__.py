from litestar import Router
from litestar.middleware.base import DefineMiddleware
from ..middlewares.authentication import JwtTokenAuthentication
from . import users
from . import auth

router = Router(
    path="api",
    route_handlers=[users.router, auth.router],
    middleware=[DefineMiddleware(JwtTokenAuthentication, exclude="/auth")],
)
