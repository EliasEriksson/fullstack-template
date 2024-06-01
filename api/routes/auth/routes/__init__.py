from litestar import Router
from litestar.middleware.base import DefineMiddleware
from . import email
from . import password
from ....middlewares.authentication import JwtTokenAuthentication
from ..controller import Controller

router = Router(
    path=Controller.path,
    route_handlers=[email.router, password.router],
    middleware=[],
)
