from __future__ import annotations
from typing import *
from database import models
from pydantic import model_validator
from ..model import Model
from .. import password


class PatchableProtocol(Protocol):
    password: password.CreatableProtocol


class Patchable(Model):
    password: password.Creatable

    def patch(self, user: models.User) -> models.User:
        models.Password(
            digest=models.Password.hash(self.password.password),
            user=user,
        )
        return user
