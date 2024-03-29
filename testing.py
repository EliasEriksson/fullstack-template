from __future__ import annotations
from typing import *


class Interface(Protocol):
    foo: str

    def method(self) -> str: ...


class Implementation(Interface):
    def __init__(self, foo: str) -> None:
        self.foo = foo


if __name__ == "__main__":
    instance = Implementation("hello world")
    print(instance.method())
