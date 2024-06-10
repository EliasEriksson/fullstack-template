from msgspec import Struct


class Schema(Struct):
    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None: ...
