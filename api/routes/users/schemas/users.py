from __future__ import annotations
from api.schemas import Base
from database import models
from database import Session
from msgspec import Struct
from msgspec import field
from shared import hash
from datetime import datetime
from ...auth.schemas import password


class Creatable(Struct):
    emails: list[str]
    password: password.Creatable

    async def create(self, session: Session) -> models.User:
        return await session.users.create(
            self.password.create_hash(),
            emails=[
                await session.emails.create(
                    address, verification=await session.verifications.create()
                )
                for address in self.emails
            ],
        )


class User(Base):
    emails: list[str]

    @classmethod
    def from_model(cls, user: models.User) -> User:
        return cls(
            id=user.id,
            created=user.created,
            modified=user.modified,
            emails=[email.address for email in user.emails],
            etag=hash.etag(user.modified),
        )


class Patchable(Struct):
    # broken
    email: str | None = field(default=None)
    password: password.Creatable | None = field(default=None)

    def patch(self, user: models.User) -> models.User:
        # database session.merge?
        if self.email is not None:
            user.emails = self.email
        if self.password and self.password.new:
            user.hash = self.password.create_hash()
        user.modified = datetime.now()
        return user
