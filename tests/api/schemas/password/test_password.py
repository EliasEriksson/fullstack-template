from api.schemas import password as schemas


class Password:
    password: str

    def __init__(self, password: str) -> None:
        self.password = password


async def test_from_object() -> None:
    password = Password("password")
    assert isinstance(schemas.Password.from_object(password), schemas.Password)
