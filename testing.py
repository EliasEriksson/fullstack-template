from __future__ import annotations
from typing import *
from abc import ABC
from configuration import Configuration
from abc import abstractmethod
from shared.dependency.exceptions import DependencyNotFoundError


class Email(ABC):
    _registry: dict[str, Type[Email]] = {}

    def __init_subclass__(cls) -> None:
        print("initializing subclass", cls)
        cls._registry.update({cls.name(): cls})

    def __new__(cls, *args, **kwargs) -> Email:
        print("new with class", cls.__name__)
        configuration = Configuration()
        try:
            return super().__new__(cls._registry[configuration.email.provider])
        except KeyError as error:
            raise DependencyNotFoundError(
                f"Email service provider: {configuration.email.provider} does not exist. "
                f"Available providers: {', '.join(cls._registry.keys())}."
            ) from error

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        ...

    @abstractmethod
    async def send_text(self, text: str) -> None:
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Local(Email):
    value: int

    def __init__(self, value: int) -> None:
        self.value = value

    @classmethod
    def name(cls) -> str:
        return "local"

    async def send_text(self, text: str) -> None:
        print(text)


service = Email(123)
print(service.value)
