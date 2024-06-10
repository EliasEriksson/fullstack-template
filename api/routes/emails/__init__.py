from litestar import Router

from .controller import Controller

router = Router(
    path="",
    route_handlers=[Controller],
)
