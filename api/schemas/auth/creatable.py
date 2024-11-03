from __future__ import annotations
from ..schema import Schema
from ...database import models


class Creatable(Schema):
    email: str

    def create(
        self, reset_password: bool
    ) -> tuple[models.User, models.Email, models.Code]:
        user = models.User()
        email = models.Email(
            address=self.email,
            user=user,
        )
        code = models.Code(
            email=email,
            reset_password=reset_password,
        )
        return user, email, code
