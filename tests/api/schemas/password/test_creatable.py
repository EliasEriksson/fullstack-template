from api.schemas import password as schemas


class Password:
    password: str
    repeat: str

    def __init__(self, password: str, repeat: str) -> None:
        self.password = password
        self.repeat = repeat


# TODO: add tests for the schema methods
