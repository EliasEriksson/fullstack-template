from __future__ import annotations
from typing import *
from litestar import Router
from litestar import Controller
from litestar import get, post
from database import models
from database import Database
from uuid import UUID


class Users(Controller):
    pass
    # @post("/{email:str}")
    # async def create(self, email: str) -> models.User:
    #     database = Database()
    #     return await database.users.create(email=email)

    # @get("/{id:uuid}")
    # async def fetch(self, id: UUID) -> models.User | None:
    #     print(id)
    #     return None

    @get("/")
    async def list(self) -> list[str]:
        database = Database()
        # return await database.users.list()
        return []
