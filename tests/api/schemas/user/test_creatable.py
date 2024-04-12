from api import schemas


class User:
    email: str
    password: schemas.password.creatable.CreatableProtocol | None

    def __init__(
        self, email: str, password: schemas.password.creatable.CreatableProtocol | None
    ) -> None:
        self.email = email
        self.password = password


async def test_from_object() -> None:
    user = User(
        "jessie@rocket.com",
        schemas.password.creatable.Creatable(password="password", repeat="password"),
    )
    assert user.password is not None
    assert isinstance(
        schemas.user.creatable.Creatable.from_object(user),
        schemas.user.creatable.Creatable,
    )
    user = User("jessie@rocket.com", None)
    print(user.email, user.password)
    assert isinstance(
        schemas.user.creatable.Creatable.from_object(user),
        schemas.user.creatable.Creatable,
    )
