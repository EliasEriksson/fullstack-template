from __future__ import annotations
from typing import *
from abc import ABC
from abc import abstractmethod
from shared.dependency import Dependency


class Email(Dependency, ABC):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @abstractmethod
    def send_text(self, text: str) -> None:
        pass
