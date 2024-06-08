from api.schemas import password as schemas


class Password:
    old: str
    password: str
    repeat: str

    def __init__(self, old: str, password: str, repeat: str) -> None:
        self.old = old
        self.password = password
        self.repeat = repeat


async def test_from_object() -> None:
    password = Password("old", "password", "password")
    assert isinstance(
        schemas.patchable.Settable.from_object(password), schemas.patchable.Settable
    )
