from __future__ import annotations
from typing import *
from ..model import Model
from database import models
from datetime import datetime
from datetime import timedelta


class CreatableProtocol(Protocol):
    email: str


class Creatable(Model):
    # TODO support email array
    email: str

    def create(self) -> models.User:
        user = models.User()
        models.Email(
            address=self.email,
            user=user,
        )
        return user
