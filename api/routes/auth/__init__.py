from litestar import Router
from .controller import Controller
from . import routes

router = Router(
    path="",
    route_handlers=[Controller, routes.router],
)
