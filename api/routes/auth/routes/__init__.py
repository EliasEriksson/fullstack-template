from litestar import Router
from . import refresh
from ..controller import Controller

router = Router(
    path=Controller.path,
    route_handlers=[refresh.router],
)
