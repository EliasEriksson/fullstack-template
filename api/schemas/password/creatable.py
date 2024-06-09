from __future__ import annotations
from .password import Password
from ...database import models


class Creatable(Password):
    repeat: str

    def to_model(self) -> models.Password:
        return models.Password(digest=models.Password.hash(self.password))

    def validate(self) -> None:
        if self.password != self.repeat:
            raise ValueError("Passwords not matching.")
