from litestar import Router
from litestar.middleware.base import DefineMiddleware
from . import refresh
from ....middlewares.authentication import JwtAuthentication
from ..controller import Controller

router = Router(
    path=Controller.path,
    route_handlers=[refresh.router],
    middleware=[DefineMiddleware(JwtAuthentication)],
)
