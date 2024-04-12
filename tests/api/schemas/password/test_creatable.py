from api.schemas import password as schemas


class Password:
    password: str
    repeat: str

    def __init__(self, password: str, repeat: str) -> None:
        self.password = password
        self.repeat = repeat


def test_from_object() -> None:
    password = Password("password", "password")
    assert isinstance(
        schemas.creatable.Creatable.from_object(password), schemas.creatable.Creatable
    )
