from typing import *
import os


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


class Configuration(metaclass=Meta):
    _environment: dict[str, Any]

    def __init__(self, environment: dict[str, Any] | None = None) -> None:
        environment = environment if environment is not None else {}
        self._environment = {
            **environment,
            **os.environ,
        }

    def _string(self, variable: str) -> str:
        return self._get(variable)

    def _integer(self, variable: str) -> int:
        value = self._get(variable)
        try:
            return int(value)
        except ValueError:
            raise ConfigurationValueError(variable, value, "int")
        except TypeError:
            raise ConfigurationMissingVariable(variable)

    def _get(self, variable: str) -> str:
        try:
            value = self._environment[variable]
            if value is None:
                raise KeyError
            return value
        except KeyError:
            raise ConfigurationMissingVariable(variable)

    def _set(self, variable: str, value: str | int) -> None:
        self._environment[variable] = f"{value}"
        os.environ[variable] = f"{value}"
