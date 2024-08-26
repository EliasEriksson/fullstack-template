from litestar import Router
from . import password
from ..controller import Controller

router = Router(
    path=Controller.path,
    route_handlers=[password.router],
    middleware=[],
)
