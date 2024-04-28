from __future__ import annotations
from abc import ABC, ABCMeta
from abc import abstractmethod
from typing import *


class Dependency:
    _key = "_factories"

    def __init_subclass__(cls):
        cls._set_or_get_factories()
        cls._factories = {}
        cls.__init_subclass__ = classmethod(
            lambda cls: cls._factories.update({cls.name: cls})
        )

    @classmethod
    def create(cls, name: str):
        factory = cls._set_or_get_factories()
        return factory and factory()

    @classmethod
    def _set_or_get_factories(cls) -> dict[str, Any]:
        factories = getattr(cls, cls._key)
        if factories is None:
            factories = {}
            setattr(cls, cls._key, factories)
        return factories

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
