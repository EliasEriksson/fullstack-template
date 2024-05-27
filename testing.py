from typing import *

from typing_extensions import Self

from pydantic import BaseModel, ValidationError, model_validator


class UserModel(BaseModel):
    username: str
    password1: str
    password2: str | None

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password1 != self.password2:
            raise ValueError("passwords do not match")
        return self


print(UserModel(username="scolvin", password1=None))
