import typing
from pydantic import BaseModel


TProtocol = typing.TypeVar("TProtocol", bound="Protocol")
TModel = typing.TypeVar("TModel", bound=typing.Annotated["Model", "Protocol"])


class Protocol(typing.Protocol[TProtocol]): ...


class Meta(type(BaseModel), type(typing.Protocol)): ...


class Model(BaseModel, Protocol, metaclass=Meta):
    @classmethod
    def from_object(cls: typing.Type[TModel], object: Protocol[TModel]) -> TModel:
        """
        Attempts to create an instance of the caller from the source object.

        The source object is not properly typed and will accept anything that is an object.
        However, proper runtime errors will be thrown.
        """
        keys = (key for key in dir(object) if not key.startswith("_"))
        return cls(**{key: value for key in keys if (value := getattr(object, key))})
