from __future__ import annotations
from typing import *
from ..model import Model
from database import models


class CreatableProtocol(Protocol):
    email: str


class Creatable(Model):
    email: str

    def create(self) -> tuple[models.User, models.Email, models.Code]:
        user = models.User()
        email = models.Email(
            address=self.email,
            user=user,
        )
        code = models.Code(
            email=email,
        )
        return user, email, code
