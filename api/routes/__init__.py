from litestar import Router
from . import users

router = Router(path="api", route_handlers=[users.Controller])
