from typing import *


class Meta(type):
    def __iter__(cls) -> Iterable[str]:
        return (key for key in dir(cls) if not key.startswith("_"))

    def __getitem__(cls, item) -> Any:
        return getattr(cls, item)


class Iterable(metaclass=Meta):
    def __iter__(self) -> Iterable[str]:
        return (key for key in dir(self) if not key.startswith("_"))

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)
