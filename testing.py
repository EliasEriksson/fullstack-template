from __future__ import annotations
from abc import ABC, abstractmethod
from typing import *


class NoNameError(Exception):
    ...


class Name(Protocol):
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        ...


class Dependency(ABC, Name):
    _factories: dict[str, Type[Dependency]] = {}

    def __init_subclass__(cls) -> None:
        cls.__init_subclass__ = classmethod(
            lambda factory: cls._factories.update({factory.name(): factory})
        )

    @classmethod
    def create(cls, name: str) -> Dependency | None:
        factory = cls._factories.get(name)
        return factory and factory()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Email(Dependency, ABC):
    pass


class Local(Email):
    @classmethod
    def name(cls) -> str:
        return "local"


print(Email.create("local"))
