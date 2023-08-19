from typing import *
import os


class Meta(type):
    """
    Configuration metaclass

    works similar to a singleton but the instance is overwritten if args/kwargs are given
    is this a good idea? probably not but it makes it easy to test for now
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances or args or kwargs:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigurationError(Exception):
    pass


class ConfigurationMissingVariable(ConfigurationError):
    def __init__(self, variable: str) -> None:
        super().__init__(f"Variable: '{variable}' is missing from environment.")


class ConfigurationValueError(ConfigurationError):
    def __init__(self, variable: str, value: str, expected: str) -> None:
        super().__init__(
            f"Unexpected type of environment variable: '{variable}', "
            f"received value: {value}, expected type: {expected}."
        )


class Configuration(metaclass=Meta):
    _environment: dict[str, str]

    def __init__(self, environment: Optional[dict[str, str]] = None) -> None:
        environment = environment if environment is not None else {}
        self._environment = {
            **os.environ,
            **environment,
        }

    def string(self, variable: str) -> str:
        return self.get(variable)

    def integer(self, variable: str) -> int:
        value = self.get(variable)
        try:
            return int(value)
        except ValueError:
            raise ConfigurationValueError(variable, value, "int")

    def get(self, variable: str) -> str:
        try:
            return self._environment[variable]
        except KeyError:
            raise ConfigurationMissingVariable(variable)
