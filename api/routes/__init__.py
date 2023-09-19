from litestar import Router
from . import users
from pathlib import Path

router = Router(path=str(Path(__file__).parent), route_handlers=[users.Controller])
