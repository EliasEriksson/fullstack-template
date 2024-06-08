from api import schemas
from datetime import datetime
from uuid import UUID, uuid4


class User:
    id: UUID
    email: str
    password: schemas.password.patchable.PatchableProtocol | None
    created: datetime
    modified: datetime

    def __init__(
        self,
        id: UUID,
        email: str,
        password: schemas.password.patchable.PatchableProtocol | None,
        created: datetime,
        modified: datetime,
    ) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.created = created
        self.modified = modified


async def test_from_object(now: datetime, soon: datetime) -> None:
    user = User(
        uuid4(),
        "jessie@rocket.com",
        schemas.password.patchable.Settable(
            old="old", password="password", repeat="password"
        ),
        now,
        soon,
    )
    assert user.password is not None
    assert isinstance(schemas.user.Settable.from_object(user), schemas.user.Settable)
    user = User(user.id, user.email, None, now, soon)
    assert user.password is None
    assert isinstance(schemas.user.Settable.from_object(user), schemas.user.Settable)
