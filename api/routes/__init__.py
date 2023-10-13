from litestar import Router
from litestar.middleware.base import DefineMiddleware
from .auth.middlewares import BearerAuthentication
from . import users
from . import auth

router = Router(
    path="api",
    route_handlers=[users.router, auth.router],
    middleware=[DefineMiddleware(BearerAuthentication, exclude="/auth")],
)
