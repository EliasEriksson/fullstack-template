from __future__ import annotations
from abc import ABC, ABCMeta
from abc import abstractmethod
from typing import *


class Dependency:
    _factories: dict[str, Any]

    def __init_subclass__(cls):
        print("Subclassing Dependency")
        cls._factories = {}
        cls.__init_subclass__ = classmethod(
            lambda cls: cls._factories.update({cls.name: cls})
        )

    @classmethod
    def create(cls, name: str):
        factory = cls._factories[name]
        return factory and factory()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Email(Dependency, ABC):
    pass


class Local(Email):
    name = "local"


class Temperature(Dependency, ABC):
    pass


class Smhi(Temperature):
    name = "smhi"


print(Email.create("local"))
