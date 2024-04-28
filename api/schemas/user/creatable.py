from __future__ import annotations
from typing import *
from ..model import Model
from database import models
from datetime import datetime
from datetime import timedelta


class CreatableProtocol(Protocol):
    email: str


class Creatable(Model):
    email: str

    def create(self, agent: str, host: str) -> models.User:
        user = models.User()
        models.Email(
            address=self.email,
            user=user,
        )
        models.Session(
            expire=datetime.now() + timedelta(days=7),
            host=host,
            agent=agent,
            user=user,
        )
        return user
