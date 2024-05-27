from __future__ import annotations
from typing import *
from . import password
from pydantic import model_validator


class CreatableProtocol(password.PasswordProtocol, Protocol):
    repeat: str


class Creatable(password.Password):
    repeat: str

    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        if self.password != self.repeat:
            raise ValueError(f"Passwords does not match.")
        return self
