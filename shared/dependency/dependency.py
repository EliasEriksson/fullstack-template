from __future__ import annotations
from typing import *
from abc import ABC
from abc import abstractmethod
from .exceptions import DependencyNotFoundError


class Dependency(ABC):
    _registry: dict[str, Type[Dependency]]

    def __init_subclass__(cls) -> None:
        cls._registry = {}
        cls.__init_subclass__ = classmethod(
            lambda cls: cls._registry.update({cls.name(): cls})
        )

    @classmethod
    def create(cls, name: str) -> Dependency:
        try:
            return cls._registry[name]()
        except KeyError as error:
            raise DependencyNotFoundError(
                f"No dependency with name: {name} exits registered under {cls.__name__}"
            ) from error

    @classmethod
    @abstractmethod
    def name(cls) -> str: ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
