from typing import *


class Meta(type):
    def __iter__(cls) -> Iterable[Tuple[str, Any]]:
        return (
            (key, getattr(cls, key)) for key in cls.__dict__ if not key.startswith("_")
        )


class Iterable(metaclass=Meta):
    def __iter__(self) -> Iterable[Tuple[str, Any]]:
        return (
            (key, getattr(self, key)) for key in dir(self) if not key.startswith("_")
        )
