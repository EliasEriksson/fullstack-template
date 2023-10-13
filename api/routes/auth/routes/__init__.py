from litestar import Router
from litestar.middleware.base import DefineMiddleware
from . import refresh
from ..middlewares import BearerAuthentication

router = Router(
    path="",
    route_handlers=[refresh.router],
    middleware=[DefineMiddleware(BearerAuthentication)],
)
