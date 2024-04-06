from __future__ import annotations
import typing
import pydantic


class Meta(type(pydantic.BaseModel), type(typing.Protocol)): ...


class BaseProtocol(typing.Protocol):
    base: str


T = typing.TypeVar("T", bound="BaseModel")


class BaseModel(pydantic.BaseModel, BaseProtocol, metaclass=Meta):
    @classmethod
    def from_object(cls: typing.Type[T], object: BaseProtocol) -> T:
        keys = (key for key in dir(object) if not key.startswith("_"))
        return cls(**{key: value for key in keys if (value := getattr(object, key))})


class FooProtocol(BaseProtocol):
    foo: str


class FooModel(BaseModel, FooProtocol): ...


class Foo:
    value: str


class Bar:
    value: str


def work(object: typing.Protocol[Foo]) -> str:
    return object.value


work(Bar())

if __name__ == "__main__":
    # first = FooModel(foo="foo", base="base")
    # other = FooModel.from_object(first)
    # result = first.dict()
    # print(result)
    custom = Custom("foo")
    print(custom)
