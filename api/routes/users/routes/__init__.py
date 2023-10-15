from litestar import Router
from ..controller import Controller

router = Router(path=Controller.path, route_handlers=[])
