from typing import *
from pydantic import BaseModel


TProtocol = TypeVar("TProtocol", bound="Protocol")
TModel = TypeVar("TModel", bound=Annotated["Model", "Protocol"])


class Model(BaseModel):
    @classmethod
    def from_object(cls: Type[TModel], object: Protocol[TModel]) -> TModel:
        """
        Attempts to create an instance of the caller from the source object.

        The source object is not properly typed and will accept anything that is an object.
        However, proper runtime errors will be thrown.
        """
        keys = (key for key in dir(object) if not key.startswith("_"))
        return cls(**{key: value for key in keys if (value := getattr(object, key))})
