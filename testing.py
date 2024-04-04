from typing import *
import msgspec
from dataclasses import dataclass

dataclass
class MyProtocol(Protocol):
    foo: str


class MyMeta(type(msgspec.Struct)):
    pass


# class MyClass(msgspec.Struct, MyProtocol, metaclass=CombinedMeta): ...


if __name__ == "__main__":
    # c = MyClass()
    # print(c)
    pass
