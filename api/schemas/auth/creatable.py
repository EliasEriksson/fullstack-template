from __future__ import annotations
from ..schema import Schema
from database import models


class Creatable(Schema):
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
