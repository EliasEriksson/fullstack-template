from __future__ import annotations
from typing import *
from pydantic import model_validator
from . import password
from ...database import models


class Creatable(password.Password):
    repeat: str

    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        if self.password != self.repeat:
            raise ValueError(f"Passwords does not match.")
        return self

    def to_model(self) -> models.Password:
        return models.Password(digest=models.Password.hash(self.password))
