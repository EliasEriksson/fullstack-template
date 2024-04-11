from uuid import UUID, uuid4
from datetime import datetime
from api.schemas import user as schemas


class User:
    id: UUID
    email: str
    created: datetime
    modified: datetime

    def __init__(
        self, id: UUID, email: str, created: datetime, modified: datetime
    ) -> None:
        self.id = id
        self.email = email
        self.created = created
        self.modified = modified


async def test_from_object(now: datetime, soon: datetime) -> None:
    user = User(uuid4(), "jessie@rocket.com", now, soon)
    assert isinstance(schemas.User.from_object(user), schemas.User)
