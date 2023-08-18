from . import models
from .engine import engine


async def create() -> None:
    models.Base.metadata.create_all(engine)


def delete() -> None:
    models.Base.metadata.drop_all(engine)
