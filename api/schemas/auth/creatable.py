from __future__ import annotations
from typing import *
from ..model import Model
from database import models


class CreatableProtocol(Protocol):
    email: str


class Creatable(Model):
    email: str

    def create(self) -> models.User:
        user = models.User()
        models.Email(
            address=self.email,
            user=user,
        )
        return user
