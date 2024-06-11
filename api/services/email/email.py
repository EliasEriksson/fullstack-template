from __future__ import annotations
from typing import *
from abc import ABC
from api.configuration import Configuration
from abc import abstractmethod
from shared.dependency.exceptions import DependencyNotFoundError


class Email(ABC):
    _registry: dict[str, Type[Email]] = {}

    @classmethod
    @abstractmethod
    def name(cls) -> str: ...

    @abstractmethod
    async def send_text(self, recipient: str, subject: str, text: str) -> None: ...

    def __init_subclass__(cls) -> None:
        cls._registry.update({cls.name(): cls})

    def __new__(cls, *args, **kwargs) -> Email:
        configuration = Configuration()
        try:
            return super().__new__(cls._registry[configuration.email.provider])
        except KeyError as error:
            raise DependencyNotFoundError(
                f"Email service provider: {configuration.email.provider} does not exist. "
                f"Available providers: {', '.join(cls._registry.keys())}."
            ) from error

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
